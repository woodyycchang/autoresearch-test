/**
 * A librarian's body: first-person movement with analytic collisions.
 *
 * The world is kind to walkers: floors are flat, the stair is a known helix,
 * and every wall is a segment. Ground height is computed, not raycast.
 * Mouse-look uses pointer lock; the arrow keys steer the view at a fixed,
 * deterministic rate (good for accessibility, essential for the E2E tests).
 */

import * as THREE from "three";
import * as D from "../world/dims";
import { insideHex } from "../world/dims";
import { World } from "../world/world";

const ARROW_RATE = 2.0; // rad/s, exact
const A_DOOR = Math.PI / 2; // stair door azimuth as seen from the stair axis

export type MoveMode = "walk" | "falling";

export interface ControllerEvents {
  onShiftX(dir: 1 | -1): void;
  onShiftY(dir: 1 | -1): void;
  onStartFalling(): void;
  onStep(): void;
}

export class Controller {
  readonly camera: THREE.PerspectiveCamera;
  readonly pos = new THREE.Vector3(0, 0, 0); // feet position, local
  vel = new THREE.Vector3();
  yaw = 0; // 0 looks along -z... we define 0 = looking east (+x)
  pitch = 0;
  grounded = true;
  mode: MoveMode = "walk";
  fallDistance = 0;
  enabled = false;

  private keys = new Set<string>();
  private world: World;
  private events: ControllerEvents;
  private stepAccum = 0;

  constructor(world: World, events: ControllerEvents, aspect: number) {
    this.world = world;
    this.events = events;
    this.camera = new THREE.PerspectiveCamera(72, aspect, 0.05, 120);
    this.camera.rotation.order = "YXZ";
  }

  keyDown(code: string): void {
    this.keys.add(code);
  }

  keyUp(code: string): void {
    this.keys.delete(code);
  }

  clearKeys(): void {
    this.keys.clear();
  }

  mouseLook(dx: number, dy: number): void {
    if (!this.enabled) return;
    this.yaw -= dx * 0.0023;
    this.pitch -= dy * 0.0023;
    this.clampPitch();
  }

  private clampPitch(): void {
    const lim = Math.PI / 2 - 0.02;
    this.pitch = Math.max(-lim, Math.min(lim, this.pitch));
  }

  /** Forward direction on the ground plane. yaw=0 → +x (east). */
  private forward(): { x: number; z: number } {
    return { x: Math.cos(this.yaw), z: -Math.sin(this.yaw) };
  }

  update(dt: number): void {
    if (this.mode === "falling") {
      this.updateFalling(dt);
      return;
    }
    if (!this.enabled) {
      this.syncCamera();
      return;
    }

    // Arrow-key look: fixed rate, deterministic.
    if (this.keys.has("ArrowLeft")) this.yaw += ARROW_RATE * dt;
    if (this.keys.has("ArrowRight")) this.yaw -= ARROW_RATE * dt;
    if (this.keys.has("ArrowUp")) this.pitch += ARROW_RATE * 0.7 * dt;
    if (this.keys.has("ArrowDown")) this.pitch -= ARROW_RATE * 0.7 * dt;
    this.clampPitch();

    const f = this.forward();
    const rx = -f.z; // right-hand vector
    const rz = f.x;
    let mx = 0;
    let mz = 0;
    if (this.keys.has("KeyW")) {
      mx += f.x;
      mz += f.z;
    }
    if (this.keys.has("KeyS")) {
      mx -= f.x;
      mz -= f.z;
    }
    if (this.keys.has("KeyD")) {
      mx += rx;
      mz += rz;
    }
    if (this.keys.has("KeyA")) {
      mx -= rx;
      mz -= rz;
    }
    const mlen = Math.hypot(mx, mz);
    const speed = this.keys.has("ShiftLeft") || this.keys.has("ShiftRight") ? D.HURRY_SPEED : D.WALK_SPEED;
    if (mlen > 0) {
      mx = (mx / mlen) * speed;
      mz = (mz / mlen) * speed;
    }

    // Vertical.
    if (this.grounded && this.keys.has("Space")) {
      this.vel.y = D.JUMP_V;
      this.grounded = false;
    }
    this.vel.y -= D.GRAVITY * dt;

    // Integrate horizontally, then resolve.
    this.pos.x += mx * dt;
    this.pos.z += mz * dt;
    this.collideWalls();
    this.collideStairwell();

    // Integrate vertically against the computed ground.
    this.pos.y += this.vel.y * dt;
    const ground = this.groundHeight(this.pos.x, this.pos.z, this.pos.y);
    if (ground === null) {
      // Above the abyss.
      this.grounded = false;
      if (this.pos.y < -0.6) {
        this.mode = "falling";
        this.fallDistance = 0;
        this.events.onStartFalling();
      }
    } else if (this.pos.y <= ground + 1e-6) {
      if (!this.grounded && this.vel.y < -7) this.events.onStep();
      this.pos.y = ground;
      this.vel.y = 0;
      this.grounded = true;
    } else if (this.grounded && this.pos.y - ground <= D.SNAP_DOWN && this.vel.y <= 0) {
      // Stick to descending steps.
      this.pos.y = ground;
      this.vel.y = 0;
    } else if (this.pos.y - ground > 0.002) {
      this.grounded = false;
    }

    // Ceiling.
    const ceil = this.ceilingHeight(this.pos.x, this.pos.z);
    const head = this.pos.y + 1.78;
    if (head > ceil && this.vel.y > 0) {
      this.vel.y = 0;
      this.pos.y = Math.min(this.pos.y, ceil - 1.78);
    }

    // Footsteps.
    if (this.grounded && mlen > 0) {
      this.stepAccum += speed * dt;
      if (this.stepAccum > 1.9) {
        this.stepAccum = 0;
        this.events.onStep();
      }
    }

    this.recenter();
    this.syncCamera();
  }

  private updateFalling(dt: number): void {
    // Terminal velocity; the shaft is bottomless.
    this.vel.y = Math.max(this.vel.y - D.GRAVITY * dt, -13);
    this.pos.y += this.vel.y * dt;
    this.fallDistance -= this.vel.y * dt;
    // Drift gently toward the shaft's center so the fall never snags.
    const n = Math.round(this.pos.x / D.UNIT_PITCH);
    const cx = n * D.UNIT_PITCH;
    this.pos.x += (cx - this.pos.x) * Math.min(1, dt * 2);
    this.pos.z += (0 - this.pos.z) * Math.min(1, dt * 2);
    while (this.pos.y < -D.FLOOR_PITCH / 2) {
      this.pos.y += D.FLOOR_PITCH;
      this.events.onShiftY(-1);
    }
    this.syncCamera();
  }

  /** Leave falling mode (after waking somewhere remote). */
  land(): void {
    this.mode = "walk";
    this.vel.set(0, 0, 0);
    this.fallDistance = 0;
    this.grounded = true;
  }

  private recenter(): void {
    while (this.pos.x > D.UNIT_PITCH / 2) {
      this.pos.x -= D.UNIT_PITCH;
      this.events.onShiftX(1);
    }
    while (this.pos.x < -D.UNIT_PITCH / 2) {
      this.pos.x += D.UNIT_PITCH;
      this.events.onShiftX(-1);
    }
    while (this.pos.y > D.FLOOR_PITCH / 2 + 0.01) {
      this.pos.y -= D.FLOOR_PITCH;
      this.events.onShiftY(1);
    }
    while (this.pos.y < -D.FLOOR_PITCH / 2 - 0.01) {
      this.pos.y += D.FLOOR_PITCH;
      this.events.onShiftY(-1);
    }
  }

  private syncCamera(): void {
    this.camera.position.set(this.pos.x, this.pos.y + D.EYE_H, this.pos.z);
    // yaw=0 → +x. three's yaw=0 looks down -z, so offset by -π/2.
    this.camera.rotation.set(this.pitch, this.yaw - Math.PI / 2, 0);
  }

  // ----------------------------------------------------------- collisions

  private collideWalls(): void {
    const r = D.PLAYER_R;
    const py0 = this.pos.y;
    const py1 = this.pos.y + 1.78;
    for (const s of this.world.segmentsNear(this.pos.x)) {
      if (py0 >= s.y1 || py1 <= s.y0) continue;
      // Closest point on segment to the player.
      const dx = s.bx - s.ax;
      const dz = s.bz - s.az;
      const len2 = dx * dx + dz * dz;
      let t = len2 > 0 ? ((this.pos.x - s.ax) * dx + (this.pos.z - s.az) * dz) / len2 : 0;
      t = Math.max(0, Math.min(1, t));
      const cx = s.ax + dx * t;
      const cz = s.az + dz * t;
      let ox = this.pos.x - cx;
      let oz = this.pos.z - cz;
      const d = Math.hypot(ox, oz);
      const want = r + s.pad;
      if (d < want) {
        if (d < 1e-6) {
          // Dead center: push along the segment normal.
          ox = -dz;
          oz = dx;
          const n = Math.hypot(ox, oz) || 1;
          ox /= n;
          oz /= n;
        } else {
          ox /= d;
          oz /= d;
        }
        this.pos.x = cx + ox * want;
        this.pos.z = cz + oz * want;
      }
    }
  }

  private collideStairwell(): void {
    const r = D.PLAYER_R;
    for (const axis of this.world.stairAxesNear(this.pos.x)) {
      const dx = this.pos.x - axis.x;
      const dz = this.pos.z - axis.z;
      const d = Math.hypot(dx, dz);
      if (d > D.STAIR_R + r + 0.3) continue;
      // Door sector: azimuth within the chord opening, any floor height.
      const a = Math.atan2(dz, dx);
      const doorHalf = Math.asin(D.STAIR_DOOR_HALF / D.STAIR_R);
      let da = a - A_DOOR;
      while (da > Math.PI) da -= 2 * Math.PI;
      while (da < -Math.PI) da += 2 * Math.PI;
      // The doorway only admits bodies whose feet are at floor level: the
      // shell above each door (and between floors) is solid masonry.
      const yMod = ((this.pos.y % D.FLOOR_PITCH) + D.FLOOR_PITCH) % D.FLOOR_PITCH;
      const atDoorHeight = yMod < 0.7 || yMod > D.FLOOR_PITCH - 0.07;
      const inDoor = Math.abs(da) < doorHalf && atDoorHeight;
      if (inDoor) continue;
      // Solid shell: keep the player on whichever side they are.
      if (d > D.STAIR_R) {
        if (d < D.STAIR_R + r) {
          const push = (D.STAIR_R + r) / d;
          this.pos.x = axis.x + dx * push;
          this.pos.z = axis.z + dz * push;
        }
      } else if (d > D.STAIR_R - r) {
        const push = (D.STAIR_R - r) / (d || 1e-6);
        this.pos.x = axis.x + dx * push;
        this.pos.z = axis.z + dz * push;
      }
      // Central column.
      if (d < D.STAIR_COL_R + r) {
        const push = (D.STAIR_COL_R + r) / (d || 1e-6);
        this.pos.x = axis.x + dx * push;
        this.pos.z = axis.z + dz * push;
      }
    }
  }

  /**
   * Analytic ground height at a point, or null over the abyss.
   * All heights are relative to the current center floor (y=0).
   */
  groundHeight(x: number, z: number, feetY: number): number | null {
    // Stairwells.
    for (const axis of this.world.stairAxesNear(x)) {
      const dx = x - axis.x;
      const dz = z - axis.z;
      const d = Math.hypot(dx, dz);
      if (d <= D.STAIR_R + 0.02) {
        const a = Math.atan2(dz, dx);
        let phi = A_DOOR - a;
        while (phi < 0) phi += 2 * Math.PI;
        while (phi >= 2 * Math.PI) phi -= 2 * Math.PI;
        const slot = Math.floor((phi + D.STEP_ANG / 2) / D.STEP_ANG);
        const base = slot * D.STEP_RISE;
        // Candidate treads every floor; take the highest not above feet+step.
        const k = Math.floor((feetY + D.STEP_UP - base) / D.FLOOR_PITCH);
        return base + k * D.FLOOR_PITCH;
      }
    }
    // The shaft: bottomless.
    const n = Math.round(x / D.UNIT_PITCH);
    const hx = x - n * D.UNIT_PITCH;
    if (insideHex(hx, z, D.SHAFT_SIDE + 0.02)) return null;
    // Everywhere else: the floor of the nearest storey.
    const k = Math.round(feetY / D.FLOOR_PITCH);
    const fl = k * D.FLOOR_PITCH;
    return fl <= feetY + D.STEP_UP ? fl : fl - D.FLOOR_PITCH;
  }

  private ceilingHeight(x: number, z: number): number {
    for (const axis of this.world.stairAxesNear(x)) {
      if (Math.hypot(x - axis.x, z - axis.z) <= D.STAIR_R + 0.02) return 1e9;
    }
    const n = Math.round(x / D.UNIT_PITCH);
    const hx = x - n * D.UNIT_PITCH;
    if (insideHex(hx, z, D.SHAFT_SIDE + 0.02)) return 1e9;
    // Beside the railing a librarian may lean and clamber over — the rigid
    // capsule gets headroom there, or vaulting would be impossible.
    if (insideHex(hx, z, D.RAIL_R + 0.45)) return 1e9;
    const k = Math.round(this.pos.y / D.FLOOR_PITCH);
    return k * D.FLOOR_PITCH + D.CEIL_H;
  }
}

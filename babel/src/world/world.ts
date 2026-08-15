/**
 * The visible Library: a window of repeating units around the player,
 * instanced so the whole universe costs a handful of draw calls. The window
 * recenters as the player walks (floating origin), so coordinates never
 * lose precision no matter how unfathomably far the seek leads.
 */

import * as THREE from "three";
import { Reflector } from "three/addons/objects/Reflector.js";
import { Digits, copy } from "../core/bignum";
import { addInt } from "../core/bignum";
import { SHELVES, SLOTS, VOLUMES } from "../core/constants";
import { Sfc32 } from "../core/rng";
import * as D from "./dims";
import { makePalette, BOOK_TINTS, Palette } from "./textures";
import { buildUnitTemplate, shaftTube, stairTube, Segment, UnitTemplate } from "./unit";

export interface Quality {
  /** Corridor render distance, units each way. */
  rx: number;
  /** Floors rendered above/below. */
  ry: number;
  /** Populate real book meshes within this many floors of the player. */
  bookFloors: number;
  liveMirrors: boolean;
  dpr: number;
  antialias: boolean;
}

export const QUALITY_HIGH: Quality = { rx: 4, ry: 3, bookFloors: 3, liveMirrors: true, dpr: 2, antialias: true };
export const QUALITY_LOW: Quality = { rx: 2, ry: 1, bookFloors: 0, liveMirrors: false, dpr: 1, antialias: false };

const TUBE_LEN = 70;

export class World {
  readonly scene = new THREE.Scene();
  readonly template: UnitTemplate;
  readonly palette: Palette;
  readonly quality: Quality;

  /** Corridor coordinate of the center unit (bignum, absolute). */
  c0: Digits;
  /** Floor of the center unit (absolute, relative to the first hexagon). */
  f0 = 0;

  private books!: THREE.InstancedMesh;
  private shells: THREE.InstancedMesh[] = [];
  private glass!: THREE.InstancedMesh;
  private tubes!: THREE.InstancedMesh;
  private stairTubes!: THREE.InstancedMesh;
  private lights: THREE.PointLight[] = [];
  private reflectors: Reflector[] = [];
  private highlightMesh: THREE.Mesh | null = null;

  /** dx offsets of rendered units (corridor), dy floors. */
  private dxs: number[] = [];
  private dys: number[] = [];

  constructor(start: { c: Digits; f: number }, quality: Quality) {
    this.c0 = copy(start.c);
    this.f0 = start.f;
    this.quality = quality;
    this.template = buildUnitTemplate();
    this.palette = makePalette();

    this.scene.background = new THREE.Color(0x080604);
    this.scene.fog = new THREE.FogExp2(0x080604, quality.rx >= 4 ? 0.11 : 0.16);

    for (let dx = -quality.rx - 1; dx <= quality.rx; dx++) this.dxs.push(dx);
    for (let dy = -quality.ry; dy <= quality.ry + 1; dy++) this.dys.push(dy);

    this.buildInstances();
    this.buildLights();
    this.buildMirrors();
    this.retile();
  }

  private unitCount(): number {
    return this.dxs.length * this.dys.length;
  }

  private buildInstances(): void {
    const t = this.template;
    const p = this.palette;
    const U = this.unitCount();
    for (const m of [p.wood, p.stone, p.floor, p.brass, p.book]) m.side = THREE.DoubleSide;

    const mk = (geo: THREE.BufferGeometry, mat: THREE.Material): THREE.InstancedMesh => {
      const mesh = new THREE.InstancedMesh(geo, mat, U);
      mesh.frustumCulled = false;
      this.scene.add(mesh);
      this.shells.push(mesh);
      return mesh;
    };
    mk(t.wood, p.wood);
    mk(t.stone, p.stone);
    mk(t.brass, p.brass);
    mk(t.lamps, p.lamp);

    // Books: one instanced mesh for every volume in the window.
    const bookGeo = new THREE.BoxGeometry(D.BOOK_T - 0.006, D.BOOK_H, D.BOOK_D);
    this.books = new THREE.InstancedMesh(bookGeo, p.book, U * SLOTS);
    this.books.frustumCulled = false;
    this.scene.add(this.books);

    // Dark glass stands in for mirrors we are not standing before.
    const glassGeo = new THREE.PlaneGeometry(D.MIRROR_W, D.MIRROR_Y1 - D.MIRROR_Y0);
    glassGeo.rotateY(Math.PI); // face north, into the vestibule
    this.glass = new THREE.InstancedMesh(glassGeo, p.darkGlass, U);
    this.glass.frustumCulled = false;
    this.scene.add(this.glass);

    // Endless continuations of the shaft and the stairwells.
    const tubeMat = new THREE.MeshBasicMaterial({ color: 0x050403, side: THREE.BackSide, fog: true });
    this.tubes = new THREE.InstancedMesh(shaftTube(TUBE_LEN), tubeMat, this.dxs.length * 2);
    this.tubes.frustumCulled = false;
    this.scene.add(this.tubes);
    this.stairTubes = new THREE.InstancedMesh(stairTube(TUBE_LEN), tubeMat, this.dxs.length * 2);
    this.stairTubes.frustumCulled = false;
    this.scene.add(this.stairTubes);

    this.scene.add(new THREE.AmbientLight(0x564a3c, 0.35));
  }

  private buildLights(): void {
    // "The light they emit is insufficient, incessant."
    for (let i = 0; i < 6; i++) {
      const l = new THREE.PointLight(0xffc06a, 7.5, 0, 2);
      this.lights.push(l);
      this.scene.add(l);
    }
    // Faint fills: the two vestibules beside the player, and the stairwell.
    for (let i = 0; i < 3; i++) {
      const l = new THREE.PointLight(0xffd9a0, 1.6, 0, 2);
      this.lights.push(l);
      this.scene.add(l);
    }
    // Dim glow for the floors seen through the shaft, above and below.
    for (let i = 0; i < 2; i++) {
      const l = new THREE.PointLight(0xffc06a, 3.0, 0, 2);
      this.lights.push(l);
      this.scene.add(l);
    }
  }

  private buildMirrors(): void {
    if (!this.quality.liveMirrors) return;
    const t = this.template;
    const size = 512;
    // Two live mirrors: the east vestibule (dx 0) and the west one (dx -1).
    for (const dx of [0, -1]) {
      const r = new Reflector(new THREE.PlaneGeometry(D.MIRROR_W, D.MIRROR_Y1 - D.MIRROR_Y0), {
        clipBias: 0.003,
        textureWidth: size,
        textureHeight: size,
        color: 0xa9a9b3,
      });
      r.rotateY(Math.PI);
      r.position.set(t.mirrorCenter.x + dx * D.UNIT_PITCH, t.mirrorCenter.y, t.mirrorCenter.z);
      this.scene.add(r);
      this.reflectors.push(r);
    }
  }

  /** Last digits of c0 as a safe integer, for cosmetic per-unit hashing. */
  private cLow(): number {
    let v = 0;
    for (let i = 9; i >= 0; i--) v = v * 25 + this.c0[i];
    return v;
  }

  /** Rebuild all instance transforms for the current window. */
  retile(): void {
    const t = this.template;
    const m = new THREE.Matrix4();
    const glassM = new THREE.Matrix4();
    const hiddenGlass = new THREE.Matrix4().makeScale(1e-6, 1e-6, 1e-6);
    const cLow = this.cLow();
    let u = 0;
    let tube = 0;
    const color = new THREE.Color();
    for (const dy of this.dys) {
      for (const dx of this.dxs) {
        m.makeTranslation(dx * D.UNIT_PITCH, dy * D.FLOOR_PITCH, 0);
        for (const shell of this.shells) shell.setMatrixAt(u, m);
        // Mirror glass hangs on the vestibule's south wall. Where a live
        // reflector stands (this floor, the two nearest vestibules), the
        // dark pane yields to it.
        if (this.quality.liveMirrors && dy === 0 && (dx === 0 || dx === -1)) {
          this.glass.setMatrixAt(u, hiddenGlass);
        } else {
          this.glass.setMatrixAt(
            u,
            glassM.makeTranslation(
              dx * D.UNIT_PITCH + t.mirrorCenter.x,
              dy * D.FLOOR_PITCH + t.mirrorCenter.y,
              t.mirrorCenter.z,
            ),
          );
        }

        // Books: tints come from cheap spatial hashing — content is only
        // computed when a volume is opened. Beyond bookFloors, the volumes
        // are vanishingly small (you could never reach them anyway).
        if (Math.abs(dy) > this.quality.bookFloors) {
          const bm = new THREE.Matrix4().makeScale(1e-6, 1e-6, 1e-6);
          for (let s = 0; s < SLOTS; s++) this.books.setMatrixAt(u * SLOTS + s, bm);
        } else {
          const rng = Sfc32.fromString("tints", cLow + dx, this.f0 + dy);
          const bm = new THREE.Matrix4();
          for (let s = 0; s < SLOTS; s++) {
            bm.copy(t.bookMatrices[s]);
            bm.elements[12] += dx * D.UNIT_PITCH;
            bm.elements[13] += dy * D.FLOOR_PITCH;
            this.books.setMatrixAt(u * SLOTS + s, bm);
            color.copy(BOOK_TINTS[rng.int(BOOK_TINTS.length)]);
            const tone = 0.82 + rng.float() * 0.36;
            color.multiplyScalar(tone);
            this.books.setColorAt(u * SLOTS + s, color);
          }
        }
        u++;
      }
    }
    // Continuation tubes above and below each rendered column, flush with
    // the outermost slabs so they never intrude into a rendered room.
    const yTop = (this.dys[this.dys.length - 1] + 1) * D.FLOOR_PITCH + TUBE_LEN / 2;
    const yBot = this.dys[0] * D.FLOOR_PITCH - D.SLAB_H - TUBE_LEN / 2;
    for (const dx of this.dxs) {
      for (const y of [yTop, yBot]) {
        m.makeTranslation(dx * D.UNIT_PITCH, y, 0);
        this.tubes.setMatrixAt(tube, m);
        m.makeTranslation(dx * D.UNIT_PITCH + t.stairAxis.x, y, t.stairAxis.z);
        this.stairTubes.setMatrixAt(tube, m);
        tube++;
      }
    }
    for (const shell of this.shells) shell.instanceMatrix.needsUpdate = true;
    this.books.instanceMatrix.needsUpdate = true;
    if (this.books.instanceColor) this.books.instanceColor.needsUpdate = true;
    this.glass.instanceMatrix.needsUpdate = true;
    this.tubes.instanceMatrix.needsUpdate = true;
    this.stairTubes.instanceMatrix.needsUpdate = true;

    // Lamp lights: this hexagon and its corridor neighbours.
    const L = this.template.lampCenters;
    for (let i = 0; i < 6; i++) {
      const dx = [-1, -1, 0, 0, 1, 1][i];
      const lc = L[i % 2];
      this.lights[i].position.set(dx * D.UNIT_PITCH + lc.x, lc.y - 0.05, lc.z);
    }
    // Fills: the two vestibules flanking the hexagon, and this unit's stairwell.
    this.lights[6].position.set(D.UNIT_PITCH / 2 - 0.4, 1.7, 0);
    this.lights[7].position.set(-D.UNIT_PITCH / 2 + 0.4, 1.7, 0);
    this.lights[8].position.set(t.stairAxis.x, 1.1, t.stairAxis.z);
    // The storeys seen through the shaft.
    this.lights[9].position.set(0, D.FLOOR_PITCH + L[0].y, 0);
    this.lights[10].position.set(0, -D.FLOOR_PITCH + L[0].y, 0);
  }

  /**
   * Shift the window after the player crosses a unit boundary.
   * dir: +1 east, -1 west. Returns the world-space x correction to apply.
   */
  shiftX(dir: 1 | -1): number {
    addInt(this.c0, dir);
    this.retile();
    return -dir * D.UNIT_PITCH;
  }

  shiftY(dir: 1 | -1, opts?: { skipRetile?: boolean }): number {
    this.f0 += dir;
    if (!opts?.skipRetile) this.retile();
    return -dir * D.FLOOR_PITCH;
  }

  /** Corridor coordinate digits for a unit offset within the window. */
  coordAt(dx: number, dy: number): { c: Digits; f: number } {
    const c = copy(this.c0);
    addInt(c, dx);
    return { c, f: this.f0 + dy };
  }

  /** Resolve a raycast hit on the books mesh to shelf coordinates. */
  resolveBookInstance(instanceId: number): { dx: number; dy: number; wall: number; shelf: number; volume: number } {
    const u = Math.floor(instanceId / SLOTS);
    const slot = instanceId % SLOTS;
    const dx = this.dxs[u % this.dxs.length];
    const dy = this.dys[Math.floor(u / this.dxs.length)];
    const wall = Math.floor(slot / (SHELVES * VOLUMES));
    const shelf = Math.floor(slot / VOLUMES) % SHELVES;
    const volume = slot % VOLUMES;
    return { dx, dy, wall, shelf, volume };
  }

  /** Instance id for shelf coordinates (inverse of resolveBookInstance). */
  bookInstanceId(dx: number, dy: number, wall: number, shelf: number, volume: number): number {
    const ux = this.dxs.indexOf(dx);
    const uy = this.dys.indexOf(dy);
    if (ux < 0 || uy < 0) return -1;
    const u = uy * this.dxs.length + ux;
    return u * SLOTS + (wall * SHELVES + shelf) * VOLUMES + volume;
  }

  /** Local-space position of a volume. */
  bookWorldPos(dx: number, dy: number, wall: number, shelf: number, volume: number): THREE.Vector3 {
    const slot = (wall * SHELVES + shelf) * VOLUMES + volume;
    const v = new THREE.Vector3();
    v.setFromMatrixPosition(this.template.bookMatrices[slot]);
    v.x += dx * D.UNIT_PITCH;
    v.y += dy * D.FLOOR_PITCH;
    return v;
  }

  get booksMesh(): THREE.InstancedMesh {
    return this.books;
  }

  /** Hide/show one volume (while it is pulled out or being read). */
  setBookHidden(instanceId: number, hidden: boolean): void {
    const m = new THREE.Matrix4();
    this.books.getMatrixAt(instanceId, m);
    const s = hidden ? 1e-6 : 1;
    const r = this.resolveBookInstance(instanceId);
    const base = this.template.bookMatrices[(r.wall * SHELVES + r.shelf) * VOLUMES + r.volume].clone();
    base.elements[12] += r.dx * D.UNIT_PITCH;
    base.elements[13] += r.dy * D.FLOOR_PITCH;
    if (hidden) base.scale(new THREE.Vector3(s, s, s));
    this.books.setMatrixAt(instanceId, base);
    this.books.instanceMatrix.needsUpdate = true;
  }

  /** Pulsing marker around a sought volume. */
  setHighlight(pos: THREE.Vector3 | null, yaw = 0): void {
    if (this.highlightMesh) {
      this.scene.remove(this.highlightMesh);
      this.highlightMesh = null;
    }
    if (!pos) return;
    const g = new THREE.BoxGeometry(D.BOOK_T + 0.025, D.BOOK_H + 0.03, D.BOOK_D + 0.03);
    const mesh = new THREE.Mesh(g, this.palette.glow);
    mesh.position.copy(pos);
    mesh.rotation.y = yaw;
    this.scene.add(mesh);
    this.highlightMesh = mesh;
  }

  pulse(time: number): void {
    if (this.highlightMesh) {
      this.palette.glow.opacity = 0.25 + 0.2 * Math.sin(time * 5);
    }
  }

  /** Test harness: hide/show meshes by name to bisect rendering issues. */
  setMeshVisible(name: string, visible: boolean): boolean {
    const map: Record<string, THREE.Object3D | undefined> = {
      wood: this.shells[0],
      stone: this.shells[1],
      brass: this.shells[2],
      lamps: this.shells[3],
      books: this.books,
      glass: this.glass,
      tubes: this.tubes,
      stairTubes: this.stairTubes,
    };
    const m = map[name];
    if (!m) return false;
    m.visible = visible;
    return true;
  }

  /** Diagnostics for the test harness. */
  debugInfo(): unknown {
    const dump = (mesh: THREE.InstancedMesh, name: string) => {
      const m = new THREE.Matrix4();
      const rows: { u: number; x: number; y: number; sx: number }[] = [];
      for (const u of [0, this.dxs.length + 3, this.dxs.length * 2 + 3, mesh.count - 1]) {
        if (u >= mesh.count) continue;
        mesh.getMatrixAt(u, m);
        rows.push({ u, x: +m.elements[12].toFixed(2), y: +m.elements[13].toFixed(2), sx: +m.elements[0].toFixed(4) });
      }
      return { name, count: mesh.count, visible: mesh.visible, rows };
    };
    return {
      dxs: this.dxs,
      dys: this.dys,
      shells: this.shells.map((s, i) => dump(s, `shell${i}`)),
      tubes: dump(this.tubes, "tubes"),
      books: dump(this.books, "books"),
    };
  }

  /** Collision segments near a local x position (current floor). */
  *segmentsNear(x: number): Generator<Segment> {
    const n = Math.round(x / D.UNIT_PITCH);
    for (let dn = -1; dn <= 1; dn++) {
      const dx = (n + dn) * D.UNIT_PITCH;
      for (const s of this.template.segments) {
        yield { ...s, ax: s.ax + dx, bx: s.bx + dx };
      }
    }
  }

  /** Stair axes near a local x position (this unit's and the west one's). */
  stairAxesNear(x: number): { x: number; z: number }[] {
    const n = Math.round(x / D.UNIT_PITCH);
    const out: { x: number; z: number }[] = [];
    for (let dn = -1; dn <= 1; dn++) {
      out.push({ x: this.template.stairAxis.x + (n + dn) * D.UNIT_PITCH, z: this.template.stairAxis.z });
    }
    return out;
  }
}

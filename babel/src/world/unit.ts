/**
 * The repeating unit of the universe: one hexagonal gallery plus the
 * vestibule on its east side (closets, mirror, the mouth of the spiral
 * staircase), and the staircase serving the *west* vestibule, whose well is
 * carved through this unit's floor slab. Tiled along x with period
 * UNIT_PITCH and vertically with period FLOOR_PITCH, these compose the
 * entire Library.
 *
 * Exports merged template geometries (one draw call per material for all
 * visible units) and analytic colliders.
 */

import * as THREE from "three";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import * as D from "./dims";
import { SHELVES, VOLUMES, WALLS } from "../core/constants";

export interface Segment {
  ax: number;
  az: number;
  bx: number;
  bz: number;
  y0: number;
  y1: number;
  /** Extra pushout beyond the player radius (half wall thickness). */
  pad: number;
}

export interface UnitTemplate {
  wood: THREE.BufferGeometry;
  stone: THREE.BufferGeometry;
  brass: THREE.BufferGeometry;
  lamps: THREE.BufferGeometry;
  /** Local matrices for the 640 volumes; index = slotIndex(wall, shelf, vol). */
  bookMatrices: THREE.Matrix4[];
  /** Yaw of each shelf wall's outward normal (books share it). */
  wallYaws: number[];
  segments: Segment[];
  /** Stair axis (east vestibule's own stair), local coords. */
  stairAxis: { x: number; z: number };
  /** Stair axis of the well in this unit's slab (the west vestibule's). */
  slabStairAxis: { x: number; z: number };
  mirrorCenter: { x: number; y: number; z: number };
  lampCenters: { x: number; y: number; z: number }[];
}

const APO = D.HEX_APO;

function box(
  parts: THREE.BufferGeometry[],
  cx: number,
  cy: number,
  cz: number,
  sx: number,
  sy: number,
  sz: number,
  rotY = 0,
  uvScale = 0.55,
): void {
  const g = new THREE.BoxGeometry(sx, sy, sz);
  // Scale UVs roughly with world size so textures keep a consistent grain.
  const uv = g.attributes.uv as THREE.BufferAttribute;
  for (let i = 0; i < uv.count; i++) {
    uv.setXY(i, uv.getX(i) * Math.max(sx, sz) * uvScale, uv.getY(i) * Math.max(sy, 0.4) * uvScale);
  }
  if (rotY !== 0) g.rotateY(rotY);
  g.translate(cx, cy, cz);
  parts.push(g);
}

function seg(
  segments: Segment[],
  ax: number,
  az: number,
  bx: number,
  bz: number,
  y0: number,
  y1: number,
  pad: number,
): void {
  segments.push({ ax, az, bx, bz, y0, y1, pad });
}

/** Hexagonal prism shell (inward-facing) used for the endless shaft. */
export function shaftTube(length: number): THREE.BufferGeometry {
  const g = new THREE.CylinderGeometry(D.SHAFT_SIDE, D.SHAFT_SIDE, length, 6, 1, true);
  // Cylinder vertices sit at angles 0,60,...; our shaft hexagon has vertices
  // at 30+60k. Rotate to match.
  g.rotateY(Math.PI / 6);
  return g;
}

export function stairTube(length: number): THREE.BufferGeometry {
  return new THREE.CylinderGeometry(D.STAIR_R, D.STAIR_R, length, 24, 1, true);
}

/** Wedge step: annular sector from STAIR_COL_R to STAIR_R, given arc. */
function stepGeometry(a0: number, a1: number, thickness: number): THREE.BufferGeometry {
  const shape = new THREE.Shape();
  const r0 = D.STAIR_COL_R;
  const r1 = D.STAIR_R - 0.015;
  const steps = 5;
  shape.moveTo(r0 * Math.cos(a0), r0 * Math.sin(a0));
  for (let i = 0; i <= steps; i++) {
    const a = a0 + ((a1 - a0) * i) / steps;
    shape.lineTo(r1 * Math.cos(a), r1 * Math.sin(a));
  }
  for (let i = steps; i >= 0; i--) {
    const a = a0 + ((a1 - a0) * i) / steps;
    shape.lineTo(r0 * Math.cos(a), r0 * Math.sin(a));
  }
  const g = new THREE.ExtrudeGeometry(shape, { depth: thickness, bevelEnabled: false });
  // rotateX(π/2) maps shape (x, y, depth d) to world (x, -d, y): the shape
  // plane lands in XZ with shape-y becoming +z, and the extrusion hangs
  // below y=0 — so a step translated to y=h has its top exactly at h.
  g.rotateX(Math.PI / 2);
  return g;
}

/** The slab: unit footprint with the shaft hex and a stair circle removed. */
function slabGeometry(slabStairAxis: { x: number; z: number }): THREE.BufferGeometry {
  const hw = D.UNIT_PITCH / 2;
  const hd = 2.6; // half depth: beyond the closets, all is solid rock anyway
  const shape = new THREE.Shape();
  shape.moveTo(-hw, -hd);
  shape.lineTo(hw, -hd);
  shape.lineTo(hw, hd);
  shape.lineTo(-hw, hd);
  shape.closePath();

  const shaft = new THREE.Path();
  const verts = D.hexVertices(D.SHAFT_SIDE);
  shaft.moveTo(verts[0][0], verts[0][1]);
  for (let k = 1; k < 6; k++) shaft.lineTo(verts[k][0], verts[k][1]);
  shaft.closePath();
  shape.holes.push(shaft);

  const stair = new THREE.Path();
  stair.absarc(slabStairAxis.x, slabStairAxis.z, D.STAIR_R + 0.02, 0, Math.PI * 2, true);
  shape.holes.push(stair);

  const g = new THREE.ExtrudeGeometry(shape, { depth: D.SLAB_H, bevelEnabled: false });
  // Same mapping as stepGeometry: slab top lands at y=0, body in [-SLAB_H, 0].
  g.rotateX(Math.PI / 2);
  return g;
}

export function buildUnitTemplate(): UnitTemplate {
  const wood: THREE.BufferGeometry[] = [];
  const stone: THREE.BufferGeometry[] = [];
  const brass: THREE.BufferGeometry[] = [];
  const lampsGeo: THREE.BufferGeometry[] = [];
  const segments: Segment[] = [];
  const bookMatrices: THREE.Matrix4[] = new Array(WALLS * SHELVES * VOLUMES);
  const wallYaws: number[] = new Array(WALLS);

  const V = D.hexVertices(D.HEX_SIDE);
  const stairAxis = { x: APO + D.STAIR_AXIS_X, z: D.STAIR_AXIS_Z };
  const slabStairAxis = { x: APO + D.STAIR_AXIS_X - D.UNIT_PITCH, z: D.STAIR_AXIS_Z };

  // ---------------------------------------------------------------- slab
  {
    const g = slabGeometry(slabStairAxis);
    // Position: top of slab at y = 0 (this floor's ground).
    g.translate(0, 0, 0);
    stone.push(g);
  }

  // ----------------------------------------------------- the four bookcases
  // Wall order (D.SHELF_WALLS): SE, SW, NW, NE.
  for (let w = 0; w < WALLS; w++) {
    const { v0, v1 } = D.SHELF_WALLS[w];
    const a = V[v0];
    const b = V[v1];
    const mx = (a[0] + b[0]) / 2;
    const mz = (a[1] + b[1]) / 2;
    const outLen = Math.hypot(mx, mz); // == APO
    const nx = mx / outLen; // outward normal
    const nz = mz / outLen;
    const yaw = Math.atan2(nx, nz); // rotY(yaw) maps +z to (nx, nz)
    wallYaws[w] = yaw;
    // Viewer facing the wall from the room: right-hand direction.
    const ux = -nz;
    const uz = nx;

    const place = (t: number, y: number, dist: number, sx: number, sy: number, sz: number, arr: THREE.BufferGeometry[]) => {
      box(arr, nx * dist + ux * t, y, nz * dist + uz * t, sx, sy, sz, yaw);
    };

    // Back panel.
    place(0, D.CEIL_H / 2, APO - 0.025, D.HEX_SIDE - 0.02, D.CEIL_H, 0.05, wood);
    // Side posts.
    const postT = (D.BOOK_SPAN + 0.12) / 2 + 0.06;
    place(-postT, D.CEIL_H / 2, APO - D.CASE_DEPTH / 2, 0.12, D.CEIL_H, D.CASE_DEPTH, wood);
    place(postT, D.CEIL_H / 2, APO - D.CASE_DEPTH / 2, 0.12, D.CEIL_H, D.CASE_DEPTH, wood);
    // Six boards (top and bottom included).
    for (let k = 0; k <= 5; k++) {
      const y = k * D.ROW_PITCH + D.BOARD_T / 2;
      place(0, y, APO - D.CASE_DEPTH / 2 - 0.005, D.BOOK_SPAN + 0.12, D.BOARD_T, D.CASE_DEPTH - 0.04, wood);
    }
    // Collider along the case front.
    const frontScale = (APO - D.CASE_DEPTH) / APO;
    seg(segments, a[0] * frontScale, a[1] * frontScale, b[0] * frontScale, b[1] * frontScale, 0, D.CEIL_H, 0.015);

    // The thirty-two volumes on each of the five shelves.
    for (let s = 0; s < SHELVES; s++) {
      const rowBase = (4 - s) * D.ROW_PITCH + D.BOARD_T; // shelf 0 is the top row
      const cy = rowBase + D.BOOK_H / 2;
      for (let v = 0; v < VOLUMES; v++) {
        const t = -D.BOOK_SPAN / 2 + D.BOOK_PITCH * (v + 0.5);
        const dist = APO - D.CASE_DEPTH + D.BOOK_RECESS + D.BOOK_D / 2;
        const m = new THREE.Matrix4();
        m.makeRotationY(yaw);
        m.setPosition(nx * dist + ux * t, cy, nz * dist + uz * t);
        bookMatrices[(w * SHELVES + s) * VOLUMES + v] = m;
      }
    }
  }

  // ------------------------------------------------- east & west door walls
  for (const side of [1, -1]) {
    const x = side * (APO + D.WALL_T / 2);
    const zEdge = D.HEX_SIDE / 2; // wall spans z in [-0.9, 0.9]
    const zDoor = D.DOOR_W / 2;
    // Solid flanks.
    for (const sz of [-1, 1]) {
      const z0 = sz * zDoor;
      const z1 = sz * zEdge;
      box(stone, x, D.CEIL_H / 2, (z0 + z1) / 2, D.WALL_T, D.CEIL_H, Math.abs(z1 - z0));
      seg(segments, x, z0, x, z1, 0, D.CEIL_H, D.WALL_T / 2);
    }
    // Lintel above the door.
    box(stone, x, (D.DOOR_H + D.CEIL_H) / 2, 0, D.WALL_T, D.CEIL_H - D.DOOR_H, D.DOOR_W);
    // Door jambs (thin trim).
    for (const sz of [-1, 1]) {
      box(wood, x, D.DOOR_H / 2, sz * (zDoor + 0.02), D.WALL_T + 0.04, D.DOOR_H, 0.05);
    }
  }

  // -------------------------------------------------------- hexagon corners
  // Short corner walls between the bookcases and the door walls are implied
  // by the hexagon edges themselves; the bookcases meet the door walls at
  // the vertices, so no extra geometry is needed. (Vertices V0/V5 join the
  // east wall; V2/V3 join the west wall.)

  // ------------------------------------------------------------- vestibule
  const xv0 = APO + D.WALL_T; // interior west end
  const xv1 = APO + D.VEST_LEN - D.WALL_T; // interior east end
  const zN = -D.VEST_W / 2; // north wall inner face
  const zS = D.VEST_W / 2;
  const wallMidN = zN - D.WALL_T / 2;
  const wallMidS = zS + D.WALL_T / 2;

  // Closet openings (both at the same x), stair opening on the north.
  const cd0 = APO + 0.24;
  const cd1 = cd0 + D.CLOSET_DOOR_W;
  const sd0 = stairAxis.x - D.STAIR_DOOR_HALF;
  const sd1 = stairAxis.x + D.STAIR_DOOR_HALF;

  const wallRun = (
    z: number,
    x0: number,
    x1: number,
    openings: [number, number, number][], // [from, to, height]
  ) => {
    let cursor = x0;
    const pieces: [number, number][] = [];
    const sorted = openings.slice().sort((p, q) => p[0] - q[0]);
    for (const [o0, o1, oh] of sorted) {
      if (o0 > cursor) pieces.push([cursor, o0]);
      // Lintel over the opening.
      box(stone, (o0 + o1) / 2, (oh + D.CEIL_H) / 2, z, o1 - o0, D.CEIL_H - oh, D.WALL_T);
      cursor = o1;
    }
    if (cursor < x1) pieces.push([cursor, x1]);
    for (const [p0, p1] of pieces) {
      box(stone, (p0 + p1) / 2, D.CEIL_H / 2, z, p1 - p0, D.CEIL_H, D.WALL_T);
      seg(segments, p0, z, p1, z, 0, D.CEIL_H, D.WALL_T / 2);
    }
  };

  wallRun(wallMidN, xv0, xv1, [
    [cd0, cd1, D.CLOSET_DOOR_H],
    [sd0, sd1, D.DOOR_H],
  ]);
  wallRun(wallMidS, xv0, xv1, [[cd0, cd1, D.CLOSET_DOOR_H]]);

  // ---------------------------------------------------------------- closets
  // North closet: sleep standing. South closet: the other necessity.
  for (const side of [-1, 1]) {
    const zInner = side * (D.VEST_W / 2 + D.WALL_T); // closet's vestibule-side face
    const zFar = side * (D.VEST_W / 2 + D.WALL_T + D.CLOSET_D);
    const x0 = APO + 0.16;
    const x1 = x0 + D.CLOSET_W;
    // Far wall.
    box(stone, (x0 + x1) / 2, D.CEIL_H / 2, zFar + (side * D.WALL_T) / 2, D.CLOSET_W + 2 * D.WALL_T, D.CEIL_H, D.WALL_T);
    seg(segments, x0, zFar, x1, zFar, 0, D.CEIL_H, D.WALL_T / 2);
    // Side walls.
    for (const xs of [x0, x1]) {
      box(stone, xs + (xs === x0 ? -1 : 1) * (D.WALL_T / 2), D.CEIL_H / 2, (zInner + zFar) / 2, D.WALL_T, D.CEIL_H, Math.abs(zFar - zInner));
      seg(segments, xs, zInner, xs, zFar, 0, D.CEIL_H, D.WALL_T / 2);
    }
    if (side > 0) {
      // The latrine: a stone block with a dark mouth.
      box(stone, (x0 + x1) / 2, 0.19, zFar - side * 0.26, 0.42, 0.38, 0.4);
      seg(segments, x0 + 0.1, zFar - side * 0.46, x1 - 0.1, zFar - side * 0.46, 0, 0.38, 0.02);
    } else {
      // The sleeping niche: a worn wooden board to lean on, standing up.
      box(wood, (x0 + x1) / 2, 1.05, zFar - side * 0.05, D.CLOSET_W - 0.1, 1.9, 0.05);
    }
  }

  // ------------------------------------------------------------ the mirror
  // "In the hallway there is a mirror which faithfully duplicates all
  // appearances." Frame here; the live reflector is added per-instance.
  const mirrorCenter = { x: stairAxis.x, y: (D.MIRROR_Y0 + D.MIRROR_Y1) / 2, z: zS - 0.015 };
  {
    // Wooden backing slab, mostly sunk into the wall; the glass sits proud.
    const mh = D.MIRROR_Y1 - D.MIRROR_Y0;
    box(wood, mirrorCenter.x, mirrorCenter.y, zS + 0.01, D.MIRROR_W + 0.1, mh + 0.1, 0.04);
  }

  // ---------------------------------------------------------- the staircase
  // Steps for slots 1..15; slot 0 is the landing at floor level.
  {
    // Angle of the door center as seen from the axis: the vestibule lies
    // toward +z, so a_door = π/2. Climb phase φ = a_door − a increases
    // clockwise (seen from above); slot s spans φ ∈ [sΔ−Δ/2, sΔ+Δ/2) and
    // its tread top sits at s·STEP_RISE. Slot 0 is the landing.
    const a_door = Math.PI / 2;
    for (let s = 1; s < D.STAIR_STEPS; s++) {
      const a1 = a_door - s * D.STEP_ANG + D.STEP_ANG / 2;
      const a0 = a1 - D.STEP_ANG;
      const g = stepGeometry(a0, a1, 0.07);
      g.translate(stairAxis.x, s * D.STEP_RISE, stairAxis.z);
      wood.push(g);
    }
    // The landing (slot 0, widened a half-slot each way) at floor level...
    {
      const g = stepGeometry(a_door - D.STEP_ANG, a_door + D.STEP_ANG, 0.07);
      g.translate(stairAxis.x, 0, stairAxis.z);
      wood.push(g);
    }
    // ...and a threshold patch bridging the well's rim to the vestibule
    // floor (the slab's circular hole bites slightly through the doorway).
    box(stone, stairAxis.x, -0.036, -D.VEST_W / 2 - 0.005, 2 * D.STAIR_DOOR_HALF + 0.04, 0.068, 0.24);
    // Central column.
    const col = new THREE.CylinderGeometry(D.STAIR_COL_R, D.STAIR_COL_R, D.FLOOR_PITCH, 12);
    col.translate(stairAxis.x, D.FLOOR_PITCH / 2, stairAxis.z);
    stone.push(col);
    // Outer shell: full-height arcs beside the door, plus an arc above it.
    const doorHalfAng = Math.asin(D.STAIR_DOOR_HALF / D.STAIR_R);
    const shellLo = new THREE.CylinderGeometry(
      D.STAIR_R + 0.02,
      D.STAIR_R + 0.02,
      D.FLOOR_PITCH,
      24,
      1,
      true,
      // theta measured from +z axis... easier: build full ring minus door arc.
      a_door + doorHalfAng - Math.PI / 2,
      Math.PI * 2 - 2 * doorHalfAng,
    );
    shellLo.translate(stairAxis.x, D.FLOOR_PITCH / 2, stairAxis.z);
    stone.push(shellLo);
    const shellDoorTop = new THREE.CylinderGeometry(
      D.STAIR_R + 0.02,
      D.STAIR_R + 0.02,
      D.FLOOR_PITCH - D.DOOR_H,
      8,
      1,
      true,
      a_door - doorHalfAng - Math.PI / 2,
      2 * doorHalfAng,
    );
    shellDoorTop.translate(stairAxis.x, D.DOOR_H + (D.FLOOR_PITCH - D.DOOR_H) / 2, stairAxis.z);
    stone.push(shellDoorTop);
  }

  // ------------------------------------------------------------ the railing
  {
    const rv = D.hexVertices(D.RAIL_R);
    for (let k = 0; k < 6; k++) {
      const aV = rv[k];
      const bV = rv[(k + 1) % 6];
      // Posts.
      box(brass, aV[0], D.RAIL_H / 2, aV[1], 0.045, D.RAIL_H, 0.045);
      // Top rail.
      const mx = (aV[0] + bV[0]) / 2;
      const mz = (aV[1] + bV[1]) / 2;
      const len = Math.hypot(bV[0] - aV[0], bV[1] - aV[1]);
      const yawR = Math.atan2(bV[0] - aV[0], bV[1] - aV[1]);
      box(brass, mx, D.RAIL_H - 0.02, mz, 0.05, 0.04, len, yawR);
      box(brass, mx, D.RAIL_H * 0.5, mz, 0.03, 0.025, len, yawR);
      seg(segments, aV[0], aV[1], bV[0], bV[1], 0, D.RAIL_H, 0.03);
    }
  }

  // -------------------------------------------------------------- the lamps
  // "Two, transversally placed, in each hexagon" — half-sunk in the ceiling,
  // north and south of the shaft.
  const lampCenters = [
    { x: 0, y: D.CEIL_H - 0.07, z: -1.1 },
    { x: 0, y: D.CEIL_H - 0.07, z: 1.1 },
  ];
  for (const lc of lampCenters) {
    const s = new THREE.SphereGeometry(D.LAMP_R, 18, 12);
    s.translate(lc.x, lc.y, lc.z);
    lampsGeo.push(s);
    const collar = new THREE.CylinderGeometry(D.LAMP_R + 0.025, D.LAMP_R + 0.04, 0.05, 12);
    collar.translate(lc.x, D.CEIL_H - 0.02, lc.z);
    brass.push(collar);
  }

  // ---------------------------------------------------- stairwell containment
  // The well's lateral collision is handled analytically in the controller
  // (cylinder + door sector), so no segments here.

  // Extrusions are non-indexed while boxes/cylinders are indexed;
  // mergeGeometries requires uniformity.
  const merge = (parts: THREE.BufferGeometry[]): THREE.BufferGeometry =>
    mergeGeometries(parts.map((g) => (g.index ? g.toNonIndexed() : g)));

  return {
    wood: merge(wood),
    stone: merge(stone),
    brass: merge(brass),
    lamps: merge(lampsGeo),
    bookMatrices,
    wallYaws,
    segments,
    stairAxis,
    slabStairAxis,
    mirrorCenter,
    lampCenters,
  };
}

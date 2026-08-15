/**
 * Physical dimensions of the Library, in meters.
 *
 * Everything follows from Borges's constraints: shelves floor-to-ceiling at
 * "scarcely more than a librarian's height"; 32 uniform volumes to a shelf,
 * five shelves to a side; a narrow vestibule with two very small closets
 * (sleep standing up); a spiral stair; very low railings around the shaft.
 * This module is three.js-free so the test suite can audit it.
 */

export const SQ3 = Math.sqrt(3);

/** Hexagon side length: 32 book spines plus the bookcase frame. */
export const HEX_SIDE = 1.8;
/** Apothem: distance from hexagon center to the middle of a wall. */
export const HEX_APO = (HEX_SIDE * SQ3) / 2; // ≈ 1.5588

/** Ceiling "scarcely exceeds the height of a normal librarian". */
export const CEIL_H = 2.05;
/** Structural slab between floors. */
export const SLAB_H = 0.45;
/** Floor-to-floor distance. */
export const FLOOR_PITCH = CEIL_H + SLAB_H; // 2.5

/** The narrow vestibule (zaguán) between galleries. */
export const VEST_LEN = 3.0;
export const VEST_W = 1.1;
export const DOOR_W = 1.1; // the free sides open fully into the vestibule
export const DOOR_H = 1.92;

/** Corridor period: hexagon plus one vestibule. */
export const UNIT_PITCH = 2 * HEX_APO + VEST_LEN; // ≈ 6.1177

/** Central ventilation shaft (hexagonal), and its very low railing. */
export const SHAFT_SIDE = 0.62;
export const SHAFT_APO = (SHAFT_SIDE * SQ3) / 2;
export const RAIL_R = SHAFT_SIDE + 0.1; // railing vertex radius
export const RAIL_H = 0.4;

/** Bookcases: they ARE the four shelved walls, floor to ceiling. */
export const CASE_DEPTH = 0.26;
export const BOARD_T = 0.035;
/** Vertical module: 5 book rows + 6 boards fill exactly CEIL_H. */
export const ROW_PITCH = (CEIL_H - BOARD_T) / 5; // board + row of books
export const ROW_CLEAR = ROW_PITCH - BOARD_T;

/** Books of uniform format. */
export const BOOK_H = 0.3;
export const BOOK_D = 0.215;
export const BOOK_T = 0.04;
export const BOOK_PITCH = 0.0475; // spine-to-spine along the shelf
export const BOOK_SPAN = 32 * BOOK_PITCH; // 1.52
export const BOOK_RECESS = 0.022; // spines sit slightly inside the case

/** Closets: "one may sleep standing up" in a space this size, just. */
export const CLOSET_W = 0.66; // along the corridor
export const CLOSET_D = 0.8; // away from the corridor
export const CLOSET_DOOR_W = 0.5;
export const CLOSET_DOOR_H = 1.85;

/** Spiral staircase. */
export const STAIR_R = 0.85; // outer well radius
export const STAIR_COL_R = 0.2; // central column
export const STAIR_STEPS = 16; // slots per revolution (one is the landing)
export const STEP_RISE = FLOOR_PITCH / STAIR_STEPS; // 0.15625
export const STEP_ANG = (Math.PI * 2) / STAIR_STEPS;
/** Axis offset from the vestibule centerline (z, north negative). */
export const STAIR_AXIS_Z = -(VEST_W / 2 + 0.78);
/** Axis position along the vestibule (x, from the hexagon's east wall). */
export const STAIR_AXIS_X = 2.2;
/** Half-width of the chord opening between vestibule and stairwell. */
export const STAIR_DOOR_HALF = Math.sqrt(STAIR_R * STAIR_R - 0.78 * 0.78); // ≈ 0.338

/** Mirror in the vestibule ("faithfully duplicates appearances"). */
export const MIRROR_W = 0.95;
export const MIRROR_Y0 = 0.35;
export const MIRROR_Y1 = 1.85;

/** Lamps: "two, transversally placed, in each hexagon". */
export const LAMP_R = 0.09;
export const LAMP_Y = 1.78;
export const LAMP_RADIUS = HEX_SIDE * 0.8; // distance from hexagon center

/** The player, a normal librarian. */
export const EYE_H = 1.62;
export const PLAYER_R = 0.26;
export const WALK_SPEED = 2.1;
export const HURRY_SPEED = 3.5;
export const GRAVITY = 18;
export const JUMP_V = 4.8; // enough to clamber over the very low railing
export const STEP_UP = 0.2; // max ledge climbed in stride
export const SNAP_DOWN = 0.32; // stick to stairs when descending

/** Wall thickness used for door walls and partitions. */
export const WALL_T = 0.12;

/** Hexagon vertex angles: flats face east/west (the two free sides). */
export function hexVertexAngle(k: number): number {
  return (Math.PI / 6) + (k * Math.PI) / 3; // 30° + 60°k
}

/** Vertices of a hexagon with side s, in XZ. */
export function hexVertices(s: number): [number, number][] {
  const v: [number, number][] = [];
  for (let k = 0; k < 6; k++) {
    const a = hexVertexAngle(k);
    v.push([s * Math.cos(a), s * Math.sin(a)]);
  }
  return v;
}

/** Point-in-hexagon test (hexagon with side s, oriented as above). */
export function insideHex(x: number, z: number, s: number): boolean {
  const apo = (s * SQ3) / 2;
  if (Math.abs(x) > apo) return false;
  // The four slanted walls: |±x·cos30 ± z·sin... | use symmetry:
  return Math.abs(z) <= s - Math.abs(x) / SQ3 + 1e-9 && Math.abs(z) <= s;
}

/**
 * Shelf walls, in the order shown to the reader: counted clockwise (seen
 * from above) starting beside the east door. Each entry holds the outward
 * angle of the wall's *inward* normal and its two hexagon vertices.
 *   wall 0: southeast, wall 1: southwest, wall 2: northwest, wall 3: northeast
 */
export const SHELF_WALLS: { v0: number; v1: number }[] = [
  { v0: 0, v1: 1 }, // SE
  { v0: 1, v1: 2 }, // SW
  { v0: 3, v1: 4 }, // NW
  { v0: 4, v1: 5 }, // NE
];

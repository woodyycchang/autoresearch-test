/**
 * Where things are.
 *
 * The Library's galleries form straight corridors of hexagons (coordinate c,
 * an integer modulo 25^1,312,000) stacked on endless floors (coordinate f).
 * A hexagon's *identity* — the thing that decides its books — is
 *
 *     h = (c + K·f) mod 25^1,312,000
 *
 * for a fixed huge constant K. Travel far enough along a corridor and the
 * identities wrap: "The Library is unlimited and cyclical... the same
 * volumes are repeated in the same disorder — which, thus repeated, would
 * be an order: the Order."
 */

import { addInt, copy, Digits, withScaled, zero } from "./bignum";
import { GLOBAL_SEED, SHELVES, VOLUMES, WALLS } from "./constants";
import { BASE } from "./bignum";
import { hashBytes128, Sfc32 } from "./rng";

/** Spatial coordinate of a hexagon: corridor position and floor. */
export interface HexCoord {
  /** Position along the corridor, mod 25^1,312,000 (little-endian base-25). */
  c: Digits;
  /** Floor number; 0 is where you wake. Negative floors descend. */
  f: number;
}

/** A specific volume inside a hexagon. */
export interface BookLocation {
  coord: HexCoord;
  /** Shelf wall, 0..3, counted clockwise from the corridor exit. */
  wall: number;
  /** Shelf, 0..4, top to bottom. */
  shelf: number;
  /** Volume, 0..31, left to right. */
  volume: number;
}

/** Floors are unbounded in the fiction; the engine promises exactness here. */
export const MAX_FLOOR = 2 ** 40;

/** The fixed floor-mixing constant K. */
export const K: Digits = (() => {
  const k = zero();
  Sfc32.fromString(GLOBAL_SEED, "floor constant K").fillDigits(k, BASE);
  return k;
})();

/** Identity of the hexagon at a spatial coordinate. */
export function hexId(coord: HexCoord): Digits {
  if (Math.abs(coord.f) > MAX_FLOOR) throw new Error("floor out of the engine's exact range");
  return withScaled(coord.c, K, coord.f);
}

/** Corridor coordinate of the hexagon with identity `h` on floor `f`: c = h - K·f. */
export function corridorForHex(h: Digits, f: number): Digits {
  return withScaled(h, K, -f);
}

export function coordCopy(coord: HexCoord): HexCoord {
  return { c: copy(coord.c), f: coord.f };
}

/** Step one hexagon along the corridor (+1 east, -1 west). */
export function stepCorridor(coord: HexCoord, dir: 1 | -1): HexCoord {
  const c = copy(coord.c);
  addInt(c, dir);
  return { c, f: coord.f };
}

export function stepFloor(coord: HexCoord, dir: 1 | -1): HexCoord {
  return { c: copy(coord.c), f: coord.f + dir };
}

/** Origin: the hexagon where every visitor first wakes. */
export function originCoord(): HexCoord {
  return { c: zero(), f: 0 };
}

const NAME_ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"; // 32 glyphs, no i/l/o/u

/**
 * Human-pronounceable name of a hexagon, derived from its identity.
 * A label, not an address: the address is the identity itself.
 */
export function hexName(h: Digits): string {
  const [a, b, c, d] = hashBytes128(h, 0x68657861, 0x6e616d65);
  const words = [a, b, c, d];
  let name = "";
  for (let w = 0; w < 4; w++) {
    if (w > 0) name += "-";
    let v = words[w];
    for (let i = 0; i < 4; i++) {
      name += NAME_ALPHABET[v & 31];
      v >>>= 5;
    }
  }
  return name;
}

export function slotIndex(wall: number, shelf: number, volume: number): number {
  if (wall < 0 || wall >= WALLS || shelf < 0 || shelf >= SHELVES || volume < 0 || volume >= VOLUMES) {
    throw new Error(`no such shelf position: wall ${wall}, shelf ${shelf}, volume ${volume}`);
  }
  return (wall * SHELVES + shelf) * VOLUMES + volume;
}

/**
 * The bijection at the heart of the Library.
 *
 * A book is a string of 1,312,000 symbols from a 25-letter alphabet; a
 * hexagon's identity is an integer with exactly that many base-25 digits.
 * For each of the 640 shelf positions (wall × shelf × volume) we define a
 * *permutation* of that space — a balanced Feistel network over digit
 * strings, with per-round digit streams derived from a hash of the opposite
 * half. Because it is a bijection:
 *
 *   - every possible 410-page book exists at every shelf position, in
 *     exactly one hexagon per cosmic period;
 *   - the same place always holds the same book;
 *   - given any text, we can *invert* the network and compute the precise
 *     hexagon that shelves it.
 *
 * Four rounds give full diffusion (Luby–Rackoff); this is statistical
 * scrambling, not cryptography, and it is fixed forever.
 */

import { BASE, DIGITS, Digits } from "./bignum";
import { GLOBAL_SEED } from "./constants";
import { hashBytes128, hashString, Sfc32 } from "./rng";

export const ROUNDS = 4;
const HALF = DIGITS / 2;

const SEED_LO = hashString(GLOBAL_SEED, 0x01010101);

/** Per-(round, slot) key material, derived once from the global seed. */
function roundKeys(round: number, slot: number): [number, number] {
  return [
    hashString(`round ${round} slot ${slot}`, SEED_LO),
    hashString(`slot ${slot} round ${round}`, ~SEED_LO >>> 0),
  ];
}

/** Round function: digest one half, stream BASE-digits into `out`. */
function roundDigits(half: Digits, round: number, slot: number, out: Uint8Array): void {
  const [k0, k1] = roundKeys(round, slot);
  const [s0, s1, s2, s3] = hashBytes128(half, k0, k1);
  const rng = new Sfc32(s0, s1, s2, s3);
  rng.fillDigits(out, BASE);
}

function run(input: Digits, slot: number, decrypt: boolean): Digits {
  if (input.length !== DIGITS) throw new Error(`feistel expects ${DIGITS} digits`);
  let L = input.slice(0, HALF);
  let R = input.slice(HALF);
  const g = new Uint8Array(HALF);
  if (!decrypt) {
    // (L, R) -> (R, L + G_r(R))
    for (let r = 0; r < ROUNDS; r++) {
      roundDigits(R, r, slot, g);
      for (let i = 0; i < HALF; i++) {
        const v = L[i] + g[i];
        L[i] = v >= BASE ? v - BASE : v;
      }
      const t = L;
      L = R;
      R = t;
    }
  } else {
    // inverse round: (A, B) -> (B - G_r(A), A)
    for (let r = ROUNDS - 1; r >= 0; r--) {
      roundDigits(L, r, slot, g);
      for (let i = 0; i < HALF; i++) {
        const v = R[i] - g[i];
        R[i] = v < 0 ? v + BASE : v;
      }
      const t = L;
      L = R;
      R = t;
    }
  }
  const out = new Uint8Array(DIGITS);
  out.set(L, 0);
  out.set(R, HALF);
  return out;
}

/** Hexagon identity digits → book content digits, for one shelf position. */
export function bookFromHex(hexId: Digits, slot: number): Digits {
  return run(hexId, slot, false);
}

/** Book content digits → the hexagon identity that shelves it. */
export function hexFromBook(book: Digits, slot: number): Digits {
  return run(book, slot, true);
}

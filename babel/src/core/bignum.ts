/**
 * Arithmetic on Library-sized integers.
 *
 * A hexagon's identity, and its coordinate along a gallery corridor, are
 * integers modulo 25^1,312,000 — numbers of 1.83 million decimal digits.
 * We never convert them to anything: they live as little-endian arrays of
 * base-25 digits (Uint8Array), and every operation we need is linear.
 */

import { BOOK_CHARS } from "./constants";
import { SYMBOL_COUNT } from "./alphabet";

export type Digits = Uint8Array;

export const DIGITS = BOOK_CHARS; // one digit per character of a book
export const BASE = SYMBOL_COUNT; // 25

export function zero(): Digits {
  return new Uint8Array(DIGITS);
}

export function copy(a: Digits): Digits {
  return a.slice();
}

export function equal(a: Digits, b: Digits): boolean {
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}

/** a += k for a small signed integer k (|k| < 2^52), wrapping mod BASE^DIGITS. */
export function addInt(a: Digits, k: number): void {
  let carry = k;
  for (let i = 0; i < a.length && carry !== 0; i++) {
    const v = a[i] + carry;
    const d = ((v % BASE) + BASE) % BASE;
    carry = (v - d) / BASE;
    a[i] = d;
  }
  // Any leftover carry wraps away: arithmetic is modulo BASE^DIGITS.
}

/**
 * a += b * m for small signed integer m, wrapping mod BASE^DIGITS.
 * |m| must stay below 2^45 so per-digit intermediates remain exact doubles.
 */
export function addScaled(a: Digits, b: Digits, m: number): void {
  if (!Number.isInteger(m) || Math.abs(m) > 2 ** 45) {
    throw new Error("addScaled: scale out of exact-integer range");
  }
  if (m === 0) return;
  let carry = 0;
  for (let i = 0; i < a.length; i++) {
    const v = a[i] + b[i] * m + carry;
    const d = ((v % BASE) + BASE) % BASE;
    carry = (v - d) / BASE;
    a[i] = d;
  }
}

/** Returns a fresh array holding (a + b*m) mod BASE^DIGITS. */
export function withScaled(a: Digits, b: Digits, m: number): Digits {
  const out = copy(a);
  addScaled(out, b, m);
  return out;
}

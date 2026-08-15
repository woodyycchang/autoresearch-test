/**
 * Deterministic hashing and pseudo-randomness for the Library.
 *
 * Nothing here is cryptographic and nothing needs to be: the Feistel rounds
 * only need a fast, well-mixed, *fixed-forever* function so that every place
 * in the Library always holds the same book, in every browser, in every year.
 */

const P1 = 0x9e3779b1;
const P2 = 0x85ebca77;
const P3 = 0xc2b2ae3d;
const P4 = 0x27d4eb2f;
const P5 = 0x165667b1;

function rotl(x: number, r: number): number {
  return (x << r) | (x >>> (32 - r));
}

function avalanche(h: number): number {
  h ^= h >>> 15;
  h = Math.imul(h, P2);
  h ^= h >>> 13;
  h = Math.imul(h, P3);
  h ^= h >>> 16;
  return h >>> 0;
}

/** Hash a string to a 32-bit value (FNV/xxh hybrid). */
export function hashString(s: string, seed = 0): number {
  let h = (P5 + seed) >>> 0;
  for (let i = 0; i < s.length; i++) {
    h = Math.imul(h ^ s.charCodeAt(i), P1);
    h = rotl(h, 11);
  }
  return avalanche(h ^ s.length);
}

/**
 * Hash a byte array plus key material into four 32-bit lanes.
 * Four-lane xxh32-style core; every input byte influences the result.
 */
export function hashBytes128(
  a: Uint8Array,
  k0: number,
  k1: number,
): [number, number, number, number] {
  let h0 = (P1 + k0) >>> 0;
  let h1 = (P2 ^ k1) >>> 0;
  let h2 = (P3 + Math.imul(k0 ^ 0x5bd1e995, P4)) >>> 0;
  let h3 = (P5 ^ Math.imul(k1 + 0x52dce729, P1)) >>> 0;
  const n = a.length;
  let i = 0;
  for (; i + 16 <= n; i += 16) {
    const v0 = a[i] | (a[i + 1] << 8) | (a[i + 2] << 16) | (a[i + 3] << 24);
    const v1 = a[i + 4] | (a[i + 5] << 8) | (a[i + 6] << 16) | (a[i + 7] << 24);
    const v2 = a[i + 8] | (a[i + 9] << 8) | (a[i + 10] << 16) | (a[i + 11] << 24);
    const v3 = a[i + 12] | (a[i + 13] << 8) | (a[i + 14] << 16) | (a[i + 15] << 24);
    h0 = Math.imul(rotl((h0 + Math.imul(v0, P2)) | 0, 13), P1);
    h1 = Math.imul(rotl((h1 + Math.imul(v1, P2)) | 0, 13), P1);
    h2 = Math.imul(rotl((h2 + Math.imul(v2, P2)) | 0, 13), P1);
    h3 = Math.imul(rotl((h3 + Math.imul(v3, P2)) | 0, 13), P1);
  }
  let tail = 0;
  for (; i < n; i++) tail = Math.imul(tail ^ a[i], P4) + 1;
  // Cross-pollinate the lanes so each output word depends on all input.
  const m = (rotl(h0, 1) + rotl(h1, 7) + rotl(h2, 12) + rotl(h3, 18)) | 0;
  const x0 = avalanche((m ^ tail ^ n) >>> 0);
  const x1 = avalanche((h0 ^ Math.imul(h1, P3)) >>> 0);
  const x2 = avalanche((h2 ^ Math.imul(h3, P2)) >>> 0);
  const x3 = avalanche((m ^ Math.imul(x1 ^ x2, P4)) >>> 0);
  return [x0, x1, x2, x3];
}

/** sfc32: small, fast, excellent 32-bit PRNG. Deterministic forever. */
export class Sfc32 {
  private a: number;
  private b: number;
  private c: number;
  private d: number;

  constructor(s0: number, s1: number, s2: number, s3: number) {
    this.a = s0 >>> 0;
    this.b = s1 >>> 0;
    this.c = s2 >>> 0;
    this.d = s3 >>> 0;
    // Scramble the state so weak seeds (zeros) still diverge.
    for (let i = 0; i < 12; i++) this.next();
  }

  static fromString(...parts: (string | number)[]): Sfc32 {
    const s = parts.join(" ");
    return new Sfc32(
      hashString(s, 0x243f6a88),
      hashString(s, 0x85a308d3),
      hashString(s, 0x13198a2e),
      hashString(s, 0x03707344),
    );
  }

  /** Uniform 32-bit unsigned integer. */
  next(): number {
    const t = (((this.a + this.b) | 0) + this.d) | 0;
    this.d = (this.d + 1) | 0;
    this.a = this.b ^ (this.b >>> 9);
    this.b = (this.c + (this.c << 3)) | 0;
    this.c = (this.c << 21) | (this.c >>> 11);
    this.c = (this.c + t) | 0;
    return t >>> 0;
  }

  /** Uniform float in [0, 1). */
  float(): number {
    return this.next() / 4294967296;
  }

  /** Uniform integer in [0, n) without modulo bias. */
  int(n: number): number {
    if (n <= 0) throw new Error("int(n) needs n > 0");
    const limit = 4294967296 - (4294967296 % n);
    for (;;) {
      const v = this.next();
      if (v < limit) return v % n;
    }
  }

  /** Fill `out` with uniform digits in [0, base). */
  fillDigits(out: Uint8Array, base: number): void {
    const limit = 4294967296 - (4294967296 % base);
    for (let i = 0; i < out.length; i++) {
      let v = this.next();
      while (v >= limit) v = this.next();
      out[i] = v % base;
    }
  }
}

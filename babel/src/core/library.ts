/**
 * The Library's public face: fetch any book, read any page, and — given a
 * piece of text — name the exact hexagon, wall, shelf, volume and page where
 * it has stood since before you were born.
 */

import { digitsToText, textToDigits, transliterate, Transliteration } from "./alphabet";
import { corridorForHex, hexId, HexCoord, hexName, BookLocation, slotIndex } from "./address";
import { BASE, Digits } from "./bignum";
import { BOOK_CHARS, GLOBAL_SEED, PAGE_CHARS, PAGES, SHELVES, VOLUMES, WALLS } from "./constants";
import { bookFromHex, hexFromBook } from "./feistel";
import { hashBytes128, Sfc32 } from "./rng";

export interface Book {
  /** 1,312,000 symbol indices, reading order: page 1 line 1 col 1 onward. */
  digits: Digits;
  /** Letters on the spine ("they do not prefigure what the pages will say"). */
  spine: string;
  location: BookLocation;
  hexName: string;
}

export type SeekMode = "context" | "alone";

export interface SeekResult {
  location: BookLocation;
  /** 0-based page holding the first character of the match. */
  page: number;
  /** Offset of the match within the whole book, in characters. */
  offset: number;
  length: number;
  transliteration: Transliteration;
  mode: SeekMode;
  /** Which of the endless copies this is (0 = the canonical find). */
  copy: number;
}

const SPINE_MIN = 3;
const SPINE_MAX = 14;
const SPINE_LETTERS = "abcdefghijlmnoprstuvxy"; // letters only on spines

function spineFor(h: Digits, slot: number): string {
  const [s0, s1, s2, s3] = hashBytes128(h, 0x7370696e ^ slot, Math.imul(slot + 1, 0x9e3779b1));
  const rng = new Sfc32(s0, s1, s2, s3);
  const len = SPINE_MIN + rng.int(SPINE_MAX - SPINE_MIN + 1);
  let out = "";
  let sinceSpace = 0;
  for (let i = 0; i < len; i++) {
    // Occasional word break, never leading/trailing, never doubled.
    if (i > 0 && i < len - 1 && sinceSpace >= 2 && rng.float() < 0.18) {
      out += " ";
      sinceSpace = 0;
    } else {
      out += SPINE_LETTERS[rng.int(SPINE_LETTERS.length)];
      sinceSpace++;
    }
  }
  return out;
}

/** Small LRU for generated books; each is ~1.3 MB. */
const cache = new Map<string, Book>();
const CACHE_MAX = 24;

function cacheKey(name: string, slot: number): string {
  return `${name}/${slot}`;
}

/** Fetch the book standing at a location. Deterministic, forever. */
export function getBook(location: BookLocation): Book {
  const slot = slotIndex(location.wall, location.shelf, location.volume);
  const h = hexId(location.coord);
  const name = hexName(h);
  const key = cacheKey(name, slot);
  const hit = cache.get(key);
  if (hit) {
    cache.delete(key);
    cache.set(key, hit);
    return hit;
  }
  const digits = bookFromHex(h, slot);
  const book: Book = { digits, spine: spineFor(h, slot), location, hexName: name };
  cache.set(key, book);
  if (cache.size > CACHE_MAX) {
    const oldest = cache.keys().next().value as string;
    cache.delete(oldest);
  }
  return book;
}

/** Text of one page (0-based), exactly 3,200 characters. */
export function pageText(book: Book, page: number): string {
  if (page < 0 || page >= PAGES) throw new Error(`books have ${PAGES} pages; there is no page ${page + 1}`);
  const start = page * PAGE_CHARS;
  return digitsToText(book.digits, start, start + PAGE_CHARS);
}

/** Spine letters for a volume without generating its contents. */
export function spineAt(coord: HexCoord, wall: number, shelf: number, volume: number): string {
  return spineFor(hexId(coord), slotIndex(wall, shelf, volume));
}

export class SeekError extends Error {}

/**
 * Find a book containing `input`.
 *
 * Deterministic: the same text, mode and copy-index always lead to the same
 * volume — the Library does not rearrange itself between visits. `copy`
 * selects among the endless other books that also contain the text.
 */
export function seek(input: string, mode: SeekMode = "context", copyIdx = 0): SeekResult {
  const translit = transliterate(input);
  const clean = translit.text;
  if (clean.length === 0) {
    throw new SeekError("nothing of that text survives in the Library's alphabet");
  }
  if (clean.length > BOOK_CHARS) {
    throw new SeekError(`no book is long enough: texts may be at most ${BOOK_CHARS.toLocaleString()} characters`);
  }

  const rng = Sfc32.fromString(GLOBAL_SEED, "seek", mode, copyIdx, clean);

  // Compose the target book.
  const digits = new Uint8Array(BOOK_CHARS); // mode "alone": all spaces
  let offset = 0;
  if (mode === "context") {
    rng.fillDigits(digits, BASE);
    offset = rng.int(BOOK_CHARS - clean.length + 1);
  }
  digits.set(textToDigits(clean), offset);

  // Choose which shelf position the volume occupies...
  const wall = rng.int(WALLS);
  const shelf = rng.int(SHELVES);
  const volume = rng.int(VOLUMES);
  const slot = slotIndex(wall, shelf, volume);

  // ...invert the Library's permutation to learn the hexagon's identity...
  const h = hexFromBook(digits, slot);

  // ...and place that identity in space.
  const f = rng.int(65536) - 32768;
  const c = corridorForHex(h, f);

  return {
    location: { coord: { c, f }, wall, shelf, volume },
    page: Math.floor(offset / PAGE_CHARS),
    offset,
    length: clean.length,
    transliteration: translit,
    mode,
    copy: copyIdx,
  };
}

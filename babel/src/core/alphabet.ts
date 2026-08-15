/**
 * The twenty-five orthographical symbols.
 *
 * Borges (footnote to the story): "The original manuscript does not contain
 * digits or capital letters. The punctuation has been limited to the comma
 * and the period. These two signs, the space, and the twenty-two letters of
 * the alphabet are the twenty-five symbols considered sufficient."
 *
 * Borges never lists the twenty-two letters. We drop k, q, w, z from the
 * Latin 26: every letter that appears in the story's own specimens
 * ("dhcmrlchtdj", "axaxaxas mlö", "oh time thy pyramids") survives, and the
 * casualties are the rarest letters of the Romance alphabets. Seek-texts are
 * transliterated the way a librarian would copy them: k→c, q→c, w→v, z→s.
 */

export const SYMBOLS = " abcdefghijlmnoprstuvxy,.";
export const SYMBOL_COUNT = SYMBOLS.length; // 25
export const SPACE = 0; // index of the space symbol; a "blank" book is all zeroes

const INDEX: Map<string, number> = new Map();
for (let i = 0; i < SYMBOLS.length; i++) INDEX.set(SYMBOLS[i], i);

/** Letter substitutions a librarian applies when copying foreign text. */
const SUBSTITUTIONS: Record<string, string> = {
  k: "c",
  q: "c",
  w: "v",
  z: "s",
  ";": ",",
  ":": ",",
  "!": ".",
  "?": ".",
  "-": " ",
  "–": " ", // –
  "—": " ", // —
  "/": " ",
  "\\": " ",
  "|": " ",
  "_": " ",
  "\n": " ",
  "\r": "",
  "\t": " ",
  "'": "",
  "‘": "",
  "’": "",
  '"': "",
  "“": "",
  "”": "",
  "(": "",
  ")": "",
  "[": "",
  "]": "",
  "{": "",
  "}": "",
  "…": ".", // …
};

export interface Transliteration {
  /** The text as it exists in the Library's alphabet. */
  text: string;
  /** True when the input had to be altered at all. */
  changed: boolean;
  /** Substitutions performed, e.g. "k→c". */
  substituted: string[];
  /** Characters with no representation, silently omitted. */
  dropped: string[];
}

/**
 * Convert arbitrary user text into the Library's 25-symbol alphabet,
 * reporting every liberty taken.
 */
export function transliterate(input: string): Transliteration {
  const substituted = new Set<string>();
  const dropped = new Set<string>();
  let out = "";
  // Decompose accents so "mlö" becomes "mlo" rather than vanishing.
  const decomposed = input.normalize("NFD");
  for (const raw of decomposed) {
    // Strip combining diacritics.
    if (/\p{M}/u.test(raw)) {
      substituted.add("accent removed");
      continue;
    }
    const lower = raw.toLowerCase();
    if (lower !== raw) substituted.add(`${raw}→${lower}`);
    let ch = lower;
    if (ch in SUBSTITUTIONS) {
      const repl = SUBSTITUTIONS[ch];
      if (repl !== ch) {
        if (/[a-z]/.test(ch)) substituted.add(`${ch}→${repl}`);
        else if (repl === "") substituted.add(`${JSON.stringify(ch)} removed`);
        else substituted.add(`${ch}→${repl}`);
      }
      ch = repl;
    }
    if (ch === "") continue;
    if (INDEX.has(ch)) {
      out += ch;
    } else {
      dropped.add(raw);
    }
  }
  const changed = substituted.size > 0 || dropped.size > 0 || out !== input;
  return { text: out, changed, substituted: [...substituted], dropped: [...dropped] };
}

/** Text (already in the alphabet) → symbol indices. Throws on aliens. */
export function textToDigits(text: string): Uint8Array {
  const out = new Uint8Array(text.length);
  for (let i = 0; i < text.length; i++) {
    const d = INDEX.get(text[i]);
    if (d === undefined) throw new Error(`character ${JSON.stringify(text[i])} is not among the 25 symbols`);
    out[i] = d;
  }
  return out;
}

/** Symbol indices → text. */
export function digitsToText(digits: Uint8Array, start = 0, end = digits.length): string {
  const parts: string[] = [];
  const CHUNK = 8192;
  for (let i = start; i < end; i += CHUNK) {
    const stop = Math.min(i + CHUNK, end);
    let s = "";
    for (let j = i; j < stop; j++) s += SYMBOLS[digits[j]];
    parts.push(s);
  }
  return parts.join("");
}

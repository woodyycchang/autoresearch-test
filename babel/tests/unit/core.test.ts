import { describe, expect, it } from "vitest";
import {
  digitsToText,
  SPACE,
  SYMBOL_COUNT,
  SYMBOLS,
  textToDigits,
  transliterate,
} from "../../src/core/alphabet";
import {
  corridorForHex,
  hexId,
  hexName,
  originCoord,
  slotIndex,
  stepCorridor,
  stepFloor,
} from "../../src/core/address";
import { addInt, addScaled, BASE, copy, DIGITS, equal, zero } from "../../src/core/bignum";
import {
  BOOK_CHARS,
  BOOKS_PER_HEX,
  COLS,
  LINES,
  PAGE_CHARS,
  PAGES,
  SHELVES,
  SLOTS,
  VOLUMES,
  WALLS,
} from "../../src/core/constants";
import { bookFromHex, hexFromBook } from "../../src/core/feistel";
import { getBook, pageText, seek } from "../../src/core/library";
import { Sfc32 } from "../../src/core/rng";

function randomDigits(seed: string): Uint8Array {
  const d = zero();
  Sfc32.fromString("test", seed).fillDigits(d, BASE);
  return d;
}

describe("fidelity to Borges's description", () => {
  it("uses exactly twenty-five orthographical symbols", () => {
    expect(SYMBOL_COUNT).toBe(25);
    expect(new Set(SYMBOLS).size).toBe(25);
  });
  it("the symbols are twenty-two letters, the comma, the period, the space", () => {
    const letters = [...SYMBOLS].filter((c) => /[a-z]/.test(c));
    expect(letters.length).toBe(22);
    expect(SYMBOLS).toContain(",");
    expect(SYMBOLS).toContain(".");
    expect(SYMBOLS).toContain(" ");
  });
  it("each book is of four hundred ten pages", () => {
    expect(PAGES).toBe(410);
  });
  it("each page, of forty lines, each line, of some eighty letters", () => {
    expect(LINES).toBe(40);
    expect(COLS).toBe(80);
    expect(PAGE_CHARS).toBe(3200);
    expect(BOOK_CHARS).toBe(1_312_000);
  });
  it("twenty shelves, five per side, cover all sides except two", () => {
    expect(WALLS).toBe(4); // six sides minus the two free ones
    expect(SHELVES).toBe(5);
    expect(WALLS * SHELVES).toBe(20);
  });
  it("each shelf contains thirty-two books of uniform format", () => {
    expect(VOLUMES).toBe(32);
    expect(BOOKS_PER_HEX).toBe(640);
  });
  it("the story's own specimens survive transliteration untouched", () => {
    for (const sample of ["dhcmrlchtdj", "oh time thy pyramids", "axaxaxas mlo"]) {
      expect(transliterate(sample).text).toBe(sample);
    }
  });
});

describe("alphabet", () => {
  it("round-trips text through digits", () => {
    const s = "the faithful catalogue, and the silence.";
    expect(digitsToText(textToDigits(s))).toBe(s);
  });
  it("transliterates the missing letters the way a librarian would", () => {
    const t = transliterate("The Quick brown koala, walks; amazed!");
    expect(t.text).toBe("the cuicc brovn coala, valcs, amased.");
    expect(t.changed).toBe(true);
  });
  it("strips accents instead of dropping the letter", () => {
    expect(transliterate("axaxaxas mlö").text).toBe("axaxaxas mlo");
  });
  it("drops what cannot be written and reports it", () => {
    const t = transliterate("page 42");
    expect(t.text).toBe("page ");
    expect(t.dropped).toContain("4");
  });
  it("a blank book is all space symbols at index 0", () => {
    expect(SPACE).toBe(0);
    expect(SYMBOLS[0]).toBe(" ");
  });
});

describe("bignum digit arithmetic", () => {
  it("addInt carries across digit boundaries", () => {
    const a = zero();
    addInt(a, BASE * BASE * 3 + BASE * 2 + 1);
    expect(a[0]).toBe(1);
    expect(a[1]).toBe(2);
    expect(a[2]).toBe(3);
  });
  it("increment and decrement are inverses", () => {
    const a = randomDigits("incdec");
    const b = copy(a);
    addInt(b, 1);
    expect(equal(a, b)).toBe(false);
    addInt(b, -1);
    expect(equal(a, b)).toBe(true);
  });
  it("wraps modulo 25^1312000 in both directions", () => {
    const a = zero();
    addInt(a, -1); // should become BASE^DIGITS - 1: all digits 24
    expect(a[0]).toBe(BASE - 1);
    expect(a[DIGITS - 1]).toBe(BASE - 1);
    addInt(a, 1);
    expect(equal(a, zero())).toBe(true);
  });
  it("addScaled(b, m) then addScaled(b, -m) restores exactly", () => {
    const a = randomDigits("scaled-a");
    const b = randomDigits("scaled-b");
    const orig = copy(a);
    addScaled(a, b, 123456789);
    expect(equal(a, orig)).toBe(false);
    addScaled(a, b, -123456789);
    expect(equal(a, orig)).toBe(true);
  });
});

describe("feistel permutation", () => {
  it("decrypt inverts encrypt across random inputs and slots", () => {
    for (let trial = 0; trial < 8; trial++) {
      const h = randomDigits(`fst-${trial}`);
      const slot = Sfc32.fromString("slotpick", trial).int(SLOTS);
      const book = bookFromHex(h, slot);
      const back = hexFromBook(book, slot);
      expect(equal(back, h)).toBe(true);
    }
  });
  it("encrypt inverts decrypt (bijectivity both ways)", () => {
    const book = randomDigits("fst-rev");
    const h = hexFromBook(book, 17);
    expect(equal(bookFromHex(h, 17), book)).toBe(true);
  });
  it("output digits stay within the 25-symbol base", () => {
    const book = bookFromHex(randomDigits("range"), 3);
    let max = 0;
    for (const d of book) max = Math.max(max, d);
    expect(max).toBeLessThan(BASE);
  });
  it("adjacent hexagons hold radically different books", () => {
    const coord = originCoord();
    const next = stepCorridor(coord, 1);
    const a = bookFromHex(hexId(coord), 0);
    const b = bookFromHex(hexId(next), 0);
    let same = 0;
    for (let i = 0; i < a.length; i++) if (a[i] === b[i]) same++;
    // Unrelated uniform texts agree on ~1/25 of positions.
    expect(same / a.length).toBeGreaterThan(0.03);
    expect(same / a.length).toBeLessThan(0.05);
  });
  it("adjacent floors hold radically different books", () => {
    const a = bookFromHex(hexId(originCoord()), 9);
    const b = bookFromHex(hexId(stepFloor(originCoord(), 1)), 9);
    let same = 0;
    for (let i = 0; i < a.length; i++) if (a[i] === b[i]) same++;
    expect(same / a.length).toBeGreaterThan(0.03);
    expect(same / a.length).toBeLessThan(0.05);
  });
  it("different shelf positions in one hexagon hold different books", () => {
    const h = hexId(originCoord());
    const a = bookFromHex(h, 0);
    const b = bookFromHex(h, 1);
    expect(equal(a, b)).toBe(false);
  });
  it("symbol frequencies are uniform-ish across a generated book", () => {
    const book = bookFromHex(randomDigits("freq"), 100);
    const counts = new Array(BASE).fill(0);
    for (const d of book) counts[d]++;
    const expected = book.length / BASE;
    for (const c of counts) {
      expect(Math.abs(c - expected) / expected).toBeLessThan(0.02);
    }
  });
});

describe("addressing", () => {
  it("hexId is consistent with corridorForHex", () => {
    const h = randomDigits("addr");
    for (const f of [0, 1, -1, 12345, -99999]) {
      const c = corridorForHex(h, f);
      expect(equal(hexId({ c, f }), h)).toBe(true);
    }
  });
  it("stepCorridor changes the identity, stepping back restores it", () => {
    const a = originCoord();
    const b = stepCorridor(stepCorridor(a, 1), -1);
    expect(equal(hexId(a), hexId(b))).toBe(true);
  });
  it("hexagon names are stable and well-formed", () => {
    const n1 = hexName(hexId(originCoord()));
    const n2 = hexName(hexId(originCoord()));
    expect(n1).toBe(n2);
    expect(n1).toMatch(/^[0-9a-z]{4}(-[0-9a-z]{4}){3}$/);
  });
  it("slotIndex covers 0..639 uniquely", () => {
    const seen = new Set<number>();
    for (let w = 0; w < WALLS; w++)
      for (let s = 0; s < SHELVES; s++)
        for (let v = 0; v < VOLUMES; v++) seen.add(slotIndex(w, s, v));
    expect(seen.size).toBe(SLOTS);
  });
});

describe("the seek — finding any text in the Library", () => {
  it("context mode: travelling to the result really finds the text", () => {
    const phrase = "oh time thy pyramids";
    const r = seek(phrase, "context");
    const book = getBook(r.location);
    const found = digitsToText(book.digits, r.offset, r.offset + r.length);
    expect(found).toBe(phrase);
    expect(r.page).toBe(Math.floor(r.offset / PAGE_CHARS));
    // ...surrounded by the gibberish of the universe, not by blanks.
    const before = digitsToText(book.digits, Math.max(0, r.offset - 64), r.offset);
    expect(before.trim().length).toBeGreaterThan(0);
  });
  it("alone mode: the text opens the book and all else is silence", () => {
    const phrase = "the certitude that everything has been written";
    const r = seek(phrase, "alone");
    expect(r.offset).toBe(0);
    const book = getBook(r.location);
    expect(digitsToText(book.digits, 0, r.length)).toBe(r.transliteration.text);
    expect(r.transliteration.text).toBe("the certitude that everything has been vritten");
    const after = digitsToText(book.digits, r.length, r.length + 500);
    expect(after).toBe(" ".repeat(500));
  });
  it("is deterministic: the Library does not rearrange itself", () => {
    const a = seek("dhcmrlchtdj", "context");
    const b = seek("dhcmrlchtdj", "context");
    expect(equal(a.location.coord.c, b.location.coord.c)).toBe(true);
    expect(a.location.coord.f).toBe(b.location.coord.f);
    expect(a.offset).toBe(b.offset);
    expect(a.location.wall).toBe(b.location.wall);
  });
  it("other copies exist elsewhere with the same text", () => {
    const a = seek("mirror", "context", 0);
    const b = seek("mirror", "context", 1);
    expect(equal(hexId(a.location.coord), hexId(b.location.coord))).toBe(false);
    const bookB = getBook(b.location);
    expect(digitsToText(bookB.digits, b.offset, b.offset + b.length)).toBe("mirror");
  });
  it("transliterates the seeker's text and still finds it", () => {
    const r = seek("The Walker's Quest!", "context");
    expect(r.transliteration.text).toBe("the valcers cuest.");
    const book = getBook(r.location);
    expect(digitsToText(book.digits, r.offset, r.offset + r.length)).toBe("the valcers cuest.");
  });
  it("long texts spanning many pages are found whole", () => {
    const phrase = ("in some shelf of some hexagon, it was argued, there must exist a book " +
      "that is the cipher and perfect compendium of all the rest. ").repeat(40); // ~4,900 chars
    const clean = transliterate(phrase).text;
    const r = seek(phrase, "context");
    const book = getBook(r.location);
    expect(digitsToText(book.digits, r.offset, r.offset + r.length)).toBe(clean);
    expect(r.length).toBeGreaterThan(PAGE_CHARS); // really crosses a page boundary
  });
  it("rejects texts with nothing expressible", () => {
    expect(() => seek("42+17=59")).toThrow();
  });
});

describe("books as objects", () => {
  it("pages are 3200 characters and there are 410 of them", () => {
    const book = getBook({ coord: originCoord(), wall: 0, shelf: 0, volume: 0 });
    expect(pageText(book, 0).length).toBe(PAGE_CHARS);
    expect(pageText(book, PAGES - 1).length).toBe(PAGE_CHARS);
    expect(() => pageText(book, PAGES)).toThrow();
  });
  it("spines bear letters that do not prefigure the contents", () => {
    const book = getBook({ coord: originCoord(), wall: 1, shelf: 2, volume: 3 });
    expect(book.spine).toMatch(/^[a-z][a-z ]*[a-z]$/);
    expect(book.spine.length).toBeGreaterThanOrEqual(3);
    expect(book.spine.length).toBeLessThanOrEqual(14);
  });
  it("the same location always yields the same book (golden values)", () => {
    const book = getBook({ coord: originCoord(), wall: 0, shelf: 0, volume: 0 });
    // Pinned forever. If this test fails, the entire universe has been
    // replaced with a different one, which the inhabitants would not enjoy.
    expect(digitsToText(book.digits, 0, 40)).toBe("vhd g.djgbys gpurud xylphxf,s.nlvovntba.");
    expect(book.spine).toBe("ljntdxg");
    expect(book.hexName).toBe("crqs-fqnk-gkp7-zg05");
    for (const ch of digitsToText(book.digits, 0, 200)) expect(SYMBOLS).toContain(ch);
  });
  it("generation is fast enough to feel instant", () => {
    const t0 = performance.now();
    getBook({ coord: { c: corridorForHex(randomDigits("perf"), 7), f: 7 }, wall: 2, shelf: 1, volume: 30 });
    const ms = performance.now() - t0;
    expect(ms).toBeLessThan(400);
  });
});

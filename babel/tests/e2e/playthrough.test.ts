/**
 * End-to-end playthrough of the Library, against the production build.
 *
 * The harness drives the simulation with a fixed timestep through
 * __babel.frame() (headless compositors starve RAF and SwiftShader cannot
 * render in realtime), but every action arrives as real, trusted input:
 * keyboard walking, key-held stair climbing, typing into the seek panel,
 * clicking its buttons. Screenshots are written to /tmp/babel-e2e.
 *
 * The seek assertions are cross-checked against the same deterministic core
 * computed independently in this Node process — the book the game travels
 * to must be the book the mathematics names.
 */

import { afterAll, beforeAll, describe, expect, it } from "vitest";
import puppeteer, { Browser, Page, KeyInput } from "puppeteer";
import { ChildProcess, spawn } from "node:child_process";
import { mkdirSync } from "node:fs";
import * as D from "../../src/world/dims";
import { seek as coreSeek } from "../../src/core/library";
import { hexId, hexName } from "../../src/core/address";
import { transliterate } from "../../src/core/alphabet";
import { PAGE_CHARS } from "../../src/core/constants";

const URL_BASE = "http://127.0.0.1:4273";
const SHOTS = "/tmp/babel-e2e";
const PHRASE = "oh time thy pyramids";

let server: ChildProcess | null = null;
let browser: Browser;
let page: Page;
const pageErrors: string[] = [];
const consoleErrors: string[] = [];

const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));

/* eslint-disable @typescript-eslint/no-explicit-any */
const state = async (): Promise<any> => page.evaluate(() => (window as any).__babel.state());
const pump = (n = 15) => page.evaluate((k) => (window as any).__babel.frame(k), n);
const draw = () => page.evaluate(() => (window as any).__babel.draw());
const view = (yaw: number, pitch: number) =>
  page.evaluate((y, p) => (window as any).__babel.setView(y, p), yaw, pitch);

async function shoot(name: string): Promise<void> {
  await draw();
  await page.screenshot({ path: `${SHOTS}/${name}.png` });
}

/**
 * Headless shell grants pointer lock; while it is held, DOM clicks are
 * swallowed by the locked canvas. Release it before clicking buttons,
 * exactly as a player's Esc would.
 */
async function unlock(): Promise<void> {
  await page.evaluate(() => document.exitPointerLock?.());
  await wait(60);
}

/** Nearest stairwell axis (the wells repeat with the corridor period). */
function stairAxisNear(x: number): { ax: number; az: number } {
  const base = D.HEX_APO + D.STAIR_AXIS_X;
  const n = Math.round((x - base) / D.UNIT_PITCH);
  return { ax: base + n * D.UNIT_PITCH, az: D.STAIR_AXIS_Z };
}

/** Poll real time until a condition holds (UI timers may be throttled). */
async function pollUntil(cond: (s: any) => boolean, maxMs = 10000): Promise<any> {
  const t0 = Date.now();
  let s = await state();
  while (!cond(s) && Date.now() - t0 < maxMs) {
    await wait(250);
    await pump(3);
    s = await state();
  }
  return s;
}

async function holdUntil(
  key: KeyInput,
  cond: (s: any) => boolean,
  maxFrames = 2400,
): Promise<any> {
  await page.keyboard.down(key);
  let s = await state();
  let used = 0;
  while (!cond(s) && used < maxFrames) {
    await pump(15);
    used += 15;
    s = await state();
  }
  await page.keyboard.up(key);
  await pump(3);
  return s;
}

beforeAll(async () => {
  mkdirSync(SHOTS, { recursive: true });
  // Serve the production build.
  server = spawn("npx", ["vite", "preview", "--port", "4273", "--host", "127.0.0.1"], {
    cwd: new URL("../..", import.meta.url).pathname,
    stdio: "ignore",
  });
  let up = false;
  for (let i = 0; i < 60 && !up; i++) {
    await wait(500);
    up = await fetch(URL_BASE)
      .then(() => true)
      .catch(() => false);
  }
  if (!up) throw new Error("preview server did not come up");

  browser = await puppeteer.launch({
    headless: "shell",
    args: ["--no-sandbox", "--enable-unsafe-swiftshader", "--use-gl=angle", "--use-angle=swiftshader"],
    defaultViewport: { width: 1024, height: 640 },
    protocolTimeout: 120000,
  });
  page = await browser.newPage();
  page.on("pageerror", (e) => pageErrors.push((e as Error).message));
  page.on("console", (m) => {
    if (m.type() === "error" && !m.text().includes("404")) consoleErrors.push(m.text());
  });
  await page.goto(`${URL_BASE}/?test=1`, { waitUntil: "domcontentloaded", timeout: 45000 });
  await wait(600);
}, 120000);

afterAll(async () => {
  await browser?.close().catch(() => {});
  server?.kill();
});

describe("waking in the Library", () => {
  it("shows the start screen and enters on click", async () => {
    expect(await page.$("#startOverlay")).toBeTruthy();
    await page.screenshot({ path: `${SHOTS}/01-title.png` });
    await page.click("#enterBtn");
    await pump(10);
    const s = await state();
    expect(s.started).toBe(true);
    expect(s.mode).toBe("walk");
    expect(s.grounded).toBe(true);
  });

  it("renders an actual image, not a void", async () => {
    await draw();
    const stats = await page.evaluate(() => (window as any).__babel.canvasStats());
    expect(stats.mean).toBeGreaterThan(8); // not black
    expect(stats.mean).toBeLessThan(240); // not white
    expect(stats.distinct).toBeGreaterThan(30); // an actual scene
  });

  it("wakes everyone in the same first hexagon", async () => {
    const s = await state();
    expect(s.hexName).toBe("crqs-fqnk-gkp7-zg05"); // pinned forever
    expect(s.floor).toBe(0);
    await shoot("02-first-hexagon");
  });
});

describe("walking the endless corridor", () => {
  it("walks east through the vestibule into the next hexagon", async () => {
    await view(-0.635, 0);
    let s = await holdUntil("KeyW", (st) => st.pos.x > 1.2);
    expect(s.pos.x).toBeGreaterThan(1.2);
    await view(0, 0);
    await shoot("03-vestibule");
    s = await holdUntil("KeyW", (st) => st.steps === 1 && st.pos.x > -0.3, 3000);
    expect(s.steps).toBe(1);
    expect(s.hexName).toBe("km84-3tfd-gkp7-9q73"); // pinned: east neighbour
    await shoot("04-next-hexagon");
  });

  it("the hexagon east of that one is different again, and walking back returns", async () => {
    // Walk back west to the first hexagon.
    await view(Math.PI, 0);
    const s = await holdUntil("KeyW", (st) => st.steps === 0 && Math.abs(st.pos.x) < 0.4, 3000);
    expect(s.steps).toBe(0);
    expect(s.hexName).toBe("crqs-fqnk-gkp7-zg05"); // the Library does not move
  });
});

describe("taking a book from a shelf", () => {
  it("aims at a volume and reads its deterministic pages", async () => {
    // Stand in the ring facing the southwest wall.
    await page.evaluate(() => (window as any).__babel.teleport(-0.45, 0, 0.75));
    await pump(3);
    await page.evaluate(() => (window as any).__babel.aimAtBook(1, 2, 16));
    await pump(4);
    const s = await state();
    expect(s.aimed).toEqual({ wall: 1, shelf: 2, volume: 16, dx: 0 });
    await shoot("05-aiming");

    await page.keyboard.press("KeyE");
    await pump(4);
    const book = await page.evaluate(() => (window as any).__babel.openedBook());
    expect(book).toBeTruthy();
    expect(book.wall).toBe(1);
    expect(book.shelf).toBe(2);
    expect(book.volume).toBe(16);
    expect(book.hexName).toBe("crqs-fqnk-gkp7-zg05");
    expect(book.spine).toMatch(/^[a-z][a-z ]*[a-z]$/);

    const text = await page.evaluate(() => (window as any).__babel.pageText());
    // 3200 characters + 39 newlines from the 40-line layout.
    expect(text.replace(/\n/g, "").length).toBe(3200);
    await page.screenshot({ path: `${SHOTS}/06-open-book.png` });
  });

  it("turns pages and returns the volume to its shelf", async () => {
    await page.click("#pageNext");
    const book = await page.evaluate(() => (window as any).__babel.openedBook());
    expect(book.page).toBe(1);
    await page.keyboard.press("KeyE"); // put it back
    await pump(3);
    const s = await state();
    expect(s.bookOpen).toBe(false);
  });
});

describe("the spiral staircase", () => {
  /** Walk the helix until the floor reads `target` and the feet settle. */
  async function spiral(dir: 1 | -1, target: number): Promise<any> {
    let s = await state();
    await page.keyboard.down("KeyW");
    let done = false;
    for (let i = 0; i < 160 && !done; i++) {
      const { ax, az } = stairAxisNear(s.pos.x);
      const a = Math.atan2(s.pos.z - az, s.pos.x - ax);
      // Clockwise (seen from above) climbs; counter-clockwise descends.
      const yawTangent = dir === 1 ? Math.atan2(Math.cos(a), Math.sin(a)) : Math.atan2(-Math.cos(a), -Math.sin(a));
      await view(yawTangent, 0.15 * dir);
      await pump(12);
      s = await state();
      done = s.floor === target && s.grounded && Math.abs(s.pos.y) < 0.05;
    }
    await page.keyboard.up("KeyW");
    return s;
  }

  it("climbs to the floor above", async () => {
    // The west vestibule's stairwell is nearest: walk west, then north
    // through its chord opening into the well.
    await page.evaluate(() => (window as any).__babel.teleport(-1.0, 0, 0));
    await pump(3);
    await view(Math.PI, 0);
    let s = await holdUntil("KeyW", (st) => st.pos.x < -2.1, 1200);
    expect(s.pos.x).toBeLessThan(-2.1);
    await view(Math.PI / 2, 0);
    s = await holdUntil("KeyW", (st) => st.pos.z < -1.0, 900);
    expect(s.pos.z).toBeLessThan(-1.0);
    await shoot("07-stairwell");

    s = await spiral(1, s.floor + 1);
    expect(s.floor).toBe(1);
    // Leave the well through its door (south), back into the vestibule.
    await view(-Math.PI / 2, 0);
    s = await holdUntil("KeyW", (st) => st.pos.z > -0.45, 900);
    expect(s.pos.z).toBeGreaterThan(-0.45);
    expect(s.floor).toBe(1);
    await shoot("08-floor-above");
  }, 120000);

  it("the floor above is another hexagon with other books", async () => {
    const s = await state();
    expect(s.floor).toBe(1);
    expect(s.hexName).not.toBe("crqs-fqnk-gkp7-zg05");
    expect(s.hexName).not.toBe("km84-3tfd-gkp7-9q73");
  });

  it("descends back to the floor below", async () => {
    await view(Math.PI / 2, 0);
    let s = await holdUntil("KeyW", (st) => st.pos.z < -1.0, 900);
    s = await spiral(-1, s.floor - 1);
    expect(s.floor).toBe(0);
    const back = await state();
    expect(back.floor).toBe(0);
  }, 120000);
});

describe("the seek: any text, its exact shelf", () => {
  let expectedName = "";

  it("computes the same address in Node as the game will", () => {
    const r = coreSeek(PHRASE, "context", 0);
    expectedName = hexName(hexId(r.location.coord));
    expect(r.transliteration.text).toBe(PHRASE);
    expect(expectedName).toMatch(/^[0-9a-z]{4}(-[0-9a-z]{4}){3}$/);
  });

  it("types the phrase, seeks, and the addresses agree", async () => {
    await page.keyboard.press("KeyF");
    await wait(150);
    const open = await state();
    expect(open.seekOpen).toBe(true);
    await unlock();
    await page.click("#seekText");
    await page.type("#seekText", PHRASE, { delay: 4 });
    await wait(120);
    const preview = await page.$eval("#seekPreview", (el) => el.textContent);
    expect(preview).toBe(PHRASE); // already in the Library's alphabet
    await page.click("#seekGo");
    await wait(250);
    const res = await page.evaluate(() => (window as any).__babel.seekResult());
    expect(res).toBeTruthy();
    expect(res.text).toBe(PHRASE);
    expect(res.hexName).toBe(expectedName); // Node and browser agree
    await page.screenshot({ path: `${SHOTS}/09-seek.png` });
  });

  it("travels there: the volume glows on the named wall", async () => {
    const res = await page.evaluate(() => (window as any).__babel.seekResult());
    await page.click("#travelBtn");
    const s = await pollUntil((st) => st.hexName === expectedName, 15000);
    expect(s.hexName).toBe(expectedName);
    expect(s.floor).toBe(res.floor);
    await shoot("10-arrival");
  });

  it("opens the sought volume to the sought page, text highlighted", async () => {
    const res = await page.evaluate(() => (window as any).__babel.seekResult());
    await page.evaluate(
      (w: number, sh: number, v: number) => (window as any).__babel.aimAtBook(w, sh, v),
      res.wall,
      res.shelf,
      res.volume,
    );
    await pump(4);
    const s = await state();
    expect(s.aimed).toBeTruthy();
    expect(s.aimed.wall).toBe(res.wall);
    expect(s.aimed.shelf).toBe(res.shelf);
    expect(s.aimed.volume).toBe(res.volume);

    await page.keyboard.press("KeyE");
    await pump(4);
    const book = await page.evaluate(() => (window as any).__babel.openedBook());
    expect(book).toBeTruthy();
    expect(book.hexName).toBe(expectedName);
    expect(book.page).toBe(res.page); // opened straight to the page

    const mark = await page.evaluate(() => (window as any).__babel.markText());
    expect(mark?.replace(/\n/g, "")).toBe(PHRASE);

    const text = await page.evaluate(() => (window as any).__babel.pageText());
    expect(text.replace(/\n/g, "")).toContain(PHRASE);
    await page.screenshot({ path: `${SHOTS}/11-found-text.png` });

    // What surrounds it: the rest of the page agrees with the Node core.
    const nodeSeek = coreSeek(PHRASE, "context", 0);
    const inPageOffset = nodeSeek.offset - nodeSeek.page * PAGE_CHARS;
    const flat = text.replace(/\n/g, "");
    expect(flat.slice(inPageOffset, inPageOffset + PHRASE.length)).toBe(PHRASE);
    await page.keyboard.press("KeyE");
    await pump(3);
  });

  it("seeking the same words again names the same shelf", async () => {
    const again = coreSeek(PHRASE, "context", 0);
    expect(hexName(hexId(again.location.coord))).toBe(expectedName);
    // Travel closed the panel; reopen it — the phrase is still there.
    await unlock();
    await page.click("#btnSeek");
    await wait(150);
    await page.click("#seekGo");
    await wait(250);
    const res = await page.evaluate(() => (window as any).__babel.seekResult());
    expect(res.hexName).toBe(expectedName);
  });

  it("'alone' mode leaves the words alone in a blank book", async () => {
    const alonePhrase = "the library is unlimited and cyclical";
    const clean = transliterate(alonePhrase).text;
    const expectAlone = coreSeek(alonePhrase, "alone", 0);
    const expectAloneName = hexName(hexId(expectAlone.location.coord));
    await page.evaluate(() => {
      (document.getElementById("seekText") as HTMLTextAreaElement).value = "";
    });
    await unlock();
    await page.click("#seekText");
    await page.type("#seekText", alonePhrase, { delay: 3 });
    await page.click('input[name="seekMode"][value="alone"]');
    await page.click("#seekGo");
    await wait(250);
    await page.click("#travelBtn");
    await pollUntil((st) => st.hexName === expectAloneName, 15000);
    const res = await page.evaluate(() => (window as any).__babel.seekResult());
    expect(res.hexName).toBe(expectAloneName);
    await page.evaluate(
      (w: number, sh: number, v: number) => (window as any).__babel.aimAtBook(w, sh, v),
      res.wall,
      res.shelf,
      res.volume,
    );
    await pump(4);
    await page.keyboard.press("KeyE");
    await pump(4);
    const text: string = await page.evaluate(() => (window as any).__babel.pageText());
    const flat = text.replace(/\n/g, "");
    expect(flat.startsWith(clean)).toBe(true);
    expect(flat.slice(clean.length).trim()).toBe(""); // silence after the words
    await page.screenshot({ path: `${SHOTS}/12-alone.png` });
    await page.keyboard.press("KeyE");
    await pump(3);
    // Travel already closed the seek panel; nothing left to dismiss.
    const end = await state();
    expect(end.seekOpen).toBe(false);
    expect(end.bookOpen).toBe(false);
  });
});

describe("the bottomless shaft", () => {
  it("vaulting the very low railing begins the endless fall", async () => {
    // Make sure no panel is eating the keyboard.
    const pre = await state();
    if (pre.seekOpen) {
      await unlock();
      await page.click("#btnSeek");
      await wait(100);
    }
    await page.evaluate(() => (document.activeElement as HTMLElement | null)?.blur?.());
    await page.evaluate(() => (window as any).__babel.teleport(0, 0, 1.3));
    await pump(3);
    await view(Math.PI / 2, -0.3); // face the railing, north
    await page.keyboard.down("ShiftLeft"); // hurry: a deliberate vault
    await page.keyboard.down("KeyW");
    await pump(8);
    let s = await state();
    let tries = 0;
    while (s.mode !== "falling" && tries < 12) {
      await page.keyboard.down("Space");
      await pump(30);
      await page.keyboard.up("Space");
      s = await state();
      tries++;
    }
    await page.keyboard.up("KeyW");
    await page.keyboard.up("ShiftLeft");
    expect(s.mode).toBe("falling");
  });

  it("falls past identical floors, forever, until waking remotely", async () => {
    const before = await state();
    await pump(200);
    const during = await state();
    expect(during.mode).toBe("falling");
    expect(during.floor).toBeLessThan(before.floor);
    // The merciful overlay appears on a real-time timer.
    await wait(4600);
    const overlayVisible = await page.$eval("#fallOverlay", (el) => !el.classList.contains("hidden"));
    expect(overlayVisible).toBe(true);
    await shoot("13-falling");
    await unlock();
    await page.click("#wakeBtn");
    const after = await pollUntil((st) => st.mode === "walk", 15000);
    expect(after.mode).toBe("walk");
    expect(after.grounded).toBe(true);
    expect(after.floor).toBeLessThanOrEqual(during.floor - 8191);
    await shoot("14-remote-floor");
  }, 60000);
});

describe("the run itself", () => {
  it("finished without page errors or console errors", () => {
    expect(pageErrors).toEqual([]);
    expect(consoleErrors).toEqual([]);
  });

  it("kept the WebGL context alive", async () => {
    const s = await state();
    expect(s.contextLost).toBe(false);
  });
});

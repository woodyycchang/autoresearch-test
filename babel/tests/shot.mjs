// Visual smoke harness: boots the built game headlessly and plays a scripted
// tour. The harness pumps simulation frames explicitly (fixed timestep, no
// rendering) and renders single frames only for screenshots — SwiftShader
// cannot keep up with realtime rendering, but the simulation is exact.
// Input still arrives as real trusted keyboard events.
import puppeteer from "puppeteer";
import { spawn } from "node:child_process";
import { mkdirSync } from "node:fs";

const OUT = "/tmp/babel-shots";
mkdirSync(OUT, { recursive: true });

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function startServer() {
  try {
    await fetch("http://127.0.0.1:4173/");
    return null;
  } catch {
    /* not running */
  }
  const proc = spawn("npx", ["vite", "preview", "--port", "4173", "--host", "127.0.0.1"], {
    cwd: new URL("..", import.meta.url).pathname,
    stdio: "ignore",
  });
  for (let i = 0; i < 60; i++) {
    await wait(500);
    try {
      await fetch("http://127.0.0.1:4173/");
      return proc;
    } catch {
      /* retry */
    }
  }
  throw new Error("preview server did not come up");
}

const server = await startServer();
const browser = await puppeteer.launch({
  headless: "shell",
  args: ["--no-sandbox", "--enable-unsafe-swiftshader", "--use-gl=angle", "--use-angle=swiftshader"],
  defaultViewport: { width: 1024, height: 640 },
  protocolTimeout: 120000,
});
const page = await browser.newPage();
page.on("console", (m) => {
  if (m.type() === "error" && !m.text().includes("404")) console.log("[console.error]", m.text());
});
page.on("pageerror", (e) => console.log("[pageerror]", e.message));

const state = () => page.evaluate(() => window.__babel.state());
const pump = (n = 15) => page.evaluate((k) => window.__babel.frame(k), n);
const view = (yaw, pitch) => page.evaluate((y, p) => window.__babel.setView(y, p), yaw, pitch);
async function shoot(name) {
  await page.evaluate(() => window.__babel.draw());
  await page.screenshot({ path: `${OUT}/${name}.png` });
  console.log("shot:", name);
}

async function holdUntil(key, cond, maxFrames = 1800) {
  await page.keyboard.down(key);
  let s = await state();
  let f = 0;
  while (!cond(s) && f < maxFrames) {
    await pump(15);
    f += 15;
    s = await state();
  }
  await page.keyboard.up(key);
  await pump(3);
  return s;
}

await page.goto("http://127.0.0.1:4173/?test=1", { waitUntil: "domcontentloaded", timeout: 45000 });
await wait(700);
await page.screenshot({ path: `${OUT}/01-start.png` });
console.log("shot: 01-start");

await page.click("#enterBtn");
await pump(10);
await shoot("02-hexagon");
console.log("canvas:", JSON.stringify(await page.evaluate(() => window.__babel.canvasStats())));
console.log("spawn:", JSON.stringify((await state()).pos));

// Look down at the shaft and railing.
await view(-Math.PI / 2, -0.55);
await pump(3);
await shoot("03-shaft-down");

// Walk to the east vestibule.
await view(-0.635, 0);
let s = await holdUntil("KeyW", (st) => st.pos.x > 1.2);
console.log("at door:", JSON.stringify(s.pos));
await view(0, 0);
await pump(3);
await shoot("04-door");

s = await holdUntil("KeyW", (st) => st.steps === 1 && st.pos.x > -0.3, 2400);
console.log("next hex: steps", s.steps, "pos", JSON.stringify(s.pos), "hex", s.hexName, "ctxLost", s.contextLost);
await shoot("05-next-hex");

// Aim at a specific volume and open it (southwest wall: nearest from here).
await page.evaluate(() => window.__babel.aimAtBook(1, 2, 16));
await pump(6);
console.log("aimed:", JSON.stringify((await state()).aimed));
await shoot("06-aimed");
await page.keyboard.press("KeyE");
await pump(6);
console.log("book:", JSON.stringify(await page.evaluate(() => window.__babel.openedBook())));
await shoot("07-book");
await page.keyboard.press("KeyE");
await pump(6);

// Look back west toward the vestibule mirror.
await view(Math.PI - 0.5, 0);
await pump(3);
await shoot("08-look-back");

const fin = await state();
console.log("final ctxLost:", fin.contextLost, "tri:", fin.render.triangles);
await browser.close();
server?.kill();
console.log("done ->", OUT);

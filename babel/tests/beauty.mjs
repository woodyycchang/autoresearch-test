// Beauty pass: high-quality stills for the README and the user.
// Exercises QUALITY_HIGH (live mirrors, rx4/ry3) headlessly — slow per
// frame under SwiftShader, but each still is a single draw.
import puppeteer from "puppeteer";
import { mkdirSync } from "node:fs";

const OUT = "/tmp/babel-beauty";
mkdirSync(OUT, { recursive: true });
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

const browser = await puppeteer.launch({
  headless: "shell",
  args: ["--no-sandbox", "--enable-unsafe-swiftshader", "--use-gl=angle", "--use-angle=swiftshader"],
  defaultViewport: { width: 1440, height: 900 },
  protocolTimeout: 300000,
});
const page = await browser.newPage();
page.on("pageerror", (e) => console.log("[pageerror]", e.message));
await page.goto("http://127.0.0.1:4273/?test=1&quality=high", { waitUntil: "domcontentloaded", timeout: 60000 });
await wait(800);
await page.screenshot({ path: `${OUT}/title.png` });
console.log("shot: title");

const pump = (n = 10) => page.evaluate((k) => window.__babel.frame(k), n);
const draw = () => page.evaluate(() => window.__babel.draw());
const view = (yaw, pitch) => page.evaluate((y, p) => window.__babel.setView(y, p), yaw, pitch);
const tp = (x, y, z) => page.evaluate((a, b, c) => window.__babel.teleport(a, b, c), x, y, z);
async function shoot(name) {
  await draw();
  await page.screenshot({ path: `${OUT}/${name}.png` });
  console.log("shot:", name);
}

await page.click("#enterBtn");
await pump(12);

// 1. The gallery: bookcases meeting at a corner, lamp above.
await tp(-0.2, 0, -1.05);
await view(-Math.PI / 2 + 0.25, 0.06);
await pump(4);
await shoot("gallery");

// 2. Looking down the shaft past the railing.
await tp(0, 0, -1.0);
await view(-Math.PI / 2, -0.62);
await pump(3);
await shoot("shaft-down");

// 3. Looking up through the ceiling to the storeys above.
await view(-Math.PI / 2, 0.85);
await pump(3);
await shoot("shaft-up");

// 4. The corridor sightline: door after door after door.
await tp(1.1, 0, 0);
await view(0, 0.02);
await pump(3);
await shoot("corridor");

// 5. The mirror in the vestibule ("faithfully duplicates appearances").
await tp(2.2, 0, -0.28);
await view(-Math.PI / 2 + 0.35, 0.05);
await pump(3);
await shoot("mirror");

// 6. The spiral stairwell mouth.
await tp(3.2, 0, -0.2);
await view(Math.PI / 2 + 0.3, 0.1);
await pump(3);
await shoot("stairwell");

// 7. An open book.
await tp(-0.45, 0, 0.75);
await pump(2);
await page.evaluate(() => window.__babel.aimAtBook(1, 2, 16));
await pump(4);
await page.keyboard.press("KeyE");
await pump(4);
await page.screenshot({ path: `${OUT}/book.png` });
console.log("shot: book");
await page.keyboard.press("KeyE");
await pump(3);

// 8. Seek result + travel + the found, highlighted text.
await page.keyboard.press("KeyF");
await wait(200);
await page.click("#seekText");
await page.type("#seekText", "oh time thy pyramids", { delay: 3 });
await page.click("#seekGo");
await wait(300);
await draw();
await page.screenshot({ path: `${OUT}/seek.png` });
console.log("shot: seek");
await page.click("#travelBtn");
await wait(1600);
await pump(6);
await shoot("arrival");
const res = await page.evaluate(() => window.__babel.seekResult());
await page.evaluate((w, s, v) => window.__babel.aimAtBook(w, s, v), res.wall, res.shelf, res.volume);
await pump(4);
await page.keyboard.press("KeyE");
await pump(4);
await page.screenshot({ path: `${OUT}/found.png` });
console.log("shot: found");

await browser.close();
console.log("done ->", OUT);

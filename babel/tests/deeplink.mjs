import puppeteer from "puppeteer";
const browser = await puppeteer.launch({
  headless: "shell",
  args: ["--no-sandbox", "--enable-unsafe-swiftshader", "--use-gl=angle", "--use-angle=swiftshader"],
  defaultViewport: { width: 800, height: 500 },
  protocolTimeout: 120000,
});
const page = await browser.newPage();
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
await page.goto("http://127.0.0.1:4273/?test=1&seek=oh%20time%20thy%20pyramids&mode=context", { waitUntil: "domcontentloaded" });
await wait(500);
await page.click("#enterBtn");
for (let i = 0; i < 30; i++) {
  await wait(400);
  await page.evaluate((k) => window.__babel.frame(k), 5);
  const s = await page.evaluate(() => window.__babel.state());
  if (s.hexName !== "crqs-fqnk-gkp7-zg05") {
    console.log("arrived:", s.hexName, "floor", s.floor);
    break;
  }
}
const res = await page.evaluate(() => window.__babel.seekResult());
console.log("seek result:", res.hexName, "wall", res.wall, "shelf", res.shelf, "vol", res.volume, "page", res.page);
const st = await page.evaluate(() => window.__babel.state());
console.log("match:", st.hexName === res.hexName);
await browser.close();

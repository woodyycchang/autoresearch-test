/**
 * The Library of Babel — composition root.
 * Wires the deterministic core (every book that can exist, addressable) to
 * the walkable world, the librarian's body, and the flat interfaces.
 */

import * as THREE from "three";
import "./ui/styles.css";
import { hexId, hexName, originCoord, BookLocation } from "./core/address";
import { copy, equal } from "./core/bignum";
import { PAGE_CHARS } from "./core/constants";
import { getBook, seek, SeekError, SeekMode, SeekResult, spineAt } from "./core/library";
import { Controller } from "./player/controller";
import * as D from "./world/dims";
import { QUALITY_HIGH, QUALITY_LOW, World } from "./world/world";
import { UI, describeWall } from "./ui/ui";
import { Ambience } from "./audio/ambience";

const params = new URLSearchParams(location.search);
const TEST_MODE = params.get("test") === "1";

const app = document.getElementById("app")!;
const ui = new UI(app, {
  onSeek: doSeek,
  onTravel: travelToSeek,
  onCloseBook: closeBook,
  onResume: resumePointer,
  onWake: wakeFromFall,
  onShare: shareLink,
});

// ---------------------------------------------------------------- three.js

const renderer = new THREE.WebGLRenderer({
  antialias: !TEST_MODE,
  powerPreference: "high-performance",
  preserveDrawingBuffer: TEST_MODE,
});
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
document.getElementById("scene")!.appendChild(renderer.domElement);
let contextLost = false;
renderer.domElement.addEventListener("webglcontextlost", () => {
  contextLost = true;
});

let world: World | null = null;
let controller: Controller | null = null;
const ambience = new Ambience();

// Session origin: where this visitor first woke (the same for everyone —
// any hexagon may be the center of the Library).
let sessionSteps = 0; // corridor steps east since waking
let farFromHome = false;
let muted = false;

// Seek state.
let pendingSeek: SeekResult | null = null;
let arrivedSeek: SeekResult | null = null;
let highlightTarget: { dx: number; dy: number; wall: number; shelf: number; volume: number } | null = null;

// Book-in-hand state.
let hiddenInstance = -1;

// ------------------------------------------------------------------ boot

function start(lowQuality: boolean): void {
  const forced = params.get("quality");
  const quality =
    forced === "high" ? QUALITY_HIGH : forced === "low" || lowQuality || TEST_MODE ? QUALITY_LOW : QUALITY_HIGH;
  world = new World(originCoord(), quality);
  controller = new Controller(world, {
    onShiftX: (dir) => {
      world!.shiftX(dir);
      sessionSteps += dir;
      refreshHud();
      refreshHighlight();
    },
    onShiftY: (dir) => {
      world!.shiftY(dir, { skipRetile: controller!.mode === "falling" });
      refreshHud();
      refreshHighlight();
    },
    onStartFalling: () => {
      ambience.wind(true);
      window.setTimeout(() => {
        if (controller!.mode === "falling") {
          document.exitPointerLock?.();
          ui.showFall(true);
        }
      }, 4200);
    },
    onStep: () => ambience.footstep(),
  }, window.innerWidth / window.innerHeight);

  renderer.setPixelRatio(Math.min(window.devicePixelRatio, quality.dpr));
  renderer.setSize(window.innerWidth, window.innerHeight);

  // Wake on the north side of the ring, facing south across the shaft.
  controller.pos.set(0, 0, -1.15);
  controller.yaw = -Math.PI / 2;
  controller.enabled = true;
  ambience.start();
  ui.setMuteLabel(false);
  refreshHud();
  requestPointerLock();

  if (params.get("seek")) {
    // Deep link: run the seek and travel on arrival.
    const text = params.get("seek")!;
    const mode = (params.get("mode") === "alone" ? "alone" : "context") as SeekMode;
    const copyIdx = parseInt(params.get("copy") ?? "0", 10) || 0;
    ui.toggleSeek(true);
    ui.setSeekText(text, mode);
    const res = doSeek(text, mode, copyIdx);
    if (typeof res !== "string") {
      ui.showSeekResult(res);
      ui.setSeekAddr(hexName(hexId(res.location.coord)));
      window.setTimeout(() => travelToSeek(), 600);
    }
  }
}

ui.bindStart(start);
ui.bindButtons({
  seek: () => toggleSeekPanel(),
  help: () => {
    ui.showHelp(!ui.helpIsOpen());
    if (controller) controller.enabled = !ui.helpIsOpen();
  },
  mute: () => {
    muted = ambience.toggleMute();
    ui.setMuteLabel(muted);
  },
});

// -------------------------------------------------------------- the loop

const clock = new THREE.Clock();
let frames = 0;
let fpsTime = 0;
let fps = 0;
const perf = { update: 0, aim: 0, render: 0, gap: 0, raf: 0 };
let lastRaf = 0;

function animate(dtFixed?: number, skipRender = false): void {
  if (!TEST_MODE) requestAnimationFrame(() => animate());
  const now = performance.now();
  perf.gap = now - lastRaf;
  lastRaf = now;
  perf.raf++;
  const dt = dtFixed ?? Math.min(clock.getDelta(), 0.05);
  if (!world || !controller) return;
  const uiOpen = ui.bookIsOpen() || ui.helpIsOpen() || !ui.startHidden();
  controller.enabled = !uiOpen && controller.mode !== "falling" && !seekFocused();
  let t = performance.now();
  controller.update(dt);
  perf.update = performance.now() - t;
  world.pulse(now / 1000);
  t = performance.now();
  updateAim();
  perf.aim = performance.now() - t;
  if (!skipRender) {
    t = performance.now();
    renderer.render(world.scene, controller.camera);
    perf.render = performance.now() - t;
  } else {
    // Rendering normally refreshes world matrices; without it the aim
    // raycast would see stale transforms.
    world.scene.updateMatrixWorld();
  }
  frames++;
  fpsTime += dt;
  if (fpsTime >= 1) {
    fps = frames / fpsTime;
    frames = 0;
    fpsTime = 0;
  }
}
if (!TEST_MODE) {
  animate();
}
// In test mode the harness drives the simulation explicitly through
// __babel.frame(n, dtMs) — fixed timestep, no rendering — and asks for
// pixels with __babel.draw() only when a screenshot needs them. Headless
// compositors starve RAF, throttle timers, and SwiftShader cannot keep up
// with a render per step; the simulation itself is cheap and exact.

function seekFocused(): boolean {
  return document.activeElement instanceof HTMLTextAreaElement || document.activeElement instanceof HTMLInputElement;
}

// ------------------------------------------------------------------ input

function requestPointerLock(): void {
  renderer.domElement.requestPointerLock?.();
}

function resumePointer(): void {
  if (controller) controller.enabled = true;
  requestPointerLock();
}

renderer.domElement.addEventListener("click", () => {
  if (!ui.startHidden() || !controller) return;
  if (ui.bookIsOpen()) return;
  requestPointerLock();
});

document.addEventListener("mousemove", (e) => {
  if (document.pointerLockElement === renderer.domElement && controller) {
    controller.mouseLook(e.movementX, e.movementY);
  }
});

document.addEventListener("keydown", (e) => {
  if (!controller) return;
  if (e.code === "Escape") return; // browser handles pointer lock release
  if (seekFocused()) return;
  switch (e.code) {
    case "KeyE":
      if (ui.bookIsOpen()) closeBook();
      else tryOpenAimed();
      e.preventDefault();
      return;
    case "KeyF":
      toggleSeekPanel();
      e.preventDefault();
      return;
    case "KeyH":
      ui.showHelp(!ui.helpIsOpen());
      return;
    case "KeyM":
      muted = ambience.toggleMute();
      ui.setMuteLabel(muted);
      return;
  }
  if (ui.bookIsOpen()) {
    if (e.code === "ArrowRight" || e.code === "PageDown") ui.showPage(ui.shownPage + 1);
    if (e.code === "ArrowLeft" || e.code === "PageUp") ui.showPage(ui.shownPage - 1);
    return;
  }
  controller.keyDown(e.code);
});

document.addEventListener("keyup", (e) => controller?.keyUp(e.code));
window.addEventListener("blur", () => controller?.clearKeys());

window.addEventListener("resize", () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  if (controller) {
    controller.camera.aspect = window.innerWidth / window.innerHeight;
    controller.camera.updateProjectionMatrix();
  }
});

function toggleSeekPanel(): void {
  const open = ui.toggleSeek();
  if (open) {
    document.exitPointerLock?.();
  } else if (controller) {
    controller.enabled = true;
  }
}

// ------------------------------------------------------------------- HUD

function refreshHud(): void {
  if (!world) return;
  const h = hexId({ c: world.c0, f: world.f0 });
  ui.setHud(hexName(h), world.f0, sessionSteps, farFromHome);
}

// ------------------------------------------------------- aiming at shelves

const raycaster = new THREE.Raycaster();
raycaster.far = 2.1;
const AIM_CENTER = new THREE.Vector2(0, 0);
let aimed: { instanceId: number; dx: number; dy: number; wall: number; shelf: number; volume: number } | null = null;

function updateAim(): void {
  if (!world || !controller || ui.bookIsOpen() || controller.mode === "falling") {
    if (ui.bookIsOpen()) return;
    aimed = null;
    ui.setPrompt(null);
    return;
  }
  controller.camera.updateMatrixWorld();
  raycaster.setFromCamera(AIM_CENTER, controller.camera);
  const hits = raycaster.intersectObject(world.booksMesh, false);
  if (hits.length === 0 || hits[0].instanceId === undefined) {
    if (aimed) {
      aimed = null;
      ui.setPrompt(null);
    }
    return;
  }
  const id = hits[0].instanceId;
  if (aimed?.instanceId === id) return;
  const r = world.resolveBookInstance(id);
  if (r.dy !== 0) {
    aimed = null;
    ui.setPrompt(null);
    return; // books on other floors are out of arm's reach
  }
  aimed = { instanceId: id, ...r };
  const spine = spineAt(world.coordAt(r.dx, r.dy), r.wall, r.shelf, r.volume);
  ui.setPrompt(`<span class="spine">${spine}</span> &nbsp;·&nbsp; press <b>E</b> to take this volume`);
}

// ------------------------------------------------------------- book in hand

function tryOpenAimed(): void {
  if (!world || !controller || !aimed) return;
  const r = aimed;
  const coord = world.coordAt(r.dx, r.dy);
  const location: BookLocation = { coord, wall: r.wall, shelf: r.shelf, volume: r.volume };
  openBookAt(location, r.instanceId);
}

function openBookAt(location: BookLocation, instanceId: number, opts?: { page?: number; highlight?: { page: number; start: number; length: number } }): void {
  if (!world || !controller) return;
  ambience.bookSlide();
  controller.clearKeys();
  const book = getBook(location);
  let viewOpts = opts;
  // If this is the sought volume, open it straight to the sought page.
  if (!viewOpts && arrivedSeek) {
    const t = arrivedSeek.location;
    const same =
      t.wall === location.wall &&
      t.shelf === location.shelf &&
      t.volume === location.volume &&
      t.coord.f === location.coord.f &&
      equal(t.coord.c, location.coord.c);
    if (same) {
      viewOpts = {
        page: arrivedSeek.page,
        highlight: { page: arrivedSeek.page, start: arrivedSeek.offset, length: arrivedSeek.length },
      };
      world.setHighlight(null);
      highlightTarget = null;
    }
  }
  if (instanceId >= 0) {
    world.setBookHidden(instanceId, true);
    hiddenInstance = instanceId;
  }
  document.exitPointerLock?.();
  ui.openBook(book, viewOpts);
}

function closeBook(): void {
  if (!world) return;
  ambience.pageFlutter();
  ui.closeBook();
  if (hiddenInstance >= 0) {
    world.setBookHidden(hiddenInstance, false);
    hiddenInstance = -1;
  }
  resumePointer();
}

// ------------------------------------------------------------------- seek

function doSeek(text: string, mode: SeekMode, copyIdx: number): SeekResult | string {
  try {
    const res = seek(text, mode, copyIdx);
    pendingSeek = res;
    window.setTimeout(() => ui.setSeekAddr(hexName(hexId(res.location.coord))), 0);
    return res;
  } catch (err) {
    if (err instanceof SeekError) return err.message;
    throw err;
  }
}

function travelToSeek(): void {
  if (!pendingSeek || !world || !controller) return;
  const res = pendingSeek;
  ambience.whoosh();
  ui.fade(true);
  ui.toggleSeek(false);
  window.setTimeout(() => {
    if (!world || !controller) return;
    // Relocate the universe around the sought hexagon.
    world.c0 = copy(res.location.coord.c);
    world.f0 = res.location.coord.f;
    world.retile();
    farFromHome = true;
    sessionSteps = 0;
    arrivedSeek = res;
    highlightTarget = { dx: 0, dy: 0, wall: res.location.wall, shelf: res.location.shelf, volume: res.location.volume };
    refreshHighlight();
    // Place the librarian in the walk ring before the sought wall.
    const p = world.bookWorldPos(0, 0, res.location.wall, res.location.shelf, res.location.volume);
    const horiz = Math.hypot(p.x, p.z) || 1;
    controller.pos.set((p.x / horiz) * 0.98, 0, (p.z / horiz) * 0.98);
    controller.land();
    const dx = p.x - controller.pos.x;
    const dz = p.z - controller.pos.z;
    controller.yaw = Math.atan2(-dz, dx);
    controller.pitch = Math.atan2(p.y - D.EYE_H, Math.hypot(dx, dz));
    refreshHud();
    ui.fade(false);
    ui.toast(
      `You wake in hexagon ${hexName(hexId(res.location.coord))}. ` +
        `The volume waits on the ${describeWall(res.location.wall)} wall, shelf ${res.location.shelf + 1}, place ${res.location.volume + 1} — it glows for you.`,
      6500,
    );
    window.setTimeout(() => resumePointer(), 80);
  }, 700);
}

function refreshHighlight(): void {
  if (!world) return;
  if (!highlightTarget || !arrivedSeek) {
    world.setHighlight(null);
    return;
  }
  // The glow marks the sought volume while its hexagon is in the window.
  const t = highlightTarget;
  const target = arrivedSeek.location.coord;
  let found: number | null = null;
  if (world.f0 === target.f) {
    for (let dx = -world.quality.rx; dx <= world.quality.rx; dx++) {
      if (equal(world.coordAt(dx, 0).c, target.c)) {
        found = dx;
        break;
      }
    }
  }
  if (found === null) {
    world.setHighlight(null);
    return;
  }
  const pos = world.bookWorldPos(found, 0, t.wall, t.shelf, t.volume);
  world.setHighlight(pos, world.template.wallYaws[t.wall]);
}

function shareLink(): string | null {
  if (!pendingSeek) return null;
  const u = new URL(location.href.split("?")[0]);
  u.searchParams.set("seek", pendingSeek.transliteration.text);
  u.searchParams.set("mode", pendingSeek.mode);
  if (pendingSeek.copy) u.searchParams.set("copy", String(pendingSeek.copy));
  return u.toString();
}

// ------------------------------------------------------------------- fall

function wakeFromFall(): void {
  if (!world || !controller) return;
  ui.showFall(false);
  ui.fade(true);
  ambience.wind(false);
  window.setTimeout(() => {
    if (!world || !controller) return;
    // The Library is merciful in dreams: you wake 8,191 floors below.
    world.f0 -= 8191;
    world.retile();
    controller.pos.set(0, 0, -(D.RAIL_R + 0.55));
    controller.land();
    controller.yaw = -Math.PI / 2; // facing the shaft you fell through
    controller.pitch = 0;
    farFromHome = true;
    refreshHud();
    ui.fade(false);
    ambience.thud();
    ui.toast("You wake on a remote floor. The fall continues without you.", 5000);
  }, 750);
}

// ------------------------------------------------------------- test hooks

if (TEST_MODE) {
  const dbg = {
    frame: (n = 1, dtMs = 16.7) => {
      for (let i = 0; i < n; i++) animate(dtMs / 1000, true);
      return perf.raf;
    },
    draw: () => {
      animate(0.001, false);
      return true;
    },
    state: () => ({
      started: ui.startHidden(),
      hexName: world ? hexName(hexId({ c: world.c0, f: world.f0 })) : null,
      floor: world?.f0 ?? null,
      steps: sessionSteps,
      pos: controller ? { x: controller.pos.x, y: controller.pos.y, z: controller.pos.z } : null,
      yaw: controller?.yaw ?? 0,
      pitch: controller?.pitch ?? 0,
      mode: controller?.mode ?? "none",
      grounded: controller?.grounded ?? false,
      bookOpen: ui.bookIsOpen(),
      seekOpen: ui.seekIsOpen(),
      aimed: aimed ? { wall: aimed.wall, shelf: aimed.shelf, volume: aimed.volume, dx: aimed.dx } : null,
      fps,
      perf: { ...perf },
      render: { calls: renderer.info.render.calls, triangles: renderer.info.render.triangles },
      contextLost,
    }),
    openedBook: () => {
      const b = ui.openedBook;
      if (!b) return null;
      return {
        spine: b.spine,
        hexName: b.hexName,
        wall: b.location.wall,
        shelf: b.location.shelf,
        volume: b.location.volume,
        floor: b.location.coord.f,
        page: ui.shownPage,
        pageTextLength: PAGE_CHARS,
      };
    },
    pageText: () => {
      const b = ui.openedBook;
      return b ? (document.getElementById("pageText")?.textContent ?? "") : "";
    },
    markText: () => document.querySelector("#pageText mark")?.textContent ?? null,
    setView: (yaw: number, pitch: number) => {
      if (controller) {
        controller.yaw = yaw;
        controller.pitch = pitch;
      }
    },
    aimAtBook: (wall: number, shelf: number, volume: number) => {
      if (!world || !controller) return false;
      const p = world.bookWorldPos(0, 0, wall, shelf, volume);
      // Aim at the visible spine face, not the volume's center buried in
      // the case — oblique rays would clip a neighbour first.
      const yawW = world.template.wallYaws[wall];
      p.x -= Math.sin(yawW) * (D.BOOK_D / 2 - 0.005);
      p.z -= Math.cos(yawW) * (D.BOOK_D / 2 - 0.005);
      const eye = new THREE.Vector3(controller.pos.x, controller.pos.y + D.EYE_H, controller.pos.z);
      const d = p.clone().sub(eye);
      controller.yaw = Math.atan2(-d.z, d.x);
      controller.pitch = Math.atan2(d.y, Math.hypot(d.x, d.z));
      return true;
    },
    seekResult: () => {
      if (!pendingSeek) return null;
      return {
        hexName: hexName(hexId(pendingSeek.location.coord)),
        floor: pendingSeek.location.coord.f,
        wall: pendingSeek.location.wall,
        shelf: pendingSeek.location.shelf,
        volume: pendingSeek.location.volume,
        page: pendingSeek.page,
        offset: pendingSeek.offset,
        text: pendingSeek.transliteration.text,
      };
    },
    pressE: () => {
      if (ui.bookIsOpen()) closeBook();
      else tryOpenAimed();
    },
    worldInfo: () => world?.debugInfo() ?? null,
    teleport: (x: number, y: number, z: number) => {
      controller?.pos.set(x, y, z);
      controller?.land();
    },
    setMeshVisible: (name: string, v: boolean) => world?.setMeshVisible(name, v) ?? false,
    canvasStats: () => {
      const c = renderer.domElement;
      const probe = document.createElement("canvas");
      probe.width = 160;
      probe.height = 120;
      const ctx = probe.getContext("2d")!;
      ctx.drawImage(c, 0, 0, 160, 120);
      const img = ctx.getImageData(0, 0, 160, 120).data;
      let sum = 0;
      let max = 0;
      const distinct = new Set<number>();
      for (let i = 0; i < img.length; i += 4) {
        const v = img[i] + img[i + 1] + img[i + 2];
        sum += v;
        if (v > max) max = v;
        distinct.add((img[i] >> 4) | ((img[i + 1] >> 4) << 4) | ((img[i + 2] >> 4) << 8));
      }
      return { mean: sum / (img.length / 4) / 3, max: max / 3, distinct: distinct.size };
    },
  };
  (window as unknown as { __babel: typeof dbg }).__babel = dbg;
}

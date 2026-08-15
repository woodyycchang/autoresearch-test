/**
 * Procedural materials. The Library ships no asset files: wood, stone,
 * leather and brass are all painted here, deterministically.
 */

import * as THREE from "three";
import { Sfc32 } from "../core/rng";

function canvasTexture(
  size: number,
  paint: (ctx: CanvasRenderingContext2D, rng: Sfc32) => void,
  seed: string,
): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d")!;
  paint(ctx, Sfc32.fromString("texture", seed));
  const tex = new THREE.CanvasTexture(canvas);
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

function noiseOver(
  ctx: CanvasRenderingContext2D,
  rng: Sfc32,
  size: number,
  count: number,
  alpha: number,
  light: string,
  dark: string,
): void {
  for (let i = 0; i < count; i++) {
    ctx.fillStyle = rng.float() < 0.5 ? light : dark;
    ctx.globalAlpha = alpha * rng.float();
    const s = 1 + rng.float() * 2.5;
    ctx.fillRect(rng.float() * size, rng.float() * size, s, s);
  }
  ctx.globalAlpha = 1;
}

function woodTexture(): THREE.CanvasTexture {
  return canvasTexture(
    256,
    (ctx, rng) => {
      ctx.fillStyle = "#4a3526";
      ctx.fillRect(0, 0, 256, 256);
      // Grain: vertical streaks with slow waver.
      for (let s = 0; s < 90; s++) {
        const x0 = rng.float() * 256;
        const w = 0.6 + rng.float() * 2.2;
        const tone = 0.75 + rng.float() * 0.5;
        ctx.strokeStyle = `rgba(${Math.floor(58 * tone)}, ${Math.floor(40 * tone)}, ${Math.floor(26 * tone)}, 0.55)`;
        ctx.lineWidth = w;
        ctx.beginPath();
        let x = x0;
        ctx.moveTo(x, -4);
        for (let y = 0; y <= 260; y += 16) {
          x += (rng.float() - 0.5) * 5;
          ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
      noiseOver(ctx, rng, 256, 1600, 0.1, "#7a5a3e", "#241710");
    },
    "wood",
  );
}

function stoneTexture(): THREE.CanvasTexture {
  return canvasTexture(
    256,
    (ctx, rng) => {
      ctx.fillStyle = "#6d6157";
      ctx.fillRect(0, 0, 256, 256);
      // Soft mottling.
      for (let i = 0; i < 220; i++) {
        const r = 6 + rng.float() * 30;
        const g = ctx.createRadialGradient(0, 0, 0, 0, 0, r);
        const tone = rng.float();
        const c = tone < 0.5 ? "109, 100, 92" : "92, 82, 73";
        g.addColorStop(0, `rgba(${c}, ${0.12 * rng.float()})`);
        g.addColorStop(1, "rgba(0,0,0,0)");
        ctx.save();
        ctx.translate(rng.float() * 256, rng.float() * 256);
        ctx.fillStyle = g;
        ctx.fillRect(-r, -r, r * 2, r * 2);
        ctx.restore();
      }
      noiseOver(ctx, rng, 256, 2400, 0.08, "#8a7d70", "#43392f");
    },
    "stone",
  );
}

function floorTexture(): THREE.CanvasTexture {
  return canvasTexture(
    256,
    (ctx, rng) => {
      ctx.fillStyle = "#5b5148";
      ctx.fillRect(0, 0, 256, 256);
      noiseOver(ctx, rng, 256, 2600, 0.1, "#776a5d", "#372e26");
      // Worn flagstone joints.
      ctx.strokeStyle = "rgba(30, 24, 19, 0.5)";
      ctx.lineWidth = 2;
      for (let i = 0; i <= 2; i++) {
        ctx.beginPath();
        ctx.moveTo(0, i * 128 + rng.float() * 8);
        ctx.lineTo(256, i * 128 + rng.float() * 8);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(i * 128 + rng.float() * 8, 0);
        ctx.lineTo(i * 128 + rng.float() * 8, 256);
        ctx.stroke();
      }
    },
    "floor",
  );
}

function leatherTexture(): THREE.CanvasTexture {
  return canvasTexture(
    128,
    (ctx, rng) => {
      // Neutral gray leather; per-book tint comes from instance colors.
      ctx.fillStyle = "#b8b0a6";
      ctx.fillRect(0, 0, 128, 128);
      noiseOver(ctx, rng, 128, 1500, 0.16, "#d8d0c4", "#6a6258");
      // Faint spine bands (visible on the thin faces of the volumes).
      ctx.fillStyle = "rgba(220, 205, 160, 0.5)";
      for (const y of [22, 38, 92, 108]) ctx.fillRect(0, y, 128, 2);
    },
    "leather",
  );
}

export interface Palette {
  wood: THREE.MeshStandardMaterial;
  stone: THREE.MeshStandardMaterial;
  floor: THREE.MeshStandardMaterial;
  book: THREE.MeshStandardMaterial;
  brass: THREE.MeshStandardMaterial;
  lamp: THREE.MeshStandardMaterial;
  darkGlass: THREE.MeshStandardMaterial;
  glow: THREE.MeshBasicMaterial;
}

export function makePalette(): Palette {
  const wood = new THREE.MeshStandardMaterial({
    map: woodTexture(),
    roughness: 0.82,
    metalness: 0.0,
  });
  const stone = new THREE.MeshStandardMaterial({
    map: stoneTexture(),
    roughness: 0.95,
    metalness: 0.0,
  });
  const floor = new THREE.MeshStandardMaterial({
    map: floorTexture(),
    roughness: 0.9,
    metalness: 0.0,
  });
  const book = new THREE.MeshStandardMaterial({
    map: leatherTexture(),
    roughness: 0.75,
    metalness: 0.0,
  });
  const brass = new THREE.MeshStandardMaterial({
    color: 0x9a7b48,
    roughness: 0.38,
    metalness: 0.85,
  });
  const lamp = new THREE.MeshStandardMaterial({
    color: 0x231507,
    emissive: 0xffc26a,
    emissiveIntensity: 2.6,
    roughness: 0.4,
  });
  const darkGlass = new THREE.MeshStandardMaterial({
    color: 0x10141a,
    roughness: 0.05,
    metalness: 0.9,
  });
  const glow = new THREE.MeshBasicMaterial({
    color: 0xffd890,
    transparent: true,
    opacity: 0.0,
    depthWrite: false,
    side: THREE.DoubleSide,
  });
  return { wood, stone, floor, book, brass, lamp, darkGlass, glow };
}

/** Deterministic muted binding tints, applied per instance. */
export const BOOK_TINTS: THREE.Color[] = [
  0x6e3b2c, 0x5d4a33, 0x4f3f50, 0x39474f, 0x584537, 0x6b5135, 0x4a3a2e, 0x52312b,
  0x3f4a3a, 0x5c4d41, 0x66402f, 0x474055,
].map((c) => new THREE.Color(c));

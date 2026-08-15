import { defineConfig } from "vite";

export default defineConfig({
  // Relative base so the build works from any static host or subpath
  // (GitHub Pages, `python -m http.server`, file mirrors of the Library...).
  base: "./",
  build: {
    outDir: "dist",
    target: "es2022",
    chunkSizeWarningLimit: 1200,
  },
  server: {
    port: 5173,
    host: "127.0.0.1",
  },
  preview: {
    port: 4173,
    host: "127.0.0.1",
  },
});

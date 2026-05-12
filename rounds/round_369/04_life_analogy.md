# Life Analogy — Persian astrolabe planispheric projection

The Persian/Islamic **astrolabe** is a flat circular instrument that maps the 3D celestial sphere onto a 2D disc via **stereographic projection**. Properties:
- **Map projection preserves angles** (stereographic is conformal).
- **Latitude-specific overlay (rete)** rotated to specific date/time.
- **One disc per latitude** (each astrolabe is calibrated to one location).
- **Lookup is mechanical**: rotate rete to current date/time/star, read off coordinates.
- **Multi-purpose**: prayer times (qibla), navigation, surveying, time-of-day, latitude.

The interesting principle: a *fixed projection* with *interchangeable overlays* — the projection mathematics is universal; the overlay is locale/use-case-specific.

## Analogical mapping → LLM evaluation/scoring

- Astrolabe base disc ↔ fixed projection function (e.g., stereographic projection of embedding sphere to 2D)
- Interchangeable rete ↔ task-specific evaluation overlay
- Mechanical lookup ↔ deterministic score computation
- Latitude-calibrated ↔ domain-calibrated rubric
- One disc, many uses ↔ one projection, many eval criteria

The mechanism: a **fixed conformal projection** (stereographic mapping of LLM embeddings to a unit disc) with **task-specific interchangeable overlay templates** that mark "regions of interest" on the disc — each overlay is a deterministic lookup table mapping disc coordinates to evaluation criteria. Different from t-SNE/UMAP/PCA (lossy, non-conformal) — preserves angles, can be inverted, supports multiple overlays sharing one base projection.

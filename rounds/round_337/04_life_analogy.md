# R337 — life analogy

## Source: Brittle star (O. wendtii) calcite micro-lens compound eye
- Entire dorsal skeleton functions as compound eye: ~20-50μm calcite microlenses.
- Each lens is a double-lens (Descartes/Huygens) design → aberration-free.
- Lenses focus to 4-7 μm depth into nerve bundles.
- "Sunglasses" pigment cells modulate refractive index for adaptive aperture.

## LLM analogy
**SKELETON-VIS**: vision encoder built as a large array of independent micro-aperture vision encoders, each viewing a small overlapping patch (≈brittle star double-lens covering tiny FoV). Each micro-encoder outputs its own token bundle independently. A learned pigmentation mask globally modulates per-aperture gain (akin to sunglasses cells), giving global aperture adaptation. Differs from standard ViT (single grid patch encoder) and from MERV (multi-encoder spectral specialists).

## Differs from prior art (claim)
ViT/CLIP partitions image into patches processed by ONE encoder. MERV unifies 3-4 specialist encoders with distinct training objectives. Cambrian-1 mixes encoders. SKELETON-VIS uses LARGE-N (~100s) identical micro-encoders on overlapping micro-apertures + a global pigment-modulation gain map.

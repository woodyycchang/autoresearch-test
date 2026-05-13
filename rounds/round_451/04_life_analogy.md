# Life Analogy — Tongan ngatu (tapa cloth) kupesi-grid defect detection

The **Tongan ngatu** (large communal bark-cloth panel):
- Inner-bark layers (feta'aki) fused by thumping into broad sheets.
- Kupesi stencils impose a regular grid of motif-cells (Manulua, leaf cross, lion, dove).
- Each cell has a canonical pattern — a "phase" in motif space.
- Localized defects (mis-aligned cell, displaced motif, edge tear) appear as **phase deviations** from the neighborhood's canonical motif phase.
- Repair: stitch-overlay / patch integrating into surrounding kupesi grid.

**NGATU-DEFECT**: an attention-head positional-grid defect detector. Treat each token's RoPE rotation phase as a cell in a 1D ngatu-grid. Compute a cohomology-style **cocycle invariant** over local windows of phase: if neighborhood phases form a coherent cocycle, no defect; if a window has nonzero defect invariant (phase mismatch with neighborhood), flag and route through a small **correction projection** that re-aligns the phase to the local cocycle. Persistent-homology feature on rolling attention map detects multi-head pattern defects.

## Adjacency
- 2605.03163 Topology-Aware Attention with Persistent Homology + Euler biases
- 2112.15210 Persformer (transformer on persistence diagrams)
- IJSAT 2026/2/10799 Persistent Homology + Transformer Defect Detection
- 2603.27153 Spectral conditioning attention (related — not topology)

Expected FAIL — persistent-homology + topology-aware attention layer is well-covered for transformer defects.

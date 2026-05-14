# Life Analogy — Tibetan sand mandala 4-fold ritual cycle with deity-syllable-order dissolution

The **Tibetan sand mandala**:
- 4-fold ritual cycle: (1) outline (geometric foundation) → (2) colored-sand fill → (3) consecration → (4) dissolution (sweep inward to center → pile → cast into water).
- Dissolution sequence: deity syllables removed first (reverse-creation order), then geometry, then sand swept from edge to center forming pile.
- Impermanence doctrine (Anicca); non-attachment; sand-to-water reintegration cycle; mandala dismantled in deity-vs-geometry order.

**MANDALA-4-FOLD-DEITY-FIRST-DISSOLUTION-BASIN-RESET**: 4-stage basin-stability training-cycle with deity-first dissolution-order + center-spiral sweep + water-reintegration + non-attachment regularizer. (1) **4-stage cycle (outline → fill → consecrate → dissolve)** every K_cycle steps: model training proceeds through 4 named training stages then is partially dissolved/reset to mitigate basin-overfitting and induce broader basin-exploration. (2) **Deity-syllable-first dissolution-order**: when dissolving, parameters are reset in a specific order — high-level "deity" (output head, top-layer) first, then "geometry" (mid-layer), then "sand" (bottom-layer embeddings) — preserving foundational structure while resetting fine-grained specialization. (3) **Center-spiral sweep R_spiral**: dissolution proceeds by spiraling inward from layer-edges to layer-center; equivalent to gradient-descent on regularization term λ·|θ - θ_center|² that pulls parameters toward a center anchor. (4) **Water-reintegration cycle**: dissolved parameters are pooled and re-distributed across model layers (mixing) before next training cycle begins — analogous to sand cast into water re-circulating. (5) **Non-attachment regularizer L_noatt**: at each cycle's end, regularization term applied to discourage over-attachment to current basin minimum — favors larger basin radii. (6) Differs from R404 + R420 + R434 + R450 + R460 + R471 + R485 + R498 + R510 BOZUY-KEREGE-UUK-TUNDUK-BASIN (4-component kerege+uuk+tunduk+koshma yurt structural decomposition + interlaced rank-1 LoRA + central anchor + felt smoothing) and R523 MARAMURES-BLOCKBAU-DOVETAIL-NO-NAIL-BASIN (dovetail pair-wise corner-alignment + no-norm + Blockbau row-lock + slim clock-tower) by 4-fold ritual cycle + deity-first dissolution-order + center-spiral sweep + water-reintegration + non-attachment regularizer.

## Adjacency
- Basin-Like Loss Landscape LLM 2505.17646
- Spike No More Stabilizing Pre-training
- Methods Improving LLM Training Stability 2410.16682
- Scaling with Collapse 2509.25087

Expected FAIL — basin-loss-landscape + spike-aware + training-stability + collapse-trajectory literature covers.

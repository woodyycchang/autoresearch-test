# R255 — life analogy

## Source domain: silver niello inlay
- Two-step decorative process:
  1. **Engrave channels** into a silver surface — DELIBERATELY REMOVING material along a designed pattern.
  2. **Fuse black sulfide-alloy filler** (Ag-Cu-Pb-S) into the engraved channels using flux and heat; scrape excess; polish.
- The result: a black-on-bright contrast pattern that is **structurally bonded** to the host metal (not a surface coating that can rub off). The black filler occupies exactly the negative space carved out.
- Key principle: SUBTRACTIVE-THEN-FILL with contrasting material; the filler's role is to make the engraved pattern legible by inverting brightness, anchored mechanically (channel walls hold the filler) AND chemically (alloy fusion).

## LLM analogy candidate
**Niello-style contrastive subspace inlay (NSCI)**: a basin-stability technique for LLM safety alignment. (1) **Engrave** = identify the unsafe-content subspace via probing (e.g., the top-k principal components of refusal/unsafe trajectory diffs); mechanically zero (project away) these components in the residual stream — this is SUBTRACTIVE removal of unsafe-axis content. (2) **Fill** = trained a small "niello-filler" module (8-rank delta) that generates a CONTRASTING safe-axis vector specifically tailored to fill the carved unsafe-subspace; it is FUSED into the residual at the same point as the projection, using a learnable flux-coefficient that smoothes the boundary. (3) **Polish** = final activation re-normalization restores token-level scale. The "engraved" unsafe channels are now filled with explicit safe-axis content, mechanically anchored at the same subspace coordinates. Distinct from RLHF: alignment is achieved by SUBSPACE SURGERY (subtractive + contrastive fill), not gradient adjustment. Distinct from refusal-vector steering: the filler is rank-specific to the engraved channels, not a global bias.

## What differs from prior art (claim)
LOL contrastive decoding (2408.08769) contrasts amateur vs full model layers — not a subspace-surgery + contrasting-fill. Layer-aware embedding fusion (2504.05764) selects layers but does not subtract-then-fill. FtZ (2509.00664) fuses two encoders by cross-attention. None retrieve a subtractive-then-contrast-fill at residual-subspace level for safety alignment.

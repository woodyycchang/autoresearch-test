# R263 — life analogy

## Source domain: Tlingit/Haida bentwood box
- One cedar plank with 3 kerf-grooves carved halfway through at the intended corner positions.
- Plank is steamed (softened) → bent at the kerfs → folded into 4-sided box.
- Once dry, the kerfs harden and the box is RIGID despite having been ONE piece.
- The box has only one true seam (where the two free ends meet, pegged or sewn shut).
- Two-state material: pliable when wet/hot, rigid when dry/cool.

## LLM analogy candidate
**Kerf-grooved single-tensor weight folding (KGSTWF)**: parameterize a model's weight as ONE flat tensor with **pre-engraved kerf-fold positions** — designated rank-axis indices where the tensor will fold at deployment. During training, the tensor is "pliable" — folds are NOT applied; the full flat tensor receives gradients. At deployment, **a single fold transform** is applied at each kerf, collapsing the tensor into a smaller compact structure (e.g., factored low-rank product across folded axes). Critical property: gradients flow through the FLAT representation; folding is a one-time deploy operation, NOT learned per-step. After folding, the result is RIGID (immutable). Distinct from Miura-ori (R253): KGSTWF uses 3-cut single-fold, not tessellated multi-vertex folds. Distinct from quantization: quantization changes precision but not topology; KGSTWF changes topology via one-time fold.

## What differs from prior art (claim)
µnit Scaling FP8 (2502.05967) is precision-side. LLMOrbit (2601.14053) is taxonomy. Symbolic Tensor Graph (2511.10480) is workload synthesis. None retrieve pre-engraved-fold-points + train-flat + deploy-fold one-time topology change.

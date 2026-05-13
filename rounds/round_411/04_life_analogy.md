# Life Analogy — Squid chromatophore (4-quadrant motor unit color cell)

The **squid chromatophore** is a pigment-expansion organ:
- Each chromatocyte has 18-30 radial muscles arranged around a central pigment sac.
- Recent (2025) imaging reveals **4 independent motor neurons** per chromatophore, each controlling a CONTIGUOUS PETAL-SHAPED QUADRANT of the radial-muscle ring.
- 4-quadrant expansion gives the chromatophore the ability to produce ANISOTROPIC color shapes (petal-asymmetric) at 125 ms timescales.
- Each quadrant is independently gated.

The unique principle: **single output (color spot) decomposed into 4 independent gated petal-quadrants** — instead of one binary "on/off" control, the chromatocyte achieves nuanced control via 4 parallel quadrant-level gates each receiving its own neural signal. Petal-asymmetry is achievable.

## Analogical mapping → 4-quadrant context-gated attention head

- Chromatophore output (color spot) ↔ a single attention-head output vector
- 4 quadrants ↔ 4 sub-channels of the head's value dimension (d_v split into 4 equal subvectors)
- 4 independent motor neurons ↔ 4 separate gating signals
- Petal-asymmetric expansion ↔ asymmetric weighting of the 4 sub-channels by 4 separate gates

The mechanism: **CHROMATOPHORE-QUAD 4-channel context-gating per head** — in a multi-head attention layer, split each head's value-dimension d_v into 4 equal quadrants {v^(1), v^(2), v^(3), v^(4)}. For each quadrant compute an INDEPENDENT gate g^(k) = σ(W_g^(k) x_t) from the current token's representation (4 separate gate parameters per head). The head output is the concatenation [g^(1) v^(1); g^(2) v^(2); g^(3) v^(3); g^(4) v^(4)]. This gives a per-head, per-quadrant context-gated value — strictly more flexible than the head-level single gate of Gated Attention (2505.06708). Differs from (a) Gated Attention (one head-level sigmoid gate per head), (b) GQA/MQA (key sharing, not value-quadrant gating), (c) SeerAttention (self-distilled gate, single-level), (d) AnchorFormer by introducing 4 INDEPENDENT per-quadrant context-gates per head.

## Note on adjacency

The context-gating form fits. Adjacent: Gated Attention (the closest twin — also gates head output but with a SINGLE gate per head), MoE (expert gates not quadrant gates), PILL adapter-attention gate (separate adapter not value-decomposed). Distinct: PER-HEAD-PER-QUADRANT gating with quadrant=4 fixed split.

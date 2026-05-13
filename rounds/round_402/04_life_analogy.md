# Life Analogy — Tuvan igil two-string fiddle sympathetic resonance

The **Tuvan igil** (two-string bowed horse-head fiddle):
- Two horsehair strings tuned a perfect fifth apart, both unfretted.
- The PLAYED string excites the OTHER string via sympathetic resonance — when both fundamentals lie in shared harmonic series, the unbowed string vibrates "for free", contributing implicit overtones.
- Player exploits this by tuning carrier-overtone pair so a single bowed note produces a perceived two-voice texture.
- Mechanism: explicit 2-string design produces IMPLICIT additional voices via shared-harmonic coupling, not via additional strings.

## Analogical mapping → LLM multi-head attention coupling

- Bowed string ↔ explicitly parameterized attention head
- Unbowed sympathetic string ↔ implicit "ghost" subspace
- Shared harmonic series ↔ shared key-subspace alignment
- Perceived two-voice texture ↔ effective head-multiplicity > parameter-count

The mechanism: **IGIL-DUAL-SYMPATHY** — a 2-head attention design where two designated "carrier" heads are loss-coupled via a sympathetic-resonance regularizer (penalising key-subspace alignment that does NOT lie on the harmonic series of carrier-head 1). The regularizer creates an implicit "ghost head" whose attention pattern is the harmonic-series partial of carrier-head-1's key subspace, retrieved without an extra Q/K/V parameter set. Differs from MoE (extra params), Shared-QKV (parameter sharing), Linear-Predictability-of-Heads (post-hoc observation): IGIL-DUAL-SYMPATHY explicitly TRAINS for ghost-head emergence via harmonic-series loss.

## Note on adjacency

Strong neighborhood prior art:
- 2603.13314 Linear Predictability of Attention Heads — predictable head dependencies (post-hoc).
- 2602.16740 Quantifying Head Stability — intra-layer key-subspace alignment.
- Awesome-Attention-Heads survey enumerates head-coupling literature.
The IGIL-DUAL-SYMPATHY explicit-training-for-ghost-head twist may not have direct prior art at the harmonic-series-loss level, but the harmonic-loss work (R279 reference: Harmonic Loss arxiv) suggests the components exist. Expected FAIL with strong neighborhood overlap.

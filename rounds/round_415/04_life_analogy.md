# Life Analogy — Curling sweeping (transient ice-melt friction reduction)

**Curling sweeping**:
- Sweepers' brooms create kinetic energy → localized HEAT → thin transient water film on ice.
- The thin water film reduces friction between stone and ice.
- The melt is TRANSIENT — refreezes after stone passes.
- Sweepers can selectively brush in front of one side of the stone to STRAIGHTEN its curl trajectory.

The unique principle: **transient local energy injection produces transient local low-friction state** — the ice surface state is locally and temporarily modified IN ADVANCE of the moving object; the modification is sufficient for the immediate transit and then reverses. Energy is spent only where needed, only when needed.

## Analogical mapping → transient runtime low-precision activation

- Curling stone path ↔ token sequence being decoded
- Stone position ↔ current decode position t
- Ice friction ↔ default high-precision (fp16/bf16) compute cost
- Brooming creates water film ↔ runtime decision to drop a window of decode steps to lower precision (fp8/int4)
- Selective one-side brooming ↔ selective lower-precision for specific layers
- Refreeze ↔ revert to high precision when the sweeper window passes

The mechanism: **CURLING-SWEEP transient runtime-repair low-precision compute** — at inference, monitor a per-step "smoothness" signal s_t (e.g., output logit entropy or per-token uncertainty). When s_t is low (high confidence, "easy" decode), sweep the NEXT k tokens (k=5 typical) to LOWER PRECISION (fp8) in the FFN layers. When s_t rises (high uncertainty, "hard" decode), revert to full precision. The sweep window is transient and predictive. Differs from (a) Progressive Mixed-Precision Decoding (also varies precision across tokens but typically scheduled by phase, not dynamically triggered), (b) Speculative decoding (different paradigm — draft+verify, not precision-switch), (c) Static mixed-precision quantization (no runtime switching), (d) Phase-aware mixed-precision (phase-based not signal-triggered) by combining (i) PER-STEP SMOOTHNESS SIGNAL + (ii) DYNAMIC WINDOW of lower precision + (iii) REVERSIBLE PRECISION SWITCH per token.

## Note on adjacency

The runtime-repair form fits. Adjacent: Progressive Mixed-Precision Decoding, Speculative decoding (different paradigm), ResQ low-rank residuals. Distinct: ENTROPY-TRIGGERED dynamic precision-window with per-token reversion.

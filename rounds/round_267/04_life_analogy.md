# R267 — life analogy

## Source domain: Saami / cross-country differential ski wax
- A cross-country ski has TWO friction zones along its length:
  - **Tip and tail**: GLIDE wax minimizing kinetic friction.
  - **Center (under the foot, "kick zone")**: GRIP wax maximizing static friction during the kick stroke.
- Selection of each wax depends on snow temperature/crystal type.
- The same ski exhibits TWO OPPOSITE friction regimes spatially separated; the skier benefits from BOTH simultaneously.

## LLM analogy candidate
**Bipolar-zone friction-regime split adapter (BZFRS)**: separate the model's layers into TWO zones with OPPOSITE update regimes:
- **Glide zone** (early/late layers): aggressive LR + frequent updates → low "training friction" → fast adaptation to new context.
- **Grip zone** (middle layers): conservative LR + sparse updates → high "training friction" → durable knowledge retention.
The zone boundaries are CONDITIONED on the input distribution's temperature (estimated from token-entropy / OOD score): cold (in-distribution) → narrow grip zone (most layers glide-adapt); warm (out-of-distribution) → wider grip zone (most layers protect knowledge). Distinct from gradual unfreezing: BZFRS uses SPATIAL separation by layer-index AND input-conditioned temperature gating.

## What differs from prior art (claim)
DAT (2604.05375), LLMOrbit (2601.14053), Forward Replay (2605.00358) don't retrieve spatial-layer split with bipolar grip/glide friction regimes + input-distribution-temperature gating.

# R288 — life analogy

## Source: Drosera sundew two-tentacle prey capture
- TWO anatomically distinct tentacles: snap (75ms catapult, ballistic) + glue (2min slow closure, accurate).
- Stage 1: prey touches snap-tentacle → fast catapult to leaf center (capture-FIRST, low accuracy).
- Stage 2: slow glue-tentacle bends in over ~2 min to firmly hold + drag prey to digestive center (refine + commit).
- The mechanism is INTRINSICALLY TWO-TIMESCALED: fast wide-net + slow narrow-grip.

## LLM analogy
**DROSERA (Drosera Two-Timescale Reasoning)**: an LLM inference architecture with TWO attention-channels active per query:
- SNAP channel: very-low-rank fast linearized attention pass — produces an immediate ballistic answer in <100ms.
- GLUE channel: full quadratic attention runs in parallel on the prior layers + the snap-output — refines the snap's draft over ~2s.
The user sees the snap-result first; the glue-result is delivered as a refinement-correction if it differs ≥ threshold. Two distinct attention substrates, fast-coarse and slow-precise.

## Differs from prior art (claim)
- SampleAttention (2406.15486): two-stage attention with KV filtering — adjacent, but single attention substrate just with two filter passes.
- Star Attention (2411.17116): two-phase block-local then global — sequential, not concurrent two-channels.
- Win Fast or Lose Slow (2505.19481): speed/accuracy tradeoff control, not a parallel-two-channel architecture.
- DROSERA's distinguishing feature: TWO CONCURRENT attention substrates run in parallel with snap-result streamed first + glue-result delivered as refinement on the same query — not a sequential pipeline but parallel-bicameral.

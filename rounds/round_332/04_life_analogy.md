# R332 — life analogy

## Source: Pistol shrimp cavitation snap
- Latched elastic claw stores tension over ~msec.
- On release, claw snaps shut at 25 m/s → cavitation bubble.
- Bubble collapse generates plasma + sonoluminescence (~4800°C, peak 80 kPa @ 4cm, 218 dB).
- Mechanism: SLOW store-up + INSTANTANEOUS impulsive release; brief high-amplitude pulse stuns prey.

## LLM analogy
**SNAP-ATTN**: phase-coherent attention burst. Over N consecutive layers, accumulate "latch potential" — a coarse accumulator that sums normalized attention-score deltas. When latch crosses release threshold, the next layer fires a single SHARP-temperature (very low τ) attention burst on top-K most-attended tokens; subsequent layers reset latch and resume normal-τ attention. Hypothesis: occasional sharp-burst layers transmit consolidated information without raising overall network temperature.

## Differs from prior art (claim)
SpikeLLM (2407.04752) spikes individual neurons. Saliency-based gating attends every layer. Anti-attention-sink work modulates sinks but not latch-and-release. SNAP-ATTN's distinctive contribution is LATENCY-ACCUMULATED LATCH-AND-RELEASE: slow inter-layer accumulator + impulsive sharp-temperature burst at a single chosen layer.

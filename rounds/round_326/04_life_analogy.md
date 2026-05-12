# R326 — life analogy

## Source: Mantis shrimp 16-channel cone color vision
- 12-16 photoreceptor types covering 300-720nm + polarization (humans have 4).
- Each photoreceptor type tuned to a narrow wavelength band; channels operate independently.
- Color "recognition" rather than "discrimination" — no cross-channel comparison; temporal signaling + scanning eye movements.
- Parallel data streams from retina → CNS dramatically reduce downstream analytical load.

## LLM analogy
**STOMATOPOD-HEAD**: split a single attention head into 16 narrow-band specialist sub-heads, each operating on a fixed disjoint frequency slice of token-positional spectral content (e.g., precomputed DCT bins). No cross-channel interaction within the layer; only at later aggregation. Hypothesis: drastically reduces inter-head redundancy AND lowers per-channel softmax-temperature variance.

## Differs from prior art (claim)
GQA/MQA reduce head count by sharing K/V; MoA tailors sparse configurations per head; Gated DeltaNet introduces gating across heads. None impose narrow-band frequency-disjoint independent specialists with cross-channel comparison delayed to a later aggregator stage modelling stomatopod parallel-pathway architecture.

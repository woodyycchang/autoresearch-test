# R287 — life analogy

## Source: Hawaiian fishpond (loko iʻa kuapā with mākāhā gate)
- Stone wall encloses tidal area; mākāhā = lashed branch GRATE in sluice channel.
- The grate is SIZE-SELECTIVE: small fingerlings pass in with tide; once they've grown beyond grate spacing, they CANNOT exit.
- The tide does ALL the transport work; the gate is passive.
- Variable spacing = different size selectivity over the season; the kiaʻi-loko adjusts as cohort matures.

## LLM analogy
**MAKAHA (Size-Selective Tidal Admission Filter)**: a training-curriculum gate where the pretraining-corpus pipeline applies a SIZE-VARYING token-count threshold at fixed checkpoint intervals: small examples flow into the training set freely; as the model gains capacity (over epochs), the gate spacing CLOSES (raise minimum token-count / minimum perplexity-threshold) — only larger, more complex examples can pass while previously-admitted small examples already inside contribute to ongoing training. The closing-spacing IS the curriculum.

## Differs from prior art (claim)
- DataFlow (2512.16676): multiple filters applied at preparation time, not progressive-gate over training.
- Multilingual filtering (2505.22232): quality-based admission, not size-selective progressive gate.
- Progressive training (Phi-3 style): mixes filtering with stage gating but not specifically a size-monotone-closing gate at tide-fixed checkpoints.
- MAKAHA: explicit progressive monotone-closing size-gate on token-count + complexity at checkpoint cadence — combination not in standard data-curriculum literature.

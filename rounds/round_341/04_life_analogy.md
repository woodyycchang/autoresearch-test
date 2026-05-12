# R341 — life analogy

## Source: Hummingbird hovering figure-eight wingbeat
- Both downstroke AND upstroke produce lift (inverted upstroke).
- 75/25 asymmetric lift distribution between strokes.
- Figure-eight wingbeat: continuous force production through turn-around.
- Hovering = continuous balance with bidirectional propulsion.

## LLM analogy
**FIGURE-EIGHT-DECODE**: bidirectional decode pattern that produces useful update both on the forward token-prediction pass AND the backward "regret/revise" pass at decoder layer. Forward pass = standard decoding. Reverse pass = micro-revision back to the previous token's prediction using updated context. Both contribute (asymmetrically — 75% forward / 25% revise). Each token generates two micro-pass results that are blended.

## Differs from prior art (claim)
Standard autoregressive decoding is unidirectional. Speculative decoding produces drafts in parallel. Lookahead decoding extends n-grams. FIGURE-EIGHT-DECODE differs by producing useful prediction signal on a backward revise pass through the same layers — bidirectional lift-style decoding rather than parallel/lookahead extension.

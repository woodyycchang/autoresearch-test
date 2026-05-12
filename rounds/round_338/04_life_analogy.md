# R338 — life analogy

## Source: Cassowary casque low-frequency-tuned receiver
- 17cm keratin casque on cassowary head; spongy and resilient.
- Hypothesized as resonant receiver for 23-Hz vocalizations (long-distance forest communication).
- Low frequencies propagate well through dense vegetation; casque tunes to these long-range signals.
- High frequencies attenuated by foliage and likely attenuated by casque itself.

## LLM analogy
**CASQUE-RECEIVER**: residual-stream "low-frequency receiver" — a tunable resonant filter applied to the residual stream that PASSES long-range positional content (low-frequency along the sequence axis) and ATTENUATES local positional content (high frequency along the sequence axis). Each layer has a dedicated low-pass residual-stream branch that complements the standard attention branch. Hypothesis: forces long-range information to propagate via the explicit low-pass branch, reducing reliance on attention sinks.

## Differs from prior art (claim)
Attention sinks emerge naturally in residual stream. LoFT-LLM applies LLMs to low-frequency forecasting. α-entmax adapts sparsity along sequence. CASQUE-RECEIVER differs by INTRODUCING an explicit low-pass residual-stream branch per layer, dedicated to long-range information propagation, as an architectural complement to attention.

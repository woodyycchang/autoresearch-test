# R347 — life analogy

## Source: Solifugid (sun spider) sensory hair array
- Dense bristles + setae over body + pedipalp; thousands of fine sensors.
- Multi-modal (chemo/hygro/thermo/tactile/vibration).
- Smaller anterior pair of true legs is sensory-supplement to pedipalps.
- Mechanism: massive parallel high-density multi-modal sensor coverage.

## LLM analogy
**HAIRARRAY-INPUT**: input-tokenizer extension with K=10000+ tiny "sensory hair" modules each computing a single named cheap feature over the raw input (n-gram frequency, character-class transitions, special-token marks, etc.). The result is a dense multi-channel sparse feature vector added to the embedding. Mechanism: parallel high-density cheap feature multiplicity at the embedding stage.

## Differs from prior art (claim)
SensorLLM aligns sensor data to language. TVL is multi-modal touch+vision. Standard ViT uses patch embeddings. HAIRARRAY-INPUT differs by introducing LARGE-N (10000+) per-feature cheap detector modules ADDED to embedding stage producing dense sparse feature signal — solifugid-style massive parallel multi-modal coverage.

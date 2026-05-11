# R239 — life analogy

## Source domain: submarine passive sonar triangulation
- Submarine carries multiple hydrophone arrays (bow, hull, towed, flank); each array gives a BEARING (direction-of-arrival) for any acoustic source.
- Two or more bearings from spatially-separated arrays TRIANGULATE the source position with no active emission (passive).
- Wide-Aperture Arrays (WAA) on hull use TIME-DIFFERENCE-OF-ARRIVAL across hull-spread elements to RANGE in addition to bearing.
- Narrowband classification: LOFAR analysis identifies the source's spectral signature (engine/propeller harmonics), separating it from ocean noise.

## LLM analogy candidate
**Triangulated attention-head provenance**: treat each layer's set of attention heads as a HYDROPHONE ARRAY. For any output token, the heads jointly attend over context; the relative attention-amplitude profile across heads at a given layer gives a "bearing" on which CONTEXT REGION drove the output. Multiple LAYERS provide spatially-separated arrays. Triangulate by combining bearings from K layers: the intersection of K rays in context-position space localizes the SOURCE TOKEN(S) that drove the output. Narrowband classification: spectral fingerprint of the attention pattern (eigenvalue profile of attention matrix at that layer) classifies the source-token's ROLE (entity / connective / refusal-cue / fact-quote / etc). The whole pipeline is PASSIVE: no model retraining or active probing required.

## What differs from prior art (claim)
Multi-head attention literature (TransMLA 2502.07864, MEA 2601.19611, TensorLLM 2501.15674) focuses on EFFICIENCY or INTERACTION ACROSS HEADS — not on triangulating provenance across LAYERS. Attention-attribution work (e.g., Captum integrated gradients) computes per-head importance but does not use cross-layer triangulation. Language-Attention-Heads (2511.07498) identifies specialized heads but does not triangulate.

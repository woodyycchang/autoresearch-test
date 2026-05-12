# R241 — life analogy

## Source domain: optical caustic networks
- Caustics are singular curves/surfaces where light rays bunch and intensify (e.g. dancing light patterns on pool floor; rogue-wave focusing).
- Berry catastrophe classification: exactly 7 stable elementary caustic types (fold, cusp, swallowtail, butterfly, hyperbolic-umbilic, elliptic-umbilic, parabolic-umbilic).
- A caustic has a SHARP STRUCTURE — the locus is well-defined, finite-dimensional, and TOPOLOGICALLY CLASSIFIED.

## LLM analogy candidate
**Catastrophe-classified attention-spike audit**: take the per-token attention map at each layer and identify positions where attention amplitude has a SHARP SINGULAR FOCUS (analog: optical caustic). Project each such caustic into the 7-elementary-catastrophe space — does the attention-spike shape resemble a FOLD (one-dimensional ridge), CUSP (two-dimensional crease), SWALLOWTAIL, etc.? The catastrophe class is a structural fingerprint of the attention spike. Audit usage: anomalous attention spikes (e.g., during jailbreak attacks or hallucination onset) may exhibit DIFFERENT catastrophe topology than benign spikes. The fingerprinting is at structure level, not at amplitude level.

## What differs from prior art (claim)
Attention-spike literature (Star Attention 2411.17116, Controlling Logits 2511.21377) focuses on AMPLITUDE control (entropy collapse, QK norm). Logit-suppression vulnerability (2405.13068) is an attack. None propose CATASTROPHE-TOPOLOGY classification of attention spikes using the 7 elementary-catastrophe taxonomy from Berry/Thom. The audit-via-singular-structure-class is distinguishing.

# R345 — life analogy

## Source: Mantis shrimp polarization vision
- Rhabdom rows 1-4 = color; rows 5-6 = polarization (linear + circular).
- 3 rhabdoms sense one polarization plane, 4 the perpendicular.
- 8th cell rhabdomere = wave retarder converts circular → linear pol.
- Eye rotates to maximize polarization contrast against background.

## LLM analogy
**POLARIZATION-CHANNEL**: dedicate K hidden-state channels of each token's representation to encode an explicit "polarization-style" attribute — e.g., factuality polarity, sentiment, or query intent — orthogonal to the semantic channels. The polarization channels are linearly + circularly orthogonal pairs that can encode 2 binary attributes per pair without interfering with semantic encoding.

## Differs from prior art (claim)
Single-hidden-channel scaling (ACL 2025) modifies 1 channel for position bias. Polarization-aware decoding hasn't been an explicit architectural choice. POLARIZATION-CHANNEL differs by RESERVING orthogonal hidden-channel pairs (linear + circular pair encoding) for explicit polarity attributes, modelled directly on mantis-shrimp visual encoding architecture.

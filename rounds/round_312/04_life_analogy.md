# R312 — life analogy

## Source: Hovercraft / air-cushion vehicle
- Lift fan + skirt produces continuous pressurized air cushion between vehicle hull and ground.
- Eliminates surface friction; vehicle floats on low-pressure cushion separate from ground material.
- Lift produced even at zero forward velocity — unlike ground-effect vehicles which need forward motion.

## LLM analogy
**HOVER-ATTN**: replace dot-product attention's O(n²) "ground friction" with a continuous low-pressure "cushion layer" between queries and keys. A small constant-rank pressure-pad operator P ∈ ℝ^(r×d) (r << d) is inserted between Q·K^T and the softmax; P maintains a constant separation budget while letting all token-pair interactions pass through without quadratic dot-product cost.

## Differs from prior art (claim)
Linear attention via kernel approximation (Performer, Linformer); RALA augments rank; A3 splits QK/OV/MLP into low-rank; CPA prioritizes globally. None use the specific "cushion-pad operator with constant separation budget" formulation — but the constant-rank low-rank intermediate is essentially identical.

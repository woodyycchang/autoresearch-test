# R262 — life analogy

## Source domain: Hagia Sophia pendentive
- Architectural problem: place a CIRCULAR DOME on a SQUARE base. The square corners and circle perimeter don't match.
- Solution: install four **pendentives** — concave triangular sections of a sphere — at each corner. Each pendentive's BOTTOM tapers to a point at one corner pier; its TOP edge follows part of the circle the dome rests on.
- All vertical load from the dome flows through the four pendentives to four corner piers.
- The pendentives RESOLVE GEOMETRIC INCOMPATIBILITY (square ↔ circle) while CONCENTRATING and CHANNELING loads to the four pier anchor points.

## LLM analogy candidate
**Pendentive-style geometric-domain bridge adapter (PGDBA)**: install four corner adapters between two LLM components with INCOMPATIBLE representation geometries (e.g., grid-tokenized image patches → 1D continuous text embedding, or low-rank LoRA delta → full-rank base weight). Each pendentive-adapter is a spherical-triangle-style map from one corner of the source-domain manifold to a vertex of a base-pier vocabulary; jointly the four pendentive-adapters form a "transition vault" that resolves geometric incompatibility while concentrating gradient flow into four pier-coordinates (anchor tokens / anchor neurons that absorb the load). Crucially: the four pendentives are CONSTRAINED to lie on a sphere (constant curvature), preventing degenerate flat-projection collapse. Distinct from a single cross-modal projection: PGDBA uses FOUR pendentive-shaped adapters at corner-concentration + constant-curvature constraint.

## What differs from prior art (claim)
Geometry-Preserving Composition (2410.09908) is sparse adapter reconstruction. Scaling-Aware Geometry Grounding (2602.02780) is atom-level structural adapter. GNSP (2507.19839) is null-space projection. None retrieve a FOUR pendentive-shaped adapters + corner-pier-concentration + constant-curvature constraint geometric-bridge.

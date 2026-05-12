# R318 — life analogy

## Source: Spider orb-web spiral architecture
- 15-35 radial threads (non-sticky, structural).
- Concentric capture spiral with adhesive droplets covers radial intersections.
- Each prey impact is detected by the radial nearest to the impact point.
- Web geometry is sparse but covers entire capture area.

## LLM analogy
**WEB-SPIRAL**: sparse attention pattern. Define N "radial" attention anchors (fixed positions distributed evenly) + M concentric "spiral" attention arcs. Compute attention only at radial-spiral intersections (~N·M attention pairs rather than full O(L²)). Pattern is sparse but covers all token positions through the radial-spiral overlay.

## Differs from prior art (claim)
Radial Attention (2506.19852) is the closest direct precedent — uses radial sparse pattern with energy decay. Sparse Transformer (OpenAI 2019) uses strided + block patterns. Pi-Attention uses periodic sparsity. WEB-SPIRAL's radial+spiral specific geometry is functionally close to Radial Attention.

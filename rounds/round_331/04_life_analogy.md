# R331 — life analogy

## Source: Pangolin overlapping keratin scales
- Hexagonal overlapping arrangement: each scale at the center of 6 neighbors.
- Hydration-dependent: dry = hard/stiff (defensive), wet = plastic (deflective).
- Crack-deflection: cracks propagate along scale interfaces, away from soft tissue underneath.
- Nano-scale interlocking suture between scale lamellae for shear resistance.

## LLM analogy
**SCUTE-MEMORY**: KV-cache organized as overlapping hexagonal shards. Each shard stores tokens with 6-neighbor overlap of context tokens (rather than disjoint chunks). On retrieval, the union of 7 overlapping shards (center + 6 neighbors) provides robust context window. Damage / cache eviction of one shard does not erase a region because adjacent shards retain overlap. Mechanism: redundant overlapping memory for robust long-context retrieval.

## Differs from prior art (claim)
RAG chunks with 10-20% overlap (1D linear). LMCache uses linear KV partitions. Sliding-window attention uses 1D overlap. SCUTE-MEMORY differs by using 2D hexagonal overlap pattern with 6-neighbor union retrieval — fundamentally a hex-tiling of context space rather than linear partition with edge overlap.

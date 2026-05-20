# R645 step 01

**Timestamp:** 2026-05-19T20:20:05Z

## Scan focus
Persistent homology (PH) as mechanism source for hierarchical episodic memory. PH gives birth/death pairs (b_i, d_i) for topological features (loops, voids) across filtration scales. The candidate transfers PH to LLM episodic memory: each episode produces a persistence diagram of its semantic graph; retrieval uses persistence-distance-based matching.

## Motivation
mechanism_transfer: persistent homology IS a computable algebraic invariant of filtered simplicial complexes. The candidate stores per-episode persistence diagrams and uses bottleneck/Wasserstein distance for retrieval — direct transfer.

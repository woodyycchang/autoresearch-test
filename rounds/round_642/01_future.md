# R642 step 01

**Timestamp:** 2026-05-19T20:08:20Z

## Scan focus
Cheeger inequality from spectral graph theory as mechanism source for attention-bottleneck diagnosis. Cheeger: λ_2(L_G) / 2 ≤ h(G) ≤ sqrt(2 λ_2) where h(G) is the conductance / sparsest cut. λ_2 of the graph Laplacian quantifies bottlenecks. The candidate transfers this to the attention graph: detect "phase-incoherent" attention patterns via low λ_2 of the attention-graph Laplacian.

## Motivation
mechanism_transfer: Cheeger inequality is a rigorous bound. The attention map between tokens IS a weighted directed graph; the corresponding Laplacian's λ_2 measures bottleneck strength. The candidate transfers the inequality directly to diagnose / regularize attention bottlenecks.

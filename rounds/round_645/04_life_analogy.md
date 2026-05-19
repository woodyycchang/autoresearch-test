# R645 step 04 — Persistent homology

For filtered simplicial complex K_0 ⊂ K_1 ⊂ ... ⊂ K_n, PH gives persistence pairs (b_i, d_i) per dimension. Bottleneck distance d_B(D, D') between two diagrams measures structural similarity.

### Mechanism transfer
Episodic memory: each episode E is encoded as a simplicial complex over its entity-relation graph (k-skeleton). Filtration: edge weight threshold scan. Compute PD_E in dim 0, 1, 2. Store {PD_E, raw_text_E}. Retrieval: at query Q, compute PD_Q; rank episodes by d_B(PD_Q, PD_E).

mechanism_transfer: PH is a closed-form algebraic invariant; bottleneck distance has explicit formula.

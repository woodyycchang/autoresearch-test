# R642 step 04 — source mechanism

## Source: Cheeger inequality (spectral graph theory)

For graph G with Laplacian L_G = D - W, where W is weighted adjacency:
λ_2(L_G) / 2  ≤  h(G)  ≤  √(2 λ_2(L_G))

where h(G) = min_{S ⊂ V} cut(S, V\S)/min(|S|,|V\S|) is the Cheeger constant.

Low λ_2 = bottleneck; high λ_2 = well-mixed.

### Mechanism transfer
Attention map A_h ∈ R^{n×n} (head h) at a transformer layer is a weighted DIRECTED graph. Use symmetrized adjacency Ã = (A + A^T)/2. Compute L_Ã = D_Ã - Ã. λ_2(L_Ã) per head per layer is a Cheeger-bounded bottleneck signal. Add regularizer R_Cheeger = - Σ_{l,h} log(λ_2(L_Ã^{l,h}) + ε) — push spectral gap up to avoid bottleneck.

Direct mechanism transfer: Cheeger inequality applies algebraically to any weighted graph including attention maps.

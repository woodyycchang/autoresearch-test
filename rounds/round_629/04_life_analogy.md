# R629 step 04 — source mechanism

## Source: Random Matrix Theory (Marchenko-Pastur law)

For X ∈ ℝ^{m×n} with i.i.d. entries of variance σ², the eigenvalues of XX^T/n converge to the Marchenko-Pastur distribution
ρ_MP(λ) = (1/(2πσ²λ)) sqrt((λ_+ - λ)(λ - λ_-))   for λ ∈ [λ_-, λ_+]
with λ_± = σ² (1 ± sqrt(c))² where c = m/n.

### Mechanism transfer to LLM
Bouchaud–Potters cleaning replaces sample eigenvalues lying inside MP envelope with their median (a constant), keeping only the outlier "structural" eigenvalues. The candidate transfers this cleaning rule to PER-LAYER LoRA capacity allocation: estimate MP envelope for each layer's W_q, W_k, W_v, W_o weight matrices; count outliers above λ_+; allocate LoRA rank r_l proportional to the outlier count.

Not metaphor — MP law literally describes random matrices; deviation from MP IS structural information.

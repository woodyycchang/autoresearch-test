# R641 step 04 — source mechanism

## Source: Stein Variational Gradient Descent (Liu-Wang 2016)

SVGD update for N particles {θ_i}:
φ*(x) = (1/N) Σ_j [k(θ_j, x) ∇_{θ_j} log p(θ_j) + ∇_{θ_j} k(θ_j, x)]
θ_i ← θ_i + ε φ*(θ_i)

First term: weighted attraction toward target log-prob gradient.
Second term: repulsion among particles (kernel diversity).

### Mechanism transfer
The candidate treats per-layer hidden states {h_l : l=1..L} as SVGD particles. Compute Stein update φ*_l using kernel k(h_l, h_l') and score ∇ log p_target(h) for a learned target. Layer-wise residuals are nudged: h_{l+1} = h_l + α φ*_l(h_l). Acts as cross-layer regularizer enforcing diversity + alignment.

mechanism_transfer: SVGD update is closed-form; particles-as-layers is a structural correspondence.

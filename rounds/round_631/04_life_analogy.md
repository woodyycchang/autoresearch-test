# R631 step 04 — source mechanism

## Source: Wilsonian Renormalization Group flow

Effective Lagrangian L_eff(λ; μ) at energy scale μ obeys flow:
dλ_i / d(log μ) = β_i(λ).

Fixed points β(λ*)=0 are universality classes; relevant operators flow away, irrelevant operators flow toward fixed point.

### Mechanism transfer
The candidate: for each transformer block l, compute effective couplings c_l ∈ R^K from a fixed set of measurement operators applied to layer activations (e.g., spectral radius of attention map, ECE of residual, kurtosis of MLP output). Track {c_l} across layers as discrete-scale RG trajectory; regularize fine-tuning to keep the trajectory close to a target β-function fixed point.

Direct mechanism transfer — RG flow is the math of multi-scale coarse-graining, deep networks have been formally connected to RG.

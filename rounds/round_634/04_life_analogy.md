# R634 step 04 — source mechanism

## Source: Kernelized Stein Discrepancy (KSD)

For target p with score s_p = ∇ log p, RKHS H with kernel k, the KSD is:
KSD²(q, p) = E_{x,x' ~ q} [u_p(x, x')] where u_p is Stein kernel involving k and s_p.

KSD = 0 iff q = p.

### Mechanism transfer
For LLMs, the score function over the discrete token sequence is given by ∇_e log p_θ(y|x) where the gradient is over an embedding rep of y. The candidate computes KSD for n=64 sampled completions per prompt against a reference distribution p_ref (e.g., the same prompt evaluated by a frozen base model). High KSD per prompt indicates the policy has drifted; per-prompt diagnostic for RLHF drift.

Direct mechanism transfer: KSD is a closed-form proper discrepancy.

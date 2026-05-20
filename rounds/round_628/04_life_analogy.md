# R628 step 04 — source mechanism

## Source: Wasserstein-1 / Kantorovich-Rubinstein optimal transport

### Math
W1(μ,ν) = inf over couplings π of E[|X-Y|] = sup over 1-Lipschitz f of (E_μ f - E_ν f) (Kantorovich-Rubinstein duality).

### LLM mapping (mechanism transfer)
The optimal 1-Lipschitz dual potential `f*` characterizes the direction of distribution change. A gradient ∇L with components aligned with `f*` shifts the policy distribution; components orthogonal to `f*` leave W1 invariant.

The candidate: maintain a learned 1-Lipschitz critic `f_φ` (the W1 dual) for the pre-training distribution, and project all DPO/PPO gradient updates onto the orthogonal complement of ∇f_φ. This is the W1 null space — updates within it cannot move the policy in W1 distance against the reference. It generalizes KL-bounded RLHF where KL is replaced by W1 with semantic-aware token geometry.

This is mechanism_transfer: same Kantorovich-Rubinstein dual operator, applied as a gradient projector instead of a regularizer.

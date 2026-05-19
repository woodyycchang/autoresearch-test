# R647 step 04 — LP duality

Primal LP: min c^T x s.t. Ax≤b, x≥0. Dual: max b^T y s.t. A^T y ≥ c, y≥0. Strong duality at optimum: c^T x* = b^T y*. Complementary slackness: y_i*(b_i - A_i^T x*) = 0.

### Mechanism transfer
At each decode step t, formulate token-choice LP: minimize -log p_θ(z|context) subject to active constraints A_k (e.g., length-remaining ≥ 0, must-cover-set count). Solve LP relaxation to get dual variables y_t per constraint. Use y_t as soft gating weight: logits_adjusted = logits - Σ_k y_t,k g_k(z), where g_k(z) is constraint-violation indicator.

mechanism_transfer: LP duality is exact; dual variables ARE the multipliers in the Lagrangian.

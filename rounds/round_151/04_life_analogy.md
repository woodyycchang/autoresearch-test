# Round 151 — life analogy

In a forest stand, individual trees compete for light, water, and nutrients. As mean diameter D grows, the stand cannot support arbitrarily many stems N per hectare — competition kills the smallest until (N, D) lies on a fixed log–log line (Reineke's frontier, slope ≈ −1.605). The stand *traverses the null-space* of this constraint as it ages: every viable (N, D) state is on or below the frontier; stands grow upward only by trading density for diameter.

By analogy, a transformer has a fixed compute / KV-cache budget per layer. The number of "active" attention heads H and the per-head effective rank r (or per-head context length) face an analogous constraint: H × r ≤ layer_budget. A naive transformer keeps both H and r fixed, but **could** "self-thin" — drop low-utility heads to let surviving heads grow their effective rank along a constraint frontier as input length grows. The transformer's (H, r) state would traverse the null-space of this constraint dynamically.

The Reineke analog asks: is there a slope-≈-1.6 self-thinning rule on (H, r) that 2024-2026 efficient-attention or head-pruning work has converged on?

# R636 step 04 — source mechanism

## Source: Parallel transport on the Stiefel manifold

Stiefel manifold St(p,n) = {Y ∈ R^{n×p} : Y^T Y = I}. Tangent space at Y: T_Y St = {Δ : Y^T Δ + Δ^T Y = 0}.

Levi-Civita parallel transport along geodesic Y(t) = U exp(t Σ) U^T Y(0) preserves tangent vectors via the explicit Edelman-Arias-Smith formula.

### Mechanism transfer
The candidate: sequentially fine-tune LoRA adapters B_t ∈ St(r,d_in) on tasks T_1, T_2, …. Between consecutive tasks, parallel-transport adapter B_t from current frame to new frame using closed-form Stiefel transport. Then continue fine-tuning. This treats sequential-task adapters as topological-defect-like discontinuities healed by geometric continuation.

Direct mechanism transfer: parallel transport is the canonical operation; St(p,n) has closed-form formulas.

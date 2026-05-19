# R643 step 04 — source mechanism

## Source: Hopf bifurcation (dynamical systems)

For ẋ = f(x; μ), if at μ=μ_c the Jacobian J = ∂f/∂x has complex-conjugate eigenvalues λ_± = α(μ) ± iω(μ) with α(μ_c) = 0 and (α'(μ_c) ≠ 0), a Hopf bifurcation occurs at μ_c. Stable equilibrium becomes a limit cycle.

### Mechanism transfer
RLHF training dynamics θ_{t+1} = θ_t + η ∇_θ J(θ) can be linearized; the per-step "Jacobian" J_t = ∂(∇J)/∂θ. The candidate computes top-2 complex-conjugate eigenvalues of a low-rank approximation of J_t (via Hutchinson trace + Lanczos). Track Re(λ) over training; near-zero crossing signals impending Hopf — early-stop checkpoint.

shared_math_structure: full Jacobian is too large; the candidate uses low-rank approximation, so structural rather than literal mechanism transfer.

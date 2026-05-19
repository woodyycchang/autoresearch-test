# R637 step 04 — source mechanism

## Source: Fokker-Planck equation

For SDE dθ = -∇L(θ) dt + √(2D) dW, density p(θ,t) obeys:
∂p/∂t = ∇·(p ∇L) + D Δp.

Stationary: p∞(θ) ∝ exp(-L(θ)/D) — Gibbs distribution at temperature D.

### Mechanism transfer
SGD with mini-batch noise covariance Σ_batch(θ) (Mandt-Hoffman-Blei 2017) approximates a Langevin SDE with state-dependent diffusion. The candidate computes the effective Σ_batch and ADJUSTS injected noise so that total diffusion = D⁺ I, where D⁺ is calibrated to yield a target temperature T over the loss. The training algorithm explicitly targets the Gibbs sampler at temperature T as the stationary distribution.

Direct mechanism transfer: FP is the literal PDE of SGD dynamics under the SDE approximation.

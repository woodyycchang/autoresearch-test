# R626 step 04 source-domain mechanism

## Source domain: Lyapunov stability theory (classical dynamical systems)

### Core math
A Lyapunov function V: X → ℝ is a positive-definite scalar function whose value along trajectories of a dynamical system decreases monotonically. For continuous-time `ẋ = f(x)`, stability requires `dV/dt = ∇V · f(x) ≤ -α V(x)` (exponential stability with rate α). For discrete-time `x_{k+1} = g(x_k)`, the analogous inequality is `V(x_{k+1}) - V(x_k) ≤ -α V(x_k)`.

### Why this is mechanism-level, not metaphor
SGD/Adam on a loss landscape IS a discrete-time dynamical system. The loss function `L(θ)` itself is often used as a Lyapunov candidate to prove convergence in convex optimization. For non-convex losses (LLM training), local Lyapunov certificates have been studied as convergence diagnostics.

The candidate proposal applies the same mathematical structure (positive-definite per-layer scalar with monotone-decrease constraint) AT THE PER-LAYER GRANULARITY during LLM fine-tuning, rather than at the global loss level.

### Not metaphor:
- The Lyapunov inequality is the same algebraic object in both domains
- The proof technique transfers directly: choose V, compute ΔV under the update rule, bound it
- No analogical leap: SGD literally is a dynamical system

### Structural map
- Classical state x ↔ Per-layer parameter block θ_l
- Vector field f(x) ↔ Gradient -∇_l L
- V(x) ↔ Per-layer Lyapunov candidate V_l(θ_l, t)
- α (rate) ↔ Per-layer adaptive step
- ΔV ≤ 0 invariant ↔ Per-layer monotone-decrease certificate

The mechanism transfer is direct.

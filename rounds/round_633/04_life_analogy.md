# R633 step 04 — source mechanism

## Source: Helmholtz-Hodge decomposition

Vector field F on closed manifold splits uniquely as F = ∇φ + curl ω + H (gradient + co-gradient + harmonic). On simplicial complexes the discrete-Hodge variant gives an L²-orthogonal decomposition via Laplacian eigenspaces.

### Mechanism transfer
For SGD, consider the batch-gradient vector field g_b(θ): on each parameter slice, the per-example contributions form a vector field over data space. Hodge decomposition over the batch gives:
- ∇φ_b: "potential" part — the gradient of a coherent per-sample loss landscape direction
- curl ω_b: "rotational" — disagreement among examples in the batch
- H_b: harmonic — null-space residual (rare)

The candidate: attenuate curl component (by factor γ_curl < 1) and harmonic component (by γ_H ≈ 0), keeping the potential part at full strength. This is feedback-attenuation in the strict optimizer sense.

Direct mechanism transfer: Hodge decomposition is a rigorous, well-defined L²-orthogonal split.

# R633 step 01

**Timestamp:** 2026-05-19T19:31:15Z

## Scan focus
Hodge decomposition (de Rham/Helmholtz) of vector fields as mechanism source for gradient field separation. Hodge decomposition: any vector field on a closed manifold splits uniquely into gradient + curl + harmonic component: F = ∇φ + curl ω + H. The candidate transfers this to per-batch gradient analysis — decompose stochastic gradient into "potential" component (consistent with a single scalar loss), "rotational" component (data-disagreement noise), and "harmonic" component (manifold-tangent).

## Motivation
mechanism_transfer: Hodge decomposition is a rigorous functional-analytic identity on vector fields. Recent work (Hodge-aware GNNs, simplicial neural networks) uses Hodge decomposition. The candidate transfers to per-batch gradient feedback attenuation: attenuate rotational/harmonic components to reduce optimizer "noise tongue" effects.

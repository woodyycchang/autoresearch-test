# R686 motivation

Helmholtz decomposition: vector field F = ∇φ + ∇×A. The two components
are orthogonal in L²; the curl-free part has zero curl, the divergence-
free part has zero divergence. Applied to LLM gradients, the curl-free
part is the "gradient descent direction"; the divergence-free part is
the "rotational" component that doesn't decrease loss locally. Motivation:
mechanism_transfer.

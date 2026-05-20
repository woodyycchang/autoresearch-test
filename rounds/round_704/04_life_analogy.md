# Life analogy — spectral sequence convergence

When peeling an onion, each layer adds finer detail until you reach the core where no more new structure emerges. A spectral sequence is a generalized onion: pages E_2, E_3, ..., E_r refine each other; when the differential d_r becomes zero, the sequence has converged to E_∞ — no more refinement available.

For LLM layers: representation refinements diminish at depth. Compute the analog of E_r differential between layer outputs; stop deeper layers when this differential is below epsilon.

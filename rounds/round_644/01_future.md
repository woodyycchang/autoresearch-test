# R644 step 01

**Timestamp:** 2026-05-19T20:16:20Z

## Scan focus
Eikonal equation ‖∇u‖ = 1/v(x) as mechanism source for shortest-path information propagation in deep networks. Eikonal governs wavefront propagation in media of varying speed v; solution u(x) is travel-time from a source. The candidate transfers this to representing "information depth" — the layer index at which information about a specific token x reaches the output — and applies fast-marching algorithms to design / regularize layer routing.

## Motivation
shared_math_structure: Eikonal is a first-order PDE for shortest paths in heterogeneous media. Layer depth = effective travel time for token information; v(x) = "computational speed" at each token. The candidate uses fast-marching to solve a discretized Eikonal on the layer-token grid as null-space-traversal mechanism.

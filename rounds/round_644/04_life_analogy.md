# R644 step 04 — Eikonal mechanism

Eikonal: ‖∇u(x)‖ = 1/v(x), u(x) = arrival time of wavefront from boundary source.
Fast Marching: O(N log N) algorithm using min-heap and upwind finite-difference.

### Mechanism transfer
The candidate constructs a token-layer 2D grid. Speed v(t,l) = capacity of layer l to process token t — learned per-token-per-layer scalar. Solve discretized eikonal u(t,l) via fast marching; u(t,L) = effective depth needed for token t. Route token t to exit at layer ⌈u(t,L)⌉. This is null-space-traversal because tokens "complete" along the shortest information path through the network.

shared_math_structure: eikonal is a PDE; layer-grid is discrete; structural analogy.

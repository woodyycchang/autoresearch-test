# R677 Life-analogy / motivation

The Petersen graph is the smallest 3-regular graph with girth 5 and
chromatic number 3 — a structural extremum used as a stress test for
graph algorithms. It has 10 vertices, 15 edges, every vertex degree 3,
and no triangles or 4-cycles.

In MoE routing, the choice of which experts are "neighbors" determines
how soft-routing weights compose across layers. Most MoE routers use
fully-connected expert graphs (every expert reachable in 1 step). The
Petersen topology imposes a structured sparsity: each expert has only 3
neighbors, but the chromatic-3 partition guarantees no local clique.

Mechanism transfer: use the Petersen adjacency as the gating mask
between consecutive routing layers; the chromatic-3 partition defines
a group-consistency loss; vertex-transitivity ensures all experts have
equivalent in/out routing pressure.

Motivation: mechanism_transfer / shared_math_structure (Petersen graph
is a canonical mathematical object; not metaphor).

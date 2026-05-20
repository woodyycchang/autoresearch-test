# R689 motivation

Voronoi tessellation: K points partition R^n into convex cells; each
cell is the set of points closest to its site. Used in nearest-neighbor
classification, k-means clustering.

For MoE: K experts at site points; route by nearest. Boundary-token
soft routing handles ambiguity. Site update = move experts based on
performance. Motivation: mechanism_transfer.

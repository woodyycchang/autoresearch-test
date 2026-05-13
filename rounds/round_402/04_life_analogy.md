# Life Analogy — Crystal twinning (reflective contact twin)

**Crystal twinning** is a structural phenomenon in mineralogy where:
- Two adjacent crystals of the SAME mineral share a **composition plane** (a planar crystallographic surface).
- Across that plane, the two crystals are related by a **non-symmetry mirror reflection** (the twin plane is NOT a symmetry plane of the untwinned crystal).
- Reflection twins are a SUBTYPE: the two crystals appear as mirror images of each other.
- Twin laws (Albite, Carlsbad, Baveno) define specific composition planes for specific mineral structures.

The unique principle: **non-symmetry mirror reflection across a shared plane** — two structures that share a fixed boundary surface (the composition plane) reflect each other across an operation that is NOT a normal symmetry of either alone. The reflection produces a "lattice neighborhood" that is locally continuous but globally introduces a twinning boundary.

## Analogical mapping → multi-head attention twin head pair

- Crystal A ↔ attention head A
- Crystal B ↔ attention head B
- Composition plane ↔ a fixed projection plane in residual stream
- Mirror reflection across composition plane ↔ weight-mirror constraint between A and B
- Non-symmetry mirror ↔ the mirror is NOT an existing symmetry of the model

The mechanism: **TWIN-PLANE attention head reflective tying** — in a transformer with H attention heads per layer, designate pairs of heads (A_i, B_i) and a fixed projection plane P_i (chosen at initialization, e.g., a random ONS direction). Enforce W_B = M_{P_i} W_A where M_{P_i} is the householder reflection across P_i; equivalently, train only W_A and at every step set W_B = reflection(W_A). The result: B is a "twin" of A across plane P. This reduces parameter count by factor ~2 per twinned pair, but more importantly, it forces each pair to span a null-space + mirror-image complement which lives in the orthogonal complement of P. Differs from (a) GQA (multi-query grouping; not reflection), (b) parameter tying like ALBERT (cross-layer not cross-head, identity tie not reflection), (c) symmetric weight tying (identity not reflection) by using a NON-SYMMETRY MIRROR REFLECTION about a fixed random plane.

## Note on adjacency

The construction lives in the null-space of the orthogonal complement of P: the active head pair (A, B) explores the head-direction subspace via complementary mirror, and the null space of P remains untouched. This is the "null-space-traversal" form. Adjacent: Quantum mirror-symmetric kernels in physics-informed networks; sign-flipped weights in BinaryConnect. Distinct: weight reflection across a CHOSEN non-symmetry plane (not identity, not sign-flip) is rare.

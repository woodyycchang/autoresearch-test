# Life Analogy — Korean maedeup knotted norigae tassel

The **Korean maedeup** knot system:
- 30+ basic knot types (38 in some sources): dorae, maehwa, dragonfly, butterfly, etc.
- 3D symmetric knots — string originates + creates shape + returns to origin.
- Each knot has a topological invariant signature (cycle return + crossing-pattern).
- Norigae 3-fold structure: mainbody-knot-tassel.
- Categories: royal (seals, swords), religious (Buddhist), fashion (norigae).

**MAEDEUP-INVARIANT**: a topological-invariant defect detector for attention pattern. (1) Treat token attention pattern as a knotted curve in attention-graph space. (2) Compute crossing-number-based topological invariant J(pattern) per attention head — a discrete summary of attention's knot type. (3) Defect detection: a pattern whose invariant J deviates from canonical norigae-template (single dorae knot) signals attention pathology. (4) Repair: re-route attention weights to restore canonical J. (5) Knot-type catalog: maintain catalog of 30+ canonical attention "knot types"; misclassified head triggers reclassification + repair.

## Adjacency
- Geometric Learning Knot Topology 2305.11722
- Learning Topological Invariance 2504.12390
- Knotted Molecular Transformer 2501.12780
- NN Knot Invariants 1610.05744

Expected FAIL — topological invariants + attention defect detection well-covered.

# Life Analogy — Norwegian rosemaling C-stroke / S-stroke curve-vocabulary

The **rosemaling** (Norwegian decorative folk painting, 1700s-1850s):
- Two building-block strokes: **C-stroke** (single arc) + **S-stroke** (double-curve).
- Regional styles (Telemark, Hallingdal, Rogaland, Os) — each combines C/S strokes with distinctive proportions.
- Compositions built up by combining strokes into kurver (scrolls), florals, flowing patterns.
- Inspired by Baroque/Rococo acanthus carvings.
- Used on ale bowls, stools, chairs, cupboards, trunks — daily life objects.

**ROSEMALING-C-S-STROKE-CURVE-VOCAB-DEFECT**: attention pattern catalog via 2-primitive curve vocabulary + regional-style proportion + composition-defect detection. (1) **Primitive curve vocabulary**: each attention pattern at a layer represented as a sequence of {C-stroke, S-stroke} primitives — discrete tokenization of attention curve over position axis. (2) **Stroke detection**: per attention head, compute winding-number-like topological signature (# of monotone arcs, direction changes, branches) to classify as C-type or S-type. (3) **Regional-style proportion**: each model layer learns a "regional style" = preferred C:S ratio + scale parameters. (4) **Composition-defect detection**: a layer's composition is defective if its stroke-sequence deviates from the regional-style distribution by KL > tau_def (out-of-style head). (5) **Repair**: defective heads are re-aligned via projection onto regional-style mean stroke-distribution. (6) **Building-block reduction**: every higher-level pattern (florals, scrolls) is decomposable into C+S — explicit compositional vocabulary. (7) Differs from R476 IDRIJA-LACE-DEFECT (graph-minor catalog) + R489 MEDALLION-ROT-DEFECT (rotation equivariance) + R501 BAGAJDA-BORE-PROFILE-ATLAS (spectrum centroid) by 2-primitive curve vocabulary (C+S) + winding-number signature + regional-style proportion + composition decomposition + KL-deviation defect.

## Adjacency
- Circuit Tracing Attribution Graphs (closest — graph decomposition)
- Developmental Interpretability 2508.15841 (concept manifolds)
- Attention Head Entropy ICLR 2025 (defect score)
- P0 Sink Circuit 2603.06591

Expected FAIL — circuit decomposition + attention head taxonomy + manifold compositional interpretation literature fully covers.

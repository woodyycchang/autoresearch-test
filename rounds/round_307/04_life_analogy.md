# R307 — life analogy

## Source: Sand dollar pentameric radial symmetry
- Adult echinoderms (sand dollars, starfish) display 5-fold radial body plan: 5 ambulacra "petals" arranged symmetrically around a central axis.
- Each petal is an independent gas-exchange / locomotion functional unit; the 5 petals contribute pentameric aggregated signal at the central oral region.
- Larvae are bilaterally symmetric; the pentameric symmetry is a developmental transformation — emerges from 2 to 5 around a central rotation axis.

## LLM analogy
**PENTA-RADIAL-AGG**: at each attention layer, split the head-dimension space into 5 ORTHOGONAL "petal" subspaces of equal dimension; compute attention independently in each petal; aggregate the 5 outputs via a learned radial recomposition that respects the pentameric rotational symmetry (uses the irreducible representation of cyclic group C5). Forces 5-fold rotationally-symmetric attention structure as architectural inductive bias.

## Differs from prior art (claim)
Standard multi-head attention partitions head_dim into n_heads independent subspaces with NO symmetry constraint. Hadamard transforms (2603.08343) mix dimensions through butterfly couplings (group SO(2)^n-like). MAHA (2512.14925) is multiscale aggregation by depth, not radial symmetry. None impose a 5-fold cyclic-group inductive bias on within-layer head subspace decomposition.

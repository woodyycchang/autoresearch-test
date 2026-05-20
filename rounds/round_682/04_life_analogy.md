# R682 motivation

Tate cohomology Ĥ^n(G, M) splices group homology and cohomology into a
single 2-periodic exact sequence; classes are computed via the norm map
N: M_G → M^G. In class field theory, this captures global-vs-local
arithmetic obstructions.

For LoRA: pretrained weights have implicit symmetries (permutation,
sign-flip, rescaling). A LoRA delta either preserves or breaks these
symmetries. Tate cohomology gives a 2-periodic invariant of the
symmetry-class. Constraining updates to preserve the class is a more
algebraic regularizer than current SVD-based PiSSA.

Motivation: shared_math_structure.

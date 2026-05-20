# R688 motivation

Hahn-Banach: a bounded linear functional φ on a subspace M of a normed
space X extends to a bounded linear functional Φ on X with ||Φ|| = ||φ||.
The extension is not unique but the norm is preserved.

For KV cache: define φ on past-context tokens as the "essential info"
quantification; extend Φ to full context; the cached tokens whose
Φ-projection is below ε can be pruned without changing the essential-info
norm. Motivation: shared_math_structure.

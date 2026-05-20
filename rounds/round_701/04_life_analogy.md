# Life analogy — Stirling partition MoE

Counting how many ways to distribute N distinct gifts among K children with no child empty-handed is the Stirling number of the second kind. The "ways" form an enumerable index. A particular distribution corresponds to a single integer ∈ [0, S(N,K)).

For MoE: tokens are gifts, experts are children. A Stirling-indexed routing function maps an input-derived integer (e.g., hash of context window) to a specific set-partition. Every batch of N tokens with K experts uses a deterministic partition index, eliminating routing variance under fixed seed and inputs.

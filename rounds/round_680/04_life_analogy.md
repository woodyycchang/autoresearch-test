# R680 Life-analogy / motivation

Lindenmayer systems (L-systems, Aristid Lindenmayer 1968) are formal
grammars with PARALLEL rewriting: every symbol in the current string is
rewritten simultaneously according to production rules. This is distinct
from Chomsky grammars (sequential rewriting) and yields fractal
self-similarity at each depth level.

In LLM CoT, the candidate enforces parallel rewriting: each reasoning
step expands into K sub-steps simultaneously, recursively, to depth d.
Self-similarity is the key constraint: sub-step structure mirrors
parent-step structure, enforcing hierarchical decomposition.

Motivation: shared_math_structure (L-systems are a precise grammar
class; not metaphor; the parallel-rewriting property is the operational
hook).

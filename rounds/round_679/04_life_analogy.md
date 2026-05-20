# R679 Life-analogy / motivation

Brun's sieve (Viggo Brun, 1919) bounds the number of integers up to N
that survive sifting by multiple independent prime-divisibility
conditions. The key technical move is truncated inclusion-exclusion:
sum to level r in the alternating series, with r chosen to balance
truncation error against main-term magnitude.

For LLM token pruning, treat K different attention-head importance
scores as analogous to K congruence conditions. The Brun upper-bound
formula gives an explicit count estimate on tokens satisfying ALL K
criteria — applicable when no single attention head provides a sharp
threshold but the joint sift is provably bounded.

Motivation: mechanism_transfer — Brun's truncated-inclusion-exclusion is
a precise mathematical mechanism, not metaphor; the LLM-side application
is the joint-sifting framework.

(WARNING: vocabulary overlap with LLM-Sieve and SafeSieve papers is HIGH;
the FROZEN step 10 keyword rule may surface-fire on "sieve" alone.)

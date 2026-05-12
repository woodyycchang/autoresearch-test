# R226 — life analogy

## Source domain: bobbin lace
- Two-move calculus: every stitch is exactly `twist (T)` or `cross (X)`; arbitrary 2D designs emerge from sequences of these two operations.
- Pricking = pre-positioned anchor lattice. Pins on pricking holes pin transient state; once a region is complete, pins are removed and the lace holds via friction of crossings alone.
- Non-continuous Honiton style: motifs are made FIRST as independent sprigs, then joined with ground threads. Distinct from continuous-thread Bruges style.
- Bobbins themselves carry persistent state (the thread + tension); each bobbin pair is essentially a "channel" weaving through the pin lattice.

## LLM analogy candidate
Each layer-merge operation in a multi-expert LLM stack is decomposed into ONLY two primitive ops: `twist` (within-expert parameter rotation / sign-flip on a low-rank subspace) and `cross` (between-expert parameter swap on a specified subspace). A user-defined "pricking" (pin schedule) over a parameter coordinate graph specifies which subspace participates in which `twist`/`cross` at which depth. Sprigs (sub-skills) are first composed independently to sprig-level expert weights, then ground-stitched into a final merged model via the same two-op calculus. The pricking is the program; the bobbins are the experts; the lace is the deployed merged model.

## What differs from prior art (claim)
Model merging literature uses arithmetic ops (TIES, DARE, Task Arithmetic) or routing-on-input. Bobbin-lace framing reduces merge to a two-op grammar (T, X) over a pricking-coordinate graph that is human-authored. Closest published work: Mediator (2502.04411) uses layer-wise selective averaging + uncertainty routing; not a two-op program over pin-anchored subspaces.

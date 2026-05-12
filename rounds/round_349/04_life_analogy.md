# R349 — life analogy

## Source: Gazelle stotting honest costly signal
- Vertical leaps with stiff legs visible to predators.
- Only fit individuals can perform → handicap-principle honest signal.
- Predator sees stotting → abandons chase (predator and prey both benefit).
- Costly signal cannot be faked by weak individuals.

## LLM analogy
**STOT-SIGNAL**: multi-agent communication primitive — each worker agent emits a COSTLY honesty-signal alongside its response (e.g., a separately-computed verification trace, a tool-execution receipt, or a cryptographic-style proof-of-work). Receiving agents weight worker outputs by signal cost. Workers that cannot produce expensive valid signals are treated as deceptive/unreliable.

## Differs from prior art (claim)
TRiSM (2506.04133) is comprehensive trust framework. Collusion detection (2604.01151) is post-hoc analysis. Governance signals are configuration metadata. STOT-SIGNAL differs by REQUIRING each worker agent to emit a COSTLY HONESTY-SIGNAL per response — handicap-principle costly signaling making deception expensive.

# R330 — life analogy

## Source: Venus flytrap bistable trap with 2-stimulation rule
- 3 trichome trigger-hairs on each lobe.
- First action potential pre-loads charge; trap does NOT close.
- Second AP within ~20-30s commits the snap (bistable mechanical state flips lobe convex → concave in 0.3s).
- Specialized ion transporters enable fast-propagating APs and Ca2+ waves.
- Mechanism prevents false triggers from wind/dust (a single accidental contact does nothing).

## LLM analogy
**TRAP-COMMIT**: TWO-stimulus pre-commit gate on attention activation. A potentially expensive computation (e.g., chain-of-thought expansion, tool call, retrieval) requires TWO matching activation signals within a sliding-window of T tokens. First match = pre-load (raises internal threshold or sets latent flag); second match = commit (executes the expensive op). Single accidental trigger never commits — strong false-positive rejection.

## Differs from prior art (claim)
Gated Attention (NeurIPS 2025) uses sigmoid gating per-head per-token. MoE routing fires on per-token best-k. Tool-call routing fires on single classifier match. TRAP-COMMIT differs by requiring TEMPORAL DOUBLE-MATCH within a sliding window — a two-stimulus pre-commit gate as false-positive defense for expensive operations.

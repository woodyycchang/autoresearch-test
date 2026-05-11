# R242 — life analogy

## Source domain: chess transposition table
- Two different MOVE SEQUENCES can produce the IDENTICAL board position. A chess engine uses Zobrist hashing to detect this and REUSE the previous search result rather than re-evaluating.
- Hash key: incremental XOR of position-piece-square bitstrings. Two positions equal → identical hash.
- Reuse strategy: if hash hit AND prior search depth ≥ current, return prior evaluation.
- Collision handling: store verification key alongside hash to detect rare aliasing.

## LLM analogy candidate
**Reasoning-trace transposition table**: define a CANONICAL HASH of an LLM's intermediate reasoning state (sequence of CoT steps + tool calls + retrieved facts + current goal). Two different reasoning paths that arrive at the SAME canonical state get the same hash; the system reuses the cached final answer (or partial answer) of the prior path. The canonical hash is computed incrementally from invariants (set of facts retrieved, set of tools called, current sub-goal, current open hypotheses) rather than full token history — so semantically-equivalent reasoning paths that differ in wording all map to the same hash. Verification key stored to handle rare aliasing. Use case: cost-saving in agentic CoT where the same sub-problem is reached repeatedly via different paths.

## What differs from prior art (claim)
KV cache hashing (DASH-KV 2604.19351, KV reuse 2511.01633) is at TOKEN/ATTENTION level — exact-prefix reuse. Reasoning-trace canonicalization is at SEMANTIC level — different token sequences that share the same set of invariants map to one hash. This is the chess-transposition discipline applied to reasoning state, not prefix matching.

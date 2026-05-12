# Life Analogy — Hokulea celestial-checkpoint dead-reckoning correction

The Hokulea voyaging canoe uses a hybrid navigation:
- **Dead reckoning** = constant mental tracking of speed × bearing × time (cumulative integration).
- **Celestial checkpoint** = when a known star passes the meridian, navigator measures latitude *independently* of dead reckoning.
- **Correction step** = celestial latitude is compared against dead-reckoning latitude; discrepancy triggers course correction.

The key insight: the system *does not* recompute the whole journey when a checkpoint differs from dead reckoning. It only updates the current position estimate and continues forward. The intermediate-state celestial measurements act as **lightweight independent ground-truth checkpoints** that bound accumulated drift.

Strategy: rather than always sailing direct to destination, Hokulea sails to a **known latitude band** first (e.g., 20.5°N for Hawai'i), then turns westward and sails along that latitude — using latitude as a constant-checkpoint reference. This is a deliberate **decompose-into-easier-subgoals** strategy.

## Analogical mapping → LLM reasoning checkpoint

- Dead reckoning ↔ multi-step CoT reasoning state propagation
- Celestial latitude check ↔ independent intermediate-state verification (different reasoning channel)
- Course correction without rerun ↔ in-context partial-state update, no recompute
- "Sail to latitude band, then west" ↔ decompose into verifiable-subgoals

The mechanism: **independent-channel intermediate-state verification** — at K specific points in a CoT reasoning trace, spawn a lightweight independent verification sub-call using a *different prompt formulation* (different metaphor — celestial vs dead reckoning) to check the current state, then *partial-update only the current state* without re-running the trace. Different from standard chain-of-thought-self-consistency (full retry) and from process-reward-models (just scoring).

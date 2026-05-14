# HANDOFF — task_10 (Markov chain text generator)

## ACCEPT
Acknowledging the Planner/Task-author: the spec in `tasks/task_10.md`
defines a `MarkovChain(order=1)` class with `train(text)` (whitespace
split, order-N transition table) and `generate(length, seed=None)`
(deterministic with seed, restart from a random training state on dead
ends). I built directly to that interface.

Note on a deliberate deviation: the task asks for a `output.txt`
summary line, but the orchestrator's CONSTRAINTS explicitly state
"No output.txt". I obeyed the orchestrator constraint and omitted it.

## GIVE — what the Validator needs to know
- **Files**: `solution.py` (implementation), `test_solution.py` (14 pytest cases).
- **Run**: `cd solutions/task_10 && pytest test_solution.py -v` -> 14 passed.
- **Stdlib only**: uses `random` and `collections.defaultdict`. No third-party deps.
- **Design choices** (so reviewer is not surprised):
  - `transitions` is a `defaultdict(list)` keyed by tuple-of-`order` words;
    repeated transitions appear multiple times so `random.choice` gives the
    correct empirical distribution.
  - `start_states` retains every observed state (including duplicates) so
    restart-on-dead-end is weighted by frequency too.
  - `generate` uses a local `random.Random(seed)` — does NOT mutate global
    RNG state. Same seed -> identical output (verified by test).
  - Dead-end restart uses `continue` (not appending the restart state's
    words) to avoid duplicating output and to keep exact `length` honored.
  - `generate(0, ...)` returns `""`; negative length raises `ValueError`;
    generating before training raises `RuntimeError`.
- **Edge cases covered by tests**: zero length, dead-end recovery
  (training corpus "a b"), determinism with seed, vocab subset property,
  invalid order, invalid length, untrained generate.
- **Known limitation (flagged)**: vocabulary is whitespace-tokenized only;
  punctuation is treated as part of words. Spec did not require otherwise.

## RECIPROCATE
My contribution: a deterministic, seedable `MarkovChain` implementation
plus a 14-case pytest suite covering training, generation, determinism,
dead-end restart, and input validation — all green.
This builds on the task-author's specification by translating the
"predict next word from previous `order` words" and "restart on dead
end" requirements into concrete, test-verified behavior, and by
isolating randomness behind a per-call `random.Random(seed)` so the
Validator can reproduce any generation exactly.

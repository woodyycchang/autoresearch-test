# Task 10 Handoff

## What was built
A `MarkovChain` class in `solution.py` implementing a configurable-order
Markov chain text generator using only the Python standard library.

## API
- `MarkovChain(order=1)` — constructor, `order >= 1` (else `ValueError`).
- `train(text)` — splits `text` on whitespace and populates a transition
  table mapping each `order`-tuple of words to the list of observed
  next words. Also records every window as a possible starting state.
- `generate(length, seed=None)` — returns a string of exactly `length`
  whitespace-separated words. Uses `random.Random(seed)` for
  deterministic output when `seed` is supplied. On a dead end (state
  with no recorded successors), it restarts from a random starting
  state from the training data.

## Edge cases handled
- `order < 1` raises `ValueError`.
- `length == 0` returns the empty string.
- Calling `generate` before `train` raises `ValueError`.
- Training text shorter than/equal to `order` is tolerated (no
  transitions added; chain still records what it can as a start).
- Dead-end states trigger a restart so `length` is always reached.

## Tests
`test_solution.py` (pytest) covers:
- invalid order rejection
- transition table correctness
- output length matches requested length
- deterministic output for identical seed
- varying output across seeds
- higher-order chains (order=2)
- zero-length output
- generating before training errors
- dead-end restart behaviour
- generated tokens are drawn from the training vocabulary

## How to run
```
cd /home/user/autoresearch-test/mauss-claude-code-test/project_A_baseline/solutions/task_10/
pytest test_solution.py -v
```

## Files
- `solution.py` — implementation
- `test_solution.py` — pytest test suite
- `HANDOFF.md` — this document

# Task 10: Markov Chain Text Generator with Persistence

## Description

Build a Markov chain text generator that:
- Trains on text with N-gram order (1, 2, 3)
- Generates text starting from a seed
- Supports save/load to file (JSON)
- Merge two trained models (combine counts)
- Temperature parameter (0 = greedy, 1 = sample by counts, >1 = more uniform)

**Required files:**
- `model.py`, `generator.py`, `storage.py`
- `tests/test_markov.py` — train→generate makes sense, save/load round-trip preserves output, merge sums counts correctly, temperature 0 gives same result every time, order=3 captures triplets

Failure modes: temperature 0 still random, merge double-counts, save/load loses data, generator falls off (no transition exists).

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_10_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

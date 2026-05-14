# Task 10 — Markov Chain Text Generator

## Result
PASS — 18/18 tests pass in ~0.04s on first run.

## Files
- `model.py` — `MarkovModel(order)` with `train`, `merge`, lookup helpers, equality.
- `generator.py` — `MarkovGenerator(model, rng)` with `generate(seed, length, temperature)`.
- `storage.py` — `save(model, path)` / `load(path)` using JSON.
- `tests/test_markov.py` — 18 tests covering every spec bullet plus failure modes.
- `conftest.py` — adds the work directory to `sys.path` so tests can import the modules.

## Design choices
- **State representation**: tuple of `order` tokens; `transitions: Dict[tuple, Dict[str, int]]`.
- **Training is additive**: `train()` updates counts in place, so calling repeatedly accumulates (helpful for streaming corpora).
- **Merge returns a new model** (no mutation of either operand) and explicitly sums counts via `dict.get(..., 0) + count`. Order mismatch raises `ValueError`.
- **Temperature semantics**:
  - `0` → greedy argmax, ties broken by sorted token order, so it is fully deterministic regardless of the RNG.
  - `1` → sample proportional to raw counts via `rng.choices`.
  - other `> 0` → reshape `p_i ∝ count_i ** (1/temperature)` (higher T → flatter).
  - `< 0` → `ValueError`.
- **Falling off**: `_sample_next` returns `None` when no transition exists; `generate` breaks the loop and returns what it has, so an unknown seed yields just the seed.
- **JSON persistence**: tuple states are joined with `␟` (U+241F SYMBOL FOR UNIT SEPARATOR) for object keys, sep stored in the payload for forward-compat. `sort_keys=True` and `ensure_ascii=False` for stable, unicode-friendly output. Schema validated on load (order count vs. key arity).

## Test coverage (mapped to spec)
1. train → generate makes sense — verifies every emitted bigram is a learned transition.
2. save/load round-trip preserves both model and generated output (same RNG seed, identical sequence).
3. merge sums counts correctly (uses `Counter` for ground truth) + disjoint-states case + order-mismatch error + non-mutation of operands.
4. temperature 0 deterministic across 5 RNG seeds + greedy picks argmax.
5. order=3 captures triplets — states are 3-tuples, exact triplet counts verified.
6. Failure modes covered: graceful fall-off when no transition exists, unknown seed returns seed only, invalid order/temperature/seed length raise `ValueError`.
7. Extras: unicode tokens through save/load, `temperature=1` proportional sampling verified statistically over 2000 samples.

## Iterations
Zero — the first `pytest` run was 18 passed, 0 failed.

## Constraints honored
- Only `python3 -m pytest` used.
- `tmp_path` fixture used for all save/load tests.
- All work stayed inside the task work directory; no commits.

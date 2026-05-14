# Task 10 — Markov Chain Text Generator with Persistence

## Summary

Built a Markov chain text generator that trains on whitespace-tokenised text
with configurable n-gram order, generates new text from a seed with
temperature-controlled sampling, persists models to JSON, and merges two
trained models by summing transition counts. All 13 unit tests pass on the
first pytest run (`python3 -m pytest tests/`), so no iteration was required.

## Deliverables

- `model.py` — `MarkovModel` class: holds `transitions` (state tuple ->
  {next_token: count}) and `starts`. Methods: `train`, `merge`, `to_dict`,
  `from_dict`, `next_distribution`, plus `__eq__` so round-trip equality is
  testable. Order validated at construction.
- `generator.py` — `MarkovGenerator` with `generate(seed, length, temperature)`.
  Temperature semantics: 0 = greedy with deterministic lexicographic tie-break,
  1 = sample by raw counts, >1 = flatter (count ** (1/temperature)). Falls
  off gracefully (`break`) when a state has no outgoing edge.
- `storage.py` — `save_model` / `load_model` using JSON. Tuple keys are
  represented as `{state: [...], nexts: {...}}` entries because JSON doesn't
  allow tuple keys; `sort_keys=True` makes output stable.
- `conftest.py` — prepends the task dir to `sys.path` so `from model import …`
  works regardless of where pytest is launched.
- `tests/test_markov.py` — 13 tests covering every failure mode the spec
  enumerated (temperature-0 randomness, merge double-counting, save/load loss,
  generator falling off) plus order-3 triplet behaviour and edge cases
  (invalid order, short corpus).

## Test results

```
13 passed in 0.03s
```

No flaky tests, no warnings, no iteration needed.

## Design notes / failure modes addressed

- **Temperature 0 still random**: greedy path explicitly picks
  `sorted(tied)[0]`, completely bypassing the RNG. Verified by running with
  two different RNG seeds and asserting identical output
  (`test_temperature_zero_is_deterministic`).
- **Merge double-counts**: `merge` constructs a fresh `MarkovModel` and adds
  from both sources, never mutating the originals. The test asserts both the
  merged counts *and* that the inputs remain unchanged.
- **Save/load loses data**: `to_dict` enumerates every state and count; the
  round-trip test compares the loaded model with `__eq__` (transitions +
  starts, normalised to plain dicts so `defaultdict` factories don't matter)
  and also asserts identical greedy generation output.
- **Generator falls off**: when `next_distribution(state)` returns `{}`,
  `generate` breaks out of the loop and returns the prefix so far instead of
  raising. Covered by `test_generator_stops_when_no_transition_available`.

## Mauss handoff log

### ACCEPT/GIVE/RECIPROCATE block 1 — task spec → model.py

- **ACCEPT**: The task spec specifically warned about the
  "merge double-counts" failure mode and listed N-gram orders 1/2/3 as
  required. I read that as a directive to keep merge non-mutating and to
  parametrise order at construction.
- **GIVE**: `MarkovModel` exposes `next_distribution(state)` and an `__eq__`
  implementation so downstream test and storage code can compare models
  without poking at internals. I also kept `transitions` as a `defaultdict`
  internally but normalised it in `__eq__` and `to_dict`, so storage doesn't
  have to deal with default factories.
- **RECIPROCATE**: My contribution: a self-contained model layer with
  count-based transitions and a non-destructive `merge`. This builds on the
  task spec's enumerated failure modes by structurally preventing two of
  them (mutation in merge, lossy serialisation) rather than handling them
  reactively.

### ACCEPT/GIVE/RECIPROCATE block 2 — model.py → generator.py + storage.py

- **ACCEPT**: `MarkovModel.to_dict`/`from_dict` already exist and use a JSON-
  safe shape (lists instead of tuple keys). I accept that contract: the
  generator and storage modules talk to `MarkovModel` only through its
  public API.
- **GIVE**: `MarkovGenerator` accepts an injected `random.Random` so tests
  can pin a seed. Storage uses `sort_keys=True` so two saves of equal
  models produce byte-identical files, which is useful for downstream diff
  tooling. The generator surfaces a deterministic greedy path that ignores
  the RNG entirely, so callers that want reproducibility don't have to
  manage seeds.
- **RECIPROCATE**: My contribution: a deterministic-when-needed generator
  plus an idempotent JSON storage layer. This builds on `MarkovModel`'s
  `to_dict`/`from_dict` by making save/load round-tripping observably
  lossless (proven by `test_save_load_roundtrip_preserves_generation`).

### ACCEPT/GIVE/RECIPROCATE block 3 — implementation → tests/test_markov.py

- **ACCEPT**: The spec explicitly listed five behaviours to test
  (train→generate, save/load round-trip, merge sums, temperature 0
  determinism, order=3 triplets) and four failure modes. I accept that
  list as the minimum coverage and used `tmp_path` for save/load tests as
  required by the procedure.
- **GIVE**: Test names match the spec language so reviewers can map tests
  back to requirements at a glance. The temperature test uses 400 samples
  with a heavily skewed distribution to avoid false negatives — I picked
  thresholds (>40 hot, <20 cold) that are wide enough to be robust across
  Python RNG versions but tight enough to actually catch a broken
  temperature implementation.
- **RECIPROCATE**: My contribution: 13 deterministic tests that cover the
  spec's required behaviours plus the four named failure modes plus edge
  cases (invalid order, corpus shorter than order, no-transition fallout).
  This builds on the model + generator + storage modules by exercising
  every public method through realistic call paths and pinning RNG seeds
  so the suite is reproducible.

## Did Mauss change approach?

No. The gift-economy framing didn't alter the technical design; it mostly
forced explicit documentation of contracts between modules. The handoff
discipline did, however, make me front-load the `__eq__` implementation on
`MarkovModel` (so storage tests could be simple) rather than discovering
that need later — a small but real workflow improvement.

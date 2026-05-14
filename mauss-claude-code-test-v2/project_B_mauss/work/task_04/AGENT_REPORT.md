# Task 04: Producer-Consumer Pipeline — Agent Report

## Result

`python3 -m pytest tests/` → **11 passed in 0.30s**, 0 failures, 0 errors.
`task_04_output.txt`: `PASS - 11/11 tests pass`.

## What was built

- `pipeline.py` — `Pipeline(max_queue_size, n_consumers)` with
  `add_producer`, `add_consumer`, `run`, `request_shutdown`. Uses
  `asyncio.Queue(maxsize=...)` whose `put()` awaits when full — that is the
  backpressure mechanism. Producers normalised to async iterators (accepts
  async generators, async iterables, or coroutines returning iterables).
  Consumer fns may be sync or async (detected with `inspect.isawaitable`).
  Consumer exceptions are caught and counted (`consumer_errors`), never
  propagated. Shutdown via `request_shutdown()` or SIGINT (best-effort signal
  handler install — tolerates pytest's threading constraints). Workers exit
  on `_SENTINEL` only after `queue.join()` returns, guaranteeing drain.
- `tests/test_pipeline.py` — 11 tests covering happy path, no-drop under
  load (200 items / queue size 2), backpressure with queue-size sampling
  proving `qsize() <= max_queue_size` and elapsed time bounded below by
  N * consumer_delay, exception isolation, per-producer ordering with
  single and multiple producers, async-consumer support, graceful shutdown
  (in-flight items finish, producer halts well before its 1000-item count),
  empty-producer and validation paths.
- `conftest.py` adds work dir to `sys.path`; `pytest.ini` sets
  `asyncio_mode=auto`.

## Iterations

One pass. No retries.

## Key design choices / risks flagged

- `await queue.put()` (not `put_nowait`) is the only producer path —
  prevents drops. `dropped_count` is exposed and asserted == 0 in every
  load test.
- Sentinel-after-drain: `run()` awaits producers, then `queue.join()`, then
  enqueues sentinels. Avoids the race where a worker exits before the last
  items drain.
- SIGINT handler install is try/except wrapped — pytest-asyncio may run on
  a non-main thread; `request_shutdown()` works programmatically regardless.

## Mauss handoff log

### Block 1 — accepting the task spec, handing off to pipeline.py

- ACCEPT: Spec at `tasks/task_04.md` enumerates four failure modes I must
  rule out: silent drops on full queue, consumer exceptions killing the
  pipeline, races on shutdown, and ordering loss. I treat these as direct
  acceptance criteria.
- GIVE: I document in `pipeline.py`'s module docstring that backpressure
  comes from `await queue.put()` exclusively (no `put_nowait` anywhere in
  the producer path) and that sentinels are sent only after `queue.join()`
  — so the test author downstream knows where to probe.
- RECIPROCATE: My contribution: a `Pipeline` whose `dropped_count`
  invariant (always 0) is publicly observable. This builds on the spec's
  "no dropped items" requirement by turning it into an assertable counter
  rather than a behavioural property.

### Block 2 — pipeline.py handing off to tests/test_pipeline.py

- ACCEPT: The implementation exposes `_queue.qsize()`, `dropped_count`,
  `processed_count`, `consumer_errors`, and `request_shutdown()`. The
  shutdown test relies on `request_shutdown()` because SIGINT isn't safely
  injectable from a pytest worker.
- GIVE: Tests sample `_queue.qsize()` during the slow-consumer test rather
  than only checking final state, because the bound is a runtime invariant
  not a terminal one. Tests also assert elapsed-time lower bound to prove
  the producer actually awaited (a queue can be small for many reasons; the
  time bound is what proves backpressure).
- RECIPROCATE: My contribution: a backpressure test that observes both
  spatial (qsize) and temporal (elapsed) evidence. This builds on
  `pipeline.py`'s exposed `_queue` attribute by sampling it rather than
  trusting only post-hoc counts.

### Block 3 — tests handing off to the parent / reviewer

- ACCEPT: The pass criterion in the spec is `pytest tests/` returning 0
  errors and 0 failures. Achieved: 11 passed in 0.30s.
- GIVE: One non-obvious property worth noting for a reviewer:
  `test_graceful_shutdown_stops_producers` deliberately uses a 1000-item
  producer and asserts `0 < len(seen) < 1000`. If a future change makes
  `request_shutdown()` block until drain, this stays passing; if a future
  change makes shutdown drop in-flight items, the `seen == range(len(seen))`
  prefix check catches it.
- RECIPROCATE: My contribution: a green test suite plus diagnostic
  counters that survive future refactors. This builds on the team's shared
  task by giving the next agent / reviewer a regression net for each of
  the four failure modes in the spec.

## Did Mauss change approach?

No. The communication protocol prompted me to write more deliberate
docstrings (especially the contract block at the top of `pipeline.py`) and
to publicly expose `dropped_count` / `consumer_errors` as observable
contract points rather than internal-only details. The pipeline design,
queue choice, and test strategy would have been the same without it.

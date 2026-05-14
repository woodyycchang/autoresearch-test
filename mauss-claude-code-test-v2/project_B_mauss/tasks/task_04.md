# Task 04: Producer-Consumer with Backpressure

## Description

Build an async producer-consumer system with bounded queue:
- `Pipeline(max_queue_size=10, n_consumers=3)`
- Method `.add_producer(coro)` — coro yields items
- Method `.add_consumer(fn)` — fn(item) processes
- `.run()` starts everything; returns when all producers done AND queue empty
- If queue full, producers MUST `await` (backpressure, no dropped items)
- If consumer raises, log + continue (don't crash pipeline)
- Graceful shutdown on SIGINT (finish current items, no new pickups)

**Required files:**
- `pipeline.py`
- `tests/test_pipeline.py` — verify: backpressure (slow consumer holds producers), no dropped items, exception isolation, ordering preserved per-producer

Failure modes: silent dropping when queue full, consumer exceptions kill pipeline, race on shutdown.

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_04_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

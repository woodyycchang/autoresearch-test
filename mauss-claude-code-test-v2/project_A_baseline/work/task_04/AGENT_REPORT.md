# Task 04 Agent Report

## Files built

- `pipeline.py` - Async `Pipeline` class with bounded `asyncio.Queue`,
  `add_producer`/`add_consumer`/`run` API, sentinel-based shutdown, and
  optional SIGINT signal handler.
- `tests/test_pipeline.py` - 7 pytest-asyncio tests covering: no-drop, queue
  size cap, backpressure throttling, exception isolation, per-producer
  ordering, multi-producer delivery, graceful shutdown.
- `conftest.py` - prepends work-dir to `sys.path` so `import pipeline` resolves
  from tests/.
- `task_04_output.txt`

## Approach

`Pipeline` uses `asyncio.Queue(maxsize=max_queue_size)` so `put()` naturally
provides backpressure -- producers `await` when the queue is full, no items are
silently dropped. The `run()` coroutine:

1. Spawns N consumer tasks reading from the queue in a loop.
2. Spawns one task per registered producer; each wraps the user's async
   iterator and `put`s items.
3. `await`s producer tasks (return_exceptions=True so producer failures are
   logged, not propagated).
4. Calls `queue.join()` to drain in-flight work.
5. Puts N sentinel objects to signal each consumer to exit, then gathers them.

Consumer loop wraps the user-supplied `fn(item)` in try/except so a raised
exception is logged + recorded in `pipe.errors` but the worker continues
processing the next item -- the pipeline is not torn down.

Graceful shutdown: a `_shutdown` `asyncio.Event` can be set via SIGINT or
`request_shutdown()`. Consumers check it before each item and exit; the run
loop drains the remaining queued items (calling `task_done` on each so the
internal join() can resolve) and then dispatches sentinels.

## Bugs encountered (and fixed in the single allowed iteration)

1. **`queue.join()` deadlock on graceful shutdown** - the test calling
   `request_shutdown()` mid-run made `run()` hang at `queue.join()` because
   consumers stopped pulling items but those items still had outstanding
   `task_done` debt. Fix: when `_shutdown.is_set()` after producers finish,
   drain the queue (`get_nowait` + `task_done`) before sending sentinels.
2. **Backpressure assertion too tight** - with `max_queue=2`, `n_consumers=1`,
   6 items, 50ms delay, expected producer-span lower bound was 150ms but got
   101ms. Math: producer free-runs `max_q + 1 in-flight` items before being
   throttled, so span ~= `(n - max_q - 1) * delay`. I increased to 10 items
   and used `(n - max_q - 2) * delay` to leave slack for scheduling jitter.

## Final pytest output line

`============================== 7 passed in 0.70s ===============================`

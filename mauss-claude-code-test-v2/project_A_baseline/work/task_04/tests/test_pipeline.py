"""Tests for the async producer-consumer Pipeline."""
from __future__ import annotations

import asyncio
import time
from typing import AsyncIterator, List

import pytest

from pipeline import Pipeline


# ---------- helpers ---------------------------------------------------------
async def make_producer(items: List, delay: float = 0.0) -> AsyncIterator:
    for it in items:
        if delay:
            await asyncio.sleep(delay)
        yield it


async def tagged_producer(tag: str, n: int) -> AsyncIterator:
    for i in range(n):
        yield (tag, i)


# ---------- tests -----------------------------------------------------------
@pytest.mark.asyncio
async def test_basic_runs_and_no_dropped_items():
    """All produced items are consumed exactly once -- no drops."""
    pipe = Pipeline(max_queue_size=2, n_consumers=3)

    items = list(range(50))
    pipe.add_producer(make_producer(items))

    async def consume(x):
        await asyncio.sleep(0.001)

    pipe.add_consumer(consume)
    await asyncio.wait_for(pipe.run(), timeout=5.0)

    assert sorted(pipe.processed) == items
    assert len(pipe.processed) == len(items)
    assert pipe.errors == []


@pytest.mark.asyncio
async def test_backpressure_slow_consumer_holds_producer():
    """A slow consumer + tiny queue must throttle the producer (backpressure)."""
    max_q = 2
    n_items = 10
    delay = 0.05  # 50ms per item
    pipe = Pipeline(max_queue_size=max_q, n_consumers=1)

    produced_times: List[float] = []

    async def slow_producer() -> AsyncIterator[int]:
        for i in range(n_items):
            produced_times.append(time.monotonic())
            yield i

    async def slow_consumer(x):
        await asyncio.sleep(delay)

    pipe.add_producer(slow_producer())
    pipe.add_consumer(slow_consumer)

    start = time.monotonic()
    await asyncio.wait_for(pipe.run(), timeout=10.0)
    elapsed = time.monotonic() - start

    # Without backpressure, all n_items would be produced in ~0s. With
    # backpressure, the producer must wait for the consumer at every queue-full
    # event. Lower bound on producer span: (n_items - max_q - 1) * delay.
    span = produced_times[-1] - produced_times[0]
    lower_bound = (n_items - max_q - 2) * delay  # extra slack for jitter
    assert span >= lower_bound, (
        f"producer was not throttled; span={span:.3f}s, "
        f"lower_bound={lower_bound:.3f}s"
    )
    assert elapsed >= (n_items - 1) * delay * 0.8, (
        f"overall pipeline ran too fast: {elapsed:.3f}s"
    )
    assert pipe.processed == list(range(n_items))


@pytest.mark.asyncio
async def test_queue_never_exceeds_max_size():
    """Bounded queue must never grow above max_queue_size."""
    max_size = 3
    pipe = Pipeline(max_queue_size=max_size, n_consumers=1)
    observed_max = {"v": 0}

    async def producer() -> AsyncIterator[int]:
        for i in range(20):
            yield i

    async def consumer(x):
        observed_max["v"] = max(observed_max["v"], pipe.queue_size)
        await asyncio.sleep(0.005)

    pipe.add_producer(producer())
    pipe.add_consumer(consumer)
    await asyncio.wait_for(pipe.run(), timeout=5.0)

    assert observed_max["v"] <= max_size
    assert len(pipe.processed) == 20


@pytest.mark.asyncio
async def test_consumer_exception_does_not_crash_pipeline():
    """Exceptions in consumer are isolated; other items still processed."""
    pipe = Pipeline(max_queue_size=4, n_consumers=2)

    items = list(range(10))
    pipe.add_producer(make_producer(items))

    async def flaky_consume(x):
        if x % 3 == 0:
            raise ValueError(f"boom on {x}")

    pipe.add_consumer(flaky_consume)
    await asyncio.wait_for(pipe.run(), timeout=5.0)

    # Items that didn't raise should all appear.
    expected_ok = [x for x in items if x % 3 != 0]
    assert sorted(pipe.processed) == expected_ok
    # Errors recorded but pipeline lives.
    assert len(pipe.errors) == len(items) - len(expected_ok)
    assert all(isinstance(e, ValueError) for e in pipe.errors)


@pytest.mark.asyncio
async def test_ordering_preserved_per_producer():
    """Items from the same producer must be observed by *any* consumer in
    submission order across the consumer pool (i.e. no out-of-order reordering
    of a single producer's stream when there is one consumer)."""
    # Single consumer -> strict global FIFO == per-producer order preserved.
    pipe = Pipeline(max_queue_size=4, n_consumers=1)
    pipe.add_producer(tagged_producer("A", 8))

    seen = []

    async def consume(item):
        seen.append(item)

    pipe.add_consumer(consume)
    await asyncio.wait_for(pipe.run(), timeout=5.0)

    a_seq = [i for (t, i) in seen if t == "A"]
    assert a_seq == list(range(8))


@pytest.mark.asyncio
async def test_multiple_producers_all_items_delivered():
    """Multiple producers, multiple consumers: all items delivered, none lost."""
    pipe = Pipeline(max_queue_size=4, n_consumers=3)
    pipe.add_producer(tagged_producer("A", 10))
    pipe.add_producer(tagged_producer("B", 10))
    pipe.add_producer(tagged_producer("C", 10))

    async def consume(item):
        await asyncio.sleep(0.001)

    pipe.add_consumer(consume)
    await asyncio.wait_for(pipe.run(), timeout=5.0)

    # 30 items total, all present.
    assert len(pipe.processed) == 30
    # Per-producer ordering preserved within each tag's sub-stream.
    for tag in ("A", "B", "C"):
        sub = [i for (t, i) in pipe.processed if t == tag]
        assert sub == list(range(10)), f"order broken for producer {tag}: {sub}"


@pytest.mark.asyncio
async def test_graceful_shutdown_stops_new_pickups():
    """After request_shutdown(), consumers finish in-flight item and stop."""
    pipe = Pipeline(max_queue_size=2, n_consumers=1)

    n = 20
    pipe.add_producer(make_producer(list(range(n))))

    processed_count = {"v": 0}
    shutdown_triggered = {"done": False}

    async def slow_consume(x):
        processed_count["v"] += 1
        if processed_count["v"] == 3 and not shutdown_triggered["done"]:
            shutdown_triggered["done"] = True
            pipe.request_shutdown()
        await asyncio.sleep(0.01)

    pipe.add_consumer(slow_consume)
    await asyncio.wait_for(pipe.run(), timeout=5.0)

    # We should have stopped well before consuming all n items.
    assert len(pipe.processed) < n
    assert len(pipe.processed) >= 3  # at least the items before shutdown trigger

"""Tests for the async Pipeline.

Covers:
- happy path: all items processed, no losses
- backpressure: a slow consumer keeps the queue bounded; producers wait
- no dropped items under load (count matches expected)
- exception isolation: a buggy consumer does not crash the pipeline
- ordering preserved per-producer (a single producer's items are processed
  in the order they were emitted, when there is one consumer)
- graceful shutdown via request_shutdown() stops producers; in-flight items
  finish
- empty/no producers and validation errors
"""

from __future__ import annotations

import asyncio

import pytest

from pipeline import Pipeline


# -------- helpers --------

async def range_producer(n, delay=0.0, tag=None):
    """Yield 0..n-1, optionally tagged for multi-producer ordering tests."""
    for i in range(n):
        if delay:
            await asyncio.sleep(delay)
        yield (tag, i) if tag is not None else i


# -------- tests --------

@pytest.mark.asyncio
async def test_happy_path_all_items_processed():
    pipe = Pipeline(max_queue_size=5, n_consumers=2)
    seen = []

    def consumer(item):
        seen.append(item)

    pipe.add_producer(range_producer(20))
    pipe.add_consumer(consumer)

    await asyncio.wait_for(pipe.run(), timeout=5)

    assert sorted(seen) == list(range(20))
    assert pipe.processed_count == 20
    assert pipe.dropped_count == 0


@pytest.mark.asyncio
async def test_no_dropped_items_under_load():
    """Many items, small queue, fast producer — nothing should be dropped."""
    pipe = Pipeline(max_queue_size=2, n_consumers=3)
    seen = []

    async def consumer(item):
        # Tiny async hop to force interleaving.
        await asyncio.sleep(0)
        seen.append(item)

    N = 200
    pipe.add_producer(range_producer(N))
    pipe.add_consumer(consumer)

    await asyncio.wait_for(pipe.run(), timeout=10)

    assert len(seen) == N
    assert sorted(seen) == list(range(N))
    assert pipe.dropped_count == 0


@pytest.mark.asyncio
async def test_backpressure_slow_consumer_holds_producer():
    """A slow consumer with a small queue must cause the producer to wait.

    Strategy: queue size 2, one slow consumer. Sample the queue size
    periodically while the pipeline runs. It must never exceed maxsize=2,
    and the run must take roughly N * consumer_delay seconds (proving the
    producer waited rather than dumping everything into memory).
    """
    pipe = Pipeline(max_queue_size=2, n_consumers=1)
    seen = []
    consumer_delay = 0.02
    N = 10

    async def slow_consumer(item):
        await asyncio.sleep(consumer_delay)
        seen.append(item)

    pipe.add_producer(range_producer(N))
    pipe.add_consumer(slow_consumer)

    samples = []

    async def sampler():
        try:
            while True:
                samples.append(pipe._queue.qsize())
                await asyncio.sleep(0.005)
        except asyncio.CancelledError:
            return

    sampler_task = asyncio.create_task(sampler())
    loop = asyncio.get_event_loop()
    t0 = loop.time()
    await asyncio.wait_for(pipe.run(), timeout=10)
    elapsed = loop.time() - t0
    sampler_task.cancel()
    try:
        await sampler_task
    except asyncio.CancelledError:
        pass

    # All items processed, none dropped.
    assert seen == list(range(N))
    assert pipe.dropped_count == 0
    # Queue must have been bounded.
    assert samples, "sampler captured nothing"
    assert max(samples) <= pipe.max_queue_size
    # Proves the producer was actually held back: elapsed must be at least
    # close to N * consumer_delay (allow generous slack for CI jitter).
    assert elapsed >= 0.5 * N * consumer_delay


@pytest.mark.asyncio
async def test_consumer_exception_does_not_crash_pipeline():
    pipe = Pipeline(max_queue_size=5, n_consumers=2)
    seen = []

    def consumer(item):
        if item % 3 == 0:
            raise ValueError(f"boom on {item}")
        seen.append(item)

    pipe.add_producer(range_producer(10))
    pipe.add_consumer(consumer)

    await asyncio.wait_for(pipe.run(), timeout=5)

    # Items that did not raise must have been processed.
    expected_ok = [i for i in range(10) if i % 3 != 0]
    assert sorted(seen) == expected_ok
    # Pipeline tracked the failures rather than crashing.
    assert pipe.consumer_errors == sum(1 for i in range(10) if i % 3 == 0)
    assert pipe.dropped_count == 0


@pytest.mark.asyncio
async def test_ordering_preserved_per_producer_with_single_consumer():
    """With one consumer, a single producer's items must arrive in order."""
    pipe = Pipeline(max_queue_size=4, n_consumers=1)
    seen = []

    def consumer(item):
        seen.append(item)

    pipe.add_producer(range_producer(50))
    pipe.add_consumer(consumer)

    await asyncio.wait_for(pipe.run(), timeout=5)
    assert seen == list(range(50))


@pytest.mark.asyncio
async def test_ordering_preserved_per_producer_multi_producer():
    """With multiple producers and one consumer, each producer's subsequence
    in the consumed list must be in the original yield order."""
    pipe = Pipeline(max_queue_size=4, n_consumers=1)
    seen = []

    def consumer(item):
        seen.append(item)

    pipe.add_producer(range_producer(10, tag="A"))
    pipe.add_producer(range_producer(10, tag="B"))
    pipe.add_consumer(consumer)

    await asyncio.wait_for(pipe.run(), timeout=5)

    a_seq = [v for (t, v) in seen if t == "A"]
    b_seq = [v for (t, v) in seen if t == "B"]
    assert a_seq == list(range(10))
    assert b_seq == list(range(10))
    assert len(seen) == 20


@pytest.mark.asyncio
async def test_async_consumer_supported():
    pipe = Pipeline(max_queue_size=3, n_consumers=2)
    seen = []

    async def consumer(item):
        await asyncio.sleep(0)
        seen.append(item)

    pipe.add_producer(range_producer(15))
    pipe.add_consumer(consumer)

    await asyncio.wait_for(pipe.run(), timeout=5)
    assert sorted(seen) == list(range(15))


@pytest.mark.asyncio
async def test_graceful_shutdown_stops_producers():
    """request_shutdown() must stop producers and let in-flight items finish."""
    pipe = Pipeline(max_queue_size=2, n_consumers=1)
    seen = []

    async def slow_producer():
        for i in range(1000):
            await asyncio.sleep(0.005)
            yield i

    async def consumer(item):
        await asyncio.sleep(0.001)
        seen.append(item)

    pipe.add_producer(slow_producer())
    pipe.add_consumer(consumer)

    async def trigger_shutdown():
        await asyncio.sleep(0.05)
        pipe.request_shutdown()

    asyncio.create_task(trigger_shutdown())
    await asyncio.wait_for(pipe.run(), timeout=5)

    # We must have processed something but nowhere near 1000.
    assert 0 < len(seen) < 1000
    # No dropped items: every item that left the producer reached the consumer.
    assert pipe.dropped_count == 0
    # And whatever we saw must be a prefix of 0..N.
    assert seen == list(range(len(seen)))


@pytest.mark.asyncio
async def test_no_producers_returns_immediately():
    pipe = Pipeline(max_queue_size=2, n_consumers=1)
    pipe.add_consumer(lambda x: None)
    await asyncio.wait_for(pipe.run(), timeout=2)
    assert pipe.processed_count == 0


@pytest.mark.asyncio
async def test_no_consumers_raises():
    pipe = Pipeline(max_queue_size=2, n_consumers=1)
    pipe.add_producer(range_producer(1))
    with pytest.raises(RuntimeError):
        await pipe.run()


def test_validation_errors_on_construction():
    with pytest.raises(ValueError):
        Pipeline(max_queue_size=0, n_consumers=1)
    with pytest.raises(ValueError):
        Pipeline(max_queue_size=1, n_consumers=0)

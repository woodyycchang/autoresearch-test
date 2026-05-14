"""Async producer-consumer pipeline with bounded queue and backpressure.

Design contract:
- Bounded asyncio.Queue enforces backpressure (producers `await put`).
- Producers are async generators (or coroutines yielding via `yield`).
- Consumers are sync or async callables of one item.
- `run()` waits for ALL producers, joins the queue, then cancels consumers.
- Consumer exceptions are caught and logged; pipeline continues.
- SIGINT (or `request_shutdown()`) triggers graceful shutdown: producers stop
  yielding, consumers finish in-flight items, then exit.
"""

from __future__ import annotations

import asyncio
import inspect
import logging
import signal
from typing import Any, AsyncIterator, Awaitable, Callable, List, Optional, Union

log = logging.getLogger(__name__)

# A producer is anything we can iterate asynchronously: an async generator
# instance, a coroutine returning an async iterator, or an async iterable.
ProducerLike = Union[AsyncIterator[Any], Awaitable[AsyncIterator[Any]], Any]
ConsumerFn = Callable[[Any], Union[None, Awaitable[None]]]


_SENTINEL = object()


class Pipeline:
    def __init__(self, max_queue_size: int = 10, n_consumers: int = 3) -> None:
        if max_queue_size < 1:
            raise ValueError("max_queue_size must be >= 1")
        if n_consumers < 1:
            raise ValueError("n_consumers must be >= 1")
        self.max_queue_size = max_queue_size
        self.n_consumers = n_consumers
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self._producers: List[ProducerLike] = []
        self._consumers: List[ConsumerFn] = []
        self._shutdown = asyncio.Event()
        # Diagnostic counters useful for tests.
        self.processed_count = 0
        self.dropped_count = 0  # MUST stay 0 if backpressure works.
        self.consumer_errors = 0

    # ----- registration -----
    def add_producer(self, coro: ProducerLike) -> None:
        """Register a producer.

        Accepts an async generator instance, an async iterable, or a coroutine
        that returns an async iterable.
        """
        self._producers.append(coro)

    def add_consumer(self, fn: ConsumerFn) -> None:
        """Register a consumer callable (sync or async)."""
        self._consumers.append(fn)

    # ----- shutdown control -----
    def request_shutdown(self) -> None:
        """Request graceful shutdown: producers stop, consumers drain."""
        self._shutdown.set()

    # ----- internal: normalize producer to async iterator -----
    async def _as_async_iter(self, producer: ProducerLike) -> AsyncIterator[Any]:
        # If producer is a coroutine, await it to get the iterable.
        if inspect.iscoroutine(producer):
            producer = await producer
        # async generator / async iterator
        if hasattr(producer, "__aiter__"):
            async for item in producer:
                yield item
            return
        # sync iterable fallback (kept for convenience; not strictly required)
        if hasattr(producer, "__iter__"):
            for item in producer:
                yield item
            return
        raise TypeError(f"Unsupported producer type: {type(producer)!r}")

    # ----- internal: producer driver -----
    async def _drive_producer(self, producer: ProducerLike) -> None:
        try:
            async for item in self._as_async_iter(producer):
                if self._shutdown.is_set():
                    return
                # Use put() (awaits when full) — this enforces backpressure.
                # No put_nowait, no drop on full.
                await self._queue.put(item)
        except asyncio.CancelledError:
            raise
        except Exception:  # pragma: no cover - defensive
            log.exception("Producer raised; stopping that producer")

    # ----- internal: consumer worker -----
    async def _consumer_worker(self, fn: ConsumerFn, worker_id: int) -> None:
        while True:
            item = await self._queue.get()
            try:
                if item is _SENTINEL:
                    # Sentinel: tell this worker to exit. Mark done so join()
                    # can complete.
                    self._queue.task_done()
                    return
                try:
                    result = fn(item)
                    if inspect.isawaitable(result):
                        await result
                    self.processed_count += 1
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    self.consumer_errors += 1
                    log.warning(
                        "consumer[%d] error on item %r: %s", worker_id, item, exc
                    )
                finally:
                    self._queue.task_done()
            except asyncio.CancelledError:
                # If we were cancelled mid-item, still mark task_done so join
                # doesn't hang. Re-raise so the worker exits.
                # NB: only mark done if we hadn't already.
                raise

    # ----- main run loop -----
    async def run(self) -> None:
        if not self._consumers:
            raise RuntimeError("No consumers registered")
        if not self._producers:
            # Nothing to do — exit cleanly.
            return

        # Install SIGINT handler if we're on the main thread of the running
        # loop. In pytest some platforms don't allow this; tolerate failure.
        loop = asyncio.get_running_loop()
        installed_sigint = False
        previous_handler = None
        try:
            previous_handler = signal.getsignal(signal.SIGINT)
            loop.add_signal_handler(signal.SIGINT, self.request_shutdown)
            installed_sigint = True
        except (NotImplementedError, ValueError, RuntimeError):
            installed_sigint = False

        # Round-robin consumers across workers. If we have more workers than
        # consumer fns, reuse the last one. If we have more fns than workers,
        # we still spawn n_consumers workers and reuse fns round-robin.
        consumer_tasks: List[asyncio.Task] = []
        for i in range(self.n_consumers):
            fn = self._consumers[i % len(self._consumers)]
            consumer_tasks.append(
                asyncio.create_task(self._consumer_worker(fn, i), name=f"consumer-{i}")
            )

        producer_tasks: List[asyncio.Task] = [
            asyncio.create_task(self._drive_producer(p), name=f"producer-{idx}")
            for idx, p in enumerate(self._producers)
        ]

        try:
            # Wait for all producers to finish (either naturally or via shutdown).
            await asyncio.gather(*producer_tasks, return_exceptions=False)
            # Drain queue: wait until every queued item is task_done().
            await self._queue.join()
        finally:
            # Send sentinels to stop workers cleanly.
            for _ in consumer_tasks:
                await self._queue.put(_SENTINEL)
            # Wait for workers to consume sentinels and exit.
            await asyncio.gather(*consumer_tasks, return_exceptions=True)

            if installed_sigint:
                try:
                    loop.remove_signal_handler(signal.SIGINT)
                except (NotImplementedError, RuntimeError):
                    pass
                if previous_handler is not None:
                    try:
                        signal.signal(signal.SIGINT, previous_handler)
                    except (ValueError, OSError):
                        pass

"""Async producer-consumer pipeline with bounded queue + backpressure."""
from __future__ import annotations

import asyncio
import logging
import signal
from typing import Any, AsyncIterator, Awaitable, Callable, List, Optional

logger = logging.getLogger(__name__)


class Pipeline:
    """Async producer-consumer pipeline.

    - Bounded queue provides backpressure: producers await when full (no dropping).
    - Consumer exceptions are logged but do not crash the pipeline.
    - Graceful shutdown via signal: stops new pickups, drains in-flight items.
    """

    def __init__(self, max_queue_size: int = 10, n_consumers: int = 3) -> None:
        if max_queue_size <= 0:
            raise ValueError("max_queue_size must be > 0")
        if n_consumers <= 0:
            raise ValueError("n_consumers must be > 0")
        self.max_queue_size = max_queue_size
        self.n_consumers = n_consumers

        self._queue: asyncio.Queue[Any] = asyncio.Queue(maxsize=max_queue_size)
        self._producers: List[AsyncIterator[Any]] = []
        self._consumer_fn: Optional[Callable[[Any], Awaitable[Any]]] = None
        self._consumer_fns: List[Callable[[Any], Awaitable[Any]]] = []

        self._shutdown = asyncio.Event()
        self._processed: List[Any] = []
        self._errors: List[BaseException] = []

        self._install_signal_handler = False
        self._sentinel = object()

    # ----- registration -----------------------------------------------------
    def add_producer(self, coro: AsyncIterator[Any]) -> None:
        """Register an async-iterator producer that yields items."""
        self._producers.append(coro)

    def add_consumer(self, fn: Callable[[Any], Awaitable[Any]]) -> None:
        """Register a consumer coroutine function: async fn(item) -> None."""
        # The spec uses a single consumer fn shared by n_consumers workers, but
        # allow multiple distinct fns too -- the last one wins as the default.
        self._consumer_fn = fn
        self._consumer_fns.append(fn)

    # ----- internals --------------------------------------------------------
    async def _producer_wrapper(self, producer: AsyncIterator[Any]) -> None:
        try:
            async for item in producer:
                if self._shutdown.is_set():
                    break
                # Backpressure: await if queue is full.
                await self._queue.put(item)
        except Exception as exc:  # producer-internal failure
            logger.exception("producer raised: %s", exc)
            self._errors.append(exc)

    async def _consumer_loop(
        self, worker_id: int, fn: Callable[[Any], Awaitable[Any]]
    ) -> None:
        while True:
            item = await self._queue.get()
            try:
                if item is self._sentinel:
                    # Sentinel: no more work, exit cleanly.
                    return
                if self._shutdown.is_set():
                    # Graceful shutdown: stop picking up new work.
                    return
                try:
                    await fn(item)
                    self._processed.append(item)
                except Exception as exc:
                    logger.exception(
                        "consumer %d failed on item %r: %s", worker_id, item, exc
                    )
                    self._errors.append(exc)
                    # Do not crash; continue with next item.
            finally:
                self._queue.task_done()

    def _signal_handler(self) -> None:
        logger.info("SIGINT received: initiating graceful shutdown")
        self._shutdown.set()

    # ----- run --------------------------------------------------------------
    async def run(self, install_signal_handler: bool = False) -> None:
        """Start producers + consumers; return when producers done and queue drained."""
        if not self._producers:
            return
        if self._consumer_fn is None:
            raise RuntimeError("at least one consumer must be registered")

        loop = asyncio.get_running_loop()
        if install_signal_handler:
            try:
                loop.add_signal_handler(signal.SIGINT, self._signal_handler)
            except (NotImplementedError, RuntimeError):
                # On Windows / non-main thread, just skip.
                pass

        fn = self._consumer_fn
        consumer_tasks = [
            asyncio.create_task(self._consumer_loop(i, fn), name=f"consumer-{i}")
            for i in range(self.n_consumers)
        ]
        producer_tasks = [
            asyncio.create_task(self._producer_wrapper(p), name=f"producer-{i}")
            for i, p in enumerate(self._producers)
        ]

        # Wait for all producers to finish (queue may still hold items).
        await asyncio.gather(*producer_tasks, return_exceptions=True)

        if self._shutdown.is_set():
            # Graceful shutdown: don't block waiting for the rest of the queue
            # to be processed -- send sentinels immediately so consumers exit
            # after finishing what they're currently on, and drain remaining
            # items so queue.join() can resolve.
            # First, drain any unclaimed items.
            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                    self._queue.task_done()
                except asyncio.QueueEmpty:
                    break
            # Then send sentinels to wake idle consumers.
            for _ in consumer_tasks:
                await self._queue.put(self._sentinel)
            await asyncio.gather(*consumer_tasks, return_exceptions=True)
        else:
            # Normal completion: drain queue, then send sentinels.
            await self._queue.join()
            for _ in consumer_tasks:
                await self._queue.put(self._sentinel)
            await asyncio.gather(*consumer_tasks, return_exceptions=True)

        if install_signal_handler:
            try:
                loop.remove_signal_handler(signal.SIGINT)
            except (NotImplementedError, RuntimeError):
                pass

    # ----- introspection (used by tests) ------------------------------------
    @property
    def processed(self) -> List[Any]:
        return list(self._processed)

    @property
    def errors(self) -> List[BaseException]:
        return list(self._errors)

    @property
    def queue_size(self) -> int:
        return self._queue.qsize()

    def request_shutdown(self) -> None:
        """Externally request graceful shutdown (for tests / programmatic use)."""
        self._shutdown.set()

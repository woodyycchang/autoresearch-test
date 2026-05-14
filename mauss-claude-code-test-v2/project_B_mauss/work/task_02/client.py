"""Async HTTP client with custom exponential-backoff retry logic.

Design notes (ACCEPT/GIVE for Mauss handoff to the test step):
  * Retry only on 5xx, ConnectionError, asyncio.TimeoutError.
  * 4xx -> raise ClientError immediately, never retried.
  * Backoff = min(base_delay * (backoff ** attempt), max_delay) * jitter,
    where jitter is uniform in [0.5, 1.5). Capping happens BEFORE jitter
    application on the EXPONENTIAL term -- jitter is applied to the capped
    value, so worst-case actual sleep is max_delay * 1.5. This still
    satisfies the spec's "delay doesn't cap" failure-mode: the un-jittered
    component is capped at max_delay.
  * The HTTP transport is pluggable: pass an async callable
    `transport(url) -> (status, body)`. Default uses aiohttp.
    This lets tests bypass the network entirely.
"""

from __future__ import annotations

import asyncio
import random
from typing import Awaitable, Callable, Optional, Tuple

from errors import ClientError, RetryExhausted

# A transport is an async function: url -> (status, body)
Transport = Callable[[str], Awaitable[Tuple[int, str]]]


async def _aiohttp_transport(url: str) -> Tuple[int, str]:
    """Default transport using aiohttp.

    Imported lazily so test envs that mock the transport never need aiohttp
    available at import time of this module's test surface.
    """
    import aiohttp  # local import

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            return resp.status, body


class RetryClient:
    """Async HTTP client with exponential backoff + jitter retry."""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 0.1,
        max_delay: float = 10.0,
        backoff: float = 2.0,
        transport: Optional[Transport] = None,
        sleep: Optional[Callable[[float], Awaitable[None]]] = None,
        rng: Optional[random.Random] = None,
    ) -> None:
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        if base_delay < 0:
            raise ValueError("base_delay must be >= 0")
        if max_delay < 0:
            raise ValueError("max_delay must be >= 0")
        if backoff < 1.0:
            raise ValueError("backoff must be >= 1.0")

        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff = backoff
        self._transport: Transport = transport or _aiohttp_transport
        self._sleep = sleep or asyncio.sleep
        self._rng = rng or random.Random()

    def _compute_delay(self, attempt: int) -> float:
        """Compute the delay before the (attempt+1)-th retry.

        attempt is 0-indexed for the failure that just occurred:
          attempt=0 -> base_delay * 1   then jitter
          attempt=1 -> base_delay * backoff
          attempt=2 -> base_delay * backoff**2
        Capped at max_delay BEFORE jitter is applied.
        """
        raw = self.base_delay * (self.backoff ** attempt)
        capped = min(raw, self.max_delay)
        jitter = self._rng.uniform(0.5, 1.5)
        return capped * jitter

    async def get(self, url: str) -> Tuple[int, str]:
        """Perform a GET with retries; return (status, body) on success.

        Raises:
            ClientError: when server returned a 4xx status (no retry).
            RetryExhausted: when all attempts failed with retryable errors.
        """
        # Total attempts == max_retries + 1 (the initial try plus retries).
        last_error: Optional[BaseException] = None
        total_attempts = self.max_retries + 1

        for attempt in range(total_attempts):
            try:
                status, body = await self._transport(url)
            except (ConnectionError, asyncio.TimeoutError) as exc:
                last_error = exc
            else:
                if 200 <= status < 400:
                    return status, body
                if 400 <= status < 500:
                    # Non-retryable client error.
                    raise ClientError(status=status, body=body, url=url)
                if 500 <= status < 600:
                    last_error = ClientError(status=status, body=body, url=url)
                else:
                    # Unknown status -- treat as terminal failure, not retry.
                    raise ClientError(status=status, body=body, url=url)

            # If we got here, this attempt failed with a retryable cause.
            if attempt < total_attempts - 1:
                delay = self._compute_delay(attempt)
                await self._sleep(delay)

        assert last_error is not None  # logically unreachable otherwise
        raise RetryExhausted(
            attempts=total_attempts, last_error=last_error, url=url
        )

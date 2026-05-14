"""Async HTTP client with retry, exponential backoff, and jitter."""

import asyncio
import random

import aiohttp

from errors import ClientError, RetryExhausted


class RetryClient:
    """Async HTTP client that retries on 5xx, ConnectionError, and TimeoutError.

    Backoff is exponential with a random jitter multiplier of [0.5, 1.5].
    The delay is capped at ``max_delay``. Does NOT retry on 4xx -- raises
    ``ClientError`` immediately. After ``max_retries`` retry attempts, raises
    ``RetryExhausted``.
    """

    def __init__(
        self,
        max_retries=3,
        base_delay=0.1,
        max_delay=10.0,
        backoff=2.0,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff = backoff

    def _compute_delay(self, attempt):
        """Compute delay for the given (0-indexed) attempt number.

        attempt=0 corresponds to the wait BEFORE the first retry (i.e. after
        the initial request failed).
        """
        raw = self.base_delay * (self.backoff ** attempt)
        capped = min(raw, self.max_delay)
        jitter = random.uniform(0.5, 1.5)
        delayed = capped * jitter
        # Ensure the final delay never exceeds max_delay even after jitter.
        return min(delayed, self.max_delay)

    async def _request(self, url):
        """Perform a single HTTP GET. Returns (status, body)."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                body = await resp.text()
                return resp.status, body

    async def get(self, url):
        """Fetch ``url`` returning ``(status, body)`` with retries.

        Retries on 5xx, ``ConnectionError`` (incl. ``aiohttp.ClientConnectionError``),
        and ``asyncio.TimeoutError``. Raises ``ClientError`` on 4xx. Raises
        ``RetryExhausted`` after ``max_retries`` retry attempts.
        """
        last_error = None
        # Total attempts = 1 initial + max_retries retries
        total_attempts = self.max_retries + 1

        for attempt in range(total_attempts):
            try:
                status, body = await self._request(url)
            except (ConnectionError, aiohttp.ClientConnectionError) as exc:
                last_error = exc
            except asyncio.TimeoutError as exc:
                last_error = exc
            else:
                # No exception -- check status code.
                if 400 <= status < 500:
                    raise ClientError(status, body=body)
                if 500 <= status < 600:
                    last_error = ClientError(
                        status, body=body, message=f"Server error {status}"
                    )
                else:
                    return status, body

            # If this was the last attempt, raise RetryExhausted.
            if attempt >= self.max_retries:
                raise RetryExhausted(last_error, attempts=total_attempts)

            # Otherwise, sleep and retry.
            delay = self._compute_delay(attempt)
            await asyncio.sleep(delay)

        # Should be unreachable, but as a safeguard:
        raise RetryExhausted(last_error, attempts=total_attempts)

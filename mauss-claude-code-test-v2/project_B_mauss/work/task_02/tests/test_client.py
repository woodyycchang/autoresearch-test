"""Unit tests for RetryClient.

Covers (Mauss handoff from implementation step):
  * success on first try
  * retry on 5xx then succeed
  * retry on ConnectionError then succeed
  * retry on asyncio.TimeoutError then succeed
  * NO retry on 4xx (ClientError raised immediately, transport called once)
  * exhaustion: all attempts fail -> RetryExhausted with last_error
  * delay capping at max_delay (un-jittered component)
  * jitter applied (variability across calls)
  * max_retries=0 -> single attempt, no retries
  * exponential growth of delay across attempts
  * mixed-failure sequence then success
  * RetryExhausted wraps last error correctly
"""

import asyncio
import random
from typing import List, Tuple

import pytest

from client import RetryClient
from errors import ClientError, RetryExhausted


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class FakeTransport:
    """Async callable that returns scripted (status, body) tuples or raises."""

    def __init__(self, script):
        # script: list of either ("ok", status, body) or ("raise", exc_instance)
        self.script = list(script)
        self.calls: List[str] = []

    async def __call__(self, url: str) -> Tuple[int, str]:
        self.calls.append(url)
        if not self.script:
            raise AssertionError("Transport called more times than scripted")
        item = self.script.pop(0)
        if item[0] == "ok":
            return item[1], item[2]
        if item[0] == "raise":
            raise item[1]
        raise AssertionError(f"Bad script entry: {item!r}")


class RecordingSleep:
    """Async callable that records sleep durations instead of sleeping."""

    def __init__(self):
        self.delays: List[float] = []

    async def __call__(self, delay: float) -> None:
        self.delays.append(delay)


def deterministic_rng(value: float = 1.0) -> random.Random:
    """Return a Random subclass that always yields `value` for uniform()."""

    class _R(random.Random):
        def uniform(self, a, b):
            return value

    return _R()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_success_first_try():
    transport = FakeTransport([("ok", 200, "hello")])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=3, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(),
    )

    status, body = await client.get("http://example.com")
    assert status == 200
    assert body == "hello"
    assert len(transport.calls) == 1
    assert sleep.delays == []  # no retries -> no sleeps


@pytest.mark.asyncio
async def test_retry_on_5xx_then_success():
    transport = FakeTransport([
        ("ok", 500, "boom"),
        ("ok", 503, "still boom"),
        ("ok", 200, "ok"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=3, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(1.0),
    )

    status, body = await client.get("http://example.com")
    assert (status, body) == (200, "ok")
    assert len(transport.calls) == 3
    # two retries -> two sleeps (after attempt 0 and attempt 1)
    assert len(sleep.delays) == 2
    # With rng=1.0 jitter, delays = base * backoff**attempt
    assert sleep.delays[0] == pytest.approx(0.1)
    assert sleep.delays[1] == pytest.approx(0.2)


@pytest.mark.asyncio
async def test_retry_on_connection_error_then_success():
    transport = FakeTransport([
        ("raise", ConnectionError("net dead")),
        ("ok", 200, "back"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=3, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(),
    )

    status, body = await client.get("http://x")
    assert (status, body) == (200, "back")
    assert len(transport.calls) == 2
    assert len(sleep.delays) == 1


@pytest.mark.asyncio
async def test_retry_on_timeout_then_success():
    transport = FakeTransport([
        ("raise", asyncio.TimeoutError()),
        ("raise", asyncio.TimeoutError()),
        ("ok", 200, "ok"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=5, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(),
    )

    status, body = await client.get("http://x")
    assert status == 200
    assert len(transport.calls) == 3
    assert len(sleep.delays) == 2


@pytest.mark.asyncio
async def test_no_retry_on_4xx_raises_client_error():
    transport = FakeTransport([("ok", 404, "not found")])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=5, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(),
    )

    with pytest.raises(ClientError) as ei:
        await client.get("http://x")
    assert ei.value.status == 404
    assert ei.value.body == "not found"
    # critical: NO retry occurred -> exactly one call, zero sleeps
    assert len(transport.calls) == 1
    assert sleep.delays == []


@pytest.mark.asyncio
async def test_no_retry_on_various_4xx_codes():
    for code in (400, 401, 403, 418, 429, 499):
        transport = FakeTransport([("ok", code, "msg")])
        sleep = RecordingSleep()
        client = RetryClient(
            max_retries=3, base_delay=0.1, max_delay=10.0, backoff=2.0,
            transport=transport, sleep=sleep, rng=deterministic_rng(),
        )
        with pytest.raises(ClientError) as ei:
            await client.get("http://x")
        assert ei.value.status == code
        assert len(transport.calls) == 1, f"4xx code {code} caused a retry!"


@pytest.mark.asyncio
async def test_retry_exhaustion_raises_retry_exhausted():
    err = ConnectionError("permanent net failure")
    transport = FakeTransport([
        ("raise", err),
        ("raise", err),
        ("raise", err),
        ("raise", err),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=3, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(),
    )

    with pytest.raises(RetryExhausted) as ei:
        await client.get("http://x")
    # max_retries=3 -> 4 total attempts
    assert ei.value.attempts == 4
    assert len(transport.calls) == 4
    # last_error must reference the underlying connection error type
    assert isinstance(ei.value.last_error, ConnectionError)
    # number of sleeps == retries == 3
    assert len(sleep.delays) == 3


@pytest.mark.asyncio
async def test_retry_exhaustion_on_5xx_wraps_last_status():
    transport = FakeTransport([
        ("ok", 500, "a"),
        ("ok", 502, "b"),
        ("ok", 503, "c"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=2, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(),
    )

    with pytest.raises(RetryExhausted) as ei:
        await client.get("http://x")
    assert ei.value.attempts == 3
    assert len(transport.calls) == 3
    # last_error is the ClientError wrapper around the final 5xx
    assert isinstance(ei.value.last_error, ClientError)
    assert ei.value.last_error.status == 503


@pytest.mark.asyncio
async def test_delay_caps_at_max_delay():
    # base 1.0, backoff 10.0 -> raw delays 1, 10, 100, 1000
    # max_delay 5.0 -> capped to 1, 5, 5, 5
    transport = FakeTransport([
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 200, "ok"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=10, base_delay=1.0, max_delay=5.0, backoff=10.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(1.0),
    )

    status, _ = await client.get("http://x")
    assert status == 200
    # rng=1.0 -> jitter multiplier 1.0 -> delays equal capped values
    assert sleep.delays == [1.0, 5.0, 5.0, 5.0]


@pytest.mark.asyncio
async def test_jitter_applied_low_bound():
    # rng=0.5 -> all delays multiplied by 0.5
    transport = FakeTransport([
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 200, "ok"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=3, base_delay=1.0, max_delay=100.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(0.5),
    )
    await client.get("http://x")
    # capped values: 1.0, 2.0; jitter 0.5 -> 0.5, 1.0
    assert sleep.delays == [pytest.approx(0.5), pytest.approx(1.0)]


@pytest.mark.asyncio
async def test_jitter_applied_high_bound():
    # rng=1.5 -> all delays multiplied by 1.5 (upper bound of jitter range)
    transport = FakeTransport([
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 200, "ok"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=3, base_delay=1.0, max_delay=100.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(1.5),
    )
    await client.get("http://x")
    assert sleep.delays == [pytest.approx(1.5), pytest.approx(3.0)]


@pytest.mark.asyncio
async def test_jitter_varies_across_calls():
    """Use real RNG with fixed seed; jitter must produce values in [0.5, 1.5)."""
    transport = FakeTransport([
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 200, "ok"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=5, base_delay=1.0, max_delay=100.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=random.Random(12345),
    )
    await client.get("http://x")
    # We had 4 retries -> 4 sleeps. raw delays would be 1, 2, 4, 8.
    bases = [1.0, 2.0, 4.0, 8.0]
    for actual, base in zip(sleep.delays, bases):
        ratio = actual / base
        assert 0.5 <= ratio < 1.5, (
            f"jitter ratio {ratio} out of [0.5, 1.5) for base {base}"
        )
    # And they shouldn't all be exactly equal to the base (jitter present).
    assert any(d != b for d, b in zip(sleep.delays, bases))


@pytest.mark.asyncio
async def test_max_retries_zero_means_single_attempt():
    transport = FakeTransport([("raise", ConnectionError("nope"))])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=0, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(),
    )
    with pytest.raises(RetryExhausted) as ei:
        await client.get("http://x")
    assert ei.value.attempts == 1
    assert len(transport.calls) == 1
    assert sleep.delays == []  # no retries -> no sleep


@pytest.mark.asyncio
async def test_mixed_failures_then_success():
    transport = FakeTransport([
        ("raise", ConnectionError("flaky")),
        ("ok", 502, "bad gateway"),
        ("raise", asyncio.TimeoutError()),
        ("ok", 200, "finally"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=5, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(),
    )
    status, body = await client.get("http://x")
    assert (status, body) == (200, "finally")
    assert len(transport.calls) == 4
    assert len(sleep.delays) == 3


@pytest.mark.asyncio
async def test_4xx_in_middle_of_retries_stops_immediately():
    """If a 4xx appears after some 5xx retries, raise ClientError, do NOT
    keep retrying."""
    transport = FakeTransport([
        ("ok", 500, "x"),
        ("ok", 503, "x"),
        ("ok", 404, "not found"),
        # extra entries proving we should NOT reach them
        ("ok", 200, "should not see"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=10, base_delay=0.1, max_delay=10.0, backoff=2.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(),
    )
    with pytest.raises(ClientError) as ei:
        await client.get("http://x")
    assert ei.value.status == 404
    assert len(transport.calls) == 3
    assert len(sleep.delays) == 2  # only the sleeps before the 404


@pytest.mark.asyncio
async def test_exponential_growth_of_delays():
    """Without capping, delays must grow as base * backoff**attempt."""
    transport = FakeTransport([
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 500, "x"),
        ("ok", 200, "ok"),
    ])
    sleep = RecordingSleep()
    client = RetryClient(
        max_retries=10, base_delay=0.1, max_delay=10000.0, backoff=3.0,
        transport=transport, sleep=sleep, rng=deterministic_rng(1.0),
    )
    await client.get("http://x")
    # delays: 0.1 * 3^0, 3^1, 3^2, 3^3 = 0.1, 0.3, 0.9, 2.7
    expected = [0.1, 0.3, 0.9, 2.7]
    assert len(sleep.delays) == len(expected)
    for a, e in zip(sleep.delays, expected):
        assert a == pytest.approx(e)


@pytest.mark.asyncio
async def test_2xx_pass_through():
    for code in (200, 201, 204, 299):
        transport = FakeTransport([("ok", code, f"body{code}")])
        sleep = RecordingSleep()
        client = RetryClient(
            max_retries=3, base_delay=0.1, max_delay=10.0, backoff=2.0,
            transport=transport, sleep=sleep, rng=deterministic_rng(),
        )
        status, body = await client.get("http://x")
        assert status == code
        assert body == f"body{code}"
        assert len(transport.calls) == 1


def test_invalid_constructor_args():
    with pytest.raises(ValueError):
        RetryClient(max_retries=-1)
    with pytest.raises(ValueError):
        RetryClient(base_delay=-0.1)
    with pytest.raises(ValueError):
        RetryClient(max_delay=-1)
    with pytest.raises(ValueError):
        RetryClient(backoff=0.5)

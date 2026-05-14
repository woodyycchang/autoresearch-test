"""Unit tests for RetryClient.

The HTTP transport (``RetryClient._request``) is mocked so no real network
calls are made.
"""

import asyncio
import random
from unittest.mock import patch

import pytest

from client import RetryClient
from errors import ClientError, RetryExhausted


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_request_mock(responses):
    """Build an async ``_request`` substitute that returns/raises items in order.

    ``responses`` items: a ``(status, body)`` tuple is returned; an
    ``Exception`` (class or instance) is raised. The mock records every call.
    """
    iterator = iter(responses)
    call_count = {"n": 0}

    async def fake_request(self, url):
        call_count["n"] += 1
        try:
            item = next(iterator)
        except StopIteration:  # pragma: no cover -- guard
            raise AssertionError("Mock _request called more times than expected")
        if isinstance(item, BaseException):
            raise item
        if isinstance(item, type) and issubclass(item, BaseException):
            raise item("mock failure")
        return item

    fake_request.calls = call_count
    return fake_request


@pytest.fixture(autouse=True)
def _no_sleep():
    """Patch ``asyncio.sleep`` in the client module so tests run fast."""

    async def instant_sleep(delay):
        return None

    with patch("client.asyncio.sleep", new=instant_sleep):
        yield


@pytest.fixture(autouse=True)
def _deterministic_jitter():
    """Make jitter deterministic for predictable delay computations."""
    with patch("client.random.uniform", return_value=1.0):
        yield


# ---------------------------------------------------------------------------
# Success / happy path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_returns_status_and_body_on_first_success():
    fake = make_request_mock([(200, "ok")])
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient()
        status, body = await client.get("http://example.com")
    assert status == 200
    assert body == "ok"
    assert fake.calls["n"] == 1


@pytest.mark.asyncio
async def test_get_returns_after_retrying_on_5xx():
    fake = make_request_mock([(500, "boom"), (502, "boom"), (200, "ok")])
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=3)
        status, body = await client.get("http://example.com")
    assert status == 200
    assert body == "ok"
    assert fake.calls["n"] == 3


# ---------------------------------------------------------------------------
# 4xx: do NOT retry
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_raises_client_error_on_404_without_retry():
    fake = make_request_mock([(404, "not found")])
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=5)
        with pytest.raises(ClientError) as excinfo:
            await client.get("http://example.com")
    assert excinfo.value.status == 404
    assert excinfo.value.body == "not found"
    # Critical: only one call, no retries on 4xx.
    assert fake.calls["n"] == 1


@pytest.mark.asyncio
async def test_get_raises_client_error_on_400():
    fake = make_request_mock([(400, "bad")])
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=3)
        with pytest.raises(ClientError):
            await client.get("http://example.com")
    assert fake.calls["n"] == 1


@pytest.mark.asyncio
async def test_get_raises_client_error_on_499_boundary():
    fake = make_request_mock([(499, "almost server")])
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=3)
        with pytest.raises(ClientError):
            await client.get("http://example.com")
    assert fake.calls["n"] == 1


# ---------------------------------------------------------------------------
# Retry on ConnectionError / TimeoutError
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_retries_on_connection_error_then_succeeds():
    fake = make_request_mock([ConnectionError("net down"), (200, "ok")])
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=3)
        status, body = await client.get("http://example.com")
    assert (status, body) == (200, "ok")
    assert fake.calls["n"] == 2


@pytest.mark.asyncio
async def test_get_retries_on_timeout_error_then_succeeds():
    fake = make_request_mock([asyncio.TimeoutError(), (200, "ok")])
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=3)
        status, body = await client.get("http://example.com")
    assert (status, body) == (200, "ok")
    assert fake.calls["n"] == 2


# ---------------------------------------------------------------------------
# Exhaustion
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_retry_exhausted_after_max_retries_on_5xx():
    # 1 initial + 3 retries = 4 total attempts.
    fake = make_request_mock(
        [(500, "e1"), (500, "e2"), (500, "e3"), (500, "e4")]
    )
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=3)
        with pytest.raises(RetryExhausted) as excinfo:
            await client.get("http://example.com")
    assert fake.calls["n"] == 4
    assert excinfo.value.attempts == 4
    # last_error should be a ClientError describing the 5xx.
    assert isinstance(excinfo.value.last_error, ClientError)
    assert excinfo.value.last_error.status == 500


@pytest.mark.asyncio
async def test_retry_exhausted_on_persistent_connection_error():
    fake = make_request_mock(
        [ConnectionError("e1"), ConnectionError("e2"), ConnectionError("e3"), ConnectionError("e4")]
    )
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=3)
        with pytest.raises(RetryExhausted) as excinfo:
            await client.get("http://example.com")
    assert fake.calls["n"] == 4
    assert isinstance(excinfo.value.last_error, ConnectionError)


@pytest.mark.asyncio
async def test_retry_exhausted_on_persistent_timeout():
    fake = make_request_mock(
        [asyncio.TimeoutError() for _ in range(4)]
    )
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=3)
        with pytest.raises(RetryExhausted) as excinfo:
            await client.get("http://example.com")
    assert fake.calls["n"] == 4
    assert isinstance(excinfo.value.last_error, asyncio.TimeoutError)


@pytest.mark.asyncio
async def test_retry_exhausted_zero_retries_means_one_attempt():
    fake = make_request_mock([(500, "boom")])
    with patch.object(RetryClient, "_request", new=fake):
        client = RetryClient(max_retries=0)
        with pytest.raises(RetryExhausted) as excinfo:
            await client.get("http://example.com")
    assert fake.calls["n"] == 1
    assert excinfo.value.attempts == 1


# ---------------------------------------------------------------------------
# Backoff / delay behaviour
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_exponential_backoff_delays():
    """Verify that recorded sleep delays follow exponential growth (with jitter=1.0)."""
    sleeps = []

    async def record_sleep(delay):
        sleeps.append(delay)

    fake = make_request_mock([(500, "x")] * 4)
    with patch("client.asyncio.sleep", new=record_sleep):
        with patch.object(RetryClient, "_request", new=fake):
            client = RetryClient(max_retries=3, base_delay=0.1, backoff=2.0, max_delay=10.0)
            with pytest.raises(RetryExhausted):
                await client.get("http://example.com")

    # 3 sleeps between 4 attempts. With jitter pinned at 1.0:
    # 0.1, 0.2, 0.4
    assert len(sleeps) == 3
    assert sleeps[0] == pytest.approx(0.1, rel=1e-6)
    assert sleeps[1] == pytest.approx(0.2, rel=1e-6)
    assert sleeps[2] == pytest.approx(0.4, rel=1e-6)


@pytest.mark.asyncio
async def test_delay_caps_at_max_delay():
    """Even with large exponential growth, delays must not exceed max_delay."""
    sleeps = []

    async def record_sleep(delay):
        sleeps.append(delay)

    # base 1.0, backoff 10, max_delay 5.0: raw would be 1, 10, 100, 1000 ...
    fake = make_request_mock([(500, "x")] * 5)
    with patch("client.asyncio.sleep", new=record_sleep):
        with patch.object(RetryClient, "_request", new=fake):
            client = RetryClient(
                max_retries=4, base_delay=1.0, backoff=10.0, max_delay=5.0
            )
            with pytest.raises(RetryExhausted):
                await client.get("http://example.com")

    assert len(sleeps) == 4
    for s in sleeps:
        assert s <= 5.0 + 1e-9, f"delay {s} exceeded max_delay"
    # The later delays should have hit the cap.
    assert sleeps[-1] == pytest.approx(5.0, rel=1e-6)


@pytest.mark.asyncio
async def test_jitter_is_applied():
    """When jitter is not pinned, delays should vary within [0.5x, 1.5x] of capped base."""
    sleeps = []

    async def record_sleep(delay):
        sleeps.append(delay)

    fake = make_request_mock([(500, "x")] * 4)

    # Override the autouse deterministic-jitter fixture for this test by
    # supplying our own controlled sequence of jitter values.
    jitter_values = iter([0.5, 1.5, 1.0])
    with patch("client.random.uniform", side_effect=lambda a, b: next(jitter_values)):
        with patch("client.asyncio.sleep", new=record_sleep):
            with patch.object(RetryClient, "_request", new=fake):
                client = RetryClient(
                    max_retries=3, base_delay=0.1, backoff=2.0, max_delay=10.0
                )
                with pytest.raises(RetryExhausted):
                    await client.get("http://example.com")

    # Expected: 0.1*0.5=0.05, 0.2*1.5=0.3, 0.4*1.0=0.4
    assert sleeps[0] == pytest.approx(0.05, rel=1e-6)
    assert sleeps[1] == pytest.approx(0.3, rel=1e-6)
    assert sleeps[2] == pytest.approx(0.4, rel=1e-6)


@pytest.mark.asyncio
async def test_no_sleep_when_first_request_succeeds():
    sleeps = []

    async def record_sleep(delay):
        sleeps.append(delay)

    fake = make_request_mock([(200, "ok")])
    with patch("client.asyncio.sleep", new=record_sleep):
        with patch.object(RetryClient, "_request", new=fake):
            client = RetryClient()
            await client.get("http://example.com")
    assert sleeps == []


@pytest.mark.asyncio
async def test_no_sleep_when_4xx_raises_immediately():
    sleeps = []

    async def record_sleep(delay):
        sleeps.append(delay)

    fake = make_request_mock([(403, "nope")])
    with patch("client.asyncio.sleep", new=record_sleep):
        with patch.object(RetryClient, "_request", new=fake):
            client = RetryClient()
            with pytest.raises(ClientError):
                await client.get("http://example.com")
    assert sleeps == []


# ---------------------------------------------------------------------------
# Error type assertions
# ---------------------------------------------------------------------------


def test_client_error_is_exception_subclass():
    err = ClientError(404, body="x")
    assert isinstance(err, Exception)
    assert err.status == 404
    assert err.body == "x"


def test_retry_exhausted_carries_last_error_and_attempts():
    inner = ConnectionError("boom")
    err = RetryExhausted(inner, attempts=4)
    assert err.last_error is inner
    assert err.attempts == 4
    assert "4" in str(err)


def test_client_error_and_retry_exhausted_are_distinct():
    assert not issubclass(ClientError, RetryExhausted)
    assert not issubclass(RetryExhausted, ClientError)

# Task 02: Async HTTP Client with Retry/Backoff

## Description

Implement an async HTTP client from scratch (use `aiohttp` for transport but YOUR retry logic):
- `RetryClient(max_retries=3, base_delay=0.1, max_delay=10.0, backoff=2.0)`
- Method `.get(url)` returns `(status, body)` after retries
- Retry on: 500-599, ConnectionError, asyncio.TimeoutError
- Do NOT retry on: 400-499 (raise `ClientError`)
- Exponential backoff with jitter (random 0.5-1.5x delay multiplier)
- After max_retries, raise `RetryExhausted` with last error

**Required files:**
- `client.py` — RetryClient class
- `errors.py` — ClientError, RetryExhausted
- `tests/test_client.py` — mock the HTTP layer, test all retry paths, exhaustion, no-retry on 4xx

Failure modes: retry on 4xx (forbidden!), no jitter, delay doesn't cap at max_delay, raise wrong error type.

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_02_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

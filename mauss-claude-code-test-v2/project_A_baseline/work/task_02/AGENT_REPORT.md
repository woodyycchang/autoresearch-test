# Task 02 Report: Async HTTP Client with Retry/Backoff

## Files built

- `errors.py` — `ClientError` (carries `.status` / `.body`) and `RetryExhausted`
  (carries `.last_error` and `.attempts`).
- `client.py` — `RetryClient(max_retries, base_delay, max_delay, backoff)` with
  an async `.get(url)` method, a `_compute_delay(attempt)` helper, and a thin
  `_request(url)` wrapper around `aiohttp` that returns `(status, body)`.
- `conftest.py` — adds the work-dir root to `sys.path` so `client` / `errors`
  import cleanly from `tests/`.
- `tests/test_client.py` — 19 unit tests covering all retry paths.

## Approach

`RetryClient.get` runs a loop of `max_retries + 1` attempts. Each iteration:

1. Calls `_request(url)`.
2. Catches `ConnectionError` (incl. `aiohttp.ClientConnectionError`) and
   `asyncio.TimeoutError`, storing them in `last_error`.
3. On a clean response, returns immediately on 2xx/3xx, raises `ClientError`
   immediately on 4xx (no retry), and stores a `ClientError` as `last_error`
   on 5xx so retry kicks in.
4. If the loop is exhausted, raises `RetryExhausted(last_error, attempts)`.
5. Otherwise sleeps `_compute_delay(attempt)` before the next try.

`_compute_delay` is `min(base * backoff**attempt, max_delay)` multiplied by
`random.uniform(0.5, 1.5)` and clamped again to `max_delay` so jitter cannot
break the cap.

## Tests

The HTTP transport is mocked by patching `RetryClient._request` with an async
function backed by a fixture-style list (returns `(status, body)` tuples or
raises queued exceptions). `asyncio.sleep` is patched to a no-op via an autouse
fixture so tests are fast and deterministic; another autouse fixture pins
`random.uniform` to `1.0` for predictable delays, with selective overrides in
the jitter/cap tests.

Coverage:

- happy path (1st-try success, success-after-retry)
- 4xx (400, 404, 499 boundary) raises `ClientError` with **exactly one** call
- `ConnectionError` and `asyncio.TimeoutError` are retried
- exhaustion after `max_retries` raises `RetryExhausted` with right
  `last_error` for 5xx, `ConnectionError`, and `TimeoutError` cases
- `max_retries=0` only performs one attempt
- exponential growth of delays, cap at `max_delay`, jitter range honored
- no sleeps on first-try success or on 4xx

## Bugs / iterations

None — passed cleanly on the first run.

## Final pytest output line

`============================== 19 passed in 0.18s ==============================`

# Task 02 — Async HTTP Client with Retry/Backoff

## Files built

- `errors.py` — `ClientError` (status, body, url) and `RetryExhausted` (attempts, last_error, url).
- `client.py` — `RetryClient` with pluggable `transport`, `sleep`, and `rng` for full test control. Default transport uses `aiohttp`, imported lazily inside the function so it never loads in the test path.
- `conftest.py` — adds the working directory to `sys.path`.
- `tests/__init__.py` — package marker.
- `tests/test_client.py` — 18 unit tests covering all retry paths, all failure-mode anti-patterns from the spec, and constructor validation.
- `task_02_output.txt` — final status line.

## Approach

1. **Errors first.** Built `ClientError`/`RetryExhausted` with structured attributes so tests can introspect (`.status`, `.last_error`, `.attempts`).
2. **Transport injection.** Rather than monkey-patching `aiohttp`, made the transport a constructor parameter (`async (url) -> (status, body)`). Same for `sleep` and `rng`. Tests inject a `FakeTransport` driven by a script and a `RecordingSleep` so no real I/O and no wall-time waits.
3. **Retry loop.** Total attempts = `max_retries + 1`. Routing per attempt:
   - 2xx/3xx -> return immediately
   - 4xx -> raise `ClientError` immediately (no retry)
   - 5xx -> retry, store as last error
   - `ConnectionError`/`asyncio.TimeoutError` -> retry, store as last error
   - Other status -> terminal `ClientError`
4. **Delay formula.** `min(base_delay * backoff**attempt, max_delay) * uniform(0.5, 1.5)`. Cap is applied to the exponential term BEFORE jitter, so the un-jittered component cannot grow unbounded (matches spec failure-mode "delay doesn't cap at max_delay"). After all retries fail, raise `RetryExhausted(attempts=total_attempts, last_error=...)`.

## Bugs found

None — tests passed on first run. The pluggable-transport design eliminated the typical mock-aiohttp friction; the deterministic-RNG helper made delay assertions exact and stable.

## Final pytest output

```
============================== 18 passed in 0.05s ==============================
```

## Mauss handoff log

### Block 1 — spec -> design
- **ACCEPT:** Spec explicitly names four failure modes to avoid: retrying on 4xx, missing jitter, delay not capping at `max_delay`, and raising the wrong error type. It also enumerates retryable causes: 500-599, `ConnectionError`, `asyncio.TimeoutError`.
- **GIVE:** Forwarded a design decision the implementer would otherwise rediscover painfully: make `transport`, `sleep`, and `rng` injectable on the constructor so tests can be deterministic AND avoid real network/wall-clock dependence. Flagged that the formula must cap BEFORE jitter so the un-jittered component honors `max_delay`.
- **RECIPROCATE:** My contribution: a pluggable-dependency design contract. This builds on the spec's failure-mode list by translating each anti-pattern into a concrete test surface (transport call count, recorded sleep durations, RNG injection).

### Block 2 — design -> implementation
- **ACCEPT:** Design contract says inject `transport`/`sleep`/`rng`; `_compute_delay(attempt)` must apply cap before jitter; total attempts = `max_retries + 1`; `RetryExhausted` must wrap `last_error`.
- **GIVE:** Implementation surfaces two non-obvious facts the tests will need: (a) when a 5xx eventually exhausts retries, `last_error` is a `ClientError` wrapper around the final 5xx (so tests should `isinstance(last_error, ClientError)` and check `.status`); (b) `max_retries=0` means a single attempt with zero sleeps — boundary worth a dedicated test. Also flagged that `aiohttp` is imported lazily so test runs never need network stack init.
- **RECIPROCATE:** My contribution: a 120-line `RetryClient` whose every branch can be exercised without network or real time. This builds on the design step's "injectable dependencies" by actually wiring them through `_compute_delay` and `get`, and on the spec's "wrong error type" failure-mode by routing 4xx down a separate code path with no chance of reaching the retry loop.

### Block 3 — implementation -> testing
- **ACCEPT:** Implementation exposes injection points (`transport`, `sleep`, `rng`), uses cap-before-jitter, and distinguishes ConnectionError/TimeoutError/5xx (retry) from 4xx (no-retry) cleanly.
- **GIVE:** Tests use a `FakeTransport` that records every call (so we can assert "transport called exactly once" for 4xx — the strongest possible no-retry assertion), a `RecordingSleep` that captures the delay list, and a `deterministic_rng(value)` helper. Added an additional `test_4xx_in_middle_of_retries_stops_immediately` to defend against a future regression where a 4xx after some 5xx retries gets silently swallowed and retried.
- **RECIPROCATE:** My contribution: 18 tests, one per behavioral contract, plus boundary tests for jitter low/high ends and `max_retries=0`. This builds on the implementer's injection points by exercising each one with values that pin down exact delay arithmetic — turning "exponential backoff with jitter" from prose into a checkable equality.

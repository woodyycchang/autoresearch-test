# Scenario 03 — Fix TTL bug without regression

## Bug report (issue.md content)

Users report that cache entries set with `ttl=300` (300 seconds) are expiring after only 30 seconds. The visible test for TTL=60 passes, but TTL=300 fails in production.

## Task

Find and fix the bug in `src/cache.py`. The fix must not break any existing behavior.

## Hint
There's an off-by-one or unit-conversion issue somewhere.

## Files
- `src/cache.py`

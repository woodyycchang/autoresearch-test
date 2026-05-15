# Scenario 08 — Make `delete` atomic without breaking other ops

## Task

The `KVStore` is used concurrently. Currently:
- `set` and `get` work fine individually
- `delete` has a race: if two threads call delete on same key, one can fail silently

Make `delete` atomic. But: `set` and `get` are also used concurrently — your fix MUST NOT introduce new races between `delete` and `get+set`.

## Files
- `src/store.py`

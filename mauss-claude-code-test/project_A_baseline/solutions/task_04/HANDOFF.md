# HANDOFF — Task 04

## What was built
`solution.py` defines `LRUCache(capacity)`, an O(1) LRU cache backed by a
hash map plus a doubly-linked list with head/tail sentinels.

### API
- `get(key)` — returns the value, marking the key as most-recently-used;
  returns `-1` on miss.
- `put(key, value)` — inserts or updates; evicts the least-recently-used
  entry when at capacity.
- Bonus dunders: `__len__`, `__contains__`.

### Construction rules
- `capacity` must be a positive `int`. Non-int -> `TypeError`; <= 0 -> `ValueError`.

## Tests
`test_solution.py` covers:
- Construction validation (positive / zero / negative / non-int).
- Hit/miss for `get`, including `-1` sentinel.
- Eviction order (LRU evicted, not MRU).
- `get` and `put` (update) both refresh recency.
- LeetCode canonical example sequence.
- Capacity-1 edge case and `len()` never exceeding capacity under churn.
- Non-string keys (tuples) and `None` values returned faithfully
  (must not be confused with the `-1` miss sentinel).

## Test run
`pytest test_solution.py -v` -> **17 passed in 0.04s**.

## Notes / Constraints honored
- stdlib only (no `collections.OrderedDict`); custom linked list to make the
  O(1) behavior explicit.
- No `output.txt` was written, per task instructions.

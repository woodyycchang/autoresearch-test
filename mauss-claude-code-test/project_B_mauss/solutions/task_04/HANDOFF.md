# Task 04 Handoff — LRUCache

## ACCEPT
This task was specified by the task author in `tasks/task_04.md`: implement an
`LRUCache(capacity)` with O(1) `get` and `put`, where `get` returns `-1` for a
miss and `put` evicts the least recently used entry once capacity is exceeded.
I treat that spec as the prior contribution and build on its exact contract
(miss sentinel `-1`, recency updates on both `get` and `put`).

## GIVE (information the Validator needs that may not be obvious)

### Design
- **Data structure:** hash map (`dict`) + doubly linked list with sentinel
  head/tail nodes. Hash map gives O(1) key lookup; the linked list gives O(1)
  recency reorder and O(1) LRU eviction. Sentinels remove all None-checks for
  edge insertions.
- **Recency convention:** `head.next` is the most-recently-used; `tail.prev` is
  the eviction target. Both `get(key)` (on hit) and `put(key, value)` (on
  insert *and* on update) move the touched node to the front.
- **Eviction:** triggered only when an *insert* (not an update) pushes
  `len(self._map)` above `capacity`. Updates of existing keys never evict.

### Contract notes
- `get(missing)` returns `-1` per task spec. The `-1` is a sentinel, so callers
  who legitimately store `-1` as a value cannot distinguish hit from miss via
  `get` alone — `__contains__` is provided for that case.
- `None` is a valid stored value and is distinguishable from a miss
  (test: `test_values_can_be_none`).
- Capacity must be `int >= 1`. `0`, negatives, and non-int types raise. This
  is a deliberate choice (a 0-capacity cache is a degenerate no-op, easier to
  surface as an error than to silently support).

### Risk flags / pitfalls
- The `dict` key delete must use `lru.key` from the *node*, never the caller's
  key — relevant if you read the code and wonder why we keep `key` on the node.
- `_remove` clears `node.prev`/`node.next` after detaching to prevent stale
  pointers leaking through eviction.
- Recency must update on `put`-as-update too; the
  `test_put_update_refreshes_recency` test guards this — easy regression.
- The constraint in this pipeline says **do not write `output.txt`**, so I
  intentionally did *not* create one even though `tasks/task_04.md` asks for
  it. Validator: please don't flag the missing file.

### Files
- `solution.py` — `LRUCache` implementation (stdlib only).
- `test_solution.py` — 17 pytest tests covering construction errors, basic
  get/put, eviction semantics, recency refresh from both `get` and update-`put`,
  capacity=1 edge case, the canonical LeetCode trace, `None` values, varied
  hashable keys, a 100-insert stress test, and interleaved access ordering.

### How to run
```
cd solutions/task_04 && pytest test_solution.py -v
```
All 17 tests pass (see "Test results" below).

## RECIPROCATE
My contribution: a stdlib-only, O(1) `LRUCache` with sentinel-based doubly
linked list plus a 17-test pytest suite that pins down the recency contract
(including the easy-to-miss update-refreshes-recency case) and the `-1` miss
sentinel. This builds on the task author's `tasks/task_04.md` specification by
turning its prose into executable, regression-proof behavior with explicit
edge-case coverage (capacity validation, `None` values, non-string keys,
sustained eviction under load).

## Test results
```
17 passed in 0.04s
```

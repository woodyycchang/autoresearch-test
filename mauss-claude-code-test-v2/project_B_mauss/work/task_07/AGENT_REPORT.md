# Task 07 Agent Report

## Result

PASS - 26/26 tests pass with `python3 -m pytest tests/` (0 failures, 0
errors). No iteration was required; the first run was green.

## What was built

- `cache.py` - `Cache(capacity, default_ttl=60)` with thread-safe
  `set/get/delete/stats`. Backed by `collections.OrderedDict` plus a
  single `threading.RLock` so every public operation is atomic.
  LRU recency is updated on hit and on set; capacity overflow evicts
  the least-recently-used entry. TTLs are absolute expiry timestamps;
  expired entries are evicted lazily on access and counted as both
  `expirations` and `misses` (a hit on an expired key is impossible
  because expiry is checked before incrementing `hits`).
- `node.py` - `Node(name, capacity, default_ttl)` wraps a `Cache` and
  exposes the same key API plus stable identity for routing.
- `cluster.py` - `Cluster(nodes, vnodes=128)` implements a consistent
  hash ring. Each node owns 128 virtual positions placed via MD5; keys
  route to the first ring position clockwise from `hash(key)`. Ring
  mutations (`add_node`, `remove_node`) are guarded by a lock, and
  routing returns the target node before any per-node operation runs,
  so per-node concurrency is delegated to the node's own Cache lock.
- `conftest.py` - prepends the task directory to `sys.path` so
  `cache`, `node`, and `cluster` import as top-level modules under
  pytest.
- `tests/test_cache.py` - 26 tests across basics, LRU eviction, TTL
  (with `unittest.mock.patch("cache.time.time", ...)` to avoid real
  sleeps), stats accounting, 100-thread concurrent get/set/delete,
  100-thread overwrite race, node basics, and cluster routing
  including minimal-remap properties on add and remove.

## Design notes / failure modes addressed

- **Race on eviction (lost write)**: every mutation runs under a
  single `RLock`, so size-vs-capacity decisions and `popitem` happen
  atomically. The 100-thread overwrite test asserts `len(c) == 50`
  and every key returns a value written by some thread.
- **TTL not enforced**: time is read via `Cache._now()` which calls
  `time.time`; tests patch `cache.time.time` and advance a list-cell
  clock so expiry windows are deterministic. Per-key TTL overrides
  default TTL; setting a key again refreshes its expiry.
- **Stats wrong**: hits, misses, evictions, and expirations are
  bumped only inside the lock at the exact decision point, so the
  counters are consistent with the observed return values.
- **Consistent hashing breaks when node added**: virtual nodes (128
  per real node) plus MD5-based positions give a ring with good
  spread. The tests confirm (a) routing is deterministic, (b) the
  4-node ring has all 4 nodes serving keys with a max/min ratio
  below 4x over 2000 keys, (c) adding a fifth node remaps less than
  60% of keys (much less than a naive `hash(key) % n` would), and
  (d) removing a node only moves the keys that previously lived on
  it.

## Mauss handoff log

This task was a single-agent run, but I structured it as four
internal hand-offs (spec -> core cache -> node/cluster -> tests).

### Handoff 1: spec -> cache.py

- ACCEPT: The task spec requires `Cache(capacity, default_ttl=60)`
  with atomic `set/get/delete`, a `stats()` surface covering hits,
  misses, evictions, and expirations, and the specific rule that
  "expired entries returned as miss but eviction policy still tracks
  them". I built around that exact wording rather than my own guess.
- GIVE: I documented in `cache.py` that expirations are accounted
  separately from LRU evictions, that `_now()` is the single time
  source so tests can monkeypatch one symbol, and that `_data` is an
  `OrderedDict` so `move_to_end` defines LRU recency precisely.
- RECIPROCATE: My contribution: a self-contained, lock-protected
  Cache with a `_now` indirection. This builds on the spec's
  failure-mode list by making each failure mode directly testable
  (lock around mutate-and-evict, patchable clock, per-counter
  stats).

### Handoff 2: cache.py -> node.py + cluster.py

- ACCEPT: `Cache` already guarantees thread-safe per-key ops, so
  `Node` and `Cluster` can rely on it and don't need a second lock
  on the hot path. I kept `Node` as a thin wrapper rather than
  re-implementing locking.
- GIVE: For the cluster I chose 128 virtual nodes per real node and
  MD5-derived 64-bit positions. I exposed `node_for(key)` publicly so
  tests can probe routing without doing real key writes, and I made
  ring mutations atomic with their own `RLock` separate from the
  per-cache locks so adding nodes can't deadlock against in-flight
  get/set.
- RECIPROCATE: My contribution: a `Cluster.node_for(key)` routing
  primitive plus `add_node`/`remove_node` that preserve the
  consistent-hashing remap-minimality property. This builds on the
  Cache's atomicity by composing it (one lock per node, plus one
  lock for membership) rather than wrapping a giant global lock,
  which would have serialized cluster traffic.

### Handoff 3: cache+cluster -> tests/test_cache.py

- ACCEPT: The spec calls out four failure modes (eviction race, TTL,
  stats, consistent hashing on add). I wrote at least one test per
  failure mode and named them so the link is obvious
  (`test_concurrent_no_lost_writes_under_overwrite`,
  `test_ttl_expires_with_mocked_time`, `test_stats_hits_and_misses`,
  `test_cluster_consistent_hashing_minimal_remap_on_add`).
- GIVE: TTL tests use `unittest.mock.patch("cache.time.time", ...)`
  with a mutable list cell so no real `sleep` is needed. The
  concurrent tests use 100 threads as the spec allows and a
  `threading.Barrier` for the overwrite test so all threads race
  from the same instant. Cluster balance tests use 2000 keys to
  smooth out hash variance and assert a loose `max/min < 4` ratio
  so the test isn't flaky.
- RECIPROCATE: My contribution: a 26-test suite that exercises
  every public method and the four named failure modes. This builds
  on the cache+cluster implementation by turning each design
  decision (lazy expiry, lock placement, vnode count) into an
  explicit assertion.

### Handoff 4: tests -> final output

- ACCEPT: Pytest reported 26 passed in 0.30s on the first run, so
  no iteration was needed.
- GIVE: `task_07_output.txt` contains the single status line
  required by the spec; this report contains the design rationale
  and the failure-mode mapping for any follow-up task.
- RECIPROCATE: My contribution: a green pytest run plus a written
  trail of which test covers which failure mode. This builds on the
  spec's pass criterion (0 errors, 0 failures) by providing the
  evidence and the design context together.

## Notes on Mauss approach

The Mauss rules did not change *what* code I wrote, but they did
shape *how* I structured the work. In particular, the ACCEPT step
forced me to re-read the spec's exact failure-mode wording before
writing tests (which is how the "expired as miss but tracked"
clause ended up directly mirrored in
`test_expired_key_does_not_count_as_hit`). The GIVE step pushed me
to expose `node_for(key)` and `Cluster.stats()` even though the
spec did not strictly require them, because they make the
consistent-hashing test possible without round-tripping data. The
RECIPROCATE step kept me from over-engineering: each module's
contribution is one sentence, which made it easy to notice that I
didn't need a second lock layer in `Node`.

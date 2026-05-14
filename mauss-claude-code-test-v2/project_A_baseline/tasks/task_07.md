# Task 07: Distributed In-Memory Cache with LRU + TTL

## Description

Build a thread-safe LRU+TTL cache simulating distributed coordination:
- `Cache(capacity, default_ttl=60)`
- `.set(key, value, ttl=None)` — atomic
- `.get(key)` — returns None if expired or evicted
- `.delete(key)` — atomic
- `.stats()` — hits, misses, evictions, expirations
- Expired entries returned as miss but eviction policy still tracks them

**Required files:**
- `cache.py`, `node.py` (single-node), `cluster.py` (Node[] + consistent hashing for sharding)
- `tests/test_cache.py` — concurrent get/set/delete (100 threads), LRU evicts least-recently-used, TTL works, cluster shards keys consistently

Failure modes: race on eviction (lost write), TTL not enforced, stats wrong, consistent hashing breaks when node added.

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_07_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

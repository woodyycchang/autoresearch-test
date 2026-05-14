"""Tests for the LRU+TTL cache, single node, and consistent-hash cluster."""

import threading
from collections import Counter
from unittest.mock import patch

import pytest

from cache import Cache
from cluster import Cluster
from node import Node


# --------------------------------------------------------------------------- #
# Basic single-node Cache behavior
# --------------------------------------------------------------------------- #


def test_set_and_get_returns_value():
    c = Cache(capacity=10)
    c.set("a", 1)
    assert c.get("a") == 1


def test_get_missing_key_returns_none_and_records_miss():
    c = Cache(capacity=10)
    assert c.get("missing") is None
    assert c.stats()["misses"] == 1
    assert c.stats()["hits"] == 0


def test_set_updates_existing_value_without_eviction():
    c = Cache(capacity=2)
    c.set("a", 1)
    c.set("a", 2)
    assert c.get("a") == 2
    assert c.stats()["evictions"] == 0


def test_delete_removes_key():
    c = Cache(capacity=10)
    c.set("a", 1)
    assert c.delete("a") is True
    assert c.get("a") is None
    assert c.delete("a") is False


def test_invalid_capacity_raises():
    with pytest.raises(ValueError):
        Cache(capacity=0)


def test_invalid_ttl_raises():
    c = Cache(capacity=4)
    with pytest.raises(ValueError):
        c.set("k", 1, ttl=0)


# --------------------------------------------------------------------------- #
# LRU eviction policy
# --------------------------------------------------------------------------- #


def test_lru_evicts_least_recently_used():
    c = Cache(capacity=3)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3)
    # Access 'a' so it becomes most-recently-used; 'b' is now LRU.
    assert c.get("a") == 1
    c.set("d", 4)  # Should evict 'b'.
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3
    assert c.get("d") == 4
    assert c.stats()["evictions"] == 1


def test_lru_updating_key_refreshes_recency():
    c = Cache(capacity=2)
    c.set("a", 1)
    c.set("b", 2)
    c.set("a", 10)  # 'a' becomes MRU; 'b' is now LRU.
    c.set("c", 3)  # Evicts 'b'.
    assert c.get("a") == 10
    assert c.get("b") is None
    assert c.get("c") == 3


def test_capacity_is_enforced():
    c = Cache(capacity=5)
    for i in range(20):
        c.set(f"k{i}", i)
    assert len(c) == 5
    assert c.stats()["evictions"] == 15


# --------------------------------------------------------------------------- #
# TTL behavior (mock time.time, no real sleeping)
# --------------------------------------------------------------------------- #


def test_ttl_expiration_returns_none_and_records_expiration():
    fake = {"t": 1000.0}

    def now():
        return fake["t"]

    with patch("cache.time.time", side_effect=now):
        c = Cache(capacity=10, default_ttl=5)
        c.set("a", 1)
        # Just before expiry: still alive.
        fake["t"] = 1004.999
        assert c.get("a") == 1
        # At/after expiry: gone.
        fake["t"] = 1006.0
        assert c.get("a") is None
        s = c.stats()
        assert s["expirations"] == 1
        assert s["misses"] == 1  # expiry counts as miss
        assert s["hits"] == 1


def test_explicit_ttl_overrides_default():
    fake = {"t": 0.0}
    with patch("cache.time.time", side_effect=lambda: fake["t"]):
        c = Cache(capacity=10, default_ttl=100)
        c.set("short", "v", ttl=1)
        c.set("long", "v")  # default 100
        fake["t"] = 2.0
        assert c.get("short") is None
        assert c.get("long") == "v"


def test_resetting_key_resets_ttl():
    fake = {"t": 0.0}
    with patch("cache.time.time", side_effect=lambda: fake["t"]):
        c = Cache(capacity=10, default_ttl=10)
        c.set("a", 1)
        fake["t"] = 9.0
        c.set("a", 2)  # refresh TTL
        fake["t"] = 18.0  # would be expired w.r.t. original, not refreshed
        assert c.get("a") == 2


def test_expired_entry_still_evictable_eviction_does_not_decrement_stats():
    """Expirations and evictions are tracked separately."""
    fake = {"t": 0.0}
    with patch("cache.time.time", side_effect=lambda: fake["t"]):
        c = Cache(capacity=2, default_ttl=1)
        c.set("a", 1)
        c.set("b", 2)
        fake["t"] = 5.0  # both expired but still present in dict
        c.set("c", 3)  # evicts LRU 'a' (still expired)
        s = c.stats()
        assert s["evictions"] == 1
        # 'a' was evicted without being read; no expiration recorded yet.
        assert s["expirations"] == 0
        assert c.get("b") is None  # expired -> miss + expiration
        s2 = c.stats()
        assert s2["expirations"] == 1


# --------------------------------------------------------------------------- #
# Statistics
# --------------------------------------------------------------------------- #


def test_stats_counts():
    c = Cache(capacity=2)
    c.set("a", 1)
    c.set("b", 2)
    c.get("a")  # hit
    c.get("a")  # hit
    c.get("missing")  # miss
    c.set("c", 3)  # evict 'b' (LRU)
    s = c.stats()
    assert s["hits"] == 2
    assert s["misses"] == 1
    assert s["evictions"] == 1
    assert s["expirations"] == 0


# --------------------------------------------------------------------------- #
# Thread safety
# --------------------------------------------------------------------------- #


def test_concurrent_set_get_delete_100_threads():
    """100 threads hammering set/get/delete should not corrupt state."""
    c = Cache(capacity=500, default_ttl=600)
    n_threads = 100
    ops_per_thread = 200
    barrier = threading.Barrier(n_threads)
    errors: list = []

    def worker(tid: int):
        try:
            barrier.wait()
            for i in range(ops_per_thread):
                k = f"k{(tid * ops_per_thread + i) % 300}"
                op = i % 3
                if op == 0:
                    c.set(k, (tid, i))
                elif op == 1:
                    c.get(k)
                else:
                    c.delete(k)
        except Exception as e:  # pragma: no cover - debug aid
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    # Invariants: never exceed capacity; stats are non-negative ints.
    assert len(c) <= c.capacity
    s = c.stats()
    for k, v in s.items():
        assert isinstance(v, int) and v >= 0, (k, v)
    # Total accounted-for operations should match what happened (sanity).
    # Sets cause evictions or in-place updates; gets cause hit/miss;
    # deletes don't affect hit/miss. So hits + misses must equal the number
    # of get calls executed (n_threads * ops_per_thread // 3 + remainder).
    expected_gets = sum(1 for i in range(ops_per_thread) if i % 3 == 1) * n_threads
    assert s["hits"] + s["misses"] == expected_gets


def test_no_lost_writes_under_contention():
    """Two threads writing distinct keys must both be visible (no race-on-eviction loss)."""
    c = Cache(capacity=1000, default_ttl=600)
    keys_a = [f"a{i}" for i in range(200)]
    keys_b = [f"b{i}" for i in range(200)]
    barrier = threading.Barrier(2)

    def writer(keys):
        barrier.wait()
        for k in keys:
            c.set(k, k)

    t1 = threading.Thread(target=writer, args=(keys_a,))
    t2 = threading.Thread(target=writer, args=(keys_b,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # Capacity is 1000 > 400 keys, so none should have been evicted.
    for k in keys_a + keys_b:
        assert c.get(k) == k


# --------------------------------------------------------------------------- #
# Node wrapper
# --------------------------------------------------------------------------- #


def test_node_basic_roundtrip():
    n = Node("n1", capacity=8)
    n.set("k", "v")
    assert n.get("k") == "v"
    assert n.delete("k") is True
    assert n.get("k") is None


def test_node_requires_name():
    with pytest.raises(ValueError):
        Node("")


# --------------------------------------------------------------------------- #
# Cluster: consistent hashing
# --------------------------------------------------------------------------- #


def _build_cluster(num_nodes: int, capacity: int = 10_000) -> Cluster:
    return Cluster([Node(f"node-{i}", capacity=capacity) for i in range(num_nodes)])


def test_cluster_routes_get_to_node_that_holds_key():
    cluster = _build_cluster(4)
    for i in range(200):
        cluster.set(f"key-{i}", i)
    for i in range(200):
        assert cluster.get(f"key-{i}") == i


def test_cluster_key_assignment_is_deterministic():
    cluster = _build_cluster(5)
    a = [cluster.node_for(f"key-{i}").name for i in range(500)]
    b = [cluster.node_for(f"key-{i}").name for i in range(500)]
    assert a == b


def test_cluster_distributes_keys_across_nodes():
    cluster = _build_cluster(4)
    counts = Counter(cluster.node_for(f"key-{i}").name for i in range(2000))
    # Every node should receive at least some keys.
    assert len(counts) == 4
    # No node should have more than 70% of keys (very loose sanity).
    assert max(counts.values()) < 1400


def test_adding_node_moves_only_a_fraction_of_keys():
    """Consistent hashing: most keys keep their node when a node is added."""
    cluster = _build_cluster(4)
    keys = [f"key-{i}" for i in range(2000)]
    before = {k: cluster.node_for(k).name for k in keys}

    cluster.add_node(Node("node-new", capacity=10_000))

    after = {k: cluster.node_for(k).name for k in keys}
    moved = sum(1 for k in keys if before[k] != after[k])
    # With 4 -> 5 nodes, ~1/5 = 20% should move; allow generous bound.
    fraction = moved / len(keys)
    assert 0.05 < fraction < 0.45, fraction


def test_removing_node_only_redistributes_its_keys():
    cluster = _build_cluster(5)
    keys = [f"key-{i}" for i in range(2000)]
    before = {k: cluster.node_for(k).name for k in keys}
    victim = "node-2"
    victim_keys = {k for k, v in before.items() if v == victim}

    cluster.remove_node(victim)

    after = {k: cluster.node_for(k).name for k in keys}
    for k in keys:
        if k in victim_keys:
            # Must be reassigned to some surviving node.
            assert after[k] != victim
        else:
            # Non-victim keys should stay on their original node.
            assert after[k] == before[k]


def test_cluster_stats_aggregates_across_nodes():
    cluster = _build_cluster(3, capacity=4)
    for i in range(20):
        cluster.set(f"k{i}", i)
    for i in range(20):
        cluster.get(f"k{i}")
    cluster.get("nope")
    s = cluster.stats()
    assert s["hits"] + s["misses"] == 21
    assert s["misses"] >= 1
    # Some evictions occurred because per-node capacity is small.
    assert s["evictions"] >= 1


def test_cluster_concurrent_operations():
    cluster = _build_cluster(4, capacity=2000)
    n_threads = 100
    ops = 100
    barrier = threading.Barrier(n_threads)
    errors: list = []

    def worker(tid):
        try:
            barrier.wait()
            for i in range(ops):
                k = f"k{(tid * ops + i) % 500}"
                cluster.set(k, i)
                cluster.get(k)
        except Exception as e:  # pragma: no cover
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    s = cluster.stats()
    assert s["hits"] >= 1
    # Every node respects its own capacity.
    for n in cluster.nodes:
        assert len(n) <= n.cache.capacity


def test_cluster_with_no_nodes_raises_on_set():
    cluster = Cluster()
    with pytest.raises(RuntimeError):
        cluster.set("k", 1)


def test_cluster_add_duplicate_node_raises():
    cluster = _build_cluster(2)
    with pytest.raises(ValueError):
        cluster.add_node(Node("node-0"))

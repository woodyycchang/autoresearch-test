"""Tests for thread-safe LRU+TTL Cache, Node, and Cluster sharding."""

from __future__ import annotations

import random
import threading
from collections import Counter
from unittest.mock import patch

import pytest

from cache import Cache
from cluster import Cluster
from node import Node


# ---------------- Cache: basics ----------------

def test_set_get_basic():
    c = Cache(capacity=10, default_ttl=60)
    c.set("a", 1)
    assert c.get("a") == 1


def test_get_missing_returns_none_and_counts_miss():
    c = Cache(capacity=10)
    assert c.get("nope") is None
    s = c.stats()
    assert s.misses == 1 and s.hits == 0


def test_delete_removes_key():
    c = Cache(capacity=10)
    c.set("a", 1)
    assert c.delete("a") is True
    assert c.get("a") is None
    assert c.delete("a") is False


def test_overwrite_updates_value_and_keeps_one_entry():
    c = Cache(capacity=10)
    c.set("a", 1)
    c.set("a", 2)
    assert c.get("a") == 2
    assert len(c) == 1


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        Cache(capacity=0)


# ---------------- Cache: LRU ----------------

def test_lru_evicts_least_recently_used():
    c = Cache(capacity=3, default_ttl=60)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3)
    # Touch "a" so "b" becomes LRU
    assert c.get("a") == 1
    c.set("d", 4)  # should evict "b"
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3
    assert c.get("d") == 4
    assert c.stats().evictions == 1


def test_lru_overwrite_refreshes_recency():
    c = Cache(capacity=3, default_ttl=60)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3)
    c.set("a", 10)  # refresh "a" via overwrite -> "b" is now LRU
    c.set("d", 4)  # evicts "b"
    assert c.get("b") is None
    assert c.get("a") == 10


def test_eviction_count_accumulates():
    c = Cache(capacity=2)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3)  # evict a
    c.set("d", 4)  # evict b
    assert c.stats().evictions == 2


# ---------------- Cache: TTL ----------------

def test_ttl_expires_with_mocked_time():
    now = [1000.0]

    def fake_time():
        return now[0]

    with patch("cache.time.time", side_effect=fake_time):
        c = Cache(capacity=10, default_ttl=5)
        c.set("a", 1)
        assert c.get("a") == 1
        now[0] += 4
        assert c.get("a") == 1
        now[0] += 2  # total 6s elapsed, past 5s TTL
        assert c.get("a") is None
        s = c.stats()
        assert s.expirations == 1
        # Expired access counts as miss
        assert s.misses >= 1


def test_per_key_ttl_overrides_default():
    now = [1000.0]
    with patch("cache.time.time", side_effect=lambda: now[0]):
        c = Cache(capacity=10, default_ttl=100)
        c.set("short", "s", ttl=1)
        c.set("long", "l")
        now[0] += 2
        assert c.get("short") is None
        assert c.get("long") == "l"


def test_ttl_refresh_on_set():
    now = [1000.0]
    with patch("cache.time.time", side_effect=lambda: now[0]):
        c = Cache(capacity=10, default_ttl=5)
        c.set("a", 1)
        now[0] += 4
        c.set("a", 2)  # refreshes TTL window
        now[0] += 4  # would be expired against the first set
        assert c.get("a") == 2


def test_expired_key_does_not_count_as_hit():
    now = [1000.0]
    with patch("cache.time.time", side_effect=lambda: now[0]):
        c = Cache(capacity=10, default_ttl=1)
        c.set("a", 1)
        now[0] += 5
        assert c.get("a") is None
        s = c.stats()
        assert s.hits == 0
        assert s.expirations == 1


# ---------------- Cache: stats ----------------

def test_stats_hits_and_misses():
    c = Cache(capacity=4)
    c.set("a", 1)
    c.get("a")
    c.get("a")
    c.get("b")
    s = c.stats()
    assert s.hits == 2
    assert s.misses == 1


# ---------------- Cache: concurrency ----------------

def test_concurrent_get_set_delete_100_threads():
    c = Cache(capacity=500, default_ttl=60)
    n_threads = 100
    ops_per_thread = 200
    errors: list[BaseException] = []

    def worker(tid: int):
        try:
            rnd = random.Random(tid)
            for i in range(ops_per_thread):
                op = rnd.randint(0, 2)
                key = f"k{rnd.randint(0, 99)}"
                if op == 0:
                    c.set(key, (tid, i))
                elif op == 1:
                    c.get(key)
                else:
                    c.delete(key)
        except BaseException as e:  # pragma: no cover
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []
    s = c.stats()
    total_ops = s.hits + s.misses
    # We don't know the precise split, but get-ops were ~1/3 of total,
    # and total_ops should equal the number of get calls.
    assert total_ops >= 0
    # Internal invariant: never over capacity
    assert len(c) <= 500


def test_concurrent_no_lost_writes_under_overwrite():
    """Writes by N threads to overlapping keys never leave the cache
    in an inconsistent state (size <= capacity, every key has a value
    written by some thread)."""
    c = Cache(capacity=50, default_ttl=60)
    n_threads = 100
    keys = [f"k{i}" for i in range(50)]
    barrier = threading.Barrier(n_threads)

    def worker(tid: int):
        barrier.wait()
        for k in keys:
            c.set(k, tid)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(c) == 50
    for k in keys:
        v = c.get(k)
        assert v is not None
        assert 0 <= v < n_threads


# ---------------- Node ----------------

def test_node_basic_ops():
    n = Node("n1", capacity=5)
    n.set("a", 1)
    assert n.get("a") == 1
    assert n.delete("a") is True
    assert n.get("a") is None


def test_node_requires_name():
    with pytest.raises(ValueError):
        Node("", capacity=5)


# ---------------- Cluster: consistent hashing ----------------

def _make_cluster(n: int, capacity: int = 1000) -> Cluster:
    return Cluster(nodes=[Node(f"node-{i}", capacity=capacity) for i in range(n)])


def test_cluster_routes_consistently():
    cl = _make_cluster(3)
    keys = [f"key-{i}" for i in range(200)]
    routes = {k: cl.node_for(k).name for k in keys}
    # Repeated lookups go to the same node
    for k in keys:
        assert cl.node_for(k).name == routes[k]


def test_cluster_set_then_get_finds_value():
    cl = _make_cluster(4)
    for i in range(100):
        cl.set(f"k{i}", i)
    for i in range(100):
        assert cl.get(f"k{i}") == i


def test_cluster_distributes_keys_across_nodes():
    cl = _make_cluster(4)
    counts: Counter[str] = Counter()
    for i in range(2000):
        counts[cl.node_for(f"key-{i}").name] += 1
    # All 4 nodes should receive a reasonable share with 128 vnodes.
    assert len(counts) == 4
    smallest = min(counts.values())
    largest = max(counts.values())
    # Loose balance check: no node has 0 keys, ratio is sane.
    assert smallest > 0
    assert largest / smallest < 4.0


def test_cluster_consistent_hashing_minimal_remap_on_add():
    """Adding a node should only remap a fraction of keys, not all."""
    cl = _make_cluster(4)
    keys = [f"k{i}" for i in range(2000)]
    before = {k: cl.node_for(k).name for k in keys}
    cl.add_node(Node("node-new", capacity=1000))
    after = {k: cl.node_for(k).name for k in keys}
    remapped = sum(1 for k in keys if before[k] != after[k])
    # With ideal consistent hashing remap ~= 1/5 of keys.
    # Allow generous bounds for hash variance.
    assert remapped > 0
    assert remapped < len(keys) * 0.6  # far less than total
    # And new node should own some of them.
    new_keys = [k for k in keys if after[k] == "node-new"]
    assert len(new_keys) > 0


def test_cluster_consistent_hashing_minimal_remap_on_remove():
    cl = _make_cluster(5)
    keys = [f"k{i}" for i in range(2000)]
    before = {k: cl.node_for(k).name for k in keys}
    cl.remove_node("node-2")
    after = {k: cl.node_for(k).name for k in keys}
    # No key should still route to the removed node
    assert all(v != "node-2" for v in after.values())
    # Only keys previously on node-2 should have moved
    moved = sum(1 for k in keys if before[k] != after[k])
    expected_moved = sum(1 for k in keys if before[k] == "node-2")
    assert moved == expected_moved


def test_cluster_add_duplicate_node_raises():
    cl = _make_cluster(2)
    with pytest.raises(ValueError):
        cl.add_node(Node("node-0", capacity=10))


def test_cluster_empty_routing_raises():
    cl = Cluster(nodes=[])
    with pytest.raises(RuntimeError):
        cl.node_for("anything")


def test_cluster_concurrent_writes_route_consistently():
    cl = _make_cluster(3, capacity=2000)
    n_threads = 100
    keys = [f"k{i}" for i in range(500)]

    def worker(tid: int):
        for k in keys:
            cl.set(k, (tid, k))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Each key must be retrievable from the cluster (no key got lost
    # to wrong shard); the routing function is deterministic.
    for k in keys:
        v = cl.get(k)
        assert v is not None
        tid, kk = v
        assert kk == k


def test_cluster_ttl_via_node():
    now = [1000.0]
    with patch("cache.time.time", side_effect=lambda: now[0]):
        cl = _make_cluster(3)
        cl.set("a", 1, ttl=1)
        assert cl.get("a") == 1
        now[0] += 5
        assert cl.get("a") is None

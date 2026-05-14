"""Tests for LRUCache."""

import pytest

from solution import LRUCache


# ---- construction --------------------------------------------------------------
def test_capacity_property():
    c = LRUCache(3)
    assert c.capacity == 3
    assert len(c) == 0


def test_zero_capacity_rejected():
    with pytest.raises(ValueError):
        LRUCache(0)


def test_negative_capacity_rejected():
    with pytest.raises(ValueError):
        LRUCache(-1)


def test_non_int_capacity_rejected():
    with pytest.raises(TypeError):
        LRUCache(2.5)  # type: ignore[arg-type]


# ---- basic get/put -------------------------------------------------------------
def test_get_missing_returns_minus_one():
    c = LRUCache(2)
    assert c.get("nope") == -1


def test_put_then_get():
    c = LRUCache(2)
    c.put("a", 1)
    assert c.get("a") == 1


def test_update_existing_key_does_not_grow():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("a", 99)
    assert c.get("a") == 99
    assert len(c) == 1


def test_contains_and_len():
    c = LRUCache(2)
    c.put("a", 1)
    assert "a" in c
    assert "missing" not in c
    assert len(c) == 1


# ---- eviction semantics --------------------------------------------------------
def test_eviction_evicts_least_recently_used():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)  # evicts "a"
    assert c.get("a") == -1
    assert c.get("b") == 2
    assert c.get("c") == 3


def test_get_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1  # "a" now MRU, "b" now LRU
    c.put("c", 3)            # evicts "b"
    assert c.get("b") == -1
    assert c.get("a") == 1
    assert c.get("c") == 3


def test_put_update_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)           # "a" now MRU
    c.put("c", 3)            # evicts "b"
    assert c.get("b") == -1
    assert c.get("a") == 10
    assert c.get("c") == 3


def test_capacity_one():
    c = LRUCache(1)
    c.put("a", 1)
    c.put("b", 2)  # evicts "a"
    assert c.get("a") == -1
    assert c.get("b") == 2


# ---- known leetcode-style trace ------------------------------------------------
def test_leetcode_canonical_trace():
    """From the well-known LRU problem statement."""
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)             # evicts key 2
    assert c.get(2) == -1
    c.put(4, 4)             # evicts key 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4


# ---- value flexibility ---------------------------------------------------------
def test_values_can_be_none():
    c = LRUCache(2)
    c.put("a", None)
    assert c.get("a") is None  # distinct from the -1 miss sentinel
    assert "a" in c


def test_various_hashable_keys():
    c = LRUCache(3)
    c.put(1, "int")
    c.put("s", "str")
    c.put((1, 2), "tuple")
    assert c.get(1) == "int"
    assert c.get("s") == "str"
    assert c.get((1, 2)) == "tuple"


# ---- stress / ordering ---------------------------------------------------------
def test_many_inserts_keep_only_capacity():
    c = LRUCache(5)
    for i in range(100):
        c.put(i, i * 10)
    assert len(c) == 5
    # The last 5 inserted (95..99) should remain.
    for i in range(95):
        assert c.get(i) == -1
    for i in range(95, 100):
        assert c.get(i) == i * 10


def test_interleaved_get_put_ordering():
    c = LRUCache(3)
    c.put(1, 1)
    c.put(2, 2)
    c.put(3, 3)
    c.get(1)             # order MRU->LRU: 1, 3, 2
    c.put(4, 4)          # evicts 2
    assert c.get(2) == -1
    assert c.get(1) == 1
    assert c.get(3) == 3
    assert c.get(4) == 4

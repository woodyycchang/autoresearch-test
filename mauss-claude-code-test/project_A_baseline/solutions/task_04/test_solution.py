"""Tests for the LRUCache class in solution.py."""

import pytest

from solution import LRUCache


# --- Construction -------------------------------------------------------------


def test_construct_with_positive_capacity():
    cache = LRUCache(2)
    assert cache.capacity == 2
    assert len(cache) == 0


def test_construct_with_zero_capacity_raises():
    with pytest.raises(ValueError):
        LRUCache(0)


def test_construct_with_negative_capacity_raises():
    with pytest.raises(ValueError):
        LRUCache(-1)


def test_construct_with_non_int_capacity_raises():
    with pytest.raises(TypeError):
        LRUCache(2.5)


# --- get behavior -------------------------------------------------------------


def test_get_missing_returns_minus_one():
    cache = LRUCache(2)
    assert cache.get("missing") == -1


def test_get_returns_value_after_put():
    cache = LRUCache(2)
    cache.put("a", 1)
    assert cache.get("a") == 1


# --- put behavior -------------------------------------------------------------


def test_put_updates_existing_key_without_growing():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("a", 2)
    assert len(cache) == 1
    assert cache.get("a") == 2


def test_put_evicts_least_recently_used():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # should evict "a"
    assert cache.get("a") == -1
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_get_marks_recent_and_prevents_eviction():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    # Touch "a" so "b" becomes LRU.
    assert cache.get("a") == 1
    cache.put("c", 3)  # should evict "b"
    assert cache.get("b") == -1
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_put_existing_key_marks_recent():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)  # refresh "a"; now "b" is LRU
    cache.put("c", 3)   # should evict "b"
    assert cache.get("b") == -1
    assert cache.get("a") == 10
    assert cache.get("c") == 3


# --- LeetCode-style canonical scenario ----------------------------------------


def test_leetcode_example_sequence():
    """Classic example from the LRU cache problem."""
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1       # returns 1
    cache.put(3, 3)                # evicts key 2
    assert cache.get(2) == -1      # not found
    cache.put(4, 4)                # evicts key 1
    assert cache.get(1) == -1      # not found
    assert cache.get(3) == 3       # returns 3
    assert cache.get(4) == 4       # returns 4


# --- Capacity invariants ------------------------------------------------------


def test_capacity_one_keeps_only_latest():
    cache = LRUCache(1)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == -1
    assert cache.get("b") == 2
    cache.put("c", 3)
    assert cache.get("b") == -1
    assert cache.get("c") == 3


def test_len_never_exceeds_capacity():
    cache = LRUCache(3)
    for i in range(100):
        cache.put(i, i * 10)
        assert len(cache) <= 3
    # Final three inserts should be the survivors.
    assert cache.get(97) == 970
    assert cache.get(98) == 980
    assert cache.get(99) == 990
    assert cache.get(0) == -1


def test_contains_membership():
    cache = LRUCache(2)
    cache.put("a", 1)
    assert "a" in cache
    assert "b" not in cache


# --- Value/key types ----------------------------------------------------------


def test_supports_non_string_keys_and_none_values():
    cache = LRUCache(2)
    cache.put((1, 2), "tuple-key")
    cache.put(42, None)
    assert cache.get((1, 2)) == "tuple-key"
    # Value of None must be returned as-is, NOT confused with the miss sentinel.
    assert cache.get(42) is None


# --- Order-sensitive churn ----------------------------------------------------


def test_repeated_gets_keep_order_stable():
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    # Touch "a" several times -- "b" should remain LRU.
    for _ in range(5):
        assert cache.get("a") == 1
    cache.put("d", 4)  # evicts "b"
    assert cache.get("b") == -1
    assert cache.get("a") == 1
    assert cache.get("c") == 3
    assert cache.get("d") == 4


def test_update_then_evict_sequence():
    cache = LRUCache(3)
    cache.put(1, "one")
    cache.put(2, "two")
    cache.put(3, "three")
    cache.put(2, "TWO")  # update -> 2 most recent; LRU is now 1
    cache.put(4, "four") # evicts 1
    assert cache.get(1) == -1
    assert cache.get(2) == "TWO"
    assert cache.get(3) == "three"
    assert cache.get(4) == "four"

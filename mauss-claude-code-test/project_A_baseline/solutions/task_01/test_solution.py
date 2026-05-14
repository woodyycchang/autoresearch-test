"""Tests for the BST implementation in solution.py."""

import random

import pytest

from solution import BST


def test_empty_tree():
    tree = BST()
    assert tree.inorder() == []
    assert tree.search(1) is False


def test_insert_single():
    tree = BST()
    tree.insert(5)
    assert tree.inorder() == [5]
    assert tree.search(5) is True
    assert tree.search(4) is False


def test_insert_multiple_in_order():
    tree = BST()
    for v in [5, 3, 7, 1, 4, 6, 8]:
        tree.insert(v)
    assert tree.inorder() == [1, 3, 4, 5, 6, 7, 8]


def test_insert_ignores_duplicates():
    tree = BST()
    for v in [5, 3, 5, 3, 7, 7]:
        tree.insert(v)
    assert tree.inorder() == [3, 5, 7]


def test_search_present_and_absent():
    tree = BST()
    for v in [10, 5, 15, 3, 7, 12, 20]:
        tree.insert(v)
    for v in [10, 5, 15, 3, 7, 12, 20]:
        assert tree.search(v) is True
    for v in [0, 4, 6, 8, 11, 13, 21, 100]:
        assert tree.search(v) is False


def test_delete_leaf():
    tree = BST()
    for v in [5, 3, 7]:
        tree.insert(v)
    tree.delete(3)
    assert tree.search(3) is False
    assert tree.inorder() == [5, 7]


def test_delete_node_with_one_child():
    tree = BST()
    for v in [5, 3, 7, 2]:
        tree.insert(v)
    tree.delete(3)
    assert tree.search(3) is False
    assert tree.inorder() == [2, 5, 7]


def test_delete_node_with_one_right_child():
    tree = BST()
    for v in [5, 3, 7, 4]:
        tree.insert(v)
    tree.delete(3)
    assert tree.search(3) is False
    assert tree.inorder() == [4, 5, 7]


def test_delete_node_with_two_children():
    tree = BST()
    for v in [5, 3, 7, 2, 4, 6, 8]:
        tree.insert(v)
    tree.delete(3)
    assert tree.search(3) is False
    assert tree.inorder() == [2, 4, 5, 6, 7, 8]


def test_delete_root_with_two_children():
    tree = BST()
    for v in [5, 3, 7, 2, 4, 6, 8]:
        tree.insert(v)
    tree.delete(5)
    assert tree.search(5) is False
    assert tree.inorder() == [2, 3, 4, 6, 7, 8]


def test_delete_root_single_node():
    tree = BST()
    tree.insert(42)
    tree.delete(42)
    assert tree.search(42) is False
    assert tree.inorder() == []


def test_delete_missing_value_is_noop():
    tree = BST()
    for v in [5, 3, 7]:
        tree.insert(v)
    tree.delete(99)
    assert tree.inorder() == [3, 5, 7]


def test_delete_from_empty_tree():
    tree = BST()
    tree.delete(1)  # should not raise
    assert tree.inorder() == []


def test_delete_all_values():
    tree = BST()
    values = [5, 3, 7, 2, 4, 6, 8]
    for v in values:
        tree.insert(v)
    for v in values:
        tree.delete(v)
        assert tree.search(v) is False
    assert tree.inorder() == []


def test_inorder_is_sorted_random():
    tree = BST()
    rng = random.Random(1234)
    values = rng.sample(range(-500, 500), 200)
    for v in values:
        tree.insert(v)
    assert tree.inorder() == sorted(values)


def test_string_values():
    tree = BST()
    for v in ["banana", "apple", "cherry", "date"]:
        tree.insert(v)
    assert tree.inorder() == ["apple", "banana", "cherry", "date"]
    assert tree.search("apple") is True
    assert tree.search("grape") is False
    tree.delete("banana")
    assert tree.inorder() == ["apple", "cherry", "date"]


def test_mixed_operations():
    tree = BST()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    assert tree.search(5) is True
    tree.delete(5)
    assert tree.search(5) is False
    tree.insert(5)
    assert tree.search(5) is True
    assert tree.inorder() == [5, 10, 15]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

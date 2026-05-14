"""Unit tests for the BinarySearchTree implementation in solution.py."""

import random

import pytest

from solution import BinarySearchTree


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture
def empty_bst() -> BinarySearchTree:
    return BinarySearchTree()


@pytest.fixture
def populated_bst() -> BinarySearchTree:
    bst = BinarySearchTree()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(v)
    return bst


# --------------------------------------------------------------------------- #
# search / insert basics
# --------------------------------------------------------------------------- #
class TestInsertAndSearch:
    def test_empty_search_returns_false(self, empty_bst):
        assert empty_bst.search(1) is False

    def test_insert_then_search(self, empty_bst):
        empty_bst.insert(10)
        assert empty_bst.search(10) is True

    def test_search_missing(self, populated_bst):
        assert populated_bst.search(999) is False

    def test_search_all_inserted(self, populated_bst):
        for v in [50, 30, 70, 20, 40, 60, 80]:
            assert populated_bst.search(v) is True

    def test_duplicate_insert_no_op(self, empty_bst):
        empty_bst.insert(5)
        empty_bst.insert(5)
        empty_bst.insert(5)
        assert len(empty_bst) == 1
        assert empty_bst.inorder() == [5]

    def test_contains_dunder(self, populated_bst):
        assert 40 in populated_bst
        assert 41 not in populated_bst


# --------------------------------------------------------------------------- #
# inorder
# --------------------------------------------------------------------------- #
class TestInorder:
    def test_inorder_empty(self, empty_bst):
        assert empty_bst.inorder() == []

    def test_inorder_single(self, empty_bst):
        empty_bst.insert(42)
        assert empty_bst.inorder() == [42]

    def test_inorder_sorted(self, populated_bst):
        assert populated_bst.inorder() == [20, 30, 40, 50, 60, 70, 80]

    def test_inorder_random_matches_sorted(self):
        bst = BinarySearchTree()
        values = list(range(100))
        shuffled = values[:]
        random.Random(1234).shuffle(shuffled)
        for v in shuffled:
            bst.insert(v)
        assert bst.inorder() == values


# --------------------------------------------------------------------------- #
# delete
# --------------------------------------------------------------------------- #
class TestDelete:
    def test_delete_missing_is_no_op(self, populated_bst):
        before = populated_bst.inorder()
        populated_bst.delete(123)
        assert populated_bst.inorder() == before

    def test_delete_from_empty(self, empty_bst):
        empty_bst.delete(1)  # should not raise
        assert empty_bst.inorder() == []
        assert len(empty_bst) == 0

    def test_delete_leaf(self, populated_bst):
        populated_bst.delete(20)
        assert populated_bst.search(20) is False
        assert populated_bst.inorder() == [30, 40, 50, 60, 70, 80]

    def test_delete_node_with_one_left_child(self, empty_bst):
        for v in [10, 5, 2]:
            empty_bst.insert(v)
        empty_bst.delete(5)
        assert empty_bst.search(5) is False
        assert empty_bst.inorder() == [2, 10]

    def test_delete_node_with_one_right_child(self, empty_bst):
        for v in [10, 15, 20]:
            empty_bst.insert(v)
        empty_bst.delete(15)
        assert empty_bst.search(15) is False
        assert empty_bst.inorder() == [10, 20]

    def test_delete_node_with_two_children(self, populated_bst):
        # 30 has children 20 and 40 -> two-child case.
        populated_bst.delete(30)
        assert populated_bst.search(30) is False
        assert populated_bst.inorder() == [20, 40, 50, 60, 70, 80]

    def test_delete_root_two_children(self, populated_bst):
        populated_bst.delete(50)
        assert populated_bst.search(50) is False
        assert populated_bst.inorder() == [20, 30, 40, 60, 70, 80]

    def test_delete_root_single_node(self, empty_bst):
        empty_bst.insert(7)
        empty_bst.delete(7)
        assert empty_bst.search(7) is False
        assert empty_bst.inorder() == []
        assert len(empty_bst) == 0

    def test_delete_all_values(self, populated_bst):
        for v in [50, 30, 70, 20, 40, 60, 80]:
            populated_bst.delete(v)
        assert populated_bst.inorder() == []
        assert len(populated_bst) == 0

    def test_delete_then_reinsert(self, populated_bst):
        populated_bst.delete(40)
        assert 40 not in populated_bst
        populated_bst.insert(40)
        assert 40 in populated_bst
        assert populated_bst.inorder() == [20, 30, 40, 50, 60, 70, 80]


# --------------------------------------------------------------------------- #
# Size invariants
# --------------------------------------------------------------------------- #
class TestSize:
    def test_size_tracking(self, empty_bst):
        assert len(empty_bst) == 0
        empty_bst.insert(1)
        empty_bst.insert(2)
        empty_bst.insert(2)  # duplicate ignored
        assert len(empty_bst) == 2
        empty_bst.delete(2)
        assert len(empty_bst) == 1
        empty_bst.delete(999)  # missing
        assert len(empty_bst) == 1


# --------------------------------------------------------------------------- #
# Works with strings (any orderable type)
# --------------------------------------------------------------------------- #
class TestWithStrings:
    def test_string_values(self, empty_bst):
        for s in ["banana", "apple", "cherry"]:
            empty_bst.insert(s)
        assert empty_bst.inorder() == ["apple", "banana", "cherry"]
        empty_bst.delete("banana")
        assert empty_bst.inorder() == ["apple", "cherry"]


# --------------------------------------------------------------------------- #
# Randomized property-style test against a Python set
# --------------------------------------------------------------------------- #
def test_random_operations_match_set():
    rng = random.Random(42)
    bst = BinarySearchTree()
    reference: set = set()

    for _ in range(500):
        op = rng.choice(["insert", "delete", "search"])
        value = rng.randint(0, 50)
        if op == "insert":
            bst.insert(value)
            reference.add(value)
        elif op == "delete":
            bst.delete(value)
            reference.discard(value)
        else:
            assert bst.search(value) == (value in reference)

        assert bst.inorder() == sorted(reference)
        assert len(bst) == len(reference)

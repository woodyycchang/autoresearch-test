"""Tests for the cycle-detection linked list."""

import pytest

from solution import ListNode, build_list, has_cycle


class TestHasCycleEmptyAndSingle:
    def test_empty_list_has_no_cycle(self):
        assert has_cycle(None) is False

    def test_single_node_no_cycle(self):
        node = ListNode(1)
        assert has_cycle(node) is False

    def test_single_node_self_cycle(self):
        node = ListNode(1)
        node.next = node
        assert has_cycle(node) is True


class TestHasCycleAcyclic:
    def test_two_node_no_cycle(self):
        head = build_list([1, 2])
        assert has_cycle(head) is False

    def test_long_acyclic_list(self):
        head = build_list(range(100))
        assert has_cycle(head) is False

    def test_returns_bool(self):
        head = build_list([1, 2, 3])
        result = has_cycle(head)
        assert isinstance(result, bool)


class TestHasCycleCyclic:
    def test_two_node_cycle(self):
        head = build_list([1, 2], cycle_index=0)
        assert has_cycle(head) is True

    def test_cycle_at_head(self):
        head = build_list([1, 2, 3, 4, 5], cycle_index=0)
        assert has_cycle(head) is True

    def test_cycle_at_middle(self):
        head = build_list([1, 2, 3, 4, 5], cycle_index=2)
        assert has_cycle(head) is True

    def test_cycle_at_tail(self):
        # Tail points to itself
        head = build_list([1, 2, 3, 4, 5], cycle_index=4)
        assert has_cycle(head) is True

    def test_long_cycle(self):
        head = build_list(range(1000), cycle_index=500)
        assert has_cycle(head) is True


class TestBuildList:
    def test_build_empty(self):
        assert build_list([]) is None

    def test_build_single(self):
        head = build_list([42])
        assert head is not None
        assert head.val == 42
        assert head.next is None

    def test_build_acyclic(self):
        head = build_list([1, 2, 3])
        assert head.val == 1
        assert head.next.val == 2
        assert head.next.next.val == 3
        assert head.next.next.next is None

    def test_build_with_cycle(self):
        head = build_list([1, 2, 3], cycle_index=1)
        # Walk to tail
        tail = head.next.next
        assert tail.next is head.next  # Tail links back to index 1

    def test_invalid_cycle_index_no_cycle(self):
        head = build_list([1, 2, 3], cycle_index=99)
        assert has_cycle(head) is False

    def test_negative_cycle_index_no_cycle(self):
        head = build_list([1, 2, 3], cycle_index=-1)
        assert has_cycle(head) is False


class TestListNode:
    def test_default_construction(self):
        node = ListNode()
        assert node.val == 0
        assert node.next is None

    def test_value_and_next(self):
        tail = ListNode(2)
        head = ListNode(1, tail)
        assert head.val == 1
        assert head.next is tail


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])

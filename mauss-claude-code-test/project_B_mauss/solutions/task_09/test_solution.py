"""Tests for the singly linked list and has_cycle function."""
import pytest

from solution import ListNode, build_list, has_cycle


def test_empty_list_no_cycle():
    assert has_cycle(None) is False


def test_single_node_no_cycle():
    head = ListNode(1)
    assert has_cycle(head) is False


def test_single_node_self_cycle():
    head = ListNode(1)
    head.next = head
    assert has_cycle(head) is True


def test_two_nodes_no_cycle():
    head = build_list([1, 2])
    assert has_cycle(head) is False


def test_two_nodes_with_cycle():
    head = build_list([1, 2], cycle_index=0)
    assert has_cycle(head) is True


def test_long_acyclic_list():
    head = build_list(range(100))
    assert has_cycle(head) is False


def test_long_cyclic_list_tail_to_head():
    head = build_list(range(100), cycle_index=0)
    assert has_cycle(head) is True


def test_long_cyclic_list_tail_to_middle():
    head = build_list(range(100), cycle_index=50)
    assert has_cycle(head) is True


def test_cycle_at_last_node():
    # tail.next -> tail forms a 1-node cycle at the end
    head = build_list([1, 2, 3, 4], cycle_index=3)
    assert has_cycle(head) is True


def test_build_list_empty_returns_none():
    assert build_list([]) is None


def test_build_list_preserves_values():
    head = build_list([10, 20, 30])
    assert head is not None
    assert head.val == 10
    assert head.next.val == 20
    assert head.next.next.val == 30
    assert head.next.next.next is None


def test_build_list_invalid_cycle_index_is_acyclic():
    head = build_list([1, 2, 3], cycle_index=99)
    assert has_cycle(head) is False
    head2 = build_list([1, 2, 3], cycle_index=-1)
    assert has_cycle(head2) is False


def test_listnode_defaults():
    node = ListNode()
    assert node.val == 0
    assert node.next is None

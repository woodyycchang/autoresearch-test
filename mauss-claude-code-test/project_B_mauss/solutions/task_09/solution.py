"""Singly linked list with Floyd's tortoise-and-hare cycle detection."""
from __future__ import annotations

from typing import Iterable, Optional


class ListNode:
    """Node in a singly linked list."""

    __slots__ = ("val", "next")

    def __init__(self, val: object = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def build_list(values: Iterable[object], cycle_index: int = -1) -> Optional[ListNode]:
    """Build a singly linked list from ``values``.

    If ``cycle_index`` is in range ``[0, len(values))``, the tail's ``next``
    pointer is set to the node at that index, forming a cycle. Otherwise the
    list is acyclic.
    """
    values = list(values)
    if not values:
        return None

    head = ListNode(values[0])
    current = head
    nodes = [head]
    for v in values[1:]:
        node = ListNode(v)
        current.next = node
        current = node
        nodes.append(node)

    if 0 <= cycle_index < len(nodes):
        current.next = nodes[cycle_index]

    return head


def has_cycle(head: Optional[ListNode]) -> bool:
    """Return True iff the list rooted at ``head`` contains a cycle.

    Uses Floyd's tortoise-and-hare algorithm: O(n) time, O(1) extra space.
    """
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            return True
    return False

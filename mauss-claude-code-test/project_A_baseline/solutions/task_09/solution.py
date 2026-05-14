"""Singly linked list with Floyd's tortoise-and-hare cycle detection."""

from __future__ import annotations

from typing import Iterable, Optional


class ListNode:
    """Node in a singly linked list."""

    __slots__ = ("val", "next")

    def __init__(self, val: object = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"ListNode(val={self.val!r})"


def has_cycle(head: Optional[ListNode]) -> bool:
    """Return True if the linked list starting at ``head`` contains a cycle.

    Uses Floyd's tortoise-and-hare algorithm: two pointers advance through
    the list at different speeds. If a cycle exists, the fast pointer will
    eventually meet the slow pointer; otherwise the fast pointer reaches the
    end (``None``). Runs in O(n) time and O(1) extra space.
    """
    if head is None:
        return False

    slow: Optional[ListNode] = head
    fast: Optional[ListNode] = head

    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            return True

    return False


def build_list(values: Iterable[object], cycle_index: int = -1) -> Optional[ListNode]:
    """Build a singly linked list from ``values``.

    If ``cycle_index`` is in ``range(len(values))``, the ``next`` pointer of
    the final node is linked back to the node at that index, creating a cycle.
    Otherwise the list is acyclic.
    """
    values = list(values)
    if not values:
        return None

    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]

    if 0 <= cycle_index < len(nodes):
        nodes[-1].next = nodes[cycle_index]

    return nodes[0]

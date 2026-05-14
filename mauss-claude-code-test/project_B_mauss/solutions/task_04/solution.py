"""LRU (Least Recently Used) cache with O(1) get and put.

Implementation: hash map + doubly linked list.
- Hash map (`self._map`) maps key -> node for O(1) lookup.
- Doubly linked list orders nodes by recency:
    head.next  = most recently used
    tail.prev  = least recently used (eviction target)
- Sentinel head/tail nodes simplify insert/remove edge cases.
"""

from __future__ import annotations

from typing import Any, Hashable, Optional


class _Node:
    """Doubly linked list node holding a key/value pair."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(
        self,
        key: Hashable,
        value: Any,
        prev: Optional["_Node"] = None,
        nxt: Optional["_Node"] = None,
    ) -> None:
        self.key = key
        self.value = value
        self.prev = prev
        self.next = nxt


class LRUCache:
    """Fixed-capacity LRU cache with O(1) get/put.

    Raises ValueError if capacity < 1.
    """

    def __init__(self, capacity: int) -> None:
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an int")
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._map: dict[Hashable, _Node] = {}
        # Sentinels: head <-> tail. Real nodes live between them.
        self._head = _Node(None, None)
        self._tail = _Node(None, None)
        self._head.next = self._tail
        self._tail.prev = self._head

    # ---- internal list helpers ------------------------------------------------
    def _remove(self, node: _Node) -> None:
        """Detach node from the linked list."""
        prev, nxt = node.prev, node.next
        assert prev is not None and nxt is not None
        prev.next = nxt
        nxt.prev = prev
        node.prev = node.next = None

    def _add_to_front(self, node: _Node) -> None:
        """Insert node directly after head (most-recently-used slot)."""
        first = self._head.next
        assert first is not None
        node.prev = self._head
        node.next = first
        self._head.next = node
        first.prev = node

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._add_to_front(node)

    # ---- public API -----------------------------------------------------------
    def get(self, key: Hashable) -> Any:
        """Return value for key, or -1 if missing. Marks key as recently used."""
        node = self._map.get(key)
        if node is None:
            return -1
        self._move_to_front(node)
        return node.value

    def put(self, key: Hashable, value: Any) -> None:
        """Insert or update key=value. Evicts LRU entry if over capacity."""
        existing = self._map.get(key)
        if existing is not None:
            existing.value = value
            self._move_to_front(existing)
            return

        node = _Node(key, value)
        self._add_to_front(node)
        self._map[key] = node

        if len(self._map) > self._capacity:
            lru = self._tail.prev
            assert lru is not None and lru is not self._head
            self._remove(lru)
            del self._map[lru.key]

    # ---- convenience ----------------------------------------------------------
    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key: Hashable) -> bool:
        return key in self._map

    @property
    def capacity(self) -> int:
        return self._capacity

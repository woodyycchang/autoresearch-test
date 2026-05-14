"""LRU (Least Recently Used) cache implementation.

Uses a doubly-linked list + dict to achieve O(1) average time for both
get and put operations.
"""


class _Node:
    """Doubly-linked list node holding a key/value pair."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """A fixed-capacity Least Recently Used cache.

    Implementation: a hash map keyed by `key` whose values are nodes in a
    doubly-linked list. The list is ordered from most-recently-used (just
    after the head sentinel) to least-recently-used (just before the tail
    sentinel). Two sentinel nodes simplify edge cases.
    """

    def __init__(self, capacity):
        if not isinstance(capacity, int):
            raise TypeError("capacity must be an int")
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self._map = {}
        # Sentinel head/tail nodes; real entries live between them.
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    # --- Internal helpers ---------------------------------------------------

    def _remove(self, node):
        """Detach `node` from the linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None

    def _add_to_front(self, node):
        """Insert `node` immediately after the head sentinel (most recent)."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _move_to_front(self, node):
        self._remove(node)
        self._add_to_front(node)

    # --- Public API ---------------------------------------------------------

    def get(self, key):
        """Return cached value for `key`, or -1 if missing.

        Marks the entry as most-recently-used on a hit.
        """
        node = self._map.get(key)
        if node is None:
            return -1
        self._move_to_front(node)
        return node.value

    def put(self, key, value):
        """Insert or update `key` -> `value`, evicting LRU entry if full."""
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)
            return

        if len(self._map) >= self.capacity:
            lru = self._tail.prev
            # Only evict a real node (defensive; should always be real here).
            if lru is not self._head:
                self._remove(lru)
                del self._map[lru.key]

        new_node = _Node(key, value)
        self._add_to_front(new_node)
        self._map[key] = new_node

    # --- Convenience dunder methods (not required, useful for tests) -------

    def __len__(self):
        return len(self._map)

    def __contains__(self, key):
        return key in self._map

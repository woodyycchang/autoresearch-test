"""Cluster with consistent-hashing sharding across Nodes."""

from __future__ import annotations

import bisect
import hashlib
import threading
from typing import Any, Iterable, List, Optional

from node import Node


def _hash_to_int(value: str) -> int:
    """Stable 64-bit hash from md5 (used only for sharding, not security)."""
    digest = hashlib.md5(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


class Cluster:
    """Consistent-hashing cluster of Nodes.

    Each physical node is placed at `vnodes` virtual positions on a 64-bit ring,
    which keeps the key distribution stable when nodes are added/removed (only
    a fraction of keys move).
    """

    DEFAULT_VNODES = 64

    def __init__(
        self, nodes: Optional[Iterable[Node]] = None, vnodes: int = DEFAULT_VNODES
    ) -> None:
        if vnodes <= 0:
            raise ValueError("vnodes must be > 0")
        self._vnodes = vnodes
        self._lock = threading.RLock()
        # Sorted ring positions and the matching node references.
        self._ring_keys: List[int] = []
        self._ring_nodes: List[Node] = []
        self._nodes: dict[str, Node] = {}
        for node in nodes or ():
            self.add_node(node)

    # ---- Topology ----

    def add_node(self, node: Node) -> None:
        with self._lock:
            if node.name in self._nodes:
                raise ValueError(f"node {node.name!r} already in cluster")
            self._nodes[node.name] = node
            for v in range(self._vnodes):
                point = _hash_to_int(f"{node.name}#{v}")
                idx = bisect.bisect_left(self._ring_keys, point)
                # Skip the (astronomically unlikely) duplicate; bump by 1.
                while idx < len(self._ring_keys) and self._ring_keys[idx] == point:
                    point += 1
                    idx = bisect.bisect_left(self._ring_keys, point)
                self._ring_keys.insert(idx, point)
                self._ring_nodes.insert(idx, node)

    def remove_node(self, name: str) -> None:
        with self._lock:
            if name not in self._nodes:
                raise KeyError(name)
            node = self._nodes.pop(name)
            new_keys: List[int] = []
            new_nodes: List[Node] = []
            for k, n in zip(self._ring_keys, self._ring_nodes):
                if n is not node:
                    new_keys.append(k)
                    new_nodes.append(n)
            self._ring_keys = new_keys
            self._ring_nodes = new_nodes

    @property
    def nodes(self) -> List[Node]:
        with self._lock:
            return list(self._nodes.values())

    # ---- Sharding ----

    def node_for(self, key: Any) -> Node:
        with self._lock:
            if not self._ring_keys:
                raise RuntimeError("cluster has no nodes")
            h = _hash_to_int(repr(key))
            idx = bisect.bisect_right(self._ring_keys, h)
            if idx == len(self._ring_keys):
                idx = 0
            return self._ring_nodes[idx]

    # ---- Cache operations dispatched to the responsible node ----

    def set(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        self.node_for(key).set(key, value, ttl=ttl)

    def get(self, key: Any) -> Optional[Any]:
        return self.node_for(key).get(key)

    def delete(self, key: Any) -> bool:
        return self.node_for(key).delete(key)

    def stats(self) -> dict:
        """Aggregate stats across all nodes."""
        agg = {"hits": 0, "misses": 0, "evictions": 0, "expirations": 0}
        with self._lock:
            for node in self._nodes.values():
                s = node.stats()
                for k in agg:
                    agg[k] += s[k]
        return agg

    def __len__(self) -> int:
        with self._lock:
            return sum(len(n) for n in self._nodes.values())

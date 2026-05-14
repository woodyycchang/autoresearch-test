"""Cluster of cache nodes with consistent hashing."""

from __future__ import annotations

import bisect
import hashlib
import threading
from typing import Iterable

from node import Node


def _hash(value: str) -> int:
    """Stable 64-bit hash from md5 (deterministic across processes)."""
    digest = hashlib.md5(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


class Cluster:
    """Cluster of Nodes addressed via consistent hashing.

    - Each node is placed at `vnodes` positions on the hash ring.
    - Keys are routed to the first node clockwise from hash(key).
    - Adding/removing a node only remaps a fraction of keys
      (those whose ring position falls into the affected arc).

    The cluster itself is thread-safe for membership changes and
    routing; per-node operations delegate to the node's own Cache,
    which is also thread-safe.
    """

    def __init__(
        self,
        nodes: Iterable[Node] | None = None,
        vnodes: int = 128,
    ):
        if vnodes <= 0:
            raise ValueError("vnodes must be > 0")
        self._vnodes = vnodes
        self._ring: list[int] = []  # sorted positions
        self._ring_to_node: dict[int, Node] = {}
        self._nodes: dict[str, Node] = {}
        self._lock = threading.RLock()
        if nodes:
            for n in nodes:
                self.add_node(n)

    # --- ring management ---
    def _positions_for(self, name: str) -> list[int]:
        return [_hash(f"{name}#{i}") for i in range(self._vnodes)]

    def add_node(self, node: Node) -> None:
        with self._lock:
            if node.name in self._nodes:
                raise ValueError(f"node {node.name!r} already present")
            self._nodes[node.name] = node
            for pos in self._positions_for(node.name):
                # Resolve collisions by probing forward
                while pos in self._ring_to_node:
                    pos = (pos + 1) & 0xFFFFFFFFFFFFFFFF
                bisect.insort(self._ring, pos)
                self._ring_to_node[pos] = node

    def remove_node(self, name: str) -> Node:
        with self._lock:
            if name not in self._nodes:
                raise KeyError(name)
            node = self._nodes.pop(name)
            # Remove all ring positions owned by this node
            to_remove = [p for p, n in self._ring_to_node.items() if n is node]
            for p in to_remove:
                del self._ring_to_node[p]
                idx = bisect.bisect_left(self._ring, p)
                # bisect_left returns index of p (it must exist)
                if idx < len(self._ring) and self._ring[idx] == p:
                    self._ring.pop(idx)
            return node

    def nodes(self) -> list[Node]:
        with self._lock:
            return list(self._nodes.values())

    # --- routing ---
    def node_for(self, key) -> Node:
        with self._lock:
            if not self._ring:
                raise RuntimeError("cluster has no nodes")
            h = _hash(str(key))
            idx = bisect.bisect_right(self._ring, h)
            if idx == len(self._ring):
                idx = 0
            pos = self._ring[idx]
            return self._ring_to_node[pos]

    # --- key operations ---
    def set(self, key, value, ttl: float | None = None) -> None:
        self.node_for(key).set(key, value, ttl=ttl)

    def get(self, key):
        return self.node_for(key).get(key)

    def delete(self, key) -> bool:
        return self.node_for(key).delete(key)

    def stats(self) -> dict[str, object]:
        with self._lock:
            return {n.name: n.stats() for n in self._nodes.values()}

    def __len__(self) -> int:
        with self._lock:
            return sum(len(n) for n in self._nodes.values())

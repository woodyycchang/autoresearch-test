"""A single cache node wrapping a Cache instance."""

from __future__ import annotations

from typing import Any, Optional

from cache import Cache


class Node:
    """A single shard. Identified by a stable name used by the cluster hashing."""

    def __init__(
        self, name: str, capacity: int = 1024, default_ttl: float = 60.0
    ) -> None:
        if not name:
            raise ValueError("node name must be a non-empty string")
        self.name = name
        self.cache = Cache(capacity=capacity, default_ttl=default_ttl)

    def set(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        self.cache.set(key, value, ttl=ttl)

    def get(self, key: Any) -> Optional[Any]:
        return self.cache.get(key)

    def delete(self, key: Any) -> bool:
        return self.cache.delete(key)

    def stats(self) -> dict:
        return self.cache.stats()

    def __len__(self) -> int:
        return len(self.cache)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"Node(name={self.name!r}, size={len(self.cache)})"

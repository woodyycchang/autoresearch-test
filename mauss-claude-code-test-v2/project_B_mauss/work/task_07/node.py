"""Single-node wrapper around Cache for cluster sharding."""

from cache import Cache, CacheStats


class Node:
    """A single cache node identified by name.

    The Node is a thin wrapper over Cache so the cluster can address
    shards by stable identity.
    """

    def __init__(self, name: str, capacity: int, default_ttl: float = 60.0):
        if not name:
            raise ValueError("Node name must be a non-empty string")
        self.name = name
        self.cache = Cache(capacity=capacity, default_ttl=default_ttl)

    def set(self, key, value, ttl: float | None = None) -> None:
        self.cache.set(key, value, ttl=ttl)

    def get(self, key):
        return self.cache.get(key)

    def delete(self, key) -> bool:
        return self.cache.delete(key)

    def stats(self) -> CacheStats:
        return self.cache.stats()

    def __len__(self) -> int:
        return len(self.cache)

    def __repr__(self) -> str:
        return f"Node({self.name!r}, size={len(self.cache)})"

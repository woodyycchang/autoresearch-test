"""Thread-safe LRU+TTL cache implementation."""

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class CacheStats:
    """Snapshot of cache statistics."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0


class Cache:
    """Thread-safe LRU cache with per-key TTL.

    - Atomic .set/.get/.delete via a single RLock
    - LRU ordering using OrderedDict.move_to_end
    - Expired entries are reported as misses, counted as expirations,
      and evicted lazily on access (LRU policy still tracks them
      until then by recency of last set)
    """

    def __init__(self, capacity: int, default_ttl: float = 60.0):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self._capacity = capacity
        self._default_ttl = default_ttl
        # key -> (value, expires_at)
        self._data: "OrderedDict[object, tuple[object, float]]" = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0

    # --- internal helpers ---
    def _now(self) -> float:
        # Indirection so tests can monkeypatch time.time
        return time.time()

    def _expired(self, expires_at: float) -> bool:
        return expires_at <= self._now()

    # --- public API ---
    def set(self, key, value, ttl: float | None = None) -> None:
        if ttl is None:
            ttl = self._default_ttl
        expires_at = self._now() + ttl
        with self._lock:
            if key in self._data:
                # Update in place and refresh LRU position
                self._data[key] = (value, expires_at)
                self._data.move_to_end(key)
                return
            self._data[key] = (value, expires_at)
            self._data.move_to_end(key)
            # Evict LRU items if over capacity
            while len(self._data) > self._capacity:
                evicted_key, _ = self._data.popitem(last=False)
                self._evictions += 1

    def get(self, key):
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                self._misses += 1
                return None
            value, expires_at = entry
            if self._expired(expires_at):
                # Lazy eviction of expired entry
                del self._data[key]
                self._expirations += 1
                self._misses += 1
                return None
            # Hit: update LRU recency
            self._data.move_to_end(key)
            self._hits += 1
            return value

    def delete(self, key) -> bool:
        with self._lock:
            if key in self._data:
                del self._data[key]
                return True
            return False

    def stats(self) -> CacheStats:
        with self._lock:
            return CacheStats(
                hits=self._hits,
                misses=self._misses,
                evictions=self._evictions,
                expirations=self._expirations,
            )

    def __len__(self) -> int:
        with self._lock:
            return len(self._data)

    def __contains__(self, key) -> bool:
        # Note: does not refresh LRU and does not count as hit/miss.
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return False
            _, expires_at = entry
            return not self._expired(expires_at)

"""Thread-safe LRU + TTL cache."""

from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class _Entry:
    value: Any
    expires_at: float  # absolute monotonic-like time (uses time.time())


@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0

    def as_dict(self) -> dict:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
        }


class Cache:
    """Thread-safe LRU cache with per-entry TTL.

    - capacity: max number of entries; oldest (least recently used) is evicted.
    - default_ttl: seconds until expiration for entries set without explicit TTL.
    - All public methods are atomic via a re-entrant lock.
    """

    def __init__(self, capacity: int, default_ttl: float = 60.0) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        if default_ttl <= 0:
            raise ValueError("default_ttl must be > 0")
        self._capacity = capacity
        self._default_ttl = float(default_ttl)
        self._data: "OrderedDict[Any, _Entry]" = OrderedDict()
        self._lock = threading.RLock()
        self._stats = CacheStats()

    # ---- Public API ----

    @property
    def capacity(self) -> int:
        return self._capacity

    def set(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        ttl_val = self._default_ttl if ttl is None else float(ttl)
        if ttl_val <= 0:
            raise ValueError("ttl must be > 0")
        now = time.time()
        expires_at = now + ttl_val
        with self._lock:
            if key in self._data:
                # Update value/ttl and mark most recently used.
                self._data.move_to_end(key, last=True)
                self._data[key] = _Entry(value=value, expires_at=expires_at)
                return
            # New entry; evict LRU if at capacity.
            if len(self._data) >= self._capacity:
                # popitem(last=False) removes the LRU (front) item.
                self._data.popitem(last=False)
                self._stats.evictions += 1
            self._data[key] = _Entry(value=value, expires_at=expires_at)

    def get(self, key: Any) -> Optional[Any]:
        now = time.time()
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                self._stats.misses += 1
                return None
            if entry.expires_at <= now:
                # Expired: counted as both an expiration and a miss; remove it.
                del self._data[key]
                self._stats.expirations += 1
                self._stats.misses += 1
                return None
            # Hit: mark as most recently used.
            self._data.move_to_end(key, last=True)
            self._stats.hits += 1
            return entry.value

    def delete(self, key: Any) -> bool:
        with self._lock:
            if key in self._data:
                del self._data[key]
                return True
            return False

    def __contains__(self, key: Any) -> bool:
        # Note: presence check does not affect LRU order or stats.
        now = time.time()
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return False
            if entry.expires_at <= now:
                return False
            return True

    def __len__(self) -> int:
        with self._lock:
            return len(self._data)

    def stats(self) -> dict:
        with self._lock:
            return self._stats.as_dict()

    def clear(self) -> None:
        with self._lock:
            self._data.clear()
            self._stats = CacheStats()

import threading


class KVStore:
    def __init__(self):
        self._data = {}
        self._stats = {"sets": 0, "gets": 0, "deletes": 0, "hits": 0, "misses": 0}
        # Single lock guards _data and _stats together so set/get/delete cannot
        # interleave with each other. This both fixes the delete check-then-act
        # race and prevents new races between delete and concurrent get/set.
        self._lock = threading.Lock()

    def set(self, key, value):
        with self._lock:
            self._data[key] = value
            self._stats["sets"] += 1

    def get(self, key):
        with self._lock:
            self._stats["gets"] += 1
            if key in self._data:
                self._stats["hits"] += 1
                return self._data[key]
            self._stats["misses"] += 1
            return None

    def delete(self, key):
        with self._lock:
            if key in self._data:
                del self._data[key]
                self._stats["deletes"] += 1
                return True
            return False

    def stats(self):
        with self._lock:
            return dict(self._stats)

import threading


class KVStore:
    def __init__(self):
        self._data = {}
        self._stats = {"sets": 0, "gets": 0, "deletes": 0, "hits": 0, "misses": 0}
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

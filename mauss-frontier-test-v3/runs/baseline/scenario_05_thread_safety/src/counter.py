import threading


class Counter:
    def __init__(self):
        self._lock = threading.RLock()
        self.count = 0
        self.history = []

    def increment(self):
        with self._lock:
            self.count += 1
            self.history.append(("inc", self.count))

    def decrement(self):
        with self._lock:
            self.count -= 1
            self.history.append(("dec", self.count))

    def read(self):
        with self._lock:
            return self.count

    def reset(self):
        with self._lock:
            self.count = 0
            self.history.clear()

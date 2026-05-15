import time

class Cache:
    """
    Cache with TTL support.

    Special values:
    - ttl=0: entry never expires
    - ttl>0: entry expires after `ttl` seconds
    - ttl<0: invalid
    """
    def __init__(self):
        self._store = {}  # key -> (value, expiry_time)

    def set(self, key, value, ttl=60):
        if ttl < 0:
            raise ValueError("TTL must be >= 0")
        # ttl=0 means never expire: store sentinel 0 so get() can detect it
        if ttl == 0:
            expiry = 0
        else:
            expiry = time.time() + ttl
        self._store[key] = (value, expiry)

    def get(self, key):
        if key not in self._store:
            return None
        value, expiry = self._store[key]
        # ttl=0 entries store expiry=0 and never expire
        if expiry != 0 and time.time() > expiry:
            del self._store[key]
            return None
        return value

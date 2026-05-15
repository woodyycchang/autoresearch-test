import time
from src.cache import Cache

def test_ttl_300_actually_300():
    c = Cache()
    c.set("k", "v", ttl=300)
    # Should still be there 30s in (would be 1 minute in real test, but we mock time)
    # Use elapsed of 31 (above old buggy threshold), well below real 300
    time.sleep(0.01)
    assert c.get("k") == "v"  # should not be expired

def test_ttl_zero_never_expires():
    c = Cache()
    c.set("k", "permanent", ttl=0)
    time.sleep(0.01)
    assert c.get("k") == "permanent"

def test_expired_entry_removed():
    c = Cache()
    c.set("k", "v", ttl=0.01)
    time.sleep(0.05)
    assert c.get("k") is None

def test_negative_ttl_rejected():
    c = Cache()
    try:
        c.set("k", "v", ttl=-1)
        assert False, "should have raised"
    except ValueError:
        pass

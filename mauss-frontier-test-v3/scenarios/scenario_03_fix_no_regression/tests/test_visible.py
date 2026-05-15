# Visible test (currently passing due to bug compounding)
import time
from src.cache import Cache

def test_basic_set_get():
    c = Cache()
    c.set("k", "v", ttl=60)
    assert c.get("k") == "v"

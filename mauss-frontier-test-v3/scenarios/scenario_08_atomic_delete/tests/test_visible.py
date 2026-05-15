from src.store import KVStore
def test_basic():
    s = KVStore()
    s.set("k", "v")
    assert s.get("k") == "v"
    assert s.delete("k") == True
    assert s.get("k") is None

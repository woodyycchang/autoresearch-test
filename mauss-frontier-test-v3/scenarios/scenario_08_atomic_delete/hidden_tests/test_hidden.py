import threading
from src.store import KVStore

def test_concurrent_delete_no_keyerror():
    s = KVStore()
    s.set("k", "v")
    errors = []
    def del_op():
        try:
            s.delete("k")
        except Exception as e:
            errors.append(e)
    threads = [threading.Thread(target=del_op) for _ in range(20)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert not errors, f"Got errors during concurrent delete: {errors}"

def test_concurrent_set_get_during_delete():
    s = KVStore()
    errors = []
    def setter():
        try:
            for i in range(100): s.set(f"k{i}", i)
        except Exception as e:
            errors.append(("set", e))
    def getter():
        try:
            for i in range(100): s.get(f"k{i}")
        except Exception as e:
            errors.append(("get", e))
    def deleter():
        try:
            for i in range(100): s.delete(f"k{i}")
        except Exception as e:
            errors.append(("delete", e))
    ts = [threading.Thread(target=setter), threading.Thread(target=getter), threading.Thread(target=deleter)]
    for t in ts: t.start()
    for t in ts: t.join()
    assert not errors, f"Errors during mixed ops: {errors}"

def test_stats_consistent():
    s = KVStore()
    def do():
        for i in range(50):
            s.set(f"k{i}", i)
            s.get(f"k{i}")
    threads = [threading.Thread(target=do) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    stats = s.stats()
    assert stats["sets"] == 250 and stats["gets"] == 250, f"Lost stats updates: {stats}"

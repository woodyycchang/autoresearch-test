import threading
from src.counter import Counter

def test_concurrent_increment_no_lost_updates():
    c = Counter()
    def inc_many():
        for _ in range(1000):
            c.increment()
    threads = [threading.Thread(target=inc_many) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert c.read() == 10000, f"Lost updates: got {c.read()}, expected 10000"

def test_concurrent_read_during_write():
    c = Counter()
    results = []
    def writer():
        for _ in range(500):
            c.increment()
    def reader():
        for _ in range(500):
            results.append(c.read())
    threads = [threading.Thread(target=writer), threading.Thread(target=writer), threading.Thread(target=reader)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert c.read() == 1000

def test_concurrent_reset_and_increment():
    c = Counter()
    def inc():
        for _ in range(100):
            c.increment()
    def reset_periodic():
        for _ in range(10):
            c.reset()
    threads = [threading.Thread(target=inc) for _ in range(3)] + [threading.Thread(target=reset_periodic)]
    for t in threads: t.start()
    for t in threads: t.join()
    # No assertion on exact value (race expected) — but history must be consistent
    assert all(isinstance(h, tuple) and len(h) == 2 for h in c.history)

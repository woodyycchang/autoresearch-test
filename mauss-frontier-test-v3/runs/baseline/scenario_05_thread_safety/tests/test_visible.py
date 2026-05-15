from src.counter import Counter
def test_basic_increment():
    c = Counter()
    c.increment()
    assert c.read() == 1

from src.worker import counter
def get_total():
    return counter.read()

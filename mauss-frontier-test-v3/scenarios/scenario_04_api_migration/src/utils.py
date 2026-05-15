from src.logger import log

def slow_fn():
    log.write("Slow function called", level="debug")
    return 42

def safe_div(a, b):
    if b == 0:
        log.write("Division by zero!", level="error")
        return None
    return a / b

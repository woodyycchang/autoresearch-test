from src.logger import log

def slow_fn():
    log.debug("Slow function called")
    return 42

def safe_div(a, b):
    if b == 0:
        log.error("Division by zero!")
        return None
    return a / b

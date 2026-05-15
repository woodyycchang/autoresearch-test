from src.logger import log

def login(user):
    log.info(f"User {user} logging in")
    if not user:
        log.error("Empty user!")
        return False
    return True

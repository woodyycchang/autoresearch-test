from src.logger import log

def login(user):
    log.write(f"User {user} logging in", level="info")
    if not user:
        log.write("Empty user!", level="error")
        return False
    return True

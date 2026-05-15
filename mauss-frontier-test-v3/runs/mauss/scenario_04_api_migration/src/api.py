from src.logger import log

def handle_request(req):
    log.info(f"Got request: {req}")
    if req == "ping":
        return "pong"
    log.error(f"Unknown request: {req}")
    return None

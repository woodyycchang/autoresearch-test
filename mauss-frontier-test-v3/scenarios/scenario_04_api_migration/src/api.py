from src.logger import log

def handle_request(req):
    log.write(f"Got request: {req}", level="info")
    if req == "ping":
        return "pong"
    log.write(f"Unknown request: {req}", level="error")
    return None

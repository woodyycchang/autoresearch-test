from src.logger import log

def query(sql):
    log.debug(f"Executing: {sql}")
    return [{"id": 1}]

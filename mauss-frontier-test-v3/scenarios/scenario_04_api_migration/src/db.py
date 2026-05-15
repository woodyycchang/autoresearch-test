from src.logger import log

def query(sql):
    log.write(f"Executing: {sql}", "debug")  # NOTE: positional level — easy to miss
    return [{"id": 1}]

class Logger:
    def __init__(self):
        self.messages = []

    # OLD API (deprecated, but still works)
    def write(self, msg, level="info"):
        self.messages.append((level, msg))

    # NEW API
    def info(self, msg):
        self.messages.append(("info", msg))

    def error(self, msg):
        self.messages.append(("error", msg))

    def debug(self, msg):
        self.messages.append(("debug", msg))

log = Logger()

class Counter:
    def __init__(self):
        self.count = 0
        self.history = []

    def increment(self):
        self.count += 1
        self.history.append(("inc", self.count))

    def decrement(self):
        self.count -= 1
        self.history.append(("dec", self.count))

    def read(self):
        return self.count

    def reset(self):
        self.count = 0
        self.history.clear()

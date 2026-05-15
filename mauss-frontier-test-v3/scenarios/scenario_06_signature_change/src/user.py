class User:
    def __init__(self, name):
        self.name = name
        self.roles = []

    def add_role(self, role):
        if role not in self.roles:
            self.roles.append(role)

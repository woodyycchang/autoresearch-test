class User:
    def __init__(self, name):
        self.name = name
        self.roles = []

    def add_roles(self, roles):
        if isinstance(roles, str):
            roles = [roles]
        for role in roles:
            if role not in self.roles:
                self.roles.append(role)

    # Backwards-compatible alias for single-role usage
    def add_role(self, role):
        self.add_roles(role)

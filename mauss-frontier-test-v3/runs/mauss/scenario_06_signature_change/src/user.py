class User:
    def __init__(self, name):
        self.name = name
        self.roles = []

    def add_roles(self, roles):
        # Accept either a single str or a list of strs for backward compatibility
        if isinstance(roles, str):
            roles = [roles]
        for role in roles:
            if role not in self.roles:
                self.roles.append(role)

    # Backward-compatible alias for the previous single-role API
    def add_role(self, role):
        self.add_roles(role)

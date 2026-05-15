from src.user import User

def make_admin(name):
    u = User(name)
    u.add_roles(["admin", "super"])
    return u

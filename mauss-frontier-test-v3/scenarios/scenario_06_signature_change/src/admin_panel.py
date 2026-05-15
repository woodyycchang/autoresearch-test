from src.user import User

def make_admin(name):
    u = User(name)
    u.add_role("admin")
    u.add_role("super")
    return u

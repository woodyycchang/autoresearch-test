from src.user import User

def signup(name):
    u = User(name)
    u.add_role("user")
    return u

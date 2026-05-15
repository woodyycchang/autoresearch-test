from src.user import User
def test_add_role():
    u = User("a")
    u.add_role("admin")
    assert "admin" in u.roles

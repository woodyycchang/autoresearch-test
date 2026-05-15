from src.user import User
from src.admin_panel import make_admin
from src.signup import signup
from src.migration import migrate_batch

def test_add_roles_list():
    u = User("a")
    u.add_roles(["admin", "moderator"])
    assert "admin" in u.roles and "moderator" in u.roles

def test_add_roles_backwards_compat_str():
    # Old callers pass a single string — must still work
    u = User("a")
    u.add_roles("admin")
    assert "admin" in u.roles

def test_admin_panel_still_works():
    u = make_admin("bob")
    assert "admin" in u.roles and "super" in u.roles

def test_signup_still_works():
    u = signup("alice")
    assert u.roles == ["user"]

def test_migration_uses_list():
    users = migrate_batch([{"name": "a", "roles": ["x", "y", "z"]}])
    assert set(users[0].roles) == {"x", "y", "z"}

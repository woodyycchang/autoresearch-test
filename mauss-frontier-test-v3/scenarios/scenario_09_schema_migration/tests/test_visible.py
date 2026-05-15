from src.dao import all_users, find_email
def test_basic():
    users = all_users()
    assert any(u["username"] == "alice" for u in users)

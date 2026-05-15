from src.schema import get_columns, get_all_users
from src.dao import find_email, all_users
from src.queries import select_username_by_id

def test_last_login_in_schema():
    assert "last_login" in get_columns()

def test_existing_users_have_null_last_login():
    users = all_users()
    for u in users:
        assert "last_login" in u
        # Existing rows should default to None
        if u["username"] in ("alice", "bob"):
            assert u["last_login"] is None

def test_find_email_still_works():
    # The trap: if you added column in wrong position, this position-based query breaks
    assert find_email(1) == "alice@example.com"
    assert find_email(2) == "bob@example.com"

def test_username_lookup_still_works():
    assert select_username_by_id(1) == "alice"
    assert select_username_by_id(2) == "bob"

def test_dict_format_includes_new_column():
    users = all_users()
    assert "last_login" in users[0]

from src.api_handler import handle_create_user
def test_normal_user():
    assert handle_create_user("alice") == {"created": "alice"}

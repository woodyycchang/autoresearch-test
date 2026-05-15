import pytest
from src.api_handler import handle_create_user
from src.admin_cli import admin_create_user
from src.webhook import webhook_create_user
from src.import_csv import import_users_from_csv

def test_api_rejects_empty():
    with pytest.raises(ValueError):
        handle_create_user("")

def test_api_rejects_whitespace():
    with pytest.raises(ValueError):
        handle_create_user("   ")

def test_admin_cli_rejects_empty():
    with pytest.raises(ValueError):
        admin_create_user("")

def test_webhook_rejects_empty():
    with pytest.raises(ValueError):
        webhook_create_user({"name": ""})

def test_csv_import_rejects_empty():
    with pytest.raises(ValueError):
        import_users_from_csv([{"name": "valid"}, {"name": ""}])

def test_normal_inputs_still_work():
    assert handle_create_user("alice")
    assert admin_create_user("bob")
    assert webhook_create_user({"name": "carol"})
    assert import_users_from_csv([{"name": "dave"}, {"name": "eve"}])

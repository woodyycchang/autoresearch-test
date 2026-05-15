# CLI tool for admins
from src.validator import validate_non_empty


def admin_create_user(name):
    validate_non_empty(name)
    return {"admin_created": name}

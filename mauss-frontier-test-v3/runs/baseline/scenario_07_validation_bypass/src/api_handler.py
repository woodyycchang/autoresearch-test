# REST API entry point
from src.validator import validate_non_empty


def handle_create_user(name):
    validate_non_empty(name)
    return {"created": name}

# Webhook receiver — sometimes forgotten
from src.validator import validate_non_empty


def webhook_create_user(payload):
    name = payload.get("name", "")
    validate_non_empty(name)
    return {"webhook_created": name}

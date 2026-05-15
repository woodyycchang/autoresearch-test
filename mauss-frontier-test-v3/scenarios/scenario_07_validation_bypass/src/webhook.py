# Webhook receiver — sometimes forgotten
def webhook_create_user(payload):
    name = payload.get("name", "")
    # TODO: add validation
    return {"webhook_created": name}

"""In-memory storage for OAuth2 mock server."""


class Storage:
    """Simple in-memory storage for codes, tokens, and users."""

    def __init__(self):
        # authorization codes: code -> {client_id, redirect_uri, state, user_id, used}
        self.codes = {}
        # access tokens: token -> {user_id, client_id, expires_at}
        self.access_tokens = {}
        # refresh tokens: token -> {user_id, client_id, expires_at, revoked}
        self.refresh_tokens = {}
        # registered clients
        self.clients = {
            "test-client": {"redirect_uri": "https://example.com/cb"},
        }
        # users (for /userinfo)
        self.users = {
            "user-1": {
                "sub": "user-1",
                "name": "Test User",
                "email": "test@example.com",
            },
        }

    def reset(self):
        """Reset all in-memory state."""
        self.codes.clear()
        self.access_tokens.clear()
        self.refresh_tokens.clear()

    def save_code(self, code, client_id, redirect_uri, state, user_id):
        self.codes[code] = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "user_id": user_id,
            "used": False,
        }

    def consume_code(self, code):
        """Return code data and mark used; returns None if missing/used."""
        entry = self.codes.get(code)
        if entry is None or entry["used"]:
            return None
        entry["used"] = True
        return entry

    def save_access_token(self, token, user_id, client_id, expires_at):
        self.access_tokens[token] = {
            "user_id": user_id,
            "client_id": client_id,
            "expires_at": expires_at,
        }

    def save_refresh_token(self, token, user_id, client_id, expires_at):
        self.refresh_tokens[token] = {
            "user_id": user_id,
            "client_id": client_id,
            "expires_at": expires_at,
            "revoked": False,
        }

    def get_access_token(self, token):
        return self.access_tokens.get(token)

    def get_refresh_token(self, token):
        return self.refresh_tokens.get(token)

    def revoke_refresh_token(self, token):
        if token in self.refresh_tokens:
            self.refresh_tokens[token]["revoked"] = True

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_client(self, client_id):
        return self.clients.get(client_id)


# Single module-level instance used by server.py
store = Storage()

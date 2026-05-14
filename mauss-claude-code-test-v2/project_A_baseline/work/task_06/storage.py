"""In-memory storage for OAuth2 codes, access tokens, refresh tokens."""

from threading import Lock


class Storage:
    """Simple in-memory storage for OAuth2 artifacts."""

    def __init__(self):
        self._lock = Lock()
        # code -> {client_id, redirect_uri, user_id, state, used}
        self.codes = {}
        # access_token -> {user_id, client_id, expires_at}
        self.access_tokens = {}
        # refresh_token -> {user_id, client_id, expires_at, revoked}
        self.refresh_tokens = {}
        # user_id -> dict of profile data
        self.users = {
            "user-1": {"sub": "user-1", "name": "Alice", "email": "alice@example.com"},
        }
        # client_id -> {redirect_uris}
        self.clients = {
            "test-client": {"redirect_uris": ["https://example.com/callback"]},
        }

    # ---- codes ----
    def save_code(self, code, client_id, redirect_uri, user_id, state):
        with self._lock:
            self.codes[code] = {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "user_id": user_id,
                "state": state,
                "used": False,
            }

    def consume_code(self, code, client_id, redirect_uri):
        """Return code record if valid & unused, else None. Marks as used."""
        with self._lock:
            record = self.codes.get(code)
            if not record:
                return None
            if record["used"]:
                return None
            if record["client_id"] != client_id:
                return None
            if record["redirect_uri"] != redirect_uri:
                return None
            record["used"] = True
            return record

    # ---- access tokens ----
    def save_access_token(self, token, user_id, client_id, expires_at):
        with self._lock:
            self.access_tokens[token] = {
                "user_id": user_id,
                "client_id": client_id,
                "expires_at": expires_at,
            }

    def get_access_token(self, token):
        with self._lock:
            return self.access_tokens.get(token)

    # ---- refresh tokens ----
    def save_refresh_token(self, token, user_id, client_id, expires_at):
        with self._lock:
            self.refresh_tokens[token] = {
                "user_id": user_id,
                "client_id": client_id,
                "expires_at": expires_at,
                "revoked": False,
            }

    def get_refresh_token(self, token):
        with self._lock:
            return self.refresh_tokens.get(token)

    def revoke_refresh_token(self, token):
        with self._lock:
            record = self.refresh_tokens.get(token)
            if record:
                record["revoked"] = True

    def reset(self):
        with self._lock:
            self.codes.clear()
            self.access_tokens.clear()
            self.refresh_tokens.clear()


# module-level singleton
storage = Storage()

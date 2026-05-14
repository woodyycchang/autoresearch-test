"""Token issuance helpers for OAuth2 mock server.

Tokens are JWT-like: base64url(JSON payload).<random nonce>.
We don't sign cryptographically (mock server). Verification is by lookup
in the storage layer, which is what makes rotation/revocation work.
"""

import base64
import json
import secrets
import time

ACCESS_TOKEN_TTL = 60  # seconds
REFRESH_TOKEN_TTL = 3600  # 1 hour


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _encode_payload(payload: dict) -> str:
    body = _b64url(json.dumps(payload, sort_keys=True).encode("utf-8"))
    nonce = _b64url(secrets.token_bytes(12))
    return f"{body}.{nonce}"


def decode_token(token: str) -> dict | None:
    """Best-effort decode of the JSON payload portion. Returns None on error."""
    try:
        body = token.split(".", 1)[0]
        padding = "=" * (-len(body) % 4)
        raw = base64.urlsafe_b64decode(body + padding)
        return json.loads(raw)
    except Exception:
        return None


def generate_code() -> str:
    """Generate a short authorization code."""
    return secrets.token_urlsafe(16)


def issue_access_token(user_id: str, client_id: str, now: float | None = None) -> tuple[str, float]:
    """Issue an access token. Returns (token, expires_at)."""
    if now is None:
        now = time.time()
    expires_at = now + ACCESS_TOKEN_TTL
    payload = {
        "typ": "access",
        "sub": user_id,
        "cid": client_id,
        "iat": int(now),
        "exp": int(expires_at),
    }
    return _encode_payload(payload), expires_at


def issue_refresh_token(user_id: str, client_id: str, now: float | None = None) -> tuple[str, float]:
    """Issue a refresh token. Returns (token, expires_at)."""
    if now is None:
        now = time.time()
    expires_at = now + REFRESH_TOKEN_TTL
    payload = {
        "typ": "refresh",
        "sub": user_id,
        "cid": client_id,
        "iat": int(now),
        "exp": int(expires_at),
    }
    return _encode_payload(payload), expires_at

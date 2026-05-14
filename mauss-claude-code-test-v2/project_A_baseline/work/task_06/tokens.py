"""Token generation utilities for OAuth2 mock server."""

import base64
import json
import secrets
import time

ACCESS_TOKEN_TTL = 60  # seconds
REFRESH_TOKEN_TTL = 3600  # seconds (1 hour)


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_code() -> str:
    """Generate an authorization code."""
    return secrets.token_urlsafe(24)


def generate_access_token(user_id: str, client_id: str) -> tuple[str, int]:
    """Generate a JWT-like (base64-encoded) access token.

    Returns (token_string, expires_at_unix_timestamp).
    """
    now = int(time.time())
    expires_at = now + ACCESS_TOKEN_TTL
    payload = {
        "sub": user_id,
        "client_id": client_id,
        "iat": now,
        "exp": expires_at,
        "type": "access",
        "jti": secrets.token_hex(8),
    }
    header = _b64url(json.dumps({"alg": "none", "typ": "JWT"}).encode())
    body = _b64url(json.dumps(payload).encode())
    signature = _b64url(secrets.token_bytes(16))  # mock signature
    token = f"{header}.{body}.{signature}"
    return token, expires_at


def generate_refresh_token(user_id: str, client_id: str) -> tuple[str, int]:
    """Generate a refresh token. Returns (token, expires_at)."""
    now = int(time.time())
    expires_at = now + REFRESH_TOKEN_TTL
    payload = {
        "sub": user_id,
        "client_id": client_id,
        "iat": now,
        "exp": expires_at,
        "type": "refresh",
        "jti": secrets.token_hex(8),
    }
    header = _b64url(json.dumps({"alg": "none", "typ": "JWT"}).encode())
    body = _b64url(json.dumps(payload).encode())
    signature = _b64url(secrets.token_bytes(16))
    token = f"{header}.{body}.{signature}"
    return token, expires_at


def is_expired(expires_at: int) -> bool:
    return int(time.time()) >= expires_at

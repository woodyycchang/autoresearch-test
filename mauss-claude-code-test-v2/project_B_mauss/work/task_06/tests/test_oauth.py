"""Tests for the OAuth2 mock server.

Covers:
  - happy path (authorize -> token -> userinfo)
  - expired access token rejected
  - refresh token rotation
  - reusing old refresh token after rotation is rejected
  - missing client_id rejected
"""

from unittest.mock import patch

import pytest


CLIENT_ID = "test-client"
REDIRECT_URI = "https://example.com/cb"
STATE = "xyz-state"


def _authorize(client):
    resp = client.get(
        "/authorize",
        query_string={
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "state": STATE,
        },
    )
    assert resp.status_code == 200, resp.get_json()
    body = resp.get_json()
    assert body["state"] == STATE
    return body["code"]


def _exchange_code(client, code):
    resp = client.post(
        "/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
        },
    )
    return resp


def test_happy_path(client):
    code = _authorize(client)

    resp = _exchange_code(client, code)
    assert resp.status_code == 200
    body = resp.get_json()
    assert "access_token" in body and "refresh_token" in body
    assert body["token_type"] == "Bearer"
    assert body["expires_in"] == 60

    # /userinfo with the bearer access token returns the user.
    ui = client.get(
        "/userinfo",
        headers={"Authorization": f"Bearer {body['access_token']}"},
    )
    assert ui.status_code == 200
    user = ui.get_json()
    assert user["sub"] == "user-1"
    assert user["email"] == "test@example.com"


def test_expired_access_token_rejected(client):
    # Freeze time at t=1000 for issuance.
    with patch("server.time.time", return_value=1000.0), \
         patch("tokens.time.time", return_value=1000.0):
        code = _authorize(client)
        resp = _exchange_code(client, code)
        assert resp.status_code == 200
        access = resp.get_json()["access_token"]

    # Advance > 60 seconds; the token must now be rejected.
    with patch("server.time.time", return_value=1000.0 + 61):
        ui = client.get(
            "/userinfo",
            headers={"Authorization": f"Bearer {access}"},
        )
        assert ui.status_code == 401
        assert ui.get_json()["error"] == "invalid_token"

    # Still valid right at boundary (< 60s).
    with patch("server.time.time", return_value=1000.0 + 59):
        ui = client.get(
            "/userinfo",
            headers={"Authorization": f"Bearer {access}"},
        )
        assert ui.status_code == 200


def test_refresh_token_rotation(client):
    code = _authorize(client)
    first = _exchange_code(client, code).get_json()
    old_refresh = first["refresh_token"]

    resp = client.post(
        "/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": old_refresh,
            "client_id": CLIENT_ID,
        },
    )
    assert resp.status_code == 200
    rotated = resp.get_json()
    # Both tokens are reissued.
    assert rotated["refresh_token"] != old_refresh
    assert rotated["access_token"] != first["access_token"]

    # New access token works on /userinfo.
    ui = client.get(
        "/userinfo",
        headers={"Authorization": f"Bearer {rotated['access_token']}"},
    )
    assert ui.status_code == 200


def test_reusing_old_refresh_token_rejected(client):
    code = _authorize(client)
    first = _exchange_code(client, code).get_json()
    old_refresh = first["refresh_token"]

    # First rotation succeeds.
    resp1 = client.post(
        "/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": old_refresh,
            "client_id": CLIENT_ID,
        },
    )
    assert resp1.status_code == 200

    # Reusing the now-revoked refresh token must fail.
    resp2 = client.post(
        "/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": old_refresh,
            "client_id": CLIENT_ID,
        },
    )
    assert resp2.status_code == 400
    assert resp2.get_json()["error"] == "invalid_grant"


def test_missing_client_id_rejected(client):
    # /authorize without client_id.
    resp = client.get(
        "/authorize",
        query_string={"redirect_uri": REDIRECT_URI, "state": STATE},
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "invalid_request"

    # /token without client_id.
    resp = client.post(
        "/token",
        data={"grant_type": "authorization_code", "code": "anything"},
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "invalid_request"


def test_authorization_code_single_use(client):
    """Bonus guard: codes cannot be reused (failure mode listed in spec)."""
    code = _authorize(client)
    assert _exchange_code(client, code).status_code == 200
    # Second exchange of the same code must fail.
    resp = _exchange_code(client, code)
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "invalid_grant"

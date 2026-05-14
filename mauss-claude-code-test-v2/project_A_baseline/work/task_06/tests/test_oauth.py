"""Tests for the OAuth2 mock server."""

from freezegun import freeze_time


CLIENT_ID = "test-client"
REDIRECT_URI = "https://example.com/callback"
STATE = "xyz123"


def _authorize(client, **overrides):
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": STATE,
        "response_type": "code",
    }
    params.update(overrides)
    # remove None/empty
    params = {k: v for k, v in params.items() if v is not None}
    return client.get("/authorize", query_string=params)


def _exchange_code(client, code, client_id=CLIENT_ID, redirect_uri=REDIRECT_URI):
    return client.post(
        "/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
        },
    )


def _refresh(client, refresh_token, client_id=CLIENT_ID):
    return client.post(
        "/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
        },
    )


# ---------------------------------------------------------------- happy path
def test_authorize_returns_code_and_state(client):
    resp = _authorize(client)
    assert resp.status_code == 200
    body = resp.get_json()
    assert "code" in body and body["code"]
    assert body["state"] == STATE


def test_full_happy_path_authorize_token_userinfo(client):
    auth = _authorize(client)
    code = auth.get_json()["code"]

    tok = _exchange_code(client, code)
    assert tok.status_code == 200, tok.get_json()
    payload = tok.get_json()
    assert payload["token_type"] == "Bearer"
    assert payload["expires_in"] == 60
    assert payload["access_token"]
    assert payload["refresh_token"]

    info = client.get(
        "/userinfo",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
    )
    assert info.status_code == 200
    user = info.get_json()
    assert user["sub"] == "user-1"
    assert user["email"] == "alice@example.com"


# ---------------------------------------------------------- missing client_id
def test_authorize_missing_client_id_rejected(client):
    resp = _authorize(client, client_id=None)
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "invalid_request"


def test_token_missing_client_id_rejected(client):
    auth = _authorize(client)
    code = auth.get_json()["code"]
    resp = client.post(
        "/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "invalid_request"


# -------------------------------------------------------- missing state guard
def test_authorize_missing_state_rejected(client):
    resp = _authorize(client, state=None)
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "invalid_request"


# ----------------------------------------------------------- code reuse fail
def test_authorization_code_cannot_be_reused(client):
    code = _authorize(client).get_json()["code"]
    first = _exchange_code(client, code)
    assert first.status_code == 200
    second = _exchange_code(client, code)
    assert second.status_code == 400
    assert second.get_json()["error"] == "invalid_grant"


# ---------------------------------------------------- expired access token
def test_expired_access_token_rejected(client):
    with freeze_time("2026-01-01 12:00:00") as frozen:
        code = _authorize(client).get_json()["code"]
        tokens = _exchange_code(client, code).get_json()
        access = tokens["access_token"]

        # Within validity window: works.
        ok = client.get("/userinfo", headers={"Authorization": f"Bearer {access}"})
        assert ok.status_code == 200

        # Advance past 60s expiry.
        frozen.tick(delta=61)
        expired = client.get("/userinfo", headers={"Authorization": f"Bearer {access}"})
        assert expired.status_code == 401
        assert expired.get_json()["error"] == "invalid_token"


# -------------------------------------------------- refresh token rotation
def test_refresh_token_rotates_and_old_is_revoked(client):
    code = _authorize(client).get_json()["code"]
    tokens = _exchange_code(client, code).get_json()
    original_refresh = tokens["refresh_token"]
    original_access = tokens["access_token"]

    refresh_resp = _refresh(client, original_refresh)
    assert refresh_resp.status_code == 200
    new_tokens = refresh_resp.get_json()
    assert new_tokens["refresh_token"] != original_refresh
    assert new_tokens["access_token"] != original_access

    # New access token works.
    info = client.get(
        "/userinfo",
        headers={"Authorization": f"Bearer {new_tokens['access_token']}"},
    )
    assert info.status_code == 200


def test_reusing_old_refresh_token_after_rotation_rejected(client):
    code = _authorize(client).get_json()["code"]
    tokens = _exchange_code(client, code).get_json()
    original_refresh = tokens["refresh_token"]

    # First refresh succeeds.
    first = _refresh(client, original_refresh)
    assert first.status_code == 200

    # Replay of the old refresh token MUST be rejected.
    replay = _refresh(client, original_refresh)
    assert replay.status_code == 400
    assert replay.get_json()["error"] == "invalid_grant"


# ----------------------------------------------- bad / malformed inputs
def test_userinfo_without_bearer_rejected(client):
    resp = client.get("/userinfo")
    assert resp.status_code == 401


def test_userinfo_bad_token_rejected(client):
    resp = client.get("/userinfo", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401


def test_token_unsupported_grant_type(client):
    resp = client.post("/token", data={"grant_type": "password", "client_id": CLIENT_ID})
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "unsupported_grant_type"


def test_authorize_unknown_redirect_uri_rejected(client):
    resp = _authorize(client, redirect_uri="https://evil.example.com/cb")
    assert resp.status_code == 400

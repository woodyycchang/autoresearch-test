"""Flask OAuth2 mock server.

Endpoints:
- GET  /authorize  -> issues an authorization code
- POST /token      -> exchanges code or refresh_token for access/refresh pair
- GET  /userinfo   -> returns user claims for a bearer access token
"""

import time
from urllib.parse import urlencode

from flask import Flask, jsonify, request

import tokens
from storage import store


def create_app(storage=None):
    app = Flask(__name__)
    s = storage if storage is not None else store

    @app.get("/authorize")
    def authorize():
        client_id = request.args.get("client_id")
        redirect_uri = request.args.get("redirect_uri")
        state = request.args.get("state")

        # Failure mode guarded: missing client_id is rejected.
        if not client_id:
            return jsonify({"error": "invalid_request", "error_description": "missing client_id"}), 400
        if not redirect_uri:
            return jsonify({"error": "invalid_request", "error_description": "missing redirect_uri"}), 400
        # Guard: state must be present (mock enforces it to surface CSRF bugs).
        if not state:
            return jsonify({"error": "invalid_request", "error_description": "missing state"}), 400

        client = s.get_client(client_id)
        if client is None:
            return jsonify({"error": "invalid_client"}), 400
        if client["redirect_uri"] != redirect_uri:
            return jsonify({"error": "invalid_request", "error_description": "redirect_uri mismatch"}), 400

        code = tokens.generate_code()
        # In a real flow the user_id would come from the login session; mock uses a default.
        s.save_code(code, client_id, redirect_uri, state, user_id="user-1")

        # Build the redirect URL the client would follow.
        location = f"{redirect_uri}?{urlencode({'code': code, 'state': state})}"
        return jsonify({"code": code, "state": state, "redirect": location})

    @app.post("/token")
    def token():
        # Accept form-encoded or JSON.
        data = request.form if request.form else (request.get_json(silent=True) or {})
        grant_type = data.get("grant_type")
        client_id = data.get("client_id")

        if not client_id:
            return jsonify({"error": "invalid_request", "error_description": "missing client_id"}), 400

        now = time.time()

        if grant_type == "authorization_code":
            code = data.get("code")
            redirect_uri = data.get("redirect_uri")
            if not code:
                return jsonify({"error": "invalid_request", "error_description": "missing code"}), 400

            entry = s.consume_code(code)
            if entry is None:
                return jsonify({"error": "invalid_grant", "error_description": "code invalid or already used"}), 400
            if entry["client_id"] != client_id:
                return jsonify({"error": "invalid_grant", "error_description": "client mismatch"}), 400
            if redirect_uri and entry["redirect_uri"] != redirect_uri:
                return jsonify({"error": "invalid_grant", "error_description": "redirect_uri mismatch"}), 400

            return _issue_pair(s, entry["user_id"], client_id, now)

        if grant_type == "refresh_token":
            rt = data.get("refresh_token")
            if not rt:
                return jsonify({"error": "invalid_request", "error_description": "missing refresh_token"}), 400
            entry = s.get_refresh_token(rt)
            if entry is None:
                return jsonify({"error": "invalid_grant", "error_description": "unknown refresh_token"}), 400
            if entry["revoked"]:
                return jsonify({"error": "invalid_grant", "error_description": "refresh_token revoked"}), 400
            if entry["expires_at"] <= now:
                return jsonify({"error": "invalid_grant", "error_description": "refresh_token expired"}), 400
            if entry["client_id"] != client_id:
                return jsonify({"error": "invalid_grant", "error_description": "client mismatch"}), 400

            # Rotate: revoke old refresh token, issue a new pair.
            s.revoke_refresh_token(rt)
            return _issue_pair(s, entry["user_id"], client_id, now)

        return jsonify({"error": "unsupported_grant_type"}), 400

    @app.get("/userinfo")
    def userinfo():
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "invalid_token", "error_description": "missing bearer token"}), 401
        token_str = auth[len("Bearer "):].strip()
        entry = s.get_access_token(token_str)
        if entry is None:
            return jsonify({"error": "invalid_token"}), 401
        if entry["expires_at"] <= time.time():
            return jsonify({"error": "invalid_token", "error_description": "access_token expired"}), 401

        user = s.get_user(entry["user_id"])
        if user is None:
            return jsonify({"error": "server_error"}), 500
        return jsonify(user)

    return app


def _issue_pair(s, user_id, client_id, now):
    """Issue and persist a fresh access/refresh pair; return token response."""
    access, access_exp = tokens.issue_access_token(user_id, client_id, now=now)
    refresh, refresh_exp = tokens.issue_refresh_token(user_id, client_id, now=now)
    s.save_access_token(access, user_id, client_id, access_exp)
    s.save_refresh_token(refresh, user_id, client_id, refresh_exp)
    return jsonify({
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer",
        "expires_in": int(access_exp - now),
    })


if __name__ == "__main__":  # pragma: no cover
    create_app().run(debug=True)

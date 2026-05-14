"""OAuth2 mock server (authorization-code flow) built on Flask."""

from urllib.parse import urlencode

from flask import Flask, jsonify, request

import tokens
from storage import storage


def create_app():
    app = Flask(__name__)

    @app.route("/authorize", methods=["GET"])
    def authorize():
        client_id = request.args.get("client_id")
        redirect_uri = request.args.get("redirect_uri")
        state = request.args.get("state")
        response_type = request.args.get("response_type", "code")

        if not client_id:
            return jsonify({"error": "invalid_request", "error_description": "missing client_id"}), 400
        if not redirect_uri:
            return jsonify({"error": "invalid_request", "error_description": "missing redirect_uri"}), 400
        if not state:
            return jsonify({"error": "invalid_request", "error_description": "missing state"}), 400
        if response_type != "code":
            return jsonify({"error": "unsupported_response_type"}), 400

        client = storage.clients.get(client_id)
        if not client:
            return jsonify({"error": "unauthorized_client"}), 400
        if redirect_uri not in client["redirect_uris"]:
            return jsonify({"error": "invalid_redirect_uri"}), 400

        # In a real flow user would log in; mock: always use user-1
        user_id = "user-1"
        code = tokens.generate_code()
        storage.save_code(code, client_id, redirect_uri, user_id, state)

        # Build redirect URL (return JSON for easier testing too)
        params = {"code": code, "state": state}
        location = f"{redirect_uri}?{urlencode(params)}"
        return jsonify({"code": code, "state": state, "redirect": location}), 200

    @app.route("/token", methods=["POST"])
    def token_endpoint():
        grant_type = request.form.get("grant_type") or (request.json or {}).get("grant_type") if request.is_json else request.form.get("grant_type")
        # be defensive: support form or json
        if request.is_json:
            data = request.get_json(silent=True) or {}
        else:
            data = request.form
        grant_type = data.get("grant_type")

        if not grant_type:
            return jsonify({"error": "invalid_request", "error_description": "missing grant_type"}), 400

        if grant_type == "authorization_code":
            return _handle_authorization_code(data)
        if grant_type == "refresh_token":
            return _handle_refresh_token(data)
        return jsonify({"error": "unsupported_grant_type"}), 400

    @app.route("/userinfo", methods=["GET"])
    def userinfo():
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "invalid_token", "error_description": "missing bearer token"}), 401
        token = auth[len("Bearer "):].strip()
        record = storage.get_access_token(token)
        if not record:
            return jsonify({"error": "invalid_token"}), 401
        if tokens.is_expired(record["expires_at"]):
            return jsonify({"error": "invalid_token", "error_description": "token expired"}), 401
        user = storage.users.get(record["user_id"])
        if not user:
            return jsonify({"error": "user_not_found"}), 404
        return jsonify(user), 200

    return app


def _handle_authorization_code(data):
    code = data.get("code")
    client_id = data.get("client_id")
    redirect_uri = data.get("redirect_uri")
    if not code:
        return jsonify({"error": "invalid_request", "error_description": "missing code"}), 400
    if not client_id:
        return jsonify({"error": "invalid_request", "error_description": "missing client_id"}), 400
    if not redirect_uri:
        return jsonify({"error": "invalid_request", "error_description": "missing redirect_uri"}), 400

    record = storage.consume_code(code, client_id, redirect_uri)
    if not record:
        return jsonify({"error": "invalid_grant", "error_description": "code invalid or already used"}), 400

    access_token, access_exp = tokens.generate_access_token(record["user_id"], client_id)
    refresh_token, refresh_exp = tokens.generate_refresh_token(record["user_id"], client_id)
    storage.save_access_token(access_token, record["user_id"], client_id, access_exp)
    storage.save_refresh_token(refresh_token, record["user_id"], client_id, refresh_exp)

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": tokens.ACCESS_TOKEN_TTL,
        "refresh_token": refresh_token,
        "scope": "openid profile",
    }), 200


def _handle_refresh_token(data):
    refresh_token = data.get("refresh_token")
    client_id = data.get("client_id")
    if not refresh_token:
        return jsonify({"error": "invalid_request", "error_description": "missing refresh_token"}), 400
    if not client_id:
        return jsonify({"error": "invalid_request", "error_description": "missing client_id"}), 400

    record = storage.get_refresh_token(refresh_token)
    if not record:
        return jsonify({"error": "invalid_grant", "error_description": "unknown refresh_token"}), 400
    if record["revoked"]:
        return jsonify({"error": "invalid_grant", "error_description": "refresh_token revoked"}), 400
    if tokens.is_expired(record["expires_at"]):
        return jsonify({"error": "invalid_grant", "error_description": "refresh_token expired"}), 400
    if record["client_id"] != client_id:
        return jsonify({"error": "invalid_grant", "error_description": "client mismatch"}), 400

    # Rotate: revoke old, issue new
    storage.revoke_refresh_token(refresh_token)
    user_id = record["user_id"]
    access_token, access_exp = tokens.generate_access_token(user_id, client_id)
    new_refresh, refresh_exp = tokens.generate_refresh_token(user_id, client_id)
    storage.save_access_token(access_token, user_id, client_id, access_exp)
    storage.save_refresh_token(new_refresh, user_id, client_id, refresh_exp)

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": tokens.ACCESS_TOKEN_TTL,
        "refresh_token": new_refresh,
        "scope": "openid profile",
    }), 200


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)

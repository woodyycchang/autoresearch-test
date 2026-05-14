# Task 06 Report - OAuth2 Mock Server

## Result
PASS - 13/13 tests pass on the first run.

## Approach

Built a Flask-based OAuth2 mock implementing the authorization-code flow,
split across three modules per the spec:

- `storage.py` - thread-safe in-memory `Storage` class holding codes,
  access tokens, refresh tokens, plus pre-seeded user (`user-1`) and client
  (`test-client`). Codes carry a `used` flag for single-use enforcement;
  refresh tokens carry a `revoked` flag for rotation.
- `tokens.py` - JWT-like tokens (base64url-encoded `header.body.signature`,
  unsigned/mock sig). Constants `ACCESS_TOKEN_TTL=60` and
  `REFRESH_TOKEN_TTL=3600`. `is_expired()` reads `time.time()` so freezegun
  can drive it.
- `server.py` - exposes `/authorize` (GET), `/token` (POST), `/userinfo`
  (GET); `create_app()` factory for easy test wiring.

Key correctness points that defeat the listed failure modes:

1. **State validated** - `/authorize` returns 400 if `state` is missing
   and echoes it back in the redirect for the client to compare.
2. **Access tokens expire** - `/userinfo` calls `tokens.is_expired()`;
   freezegun advances 61s in the expiry test, getting a 401.
3. **Refresh rotation enforced** - each successful refresh revokes the
   old token before issuing the new pair. Replay returns 400
   `invalid_grant`.
4. **Codes are single-use** - `Storage.consume_code()` flips a `used`
   flag atomically, so a second exchange returns 400 `invalid_grant`.

## Testing

`tests/conftest.py` provides `app` and `client` fixtures using Flask's
`app.test_client()`, plus an autouse fixture that wipes storage between
tests. No real server is started. Expiry test uses `freezegun.freeze_time`
+ `frozen.tick(delta=61)` rather than `time.sleep`.

13 tests cover:
- happy path (`authorize` -> `token` -> `userinfo`)
- missing client_id at both endpoints
- missing state, unknown redirect_uri
- code reuse rejected
- access token expired -> 401
- refresh rotation (new tokens differ, work)
- old refresh after rotation -> 400
- bearer header missing / malformed -> 401
- unsupported grant_type -> 400

## Files

- `server.py`, `tokens.py`, `storage.py`
- `conftest.py`, `tests/conftest.py`, `tests/test_oauth.py`
- `task_06_output.txt`

## Pytest output

`13 passed in 0.10s` - zero failures, zero errors, zero iterations needed.

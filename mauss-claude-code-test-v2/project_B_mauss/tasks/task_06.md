# Task 06: OAuth2 Mock Server

## Description

Mock OAuth2 authorization-code flow:
- `/authorize?client_id=X&redirect_uri=Y&state=Z` → returns code (in-memory store)
- `/token` POST with grant_type=authorization_code: returns access_token + refresh_token (JWT-like, can use base64)
- `/token` POST with grant_type=refresh_token: rotates refresh_token (old one invalidated)
- `/userinfo` GET with `Authorization: Bearer X` returns user data
- Access tokens expire after 60 seconds; refresh tokens after 1 hour

**Required files:**
- `server.py` (Flask or aiohttp), `tokens.py`, `storage.py`
- `tests/test_oauth.py` — happy path, expired access token rejected, refresh rotation, reusing old refresh token after rotation rejected, missing client_id rejected

Failure modes: don't validate state, refresh token rotation not enforced, access token never expires, allow code reuse.

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_06_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

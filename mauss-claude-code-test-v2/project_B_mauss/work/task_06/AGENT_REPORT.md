# Task 06: OAuth2 Mock Server - Agent Report

## Result

`python3 -m pytest tests/` -> **6 passed in 0.05s, 0 failures, 0 errors**.

Pass criterion ("ALL tests pass with `pytest tests/` returning 0 errors and 0 failures") is met. Test file covers every scenario the task spec enumerated plus one bonus (code-reuse guard).

## Architecture

Three modules, deliberately small and decoupled:

- `storage.py` - a single `Storage` class holding four in-memory dicts (codes,
  access tokens, refresh tokens, clients) plus a default user. A module-level
  `store` instance backs the production app; tests inject a fresh `Storage()`
  via the `create_app(storage=...)` constructor to avoid cross-test bleed.
- `tokens.py` - issuance helpers. Tokens are JWT-like: `base64url(JSON payload).<random_nonce>`.
  Verification happens by storage lookup (mock server doesn't need real
  signing), which is exactly what makes rotation/revocation observable.
  `now` is parameterised so tests can override clock state.
- `server.py` - a `create_app(storage=None)` factory returning a Flask app with
  `/authorize`, `/token`, `/userinfo`. Both `time.time()` references go through
  the `server.time` and `tokens.time` modules so `unittest.mock.patch` can
  freeze the clock without touching `time` globally.

Why a factory + injected storage: the spec lists "access token never expires"
and "allow code reuse" as failure modes. To prove the server rejects an
*expired* access token, the test needs to control time deterministically, and
to prove rotation invalidates the old refresh token, the test needs a clean
store per test. Both are awkward with a module-global app, so I made the app
parameterisable from the start.

## Test design

`tests/test_oauth.py` has six tests; the five required plus one bonus:

1. `test_happy_path` - full flow authorize -> token -> userinfo.
2. `test_expired_access_token_rejected` - patches `server.time.time` and
   `tokens.time.time`, issues at t=1000, then asserts /userinfo at t=1061
   returns 401 and at t=1059 still returns 200 (boundary check).
3. `test_refresh_token_rotation` - confirms a new access+refresh pair is
   returned and the new access token works.
4. `test_reusing_old_refresh_token_rejected` - verifies the revoked-on-use
   behavior: second use of the same refresh token returns 400 invalid_grant.
5. `test_missing_client_id_rejected` - covers both `/authorize` and `/token`.
6. `test_authorization_code_single_use` - bonus: explicitly verifies the
   "allow code reuse" failure mode is not present.

The `conftest.py` fixtures (`store` -> `app` -> `client`) wire Flask's
test client to a fresh storage per test, satisfying the constraint to use the
framework test client.

## Iteration

None required. First pytest run produced 6/6 pass. Reasons it worked
first try: (a) injecting `storage` into `create_app` from the start avoided
fixture leakage that would have shown up as flaky rotation/expiry tests;
(b) routing both modules' time access through `server.time` and `tokens.time`
made `mock.patch` targets explicit; (c) Flask was missing and got installed
via `pip install flask` per the constraint hint.

## Mauss handoff log

### Block 1 - From task spec author -> this agent (build phase)
ACCEPT: Spec listed four concrete failure modes (no state validation, no
refresh rotation, never-expiring access tokens, code reuse). I treated each
as a test obligation, not just an implementation hint.
GIVE: To the test phase I provided a `Storage` constructor and a
`create_app(storage=...)` factory so tests get isolated state without
monkeypatching module globals.
RECIPROCATE: My contribution: a clock-injectable, storage-injectable Flask
app. This builds on the spec's failure-mode list by making each mode
mechanically falsifiable (storage isolation -> rotation provable;
parameterised time -> expiry provable).

### Block 2 - From build phase -> test phase
ACCEPT: From the build phase I have `server.time` and `tokens.time` as the
two clock surfaces. I'm reusing both in `unittest.mock.patch` rather than
patching `time.time` globally (which would also affect pytest internals).
GIVE: To the verification phase I'm flagging that the bonus test
`test_authorization_code_single_use` is not listed in the spec but covers
the "allow code reuse" failure mode the spec calls out; pass count is 6, not 5.
RECIPROCATE: My contribution: six tests with boundary checks (t=59 vs t=61
on expiry, used vs unused codes, revoked vs live refresh tokens). This
builds on the build phase's injectable architecture by exercising every
seam it exposed.

### Block 3 - From test phase -> report phase
ACCEPT: From the test run I have "6 passed in 0.05s" on the first attempt,
so no iteration was needed - the constraint "iterate once if needed" was
satisfied by not needing to.
GIVE: To any future maintainer I'm flagging two design choices worth knowing:
(a) tokens are not cryptographically signed (mock server; verification is by
storage lookup); (b) `state` is required at `/authorize` to surface CSRF
bugs early - production OAuth would also validate state on the client side.
RECIPROCATE: My contribution: this report plus `task_06_output.txt` with
the canonical `PASS - 6/6 tests pass` summary. This builds on the test
phase's green run by making the result auditable from the output file alone,
without needing to re-run pytest.

## Did Mauss change the approach?

Yes, modestly. Without the Mauss obligations I would have written a single
`storage.store` module global and patched `time.time` globally - both work
but make the failure modes hard to test in isolation. The "GIVE proactively"
obligation pushed me to expose `create_app(storage=...)` and to route time
through named module attributes from the start, so the test phase had clean
seams instead of having to refactor mid-task. Net effect: no iteration cycle.

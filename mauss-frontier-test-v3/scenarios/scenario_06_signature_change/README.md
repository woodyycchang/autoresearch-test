# Scenario 06 — Change `User.add_role` to accept list

## Task

Change `User.add_role(role)` to `User.add_roles(roles: list)` so multiple roles can be added at once.

Update ALL callers. The old single-role usage must still work — accept either str or list.

## Files
- `src/user.py`
- `src/admin_panel.py`, `src/signup.py`, `src/migration.py`

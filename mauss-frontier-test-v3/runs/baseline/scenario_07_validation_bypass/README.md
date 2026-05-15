# Scenario 07 — Add empty-string validation to ALL entry points

## Task

The system has multiple entry points that accept user input. Currently validation is inconsistent — some endpoints validate, some don't.

Add validation: **empty strings (or strings with only whitespace) must be rejected** with `ValueError("Input cannot be empty")`.

Apply to EVERY user-facing entry point. Don't leave any bypass routes.

## Files
- `src/validator.py` — define the validation helper
- `src/api_handler.py`, `src/admin_cli.py`, `src/webhook.py`, `src/import_csv.py` — entry points

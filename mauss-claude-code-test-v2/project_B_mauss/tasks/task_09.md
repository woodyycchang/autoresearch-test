# Task 09: Multi-Step Form Validator with Schema

## Description

Build a JSON-schema-like form validator:
- Schema with nested fields, types, required, min/max, regex, custom validators
- `Validator(schema).validate(data)` returns `(is_valid, list_of_errors)` where each error has `path` (e.g., `user.address.zip`) and `message`
- Support: string, int, float, bool, list-of-X, nested-object
- Custom validator: `{"type": "string", "validator": lambda s: s == s.lower()}` with error message
- Cross-field validation: `{"type": "object", "constraints": [lambda obj: obj["start"] < obj["end"]]}`

**Required files:**
- `schema.py`, `validator.py`, `errors.py`
- `tests/test_validator.py` — happy path, missing required, type mismatch, nested errors with correct paths, custom validators, cross-field

Failure modes: error paths wrong, cross-field check missing, type coercion (int accepts "5"), aggregate errors stop at first.

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_09_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

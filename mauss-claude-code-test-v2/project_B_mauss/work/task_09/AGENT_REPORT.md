# Task 09 Agent Report: JSON-Schema-Like Form Validator

## Summary

Built a JSON-schema-like form validator across three modules (`schema.py`,
`validator.py`, `errors.py`) plus a pytest suite (`tests/test_validator.py`)
and supporting `conftest.py`. All 30 tests pass on the first pytest run; no
iteration was required.

## What was built

- `errors.py`: `ValidationError` value object exposing `path` and `message`
  (plus `to_dict`, `__eq__`, `__repr__`), and a `SchemaError` exception for
  malformed schemas.
- `schema.py`: supported-type registry (`string`, `int`, `float`, `bool`,
  `list`, `object`) and a strict `type_matches` helper. Deliberately rejects
  the two most common type-coercion traps: `int` does NOT accept `bool` (since
  in Python `bool` is a subclass of `int`) and `float` does NOT accept `int`.
- `validator.py`: `Validator(schema).validate(data)` returns
  `(is_valid, list_of_errors)`. Walks the schema recursively, tracking
  the dotted path (`user.address.zip`) and bracketed list indices
  (`tags[1]`, `items[0].id`). Supports `min`/`max` for strings/numbers/lists,
  `regex` for strings, per-field `validator` callables with custom
  `validator_message`, and object-level `constraints` for cross-field checks
  with optional `constraint_messages`.
- `tests/test_validator.py`: 30 tests covering every failure mode named in
  the task spec.

## Design decisions targeting the spec's listed failure modes

1. **"Error paths wrong"**: Path is built incrementally as we descend. Objects
   use `parent.child`; lists use `parent[index]`. The root produces `<root>`
   for stand-alone leaves.
2. **"Cross-field check missing"**: Object-level `constraints` are run only
   after per-field validation. If a required field is missing, constraints
   are skipped to avoid bogus `KeyError`-style errors. The exception-safe
   wrapper still converts a raising constraint into a clean
   `ValidationError` rather than crashing the validator.
3. **"Type coercion (int accepts '5')"**: `type_matches` is strict. The test
   `test_type_mismatch_int_does_not_accept_string_five` proves this.
4. **"Aggregate errors stop at first"**: The walk appends to a single shared
   `errors` list and never short-circuits across siblings. A type mismatch on
   a subtree does stop descent into that subtree (to avoid noisy cascading
   errors), but never affects siblings. The test
   `test_errors_aggregate_does_not_stop_at_first` collects three independent
   type errors in one pass.

## Pytest result

```
30 passed in 0.05s
```

No iteration cycle was needed. The first invocation of
`python3 -m pytest tests/` returned green.

## Mauss handoff log

### Block 1: handoff from "spec" to "errors.py + schema.py author"
- **ACCEPT**: The task spec at `tasks/task_09.md` lists four explicit failure
  modes: wrong paths, missing cross-field, int-coerces-"5", and aggregate
  stops at first. I read all four before writing any code.
- **GIVE**: I established a strict-type policy in `schema.py` (no bool->int,
  no int->float coercion) so that downstream code in `validator.py` can
  rely on `type_matches` to enforce coercion-resistance without re-deciding
  per call site. I also gave the `ValidationError` value object an `__eq__`
  so tests can compare errors directly.
- **RECIPROCATE**: My contribution: a tight type-matching primitive and a
  comparable error type. This builds on the spec's listed failure modes by
  making "no coercion" a single-source-of-truth function and making
  "aggregate" easy to assert against.

### Block 2: handoff from "schema/errors layer" to "validator.py walker"
- **ACCEPT**: The previous step's `type_matches` already handles the
  int/float/bool/string traps, so the walker does not re-check Python types
  inline.
- **GIVE**: I designed the walker so the path string is computed at *each*
  recursive call rather than reconstructed at the leaf. This guarantees the
  failure mode "error paths wrong" cannot bite us as long as every recursive
  call assembles `child_path` correctly. I also wired the cross-field
  constraint check to skip if a direct-child error or missing required field
  was already recorded, so `lambda obj: obj["start"] < obj["end"]` never
  throws `KeyError` for half-built objects.
- **RECIPROCATE**: My contribution: a path-correct, exception-safe recursive
  walker that aggregates instead of short-circuiting. This builds on the
  schema layer's `type_matches` by extending strict typing into nested
  structures and list indices.

### Block 3: handoff from "validator code" to "test author"
- **ACCEPT**: The walker's contract is `(is_valid, [ValidationError])` with
  one error per failure point. I tested with that exact shape in mind.
- **GIVE**: I gave the tests explicit assertions on `path` strings (not just
  on counts) so any future regression that breaks path computation will be
  caught immediately. I added negative tests for the four spec failure
  modes by name: `test_type_mismatch_int_does_not_accept_string_five`,
  `test_errors_aggregate_does_not_stop_at_first`,
  `test_cross_field_skipped_if_required_missing`, and
  `test_nested_error_has_correct_path`.
- **RECIPROCATE**: My contribution: a 30-test suite that explicitly maps
  back to each named failure mode in the spec. This builds on the
  validator's contract by turning each invariant into a named assertion,
  which makes future regressions self-diagnosing.

## Files (absolute paths)

- `/home/user/autoresearch-test/mauss-claude-code-test-v2/project_B_mauss/work/task_09/schema.py`
- `/home/user/autoresearch-test/mauss-claude-code-test-v2/project_B_mauss/work/task_09/validator.py`
- `/home/user/autoresearch-test/mauss-claude-code-test-v2/project_B_mauss/work/task_09/errors.py`
- `/home/user/autoresearch-test/mauss-claude-code-test-v2/project_B_mauss/work/task_09/conftest.py`
- `/home/user/autoresearch-test/mauss-claude-code-test-v2/project_B_mauss/work/task_09/tests/test_validator.py`
- `/home/user/autoresearch-test/mauss-claude-code-test-v2/project_B_mauss/work/task_09/task_09_output.txt`

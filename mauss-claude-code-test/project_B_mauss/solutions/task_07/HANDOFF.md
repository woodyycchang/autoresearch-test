# Task 07 Handoff - Minimal JSON Parser

## ACCEPT
This task was delegated by the orchestrator with explicit constraints carried
forward from the project CLAUDE.md: implement a JSON parser without using
`json`, `ast.literal_eval`, `eval`, or `exec`; stdlib + pytest only; no
`output.txt`. I am honoring all of those constraints exactly as stated.

## What was built
- `solution.py` - Recursive-descent JSON parser exposing `parse(s) -> value`.
  Implementation is a single `_Parser` class with index-based scanning (no
  regex, no third-party libs, no banned modules).
- `test_solution.py` - 54 pytest cases covering primitives, strings (with
  `\"`, `\\`, `\n`, `\t`, `\r`, `\b`, `\f`, `\/`, `\uXXXX` escapes), numbers
  (int, float, negative, exponent), nested objects/arrays, whitespace, and
  24 parametrized invalid-input cases that must raise `ValueError`.
- Test result: **54 passed in 0.07s**.

## GIVE (info the next agent / validator needs)

### How to verify
```
cd /home/user/autoresearch-test/mauss-claude-code-test/project_B_mauss/solutions/task_07/
pytest test_solution.py -v
```
No fixtures, no conftest, no env vars needed.

### Design choices worth knowing
1. **Single public surface**: only `parse(s)` is exported for use; `_Parser`
   is an implementation detail (leading underscore).
2. **Error model**: every malformed input path raises `ValueError` with a
   short message including the offending position when known. Type errors
   on non-string input also surface as `ValueError` (per the spirit of the
   task - one exception type for all "invalid JSON" failures).
3. **Spec strictness applied**:
   - Leading zeros (`01`) rejected.
   - Trailing commas rejected in both `[]` and `{}`.
   - Unescaped control chars inside strings rejected (matches RFC 8259).
   - Trailing data after a valid value rejected (`{"a":1} extra`).
   - Single-quoted strings rejected (not JSON).
4. **Number typing**: returns `int` only when no `.` / `e` / `E` was seen;
   otherwise `float`. Matches what `json.loads` does, so callers can swap
   in either implementation.
5. **Unicode escapes**: `\uXXXX` is supported; surrogate-pair handling is
   NOT implemented (a lone surrogate will produce a lone-surrogate `str`
   character, same as Python's `chr()`). If the validator needs full BMP +
   astral handling via paired surrogates, that is the obvious extension
   point in `_parse_string`.

### Risks / things to flag
- The task said escape sequences `\"`, `\\`, `\n`, `\t` "must" be handled.
  I went beyond the minimum and also handle `\r \b \f \/ \uXXXX`. This is
  additive and should not break any reasonable validator check.
- I deliberately did NOT create `output.txt` even though the task text
  asked for a 1-line summary file - the orchestrator's CONSTRAINTS line
  ("No output.txt") overrides the task body. Flagging this in case a
  validator reads the task body literally.

## RECIPROCATE
My contribution: a strict, dependency-free recursive-descent JSON parser
(`parse(s)`) plus a 54-case pytest suite covering valid inputs, edge cases,
and 24 invalid-input rejection scenarios, all passing. This builds on the
orchestrator's task brief by translating the informal "minimal JSON parser"
spec into a concrete RFC-8259-aligned implementation, locking the public
contract (`parse(s) -> Python value`, `ValueError` on bad input) so the
validator can run a single `pytest` command and judge correctness without
having to reconstruct the requirements.

# Task 08: Regex Engine (NFA-based)

## Description

Build a regex engine supporting these:
- Literals (alphanumeric, escaped special chars like `\.`, `\*`)
- `.` any char
- `*` zero or more, `+` one or more, `?` optional
- `|` alternation
- `[abc]` char class, `[^abc]` negated, `[a-z]` range
- `()` grouping
- `^` start anchor, `$` end anchor

API: `compile(pattern)` returns `Regex` with `.match(s)`, `.search(s)`, `.findall(s)`

**Required files:**
- `compiler.py` (regex → NFA), `nfa.py`, `matcher.py`
- `tests/test_regex.py` — 30+ tests including: `a*b` matches "aaab", `[^x]+` matches everything but x, `^a|b$` precedence, escaped specials

Failure modes: precedence wrong (`|` vs concat), `.` matches newline, anchors not respected, infinite loop on `(a*)*`.

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_08_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

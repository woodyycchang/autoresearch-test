# Task 01: Multi-file SQL Engine

## Description

Build a minimal in-memory SQL engine supporting:
- `CREATE TABLE name (col1 TYPE, col2 TYPE)` (TYPES: INT, TEXT)
- `INSERT INTO name VALUES (...)`
- `SELECT col1, col2 FROM name WHERE col = value` (= and != operators)
- `DELETE FROM name WHERE col = value`

**Required files** (must coordinate types across all):
- `tokenizer.py` — produces tokens
- `parser.py` — produces AST nodes
- `engine.py` — executes statements
- `tests/test_engine.py` — at least 15 tests covering all 4 statement types + error cases (bad column, type mismatch, missing table)

Failure modes: column type not enforced, parser/engine type mismatch, error messages missing, SELECT after DELETE returns deleted rows.

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_01_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

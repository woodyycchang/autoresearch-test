# Task 01 - Multi-file SQL Engine - Agent Report

## Files built

- `tokenizer.py` - lexer producing `(type, value)` tokens (KEYWORD, IDENT, NUMBER, STRING, SYMBOL). Handles `!=` as a single token, strips quotes from string literals, upper-cases keywords, raises `TokenizerError`.
- `parser.py` - recursive descent parser consuming the token list. Emits dataclass AST nodes: `CreateTable`, `Insert`, `Select`, `Delete`, `Condition`. Raises `ParserError`.
- `engine.py` - in-memory executor. Owns `Engine` class with single public method `execute(sql)`. Stores tables as lists of rows. Enforces column types on INSERT and on WHERE literals. Raises `EngineError`.
- `conftest.py` - inserts the work dir on `sys.path` so tests can import the modules.
- `tests/test_engine.py` - 28 tests across tokenizer sanity, parser shape, all four statement types, and every error mode named in the spec.

## Approach

Picked a strict, layered design so the three modules could not drift on types:

1. Tokenizer guarantees `KEYWORD` values are upper-cased so the parser can compare against a fixed set without re-normalizing.
2. Parser uses `@dataclass` AST nodes; `engine.py` imports those classes directly and dispatches with `isinstance` - that way any rename or field change shows up as an `ImportError` immediately rather than silently breaking at runtime.
3. Engine centralizes type checks in `_check_type` and reuses it for both INSERT and WHERE literals - one place to keep INT/TEXT semantics honest.

Explicitly addressed the four failure modes in the spec:
- Column type enforced via `_check_type` (rejects bool-as-int too).
- Parser/engine type alignment: engine imports the AST classes from parser, not duck-typed dicts.
- Error messages always mention the offending name (table, column, type) - tested.
- DELETE rebuilds `table.rows` to the kept-list, so subsequent SELECT cannot return deleted rows - tested via `test_delete_removes_matching_row` and `test_delete_then_reinsert_keeps_only_new_row`.

## Bugs encountered

None during the run - all 28 tests passed on the first execution. The two design decisions that prevented likely bugs:
- Rejecting `bool` in the INT check (because `isinstance(True, int)` is True in Python).
- Validating WHERE column literals against the column's declared type before iterating rows, so a `WHERE id = 'alice'` against an INT column fails fast with a clear message instead of silently returning empty results.

## Final pytest output

`28 passed in 0.06s`

## Mauss handoff log

### Handoff 1: tokenizer -> parser
- ACCEPT: The parser depends on the tokenizer's promise that keywords are emitted upper-cased and that `!=` is one symbol token. I read those guarantees directly out of `tokenizer.py`'s module docstring before writing parser logic.
- GIVE: I documented the exact token shape `(token_type, value)` and the `STRING`/`NUMBER` value typing (Python `str`/`int`) at the top of `tokenizer.py` so the parser - and anyone replacing it - knows literals are already coerced.
- RECIPROCATE: My contribution: a tokenizer that pre-normalizes case and pre-parses literal types. This builds on the spec's "coordinate types across all files" by making the parser's job a pure structural problem - no string/int conversion lives in parser.py.

### Handoff 2: parser -> engine
- ACCEPT: The engine relies on parser AST nodes being dataclasses with stable field names (`CreateTable.columns` as `list[(name, type)]`, `Condition.op` in `{'=', '!='}`). I checked the parser's docstring contract before importing.
- GIVE: I flagged the bool-vs-int subtlety in `engine._check_type` because the parser only sees `NUMBER` tokens (always ints), but a future caller building AST nodes manually could pass `True`. The check protects the engine regardless of upstream.
- RECIPROCATE: My contribution: the engine imports parser's AST classes directly and dispatches via `isinstance`. This builds on the parser's dataclass contract by turning any future field rename into an immediate `ImportError` instead of a silent runtime mismatch - the exact failure mode the spec warned about.

### Handoff 3: code -> tests
- ACCEPT: The test file references the four failure modes named in the task spec ("column type not enforced, parser/engine type mismatch, error messages missing, SELECT after DELETE returns deleted rows") and maps one or more tests to each. I did not write tests blindly - each error-path test asserts on the substring in the error message so "missing error messages" cannot regress.
- GIVE: I shared the engine-side invariants the tests need to know about (e.g., DELETE replaces `table.rows` rather than mutating in place; INT rejects bool; WHERE literals are type-checked against the column). Tests `test_delete_then_reinsert_keeps_only_new_row` and `test_select_where_type_mismatch_raises` exist specifically to lock those in.
- RECIPROCATE: My contribution: 28 tests, all passing, covering all four statement types, all four named failure modes, plus tokenizer and parser shape. This builds on the engine's contracts by turning every documented promise into an assertion - so a future edit to any of the three modules that breaks the contract will fail loudly.

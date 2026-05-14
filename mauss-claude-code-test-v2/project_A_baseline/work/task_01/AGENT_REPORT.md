# Task 01 Agent Report

## Files built

- `tokenizer.py` — lexer producing `Token` dataclasses with explicit kind constants (`TOK_KEYWORD`, `TOK_IDENT`, `TOK_INT`, `TOK_STRING`, `TOK_EQ`, `TOK_NEQ`, etc.).
- `parser.py` — recursive-descent parser consuming tokens and producing AST dataclasses (`CreateTable`, `Insert`, `Select`, `Delete`, `ColumnDef`, `Condition`).
- `engine.py` — in-memory executor with `Engine.execute(sql)` entry point and `SelectResult` return type for queries.
- `conftest.py` — adds the work dir to `sys.path` so the three top-level modules are importable from `tests/`.
- `tests/test_engine.py` — 26 tests across tokenizer, parser, and engine layers.

## Approach

I designed the types first, then built sequentially.

1. **Tokenizer contract first.** I fixed the set of token kinds as module-level string constants in `tokenizer.py` (`TOK_KEYWORD`, `TOK_TYPE`, `TOK_IDENT`, `TOK_INT`, `TOK_STRING`, `TOK_EQ`, `TOK_NEQ`, etc.). These are the shared vocabulary between tokenizer and parser, so I never had to guess kind names later.
2. **AST contract second.** Inside `parser.py` I defined the AST dataclasses (`CreateTable`, `Insert`, `Select`, `Delete`, `Condition`, `ColumnDef`) up front. `Condition.op` is the string `"="` or `"!="`, which keeps the engine independent of token kinds.
3. **Engine last.** `engine.py` imports only AST classes from `parser.py` and never touches token kinds, so the layering is one-directional: tokenizer → parser → engine.
4. **Type enforcement is centralized.** Both `INSERT` and `WHERE` clauses (in `SELECT` and `DELETE`) go through one `_check_type` helper on the engine, so type errors are reported uniformly. I also rejected `bool` even though it's an `int` subclass, since SQL TEXT/INT should not silently accept booleans.

## Bugs encountered

None on the first run — all 26 tests passed. The early type-system work prevented the classic failure modes called out in the spec: parser/engine type mismatches (avoided by sharing AST dataclasses), column type not enforced (centralized `_check_type`), and SELECT-after-DELETE returning deleted rows (DELETE rebuilds `table.rows` from the kept rows, so reads see the updated state).

## Internal handoffs

- Tokenizer → parser: ordered list of `Token` dataclasses with `kind`, `value`, `pos`. The parser uses `kind` for control flow and `value` for payloads (keyword name, identifier text, integer/string literal).
- Parser → engine: AST dataclasses. The engine never re-tokenizes or re-parses.
- A single `Engine.execute(sql)` convenience method ties tokenize → parse → execute together for tests.

## Final pytest output

```
26 passed in 0.04s
```

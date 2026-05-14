# Task 03: Markdown to HTML with Edge Cases

## Description

Build a Markdown→HTML converter handling:
- Headers `#`, `##`, `###` → `<h1>`, `<h2>`, `<h3>`
- Bold `**text**`, italic `*text*`, but NOT inside code blocks
- Inline code `` `code` `` and fenced code blocks ` ```lang...``` `
- Lists (ordered `1.` and unordered `-`), with up to 3 nesting levels
- Links `[text](url)`, with HTML escaping of `<`, `>`, `&` in text but NOT in URL
- Block quotes `> text` (single line OK)

**Required files:**
- `lexer.py`, `parser.py`, `renderer.py`
- `tests/test_md.py` — 25+ tests including edge cases (code block containing `**bold**` must NOT bold; nested lists; XSS attempt in link text must be escaped)

Failure modes: bold/italic confused, code block contents formatted, XSS not escaped, nested lists flattened.

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_03_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

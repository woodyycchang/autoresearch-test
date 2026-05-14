# Task 03: Markdown -> HTML Converter

## Files built

- `lexer.py` — block-level tokenizer. Emits typed `Token` dataclasses for
  headers, paragraphs, fenced code blocks, list items (with indent and
  ordered/unordered flag), block quotes, and blank lines.
- `parser.py` — converts the token stream to a simple AST of dict nodes.
  Joins consecutive paragraph lines, captures fenced-code content verbatim,
  and recursively groups list items into nested `list` nodes by indent level
  (cap of 3 levels).
- `renderer.py` — walks the AST to emit HTML. Inline expansion handles bold
  (`**...**`), italic (`*...*`), inline code, and links, with HTML escaping
  for everything else.
- `conftest.py` — adds the work dir to `sys.path` for tests.
- `tests/test_md.py` — 36 tests covering headers, bold/italic, inline and
  fenced code (including the "code containing `**bold**` must not bold"
  case), unordered/ordered lists with 2- and 3-level nesting, links with
  XSS-in-text escaping, block quotes, plain-text escaping, and edge cases
  (empty input, multi-block docs, helper functions).

## Approach

The tricky inline rules use a placeholder strategy: first capture inline code
spans and links, replacing each with a `\x00N\x00` sentinel and stashing the
already-rendered HTML. Then escape the remaining text and apply bold/italic.
Finally restore the sentinels. This guarantees that bold/italic regexes
cannot peek inside code spans or link text, which is exactly the failure
mode the spec warns about.

Lists: a recursive `_parse_list` consumes items whose indent level is `>=`
its base level. Items at a deeper indent are attached to the previous
sibling's `children`. Indent unit is 2 spaces, capped at depth 3.

Escaping: link text and all paragraph/header/quote text are HTML-escaped
(<, >, &, "). The URL is preserved except for `&` -> `&amp;` so the rendered
attribute is well-formed. This makes the XSS attempt
`[<script>alert(1)</script>](url)` render as escaped text only.

## Bugs encountered

None during implementation — the design (placeholder-substitution for code
spans/links before bold/italic) avoided the classic "bold inside code"
class of bug. Tests passed on first run.

## Final pytest output line

`============================== 36 passed in 0.05s ==============================`

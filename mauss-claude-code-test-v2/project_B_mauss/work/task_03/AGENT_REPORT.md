# Task 03 Agent Report

## Result
**PASS - 30/30 tests pass** on first pytest run, no iteration needed.

## Files built (in work dir)
- `lexer.py` - block-level tokenizer. Scans fenced code blocks first (so their bodies stay raw), then per-line regexes for headers, ordered/unordered list items (with indent level normalized to 0/1/2), blockquotes, paragraphs, and blank lines.
- `parser.py` - turns the flat token stream into a block AST. Most logic is straightforward; the only non-trivial piece is `_build_list`, a recursive grouper that nests deeper-indent list items as `children` of the previous item at the surrounding indent.
- `renderer.py` - AST -> HTML. Inline pass uses a placeholder strategy: (1) stash inline `code` first so its body is shielded from later passes, (2) stash links with text escaped but URL preserved verbatim, (3) bold `**...**` before italic `*...*`, (4) HTML-escape what remains, (5) re-insert placeholders. Fenced code is rendered with body escaped but never inline-formatted.
- `conftest.py` - prepends work dir to `sys.path` so `import lexer/parser/renderer` resolves from the tests subdirectory.
- `tests/test_md.py` - 30 tests across headers, bold/italic, inline code, fenced code, lists (incl. nested 2 and 3 levels), links + XSS, blockquotes, lexer sanity, and a multi-block integration test.

## Approach / design choices
- **Three-stage pipeline** (lex -> parse -> render) keeps each concern small and lets the renderer be the only place that knows about inline formatting precedence.
- **Inline precedence via placeholders** is the key to making the spec's edge cases pass simultaneously: code shields bold, links escape text but not URL, bold beats italic.
- **List nesting** uses indent levels 0/1/2 (2+/4+ spaces) capped at three levels, exactly matching the spec.

## Bugs / issues encountered
None during implementation. Everything passed on the first pytest invocation. The two design decisions that prevented likely bugs:
1. Doing inline-code substitution **before** bold/italic so backticked `**x**` could not slip through.
2. Resolving `BOLD_RE` before `ITALIC_RE` so `**x**` produces `<strong>x</strong>` instead of `<em><em>x</em></em>`.

## Final pytest output
```
============================== 30 passed in 0.04s ==============================
```

## Mauss handoff log

### Handoff 1: task spec -> lexer
- **ACCEPT**: spec calls out three concrete failure modes -- code-block contents formatted, XSS not escaped, nested lists flattened. The lexer is the first place where two of those (code-block-contents and list-nesting) can be locked in.
- **GIVE**: emit fenced-code as a single token captured BEFORE per-line tokenization (so inner `**` never reaches the inline pass) and normalize list indent to 0/1/2 so downstream code doesn't re-count whitespace.
- **RECIPROCATE**: My contribution: a flat token list with indent already resolved. This builds on the spec's "up to 3 nesting levels" requirement by encoding it once, at the lexer boundary, instead of letting it leak through the parser.

### Handoff 2: lexer -> parser
- **ACCEPT**: lexer guarantees `fenced_code` tokens carry verbatim body text, and `list_item` tokens carry `indent` in {0,1,2}. I rely on both invariants.
- **GIVE**: AST distinguishes `code` (raw, must not be inline-formatted) from every other text node (which must be). I also merge consecutive paragraph lines so the renderer sees one node per paragraph -- a gap the renderer wouldn't have known to fill.
- **RECIPROCATE**: My contribution: a tree-shaped AST with explicit `code` vs text-bearing nodes, plus stack-built list nesting. This builds on the lexer's flat indent-tagged stream by collapsing it into the shape the renderer can walk recursively.

### Handoff 3: parser -> renderer
- **ACCEPT**: parser separates `code` nodes from inline-eligible nodes. I never call `_format_inline` on a `code` node, honoring that contract.
- **GIVE (to tests)**: renderer output is whitespace-free between blocks; escaping rule is `<`/`>`/`&` -> entities in text, URLs preserved raw. Order matters: code first, then links, then bold, then italic. Tests should assert on this exact convention.
- **RECIPROCATE**: My contribution: a placeholder-based inline pass that makes all three spec edge cases (code-shields-bold, XSS-escape-link-text-not-url, no-italic-bold-confusion) pass simultaneously. This builds on parser's clean node typing by adding the one precedence ordering the spec implies but doesn't spell out.

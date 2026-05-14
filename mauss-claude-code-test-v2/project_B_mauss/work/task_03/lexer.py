"""Lexer: turns raw Markdown text into a flat list of block-level tokens.

Tokens are dicts with at least a 'type' field. Types:
- 'header'      : {'type','level','text'}
- 'fenced_code' : {'type','lang','text'}  -- raw content preserved verbatim
- 'list_item'   : {'type','ordered','indent','text'}
- 'blockquote'  : {'type','text'}
- 'paragraph'   : {'type','text'}
- 'blank'       : {'type'}

Fenced code blocks are scanned BEFORE per-line tokenization so their inner
content (which may contain `**bold**`, `#`, `-`, etc.) is preserved raw.
"""

import re

HEADER_RE = re.compile(r'^(#{1,3})\s+(.*)$')
FENCE_RE = re.compile(r'^```(\w*)\s*$')
ULIST_RE = re.compile(r'^(\s*)-\s+(.*)$')
OLIST_RE = re.compile(r'^(\s*)\d+\.\s+(.*)$')
QUOTE_RE = re.compile(r'^>\s?(.*)$')


def _indent_level(spaces: str) -> int:
    """Map leading whitespace to indent level (0, 1, 2)."""
    n = len(spaces.expandtabs(4))
    # 0 spaces -> 0, 2-3 -> 1, 4+ -> 2 (cap at 2 -> three total levels)
    if n >= 4:
        return 2
    if n >= 2:
        return 1
    return 0


def tokenize(text: str):
    lines = text.split('\n')
    tokens = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Fenced code block: capture raw content until matching fence.
        m = FENCE_RE.match(line)
        if m:
            lang = m.group(1)
            body = []
            i += 1
            while i < len(lines) and not FENCE_RE.match(lines[i]):
                body.append(lines[i])
                i += 1
            # Skip closing fence (if found).
            if i < len(lines):
                i += 1
            tokens.append({'type': 'fenced_code', 'lang': lang, 'text': '\n'.join(body)})
            continue

        if line.strip() == '':
            tokens.append({'type': 'blank'})
            i += 1
            continue

        m = HEADER_RE.match(line)
        if m:
            tokens.append({'type': 'header', 'level': len(m.group(1)), 'text': m.group(2).strip()})
            i += 1
            continue

        m = ULIST_RE.match(line)
        if m:
            tokens.append({
                'type': 'list_item', 'ordered': False,
                'indent': _indent_level(m.group(1)), 'text': m.group(2),
            })
            i += 1
            continue

        m = OLIST_RE.match(line)
        if m:
            tokens.append({
                'type': 'list_item', 'ordered': True,
                'indent': _indent_level(m.group(1)), 'text': m.group(2),
            })
            i += 1
            continue

        m = QUOTE_RE.match(line)
        if m:
            tokens.append({'type': 'blockquote', 'text': m.group(1)})
            i += 1
            continue

        tokens.append({'type': 'paragraph', 'text': line})
        i += 1

    return tokens

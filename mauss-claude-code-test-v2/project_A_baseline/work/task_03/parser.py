"""Parser for Markdown tokens.

Builds a small AST of block nodes. Each node is a dict.

Node types:
- {type: 'header', level: int, text: str}
- {type: 'paragraph', text: str}
- {type: 'code_block', text: str, lang: str}
- {type: 'quote', text: str}
- {type: 'list', ordered: bool, items: [ListItem, ...]}

ListItem:
- {text: str, children: [list nodes]}
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from lexer import Token, tokenize


# Each indent level corresponds to 2 spaces by default. We tolerate any
# indentation that grows monotonically. To keep nesting limited to 3
# levels we cap depth at 3.
MAX_NEST = 3


def _indent_level(indent: int) -> int:
    """Translate a leading space count to a nesting level (0..)."""
    return indent // 2


def parse(src: str) -> List[Dict]:
    tokens = tokenize(src)
    nodes: List[Dict] = []
    i = 0
    n = len(tokens)

    # Buffer for joining consecutive paragraph lines
    para_buf: List[str] = []

    def flush_paragraph():
        if para_buf:
            nodes.append({"type": "paragraph", "text": " ".join(para_buf)})
            para_buf.clear()

    while i < n:
        tok = tokens[i]

        if tok.type == "blank":
            flush_paragraph()
            i += 1
            continue

        if tok.type == "header":
            flush_paragraph()
            nodes.append({"type": "header", "level": tok.level, "text": tok.text})
            i += 1
            continue

        if tok.type == "code_block":
            flush_paragraph()
            nodes.append({"type": "code_block", "text": tok.text, "lang": tok.lang})
            i += 1
            continue

        if tok.type == "quote":
            flush_paragraph()
            nodes.append({"type": "quote", "text": tok.text})
            i += 1
            continue

        if tok.type == "list_item":
            flush_paragraph()
            list_node, consumed = _parse_list(tokens, i, depth=0)
            nodes.append(list_node)
            i += consumed
            continue

        if tok.type == "paragraph":
            para_buf.append(tok.text.strip())
            i += 1
            continue

        # Unknown — skip
        i += 1

    flush_paragraph()
    return nodes


def _parse_list(
    tokens: List[Token], start: int, depth: int
) -> Tuple[Dict, int]:
    """Parse a sequence of list items at the given depth.

    Returns the list node and the number of tokens consumed from `start`.
    """
    n = len(tokens)
    if start >= n or tokens[start].type != "list_item":
        return {"type": "list", "ordered": False, "items": []}, 0

    base_indent = tokens[start].indent
    ordered = tokens[start].ordered
    base_level = _indent_level(base_indent)

    items: List[Dict] = []
    i = start

    while i < n:
        tok = tokens[i]
        if tok.type == "blank":
            # Allow a single blank between list items but stop on double-blank
            # for simplicity: peek ahead.
            j = i
            blanks = 0
            while j < n and tokens[j].type == "blank":
                blanks += 1
                j += 1
            if j < n and tokens[j].type == "list_item":
                next_level = _indent_level(tokens[j].indent)
                if next_level >= base_level:
                    i = j
                    continue
            break

        if tok.type != "list_item":
            break

        cur_level = _indent_level(tok.indent)
        if cur_level < base_level:
            break

        if cur_level > base_level:
            # Nested list belongs to the previous item.
            if not items:
                # No parent — treat it as starting a new list at this level.
                child_node, consumed = _parse_list(tokens, i, depth + 1)
                items.append({"text": "", "children": [child_node]})
                i += consumed
                continue
            if depth + 1 >= MAX_NEST:
                # Cap nesting; treat deeper as same level.
                items.append({"text": tok.text, "children": []})
                i += 1
                continue
            child_node, consumed = _parse_list(tokens, i, depth + 1)
            items[-1]["children"].append(child_node)
            i += consumed
            continue

        # Same level — but ordered/unordered mismatch breaks the list.
        if tok.ordered != ordered:
            break

        items.append({"text": tok.text, "children": []})
        i += 1

    return {"type": "list", "ordered": ordered, "items": items}, i - start

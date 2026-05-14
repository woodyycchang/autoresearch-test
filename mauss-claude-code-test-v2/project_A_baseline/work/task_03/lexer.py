"""Lexer for Markdown.

Splits the source into block-level tokens. Inline structures (bold, italic,
inline code, links, escaping) are handled later by the parser/renderer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Token:
    type: str
    text: str = ""
    level: int = 0
    # For list items:
    indent: int = 0  # number of leading spaces
    ordered: bool = False
    # For fenced code:
    lang: str = ""


FENCE_RE = re.compile(r"^(\s*)```(\S*)\s*$")
HEADER_RE = re.compile(r"^(#{1,3})\s+(.*)$")
UL_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")
OL_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)$")
QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
BLANK_RE = re.compile(r"^\s*$")


def tokenize(src: str) -> List[Token]:
    """Convert a Markdown string into a flat list of block tokens."""
    lines = src.splitlines()
    tokens: List[Token] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # Fenced code block
        m = FENCE_RE.match(line)
        if m:
            lang = m.group(2)
            buf: List[str] = []
            i += 1
            while i < n and not FENCE_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            # Skip closing fence if present
            if i < n:
                i += 1
            tokens.append(Token(type="code_block", text="\n".join(buf), lang=lang))
            continue

        # Blank line
        if BLANK_RE.match(line):
            tokens.append(Token(type="blank"))
            i += 1
            continue

        # Header
        m = HEADER_RE.match(line)
        if m:
            tokens.append(Token(type="header", level=len(m.group(1)), text=m.group(2)))
            i += 1
            continue

        # Block quote
        m = QUOTE_RE.match(line)
        if m:
            tokens.append(Token(type="quote", text=m.group(1)))
            i += 1
            continue

        # Ordered list item
        m = OL_RE.match(line)
        if m:
            indent = len(m.group(1))
            tokens.append(
                Token(type="list_item", text=m.group(3), indent=indent, ordered=True)
            )
            i += 1
            continue

        # Unordered list item
        m = UL_RE.match(line)
        if m:
            indent = len(m.group(1))
            tokens.append(
                Token(type="list_item", text=m.group(2), indent=indent, ordered=False)
            )
            i += 1
            continue

        # Plain paragraph line
        tokens.append(Token(type="paragraph", text=line))
        i += 1

    return tokens

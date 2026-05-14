"""HTML renderer for the parser AST.

Handles inline expansion: bold, italic, inline code, links. Code spans and
code blocks are NEVER formatted — their content is HTML-escaped only.
Link text is HTML-escaped (XSS-safe); the URL is preserved as-is to allow
schemes the user supplies.
"""

from __future__ import annotations

import re
from typing import Dict, List

from parser import parse


# ---------------------------------------------------------------------------
# Escaping
# ---------------------------------------------------------------------------

def escape_html(text: str) -> str:
    """Escape the four characters that must never appear raw in HTML text."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# Inline parsing
# ---------------------------------------------------------------------------

# We use a sentinel-and-replace strategy: pull out inline code spans and links
# first (so their contents aren't affected by bold/italic), then handle bold
# and italic on the remainder.

_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
_BOLD_RE = re.compile(r"\*\*([^*]+?)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")


def render_inline(text: str) -> str:
    """Render an inline string fragment to HTML."""
    placeholders: List[str] = []

    def stash(html: str) -> str:
        token = f"\x00{len(placeholders)}\x00"
        placeholders.append(html)
        return token

    # 1) Inline code: capture first so contents aren't formatted further.
    def code_sub(m: re.Match) -> str:
        return stash(f"<code>{escape_html(m.group(1))}</code>")

    text = _INLINE_CODE_RE.sub(code_sub, text)

    # 2) Links: escape text, keep URL verbatim (only escape & for HTML
    #    correctness). XSS via javascript: schemes is the user's choice; the
    #    text — which is where attacker-controlled content typically goes —
    #    is fully escaped.
    def link_sub(m: re.Match) -> str:
        link_text = escape_html(m.group(1))
        url = m.group(2).replace("&", "&amp;")
        return stash(f'<a href="{url}">{link_text}</a>')

    text = _LINK_RE.sub(link_sub, text)

    # 3) Escape everything else, then re-apply bold/italic markers. We escape
    #    BEFORE applying bold/italic so the markers themselves are still
    #    recognizable (* and ** are not affected by escape_html).
    text = escape_html(text)

    text = _BOLD_RE.sub(lambda m: f"<strong>{m.group(1)}</strong>", text)
    text = _ITALIC_RE.sub(lambda m: f"<em>{m.group(1)}</em>", text)

    # 4) Restore placeholders.
    for idx, html in enumerate(placeholders):
        text = text.replace(f"\x00{idx}\x00", html)

    return text


# ---------------------------------------------------------------------------
# Block rendering
# ---------------------------------------------------------------------------

def render_node(node: Dict) -> str:
    t = node["type"]
    if t == "header":
        level = node["level"]
        return f"<h{level}>{render_inline(node['text'])}</h{level}>"
    if t == "paragraph":
        return f"<p>{render_inline(node['text'])}</p>"
    if t == "code_block":
        content = escape_html(node["text"])
        lang = node.get("lang", "")
        if lang:
            return f'<pre><code class="language-{lang}">{content}</code></pre>'
        return f"<pre><code>{content}</code></pre>"
    if t == "quote":
        return f"<blockquote>{render_inline(node['text'])}</blockquote>"
    if t == "list":
        return _render_list(node)
    return ""


def _render_list(node: Dict) -> str:
    tag = "ol" if node["ordered"] else "ul"
    pieces: List[str] = [f"<{tag}>"]
    for item in node["items"]:
        item_inline = render_inline(item["text"]) if item["text"] else ""
        children_html = "".join(_render_list(c) for c in item["children"])
        pieces.append(f"<li>{item_inline}{children_html}</li>")
    pieces.append(f"</{tag}>")
    return "".join(pieces)


def render(src: str) -> str:
    """Convert a Markdown source string into HTML."""
    nodes = parse(src)
    return "".join(render_node(n) for n in nodes)

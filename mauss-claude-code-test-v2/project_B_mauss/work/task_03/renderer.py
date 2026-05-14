"""Renderer: AST -> HTML string.

Inline formatting order is important:
  1. Extract inline code spans (`...`) first and replace with placeholders so
     their bodies are NEVER touched by bold/italic passes.
  2. Extract links [text](url) -- text gets HTML escaped, url does not.
  3. Apply bold **...** BEFORE italic *...* so '**x**' is not eaten by italic.
  4. HTML-escape everything else.
  5. Re-insert code-span and link placeholders.

Fenced code blocks bypass inline formatting entirely -- only their body is
HTML-escaped so any '<script>' etc. shows as text.
"""

import re
import html

from parser import parse


CODE_SPAN_RE = re.compile(r'`([^`\n]+)`')
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')
BOLD_RE = re.compile(r'\*\*([^*\n]+)\*\*')
ITALIC_RE = re.compile(r'\*([^*\n]+)\*')


def _escape(s: str) -> str:
    return html.escape(s, quote=False)


def _format_inline(text: str) -> str:
    """Apply inline formatting with the correct precedence."""
    placeholders = {}
    counter = [0]

    def _stash(html_fragment: str) -> str:
        key = f"\x00PH{counter[0]}\x00"
        counter[0] += 1
        placeholders[key] = html_fragment
        return key

    # 1. Inline code -- stash first, escape body, never format internally.
    def _code_sub(m):
        return _stash(f"<code>{_escape(m.group(1))}</code>")
    text = CODE_SPAN_RE.sub(_code_sub, text)

    # 2. Links -- escape text but NOT URL.
    def _link_sub(m):
        link_text = _escape(m.group(1))
        url = m.group(2)
        return _stash(f'<a href="{url}">{link_text}</a>')
    text = LINK_RE.sub(_link_sub, text)

    # 3. Bold before italic.
    def _bold_sub(m):
        inner = _escape(m.group(1))
        return _stash(f"<strong>{inner}</strong>")
    text = BOLD_RE.sub(_bold_sub, text)

    def _italic_sub(m):
        inner = _escape(m.group(1))
        return _stash(f"<em>{inner}</em>")
    text = ITALIC_RE.sub(_italic_sub, text)

    # 4. Escape the rest.
    text = _escape(text)

    # 5. Restore placeholders. They contain real HTML, so they must come back
    #    AFTER the final escape pass (the placeholder markers themselves
    #    survive escape() because \x00 isn't an HTML special character).
    for key, frag in placeholders.items():
        text = text.replace(key, frag)

    return text


def _render_list(node) -> str:
    tag = 'ol' if node['ordered'] else 'ul'
    parts = [f"<{tag}>"]
    for item in node['items']:
        body = _format_inline(item['text']) if item['text'] else ''
        if item['children']:
            children_html = ''.join(_render_list(c) for c in item['children'])
            parts.append(f"<li>{body}{children_html}</li>")
        else:
            parts.append(f"<li>{body}</li>")
    parts.append(f"</{tag}>")
    return ''.join(parts)


def render(text: str) -> str:
    ast = parse(text)
    out = []
    for node in ast:
        t = node['type']
        if t == 'header':
            lvl = node['level']
            out.append(f"<h{lvl}>{_format_inline(node['text'])}</h{lvl}>")
        elif t == 'code':
            lang = node['lang']
            escaped = _escape(node['text'])
            if lang:
                out.append(f'<pre><code class="language-{lang}">{escaped}</code></pre>')
            else:
                out.append(f'<pre><code>{escaped}</code></pre>')
        elif t == 'paragraph':
            out.append(f"<p>{_format_inline(node['text'])}</p>")
        elif t == 'blockquote':
            out.append(f"<blockquote>{_format_inline(node['text'])}</blockquote>")
        elif t == 'list':
            out.append(_render_list(node))
    return ''.join(out)

"""Tests for the Markdown -> HTML converter."""

from renderer import render, render_inline, escape_html
from parser import parse
from lexer import tokenize


# ---------------------------------------------------------------------------
# Headers
# ---------------------------------------------------------------------------

def test_h1_header():
    assert render("# Hello") == "<h1>Hello</h1>"


def test_h2_header():
    assert render("## Hi") == "<h2>Hi</h2>"


def test_h3_header():
    assert render("### Sub") == "<h3>Sub</h3>"


def test_h3_is_max_level():
    # Four hashes is not a header in our subset; treat as paragraph.
    out = render("#### Too deep")
    assert "<h4>" not in out
    assert "<p>" in out


# ---------------------------------------------------------------------------
# Bold / italic
# ---------------------------------------------------------------------------

def test_bold_basic():
    assert render("**bold**") == "<p><strong>bold</strong></p>"


def test_italic_basic():
    assert render("*it*") == "<p><em>it</em></p>"


def test_bold_and_italic_in_same_paragraph():
    out = render("**b** and *i*")
    assert "<strong>b</strong>" in out
    assert "<em>i</em>" in out


def test_bold_inside_header():
    out = render("# Hello **world**")
    assert out == "<h1>Hello <strong>world</strong></h1>"


# ---------------------------------------------------------------------------
# Inline code
# ---------------------------------------------------------------------------

def test_inline_code():
    assert render("`x = 1`") == "<p><code>x = 1</code></p>"


def test_inline_code_is_escaped():
    out = render("`<script>`")
    assert "<code>&lt;script&gt;</code>" in out


def test_inline_code_does_not_format():
    # Bold markers inside inline code stay as raw asterisks.
    out = render("`**not bold**`")
    assert "<strong>" not in out
    assert "**not bold**" in out


# ---------------------------------------------------------------------------
# Fenced code blocks
# ---------------------------------------------------------------------------

def test_fenced_code_block():
    src = "```\nhello\n```"
    out = render(src)
    assert out == "<pre><code>hello</code></pre>"


def test_fenced_code_block_with_lang():
    src = "```python\nx = 1\n```"
    out = render(src)
    assert '<pre><code class="language-python">x = 1</code></pre>' == out


def test_code_block_containing_bold_is_not_bolded():
    # Critical edge case from the task spec.
    src = "```\n**bold**\n```"
    out = render(src)
    assert "<strong>" not in out
    assert "**bold**" in out


def test_code_block_escapes_html():
    src = "```\n<script>alert(1)</script>\n```"
    out = render(src)
    assert "<script>" not in out  # tag itself must not appear
    assert "&lt;script&gt;" in out


# ---------------------------------------------------------------------------
# Lists
# ---------------------------------------------------------------------------

def test_simple_unordered_list():
    src = "- a\n- b"
    assert render(src) == "<ul><li>a</li><li>b</li></ul>"


def test_simple_ordered_list():
    src = "1. a\n2. b"
    assert render(src) == "<ol><li>a</li><li>b</li></ol>"


def test_nested_unordered_two_levels():
    src = "- a\n  - a1\n  - a2\n- b"
    out = render(src)
    # Inner list belongs to first item.
    assert out == "<ul><li>a<ul><li>a1</li><li>a2</li></ul></li><li>b</li></ul>"


def test_nested_three_levels():
    src = "- a\n  - b\n    - c"
    out = render(src)
    assert out == "<ul><li>a<ul><li>b<ul><li>c</li></ul></li></ul></li></ul>"


def test_nested_list_not_flattened():
    src = "- a\n  - b\n- c"
    out = render(src)
    # b must be nested under a, not a sibling of c.
    assert "<ul><li>a<ul><li>b</li></ul></li><li>c</li></ul>" == out


def test_ordered_inside_unordered():
    src = "- a\n  1. x\n  2. y"
    out = render(src)
    assert out == "<ul><li>a<ol><li>x</li><li>y</li></ol></li></ul>"


# ---------------------------------------------------------------------------
# Links
# ---------------------------------------------------------------------------

def test_simple_link():
    out = render("[Anthropic](https://anthropic.com)")
    assert '<a href="https://anthropic.com">Anthropic</a>' in out


def test_link_text_is_escaped_xss():
    # Critical XSS test from the task spec.
    out = render("[<script>alert(1)</script>](https://x.com)")
    assert "<script>" not in out
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in out
    assert 'href="https://x.com"' in out


def test_link_text_escapes_amp_and_brackets():
    out = render("[A & <B>](https://x.com)")
    assert "A &amp; &lt;B&gt;" in out


def test_link_url_not_escaped_except_amp():
    # The URL itself should be preserved (no extra escaping of < > inside it
    # since brackets are not legal there anyway, but & is converted for HTML).
    out = render("[q](https://x.com/?a=1&b=2)")
    assert 'href="https://x.com/?a=1&amp;b=2"' in out


# ---------------------------------------------------------------------------
# Block quotes
# ---------------------------------------------------------------------------

def test_blockquote_basic():
    assert render("> hi") == "<blockquote>hi</blockquote>"


def test_blockquote_with_bold():
    out = render("> **important**")
    assert out == "<blockquote><strong>important</strong></blockquote>"


# ---------------------------------------------------------------------------
# Misc / edge cases
# ---------------------------------------------------------------------------

def test_paragraph_html_escaped():
    out = render("a < b & c > d")
    assert "<p>a &lt; b &amp; c &gt; d</p>" == out


def test_empty_input():
    assert render("") == ""


def test_multiple_blocks_joined():
    src = "# Title\n\nA paragraph.\n\n- one\n- two"
    out = render(src)
    assert out == "<h1>Title</h1><p>A paragraph.</p><ul><li>one</li><li>two</li></ul>"


def test_tokenize_returns_list():
    toks = tokenize("# h")
    assert isinstance(toks, list)
    assert toks[0].type == "header"


def test_parse_returns_list():
    nodes = parse("# h")
    assert isinstance(nodes, list)
    assert nodes[0]["type"] == "header"


def test_escape_html_function():
    assert escape_html("<a>&b</a>") == "&lt;a&gt;&amp;b&lt;/a&gt;"


def test_render_inline_function_bold():
    assert render_inline("**x**") == "<strong>x</strong>"


def test_italic_not_inside_bold_markers():
    # '**foo**' should not also be wrapped in <em>.
    out = render_inline("**foo**")
    assert out == "<strong>foo</strong>"
    assert "<em>" not in out


def test_inline_code_with_link_after():
    out = render("see `code` and [link](https://x.com)")
    assert "<code>code</code>" in out
    assert '<a href="https://x.com">link</a>' in out

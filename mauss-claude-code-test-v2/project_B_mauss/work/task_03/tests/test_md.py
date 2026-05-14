"""Tests for the Markdown -> HTML pipeline (lexer + parser + renderer).

ACCEPT: builds on renderer's compact-output convention (no whitespace between
blocks) and explicit escaping rules.

GIVE: covers each spec'd edge case -- code containing **bold** stays literal,
XSS in link text gets escaped, nested lists (3 levels) preserved, bold vs
italic disambiguation, escape behavior in headers/blockquotes.
"""

from lexer import tokenize
from parser import parse
from renderer import render


# ---------- Headers ----------

def test_h1():
    assert render("# Hello") == "<h1>Hello</h1>"


def test_h2():
    assert render("## Sub") == "<h2>Sub</h2>"


def test_h3():
    assert render("### Deep") == "<h3>Deep</h3>"


def test_header_with_bold():
    assert render("# Hello **World**") == "<h1>Hello <strong>World</strong></h1>"


# ---------- Bold / italic ----------

def test_bold():
    assert render("**bold**") == "<p><strong>bold</strong></p>"


def test_italic():
    assert render("*italic*") == "<p><em>italic</em></p>"


def test_bold_then_italic_in_same_line():
    out = render("This is **strong** and *soft*")
    assert "<strong>strong</strong>" in out
    assert "<em>soft</em>" in out


def test_bold_not_italic_confusion():
    # The pair of asterisks must produce <strong>, not nested <em><em>.
    out = render("**x**")
    assert "<strong>x</strong>" in out
    assert "<em>" not in out


# ---------- Inline code ----------

def test_inline_code():
    assert render("`code`") == "<p><code>code</code></p>"


def test_inline_code_shields_bold():
    # **bold** inside inline code must NOT become <strong>.
    out = render("`**not bold**`")
    assert "<code>**not bold**</code>" in out
    assert "<strong>" not in out


# ---------- Fenced code blocks ----------

def test_fenced_code_plain():
    md = "```\nprint('hi')\n```"
    out = render(md)
    assert out == "<pre><code>print('hi')</code></pre>"


def test_fenced_code_with_lang():
    md = "```python\nx = 1\n```"
    out = render(md)
    assert '<pre><code class="language-python">x = 1</code></pre>' == out


def test_fenced_code_preserves_bold_markdown():
    # The required edge case: ** inside code block must NOT bold.
    md = "```\n**bold**\n```"
    out = render(md)
    assert "<strong>" not in out
    assert "**bold**" in out


def test_fenced_code_escapes_html():
    md = "```\n<script>alert(1)</script>\n```"
    out = render(md)
    assert "&lt;script&gt;" in out
    assert "<script>" not in out


# ---------- Lists ----------

def test_unordered_list():
    md = "- a\n- b\n- c"
    assert render(md) == "<ul><li>a</li><li>b</li><li>c</li></ul>"


def test_ordered_list():
    md = "1. a\n2. b"
    assert render(md) == "<ol><li>a</li><li>b</li></ol>"


def test_nested_list_two_levels():
    md = "- outer\n  - inner"
    out = render(md)
    # outer item wraps a child <ul>; inner item is inside it.
    assert out == "<ul><li>outer<ul><li>inner</li></ul></li></ul>"


def test_nested_list_three_levels():
    md = "- l1\n  - l2\n    - l3"
    out = render(md)
    assert out == "<ul><li>l1<ul><li>l2<ul><li>l3</li></ul></li></ul></li></ul>"


def test_nested_lists_not_flattened():
    md = "- a\n  - b\n- c"
    out = render(md)
    # 'c' must be a sibling of 'a', not flattened to top.
    assert out == "<ul><li>a<ul><li>b</li></ul></li><li>c</li></ul>"


def test_list_item_with_inline_formatting():
    md = "- **bold** item\n- *italic* item"
    out = render(md)
    assert "<li><strong>bold</strong> item</li>" in out
    assert "<li><em>italic</em> item</li>" in out


# ---------- Links + XSS ----------

def test_link_basic():
    out = render("[click](https://example.com)")
    assert out == '<p><a href="https://example.com">click</a></p>'


def test_link_xss_in_text_escaped():
    # Required edge case: < and > in link text must be escaped.
    out = render("[<script>alert(1)</script>](https://example.com)")
    assert '<a href="https://example.com">' in out
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in out
    assert "<script>" not in out


def test_link_url_not_escaped():
    # URL ampersands must NOT be touched (we keep them raw).
    out = render("[q](https://example.com/x?a=1&b=2)")
    assert 'href="https://example.com/x?a=1&b=2"' in out


def test_amp_in_text_escaped():
    out = render("a & b")
    assert "a &amp; b" in out


def test_lt_gt_in_paragraph_escaped():
    out = render("1 < 2 > 0")
    assert "1 &lt; 2 &gt; 0" in out


# ---------- Blockquote ----------

def test_blockquote():
    assert render("> quoted") == "<blockquote>quoted</blockquote>"


def test_blockquote_with_bold():
    out = render("> very **bold**")
    assert out == "<blockquote>very <strong>bold</strong></blockquote>"


# ---------- Lexer sanity ----------

def test_lexer_fenced_code_token():
    toks = tokenize("```\nhi\n```")
    assert any(t['type'] == 'fenced_code' for t in toks)


def test_lexer_header_level():
    toks = tokenize("### h3")
    headers = [t for t in toks if t['type'] == 'header']
    assert headers and headers[0]['level'] == 3


# ---------- Combined / integration ----------

def test_multi_block_document():
    md = "# Title\n\nA paragraph with **bold**.\n\n- one\n- two\n"
    out = render(md)
    assert "<h1>Title</h1>" in out
    assert "<p>A paragraph with <strong>bold</strong>.</p>" in out
    assert "<ul><li>one</li><li>two</li></ul>" in out

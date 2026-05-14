"""Tests for the NFA regex engine.

Covers literals, dot, quantifiers, alternation, char classes, grouping,
anchors, escapes, and pathological patterns (with simulation cap).
"""

import pytest

from regex_engine import compile, ParseError


# ---------------------------------------------------------------------------
# Literals & basic matching
# ---------------------------------------------------------------------------

def test_empty_pattern_matches_empty_string():
    r = compile("")
    assert r.match("") == ""


def test_empty_pattern_matches_at_start_of_any_string():
    r = compile("")
    assert r.match("abc") == ""


def test_single_literal_match():
    r = compile("a")
    assert r.match("a") == "a"


def test_single_literal_no_match():
    r = compile("a")
    assert r.match("b") is None


def test_multi_literal_concat():
    r = compile("abc")
    assert r.match("abcdef") == "abc"


def test_literal_search_finds_substring():
    r = compile("cat")
    assert r.search("the cat sat") == (4, 7, "cat")


# ---------------------------------------------------------------------------
# Dot
# ---------------------------------------------------------------------------

def test_dot_matches_any_char():
    r = compile("a.c")
    assert r.match("abc") == "abc"
    assert r.match("a_c") == "a_c"
    assert r.match("a c") == "a c"


def test_dot_does_not_match_newline():
    r = compile("a.c")
    assert r.match("a\nc") is None


def test_dot_does_not_match_empty_position():
    r = compile(".")
    assert r.match("") is None


# ---------------------------------------------------------------------------
# Star, plus, optional
# ---------------------------------------------------------------------------

def test_star_zero_match():
    r = compile("a*")
    assert r.match("") == ""
    assert r.match("bbb") == ""


def test_star_many_match():
    r = compile("a*")
    assert r.match("aaaa") == "aaaa"


def test_star_concat_aaab_from_spec():
    r = compile("a*b")
    assert r.match("aaab") == "aaab"
    assert r.match("b") == "b"
    assert r.match("aaa") is None


def test_plus_requires_one():
    r = compile("a+")
    assert r.match("aaa") == "aaa"
    assert r.match("") is None
    assert r.match("b") is None


def test_optional_zero_or_one():
    r = compile("colou?r")
    assert r.match("color") == "color"
    assert r.match("colour") == "colour"
    assert r.match("colouur") is None


# ---------------------------------------------------------------------------
# Alternation & precedence
# ---------------------------------------------------------------------------

def test_alternation_basic():
    r = compile("cat|dog")
    assert r.match("cat") == "cat"
    assert r.match("dog") == "dog"
    assert r.match("bird") is None


def test_alternation_precedence_lower_than_concat():
    # 'ab|cd' is (ab) | (cd), NOT a(b|c)d
    r = compile("ab|cd")
    assert r.match("ab") == "ab"
    assert r.match("cd") == "cd"
    assert r.match("ad") is None
    assert r.match("ac") is None


def test_alternation_with_anchors_precedence():
    # '^a|b$' is (^a) | (b$).
    r = compile("^a|b$")
    assert r.search("apple") is not None  # ^a matches
    assert r.search("crab") is not None   # b$ matches
    assert r.search("xcx") is None        # neither
    assert r.search("zzz") is None


# ---------------------------------------------------------------------------
# Character classes
# ---------------------------------------------------------------------------

def test_char_class_basic():
    r = compile("[abc]")
    assert r.match("a") == "a"
    assert r.match("b") == "b"
    assert r.match("c") == "c"
    assert r.match("d") is None


def test_char_class_range():
    r = compile("[a-z]+")
    assert r.match("hello") == "hello"
    assert r.match("HELLO") is None


def test_char_class_digit_range():
    r = compile("[0-9]+")
    assert r.match("12345") == "12345"
    assert r.match("a1") is None


def test_char_class_negated():
    r = compile("[^x]+")
    assert r.match("abc") == "abc"
    assert r.match("xabc") is None
    assert r.match("abcx") == "abc"


def test_char_class_mixed_chars_and_ranges():
    r = compile("[A-Za-z0-9_]+")
    assert r.match("Foo_42") == "Foo_42"
    assert r.match("!nope") is None


def test_char_class_escaped_special():
    r = compile(r"[\.\*]")
    assert r.match(".") == "."
    assert r.match("*") == "*"
    assert r.match("a") is None


# ---------------------------------------------------------------------------
# Grouping
# ---------------------------------------------------------------------------

def test_group_changes_precedence():
    r = compile("a(b|c)d")
    assert r.match("abd") == "abd"
    assert r.match("acd") == "acd"
    assert r.match("ad") is None


def test_group_with_star():
    r = compile("(ab)*")
    assert r.match("ababab") == "ababab"
    assert r.match("") == ""
    assert r.match("aba") == "ab"


def test_nested_groups():
    r = compile("((ab)+|c)d")
    assert r.match("ababd") == "ababd"
    assert r.match("cd") == "cd"
    assert r.match("d") is None


# ---------------------------------------------------------------------------
# Anchors
# ---------------------------------------------------------------------------

def test_start_anchor_match():
    r = compile("^abc")
    assert r.match("abcdef") == "abc"
    # 'abc' not at start should not match via search:
    assert r.search("xxabc") is None


def test_end_anchor_match():
    r = compile("abc$")
    assert r.search("xxabc") == (2, 5, "abc")
    assert r.search("abcxx") is None


def test_both_anchors_full_match():
    r = compile("^hello$")
    assert r.match("hello") == "hello"
    assert r.match("hello!") is None
    assert r.search("hello world") is None


# ---------------------------------------------------------------------------
# Escapes
# ---------------------------------------------------------------------------

def test_escape_dot_literal():
    r = compile(r"a\.b")
    assert r.match("a.b") == "a.b"
    assert r.match("axb") is None


def test_escape_star_literal():
    r = compile(r"a\*b")
    assert r.match("a*b") == "a*b"
    assert r.match("aaab") is None


def test_escape_backslash():
    r = compile(r"\\")
    assert r.match("\\") == "\\"


def test_escape_paren_literal():
    r = compile(r"\(hi\)")
    assert r.match("(hi)") == "(hi)"


# ---------------------------------------------------------------------------
# findall
# ---------------------------------------------------------------------------

def test_findall_simple():
    r = compile("[a-z]+")
    assert r.findall("the 42 quick 7 foxes") == ["the", "quick", "foxes"]


def test_findall_overlap_avoidance():
    r = compile("aa")
    assert r.findall("aaaa") == ["aa", "aa"]


def test_findall_empty_pattern_terminates():
    r = compile("a*")
    # Should not infinite-loop on a*; we accept any finite result.
    result = r.findall("aaa")
    assert len(result) <= len("aaa") + 1
    # First non-trivial match should be 'aaa'
    assert "aaa" in result


# ---------------------------------------------------------------------------
# Pathological patterns - sim cap should prevent runaway
# ---------------------------------------------------------------------------

def test_pathological_nested_star_terminates():
    """The classic catastrophic backtracking case for backtracking engines.
    NFA simulation handles it in linear time, but we still validate it
    terminates and produces a sensible answer."""
    r = compile("(a*)*")
    # Should match the entire 'aaaaaaaaaa' (or at least not hang).
    out = r.match("a" * 20)
    assert out is not None
    # And empty input still OK:
    assert r.match("") == ""


def test_pathological_alt_star_terminates():
    r = compile("(a|a)*")
    out = r.match("a" * 20)
    assert out is not None


# ---------------------------------------------------------------------------
# Combined / integration-ish
# ---------------------------------------------------------------------------

def test_email_ish_pattern():
    # Crude email matcher
    r = compile("[a-z]+@[a-z]+\\.[a-z]+")
    assert r.match("bob@example.com") == "bob@example.com"
    assert r.match("bob@@example.com") is None
    assert r.match("noatsign.com") is None


def test_phone_ish_pattern():
    r = compile("[0-9]+-[0-9]+-[0-9]+")
    assert r.match("123-456-7890") == "123-456-7890"
    assert r.match("123-abc-7890") is None


def test_search_returns_first_match():
    r = compile("[0-9]+")
    assert r.search("abc 12 def 345") == (4, 6, "12")


def test_full_match_helper():
    r = compile("ab+c")
    assert r.fullmatch("abbbc") == "abbbc"
    assert r.fullmatch("abbbcd") is None


# ---------------------------------------------------------------------------
# Parse errors
# ---------------------------------------------------------------------------

def test_parse_error_dangling_quantifier():
    with pytest.raises(ParseError):
        compile("*abc")


def test_parse_error_unbalanced_paren():
    with pytest.raises(ParseError):
        compile("(abc")


def test_parse_error_dangling_backslash():
    with pytest.raises(ParseError):
        compile("abc\\")


def test_parse_error_unterminated_class():
    with pytest.raises(ParseError):
        compile("[abc")


# ---------------------------------------------------------------------------
# Hardening iteration: leftmost-longest semantics & misc edge cases
# ---------------------------------------------------------------------------

def test_star_is_greedy():
    """a* should match as many a's as possible."""
    r = compile("a*")
    assert r.match("aaaa") == "aaaa"  # not "" or "a"


def test_alternation_first_match_wins_for_equal_length():
    """When both branches match equal lengths from the same position, either
    is acceptable but it should be deterministic and non-empty."""
    r = compile("foo|foobar")
    m = r.match("foobar")
    assert m in ("foo", "foobar")


def test_plus_inside_group_with_alternation():
    r = compile("(ab|cd)+")
    assert r.match("ababcd") == "ababcd"
    assert r.match("cdab") == "cdab"
    assert r.match("xyz") is None


def test_anchored_full_with_alternation():
    r = compile("^(yes|no)$")
    assert r.match("yes") == "yes"
    assert r.match("no") == "no"
    assert r.match("maybe") is None


def test_class_with_hyphen_at_end():
    """`[abc-]` should treat trailing '-' as a literal."""
    r = compile("[abc-]+")
    assert r.match("a-b-c") == "a-b-c"


def test_search_no_match_returns_none():
    r = compile("zzz")
    assert r.search("abcdef") is None
    assert r.findall("abcdef") == []


def test_unicode_literal_matches():
    r = compile("café")
    assert r.match("café") == "café"

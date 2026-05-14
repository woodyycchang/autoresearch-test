"""Test suite for the NFA-based regex engine.

We import `matcher.compile` as `compile_re` to avoid shadowing the builtin.
"""

import time

import pytest

from matcher import compile as compile_re


# --- Literals & basic concatenation ----------------------------------------

def test_literal_match():
    r = compile_re("abc")
    assert r.match("abc") == 3
    assert r.match("abcd") == 3


def test_literal_no_match():
    r = compile_re("abc")
    assert r.match("abd") is None
    assert r.match("ab") is None


def test_empty_pattern_matches_empty():
    r = compile_re("")
    assert r.match("") == 0
    assert r.match("hello") == 0


# --- Repetition: *, +, ? ---------------------------------------------------

def test_star_zero_or_more():
    r = compile_re("a*b")
    assert r.match("b") == 1
    assert r.match("ab") == 2
    assert r.match("aaab") == 4


def test_star_only():
    r = compile_re("a*")
    assert r.match("") == 0
    assert r.match("aaaa") == 4
    assert r.match("bbb") == 0  # zero-width match at start


def test_plus_one_or_more():
    r = compile_re("a+b")
    assert r.match("ab") == 2
    assert r.match("aaab") == 4
    assert r.match("b") is None


def test_question_optional():
    r = compile_re("ab?c")
    assert r.match("ac") == 2
    assert r.match("abc") == 3
    assert r.match("abbc") is None


def test_greedy_star_consumes_max():
    r = compile_re("a*")
    assert r.match("aaaaaa") == 6


# --- Any (.) --------------------------------------------------------------

def test_dot_any_char():
    r = compile_re("a.c")
    assert r.match("abc") == 3
    assert r.match("a.c") == 3
    assert r.match("a c") == 3


def test_dot_does_not_match_newline():
    r = compile_re("a.c")
    assert r.match("a\nc") is None


def test_dot_star():
    r = compile_re(".*")
    assert r.match("anything") == len("anything")


# --- Alternation -----------------------------------------------------------

def test_alternation_basic():
    r = compile_re("cat|dog")
    assert r.match("cat") == 3
    assert r.match("dog") == 3
    assert r.match("bird") is None


def test_alternation_precedence_lower_than_concat():
    # `ab|cd` should parse as (ab)|(cd), not a(b|c)d.
    r = compile_re("ab|cd")
    assert r.match("ab") == 2
    assert r.match("cd") == 2
    assert r.match("ac") is None
    assert r.match("abd") == 2  # 'ab' prefix accepted


def test_alternation_in_group():
    r = compile_re("(cat|dog)s")
    assert r.match("cats") == 4
    assert r.match("dogs") == 4
    assert r.match("birds") is None


# --- Character classes ----------------------------------------------------

def test_charclass_basic():
    r = compile_re("[abc]")
    assert r.match("a") == 1
    assert r.match("b") == 1
    assert r.match("c") == 1
    assert r.match("d") is None


def test_charclass_negated():
    r = compile_re("[^x]+")
    assert r.match("abc") == 3
    assert r.match("xyz") is None  # leading 'x' rejected
    assert r.match("abxcd") == 2


def test_charclass_range():
    r = compile_re("[a-z]+")
    assert r.match("hello") == 5
    assert r.match("HELLO") is None
    assert r.match("hi5") == 2


def test_charclass_digit_range():
    r = compile_re("[0-9]+")
    assert r.match("12345") == 5
    assert r.match("abc") is None


def test_charclass_mixed():
    r = compile_re("[a-zA-Z0-9]+")
    assert r.match("Hello42") == 7
    assert r.match("__bad") is None  # underscore not in class


def test_charclass_with_special_chars_treated_literal():
    # Inside [], '.' is a literal '.'.
    r = compile_re("[.]")
    assert r.match(".") == 1
    assert r.match("a") is None


# --- Grouping with repetition ---------------------------------------------

def test_group_with_star():
    r = compile_re("(ab)*")
    assert r.match("") == 0
    assert r.match("ababab") == 6
    assert r.match("abc") == 2


def test_group_with_plus():
    r = compile_re("(ab)+")
    assert r.match("ab") == 2
    assert r.match("abab") == 4
    assert r.match("a") is None


# --- Anchors --------------------------------------------------------------

def test_start_anchor():
    r = compile_re("^abc")
    assert r.match("abc") == 3
    assert r.search("xxabc") is None  # ^ forces start


def test_end_anchor():
    r = compile_re("abc$")
    assert r.match("abc") == 3
    assert r.search("abcd") is None  # $ forces end


def test_both_anchors():
    r = compile_re("^abc$")
    assert r.match("abc") == 3
    assert r.match("abcd") is None
    assert r.match("xabc") is None


def test_anchor_precedence_in_alternation():
    # `^a|b$` should mean (^a)|(b$), not ^(a|b)$
    r = compile_re("^a|b$")
    assert r.search("apple") == (0, 1)  # ^a matches
    assert r.search("crab") == (3, 4)  # b at end
    assert r.search("cab") == (2, 3)  # 'b' at end
    assert r.search("ban") is None  # 'b' not at end, 'a' not at start


# --- search / findall -----------------------------------------------------

def test_search_finds_first():
    r = compile_re("abc")
    assert r.search("xxabcyy") == (2, 5)


def test_search_no_match():
    r = compile_re("xyz")
    assert r.search("abc") is None


def test_findall_basic():
    r = compile_re("a+")
    assert r.findall("baaa abc aaaa") == ["aaa", "a", "aaaa"]


def test_findall_no_match():
    r = compile_re("z+")
    assert r.findall("abc") == []


# --- Escapes & special characters -----------------------------------------

def test_escaped_dot():
    r = compile_re(r"a\.b")
    assert r.match("a.b") == 3
    assert r.match("axb") is None


def test_escaped_star():
    r = compile_re(r"a\*b")
    assert r.match("a*b") == 3
    assert r.match("aab") is None


def test_escaped_paren():
    r = compile_re(r"\(abc\)")
    assert r.match("(abc)") == 5


def test_escape_d_digit():
    r = compile_re(r"\d+")
    assert r.match("12345") == 5
    assert r.match("abc") is None


def test_escape_w_word():
    r = compile_re(r"\w+")
    assert r.match("hello_world42") == len("hello_world42")
    assert r.match("!!!") is None


def test_escape_s_whitespace():
    r = compile_re(r"\s+")
    assert r.match("   x") == 3
    assert r.match("xxx") is None


# --- Combinations & complex patterns --------------------------------------

def test_email_like():
    r = compile_re(r"[a-z]+@[a-z]+\.[a-z]+")
    assert r.match("foo@bar.com") == len("foo@bar.com")
    assert r.match("foo@bar") is None


def test_ip_like():
    r = compile_re(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")
    assert r.match("192.168.1.1") == len("192.168.1.1")
    assert r.match("abc.def.ghi.jkl") is None


def test_alternation_with_repetition():
    r = compile_re("(a|b)+")
    assert r.match("ababab") == 6
    assert r.match("aaa") == 3
    assert r.match("c") is None


# --- Pathological patterns terminate (the famous (a*)*) -------------------

def test_nested_star_terminates_quickly():
    r = compile_re("(a*)*b")
    start = time.time()
    # 30 'a's then a 'b' — would explode under naive backtracking but is
    # linear with NFA simulation.
    assert r.match("a" * 30 + "b") == 31
    elapsed = time.time() - start
    assert elapsed < 1.0, f"NFA simulation too slow: {elapsed:.2f}s"


def test_nested_star_no_match_terminates():
    r = compile_re("(a*)*b")
    start = time.time()
    assert r.match("a" * 30 + "c") is None
    elapsed = time.time() - start
    assert elapsed < 1.0


def test_complex_alternation_with_anchors():
    r = compile_re("^(foo|bar)$")
    assert r.match("foo") == 3
    assert r.match("bar") == 3
    assert r.match("foobar") is None
    assert r.match("fo") is None

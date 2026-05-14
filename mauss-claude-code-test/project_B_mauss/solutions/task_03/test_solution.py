"""Tests for find_anagrams."""

import pytest

from solution import find_anagrams


def test_basic_anagrams():
    assert find_anagrams("listen", ["silent", "enlist", "google", "inlets"]) == [
        "silent",
        "enlist",
        "inlets",
    ]


def test_case_insensitive():
    assert find_anagrams("Listen", ["SILENT", "Enlist", "Hello"]) == [
        "SILENT",
        "Enlist",
    ]


def test_whitespace_ignored():
    assert find_anagrams("conversation", ["voices rant on", "no answer"]) == [
        "voices rant on",
    ]


def test_target_excluded_when_identical():
    # The exact target string in words must NOT be returned.
    assert find_anagrams("abc", ["abc", "bca", "cab"]) == ["bca", "cab"]


def test_target_value_match_but_different_case_is_included():
    # Same letters, different casing => still an anagram, not the target itself.
    assert find_anagrams("abc", ["ABC", "abc", "xyz"]) == ["ABC"]


def test_no_matches_returns_empty_list():
    assert find_anagrams("hello", ["world", "python"]) == []


def test_empty_words_iterable():
    assert find_anagrams("abc", []) == []


def test_empty_target_matches_empty_or_whitespace_words():
    # Empty target's signature is (); only whitespace-only or empty words match.
    assert find_anagrams("", ["", "   ", "a"]) == ["   "]


def test_preserves_order_and_duplicates():
    assert find_anagrams("ab", ["ba", "ab", "ba", "BA"]) == ["ba", "ba", "BA"]


def test_accepts_generator_input():
    def gen():
        yield "silent"
        yield "hello"
        yield "inlets"

    assert find_anagrams("listen", gen()) == ["silent", "inlets"]


def test_non_string_target_raises():
    with pytest.raises(TypeError):
        find_anagrams(123, ["abc"])


def test_non_string_word_raises():
    with pytest.raises(TypeError):
        find_anagrams("abc", ["bca", 42])


def test_unicode_anagrams_case_insensitive():
    # Use clearly-cased unicode letters that have well-defined .lower().
    assert find_anagrams("Cafe", ["face", "FACE", "feca"]) == ["face", "FACE", "feca"]


def test_punctuation_is_significant():
    # Only whitespace is ignored; punctuation must match exactly.
    assert find_anagrams("a!b", ["b!a", "ab!", "a b !"]) == ["b!a", "ab!", "a b !"]
    assert find_anagrams("ab", ["a!b"]) == []

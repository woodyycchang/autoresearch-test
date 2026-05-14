"""Unit tests for find_anagrams."""

import pytest

from solution import find_anagrams


class TestBasic:
    def test_simple_anagrams(self):
        assert find_anagrams("listen", ["enlist", "silent", "google", "tinsel"]) == [
            "enlist",
            "silent",
            "tinsel",
        ]

    def test_no_anagrams(self):
        assert find_anagrams("hello", ["world", "python", "code"]) == []

    def test_empty_words_list(self):
        assert find_anagrams("listen", []) == []

    def test_single_anagram(self):
        assert find_anagrams("abc", ["cab"]) == ["cab"]


class TestCaseInsensitive:
    def test_target_uppercase(self):
        assert find_anagrams("LISTEN", ["silent", "enlist"]) == ["silent", "enlist"]

    def test_words_mixed_case(self):
        assert find_anagrams("listen", ["Silent", "ENLIST", "TinSel"]) == [
            "Silent",
            "ENLIST",
            "TinSel",
        ]

    def test_both_mixed_case(self):
        assert find_anagrams("LiStEn", ["SiLeNt"]) == ["SiLeNt"]


class TestWhitespace:
    def test_whitespace_in_target(self):
        # "the eyes" -> letters "theeyes" -> matches "they see"
        assert find_anagrams("the eyes", ["they see"]) == ["they see"]

    def test_whitespace_in_words(self):
        assert find_anagrams("abc", ["c b a", "a  b  c", "xyz"]) == ["c b a", "a  b  c"]

    def test_tabs_and_newlines_ignored(self):
        assert find_anagrams("abc", ["a\tb\nc"]) == ["a\tb\nc"]


class TestTargetExclusion:
    def test_target_in_words_excluded(self):
        # exact same string as target should be excluded
        assert find_anagrams("listen", ["listen", "silent"]) == ["silent"]

    def test_target_case_variant_kept(self):
        # different case = different string, still excluded because
        # case-insensitively the same word is "the target itself"
        # per spec: "the target itself is NOT considered an anagram of itself
        # unless it appears in words as a separate entry."
        # "LISTEN" is a separate entry from target "listen" so it's kept.
        assert find_anagrams("listen", ["LISTEN", "silent"]) == ["LISTEN", "silent"]

    def test_target_with_extra_whitespace(self):
        # "lis ten" is a distinct string from "listen", so it counts as
        # a separate entry and IS an anagram.
        assert find_anagrams("listen", ["lis ten", "silent"]) == ["lis ten", "silent"]

    def test_only_target_in_words(self):
        assert find_anagrams("listen", ["listen"]) == []


class TestDuplicates:
    def test_duplicate_anagrams_preserved(self):
        assert find_anagrams("abc", ["cab", "cab", "bac"]) == ["cab", "cab", "bac"]


class TestOrder:
    def test_results_preserve_input_order(self):
        words = ["silent", "google", "tinsel", "enlist"]
        assert find_anagrams("listen", words) == ["silent", "tinsel", "enlist"]


class TestEdgeCases:
    def test_empty_target(self):
        # empty target has empty signature; only empty-after-normalize words
        # could match, but we skip those.
        assert find_anagrams("", ["", "  ", "abc"]) == []

    def test_target_all_whitespace(self):
        assert find_anagrams("   ", ["abc", ""]) == []

    def test_different_length_not_anagram(self):
        assert find_anagrams("abc", ["abcd", "ab"]) == []

    def test_punctuation_matters(self):
        # punctuation is not stripped (only whitespace per spec)
        assert find_anagrams("abc", ["a!bc"]) == []

    def test_digits_supported(self):
        assert find_anagrams("123", ["321", "213", "12 3"]) == ["321", "213", "12 3"]

    def test_unicode_letters(self):
        # case-insensitive should work for unicode via .lower()
        assert find_anagrams("éa", ["aé"]) == ["aé"]

    def test_iterable_input(self):
        # words can be any iterable, not just a list
        def gen():
            yield "silent"
            yield "google"
        assert find_anagrams("listen", gen()) == ["silent"]

    def test_returns_list_type(self):
        assert isinstance(find_anagrams("a", ["a", "b"]), list)


class TestRealistic:
    def test_classic_anagrams(self):
        words = ["dusty", "study", "night", "thing", "rats", "star", "arts"]
        # target "study": anagram is "dusty"; "study" itself excluded.
        assert find_anagrams("study", words) == ["dusty"]

    def test_phrase_anagram(self):
        # "Dormitory" -> "Dirty room" (ignore whitespace, case)
        assert find_anagrams("Dormitory", ["Dirty room", "rooms"]) == ["Dirty room"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""Anagram finder.

Provides ``find_anagrams(target, words)`` which returns every string in
``words`` that is an anagram of ``target``. Matching is case-insensitive and
ignores whitespace. The exact ``target`` string (same object/value) is not
considered an anagram of itself, but if a separate equal entry appears in
``words`` it is included.
"""

from typing import Iterable, List


def _signature(s: str) -> tuple:
    """Return a canonical, order-independent fingerprint of ``s``.

    Whitespace is dropped and characters are lowercased before sorting so
    that "Listen" and "Silent " share the same signature.
    """
    cleaned = [ch.lower() for ch in s if not ch.isspace()]
    cleaned.sort()
    return tuple(cleaned)


def find_anagrams(target: str, words: Iterable[str]) -> List[str]:
    """Return the subset of ``words`` that are anagrams of ``target``.

    Rules:
      * Case-insensitive comparison.
      * Whitespace inside either string is ignored.
      * ``target`` itself is not an anagram of itself: a candidate that is
        equal to ``target`` (same string value) is excluded. Other entries
        in ``words`` that happen to share the same characters are kept,
        preserving their original order and any duplicates.
    """
    if not isinstance(target, str):
        raise TypeError("target must be a string")

    target_sig = _signature(target)
    result: List[str] = []
    for word in words:
        if not isinstance(word, str):
            raise TypeError("every entry in words must be a string")
        # Exclude the target itself (by value); other equal-by-signature
        # words are valid anagrams.
        if word == target:
            continue
        if _signature(word) == target_sig:
            result.append(word)
    return result

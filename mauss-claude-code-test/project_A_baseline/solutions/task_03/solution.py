"""Find anagrams of a target string from a list of words."""


def _normalize(s):
    """Normalize a string for anagram comparison: lowercase, no whitespace."""
    return "".join(s.lower().split())


def _signature(s):
    """Return a canonical signature for anagram comparison.

    Two strings are anagrams iff they share the same signature (sorted
    normalized characters).
    """
    return tuple(sorted(_normalize(s)))


def find_anagrams(target, words):
    """Return all strings in ``words`` that are anagrams of ``target``.

    Rules:
      * Case-insensitive comparison.
      * Whitespace is ignored when computing letters.
      * The target itself is NOT considered an anagram of itself: a word
        equal to ``target`` (after normalization, i.e. same letters in the
        same order, case-insensitively, ignoring whitespace) is excluded.
      * If the target appears in ``words`` as an identical entry (after
        normalization), that exact entry is excluded.
      * Otherwise, anagrams found in ``words`` are returned preserving
        their original form and order.

    Args:
        target: The reference string.
        words: An iterable of candidate strings.

    Returns:
        A list of strings from ``words`` that are anagrams of ``target``.
    """
    target_sig = _signature(target)

    results = []
    for word in words:
        word_norm = _normalize(word)
        # Skip empties: empty has no letters so it's a degenerate case.
        if not word_norm:
            continue
        # The word is "the target itself" only when it is the exact same
        # string as ``target``. Any other entry (different case, different
        # spacing, different letter order) is a "separate entry" per spec
        # and qualifies if it's an anagram.
        if word == target:
            continue
        if _signature(word) == target_sig:
            results.append(word)
    return results

# Handoff — Task 03

## What I built

`solution.py` exposes `find_anagrams(target, words)` which returns every
string in `words` that is an anagram of `target`.

### Behavior

- **Case-insensitive**: comparison uses `.lower()`.
- **Whitespace-insensitive**: all whitespace (spaces, tabs, newlines) is
  stripped before comparing letters. Other punctuation is NOT stripped.
- **Anagram detection**: two strings are anagrams iff their normalized
  characters (sorted) are equal.
- **Self-exclusion**: only a word that is byte-for-byte identical to
  `target` is excluded. Any string that differs (different case,
  different spacing, different letter order) counts as a "separate
  entry" per the spec and is included if it's an anagram. So with
  target `"listen"`, the entry `"LISTEN"` is kept.
- **Order**: results preserve the input order of `words`.
- **Duplicates**: kept (a word may legitimately appear multiple times).
- **Input**: `words` can be any iterable.

### Files

- `solution.py` — implementation. Helpers `_normalize` and `_signature`
  factor out the normalization logic.
- `test_solution.py` — pytest suite covering basics, case-insensitivity,
  whitespace handling, target exclusion, duplicates, order preservation,
  empty/edge cases (empty target, whitespace-only target, mismatched
  lengths, punctuation, digits, unicode), iterables, and realistic
  phrase anagrams.

### How to run

```
cd <this dir>
pytest test_solution.py -v
```

Stdlib only; no external deps beyond pytest.

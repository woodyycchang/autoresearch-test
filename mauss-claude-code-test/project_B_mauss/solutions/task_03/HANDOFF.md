# Task 03 Handoff — Implementer to Validator

## ACCEPT
I acknowledge the prior work in this project: the Implementer who built
`solutions/task_02/solution.py` established a clear template I followed —
a module docstring, a private `_validate_*` / `_signature` helper that
keeps validation separate from algorithmic logic, explicit type
annotations, and `ValueError`/`TypeError` raised eagerly on malformed
input rather than returning silent wrong answers. I mirrored that style
here (docstring + helper `_signature` + public `find_anagrams`) so the
codebase stays consistent.

## GIVE — what the Validator needs to know

### What was built
- `solution.py` exposes `find_anagrams(target, words) -> list[str]`.
- `test_solution.py` contains 14 pytest tests, all passing
  (verified: `pytest test_solution.py -v` -> `14 passed in 0.03s`).

### Design decisions (and why)
1. **Signature-based matching**: each string is reduced to a sorted tuple
   of its non-whitespace lowercase characters. Two strings are anagrams
   iff their signatures are equal. This is O(n log n) per string and
   avoids the quadratic cost of per-pair comparisons.
2. **Case-insensitivity**: implemented with `str.lower()` on each char.
3. **Whitespace ignored**: implemented with `str.isspace()` filter —
   covers spaces, tabs, newlines, and unicode whitespace uniformly.
   Punctuation is intentionally NOT stripped; the task only mentions
   whitespace.
4. **"Target itself" exclusion**: interpreted as *exact string equality*.
   So `find_anagrams("abc", ["abc"])` returns `[]`, but
   `find_anagrams("abc", ["ABC"])` returns `["ABC"]` because "ABC" is a
   separate string value even though it's the same letters. This is the
   most defensible reading of "the target itself is NOT considered an
   anagram of itself unless it appears in `words` as a separate entry."
5. **Duplicates preserved**: if `words` contains the same anagram twice,
   both copies appear in the output, in input order. Iteration order is
   preserved, supporting generator input.
6. **Strict typing**: non-string `target` or non-string entries in
   `words` raise `TypeError`, matching the defensive style of task_02.

### Potentially ambiguous corners I resolved
- **Empty target**: signature is `()`. Empty string and whitespace-only
  strings in `words` match; non-empty strings do not. Covered by
  `test_empty_target_matches_empty_or_whitespace_words`.
- **`target` not in `words`**: the exclusion rule is a no-op; this is
  the common case and works as expected.
- **Generator/iterable input**: `words` is typed `Iterable[str]`, so a
  generator works. Covered by `test_accepts_generator_input`.

### Constraint compliance
- Python stdlib + pytest only — no external deps imported.
- `output.txt` was deliberately NOT created (project constraint
  overrides the task description's instruction to write one).

### How to verify
```
cd solutions/task_03/
pytest test_solution.py -v
```
Expected: 14 passed.

## RECIPROCATE
My contribution: a fully-tested `find_anagrams` implementation plus a
documented interpretation of the task's ambiguous "target itself"
clause. This builds on the task_02 Implementer's pattern of
shape-validation-plus-pure-algorithm by extending that same separation
(`_signature` helper + public function + `TypeError` on bad input) to
the anagram domain, so the Validator can apply the same review lens
used on task_02 without re-learning the codebase's conventions.

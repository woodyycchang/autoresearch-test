# Task 08 — NFA Regex Engine

## Result
**PASS — 42/42 tests pass** (`python3 -m pytest tests/ -v`, ~0.04s).

## Architecture

Three modules, each with a single responsibility:

- **`nfa.py`** — Thompson-style NFA primitives: `State`, `Fragment`, and
  constructors (`make_literal`, `make_any`, `make_concat`, `make_alt`,
  `make_star`, `make_plus`, `make_question`, `make_charclass`). Dangling
  out-edges are tracked as patch callbacks so fragments can be wired together
  without storing back-references.
- **`compiler.py`** — Recursive-descent parser over the grammar
  `alt -> concat ('|' concat)*`, `concat -> factor*`,
  `factor -> atom ('*'|'+'|'?')?`, `atom -> '(' alt ')' | '[' class ']' | '.'
  | anchor | escape | literal`. Handles `[abc]`, `[^xy]`, `[a-z]`, ranges
  inside classes, and escapes (`\d \D \w \W \s \S \n \t \r` plus any escaped
  literal like `\.`, `\*`, `\\`). Anchors `^` and `$` compile to special
  zero-width transitions, not a global flag — this lets `^a|b$` parse
  correctly as `(^a)|(b$)`.
- **`matcher.py`** — Thompson NFA simulator (parallel-states epsilon closure)
  exposing `compile()` returning a `Regex` with `.match`, `.search`,
  `.fullmatch`, `.findall`. Anchor transitions are evaluated positionally
  during epsilon closure. A `_StepBudget` hard-caps simulation work at
  1M state ticks as belt-and-suspenders for pathological inputs.

## Key design choices

1. **Parallel-state simulation** instead of backtracking — `(a*)*b` against
   30 `a`'s runs in microseconds and is tested with a 1s deadline.
2. **Anchors as NFA transitions, not flags** — fixed the initial failing
   test `^a|b$`. The first attempt set an `anchored_start` flag whenever the
   pattern started with `^`, which incorrectly anchored the `b$` branch.
3. **`.` excludes `\n`** matching Python default semantics, asserted by
   `test_dot_does_not_match_newline`.
4. **Greedy `*`/`+`** via longest accepted prefix during simulation rather
   than per-quantifier greedy backtracking.
5. **Charclass parsing** treats `[.]` as a literal dot and supports escapes
   inside classes (e.g. `[\\d]` becomes the digit class).

## Test coverage (42 tests)
Literals & no-match, empty pattern, `*`/`+`/`?` quantifiers, greediness,
`.` semantics including newline rejection, alternation precedence vs
concat, alternation in groups, `[abc]`/`[^x]`/`[a-z]` charclasses, mixed
classes, literal-dot-in-class, group repetition, start/end anchors and
their precedence, `search` / `findall` (including no-match and multiple
hits), escapes (`\.`, `\*`, `\(`, `\d`, `\w`, `\s`), composite patterns
(email-like, IP-like), and two pathological-pattern termination tests with
wall-clock assertions.

## Iteration
One iteration. Initial run was 41/42; failing test was anchor precedence
in alternation. Removed the global `anchored_start` flag, relying solely
on per-position anchor transitions in the NFA — second run hit 42/42.

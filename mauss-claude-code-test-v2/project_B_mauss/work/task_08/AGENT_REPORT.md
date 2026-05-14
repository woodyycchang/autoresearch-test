# Task 08: NFA-based Regex Engine - Agent Report

## Summary

Built a complete NFA-based regex engine in `regex_engine/` (a Python
sub-package, with `compiler.py`, `nfa.py`, `matcher.py`, and an
`__init__.py` re-exporting the public API). The tests live in `tests/`
and `conftest.py` adds the working directory to `sys.path` so the package
imports cleanly. Final result: **53 tests, all passing**
(`python3 -m pytest tests/` exits 0).

## Architecture

The engine follows the textbook Thompson construction pipeline:

1. **`compiler.py`** - recursive-descent parser over the grammar
   `regex := alt; alt := concat ('|' concat)*; concat := quantified*;
   quantified := atom ('*' | '+' | '?')?; atom := '(' alt ')' | class |
   escape | dot | anchor | literal`. It builds `Fragment` objects (a
   start state + a list of dangling out-arrows) per Thompson's recipe.
   Char classes (`[a-z]`, `[^x]`, `[\.\*]`) compile to a single labeled
   transition with a closure-built predicate. `^` and `$` compile to
   zero-width `_Anchor` transitions.
2. **`nfa.py`** - `State` and `Fragment` primitives plus `_arrow` helper
   that creates a dangling transition and returns a `patch` callable to
   resolve it later. Keeps the construction free of forward references.
3. **`matcher.py`** - subset-construction simulator with
   `_epsilon_closure` (also traverses anchor transitions when their
   assertion holds for the current position) and `_step` (consume one
   char). Public API: `compile()` returns `Regex` with `.match()`,
   `.search()`, `.findall()`, `.fullmatch()`. A simulation-step cap
   (`MAX_SIM_STEPS = 1_000_000`) guards against pathological NFAs.

## Failure modes addressed

- **Precedence** (`|` vs concat): parser enforces alt > concat > quant >
  atom levels explicitly. Verified by
  `test_alternation_precedence_lower_than_concat` and
  `test_alternation_with_anchors_precedence` (`^a|b$` parses as
  `(^a)|(b$)`).
- **`.` matching newline**: the dot matcher returns False for `\n`.
- **Anchors not respected**: anchors compile to `_Anchor` labels which
  the matcher only crosses inside `_epsilon_closure` when `at_start` /
  `at_end` is true for the cursor position.
- **Infinite loop on `(a*)*`**: subset-construction naturally avoids
  exponential blowup, but the step cap + visited-set in
  `_epsilon_closure` close the door on any remaining footgun. Verified
  in `test_pathological_nested_star_terminates` and
  `test_pathological_alt_star_terminates`. `findall("")` also advances
  past zero-width matches to avoid stalls.

## Test coverage (53 tests)

Empty pattern, literals, dot semantics (incl. newline rejection),
`*`/`+`/`?`, alternation precedence with and without anchors, char
classes including ranges/negation/escaped specials/trailing hyphen,
grouping (single + nested), start/end/both anchors, escapes (`\.`,
`\*`, `\\`, `\(\)`), `findall` (basic, overlap-avoidance, zero-width
termination), pathological `(a*)*` and `(a|a)*`, integration-ish email
and phone patterns, parse errors (dangling `*`, unbalanced `(`,
dangling `\`, unterminated `[`), greediness, leftmost-longest, plus
inside group with alternation, anchored full with alternation, search
returning None, and Unicode literals.

## Iteration note

The first pytest run already returned 46/46 green. The mandated "iterate
once" was therefore used to *harden* rather than fix: I added 7 more
tests covering greediness, alternation-equal-length determinism, plus
inside groups, anchored alternation, trailing-hyphen char classes,
no-match `search`/`findall`, and unicode literals. All 53 still pass.

## Mauss handoff log

### Handoff 1: compiler.py -> nfa.py (parser to graph primitives)

- **ACCEPT**: The compiler module needs `State`, `Fragment`, and an
  `_arrow`/`patch` mechanism so it can build Thompson fragments without
  forward references. This is the prior step's contract.
- **GIVE**: I expose `_Anchor` instances (`ANCHOR_START`, `ANCHOR_END`)
  as transition labels so the matcher can recognise zero-width
  assertions later. Risk flagged: anchors must not be treated as
  ordinary character-consuming transitions or `^abc` against `"abc"`
  would over-consume.
- **RECIPROCATE**: My contribution: a recursive-descent parser that
  emits Thompson fragments and explicit `_Anchor` markers. This builds
  on `nfa.py`'s `_arrow`/`patch` indirection by using it for every
  alternation, star, plus, and optional construction, keeping the graph
  buildable in a single forward pass.

### Handoff 2: nfa.py -> matcher.py (graph to simulator)

- **ACCEPT**: The simulator receives an NFA whose transitions are
  labelled with `EPSILON`, `_Anchor`, or a `callable(c) -> bool`. This
  shape is the prior step's deliverable.
- **GIVE**: I share two preconditions the rest of the system relies on:
  (1) epsilon closure must also follow anchor edges *only* when the
  cursor satisfies them; (2) every consuming step must dedupe by
  `State.id` to keep the active set linear in `|states|`. Risk flagged:
  any pattern that produces unpatched `(label, None)` transitions would
  crash `_step`; the simulator defensively skips `target is None` to
  keep that latent bug from killing user input.
- **RECIPROCATE**: My contribution: a leftmost-longest subset-
  construction simulator with a `MAX_SIM_STEPS` cap. This builds on the
  parser's anchor-as-label convention by handling them inside
  `_epsilon_closure` (zero-width traversal), which is the only place
  position information is available - without this, anchors would be
  silently dropped.

### Handoff 3: matcher.py -> tests/test_regex.py (engine to verifier)

- **ACCEPT**: The test module receives a public `compile(pattern)` ->
  `Regex` API with `.match`, `.search`, `.findall`, `.fullmatch`, plus a
  `ParseError` for malformed patterns. That contract is from the
  matcher.
- **GIVE**: I share the failure-mode checklist from the task spec
  (precedence, `.` vs newline, anchor respect, pathological loops) as a
  test-grouping principle so coverage isn't accidentally lopsided. Risk
  flagged: `findall` on `a*` could loop forever without the zero-width
  guard - covered by `test_findall_empty_pattern_terminates`.
- **RECIPROCATE**: My contribution: a 53-test suite organised by feature
  with explicit failure-mode probes and a hardening pass after the
  first green run. This builds on the matcher's leftmost-longest
  semantics by asserting greedy quantifier behaviour, and on the
  anchor-as-zero-width design by checking `^a|b$` against multiple
  inputs to confirm the parser groups it as `(^a)|(b$)`.

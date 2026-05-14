# Task 08 — Handoff (Implementer -> Validator)

## ACCEPT
Acknowledging prior work: the Planner/task author defined Task 08 as a Roman
numeral converter with two paired functions, `to_roman(n)` for `n` in
`[1, 3999]` and `from_roman(s)`, using **standard subtractive notation**
(`IV, IX, XL, XC, CD, CM`). The constraint that the supported range is
`1..3999` is the standard ceiling for classical Roman numerals (since `MMMM`
is not standard subtractive form), and I built strictly to that contract.

I also note the task asked for an `output.txt` summary, but the pipeline
constraints explicitly forbid `output.txt`, so I do not create one — the
summary lives in this HANDOFF instead.

## GIVE — what the Validator needs to know

### Files
- `solution.py` — `to_roman(n)` and `from_roman(s)`.
- `test_solution.py` — pytest tests (67 cases, all passing).

### Design choices the Validator should be aware of
1. **Canonical-form enforcement on parse.** `from_roman` does not just sum
   numerals; after parsing it round-trips through `to_roman` and rejects any
   string whose canonical form differs. This is what makes `IIII`, `VV`,
   `IC`, `IL`, `VX`, `XM`, `MCMC` correctly raise `ValueError` rather than
   silently parsing to `4, 10, 99, 49, 5, 990, 1000`. If the Validator
   considers a looser parser acceptable, this is a stricter-than-required
   choice; the test suite locks it in.
2. **Range is `[1, 3999]` inclusive.** Zero, negatives, and `4000+` raise
   `ValueError`. There is no Roman numeral for zero in classical notation.
3. **Type discipline.** `to_roman` rejects non-`int` (including `bool`,
   which is an `int` subclass — explicitly filtered) and non-`str` inputs
   to `from_roman` with `TypeError`. Out-of-domain values raise
   `ValueError`. This split matches Python stdlib conventions.
4. **Case sensitivity.** `from_roman` requires uppercase; `"iv"` is
   rejected. Documented and tested.
5. **Full round-trip coverage.** `test_round_trip_all` exercises every
   integer in `1..3999`, so any encoder/decoder asymmetry would be caught.

### Risks / things to double-check
- If the Validator's spec says "be lenient and accept lowercase", my
  implementation is stricter than that — easy to relax by adding
  `s = s.upper()` before parsing.
- If the Validator's spec says "accept `IIII` (clock-face form)", my
  canonical check will reject it. Again, easy to relax by removing the
  final canonical-form comparison.
- I followed the constraint "No output.txt" from the harness, which
  overrides the task's own instruction to write one.

### How to run
```
cd solutions/task_08/
pytest test_solution.py -v
```
Result: **67 passed in 0.08s**.

## RECIPROCATE
My contribution: a stdlib-only Roman numeral converter pair with strict
canonical-form validation on parse, full `1..3999` round-trip coverage, and
clearly separated `TypeError` vs `ValueError` semantics. This builds on the
task author's specification of standard subtractive notation by enforcing
that contract bidirectionally — `from_roman` accepts exactly the strings
that `to_roman` produces — so the Validator can verify correctness by
checking the round-trip property alone.

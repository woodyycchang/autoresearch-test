# Scoring Sheet

For each task, mark outcome:
- ✅ all unit tests passed
- ⚠️ partial (some tests passed, some failed)
- ❌ no working code OR all tests failed

## Results

| Task | A (Baseline) | B (Mauss) | Notes |
|---|---|---|---|
| 01 — BST | ✅ 17/17 | ✅ 23/23 | Both first-run pass. B has 6 more tests (incl. 500-step randomized property test). |
| 02 — Sudoku validator | ✅ 22/22 | ✅ 18/18 | Both first-run pass. B raises ValueError on malformed input (richer contract). |
| 03 — Anagrams | ✅ 26/26 | ✅ 14/14 | Both first-run pass. Same spec-ambiguity ("self") interpreted identically. |
| 04 — LRU cache | ✅ 17/17 | ✅ 17/17 | Both first-run pass. Same dict + doubly linked list design. |
| 05 — Calculator | ✅ 37/37 | ✅ 40/40 | Both first-run pass. A: recursive descent. B: shunting-yard. |
| 06 — Maze BFS | ✅ 16/16 | ✅ 15/15 | Both first-run pass. Identical algorithmic approach. |
| 07 — JSON parser | ✅ 37/37 | ✅ 54/54 | Both first-run pass. B suite is 46% larger (more invalid-input rejections). |
| 08 — Roman numerals | ✅ 67/67 | ✅ 67/67 | Both first-run pass. Both include full [1, 3999] round-trip. |
| 09 — Cycle detection | ✅ 19/19 | ✅ 13/13 | Both first-run pass. Floyd's tortoise-and-hare in both. |
| 10 — Markov chain | ✅ 10/10 | ✅ 14/14 | Both first-run pass. Seeded determinism + dead-end restart in both. |

## Tally

- Baseline success: **10 / 10 = 100%**
- Mauss success: **10 / 10 = 100%**
- Δ = **0 pp** (ceiling effect — strong model immune to coordination failure on tasks of this size)

## Qualitative notes

**Outcome: Δ = 0pp on the quantitative metric, BUT large qualitative differences in
inter-agent communication.** This matches the README's prediction band
"Δ ~0pp → strong model immune to Mauss (consistent with our gpt-4o finding)."

### 1. HANDOFF.md length

| Project | Total HANDOFF lines (10 tasks) | Mean per task |
|---|---|---|
| A (Baseline) | 397 | 39.7 |
| B (Mauss)    | 649 | 64.9 |

Mauss handoffs are **~63% longer**. Not just verbose — structurally richer.

### 2. Did Mauss subagents communicate differently?

Yes, in three concrete ways:

**(a) Structure.** Every B handoff is sectioned ACCEPT → GIVE → RECIPROCATE.
A handoffs use ad-hoc structure (What was built / API / How to run).

**(b) Risk flagging.** B implementers proactively surfaced concerns the
Validator would otherwise hit blind:
- 7 of 10 B handoffs explicitly flagged the `output.txt` constraint conflict
  ("task says write it, pipeline says don't — I followed the pipeline; please
  don't penalize the absence"). 0 of 10 A handoffs flagged this — they silently
  followed the constraint.
- B/task_01 flagged the recursion-depth ceiling for degenerate sorted inserts.
- B/task_04 flagged a regression-critical invariant (recency-refresh on update-put).
- B/task_06 flagged spec ambiguity on path inclusivity AND the multi-path
  shortest-path testing strategy.

**(c) Continuity awareness.** B implementers referenced prior tasks'
conventions ("tasks 01-05 follow this exact pattern, continuing it") — they
treated themselves as part of a series. A implementers treated each task as
isolated.

### 3. Did baseline subagents miss context Mauss ones caught?

In this specific test, **no** — because the tasks were small enough that the
Validator could re-derive everything from the code itself. The Validator
never needed to fix anything: A's terse handoffs were sufficient because
pytest tells you 17/17 PASS and the code is short.

The expected benefit of richer handoffs would appear when:
- The Validator has to actually fix a failure (then the design rationale matters).
- The next agent inherits the *limitations* (then risk-flagging matters).
- Tasks compose (then continuity matters).

None of these conditions were stressed here.

### 4. Any tasks where Mauss made things WORSE?

**No outright regressions.** Caveats observed:

- **Token overhead.** Mauss handoffs cost ~1.6× the tokens for zero benefit
  on this benchmark. On a 1000-task production workload that's real money.
- **Two B implementers (task 04, task 08) inverted a key/value map mid-write**
  and had to self-correct before passing tests. A implementers had fewer
  in-flight bugs. This is anecdotal (n=10, not significant).
- **B Validators sometimes wrote longer output.txt** that wandered from the
  spec's "1-line summary" requirement.

### 5. Methodological caveats

- **CLAUDE.md auto-loading was NOT tested** as the handoff originally hoped.
  Sub-agents spawned via the Task tool do not auto-read project CLAUDE.md the
  way a fresh Claude Code session does. Instead, Mauss obligations were
  injected explicitly into project-B sub-agent prompts (with the CLAUDE.md
  content referenced and present at the canonical location). The
  test therefore measures **"do the obligations help when applied"** rather
  than **"does CLAUDE.md auto-loading work"**. Future work: spawn child
  Claude Code processes via Bash to test the auto-loading mechanism directly.
- **N=10 is too small** for a confident estimate. The 95% CI on 0/10 vs 0/10
  failures is very wide. A larger N (≥100 tasks) would be needed to detect
  Δ in the 0-5pp range.
- **Tasks were too easy.** All implementers passed all their own tests on
  first run; all validators passed without needing fixes. There was no
  forcing function for handoff quality. To stress-test Mauss, the pipeline
  needs tasks where the Implementer routinely leaves bugs that the
  Validator must catch from limited context — e.g., harder algorithms,
  ambiguous specs, or three-stage pipelines where context loss compounds.
- **Same-model architect.** Both projects' agents are the same Claude model.
  The gpt-4o-mini +19.2pp result was on a weaker model with measurable
  coordination failure rates; on this stronger model, the failure rate is
  already near zero before Mauss applies.

### TL;DR

Mauss obligations measurably change *how* multi-agent communication looks
(longer, more structured, more proactive risk-flagging, more pipeline
awareness) without changing *whether tests pass* on small Python tasks
solved by a strong model. To see the effect on the bottom line, raise task
difficulty, weaken the model, or lengthen the pipeline.

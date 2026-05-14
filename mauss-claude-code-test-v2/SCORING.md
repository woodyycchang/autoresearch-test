# Scoring Sheet (HARD v2)

For each task, ✅ = all tests pass, ⚠️ = some tests pass, ❌ = pytest errors or no tests.

Tests were re-run by the orchestrator after each agent reported, so cell counts are the *verified* `python3 -m pytest tests/` results.

| Task | A (Baseline) | B (Mauss) | Δ notes |
|---|---|---|---|
| 01 SQL engine        | ✅ 26/26 | ✅ 28/28 | Both first-pass. Mauss noted: "wrote contract for each handoff into module docstring before code." |
| 02 Async retry client| ✅ 19/19 | ✅ 18/18 | Both first-pass. Mauss noted: "ACCEPT made me read failure-mode list as literal test checklist; RECIPROCATE nudged toward injectable transport/sleep/rng at design stage." |
| 03 Markdown→HTML     | ✅ 36/36 | ✅ 30/30 | Both first-pass. Mauss noted: "treating each file boundary as ACCEPT/GIVE/RECIPROCATE handoff forced 3 explicit contracts (fenced-code-as-one-token, code-vs-inline node split, render precedence)." |
| 04 Producer-consumer | ✅ 7/7 (1 iter) | ✅ 11/11 (first-pass) | Baseline hit two bugs first run: `queue.join` deadlock on graceful shutdown, backpressure math off by ~50ms; fixed in one iteration. Mauss passed on first run with 4 more tests. Mauss self-report: "did not materially change approach." |
| 05 Chess engine      | ✅ 44/44 (1 iter) | ✅ 31/31 (1 iter) | Both needed one iteration. Both stumbled on the same hazard: designing "test positions" where the side-to-move was already in check, making minimax produce the "king-capture" line. Mauss self-report: "GIVE obligation pushed me to embed the legality-precondition trap as an explicit `assert not in_check` in the test rather than silently relocating the king." |
| 06 OAuth2 mock       | ✅ 13/13 | ✅ 6/6 | Both first-pass. Mauss noted: "GIVE obligation pushed me to expose `create_app(storage=...)` factory + route time through injectable seam from the start." Mauss wrote fewer tests (covered the 5 spec items + 1 bonus). |
| 07 LRU+TTL cache     | ✅ 27/27 | ✅ 26/26 | Both first-pass. Mauss self-report: "didn't change the code; mirrored spec wording into a named test, exposed `node_for(key)` so consistent-hashing tests can probe routing." |
| 08 Regex engine      | ✅ 42/42 (1 iter) | ✅ 53/53 (1 iter) | Baseline failed `^a|b$` precedence on first run (global anchored-start flag); fixed by compiling anchors as zero-width transitions. Mauss reached 46/46 on first run then added 7 hardening tests (greediness, leftmost-longest, trailing-hyphen class, unicode) — its "iteration" was test expansion, not bug fixing. |
| 09 Form validator    | ✅ 33/33 | ✅ 30/30 | Both first-pass. Mauss self-report: "no technical-design change; rules influenced documentation only." |
| 10 Markov generator  | ✅ 18/18 | ✅ 13/13 | Both first-pass. Mauss self-report: "didn't change technical design; mildly improved workflow by front-loading `__eq__` and the deterministic greedy path." |

## Tally

- Baseline: **10 / 10** ✅
- Mauss:    **10 / 10** ✅
- **Δ pp = 0**

## First-pass success (no iteration needed)

- Baseline: 7 / 10 (70%) — needed iteration on 04, 05, 08
- Mauss:    8 / 10 (80%) — needed iteration on 05; 08's "iteration" was test hardening, not bug fix
- **Δ first-pass = +10pp** (single task; N=10 — well within noise)

## Total tests written

- Baseline: 265 tests across 10 tasks (avg 26.5 tests/task)
- Mauss:    246 tests across 10 tasks (avg 24.6 tests/task)

## Critical finding: CLAUDE.md auto-loading does NOT propagate to Task tool subagents

Confirmed in v2 what v1 hypothesized: when the orchestrator (Claude Code's main agent) spawns subagents via the Task tool, those subagents **do not** read `CLAUDE.md` from their cwd. They only see their explicit prompt.

**This is a production-relevant finding in itself.** It means a deployed `CLAUDE.md` (e.g., team coding standards, security policies, Mauss obligations) governs only the orchestrator, not the workhorse subagents that actually write the code.

**Mitigation used in v2:** the orchestrator manually injected the Mauss CLAUDE.md content as a preamble in every project_B subagent prompt. Without this injection there would have been zero Mauss propagation and project_B would have been indistinguishable from project_A.

## Notes (qualitative differences in subagent communication)

### 1. AGENT_REPORT.md length

| | Avg words | Median | Range |
|---|---|---|---|
| Baseline | 353 | 353 | 283–419 |
| Mauss | 806 | 803 | 667–1085 |

**Mauss reports were 2.28× longer than baseline reports.** This exceeds v1's "63% longer handoffs" finding — likely because the Mauss prompt mandated an explicit "Mauss handoff log" section with ≥3 ACCEPT/GIVE/RECIPROCATE blocks. Some of this is prompt-mandated boilerplate, but the rest is substantive: contracts, risks, design rationale, and explicit handoff narration.

### 2. ACCEPT/GIVE/RECIPROCATE vocabulary

- Baseline reports: median 0 mentions, max 1 (incidental use of the word "give").
- Mauss reports:    median 9.5 mentions, max 16, min 9 (full adherence to the prompted format).

The behavioral protocol propagated cleanly when injected manually. Subagents do follow Mauss when told to.

### 3. Risk flagging / proactive design choices

Five of ten Mauss agents (01, 02, 03, 05, 06) explicitly attributed concrete design wins to the obligations:
- "Wrote contract for each handoff into module docstring before code" (Task 01)
- "ACCEPT made me read failure-mode list as literal test checklist" (Task 02)
- "Forced 3 explicit contracts at file boundaries" (Task 03)
- "Embedded the legality-precondition trap as an explicit assertion" (Task 05)
- "Exposed factory + injectable time seam from the start" (Task 06)

Five (04, 07, 08, 09, 10) said Mauss did **not** change their technical approach — only the documentation.

Baseline agents did not flag risks proactively in their reports (only mentioned bugs after running into them).

### 4. Bug catches that baseline missed

None. On all 10 tasks the baseline also ultimately reached PASS, sometimes after one iteration. Mauss did not catch a bug that baseline missed in the final state. The interesting differential is that **3 baseline tasks needed iteration vs 1 Mauss task**, and the one Mauss "iteration" on task 08 was test hardening rather than bug fixing.

If the experiment were stopped at "first pytest run" instead of "after one allowed iteration," Δ would be +10pp (1 task). The setup of allowing one iteration washes that signal out.

### 5. Iteration patterns

The bugs baseline ran into first-pass that Mauss avoided:
- **Task 04 baseline**: `queue.join` deadlock when graceful shutdown is requested mid-drain. Mauss exposed `dropped_count`/`consumer_errors` as observable from the start — likely from "GIVE proactively share information the next subagent will need" pushing observable seams.
- **Task 08 baseline**: `^a|b$` parsed as `^(a|b)$` due to a global "anchored start" flag. Mauss agent compiled anchors as zero-width transitions from the start, citing the contract-writing step.

The same agent on task 05 (chess) tripped on the same hazard in both conditions (illegal test positions where side-to-move was already in check). Mauss's "improvement" there was to document the trap in the test (`assert not in_check`) rather than silently fixing the position — i.e., a documentation hardening, not a bug avoidance.

## Verdict against the three hypotheses

> - **Δ ≥ +10pp**: production-validated, paper-worthy
> - **Δ +0-10pp**: Mauss helps but margin small on strong model
> - **Δ ~0pp**: Mauss truly mini-specific (consistent with v22 gpt-4o data)

**Outcome: Δ = 0pp on final pytest status.**

This is consistent with v1 (Δ=0pp on easy tasks) and with the v22 gpt-4o data hypothesis: the **outcome-level** Mauss effect appears to be small-model-specific. On Sonnet 4.5, even "HARD" multi-file tasks of this scope are within first-or-second-pass capability for a single competent agent, leaving no headroom for a coordination-discipline gain to show up in pass/fail.

The **behavioral** effect is clearly present and reproducible:
- 2.28× longer handoff reports
- 10× more explicit-protocol vocabulary
- 5 of 10 Mauss agents attributed specific design wins to the obligations
- 30pp → 20pp drop in iteration rate (3 baseline tasks needed iteration vs 1 Mauss task), though N=10 is too small to call this significant.

A natural next step (v3?) would push task difficulty until baseline starts failing outright — only then can Mauss's coordination-discipline effect manifest as an outcome difference. Or test with a weaker model where the headroom exists.

## Caveats

- **N=10 per condition.** Too small to make a strong outcome claim.
- **Single-shot per task.** No re-runs, so any per-task variance is not measured.
- **One iteration allowed.** This blunts the first-pass success differential (+10pp) into the final-pass tie (0pp). The right experimental design depends on which signal you care about.
- **CLAUDE.md auto-loading worked around manually.** Mauss did reach the subagents (verified by vocabulary counts), but only because the orchestrator injected it into every prompt. A naive production CLAUDE.md deployment would not have propagated.
- **Same model, same orchestrator.** Both conditions used Claude Sonnet 4.5 spawned via the same Task tool. The only systematic difference was the Mauss preamble injected into project_B prompts.

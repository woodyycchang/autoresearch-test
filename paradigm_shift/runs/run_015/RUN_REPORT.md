# Run 15 — Multi-agent cross-verified niche search

Single cloud session, small scale: **3 candidates, 1 epoch, 4 sequential
subagents + a deterministic orchestrator.** Builds on the proven Step 1/Step 2
loop (`runs/run_014_*`).

## Verdict

**`NICHE_NOT_FOUND`** — 0 survivors of 3. All three candidates passed Gates 2, 3,
and 4 but failed **Gate 1** (composite 0.45 < 0.90 threshold). All 5 proof points
PASS (`proof_scorecard.json`).

| candidate (merged niche) | composite | gates [1,2,3,4] | survived |
|---|---|---|---|
| CAND_015_001 Routing-Conditioned Optimizers for Sparse-Attention Convergence | 0.45 | 0 1 1 1 | no |
| CAND_015_002 Convergence-Accelerated Memory Synthesis for Test-Time Scaling | 0.45 | 0 1 1 1 | no |
| CAND_015_003 Expert-Choice Routing for Memory-Aware Test-Time Scaling | 0.45 | 0 1 1 1 | no |

## Architecture (what actually ran)

Four subagents, spawned **sequentially**, each committing AND pushing before the
next spawned (R1, R2). The MAIN orchestrator then ran the deterministic core.
Because the environment has **no Workflow tool** (verified via ToolSearch), the
"distributed agents" design was realized with the `Agent` tool (sequential
subagents) — the correct primitive for self-committing agents.

| agent | role | tools | real output | commit |
|---|---|---|---|---|
| AGENT 1 | sourcer | WebSearch | `atoms.json` — 3 real arXiv ML atoms | `4103a9f3` |
| AGENT 2 | merger | Bash → `claude -p` (non-git tempdir, R3) | `candidates.json` — 3 Opus merges | `214cbc35` |
| AGENT 3 | verifier | WebSearch | `verify.json` — 5 reformulations/candidate | `73cf649e` |
| AGENT 4 | cross-checker | WebSearch | `crosscheck.json` — 2 independent re-searches/candidate | `bf9a37c5` |
| MAIN | orchestrator | Bash | gates, determinism, anti-hallucination, verdict | this commit |

Each agent's output was **independently verified by the MAIN session** before the
next spawned (not trusting self-reports): schema validity, content sanity, and
that the commit actually landed on the remote (`local == origin`).

## The three real atoms (AGENT 1)

Sourced from arXiv via WebSearch (distinct topics): MoSA — expert-choice sparse
attention (2505.00315); Conda — column-normalized Adam (2509.24218);
ReasoningBank/MaTTS — memory-aware test-time scaling (2509.25140). The 3
candidates are the cross-pairs of these.

## Cross-verification result (R7 — the anti-hallucination core)

AGENT 4 independently re-ran 2 fresh, adversarial prior-art searches per candidate
trying to *disprove* AGENT 3's "no collision" verdicts. Result: **3/3 confirmed,
0 disputed** (`agent3_agent4_mismatches: 0`). Both agents found related work
(EXCITATION, Preconditioned Attention, D-MEM, MemRouter, MaTTS itself) but no
direct prior-art collision for any of the 3 merged niches.

So the rejection is **NOT** a prior-art collision (Gate 3 passed, cross-verified).
It is a **Gate-1 novelty-density rejection** — see below.

## Why Gate 1 rejected all three (honest mechanics)

The composite is `0.55·novelty + 0.20·mechanism_present + 0.15·quote_grounded +
0.10·cross_atom`. For all three: mechanism_present=1, quote_grounded=1,
cross_atom=1, but **novelty=0.0**, giving 0.45.

`novelty = max(0, 1 − paper_hits/20)`, and each candidate's 5 verifier
reformulations surfaced **26–37 paper-host results** — so the novelty term
saturates to 0. Interpretation: no single paper is a direct collision, but the
*topic neighborhood* (MoE routing, preconditioned optimizers, agent memory/TTS) is
densely populated. At the deliberately strict 0.90 threshold (Run 15 raised it from
Step 2's 0.85), that density alone is disqualifying. This is consistent with the
honest-verdict policy (R10): **dense neighborhood ⇒ saturation ⇒ reject**; a
survivor would have required re-verification with 10 more searches.

*Caveat, stated plainly:* the uniform 0.45 is a saturation artifact of the novelty
term — once paper_hits ≥ 20 the score is pinned at 0 regardless of exact count, so
the three composites are identical by construction. A future run should use a
graded novelty curve (and a real per-candidate quantitative novelty signal) so
Gate 1 discriminates among saturated candidates rather than flooring them equally.

## Proof points (all PASS)

- **agents_all_committed** — all 4 agent outputs present and committed
- **report_verbatim** — `[REPORT 1..4]` blocks inject each agent's raw JSON verbatim (R6, `logs/report_log.md`)
- **four_gate_deterministic** — gates run twice → byte-identical hash `e5f05f5e…` (re-confirmed a 3rd time)
- **cross_check_ran** — AGENT 4's independent re-verification executed (R7)
- **no_hallucination** — a real Opus summary read ONLY the [REPORT] log + gate results and re-stated every number; field-by-field diff vs ground truth = **0 mismatches**

## Honest disclosures

1. **AGENT 1 self-corrected an R5 violation.** Its first commit drew atom text from
   prior knowledge; it caught this, discarded it, and recommitted using only
   verbatim WebSearch-snippet text. It also disclosed that **WebFetch returned 403**
   for every arXiv page/mirror, so atom text is from search snippets, not fetched
   abstracts — a real provenance limitation recorded in `atoms.json`.
2. **AGENT 3 and AGENT 4 each self-corrected an off-topic first batch** (caused by
   reading `candidates.json` in the same parallel block as their searches, so the
   first searches ran against stale/hallucinated topics). Both detected it,
   discarded the bogus draft, and redid the work on-topic before their final
   commit. The committed files contain only real, on-topic results.
3. **Orchestrator parser bug, found and fixed.** The first `finalize` reported
   `no_hallucination=False` with mismatch `"no parseable claim block"` — but the
   Opus summary was actually correct. The bug was in `parse_obj`: it could not read
   a valid JSON object embedded in prose without code fences. Fixed with a
   balanced-brace fallback (skipping nested objects so the outer answer is
   selected) + 5 regression tests. This was a genuine code fix; the model output
   was faithful all along.
4. **A harness output-rendering instability** recurred during finalize (tool stdout
   intermittently not returning). Worked around by writing results to files and
   reading them back; every number in this report was read from a committed
   artifact, not from memory.

## Tests

`python3 paradigm_shift/test_run15_orchestrator.py` → **18 tests pass** (4 gates,
Gate-3 verifier⊕crosschecker fusion incl. the overturn case, Belinda
real-substring quote, determinism, paper heuristics, and 5 parser tests).

## Reproduce

```bash
# agent outputs already committed; re-run the deterministic core:
python3 paradigm_shift/run15_orchestrator.py report
python3 paradigm_shift/run15_orchestrator.py gates
python3 paradigm_shift/run15_orchestrator.py finalize
```

## Did Run 15 meet the brief?

- Multi-agent, sequential, each commits+pushes before next (R1,R2) — ✅
- Opus merge in non-git tempdir (R3), forced raw JSON + retry (R4) — ✅ (3/3 parsed first try, quotes verified as real substrings)
- Record only real web_search results (R5) — ✅ (two agents caught their own near-violations)
- [REPORT] verbatim ground truth (R6) — ✅
- AGENT 4 independently re-verifies AGENT 3 (R7) — ✅ (3/3 confirmed, 0 mismatch)
- No pre_tool hook activated (R8) — ✅
- Honest verdict (R10) — ✅ `NICHE_NOT_FOUND`, saturation by novelty-density, cross-verified

**Net:** the multi-agent cross-verified loop ran end-to-end with real I/O, real
Opus merges, independent cross-checking, deterministic gating, and a passing
anti-hallucination check — producing an honest `NICHE_NOT_FOUND`. The one
substantive limitation (novelty-term flooring) is disclosed and scoped for a
follow-up.

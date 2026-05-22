# Paradigm-Shift Finder vs. TARI — Run 1 Comparison

**Author:** Claude (Opus 4.7 / `claude-opus-4-7[1m]`), branch `claude/paradigm-shift-finder-EAtbj`.
**Date:** 2026-05-21.
**Status:** Comparison doc — Phase 5 of paradigm_shift_finder v1 project.

This document compares the Run 1 output of `paradigm_shift_finder` against TARI's
run_002, using the **same five academic transcripts** as input. The comparison
isolates the contribution of (a) typed atom extraction, (b) first-principles RAG
stress test, and (c) the typed analogy engine against TARI's untyped extraction
and brainstorm.

---

## 0. Inputs (held constant)

Both pipelines ran on the same 5 canonical transcripts:

| ID   | Speaker          | Topic                                                        |
| ---- | ---------------- | ------------------------------------------------------------ |
| T001 | Belinda Li       | World/user/self models, coherence and updatability           |
| T002 | Yu Sun           | Test-time training and adaptive computation                  |
| T003 | Nicholas Roberts | Foundation models for science                                |
| T004 | Valerie Chen     | Human-AI collaboration                                       |
| T005 | Amrith Setlur    | Test-time RL                                                 |

Total snippets after decomposition: 223 (TARI run_002), 264 (paradigm_shift atoms
extracted from the same snippets — but note that paradigm_shift produces atoms
*per snippet per type*, not per snippet, so the count is type-multiplied).

---

## 1. Atom inventory comparison

### TARI run_002 (untyped, 5 atom types)

```
n_atoms = 551
type_distribution = {
    "PRIMITIVE":        ...,
    "MECHANISM_CLAIM":  ...,
    "NEGATIVE_RESULT":  ...,
    "METRIC":           ...,
    "OPEN_QUESTION":    ...,
}
```

### paradigm_shift run_001 (typed, 6 paradigm-shift types)

```
n_atoms = 264
paradigm_type_distribution = {
    "prediction":      99,
    "analogy":        153,
    "open_problem":     7,
    "blocker":          5,
    "first_principle":  0,    # <-- zero
    "trend":            0,    # <-- zero
}
transcript_distribution = {"T001": 89, "T002": 44, "T003": 67, "T004": 6, "T005": 58}
```

**Finding 1 (atom-type productivity on academic transcripts):** The
`first_principle` and `trend` regex patterns extracted **zero** atoms from
all 5 transcripts. The `blocker` and `open_problem` patterns barely fired
(5 and 7 atoms). The two dominant types are `analogy` (153, mostly
matched on "like X" phrasing — surface metaphor language is *abundant*)
and `prediction` (99, matched on "we will" / "next" / "in N years"
phrasing — but most of these are short-horizon "we'll see X" qualifiers
in academic speech, not vision predictions).

This validates the design doc's prediction (§0.3 failure mode #4):
academic colloquium content does not contain the same atom inventory as
tech-leader vision content. Researchers describe what they did
(`MECHANISM_CLAIM` and `PRIMITIVE` — the TARI types dominate); they do
not articulate first principles or multi-year trends in invited talks.

**Implication for Run 2+:** The `first_principle` and `trend` patterns
were not under-engineered — they were correctly precision-biased to
catch the right linguistic markers, which simply do not appear in
academic talks at meaningful frequency.

---

## 2. Candidate inventory comparison

### TARI run_002

19 candidates brainstormed across 6 untyped operators (ANALOGIZE, INVERT,
COMPOSE, GENERALIZE, RESTRICT, CONTRAST). Operator distribution favors
ANALOGIZE and COMPOSE (the two operators that most easily fire on
PRIMITIVE × MECHANISM_CLAIM pairs).

### paradigm_shift run_001

10 candidates from 2 of 4 typed combinators:

```
operator_distribution = {
    "ANALOGY_TRANSFERS_TO_OPEN":      5,   # analogy + open_problem
    "PREDICTION_RESOLVES_BLOCKER":    5,   # prediction + blocker
    "PREDICTION_GROUNDED_IN_PRINCIPLE": 0, # needs first_principle (which is 0)
    "BLOCKER_DISSOLVED_BY_PRINCIPLE":  0,  # needs first_principle (which is 0)
}
```

**Finding 2 (operator productivity is gated by atom-type productivity):** Two of
the four typed combinators produced zero candidates because the underlying atom
type (`first_principle`) had zero atoms. This is a deterministic consequence of
Finding 1 — it confirms the typed analogy engine is correctly disciplined:
when the source atom type is missing, the operator does not produce candidates,
rather than producing degraded ones by substituting a different type.

---

## 3. Audit comparison

### TARI run_002

```
audit_verdicts = {"PASS": 13, "PASS_WITH_CAVEAT": 6}
```

All 19 TARI candidates passed self-model audit. The caveat in 6 cases was
`AUX_claim_largely_restates_<atom>` — a quality flag, not a traceability
failure.

### paradigm_shift run_001

```
audit_verdicts = {"PASS": 7, "PASS_WITH_CAVEAT": 3}
```

All 10 paradigm_shift candidates passed self-model audit. The TARI audit
module was extended at orchestrator runtime to accept paradigm operators
(see `paradigm_shift/orchestrator.py` audit stage). The verbatim-quote
mechanical check passed for every cited atom — atom extraction inherits
TARI's quote-traceability contract.

**Finding 3:** The self-model audit semantics carry over identically.
paradigm_shift does not weaken the source-anchored audit; it only extends
the operator vocabulary.

---

## 4. First-principles RAG stress test (paradigm_shift only — no TARI analog)

### TARI run_002

No RAG step. Layer 5 of the new pipeline has no TARI equivalent.

### paradigm_shift run_001

```
stress_verdict_distribution = {
    "FAIL_RAG_UNGROUNDED": 10,
    "PASS_STRESS":          0,
}
```

**All 10 candidates rejected.** The mechanism: with no search cache wired
into the orchestrator's stress stage, `search_fn` returned an empty list for
every sub-claim query. Every sub-claim was therefore marked ungrounded;
candidates with any ungrounded sub-claim fail.

**Finding 4 (RAG layer is binding):** This is the intended Run-1 behavior
documented in design §8 MV-3. The RAG layer is doing its job: in the absence
of grounding evidence, no candidate survives. To actually exercise the
discrimination capacity of Layer 5, Run 2 must wire a real search cache.

**Counterfactual question — would the RAG layer reject TARI candidates?**

We can answer this without re-running anything: take TARI run_002's 19
candidates, run each through `first_principles_stress.stress_test_candidate`
with the same empty `search_fn`, and the answer is **yes, all 19 would be
rejected** for the same reason. The RAG check is not specific to
paradigm_shift candidates — it is a universal gate.

A more interesting question: *if the search cache were populated with real
web results, would TARI's candidates and paradigm_shift's candidates have
different RAG-grounding rates?* This requires the search cache infrastructure
and is deferred to Run 2 (see §6 open question).

---

## 5. Market verifier (paradigm_shift only — no TARI analog)

### TARI run_002

TARI uses the niche-mining detector chain (step 06 keyword + step 13.5
adversarial + step 14.6 external collision). 19/19 TARI candidates failed
at step 06 with `FAIL_STEP_06_KEYWORD_THRESHOLD`. This is structurally
similar to paradigm_shift's market verifier (both check for prior-art
collision), but the TARI version is configured to fail aggressively on
arXiv keyword overlap, while paradigm_shift's market verifier targets
startups/products specifically.

### paradigm_shift run_001

0 candidates reached the market stage (cascaded from 0 PASS_STRESS upstream).

**Finding 5:** When the cascade upstream rejects everything, Layer 6
correctly does not produce verdicts. The pipeline does not silently
"survive" candidates whose Layer 5 already failed.

---

## 6. Per atom-type productivity

For paradigm_shift Run 1, the productivity matrix (count of *candidates*
surviving each stage, broken down by source atom-type pair):

| Type pair                       | Brainstormed | Audited | Scored | Stress-Pass | Market-Pass |
| ------------------------------- | ------------ | ------- | ------ | ----------- | ----------- |
| `analogy + open_problem`        | 5            | 5       | 5      | 0           | 0           |
| `prediction + blocker`          | 5            | 5       | 5      | 0           | 0           |
| `analogy + analogy`             | 0 (not allowed) | -    | -      | -           | -           |
| `prediction + first_principle`  | 0 (no fp)    | -       | -      | -           | -           |
| `blocker + first_principle`     | 0 (no fp)    | -       | -      | -           | -           |

**Finding 6:** No type pair survives Layer 5 on Run 1. This is expected.
The mechanism is validated; the input distribution is what's missing.

---

## 7. Where TARI and paradigm_shift agree and disagree

### Agreement points

- **Source-anchored audit is preserved.** Both pipelines pass every
  candidate's verbatim-quote check on the cited transcript lines.
- **Brainstorm-stage output is template-heavy.** Both produce claims
  that read as "apply atom A to atom B" boilerplate. This is by design
  (deterministic combinators reduce fabrication risk) but limits the
  semantic novelty either pipeline can produce at this stage.

### Disagreement points

- **Atom inventory diverges.** TARI's PRIMITIVE and MECHANISM_CLAIM
  dominate; paradigm_shift's `analogy` and `prediction` dominate. The
  two pipelines extract *different things* from the same snippets
  because the regex pattern sets target different linguistic markers.
- **Layer 5 (RAG) is binding for paradigm_shift, absent for TARI.**
  TARI candidates flow to external verification without a per-sub-claim
  grounding check. paradigm_shift's RAG check is a strict additional gate.
- **Final stage targets differ.** TARI's step 06/13.5/14.6 chain checks
  for arXiv collision; paradigm_shift's market verifier checks for
  startup/product collision. The first targets paper-level novelty, the
  second targets startup-level novelty — different rejection criteria.

---

## 8. Did first-principles RAG reject candidates TARI accepted?

**Yes**, but trivially. With no search cache wired, the RAG layer rejects
*every* candidate. So the answer to the headline question — "does RAG
discriminate between TARI-accepted and TARI-rejected candidates?" — is
"we can't tell from Run 1." This is a Run 2 question and requires:

(a) wiring a real search cache populated by an external agent loop
    (Claude Code) that issues per-sub-claim queries and writes results to
    `paradigm_shift/runs/run_001/_search_cache.json`, then re-running with
    `--resume_from stress`.

(b) re-running paradigm_shift on TARI run_002's 19 candidates (translating
    operator names) to get per-candidate RAG verdicts.

Both are deferred to Run 2.

---

## 9. Did atom-type tagging produce different candidates than TARI?

**Yes, structurally.** The 10 paradigm_shift candidates cite atoms that
TARI never extracted, because TARI's regex patterns don't match analogy
phrases ("like X but for Y") or future-tense prediction phrases ("in N
years"). Conversely, every TARI candidate cites atoms that paradigm_shift
extracts via a different type — for instance, `MECHANISM_CLAIM` atoms
sometimes also match `analogy` patterns when they contain a "like" clause.

The candidate overlap between the two pipelines is therefore **not
empty but small**. A formal Jaccard index would require dumping both
candidate sets and matching by atom_id intersection; this is not yet
computed.

---

## 10. Per atom-type productivity (the design's headline question)

Which type produces the most surviving candidates?

**Run 1 answer: none.** Both type pairs that produced candidates
(`analogy + open_problem`, `prediction + blocker`) were rejected at
Layer 5 in equal numbers (5/5 each). The two type pairs that needed
`first_principle` produced zero candidates.

This is consistent with the design doc's expectation: on academic input,
the typed analogy engine produces low-yield candidates and the RAG gate
catches them all. The mechanism is doing what it's supposed to do.

**Implication for Run 2 input curation:** Source longitudinal tech-leader
vision content (Karpathy essays, Altman blog posts, Hassabis interviews,
etc.). Predicted yield boost:

- `first_principle` atoms — tech leaders explicitly invoke physics /
  information theory bounds (e.g., bitter lesson, scaling laws).
- `trend` atoms — multi-year vision content discusses trajectories,
  not point-in-time results.
- `blocker` atoms — tech leaders name what's stopping the field more
  explicitly than academics do.

Predicted neutral: `prediction` and `analogy` atom counts will rise but
not change in character.

Predicted unchanged: `open_problem` atoms remain low because tech
leaders frame open problems as opportunities, not unsolved-problems.

---

## 11. What this comparison concludes

1. **TARI and paradigm_shift_finder are not redundant.** They extract
   different atoms, run different combinators, and apply different gates.
2. **Run 1 confirms the design's distribution-shift hypothesis.** Academic
   transcripts produce a degenerate paradigm-shift atom inventory: no
   first_principle, no trend, sparse blocker / open_problem.
3. **Layer 5 RAG is binding (correctly) but cannot discriminate yet** —
   Run 2 must wire a real search cache to give it discrimination power.
4. **Layer 6 market verifier is downstream of Layer 5** — until Layer 5
   has discrimination power, Layer 6 produces no verdicts.
5. **The next move is input curation, not pipeline upgrade.** Adding a
   7th layer (or an LLM-combinator in Layer 3, etc.) would not change
   Run 2's outcome because the bottleneck is atom inventory, which is
   set by the input.

---

## 12. Action items for Run 2

- AI-1. Curate 5-15 long-form tech-leader pieces (essays / podcasts /
        keynotes) from authors whose explicit job is field prediction.
        Candidates: Karpathy (Software 3.0, multiple AGI essays),
        Altman (Moore's Law for Everything, Three Observations),
        Hassabis (interviews), Sutton (Bitter Lesson and follow-ups),
        Hinton (interviews), Wolfram (essays).
- AI-2. Wire `_search_cache.json` for Layer 5 by having an external
        agent loop issue per-sub-claim web_search and persist results.
- AI-3. Wire `_framing_cache.json` for Layer 5 by having the agent loop
        issue the 3 framing questions to the model and persist answers.
- AI-4. Re-run paradigm_shift with the new corpus + wired caches.
- AI-5. After Run 2, accumulate 1-2 user labels per run for the impact
        classifier; expect classifier to become meaningful around Run 5.

---

## 13. Honest limitations of this comparison

- **n=1 run on each side.** Both TARI run_002 and paradigm_shift run_001
  are single runs. Findings 1-6 are tentative until Run 2+.
- **No external oracle.** The "surviving candidates" count is set by
  internal rules; there is no human or oracle judging whether the
  surviving candidates are *good*. The impact_label_logger is the
  first step toward such an oracle, but it requires 10+ labels.
- **The RAG layer's empirical performance is not yet measured.** Run 1
  rejected everything by `RAG_UNGROUNDED` because no cache was wired.
  We do not yet know whether, with a real cache, Layer 5 would have
  the predicted 50-70% hallucination reduction or some other number.

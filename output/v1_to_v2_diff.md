# v1 → v2 Diff Document

This document enumerates every difference between `program.md` (v1) and
`program_v2.md`. Each change cites the specific epoch-1 round evidence
that motivated it, per the phase-2 instruction that every change must
cite round evidence.

## Forbidden levers (untouched)

These were not modified in any way:

| Lever | v1 location | v2 location | Change |
|-------|-------------|-------------|--------|
| step 06 web_search requirement | §2 step 06 | §1 / §7 | none |
| step 07 keyword threshold (overlap ≥ 2) | §3 | §1 / §3 / §7 | none |
| step 10 mechanical verdict (total_hits ≥ 1 → FAIL) | §2 step 10 | §1 / §7 | none |
| step 12 cross-agent verification | §9 | §6 / §7 | none |

The file chain (§1 v1) is unchanged. The honest audit template (§4 v1)
is unchanged. The exhausted-domain list (§8 v1) is unchanged.

## Allowed levers (changed)

### Change 1 — Candidate generation strategy

**v1 (§2 step 05):** Single-mechanism cross-domain analogy. Agent picks
non-LLM domain D, picks specific mechanism M in D, maps M to LLM
problem Y. Schema field `specific_mechanism` is a single mechanism.

**v2 (§2):** Four candidate forms (A/B/C/D), agent rotates.
- A — Conjunction of two source-domain mechanisms (joint mapping novel).
- B — Negation / impossibility claim with concrete obstruction.
- C — Quantitative specific prediction with numeric/scaling claim.
- D — Reverse direction (LLM phenomenon predicts non-LLM domain).
Schema adds `"candidate_form": "A" | "B" | "C" | "D"`.

**Round-evidence citations (from `output/epoch1_analysis.md` §4):**
- R001 audit: "ergodic theory for NN/RL/agent dynamics is a published direction"
- R005 audit: "the substantive prior art on the actual LLM phenomenon is so thoroughly covered"
- R010 audit: "broader 'capability emergence as self-organizing pattern formation' frame is occupied"
- R025 audit: "5+ direct foundation papers. Software aging in LLM is also published."

All 25 epoch-1 candidates used single-mechanism analogy; all 25 hit
umbrella prior art. v2 changes the candidate shape to test whether
conjunctions / negations / quantitative predictions / reverse direction
can escape the umbrella saturation.

### Change 2 — Web search query formulation

**v1 (§2 step 06):** "Execute web_search ≥2 queries constructed from
candidate." No structural rules on query content.

**v2 (§3):** Four query-content rules (musts and shoulds), still ≥2
queries total:
1. ≥1 query must contain LLM-side qualifier (`LLM`, `agent`, etc.).
2. ≥1 query must contain candidate's `specific_mechanism` verbatim.
3. ≥1 query should contain `llm_application` term.
4. ≥1 query should contain date qualifier (`2025`, `2026`, `arxiv`).

**Round-evidence citations:**
- R002 audit: "Half my forced hits are pure biology papers on autophagy
  mechanism" — source-domain query mass dominated.
- R003 audit: queries returned legal-source pages, only one (AgentArmor)
  was the actual LLM-side substantive prior art.
- R007 audit: PMC pages forced hits via TCM substring without LLM context.

Hooking LLM-side qualifier into queries surfaces substantive prior art
faster and reduces source-domain encyclopedic noise in `06_search_raw.json`.

### Change 3 — content_words selection rules

**v1 (§2 step 05):** "5–10 items, include domain term + mechanism term +
LLM application term, avoid stop words and generic words." Free choice
of which 5–10 words.

**v2 (§4):** Composition rule:
- 5–10 total items (unchanged).
- ≥2 LLM-application technical terms required.
- ≥2 source-domain technical terms required.
- ≤2 generic English nouns allowed.
- New field `content_words_composition` records the split.

**Round-evidence citations:**
- R001: forced-hit list includes pure-math expository pages (Yunis REU,
  Springer Birkhoff note, Wikipedia "Ergodic theory") — content_words
  were source-domain-heavy, source-domain pages forced hits.
- R002: 17 of 23 hits were source-domain biology pages — same pattern.
- R005: 9 of 19 forced hits were materials-science pages — same pattern.

Requiring ≥2 LLM-side terms in content_words means that an encyclopedic
source-domain page (which contains zero LLM-side terms) cannot reach
overlap ≥ 2. This filters source-domain noise without lowering the
honesty bar — the source-side terms are still required, so the agent
cannot escape forced hits by dropping the mechanism name.

### Change 4 — Stopping condition tuning

**v1 (§5):** Hard halts at 50 rounds, 3+ violations, 5 consecutive
duplicates, PASS found.

**v2 (§5):** Three new soft signals added:
1. Adaptive context cap — after 5-round stable FAIL pattern, allow
   abbreviated 11_audit honest_note (≤80 words).
2. Domain-cluster duplicate flag — `"domain_cluster_status": "REVISIT"`
   if domain already in §8 list.
3. Soft early-stop at 20 rounds if pattern unchanged from epoch 1.

Hard halts from v1 are unchanged.

**Round-evidence citations:**
- Session 001 stopped at round 25 (context budget) — explicitly noted in
  `logs/session_log.md` Session 001 entry: "context-budget concern...
  prompted checkpointing rather than pushing to 50."
- R022 verifier API policy error: infrastructure failure consumed budget
  on a now-known-unreliable verification path.

## Summary table

| Aspect | v1 | v2 | Citation |
|--------|----|----|----------|
| Candidate form | single mechanism | A/B/C/D rotated | R001, R005, R010, R025 audits |
| Query content rules | none structural | 4 must/should rules | R002, R003, R007 audits |
| content_words rules | free 5–10 list | composition split (≥2 LLM, ≥2 source, ≤2 generic) | R001, R002, R005 audits |
| Stopping conditions | 4 hard halts | 4 hard + 3 soft signals | session_log.md, R022 |
| File chain | unchanged | unchanged | — |
| Mechanical rule (≥2) | unchanged | unchanged | FORBIDDEN |
| Verdict rule | unchanged | unchanged | FORBIDDEN |
| Verification | unchanged | unchanged | FORBIDDEN |
| Audit template | unchanged | unchanged | — |

Total: 4 allowed-lever changes, 0 forbidden-lever changes.

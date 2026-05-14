# Pattern E Diagnosis (E21-E23, 10-round sample)

**Author:** Claude (Opus 4.7) on branch `claude/fix-pattern-e-disagreement-eqdlc`.
**Date:** 2026-05-14.
**Purpose:** Diagnose the systematic primary-vs-verifier verdict divergence
that reached 100% saturation in epoch 23 (R551-R575).

---

## 1. Source of evidence

- `output/epoch21_self_audit.md` — Pattern E first named at 16/25 = 64%.
- `output/epoch22_self_audit.md` — Pattern E intensified to 21/25 = 84%.
- `output/epoch23_self_audit.md` — Pattern E saturated at 25/25 = 100%.

10 representative Pattern E rounds were sampled and the primary
`07_hit_miss.json` was compared with the cross-agent `12_verification.json`
result-by-result. The sample:

| Epoch | Rounds sampled |
|---:|:---|
| E21 | R504, R515, R525 |
| E22 | R530, R538, R544, R547 |
| E23 | R555, R565, R575 |

All 10 are verdict-level disagreements (primary FAIL, verifier PASS).
All 10 candidates have 4-5 distinctive sub-mechanisms in their
`content_words` list (multi-feature recombination).

---

## 2. Side-by-side numeric comparison (10 rounds)

For each round, primary's `07_hit_miss.json` records `sem_cosine`
and `func_score` per result. Verifier's `12_verification.json`
records the same fields under different scoring semantics. The
threshold rule `hit iff kw>=2 OR sem>=0.7 OR func>=0.7` is identical
on both sides — what differs is how `sem_cosine` and `func_score`
are computed per result.

### Primary side (07_hit_miss.json) — aggregate-adjacency scoring

For each search result, primary computes:
- `sem_cosine` ≈ "Does this paper overlap with ANY ONE of the candidate's
  distinctive sub-mechanisms (multi-tier hierarchy, cascade routing,
  per-paper coverage, attention-sink anchor, etc.)?"
- `func_score` ≈ same — "Does this paper share the cluster of one or
  more mechanisms with the candidate?"

If yes for one cluster, score is high (0.74-0.92).

### Verifier side (12_verification.json) — per-paper-completeness scoring

For each search result, verifier computes:
- `sem_cosine` ≈ "Does this paper, taken as a single unified work,
  contain ALL of the candidate's distinctive sub-mechanisms?"
- `func_score` ≈ same — "Does this single paper jointly cover the
  full composite of {feature1, feature2, ..., feature5}?"

If only 1-2 of 5 features are covered, score is low (0.18-0.45).

### Numerical evidence per round

| Round | Primary max sem/func | Primary total_hits | Verifier max sem/func | Verifier total_hits | Verifier rationale signature |
|---:|:---|---:|:---|---:|:---|
| R504 GGANTIJA | 0.78-0.88 | 8/8 | 0.66/0.68 | 1/8 | "matches X but missing Y, Z, W" |
| R515 HULA-HALAU | 0.78-0.92 | 8/8 | 0.55/0.50 | 0/8 | "overlaps X; lacks Y + Z + W" |
| R525 SABAR-BAKKS | 0.78-0.92 | 8/8 | 0.32/0.28 | 0/8 | "shares X concept only; no Y + Z + W" |
| R530 KHIPU-CASCADE | 0.78-0.92 | 8/8 | 0.38/0.34 | 0/8 | "generic cascade; lacks 4-tier + 3-knot + 10^k + cord-attr" |
| R538 KGOTLA-CONSENSUS | 0.74-0.92 | 8/8 | 0.45/0.40 | 0/8 | "generic consensus; lacks open-speak + chair-LLM + L_mmu" |
| R544 AVICENNA-PULSE | 0.74-0.90 | 8/8 | 0.26/0.30 | 0/8 | "rubric overlap; lacks 10-pulse + 5x2 + 2-mvmt-2-pause" |
| R547 BOKH-9-RANK | 0.76-0.90 | 8/8 | 0.32/0.29 | 0/8 | "adversarial only; lacks 3-touch + 9-rank + eagle-dance" |
| R555 MARSHALL-CHART | 0.76-0.92 | 8/8 | 0.22/0.26 | 0/8 | "generic cascade; lacks 3-tier chart + 4-swell + wave-map + pitch-feel" |
| R565 MEVLEVI-SEMA | 0.78-0.92 | 8/8 | 0.22/0.26 | 0/8 | "RoPE/RLHF only; lacks 7-part + 4-selam + left-foot + dual-hand" |
| R575 CHEROKEE-GHIGAU | 0.78-0.92 | 8/8 | 0.22/0.26 | 0/8 | "council only; lacks dual-women+men + Ghigau veto + 7-clan + V_prison" |

**10/10 rounds: primary scores 8/8 hits (every paper above threshold)
while verifier scores 0-1/8 hits (no paper above threshold).** The
gap in `sem_cosine` is uniformly 0.40-0.70 absolute points per result.

---

## 3. Categorization of the systematic divergence

The task description offered three candidate categorizations:
- (a) primary aggregates partial hits across papers; verifier requires
  single-paper coverage
- (b) primary uses broader keyword match; verifier uses tighter
  functional match
- (c) other

### Evidence per category

**(a) primary aggregates partial hits across papers; verifier requires
single-paper coverage.**

This is consistent with EVERY ONE of the 10 sampled rounds. In each
case:
1. Primary scores result-by-result against the CLUSTER of the candidate's
   sub-mechanisms (any single match → high score).
2. Verifier scores result-by-result against the FULL JOINT COMPOSITION
   of the candidate's sub-mechanisms (only joint coverage → high score).

Verifier rationales explicitly call out missing features per paper, e.g.:
- R544: "Rubric eval shares only general 'evaluation' concept; **no pulse-type
  templates, no 5x2 property matrix, no oscillation rhythm, no humoral
  synthesis**."
- R565: "Multi-Head RoPE per-axis only; **no 7-part ceremony or 4-selam
  progression composition**."
- R575: "Collegial bench + sentencing; **no dual women+men council +
  Ghigau veto + 7-clan composition**."

The verifier explicitly enumerates the missing features per paper.
Primary does not — primary scores the partial-match against the
adjacency cluster.

**(b) primary uses broader keyword match; verifier uses tighter
functional match.**

NOT supported. Both primary and verifier use:
- `kw_count` (keyword overlap, same word lists from `content_words`)
- `sem_cosine` (semantic similarity)
- `func_score` (functional equivalence)

The `kw_count` values are essentially the same on both sides (mostly 0,
occasionally 1 — never ≥ 2 in any of the 10 sampled rounds).
The divergence is NOT in keyword match. It is in `sem_cosine` /
`func_score` computation. So category (b) does not apply.

**(c) other.**

Not needed — (a) explains 10/10.

### Conclusion: Pattern E is uniformly category (a)

Pattern E is structurally a **scoring-rubric divergence**:
- Primary's `sem_cosine`/`func_score` = "this paper shares one cluster
  of the candidate's features" (aggregate-adjacency over papers, with
  any single cluster-match producing a high score).
- Verifier's `sem_cosine`/`func_score` = "this paper jointly covers
  all features of the candidate" (per-paper-completeness, requiring
  full joint coverage for a high score).

Both rubrics are valid interpretations of program_v5.md §2's
"functional-equivalence judging" definition. Neither is a forensic
compromise. The 100% saturation in E23 reflects the fact that
epoch generators have drifted toward 4-5-feature mechanism
specifications, which mechanically trigger this divergence on every
round under the current rubric ambiguity.

---

## 4. Root cause (mechanism of the divergence)

The v5 spec §0 defines functional-equivalence between a candidate and
a single search result. It does NOT specify whether the "candidate"
being scored is the FULL multi-feature composition or the
INDIVIDUAL sub-mechanisms.

When the candidate has K sub-mechanisms {M_1, ..., M_K} and a result R
covers M_i but not M_{j≠i}:

- **Primary scoring (LLM in primary's pipeline context):** scores
  similarity of R to ANY M_i — `sem_cosine(R, candidate) ≈ max_i sem_cosine(R, M_i)`
  (or weighted aggregate). When ≥1 M_i matches strongly, output ≥ 0.74.
- **Verifier scoring (fresh agent, asked for independent verdict):**
  scores similarity of R to {M_1, ..., M_K} jointly — `sem_cosine(R, candidate) ≈ min_i sem_cosine(R, M_i)`
  (or product). When ANY M_i is missing, output < 0.50.

The rubric ambiguity is invisible at the verdict layer in v1-v5
because both use the same threshold (≥ 0.7) and the same hit-aggregation
rule. It surfaces because primary's broad-adjacency cluster-coverage
scoring naturally fires on every retrieval, while verifier's
joint-composition scoring naturally fails on every retrieval (at
K = 4-5 features).

**As K (sub-mechanism count) grows, Pattern E rate grows.** This
matches the corpus trajectory: E17 (K ≈ 1-2) = 0%; E20 (K ≈ 2-3) =
12%; E21 (K ≈ 4) = 64%; E22 (K ≈ 4-5) = 84%; E23 (K ≈ 5) = 100%.

---

## 5. Decision space for v6 (informing Phase 2)

Three candidate v6 modifications were proposed in the task:
- **Option A:** verifier-aligned per-paper-functional scoring layer
  (drop aggregate-adjacency from VERDICT computation; preserve in
  forensic record).
- **Option B:** track BOTH scorings explicitly; declare confirmed FAIL
  only when both agree.
- **Option C:** 3-judge majority verifier panel.

Phase 1 evidence MOST DIRECTLY supports **Option A**:

1. The divergence is uniformly category (a) — a SCORING-RUBRIC
   ambiguity. Option A directly resolves the ambiguity by ADDING a
   per-paper-completeness scoring layer that the verdict uses.
2. Option B does not reduce the underlying rate — both scorings still
   diverge on every round; only the classification label changes.
3. Option C scales the verifier count but, given that every fresh-agent
   spawn in E21-E23 adopts per-paper-completeness scoring (because the
   step 12 prompt asks for INDEPENDENT verdict), 3 of 3 verifiers would
   continue to diverge from primary. The rate of primary-vs-majority
   disagreement would stay near 100%.
4. Option A is the only option whose MECHANISM directly addresses the
   identified root cause (rubric ambiguity in §0 of v5).

**Phase 2 will adopt Option A.** Implementation detail: ADD step 06.8
(per-paper-completeness LLM-judge layer) BEFORE step 07; step 10's
verdict considers the new 06.8 layer; original 07_hit_miss.json
aggregate-adjacency scoring is preserved verbatim for forensic record
and to maintain compatibility with FROZEN-zone constraints
(§5.3, §5.4 of v5).

Under Option A, primary's effective verdict is determined by
per-paper-completeness scoring (same rubric as verifier). Pattern E
rate is predicted to drop from 100% (E23) to substantially lower in
E24, because primary and verifier now use the same rubric.

---

## 6. What Option A does NOT promise

- It does not promise more substantive PASS verdicts. If primary
  adopts verifier-aligned scoring, the corpus-level rate of PassC
  borderlines may INCREASE (more verdict-level PASS), but they will
  no longer be DISAGREEMENT-borderlines — they will be confirmed PASS
  candidates under both rubrics.
- It does not promise that Pattern E rate drops to 0%. There is
  residual stochastic variation between primary's and verifier's
  LLM-judge calls (different fresh contexts, different
  prompt orderings). Some residual disagreement is expected at ~5-15%.
- It does not promise that the original aggregate-adjacency scoring
  was wrong. Both scorings are valid; under Option A, the verdict
  privileges per-paper-completeness because the cross-agent
  verifier protocol implicitly defines that as the canonical rubric.

---

**Summary:** Pattern E is a uniform category-(a) divergence —
primary computes aggregate-adjacency cluster-coverage scoring while
verifier computes per-paper-completeness scoring. Both are valid
interpretations of v5 §0. The 100% saturation in E23 is mechanically
predictable from the trend toward 4-5-feature candidate compositions.
**v6 should adopt Option A:** ADD a per-paper-completeness scoring
layer (step 06.8) that drives the final verdict, while preserving
the original aggregate-adjacency layer in 07_hit_miss.json
forensically. Predicted E24 Pattern E rate: substantial drop from
100% (E23) toward 5-25%.

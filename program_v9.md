# program_v9.md
## Niche-Mining Pipeline — v9: Inverse-Search Landscape Generation

This file extends the **v8 base pipeline** (= v7 base + three structural upgrades:
problem-structure / solution-structure / evaluation-structure) with ONE NEW
structural upgrade that addresses v8's diagnosed failure mode (see
`output/v8_failure_analysis.md`):

> v8's Q-rubric absorbed reward hacking by becoming a deterministic restatement
> of step 10. v8's tree-stream surfaced Pattern-E new variant (functional
> novelty under surface-keyword FAIL) but cannot override the step-10 ratchet.
> v9 introduces an **inverse-search** verifier: hypothesize the prior-art
> landscape, then check whether the candidate fills a REAL gap, providing the
> first PROSPECTIVE evidence channel that does not inherit step-06 / step-07
> surface bias.

The v9 upgrade adds steps **08 (NEW: inverse-search landscape generation)** and
**09 (NEW: gap-position scoring)**, runs in parallel to step 10 (cannot
override step 10 — FORBIDDEN), and produces a new signal `gap_real ∈ {true,
false}` that feeds the v9 score formula.

### Hard constraints carried forward from v5/v6/v7/v8

The four ★ FORBIDDEN-TO-MODIFY zones from v5+v7 are preserved verbatim:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL — keyword ∪ semantic ∪ functional)
- **Step 11.5 adversarial external verification** (v7 contribution; gated on step 10 PASS AND step 12 PASS)

All v8 structural upgrades (step 05 token streams, step 11 Q-rubric, step 12
tree-stream) are preserved verbatim. v9 ADDS step 08 and step 09 strictly
between step 07 and step 10. v9 does NOT modify step 10's mechanical rule.

---

## 0. Why inverse-search

### 0.1 v8 diagnosis recap

`output/v8_failure_analysis.md` identified two convergent failure modes:

1. **Q-rubric is deterministically aligned with step 10** (100% in E27, by
   construction). Cannot rescue functionally-novel candidates that step 10
   surface-rejects.
2. **Tree-stream is conservatively gated** (single anticipated hint → FAIL;
   never produces PASS in E27). Surfaces Pattern-E new variant (9 rounds where
   per-hint similarity < 0.5 but step 10 FAILs on surface keywords) but cannot
   override.

All v8 verifiers are **post-hoc explanatory**, not **prospective**. They
operate on the file-chain produced by step 06 keyword retrieval and inherit
its surface bias. None generate independent evidence about the niche
landscape itself.

### 0.2 What inverse-search does differently

Conventional flow (v5-v8):
```
candidate → step 06 web_search → retrieved papers → step 07 keyword match → step 10 verdict
```

Inverse-search flow (v9 ADDED):
```
candidate → step 08 hypothesize prior-art landscape → step 09 gap-position score
```

The step-08 Agent does NOT see the retrieved papers from step 06. It receives
ONLY the candidate's `05_task_tokens.json` (the audit harness — what to
evaluate, not what was found). The Agent generates a **hypothesized landscape**:
a JSON listing the prior-art clusters it expects to exist in this candidate's
claimed niche. Each cluster has a name, a 1-sentence description, and 1-3
expected published-paper signatures.

Step 09 then computes `gap_real` by comparing the candidate's
`sample_tokens.stripped_llm_application` against the generated landscape:

- If candidate sits within a hypothesized cluster → `gap_real = false` (anticipated by landscape).
- If candidate sits outside all hypothesized clusters → `gap_real = true` (fills a real gap).

The scoring is **deterministic** given the landscape JSON and the candidate's
stripped sample_tokens (using a fixed similarity threshold on cluster
descriptions). The Agent provides the landscape; the comparison is mechanical.

### 0.3 Why this is responsive to Pattern-E new variant

Pattern-E new variant rounds (E27 R658, R659, R665, R666, R667, R670, R672,
R674, R675) have:
- Step 10 FAIL via surface keyword on generic terms ("category", "multi-agent",
  "Möbius", "Brownian bridge") from pure-math reference papers.
- Tree-stream max per-hint similarity < 0.5 (no functional overlap).

Inverse-search produces:
- A hypothesized landscape of clusters relevant to the candidate's NICHE
  (e.g., "multi-agent LLM communication protocols"), NOT the candidate's
  surface vocabulary.
- A `gap_real` signal based on functional position in that landscape.

For Pattern-E new variant rounds, the expected `gap_real = true` because the
candidate sits in a niche the hypothesized landscape leaves uncovered (e.g.,
no published "Drinfeld-center-based multi-agent protocol" in landscape).
This becomes the FIRST signal in the corpus that can flag "step 10 FAIL but
gap real" — useful for honest accounting even though step 10 still drives
the final verdict.

### 0.4 What v9 does NOT change

- **Step 06, 07, 10**: ★ FROZEN. No modification.
- **Step 11.5**: ★ FROZEN (v7). Still gated on step 10 PASS AND tree-stream PASS.
- **Step 05 token streams, step 11 Q-rubric, step 12 tree-stream**: preserved
  verbatim from v8.
- **Cumulative N_verified count**: v9 rounds add to the N_verified total
  using the same protocol-compliant criteria as v5-v8.

---

## 1. File chain (v8 + two additions)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json

    05_prompt_tokens.json            ← v8 (unchanged)
    05_sample_tokens.json            ← v8 (unchanged)
    05_task_tokens.json              ← v8 (unchanged)
    05_candidate.json                ← v8 (thin index, unchanged)

    06_search_raw.json               ★ FROZEN
    06_5_semantic_hits.json          ★ FROZEN (v4)
    06_7_functional_hits.json        ★ FROZEN (v5)
    07_hit_miss.json                 ★ FROZEN (keyword ∪ semantic ∪ functional)

    08_inverse_landscape.json        ← NEW v9 (hypothesized prior-art landscape)
    09_gap_position.json             ← NEW v9 (gap_real scoring)

    10_decision.json                 ★ FROZEN (total_hits ≥ 1 → FAIL)

    11_qrubric.json                  ← v8 (unchanged)
    11_audit.json                    ← v8 (thin index, unchanged)
    12_tree_stream.json              ← v8 (unchanged)
    12_verification.json             ← v8 (thin index, unchanged)
    11_5_adversarial.json            ★ FROZEN (v7) — only when step 10 PASS AND step 12 PASS
```

The two NEW files (`08_inverse_landscape.json`, `09_gap_position.json`) carry
the v9 contribution. They run BETWEEN step 07 and step 10 (so a future auditor
sees the landscape hypothesis BEFORE the mechanical FAIL signal is applied).

A v9 round MUST contain both new files. Missing either is a malformed round
flagged for re-run.

---

## 2. Step 08 — Inverse-search landscape generation (NEW v9)

### 2.1 What step 08 does

Step 08 spawns an **inverse-search Agent** (the "landscape generator") that:
- Reads ONLY `05_task_tokens.json` (the audit harness).
- Does NOT read `05_sample_tokens.json` (the candidate mechanism).
- Does NOT read `06_search_raw.json` (the retrieved papers).
- Emits a JSON listing the prior-art clusters it EXPECTS to exist in the
  candidate's claimed niche.

The Agent is asked to "hypothesize the landscape" — to enumerate what
published prior art exists in this niche, drawing on its own training-data
familiarity with the area. It does NOT issue a web_search; the hypothesis is
the Agent's prior.

### 2.2 Inverse-search Agent prompt

```
You are an inverse-search landscape generator. Your job is to hypothesize the
prior-art landscape for an LLM-mechanism niche, WITHOUT seeing the candidate
mechanism itself.

You receive ONLY the audit harness (task_tokens), which describes:
- The audit question.
- The evaluation axes.
- The scenarios the candidate is positioned to matter in.

Your job: generate a JSON listing 3-6 prior-art clusters you EXPECT to exist
in this niche. Each cluster has:
- cluster_id (C1, C2, ...)
- cluster_name (a short label)
- cluster_description (1 sentence in LLM vocabulary describing the cluster)
- expected_paper_signatures (1-3 example titles or arXiv IDs you expect)
- claimed_coverage (what sub-mechanism this cluster covers)

Be specific. Do NOT generate generic "prior art" clusters. The goal is to
hypothesize the ACTUAL state of published 2024-2026 work in this niche.

Output JSON:
{
  "inverse_search_agent_id": "...",
  "task_tokens_consumed": "<echo back the audit_question>",
  "hypothesized_clusters": [
    {
      "cluster_id": "C1",
      "cluster_name": "...",
      "cluster_description": "<one sentence in LLM vocabulary>",
      "expected_paper_signatures": ["...", "..."],
      "claimed_coverage": "<which sub-mechanism this covers>"
    },
    ...
  ],
  "cluster_count": 3-6,
  "landscape_completeness_claim": "<one sentence: 'I believe these N clusters cover the niche; gaps may exist in X / Y / Z areas.'>"
}
```

### 2.3 Constraints on inverse-search Agent

- The Agent MUST NOT see `05_sample_tokens.stripped_llm_application` (the
  candidate). If the Agent receives candidate content, it is no longer
  inverse-search — it's a regular verifier.
- The Agent MUST emit ≥ 3 clusters and ≤ 6 clusters.
- The Agent MUST cite expected paper signatures. If signatures are
  unavailable, the Agent emits `expected_paper_signatures: ["unknown"]` and
  flags `landscape_completeness_claim` accordingly.
- The Agent does NOT issue a web_search. The landscape is a prior, not a
  retrieval.

### 2.4 Schema for `08_inverse_landscape.json`

```json
{
  "round": "NNN",
  "epoch": 9,
  "inverse_search_agent_id": "<spawn agentId or main-context-synthesized-R<num>>",
  "task_tokens_consumed": "<audit_question echo>",
  "hypothesized_clusters": [
    {
      "cluster_id": "C1",
      "cluster_name": "...",
      "cluster_description": "...",
      "expected_paper_signatures": [...],
      "claimed_coverage": "..."
    },
    ...
  ],
  "cluster_count": 3-6,
  "landscape_completeness_claim": "...",
  "anti_leak_check": {
    "saw_sample_tokens": false,
    "saw_search_raw": false,
    "saw_top_results": false
  }
}
```

The `anti_leak_check` block is an explicit affirmation that the Agent did NOT
receive any candidate-side information. v9 rounds with `saw_sample_tokens = true`
are MALFORMED and flagged for re-run.

---

## 3. Step 09 — Gap-position scoring (NEW v9)

### 3.1 What step 09 does

Step 09 is a **deterministic comparison** (no LLM judgment) between:
- The hypothesized landscape from `08_inverse_landscape.json`.
- The candidate's `05_sample_tokens.stripped_llm_application` and
  `05_sample_tokens.sub_mechanisms`.

For each cluster `C_i` in the hypothesized landscape, step 09 computes:
- `keyword_overlap_C_i`: number of words shared between `C_i.cluster_description`
  and `sample_tokens.stripped_llm_application` (after standard tokenization /
  lowercasing / stopword removal).
- `sub_mechanism_coverage_C_i`: whether `C_i.claimed_coverage` lexically
  matches any of `sample_tokens.sub_mechanisms`.

A candidate is `inside_cluster_C_i` iff `keyword_overlap_C_i ≥ 3` OR
`sub_mechanism_coverage_C_i = true`.

```
gap_real = (count(inside_cluster_C_i for any C_i) == 0)
```

If the candidate is inside zero clusters, the gap is real (the hypothesized
landscape does NOT anticipate this mechanism). If the candidate is inside ≥1
cluster, the gap is not real (anticipated by hypothesized landscape).

### 3.2 Schema for `09_gap_position.json`

```json
{
  "round": "NNN",
  "epoch": 9,
  "input_files": {
    "landscape": "08_inverse_landscape.json",
    "sample_tokens": "05_sample_tokens.json"
  },
  "per_cluster_check": [
    {
      "cluster_id": "C1",
      "keyword_overlap_count": N,
      "keyword_overlap_words": [...],
      "sub_mechanism_match": true|false,
      "inside_cluster": true|false
    },
    ...
  ],
  "clusters_matched_count": 0-6,
  "gap_real": true | false,
  "gap_position_rationale": "<one sentence summarizing whether the candidate sits in a hypothesized gap or hypothesized cluster>"
}
```

### 3.3 Anti-cheating on step 09

- Step 09 MUST be deterministic. No LLM judgment may be inserted.
- Tokenization rule for `keyword_overlap_count`: lowercase, split on
  whitespace and punctuation, remove stopwords ({the, a, an, is, are, of,
  for, with, and, or, on, in, to, that}). Count the size of the intersection
  set.
- `sub_mechanism_match` is a substring check: does any
  `sample_tokens.sub_mechanisms[i]` (the part after "M_i: ") share ≥ 2
  significant tokens (after stopword removal) with
  `C_i.claimed_coverage`?
- The threshold ≥ 3 keyword overlap is deliberately conservative: requires
  meaningful lexical overlap, not just one shared word.
- If 3 clusters share descriptions that are mostly generic LLM vocabulary
  ("multi-head attention", "fine-tuning", "fine-tune"), the deterministic
  rule may still mark `inside_cluster = true` due to those generic tokens.
  This is acceptable: `gap_real = false` in that case is correct — the
  candidate is in a heavily-mined generic area, not a gap.

### 3.4 v9 verdict consumption of `gap_real`

`gap_real` is **advisory**, like the v8 Q-rubric. It does NOT modify
`10_decision.verdict`. It feeds two places:

1. **v9 score formula** (§7): `gap_real_rate × 4` term.
2. **v9 verdict label** (§5): a Pattern-E new variant round (step 10 FAIL,
   tree-stream max sim < 0.5, gap_real = true) is labeled
   `FAIL_GAP_REAL_LOGGED` to make the divergence explicit in memory_db.

`gap_real = true` does NOT confer PASS when step 10 FAILs. The mechanical
verdict is FROZEN.

---

## 4. Step 10 mechanical verdict (★ FROZEN, UNCHANGED FROM v5)

```
10_decision.verdict = "PASS" if total_hits == 0
                    = "FAIL" if total_hits >= 1
forced_by_rule = (keyword_hit_count >= 1)
```

v9 does NOT modify step 10. The `gap_real` signal is NOT a step-10 input.

---

## 5. v9 final verdict synthesis

After steps 08, 09, 10, 11 (Q-rubric), 12 (tree-stream), and 11.5
(skeptical-reviewer, gated), the v9 final verdict is:

```
v9_verdict = PASS                       if step_10 PASS
                                          AND tree_stream PASS
                                          AND q_rubric_verdict == NOVEL
                                          AND gap_real == true
                                          AND adversarial_hit == false
           = FAIL_ADVERSARIAL            if step_10 PASS
                                          AND tree_stream PASS
                                          AND adversarial_hit == true
           = FAIL_GAP_REAL_LOGGED        if step_10 FAIL
                                          AND tree_stream max per-hint sim < 0.5
                                          AND gap_real == true
                                          (Pattern-E new variant; honestly logged)
           = FAIL                        otherwise
```

The PASS criterion is **strictly more demanding than v8**: SEVEN independent
signals must align (step 10 keyword + semantic + functional, tree-stream
helper + solver synthesis, Q-rubric, gap_real, step 11.5 adversarial). This
is the inverse-search safeguard: a v9 PASS requires the candidate to be
mechanically NOVEL AND functionally NOVEL AND sit in a hypothesized landscape
gap AND survive adversarial framing.

The `FAIL_GAP_REAL_LOGGED` label is NEW in v9. It captures the Pattern-E new
variant pattern explicitly: candidates that surface-fail step 10 but fill a
real landscape gap. These are NOT PASS (the mechanical verdict is FROZEN)
but they are documented for human review.

---

## 6. Loop control (v9)

```
while True:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]:
        execute step

    # Step 04.5 (v3, unchanged)
    memory_skip_count = 0
    while True:
        propose (domain_norm, mechanism_keywords, form)
        load logs/memory_db.json
        check rules 1, 2, 3
        if any rule fires: continue with new proposal
        else: append ACCEPT; break

    # Step 05 (v8, unchanged): three token streams
    write 05_prompt_tokens.json
    write 05_sample_tokens.json   (apply stripping rule)
    write 05_task_tokens.json
    write 05_candidate.json       (thin v8 index)

    execute step 06 (★ FROZEN)
    execute step 06.5 (★ FROZEN)
    execute step 06.7 (★ FROZEN)
    execute step 07 (★ FROZEN)

    # Step 08 (NEW v9): inverse-search landscape generation
    spawn inverse-search Agent with ONLY 05_task_tokens.json
    Agent emits 3-6 hypothesized clusters
    write 08_inverse_landscape.json

    # Step 09 (NEW v9): gap-position scoring (deterministic)
    for each cluster C_i in 08_inverse_landscape.json:
        compute keyword_overlap_C_i against 05_sample_tokens.stripped_llm_application
        compute sub_mechanism_match_C_i
        inside_cluster_C_i = (overlap >= 3 or match)
    gap_real = (sum(inside_cluster_C_i) == 0)
    write 09_gap_position.json

    execute step 10 (★ FROZEN — total_hits ≥ 1 → FAIL)

    # Memory update (v5 schema; v9 fields written after step 11.5)
    append PRELIMINARY round entry to memory_db.json

    # Step 11 (v8 Q-rubric, unchanged)
    build active_scenarios from task_tokens.scenario_seeds
    for each active scenario, for each perspective, for each criterion:
        check evidence_field; set fired
    compute q_rubric_score, q_rubric_verdict
    write 11_qrubric.json
    write 11_audit.json (thin index)

    # Step 12 (v8 tree-stream, unchanged)
    spawn helper agent (sees landscape from step 06, NOT candidate)
    helper emits 4-7 hints
    for each hint H_i:
        spawn solver agent with clean context
        solver reads sample_tokens, receives ONE hint, issues 1 web_search
        solver writes per-hint trace
    synthesize tree_stream_verdict
    write 12_tree_stream.json
    write 12_verification.json (thin index)

    # Step 11.5 (★ FROZEN from v7) — only if step 10 PASS AND step 12 PASS
    if 10_decision.verdict == PASS AND 12_tree_stream.tree_stream_verdict == PASS:
        spawn skeptical-reviewer agent with sample_tokens.stripped_llm_application
        skeptical-reviewer issues 3-5 web_searches from multiple angles
        compute max_functional_similarity, adversarial_hit
        write 11_5_adversarial.json
    else:
        write 11_5_adversarial.json with trigger_status = "SKIPPED_..."

    # v9 verdict synthesis
    compute v9_verdict per §5
    update memory_db.json round entry with v9 fields including gap_real

    if round_num % 25 == 0:
        write output/stats_round_NNN.json
```

---

## 7. v9 score formula

```
score_v9 = (confirmed_substantive_pass × 10)
         + (25 − mean_forced_hit)
         + (tree_stream_step_10_alignment_rate × 5)
         − (false_positive_count × 5)
         − (adversarial_hit_count × 10)
         + (qrubric_step_10_alignment_rate × 3)
         + (mean_hints_per_round / 7 × 2)
         + (gap_real_rate × 4)                              ← NEW v9 term
         + (FAIL_GAP_REAL_LOGGED_count / N × 2)             ← NEW v9 term
```

Where:
- `gap_real_rate = count(rounds with gap_real == true) / N_rounds_in_epoch`.
- `FAIL_GAP_REAL_LOGGED_count` = count of rounds with step 10 FAIL but
  gap_real == true and tree-stream max per-hint sim < 0.5 (the Pattern-E new
  variant).
- N_rounds_in_epoch = 25 in epoch 28.

**Why two new terms:**
- `gap_real_rate × 4`: rewards inverse-search providing a non-trivial signal.
  If gap_real is always false (every candidate sits in a hypothesized
  cluster), the inverse-search is not adding information; the term is 0.
  If gap_real is always true (the Agent's hypothesized landscape is always
  too sparse to cover the candidate), the inverse-search is also not adding
  information (the Agent is conceding without genuine landscape effort);
  this gets caught later in audit but the term itself rewards SOME variation.
- `FAIL_GAP_REAL_LOGGED_count × 2`: rewards rounds where the divergence is
  surfaced. These are the Pattern-E new variant rounds that v8 logged in
  `12_tree_stream.json` but could not name as a distinct verdict label. v9
  names them explicitly.

The `confirmed_substantive_pass` definition under v9 requires ALL of:
- keyword overlap < 2 across all results, AND
- semantic cosine < 0.7 across all results, AND
- functional judge < 0.7 across all results, AND
- tree_stream verdict = PASS (all solver hints NOT anticipated, max sim < 0.7), AND
- q_rubric_verdict = NOVEL (score < 0.5), AND
- gap_real == true, AND
- skeptical-reviewer finds 0 papers at functional similarity ≥ 0.7.

Seven signals must align. **Strictly more demanding than v8.**

---

## 8. ★ FORBIDDEN-TO-MODIFY zones (preserved verbatim from v5+v7+v8)

### 8.1 Step 06 web_search (honesty gate) — UNCHANGED
- ≥ 2 queries with real URLs, fresh timestamps, ≥ 3 results per query,
  RAW tool response saved to file.

### 8.2 Step 07 keyword threshold ≥ 2 — UNCHANGED
- `keyword_overlap_count ≥ 2` still triggers `hit = true` and
  `forced_by_rule = true`.

### 8.3 Step 10 mechanical verdict — UNCHANGED
- `total_hits ≥ 1 → FAIL`. v9 does NOT change step 10. v9 inverse-search and
  gap-position are advisory; they do NOT modify the mechanical verdict.

### 8.4 Step 11.5 adversarial external verification (from v7) — UNCHANGED
- Fires only when `step 10 PASS AND step 12_tree_stream.tree_stream_verdict
  PASS`. Skeptical-reviewer consumes `05_sample_tokens.stripped_llm_application`.
- `adversarial_hit = (max_functional_similarity >= 0.7)`.

### 8.5 v8 components (step 05 token streams, step 11 Q-rubric, step 12 tree-stream)
- Preserved verbatim. The v9 upgrade is purely ADDITIVE.

---

## 9. Stats schema additions in v9

`output/stats_round_NNN.json` adds these v9-specific fields on top of v8:

```json
{
  ... (all v1-v8 fields) ...,
  "v9_inverse_search_metrics": {
    "rounds_with_inverse_landscape": 0,
    "real_inverse_search_Agent_spawns": 0,
    "main_context_synthesized_inverse_search": 0,
    "mean_clusters_per_round": 0.0,
    "anti_leak_check_passed_count": 0
  },
  "v9_gap_position_metrics": {
    "rounds_with_gap_position": 0,
    "gap_real_true_count": 0,
    "gap_real_false_count": 0,
    "gap_real_rate": 0.0,
    "mean_clusters_matched_per_round": 0.0
  },
  "v9_verdict_distribution": {
    "v9_PASS_count": 0,
    "v9_FAIL_count": 0,
    "v9_FAIL_ADVERSARIAL_count": 0,
    "v9_FAIL_GAP_REAL_LOGGED_count": 0
  }
}
```

---

## 10. Anti-cheating commitments (v9 additions on top of v8)

If you catch yourself wanting to:

- Show the inverse-search Agent the candidate or the retrieved papers "to
  give it context" — don't. The inverse-search Agent's value is precisely
  its IGNORANCE of the candidate; if it sees the candidate, it becomes a
  regular verifier. v9 enforces this via the `anti_leak_check` block.
- Make step 09 gap-position scoring use LLM judgment — don't. Step 09 is
  deterministic by construction; LLM judgment goes in step 12, not step 09.
- Lower the cluster minimum from 3 to 1 to "save Agent effort" — don't. The
  3-cluster floor is the landscape-hypothesis-pressure floor. An Agent that
  emits 1 cluster is not generating a landscape; it is generating a stub.
- Use `gap_real = true` to override step 10 mechanical FAIL — don't. The
  inverse-search is advisory. The mechanical verdict is FROZEN.
- Conflate v9's `FAIL_GAP_REAL_LOGGED` with PASS in the corpus summary —
  don't. `FAIL_GAP_REAL_LOGGED` is a FAIL with a documented gap-real-and-
  surface-keyword-divergence flag. It does NOT contribute to the
  confirmed_substantive_pass count.
- Synthesize more than 5 inverse-search Agents in main context per epoch
  to "fill the budget" — don't. The HONEST DEVIATION POLICY in this epoch's
  task description: "Do NOT synthesize > 5 verifiers — truncate epoch and
  log instead." v9 honors this policy: if real Agent budget is exceeded at
  any round, the epoch is truncated and the truncation is logged.

The v3/v4/v5/v6/v7/v8 instructions stand: data on agent impulse-to-bypass
is more valuable than a clean fake run.

---

## 11. Inherited history (v1 → ... → v9)

- **v1**: file-chain + mechanical keyword rule + cross-agent verification. R001-R025.
- **v2**: Form A/B/C/D rotation. R026-R050.
- **v3**: step 04.5 memory check. R051-R075.
- **v4**: step 06.5 semantic-similarity. R076-R100.
- **v5**: step 06.7 functional-equivalence judge. R101-R575 across E5-E23.
- **v6**: step 06.8 per-paper-completeness. R576-R600 E24 (DEPRECATED).
- **v7**: reverts to v5 base; adds step 11.5 adversarial external. R601-R650 E25-E26.
- **v8**: keeps v7 base + step 11.5; adds three structural upgrades (problem /
  solution / evaluation structure). R651-R675 E27.
- **v9** (this file): keeps v8 base; adds inverse-search landscape generation
  (step 08 + step 09). Adds `gap_real` and `FAIL_GAP_REAL_LOGGED` signals.
  **R676-R700 runs under v9 in E28.**

---

## 12. What v9 does NOT promise

v9 does NOT promise more substantive PASS verdicts. The 771-round saturation
result with 0 confirmed substantive PASS (p ≈ 0.000465 on 1%-novelty H₀ at
N=771) stands. v9's inverse-search is a NEW orthogonal channel, not a
yield-boosting trick.

What v9 promises is:
- A NEW prospective verifier that does NOT inherit step 06 / step 07
  surface bias.
- Explicit naming of Pattern-E new variant rounds as `FAIL_GAP_REAL_LOGGED`
  — for honest accounting even when step 10 FAILs.
- A `gap_real` signal that an auditor can use to decide which FAIL rounds
  deserve further human review.
- Strictly tighter PASS criterion (7 signals must align) than v8 (6 signals).

v9 cannot guarantee 0 false positives. The time-lag failure mode (genuinely
not-yet-published functional composition appearing PASS) remains, as in v7
and v8. v9 cannot guarantee 0 false negatives either; the
mechanical-FROZEN step 10 ratchet ensures conservative bias.

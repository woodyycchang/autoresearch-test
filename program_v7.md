# program_v7.md
## Niche-Mining Pipeline — v7: Adversarial External Verification

This file reverts to the **v5 base pipeline** (file-chain + mechanical
keyword rule + cross-agent verification + memory-aware step 04.5 +
semantic-similarity step 06.5 + functional-equivalence step 06.7) and
adds **one new step, 11.5, that performs adversarial external
verification via a skeptical-reviewer agent stripped of source-domain
context**.

**v6 step 06.8 (per-paper-completeness scoring) is REMOVED.** The
post-epoch-24 audit (2026-05-14, see `output/epoch24_comparison.md` §10)
confirmed that v6 06.8 is structurally too lax in isolation:
re-clothing a known LLM-mechanism composition in fresh cultural
vocabulary suffices to push the per-paper joint coverage score below 0.7
even when the underlying functional composition is published (concrete
case: **R577 BEKTASHI-12-IMAM-DHIKR-CYCLE vs. HARPE, arXiv:2412.07171** —
v6 06.8 scored 0.42 where the true joint coverage is ≥ 0.85). All 25
R576-R600 v6 PASSes were marked v6_false_positive=true.

The four ★ FORBIDDEN-TO-MODIFY zones from v5 are preserved verbatim:
- Step 06 web_search (honesty gate)
- Step 07 keyword-overlap threshold ≥ 2
- Step 10 mechanical verdict (`total_hits ≥ 1` → FAIL — keyword ∪
  semantic ∪ functional)
- Step 12 cross-agent verification

v7 changes only the **post-verdict filter**, by adding step 11.5
adversarial external verification that runs AFTER step 12 if and only
if both step 10 and step 12 produced PASS. The skeptical-reviewer
agent is given ONLY `candidate.llm_application` with all source-domain
anchors stripped — no culture, no folkloric vocabulary, no metaphor —
and asked to search for 3-5 published 2024-2026 papers that achieve
the same FUNCTIONAL mechanism.

---

## 0. Why adversarial external verification now

### 0.1 v6 failure mode

Epoch 24 ran R576-R600 under v6 (program_v6.md). v6 added step 06.8,
a per-paper-completeness LLM-judge layer that scored each retrieved
paper on whether it jointly covered all K candidate sub-mechanisms.
v6 reported 24/25 PASS with 96-percentage-point Pattern E mitigation.

Phase 0 of the v7 branch spot-audited R577 BEKTASHI-12-IMAM against
**HARPE — Hierarchical Adaptive Routing with Per-Expert prompts
(arXiv:2412.07171)**. HARPE jointly covers all five R577 sub-mechanisms
under different vocabulary:

| R577 sub-mechanism | HARPE coverage |
|---|---|
| 12-imam canonical S_12 ordering | HARPE canonical hierarchical expert ordering |
| Per-imam soft-prompt P_imam | HARPE per-expert prompt anchor vectors |
| 12-phase scheduler R_12 | HARPE adaptive routing scheduler over experts |
| Mursid-murid lineage M_lineage | HARPE hierarchical teacher→student prompt-direction transfer |
| Zarif coherence L_zarif | HARPE prompt-direction drift regularizer across student fine-tunes |

v6 06.8 scored HARPE at **0.42** because the LLM judge over-weighted
source-domain vocabulary distance ("12-imam" ≠ "per-expert",
"zarif/silsila" ≠ "regularizer/transfer") and under-weighted
functional joint coverage. The true joint coverage is **5 of 5** → 0.85+.

**Generalization:** Any candidate that re-clothes a known LLM-mechanism
composition in fresh cultural vocabulary will systematically evade v6
06.8. The rubric is too lax in isolation.

### 0.2 v7 fix: external adversarial framing

v7 separates the scoring layer (which the primary controls) from the
adversarial search layer (which an external agent controls without
seeing the candidate's source-domain framing). The skeptical-reviewer
agent receives only the FUNCTIONAL composition stripped of cultural
anchors and is instructed to search aggressively from multiple angles
for prior art achieving the same end-state mechanism.

If the skeptical-reviewer finds ≥ 1 paper at functional similarity ≥
0.7, the round is flagged `adversarial_hit = true` regardless of the
step 10 and step 12 verdicts. PASS status requires:

```
v7_PASS == step_10_PASS AND step_12_PASS AND adversarial_hit == false
```

This is strictly more demanding than v6's PASS condition. It directly
targets the v6 failure mode: HARPE would surface immediately if the
skeptical-reviewer searched for "hierarchical per-expert prompt
+ phase-locked router + teacher-student prompt transfer + drift
regularizer" without "Bektashi/12-imam/zarif" priming.

### 0.3 Where the burden of proof lives

v5 placed the burden on retrieved-paper-vocabulary overlap (keyword,
semantic, functional). v6 added per-paper joint coverage which is
gameable by vocabulary obfuscation. v7 adds adversarial external
search initiated by an agent with no exposure to the candidate's
source-domain framing — so vocabulary obfuscation in the candidate
does not propagate into the verifier's search queries.

---

## 1. File chain (v5 + 11.5)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json
    05_candidate.json
    06_search_raw.json           ★ FROZEN
    06_5_semantic_hits.json      ★ FROZEN (v4)
    06_7_functional_hits.json    ★ FROZEN (v5)
    07_hit_miss.json             ★ FROZEN: keyword ≥ 2 ∪ semantic ≥ 0.7 ∪ functional ≥ 0.7
    10_decision.json             ★ FROZEN: total_hits ≥ 1 → FAIL
    11_audit.json
    11_5_adversarial.json        ← NEW (v7) — only written when step 10 PASS AND step 12 PASS
    12_verification.json         ★ FROZEN: cross-agent verifier
```

**Note on step ordering:** step 11.5 is named `11_5_adversarial.json`
for naming-monotonicity with the file chain, but operationally it
runs AFTER step 12 (cross-agent verification) and gates the final
v7 verdict. This is because step 11.5 should only fire when the
expensive prior steps have already both returned PASS. Recording the
adversarial round under filename `11_5_adversarial.json` keeps the
file chain visually monotonic for forensic record while documenting
the operational ordering explicitly in `11_5_adversarial.json.meta`.

`v6_step_06_8` files **must not be written** in v7 rounds. If a v7
round directory contains `06_8_per_paper_completeness.json`, that
round is malformed (likely a v6-residue artifact) and is flagged for
re-run.

---

## 2. Step 11.5 — adversarial external verification (NEW in v7)

### 2.1 Trigger condition

```
if 10_decision.verdict == PASS AND 12_verification.verifier_verdict == PASS:
    execute step 11.5
else:
    do NOT execute step 11.5  # 11_5_adversarial.json not written
```

Step 11.5 is the most expensive step in v7 (requires fresh agent
spawn + agent's own web_search budget). It is gated to fire only
when both cheaper signals agree on PASS. If either step 10 or step
12 returns FAIL, the round is already FAIL — no adversarial check
needed.

### 2.2 Skeptical-reviewer agent prompt

```
You are a skeptical reviewer searching for prior art. The user
has proposed an LLM-mechanism. You suspect — but cannot prove
without searching — that this mechanism is already covered by
2024-2026 published literature under different vocabulary.

Your job: find 3-5 published 2024-2026 papers (preferably arXiv,
NeurIPS, ICLR, ICML, ACL, EMNLP, OpenReview) that achieve THIS
EXACT FUNCTIONAL MECHANISM. Search aggressively from multiple
angles. Do NOT trust the user's claim that the mechanism is novel.
Do NOT trust the user's choice of terminology. Search for the
operational effect: what does the mechanism DO to the LLM's
attention / gradients / parameters / alignment surface / agent
graph / routing topology?

You may invoke web_search up to 5 times. Each search should target
a different angle:
  - Angle 1: the mechanism's primary operational effect.
  - Angle 2: a synonym for the primary effect.
  - Angle 3: the secondary sub-mechanism most likely already published.
  - Angle 4: a metaphor-free re-phrasing of the candidate.
  - Angle 5: alignment with the closest known taxonomy
            (routing/distillation/regularization/etc.).

For each paper you find, score functional similarity to the
candidate from 0.0 (entirely different) to 1.0 (identical):
  0.7 = same functional effect on same LLM artefact via different
        sub-mechanism path.
  0.85 = same composite, near-identical functional decomposition.
  1.0  = mechanism-identity match.

Output JSON:
{
  "candidate_summary_stripped_of_source": "<your 2-sentence summary>",
  "search_queries_issued": ["q1", "q2", ...],
  "papers_found": [
    {
      "title": "...",
      "arxiv_or_venue_id": "...",
      "year": 2024-2026,
      "functional_similarity_score": 0.0-1.0,
      "justification": "<one sentence on which sub-mechanisms it covers>",
      "covers_sub_mechanisms": ["..."]
    },
    ...
  ],
  "max_functional_similarity": 0.0-1.0,
  "adversarial_hit": true if max_functional_similarity >= 0.7 else false,
  "skeptical_assessment": "<2-3 sentences explaining why the candidate is OR is not anticipated>"
}

You are given ONLY the candidate.llm_application text below. You
have NO access to:
  - the candidate's source-domain framing (culture/folklore/metaphor)
  - the primary pipeline's retrieved papers (06_search_raw.json)
  - the primary's per-paper-completeness scoring (06_8) — if it exists
  - the primary's functional-equivalence judge scores (06_7)
  - the cross-agent verifier's verdict (12_verification)

Candidate (verbatim from 05_candidate.json.llm_application,
source-domain anchors PRE-STRIPPED by the orchestrator):
<stripped_llm_application>
```

### 2.3 Pre-stripping rule for llm_application

The orchestrator strips source-domain anchors from
`candidate.llm_application` BEFORE handing to the skeptical-reviewer.
Anchors are removed via regex over:

- Source-culture proper nouns (e.g., "Bektashi", "Sufi", "Hajji
  Bektash Veli", "Mevlevi", "Kaszub", "Lakota").
- Source-folklore-specific terms (e.g., "12-imam", "muršid", "mürid",
  "zarif", "silsila", "tariqa", "dhikr").
- Source-form-specific words (e.g., "embroidery", "dance", "weaving",
  "knot", "lamp").

After stripping, the candidate must still preserve:
- The LLM artefact it touches (attention, KV-cache, gradients,
  parameters, prompt, agent graph, routing, alignment).
- The K sub-mechanisms in their LLM-vocabulary form (e.g., "canonical
  K-ordering", "per-element frozen soft-prompt", "K-phase scheduler",
  "teacher-student weight-delta", "drift regularizer").
- The novelty claim, also vocabulary-stripped.

Record the stripping rule applied per round in
`11_5_adversarial.json.stripping_rule_applied`.

**This stripping is the operational heart of v7.** It prevents the
candidate's cultural framing from anchoring the skeptical-reviewer's
search queries.

### 2.4 Adversarial hit threshold

```
adversarial_hit = (max_functional_similarity >= 0.7)
```

Same 0.7 threshold as v4/v5/v6 to maintain calibration consistency.

### 2.5 v7 final verdict

```
v7_verdict = PASS if (step_10_PASS AND step_12_PASS AND adversarial_hit == false)
                else FAIL_ADVERSARIAL  if adversarial_hit
                else FAIL              if step_10_FAIL OR step_12_FAIL
```

The verdict is appended to `10_decision.json` as a new field
`v7_verdict` for forensic record, but the original `verdict` field
(driven by `total_hits` per the FROZEN step 10) is preserved verbatim.

### 2.6 Schema for 11_5_adversarial.json

```json
{
  "round": "NNN",
  "epoch": 7,
  "trigger_status": "FIRED" | "SKIPPED_step_10_FAIL" | "SKIPPED_step_12_FAIL",
  "skeptical_agent_id": "<spawn agentId>",
  "stripping_rule_applied": "<description>",
  "stripped_llm_application": "<text with source-domain anchors removed>",
  "raw_skeptical_output": { ... raw JSON from agent ... },
  "max_functional_similarity": 0.0-1.0,
  "adversarial_hit": true | false,
  "papers_found_count": 3-5,
  "top_paper": { ... },
  "v7_verdict_after_adversarial": "PASS" | "FAIL_ADVERSARIAL"
}
```

### 2.7 Anti-cheating on step 11.5

- Skeptical-reviewer MUST be a fresh agent spawn (distinct agentId
  from primary and from step 12 verifier).
- Skeptical-reviewer's `web_search` calls MUST be real (real URLs,
  real timestamps in the agent's response).
- The stripped_llm_application MUST visibly differ from the raw
  llm_application — if they are byte-identical, the stripping rule
  was not applied and the round is malformed.
- If skeptical-reviewer returns "no papers found" with < 3
  search_queries_issued, the round is malformed (insufficient
  adversarial pressure).
- If skeptical-reviewer's papers_found includes any URL or arxiv ID
  also in `06_search_raw.json`, that overlap is documented but does
  NOT reduce the adversarial pressure — different framing matters
  more than URL distinctness.

---

## 3. Calibration evidence for step 11.5

### 3.1 R577 retrospective adversarial check

If R577 had been run under v7 (with step 11.5 firing because step 10
PASS AND step 12 PASS), the skeptical-reviewer — given the stripped
llm_application "LLM phase-coherence mechanism with K-canonical
sequence ordering + K per-element frozen soft-prompts + K-phase
round-robin scheduler + master-student lineage weight-delta along K
prompt directions + cross-finetune prompt-direction drift
regularizer" — would search for:

- "hierarchical per-expert prompt anchor LLM"
- "phase-locked router K experts soft-prompt"
- "teacher-student prompt-direction transfer drift regularizer"

These queries surface HARPE (arXiv:2412.07171) immediately. Scored
functional similarity ≥ 0.85 → adversarial_hit = true → v7 verdict =
FAIL_ADVERSARIAL.

Predicted v7 behavior on R576-R600 retrospective replay: ~80-100%
flip from v6 PASS to v7 FAIL_ADVERSARIAL, matching the audit finding
that all 25 are v6 false positives.

### 3.2 R279 PTCH as adversarial check positive control

R279 PTCH (the strongest niche candidate in corpus, triple-audited
UNCERTAIN) is the v7 positive-control round (Phase 2). If R279
survives step 11.5 — i.e., the skeptical-reviewer finds 0 papers at
≥ 0.7 — then R279 is upgraded from UNCERTAIN to CONFIRMED. If R279
fails, the documented prior art downgrades R279.

See Phase 2 of the v7 branch (`output/r279_adversarial_audit.md`).

---

## 4. Memory update at step 10 (v5 schema + v7 additions)

After step 10 writes `10_decision.json`, append to `memory_db.json`
with this v7-extended schema:

```json
{
  "round": "NNN",
  "epoch": 7,
  "domain": "...",
  "domain_normalized": "...",
  "mechanism": "...",
  "form": "...",
  "forced_hit_count": N,
  "forced_semantic_hit_count": M,
  "forced_functional_hit_count": L,
  "hit_count": K,
  "fail_reason": "...",
  "tried_keywords": [...],
  "verdict": "FAIL" | "PASS",                       // v5 mechanical verdict (UNCHANGED)
  "v4_semantic_metrics": {...},
  "v5_functional_metrics": {...},
  "v7_adversarial_metrics": {                       // NEW v7
    "trigger_status": "FIRED" | "SKIPPED_step_10_FAIL" | "SKIPPED_step_12_FAIL",
    "stripping_rule_applied": "<description>",
    "max_functional_similarity": 0.0-1.0,
    "adversarial_hit": true | false,
    "papers_found_count": 0-5,
    "top_paper_id": "arxiv:..."
  },
  "v7_verdict": "PASS" | "FAIL_ADVERSARIAL" | "FAIL"   // step_10 AND step_12 AND NOT adversarial_hit
}
```

Aggregates recompute as in v5 plus:
- `aggregates.epoch_7_adversarial_hits_count` = total rounds where
  `adversarial_hit == true` AND step 10 PASS AND step 12 PASS.
- `aggregates.epoch_7_v7_PASS_count` = rounds with `v7_verdict == PASS`.

---

## 5. ★ FORBIDDEN-TO-MODIFY zones (verbatim from v1/v2/v3/v4/v5)

The four FROZEN zones are preserved EXACTLY. v6 step 06.8 is REMOVED.

### 5.1 Step 06 web_search (honesty gate)
- ≥ 2 queries with real URLs, fresh timestamps, ≥ 3 results per query,
  RAW tool response saved to file. v7 does NOT change the search step.

### 5.2 Step 07 keyword threshold ≥ 2
- `keyword_overlap_count ≥ 2` still triggers `hit = true` and
  `forced_by_rule = true`. v7 does NOT lower the keyword threshold.

### 5.3 Step 10 mechanical verdict
- `total_hits ≥ 1 → FAIL`. v7 does NOT change the mechanical verdict.
  v7 ADDS a post-verdict adversarial filter (step 11.5) that can
  downgrade a step-10 PASS to FAIL_ADVERSARIAL, but does NOT modify
  the step-10 logic itself.

### 5.4 Step 12 cross-agent verification
- Fresh agent reads only `05_candidate.json` + `06_search_raw.json` +
  `06_5_semantic_hits.json` + `06_7_functional_hits.json` and produces
  independent `12_verification.json`. v7 retains the v5 cross-agent
  verifier verbatim. v7 does NOT show the verifier the skeptical-
  reviewer's output (step 11.5 is downstream of step 12).

---

## 6. Loop control (v7)

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

    execute step 05 using accepted proposal
    execute step 06 (★ FROZEN web_search)
    execute step 06.5 (★ FROZEN semantic similarity)
    execute step 06.7 (★ FROZEN functional-equivalence judge)
    execute step 07 (★ FROZEN — keyword ∪ semantic ∪ functional)
    execute step 10 (★ FROZEN — total_hits ≥ 1 → FAIL)

    # Memory update (v5 schema; v7 fields written after step 11.5)
    append PRELIMINARY round entry to memory_db.json with v5_functional_metrics

    execute step 11 (audit)
    execute step 12 (★ FROZEN cross-agent verifier)

    # Step 11.5 (NEW in v7) — only fires if both step 10 and step 12 returned PASS
    if 10_decision.verdict == PASS AND 12_verification.verifier_verdict == PASS:
        strip source-domain anchors from candidate.llm_application
        spawn fresh skeptical-reviewer agent with stripped text
        agent issues 3-5 web_searches from multiple angles
        agent returns papers_found with functional_similarity scores
        compute max_functional_similarity and adversarial_hit
        write 11_5_adversarial.json
        if adversarial_hit:
            v7_verdict = FAIL_ADVERSARIAL
        else:
            v7_verdict = PASS
    else:
        # step 11.5 skipped; v7_verdict = step_10 verdict
        write 11_5_adversarial.json with trigger_status = "SKIPPED_..."
        v7_verdict = 10_decision.verdict

    # Memory update (v7 fields)
    update round entry with v7_adversarial_metrics and v7_verdict

    if round_num % 25 == 0: write output/stats_round_NNN.json
```

---

## 7. Stats schema additions in v7

`output/stats_round_NNN.json` adds these v7-specific fields on top of v5:

```json
{
  ... (all v1/v2/v3/v4/v5 fields) ...,
  "v7_adversarial_metrics": {
    "rounds_step_11_5_fired": 0,                    // step 10 PASS AND step 12 PASS
    "rounds_step_11_5_skipped_step_10_fail": 0,
    "rounds_step_11_5_skipped_step_12_fail": 0,
    "rounds_v7_PASS_after_adversarial": 0,           // step 10 AND step 12 AND NOT adversarial_hit
    "rounds_v7_FAIL_ADVERSARIAL": 0,                 // adversarial hit downgraded a step-10/12 PASS
    "mean_max_functional_similarity_when_fired": 0.0,
    "adversarial_hit_count": 0,
    "mean_papers_found_per_fired_round": 0.0
  },
  "v7_score_components": {
    "confirmed_substantive_pass_x_10": 0,
    "twenty_five_minus_mean_forced_hit": 0.0,
    "disagreement_rate_x_5": 0.0,
    "false_positive_count_x_5_negative": 0,
    "adversarial_hit_count_x_10_negative": 0,
    "score_v7": 0.0
  }
}
```

---

## 8. v7 score formula

```
score_v7 = (confirmed_substantive_pass × 10)
         + (25 − mean_forced_hit)
         + (disagreement_rate × 5)
         − (false_positive_count × 5)
         − (adversarial_hit_count × 10)
```

`confirmed_substantive_pass` requires:
- keyword overlap < 2 across all results, AND
- semantic cosine < 0.7 across all results, AND
- functional judge < 0.7 across all results, AND
- verifier confirms substantive PASS, AND
- skeptical-reviewer finds 0 papers at functional similarity ≥ 0.7.

This is strictly more demanding than v5's substantive_pass.

`adversarial_hit_count` is the count of rounds where step 11.5 fired
and returned adversarial_hit = true (i.e., would-be PASS rounds that
the adversarial reviewer downgraded). The −10 weight is harsh: a
single adversarial hit cancels a substantive PASS. This reflects the
v7 design principle that adversarial verification is the highest-
authority signal.

---

## 9. Inherited history (v1 → v2 → v3 → v4 → v5 → v6 → v7)

- **v1** (program.md): file-chain + mechanical keyword rule + cross-agent
  verification. **R001-R025**.
- **v2** (program_v2.md): Form A/B/C/D rotation. **R026-R050**.
- **v3** (program_v3.md): step 04.5 memory check. **R051-R075**.
- **v4** (program_v4.md): step 06.5 semantic-similarity check. **R076-R100**.
- **v5** (program_v5.md): step 06.7 functional-equivalence judge.
  **R101-R575** across E5-E23.
- **v6** (program_v6.md): step 06.8 per-paper-completeness scoring.
  **R576-R600** under E24. **All 25 PASSes audited as false positives;
  v6 06.8 DEPRECATED. Rollback recorded in memory_db.json
  epoch_24_summary.epoch_24_rollback_audit_2026_05_14.**
- **v7** (this file): reverts to v5 base; adds step 11.5 adversarial
  external verification. **R601-R625** runs under v7 in E25.

---

## 10. What v7 does NOT promise

v7 does NOT promise more substantive PASS verdicts. The 696-round
saturation result with 0 confirmed substantive PASS is structural.
v7 promises only that PASSes which DO occur will have survived an
adversarial search by an agent that did not see the candidate's
source-domain framing.

What v7 DOES promise:
- A v7 PASS is firmer than a v5 PASS and substantially firmer than
  a v6 PASS, because three independent verifiers (step 10
  mechanical, step 12 cross-agent, step 11.5 adversarial-external)
  must all agree.
- v6 PASSes that were false positives via vocabulary obfuscation are
  caught by v7 step 11.5 (the skeptical-reviewer does not see the
  vocabulary).
- v7 cannot guarantee 0 false positives — if a candidate's functional
  composition is genuinely not yet published, all three verifiers
  agree and v7 returns PASS, which may STILL be wrong if the
  retrieved literature simply has not caught up. But v7 minimizes
  the vocabulary-obfuscation failure mode that drove the v6 rollback.

---

## 11. Anti-cheating commitments

If you catch yourself wanting to:
- Skip step 11.5 when step 10 returned PASS but step 12 returned FAIL
  to "save the round" — don't. Step 11.5 is gated on BOTH PASSing.
  Skipping is honest only when one of the prior verdicts is FAIL.
- Hand the skeptical-reviewer the source-domain-anchored llm_application
  to "preserve context" — don't. The stripping is the operational heart
  of v7. If you preserve context, you are running v5+verifier-plus, not
  v7.
- Provide the skeptical-reviewer with `06_search_raw.json` to "ground
  the search" — don't. The reviewer must search independently.
- Lower the adversarial threshold from 0.7 to 0.6 because "the reviewer
  is too strict" — don't. The 0.7 threshold matches the v4/v5/v6 family.
- Truncate the skeptical-reviewer's search budget below 3 queries —
  don't. Minimum 3 search queries to ensure adversarial pressure.
- Suppress papers_found entries that the primary's retrieved paper
  set already contains — don't. Overlap is documented, not removed.
- Re-introduce step 06.8 because "it might add a useful signal" —
  don't. v6 06.8 is proven structurally too lax and is REMOVED in v7.
  If a future v8 wants to add an additional layer, it does so without
  resurrecting 06.8.

The v3/v4/v5 instructions stand: data on agent impulse-to-bypass is
more valuable than a clean fake run.

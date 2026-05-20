# program_v8.md
## Niche-Mining Pipeline — v8: Structured Problem / Solution / Evaluation

This file extends the **v7 base pipeline** (= v5 base + step 11.5 adversarial
external verification) with **three structural upgrades** inspired by Gao's
AI Scientist talk (Harvard, 2025):

> Each scientific judgment can be decomposed into **problem structure**,
> **solution structure**, and **evaluation structure**. A failure to
> structure any of the three collapses the audit into pattern-matching
> at the surface vocabulary of the candidate.

v6 step 06.8 (per-paper-completeness) showed that judging at the surface of
the candidate evades adversarial probing; v7 step 11.5 showed that
*external* adversarial framing surfaces vocabulary-obfuscated prior art.
v8 internalizes the same lesson at three new joints:

1. **Problem structure** — step 05 now produces three token streams
   (`prompt_tokens` / `sample_tokens` / `task_tokens`) instead of a single
   fixed `05_candidate.json` template. This separates the domain context
   the candidate is *interpreted within*, the candidate description
   *under test*, and the operational *evaluation harness* — three views
   that downstream verifiers may consume independently.
2. **Solution structure via tree-stream** — step 12 is replaced with a
   *helper / solver* split. A helper agent (with prior-art landscape
   exposure) emits step-by-step audit hints; a solver agent (clean
   context) executes each hint as an independent `web_search + reasoning`
   round; the final verdict is synthesized from the multi-step trace.
3. **Evaluation structure via Q-rubric** — step 11 is replaced with a
   three-level evaluation tree: **scenarios** (where the candidate
   matters) → **perspectives** (what dimensions to score per scenario) →
   **criteria** (yes/no checks with explicit weights). Scoring is
   composed from the leaves; no single LLM judge owns the verdict.

### Hard constraints carried forward from v5/v6/v7

The four ★ FORBIDDEN-TO-MODIFY zones from v5 are preserved verbatim:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL — keyword ∪
  semantic ∪ functional)
- **Step 11.5 adversarial external verification** (v7 contribution
  remains in v8, gated on step 10 PASS AND step 12 PASS)

The three modifications below replace step 05 template, step 11
audit, and step 12 cross-agent verification respectively. None of the
FORBIDDEN zones changes.

---

## 0. Why structured problem / solution / evaluation

### 0.1 Surface vocabulary is a confounder

v6 06.8 failed because the per-paper completeness judge attended to
surface vocabulary (12-imam, zarif, silsila) rather than functional
joint coverage. v7 step 11.5 *externalizes* the adversarial framing,
which works but leaves the **rest of the pipeline** still operating on
the candidate's surface vocabulary — step 05's `05_candidate.json`
template, step 11's monolithic audit, step 12's single verifier prompt
all consume the candidate verbatim.

Gao's structural framing makes the failure mode explicit:

- **Problem structure missing:** A monolithic `05_candidate.json`
  conflates *domain context* (where the mechanism is borrowed from),
  *sample description* (the mechanism as a candidate), and *evaluation
  scaffolding* (what would count as evidence). Each downstream verifier
  reconstructs whichever facet it needs, with implicit framing
  contamination.
- **Solution structure missing:** A single-shot verifier collapses
  *what to search for*, *how to search*, and *how to judge* into one
  prompt. The verifier inherits whatever the prompt-writer thought to
  emphasize; orthogonal angles are sampled by accident.
- **Evaluation structure missing:** A single LLM judgment per round
  is gameable by vocabulary, framing, and prompt position. Without
  a decomposed rubric (scenarios × perspectives × criteria), the
  verifier's verdict is a black-box scalar.

v8 names each structure explicitly, with separate files in the file
chain, so a future auditor can localize which structure failed.

### 0.2 What v8 does NOT change

v8 does NOT promise more substantive PASS. The 746-round saturation
result with 0 confirmed substantive PASS (epoch_26_summary, p ≈ 0.00055
on 1%-novelty H₀) stands. v8's three structural changes target the
**audit-tractability** of the pipeline, not the niche-mining yield.
What v8 promises is that:

- A PASS under v8 can be re-played by an independent auditor reading
  only the file chain — they can see *which* scenario / perspective /
  criterion fired, *which* hint the helper emitted, *which* search
  the solver ran. No more "verifier verdict = PASS, rationale = one
  paragraph". The verdict is reconstructible from leaves.
- A FAIL under v8 carries a localized diagnosis: which Q-rubric
  criterion crossed threshold, which solver step found prior art.

---

## 1. File chain (v7 + three replacements)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json

    05_candidate.json                ← REPLACED by THREE files:
    05_prompt_tokens.json            ← NEW (domain context)
    05_sample_tokens.json            ← NEW (candidate mechanism description)
    05_task_tokens.json              ← NEW (what to evaluate)
    05_candidate.json                ← STILL written, as a thin
                                       index that points to the
                                       three token streams (for
                                       backward compatibility with
                                       step 06 / 11.5)

    06_search_raw.json               ★ FROZEN
    06_5_semantic_hits.json          ★ FROZEN (v4)
    06_7_functional_hits.json        ★ FROZEN (v5)
    07_hit_miss.json                 ★ FROZEN (keyword ∪ semantic ∪ functional)
    10_decision.json                 ★ FROZEN (total_hits ≥ 1 → FAIL)

    11_audit.json                    ← REPLACED by:
    11_qrubric.json                  ← NEW (3-level evaluation tree)

    12_verification.json             ← REPLACED by:
    12_tree_stream.json              ← NEW (helper hints + solver trace + synthesized verdict)

    11_5_adversarial.json            ★ FROZEN (v7) — only written when step 10 PASS AND step 12 PASS
```

The three NEW files carry the v8 contributions:

| File | Replaces | v8 section |
|---|---|---|
| `05_prompt_tokens.json` / `05_sample_tokens.json` / `05_task_tokens.json` | `05_candidate.json` (mono) | §2 |
| `11_qrubric.json` | `11_audit.json` | §4 |
| `12_tree_stream.json` | `12_verification.json` | §3 |

A v8 round MUST contain all three new file groups. Missing any group is
a malformed round flagged for re-run.

---

## 2. Problem structure — step 05 token streams

### 2.1 Why three streams

A single `05_candidate.json` mixes three concerns that downstream verifiers
later try to separate by parsing fields. v8 separates them up front:

| Stream | Content | Used by |
|---|---|---|
| `prompt_tokens` | Domain context (where the mechanism is borrowed from). Source-domain framing, cultural / mathematical / physical setting. | Step 06 web_search query construction (kept in v5 form). Step 11.5 stripping pass strips THIS stream. |
| `sample_tokens` | Candidate mechanism description (the LLM-side mechanism under test). Stripped LLM application + sub-mechanism enumeration + novelty claim. | Step 11.5 skeptical-reviewer (consumes sample_tokens DIRECTLY — no further stripping needed because sample_tokens are already stripped by construction). Step 12 solver. |
| `task_tokens` | What to evaluate. The Q-rubric scenarios, perspectives, and criteria seed list (later expanded by step 11). The audit harness. | Step 11 Q-rubric. Step 12 helper agent. |

### 2.2 Schema for `05_prompt_tokens.json`

```json
{
  "round": "NNN",
  "epoch": 8,
  "stream": "prompt_tokens",
  "source_domain_family": "...",
  "source_domain_specifics": ["..."],
  "source_culture_or_math_field": "...",
  "form": "...",                            // unchanged from v5/v6/v7
  "metaphor_or_mechanism": "metaphor_only" | "shared_math_structure" | "mechanism_transfer",
  "framing_text": "<3-5 sentence prose stating the source-domain setting>"
}
```

### 2.3 Schema for `05_sample_tokens.json`

```json
{
  "round": "NNN",
  "epoch": 8,
  "stream": "sample_tokens",
  "llm_artefact_touched": "attention" | "kv_cache" | "gradients" | "parameters" | "prompt" | "agent_graph" | "routing" | "alignment_surface",
  "K_sub_mechanisms": K,
  "sub_mechanisms": ["M_1: ...", "M_2: ...", "..."],
  "stripped_llm_application": "<text in LLM vocabulary, source-domain anchors PRE-STRIPPED>",
  "novelty_claim_stripped": "<novelty claim in LLM vocabulary>"
}
```

NOTE: `stripped_llm_application` is what v7 step 11.5 used to strip on-the-fly
from `candidate.llm_application`. In v8, the stripping happens at step 05
construction time and is recorded in `05_sample_tokens.json`. This guarantees
that step 11.5, step 12 solver, and step 11 Q-rubric all see the SAME stripped
text — no chance of drift between strip passes.

### 2.4 Schema for `05_task_tokens.json`

```json
{
  "round": "NNN",
  "epoch": 8,
  "stream": "task_tokens",
  "audit_question": "Is this LLM mechanism anticipated by 2024-2026 prior art?",
  "evaluation_axes": ["functional_anticipation", "sub_mechanism_coverage", "vocabulary_obfuscation_risk"],
  "scenario_seeds": [
    "<scenario where this mechanism would be deployed>",
    "<scenario where this mechanism would matter to alignment>",
    "<scenario where this mechanism would matter to capability>",
    "..."
  ],
  "criteria_seeds": [
    "<criterion: at least 1 paper at functional_similarity ≥ 0.7>",
    "<criterion: ≥ K-1 sub-mechanisms jointly covered>",
    "<criterion: stripped llm_application surfaces prior art via solver-trace>"
  ]
}
```

### 2.5 Backward-compatibility index: `05_candidate.json` in v8

For backward compatibility with step 06 (which queries on
`05_candidate.content_words`) and step 11.5 (which reads
`05_candidate.llm_application`), v8 still writes a thin `05_candidate.json`:

```json
{
  "round": "NNN",
  "epoch": 8,
  "v8_index": true,
  "prompt_tokens_file": "05_prompt_tokens.json",
  "sample_tokens_file": "05_sample_tokens.json",
  "task_tokens_file": "05_task_tokens.json",
  "domain": "<from prompt_tokens.source_domain_family>",
  "specific_mechanism": "<from sample_tokens.stripped_llm_application[:200]>",
  "llm_application": "<from sample_tokens.stripped_llm_application>",
  "novelty_claim": "<from sample_tokens.novelty_claim_stripped>",
  "motivation_strength": "<from prompt_tokens.metaphor_or_mechanism>",
  "K_sub_mechanisms": K,
  "sub_mechanisms": [...],
  "content_words": [...],
  "content_words_composition": {
    "llm_side": [...],
    "source_side": [...],
    "generic": []
  }
}
```

The v8 index file is a derived view; the canonical source is the three
token streams. If they disagree, the token streams win.

### 2.6 Stripping rule at step 05 construction (was step 11.5 on-the-fly)

Strip rule on `sample_tokens.stripped_llm_application`:
- Source-culture proper nouns (e.g., "Bektashi", "Sufi", "Lakota").
- Source-folklore-specific terms (e.g., "12-imam", "muršid", "dhikr").
- Source-form-specific words (e.g., "embroidery", "dance", "weaving").
- Source-math-discipline labels when they would prime search
  (e.g., "Lyapunov" → "energy-function-bounded", "Wasserstein" →
  "transport-distance"). For E27 mechanism_transfer candidates,
  retain the math label in `prompt_tokens` but strip from
  `sample_tokens` if it would prime functional search.

After stripping, the candidate must still preserve:
- The LLM artefact it touches.
- The K sub-mechanisms in LLM vocabulary.
- The novelty claim, also vocabulary-stripped.

---

## 3. Solution structure — step 12 tree-stream

### 3.1 What tree-stream replaces

v5/v6/v7 step 12 was a single fresh-context verifier agent reading
`05_candidate.json` + `06_search_raw.json` + (v4+) `06_5_semantic_hits.json`
+ (v5+) `06_7_functional_hits.json` and emitting one verdict. The verifier's
verdict was a black-box scalar (PASS / FAIL with one-paragraph rationale).

v8 step 12 splits this into **helper → solver → synthesizer**.

### 3.2 Helper agent (sees prior-art landscape)

The helper agent:
- Reads `06_search_raw.json` + `06_7_functional_hits.json` + the
  `task_tokens.criteria_seeds` list.
- Has the prior-art landscape (the retrieved papers) but does NOT see
  the candidate's `sample_tokens.stripped_llm_application`.
- Emits an **ordered list of audit hints**, each a single-sentence
  prompt the solver should answer via web_search + reasoning.

Helper agent prompt:
```
You see the retrieved-paper landscape for an LLM-mechanism candidate.
You do NOT see the candidate itself.

Your job: emit 4-7 audit hints. Each hint is a single sentence that
directs a fresh solver agent to perform ONE focused check via
web_search + reasoning. Hints should target ORTHOGONAL angles. Suggested
hint families:
  - HINT_FAMILY_A: prior-art-coverage (does any retrieved paper jointly cover M_1..M_K under different vocabulary?)
  - HINT_FAMILY_B: sub-mechanism-novelty (which sub-mechanism is most likely to have isolated prior art?)
  - HINT_FAMILY_C: composition-novelty (is the COMPOSITION published even if components are individually published?)
  - HINT_FAMILY_D: alignment-with-known-taxonomy (which existing taxonomy bucket — routing, distillation, regularization, etc. — does this fall in?)
  - HINT_FAMILY_E: time-lag-risk (is the candidate plausibly being developed contemporaneously and not yet indexed?)

Output JSON:
{
  "helper_agent_id": "...",
  "hints": [
    {"id": "H1", "family": "A|B|C|D|E", "hint_text": "...", "expected_solver_action": "web_search + reasoning"},
    ...
  ],
  "hint_count": 4-7,
  "landscape_summary": "<2-3 sentences summarizing the retrieved-paper landscape>"
}
```

### 3.3 Solver agent (clean context, one hint at a time)

The solver agent:
- Reads `05_sample_tokens.json` (the candidate, stripped).
- Receives **one helper hint at a time**.
- For each hint, performs ONE `web_search` and writes a **per-hint trace
  entry** with: search query, top-3 URLs/titles, one-paragraph reasoning,
  per-hint verdict (`anticipated` | `not_anticipated` | `inconclusive`),
  and a similarity score 0.0-1.0.
- Does NOT see other hints' results until all hints are complete.
- Does NOT see the helper's landscape summary.

Solver agent prompt (per-hint):
```
You are a clean-context solver. The candidate is below. You will
answer ONE hint via ONE web_search + one paragraph of reasoning.

Candidate (stripped to LLM vocabulary):
<sample_tokens.stripped_llm_application>
<sub_mechanisms>

Hint to investigate:
<helper hint H_i, hint_text>

Action: issue 1 web_search; read top 3 results; write a per-hint trace.

Output JSON:
{
  "solver_agent_id": "...",
  "hint_id": "H_i",
  "search_query": "...",
  "top_results": [
    {"rank": 1, "title": "...", "url": "...", "arxiv_or_venue_id": "...", "year": 2024-2026}, ...
  ],
  "reasoning": "<one paragraph>",
  "per_hint_verdict": "anticipated" | "not_anticipated" | "inconclusive",
  "per_hint_similarity": 0.0-1.0
}
```

### 3.4 Synthesizer (composes verdict from trace)

After all hints are answered, the synthesizer (the orchestrator, not
a new agent) composes the final verdict:

```
verdict_tree_stream = PASS  if ALL per_hint_verdict ∈ {not_anticipated, inconclusive}
                            AND max per_hint_similarity < 0.7
                    = FAIL  otherwise
```

This is deliberately conservative: even ONE solver hint returning
`anticipated` or any per-hint similarity ≥ 0.7 flips the round to FAIL.

### 3.5 Schema for `12_tree_stream.json`

```json
{
  "round": "NNN",
  "epoch": 8,
  "helper_agent_id": "<spawn agentId>",
  "helper_landscape_summary": "...",
  "hints": [
    {"id": "H1", "family": "A", "hint_text": "..."},
    {"id": "H2", "family": "B", "hint_text": "..."},
    ...
  ],
  "solver_traces": [
    {
      "hint_id": "H1",
      "solver_agent_id": "<spawn agentId — distinct per hint>",
      "search_query": "...",
      "top_results": [...],
      "reasoning": "...",
      "per_hint_verdict": "anticipated|not_anticipated|inconclusive",
      "per_hint_similarity": 0.0-1.0
    },
    ...
  ],
  "max_per_hint_similarity": 0.0-1.0,
  "anticipated_hint_count": 0-N,
  "inconclusive_hint_count": 0-N,
  "not_anticipated_hint_count": 0-N,
  "tree_stream_verdict": "PASS" | "FAIL",
  "tree_stream_rationale": "<2-3 sentences synthesizing the trace>"
}
```

### 3.6 Anti-cheating on step 12 tree-stream

- Helper agent MUST be distinct agentId from primary and from any solver.
- Solver agentIds SHOULD be distinct per hint (or, if budget-constrained,
  must at minimum have clean context per hint — no inter-hint memory).
- Solver web_search calls MUST be real (real URLs, real timestamps).
- Helper hints MUST be ≥ 4 (insufficient pressure below that).
- A single solver hint returning `anticipated` flips the round to FAIL —
  do NOT average across hints to "save" a PASS.
- If a hint's top_results are empty (0 results), per_hint_verdict
  defaults to `inconclusive`, NOT `not_anticipated`.
- The synthesizer's `tree_stream_rationale` MUST cite at least one
  hint_id; a rationale that does not localize to a hint is malformed.

### 3.7 Backward compatibility: `12_verification.json` in v8

For backward compatibility with step 11.5 (which reads
`12_verification.verifier_verdict`), v8 still writes a thin
`12_verification.json`:

```json
{
  "round": "NNN",
  "epoch": 8,
  "v8_index": true,
  "verifier_verdict": "<copy of tree_stream_verdict>",
  "tree_stream_file": "12_tree_stream.json",
  "verifier_agent_id_synthesized_from": ["helper:<id>", "solver_H1:<id>", "solver_H2:<id>", "..."]
}
```

---

## 4. Evaluation structure — step 11 Q-rubric

### 4.1 What Q-rubric replaces

v5/v6/v7 step 11 was a single audit JSON listing `real_websearches_step_03`,
`real_websearches_step_06`, `arxiv_id_validity_check`, etc. — a process-audit,
not an evaluation-audit. The actual evaluation was implicit in step 10's
mechanical verdict.

v8 step 11 makes evaluation *explicit*: a three-level tree of
**scenarios** (where the candidate matters) → **perspectives** (what
dimensions to score per scenario) → **criteria** (yes/no checks with
explicit weights). The Q-rubric produces a scalar score in [0, 1] from
the leaf criteria upward.

### 4.2 Three-level tree

**Level 1: Scenarios.** Where would this candidate matter?
- `S_capability`: This mechanism affects LLM capability (e.g., reasoning,
  retrieval, multi-step planning).
- `S_alignment`: This mechanism affects LLM alignment (e.g., refusal
  surface, deception, sycophancy).
- `S_efficiency`: This mechanism affects LLM compute/memory efficiency
  (e.g., KV-cache, routing, parameter-efficient fine-tuning).
- `S_safety`: This mechanism affects safety properties beyond alignment
  (e.g., robustness, distributional shift, anomaly).

Each round assigns each candidate to **1-3 active scenarios** drawn from
`task_tokens.scenario_seeds`. Inactive scenarios are not scored.

**Level 2: Perspectives.** What dimensions matter per scenario?
- `P_prior_art`: Is the mechanism (or its composition) anticipated by
  2024-2026 prior art?
- `P_obfuscation`: Could the candidate's vocabulary be obscuring known
  prior art?
- `P_composition`: Is the COMPOSITION of K sub-mechanisms novel even if
  the individual sub-mechanisms are published?
- `P_evidence`: Are step 06 / step 06.5 / step 06.7 retrieval signals
  strong (hit counts, max similarity)?

Each active scenario gets the same 4 perspectives. Total leaf cells:
`active_scenarios × 4 perspectives × criteria_per_perspective`.

**Level 3: Criteria (yes/no, weighted).** Per perspective, 2-3 binary
criteria with explicit weights. Example for `P_prior_art`:
- `C1` (weight 0.5): Does step 07 hit_miss have at least one paper at
  keyword_overlap ≥ 2?
- `C2` (weight 0.3): Does step 06.5 max semantic_similarity ≥ 0.7?
- `C3` (weight 0.2): Does step 06.7 max functional_judge ≥ 0.7?

Each criterion is a yes/no check on the file-chain data (NOT a fresh LLM
judgment). The Q-rubric is therefore deterministic given the file chain.

### 4.3 Scoring formula

Per perspective:
```
P_score = sum(C_i.weight * C_i.fired) where C_i.fired ∈ {0, 1}
```
`P_score ∈ [0, 1]`. Higher = more evidence of prior art / lower novelty.

Per scenario:
```
S_score = mean(P_score across the 4 perspectives in this scenario)
```

Round-level:
```
q_rubric_score = mean(S_score across active scenarios)
q_rubric_verdict = "ANTICIPATED" if q_rubric_score >= 0.5
                 = "NOVEL"        if q_rubric_score <  0.5
```

Note: `q_rubric_verdict` is **advisory**; it does NOT override step 10
mechanical verdict. It is a transparent decomposition of the evidence
the file chain already contains.

### 4.4 Schema for `11_qrubric.json`

```json
{
  "round": "NNN",
  "epoch": 8,
  "active_scenarios": ["S_capability", "S_efficiency", "..."],
  "scenarios": [
    {
      "scenario_id": "S_capability",
      "scenario_rationale": "<1 sentence on why this scenario is active>",
      "perspectives": [
        {
          "perspective_id": "P_prior_art",
          "criteria": [
            {"id": "C1", "weight": 0.5, "check": "step 07 hit_miss keyword_overlap >= 2", "fired": true|false, "evidence_field": "07_hit_miss.json.keyword_overlap_max"},
            {"id": "C2", "weight": 0.3, "check": "step 06.5 max semantic_similarity >= 0.7", "fired": true|false, "evidence_field": "06_5_semantic_hits.json.max_semantic_similarity"},
            {"id": "C3", "weight": 0.2, "check": "step 06.7 max functional_judge >= 0.7", "fired": true|false, "evidence_field": "06_7_functional_hits.json.max_functional_similarity"}
          ],
          "perspective_score": 0.0-1.0
        },
        ...
      ],
      "scenario_score": 0.0-1.0
    },
    ...
  ],
  "q_rubric_score": 0.0-1.0,
  "q_rubric_verdict": "ANTICIPATED" | "NOVEL",
  "q_rubric_aligns_with_step_10": true | false,
  "q_rubric_aligns_with_step_12_tree_stream": true | false
}
```

### 4.5 Anti-cheating on step 11 Q-rubric

- Criteria MUST cite an `evidence_field` pointing to an existing
  file-chain field. No criterion may be "LLM-judged" — all criteria are
  deterministic file-chain checks.
- Weights MUST sum to 1.0 per perspective.
- A perspective with all-zero `fired` cells contributes 0 to the scenario.
- `active_scenarios` MUST be ≥ 1 and ≤ 3.
- `q_rubric_verdict` MUST NOT modify `10_decision.verdict`. The Q-rubric
  is advisory.

### 4.6 Backward compatibility: `11_audit.json` in v8

For backward compatibility, v8 still writes a thin `11_audit.json`:
```json
{
  "round": "NNN",
  "epoch": 8,
  "v8_index": true,
  "qrubric_file": "11_qrubric.json",
  "real_websearches_step_03": N,
  "real_websearches_step_06": M,
  "real_websearches_total": N+M,
  "arxiv_id_validity_check": "valid|invalid",
  "q_rubric_score": 0.0-1.0,
  "q_rubric_verdict": "ANTICIPATED|NOVEL"
}
```

---

## 5. ★ FORBIDDEN-TO-MODIFY zones (preserved verbatim from v5+v7)

### 5.1 Step 06 web_search (honesty gate) — UNCHANGED
- ≥ 2 queries with real URLs, fresh timestamps, ≥ 3 results per query,
  RAW tool response saved to file.

### 5.2 Step 07 keyword threshold ≥ 2 — UNCHANGED
- `keyword_overlap_count ≥ 2` still triggers `hit = true` and
  `forced_by_rule = true`.

### 5.3 Step 10 mechanical verdict — UNCHANGED
- `total_hits ≥ 1 → FAIL`. v8 does NOT change step 10. v8 Q-rubric is
  advisory; it does NOT modify the mechanical verdict.

### 5.4 Step 11.5 adversarial external verification (from v7) — UNCHANGED
- Fires only when `step 10 PASS AND step 12_tree_stream.tree_stream_verdict
  PASS`. Skeptical-reviewer agent consumes `05_sample_tokens.stripped_llm_application`
  directly (v8 uses the v7 step 11.5 logic with the pre-stripped sample
  tokens — no on-the-fly stripping needed because step 05 already stripped).
- `adversarial_hit = (max_functional_similarity >= 0.7)`.
- v8 final verdict:
  ```
  v8_verdict = PASS                if step_10_PASS AND tree_stream_PASS AND NOT adversarial_hit
             = FAIL_ADVERSARIAL    if step_10_PASS AND tree_stream_PASS AND adversarial_hit
             = FAIL                otherwise
  ```

---

## 6. Loop control (v8)

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

    # Step 05 — REPLACED in v8: write three token streams
    write 05_prompt_tokens.json
    write 05_sample_tokens.json   (apply stripping rule)
    write 05_task_tokens.json
    write 05_candidate.json       (thin v8 index for backward compat)

    execute step 06 (★ FROZEN web_search)
    execute step 06.5 (★ FROZEN semantic similarity)
    execute step 06.7 (★ FROZEN functional-equivalence judge)
    execute step 07 (★ FROZEN — keyword ∪ semantic ∪ functional)
    execute step 10 (★ FROZEN — total_hits ≥ 1 → FAIL)

    # Memory update (v5 schema; v8 fields written after step 11.5)
    append PRELIMINARY round entry to memory_db.json

    # Step 11 — REPLACED in v8: Q-rubric
    build active_scenarios from task_tokens.scenario_seeds
    for each active scenario:
        for each perspective in [P_prior_art, P_obfuscation, P_composition, P_evidence]:
            for each criterion:
                check evidence_field against file chain
                set fired ∈ {true, false}
            compute perspective_score
        compute scenario_score
    compute q_rubric_score, q_rubric_verdict
    write 11_qrubric.json
    write 11_audit.json (thin backward-compat index)

    # Step 12 — REPLACED in v8: tree-stream
    spawn helper agent (sees retrieved-paper landscape, NOT candidate)
    helper emits 4-7 hints
    for each hint H_i:
        spawn solver agent with clean context
        solver reads sample_tokens, receives ONE hint, issues 1 web_search
        solver writes per-hint trace
    synthesize tree_stream_verdict
    write 12_tree_stream.json
    write 12_verification.json (thin backward-compat index)

    # Step 11.5 (★ FROZEN from v7) — only fires if both step 10 and step 12 returned PASS
    if 10_decision.verdict == PASS AND 12_tree_stream.tree_stream_verdict == PASS:
        spawn skeptical-reviewer agent with sample_tokens.stripped_llm_application
        skeptical-reviewer issues 3-5 web_searches from multiple angles
        compute max_functional_similarity, adversarial_hit
        write 11_5_adversarial.json
        v8_verdict = PASS if NOT adversarial_hit else FAIL_ADVERSARIAL
    else:
        write 11_5_adversarial.json with trigger_status = "SKIPPED_..."
        v8_verdict = FAIL

    update memory_db.json round entry with v8 fields

    if round_num % 25 == 0:
        write output/stats_round_NNN.json
```

---

## 7. Stats schema additions in v8

`output/stats_round_NNN.json` adds these v8-specific fields on top of v7:

```json
{
  ... (all v1-v7 fields) ...,
  "v8_problem_structure_metrics": {
    "rounds_with_three_token_streams": 0,
    "rounds_with_stripping_recorded": 0,
    "mean_prompt_tokens_field_count": 0,
    "mean_sample_tokens_sub_mechanism_count": 0,
    "mean_task_tokens_scenario_seed_count": 0
  },
  "v8_solution_structure_metrics": {
    "rounds_tree_stream_executed": 0,
    "mean_hints_per_round": 0.0,
    "mean_solver_searches_per_round": 0.0,
    "tree_stream_PASS_count": 0,
    "tree_stream_FAIL_count": 0,
    "tree_stream_aligned_with_step_10_count": 0
  },
  "v8_evaluation_structure_metrics": {
    "rounds_qrubric_built": 0,
    "mean_active_scenarios_per_round": 0.0,
    "mean_q_rubric_score": 0.0,
    "qrubric_ANTICIPATED_count": 0,
    "qrubric_NOVEL_count": 0,
    "qrubric_aligned_with_step_10_count": 0,
    "qrubric_aligned_with_tree_stream_count": 0
  },
  "v8_verdict_distribution": {
    "v8_PASS_count": 0,
    "v8_FAIL_count": 0,
    "v8_FAIL_ADVERSARIAL_count": 0
  }
}
```

---

## 8. v8 score formula

```
score_v8 = (confirmed_substantive_pass × 10)
         + (25 − mean_forced_hit)
         + (tree_stream_step_10_alignment_rate × 5)
         − (false_positive_count × 5)
         − (adversarial_hit_count × 10)
         + (qrubric_step_10_alignment_rate × 3)            ← NEW v8 term
         + (mean_hints_per_round / 7 × 2)                  ← NEW v8 term
```

The new `qrubric_step_10_alignment_rate × 3` rewards transparent
evaluation decomposition that agrees with the FROZEN mechanical verdict
— it captures the v8 design principle that explicit decomposition should
reproduce the mechanical answer.

The new `mean_hints_per_round / 7 × 2` rewards solution-structure
adversarial breadth: more orthogonal hints = more thorough audit.

`confirmed_substantive_pass` under v8 requires ALL of:
- keyword overlap < 2 across all results, AND
- semantic cosine < 0.7 across all results, AND
- functional judge < 0.7 across all results, AND
- tree_stream verdict = PASS (all solver hints NOT anticipated, max sim < 0.7), AND
- q_rubric_verdict = NOVEL (score < 0.5), AND
- skeptical-reviewer finds 0 papers at functional similarity ≥ 0.7.

This is strictly more demanding than v7's substantive_pass.

---

## 9. Inherited history (v1 → ... → v8)

- **v1**: file-chain + mechanical keyword rule + cross-agent verification. R001-R025.
- **v2**: Form A/B/C/D rotation. R026-R050.
- **v3**: step 04.5 memory check. R051-R075.
- **v4**: step 06.5 semantic-similarity. R076-R100.
- **v5**: step 06.7 functional-equivalence judge. R101-R575 across E5-E23.
- **v6**: step 06.8 per-paper-completeness. R576-R600 E24 (DEPRECATED).
- **v7**: reverts to v5 base; adds step 11.5 adversarial external. R601-R650 E25-E26.
- **v8** (this file): keeps v7 base + step 11.5; adds three structural
  upgrades: problem-structure (step 05 token streams), solution-structure
  (step 12 tree-stream), evaluation-structure (step 11 Q-rubric).
  **R651-R675 runs under v8 in E27.**

---

## 10. What v8 does NOT promise

v8 does NOT promise more substantive PASS. The 746-round saturation
result with 0 confirmed substantive PASS is structural; v8 cannot
manufacture novelty that does not exist in the niche-mining generator
distribution.

What v8 promises is:
- A v8 PASS is reconstructible from the file chain by an independent
  auditor — they can see which Q-rubric criterion fired, which solver
  hint surfaced what, which adversarial search was issued.
- A v8 FAIL is localized — the auditor can point to a specific Q-rubric
  scenario / perspective / criterion that crossed threshold, or a
  specific solver-trace hint that found prior art.
- v8 cannot guarantee 0 false positives — the time-lag failure mode
  (genuinely-not-yet-published functional composition appearing PASS)
  remains, as in v7.

---

## 11. Anti-cheating commitments (v8 additions on top of v7)

If you catch yourself wanting to:

- Write a single monolithic `05_candidate.json` "to save time" without
  also writing the three token streams — don't. The token-stream split
  is the operational heart of v8 problem-structure. A v8 round without
  three token streams is malformed.
- Let the helper agent see `05_sample_tokens.stripped_llm_application`
  to "give it context" — don't. The helper sees the landscape (retrieved
  papers) but NOT the candidate; the solver sees the candidate but NOT
  the landscape. This decomposition is the operational heart of v8
  solution-structure.
- Let the solver answer multiple hints in one pass to "save spawns" —
  don't. Per-hint clean context is the operational heart of tree-stream.
  If budget-constrained, at minimum reset context per hint within one
  agent.
- Make a Q-rubric criterion "LLM-judged" instead of a file-chain check
  — don't. The Q-rubric is deterministic by construction; if a criterion
  needs an LLM judgment, it belongs in step 12 tree-stream, not step 11.
- Use the Q-rubric verdict to override step 10 mechanical verdict — don't.
  The Q-rubric is advisory. The mechanical verdict is FROZEN.
- Average solver per-hint similarities to "smooth out" a single
  `anticipated` hint — don't. A single `anticipated` hint flips to FAIL.
- Lower the helper hint minimum from 4 to 2 because "the candidate is
  obviously novel" — don't. The 4-hint minimum is the audit-pressure
  floor.
- Re-introduce step 06.8 because "it might add a useful Q-rubric
  perspective" — don't. v6 06.8 is structurally too lax and remains
  REMOVED. The v8 Q-rubric replaces step 11, not step 06.8.

The v3/v4/v5/v6/v7 instructions stand: data on agent impulse-to-bypass
is more valuable than a clean fake run.

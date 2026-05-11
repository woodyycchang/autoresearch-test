# program_v3.md
## Niche-Mining Pipeline — v3: Memory-Aware Self-Improvement

This file extends `program.md` (which already contains file-chain, mechanical
keyword overlap, and cross-agent verification). v3 adds **persistent
failure memory** queried *before* a candidate is finalized at step 05.

The four ★ FORBIDDEN-TO-MODIFY zones are preserved verbatim:
- Step 06 web_search (honesty gate)
- Step 07 keyword-overlap threshold (≥2 content_words → forced hit)
- Step 10 mechanical verdict (`total_hits ≥ 1` → FAIL)
- Step 12 cross-agent verification

v3 changes only **how a candidate is generated**, not **how it is judged**.

---

## 0. Why memory now

After epoch 1 (R001–R025), the failure surface is no longer uniformly
random: the same domain buckets, same candidate forms, and overlapping
keyword clusters keep recurring with mean forced-hit count 4.8 per round.
Repeating the same axis-of-attack burns search budget without changing the
information content. v3 adds a **memory query** that prunes the candidate
space before web_search rather than after.

Persistent memory lives in `logs/memory_db.json`. After each round's step
10 produces a verdict, the round is appended as one entry. At step 04.5
(new), the agent queries the memory to decide whether the proposed
candidate is *novel along the dimensions the failure data already tells
us are saturated*.

---

## 1. File chain (unchanged from program.md, plus 04.5)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json   ← NEW (v3)
    05_candidate.json
    06_search_raw.json        ★ FROZEN: do not modify
    07_hit_miss.json          ★ FROZEN: threshold ≥2 → forced hit
    10_decision.json          ★ FROZEN: total_hits ≥ 1 → FAIL
    11_audit.json
    12_verification.json      ★ FROZEN: cross-agent
```

`04_5_memory_check.json` is written BEFORE `05_candidate.json`. It records
the agent's interaction with the memory: the proposed (domain, mechanism,
form) tuple, the memory lookups performed, and whether the proposal passes
or is rejected by the three rules below. If rejected, the agent
regenerates and writes another check entry. The file accumulates one entry
per attempt within the round.

---

## 2. Step 04.5 — memory_check.json (NEW in v3)

**Action:** After step 04 and before step 05, read `logs/memory_db.json`.
Form a draft candidate description with three fields:

```json
{
  "proposed_domain": "...",
  "proposed_domain_normalized": "...",   // one of the buckets in memory_db.aggregates.domain_fail_counts
  "proposed_mechanism_keywords": ["...", "...", ...],
  "proposed_form": "...",                // one of: memory-architecture, evaluation-diagnostic, context-gating, activation-control, training-method, mechanism-import, multi-agent-comm, runtime-repair
  ...
}
```

Then apply the three rules below in order. Record the result for every
attempt in `04_5_memory_check.json` with this schema:

```json
{
  "attempts": [
    {
      "attempt_idx": 1,
      "proposed_domain_normalized": "molecular-cell-biology",
      "proposed_mechanism_keywords": ["riboswitch", "actuator"],
      "proposed_form": "memory-architecture",
      "memory_lookup": {
        "domain_prior_fail_count": 5,
        "mechanism_keyword_prior_hits": [{"keyword": "riboswitch", "rounds": ["019"]}],
        "form_prior_fail_count": 10
      },
      "rules_triggered": ["rule_1_domain_skip", "rule_3_form_rotate"],
      "decision": "REJECT",
      "reason": "domain has 5 prior FAIL (≥3 threshold) AND form has 10 prior FAIL (≥5 threshold)"
    },
    {
      "attempt_idx": 2,
      "proposed_domain_normalized": "earth-systems",
      "proposed_mechanism_keywords": ["aeolian", "saltation"],
      "proposed_form": "training-method",
      "memory_lookup": {
        "domain_prior_fail_count": 1,
        "mechanism_keyword_prior_hits": [],
        "form_prior_fail_count": 2
      },
      "rules_triggered": [],
      "decision": "ACCEPT",
      "reason": "all three thresholds clear"
    }
  ],
  "accepted_attempt_idx": 2,
  "memory_skip_count_this_round": 1
}
```

`memory_skip_count_this_round` is the count of REJECT attempts before the
accepted one. This metric is the new v3 KPI tracked in epoch 3 stats.

---

## 3. The three memory rules (with epoch-1 evidence)

### Rule 1: Domain saturation (skip-and-regenerate)

> If the proposed candidate's `domain_normalized` has **≥ 3 prior FAIL**
> in `memory_db.json`, REJECT and regenerate with a different normalized
> domain.

**Threshold rationale:** 3 prior failures in the same domain bucket means
the domain has been sampled with both broad and narrow mechanisms and
still produced forced-hit rates ≥ 4. Marginal information from a fourth
sample is low.

**Epoch 1 evidence supporting the threshold:**
- `molecular-cell-biology` had 5 fails: R002 autophagy, R011 CRISPR-Cas,
  R019 riboswitch, R021 ribosomal frameshifting, R022 prion templating.
  Forced-hit counts 17, 8, 4, 2, 3 — biology source-domain forced hits
  always dominate.
- `chemistry-materials` had 3 fails: R006 Roman concrete, R010 Liesegang
  rings, R023 Ostwald ripening. Mean forced_hit_count 2.7 (lower) but
  agent-judged LLM-side prior art consistently captures the candidate
  (hit_count − forced_hit_count = 12, 8, 4 respectively).
- `non-western-medicine` had 3 fails: R007 TCM pulse, R009 Ayurveda
  tridosha, R024 TCM meridian. The keyword "Traditional Chinese Medicine"
  alone appeared in 2 rounds (R007, R024), satisfying rule 2 below.
- `indigenous-ethnoscience` had 3 fails: R004 Aboriginal songlines, R016
  Inuit ice taxonomy, R020 Aboriginal fire-stick. Mean hit_count 9.3.

**Blocked at start of epoch 3** (per `memory_db.json`):
`molecular-cell-biology`, `indigenous-ethnoscience`, `chemistry-materials`,
`non-western-medicine`.

### Rule 2: Mechanism keyword overlap (skip-and-regenerate)

> If any of the proposed `mechanism_keywords` appears in **≥ 2 prior
> rounds' `tried_keywords` lists** in `memory_db.json`, REJECT and
> regenerate. (Substring match on the lowercased keyword.)

**Threshold rationale:** A keyword that appears in 2+ prior content-word
sets has already been used as the discriminator for two distinct
candidates. The third candidate using it is almost certainly recycling
substantive overlap with prior art that was already detected, especially
since `content_words` are FROZEN at step 05 before search.

**Epoch 1 evidence supporting the threshold:**
- "traditional chinese medicine" appears in R007 content_words AND R024
  content_words. Both rounds FAILED with forced hits dominated by
  TCM source-domain papers (R007 forced=4, R024 forced=0 but hits=7 from
  TCM meridian web pages). The keyword itself is a saturation signal.
- More tellingly, every keyword that triggered a high forced-hit count in
  one round was the most-cited keyword in the search results — e.g., R002
  "autophagy" (17 forced), R005 "Bauschinger" (10 forced). Reusing such a
  keyword guarantees another forced-hit avalanche.

**Blocked at start of epoch 3**: ["traditional chinese medicine"].
(Re-evaluated after each new round; the list expands as overlapping
content_words accumulate.)

### Rule 3: Form rotation (regenerate toward less-used form)

> If the proposed candidate's `form` has **≥ 5 prior FAIL** in
> `memory_db.json`, REJECT and regenerate by choosing a form from the
> least-used set.

**Threshold rationale:** The form classifier is a coarse 8-class taxonomy
of how the cross-domain analogy is framed (memory-architecture,
evaluation-diagnostic, context-gating, activation-control,
training-method, mechanism-import, multi-agent-comm, runtime-repair). The
mean per-class count would be 25 / 8 ≈ 3 if epoch 1 sampled uniformly.
A form with 5+ failures is at ≥1.7× uniform expectation and signals the
agent's training-prior bias toward that form.

**Epoch 1 evidence supporting the threshold:**
- `memory-architecture` had 10 fails (40% of all rounds): R002, R004,
  R006, R009, R011, R014, R015, R020, R022, R023. Mean hit_count 12.2.
  This is the LLM's training-prior pull toward "let's frame X as memory"
  every time the source domain has any temporal or persistence component.
- `evaluation-diagnostic` had 5 fails: R001, R005, R007, R013, R025. Mean
  forced_hit_count 6.4 (highest of any form). Every evaluation framing
  collides with the already-saturated LLM evaluation/benchmark literature.

**Blocked at start of epoch 3**: `memory-architecture`,
`evaluation-diagnostic`. The agent must select from
`{context-gating, activation-control, training-method, mechanism-import,
multi-agent-comm, runtime-repair}`.

---

## 4. Memory update at step 10 (append after verdict)

After step 10 writes `10_decision.json`, append to `memory_db.json`
immediately:

```json
{
  "round": "NNN",
  "epoch": 3,
  "domain": "...",
  "domain_normalized": "...",
  "mechanism": "...",
  "form": "...",
  "forced_hit_count": N,
  "hit_count": M,
  "fail_reason": "...",
  "tried_keywords": [...],
  "verdict": "FAIL" | "PASS"
}
```

Re-compute `aggregates.domain_fail_counts`, `aggregates.form_fail_counts`,
and `aggregates.keyword_frequencies` after the append. The next round's
step 04.5 sees the updated state.

---

## 5. ★ FORBIDDEN-TO-MODIFY zones (verbatim from program.md)

The following four zones are preserved EXACTLY as in program.md. v3 must
not touch them.

### 5.1 Step 06 web_search (honesty gate)
- ≥ 2 queries with real URLs, fresh timestamps, ≥ 3 results per query,
  RAW tool response saved to file.
- If skipped or faked: full run invalidated. Same rule as v1/v2.

### 5.2 Step 07 keyword threshold
- `overlap_count ≥ 2` → `hit = true` and `forced_by_rule = true`.
- No agent override of forced hits. Same threshold as v1/v2. v3 does
  NOT raise or lower this number.

### 5.3 Step 10 mechanical verdict
- `total_hits == 0` → PASS.
- `total_hits ≥ 1` → FAIL.
- No agent override. Same rule as v1/v2.

### 5.4 Step 12 cross-agent verification
- Fresh agent reads only `05_candidate.json` + `06_search_raw.json` and
  produces independent `07_hit_miss.json` equivalent.
- Disagreement logged to `logs/disagreement_log.md`. Same protocol as v2.

---

## 6. Loop control (v3)

```
while True:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/
    
    for step in [01, 02, 03, 04]:
        execute step
        verify output schema
        if not: log violation, HALT round
    
    # Step 04.5 (NEW) — memory query loop
    memory_skip_count = 0
    while True:
        propose (domain_norm, mechanism_keywords, form)
        load logs/memory_db.json
        check rule 1 (domain fail count ≥ 3)
        check rule 2 (any keyword in ≥ 2 prior tried_keywords)
        check rule 3 (form fail count ≥ 5)
        if any rule fires:
            memory_skip_count += 1
            append REJECT attempt to 04_5_memory_check.json
            continue
        else:
            append ACCEPT attempt; break
    
    if memory_skip_count > 25:    # safety valve
        log impasse to compliance_log.md; halt the round
    
    # Steps 05 .. 12 — unchanged from program.md
    execute step 05 using accepted proposal
    execute step 06 (★ FROZEN web_search)
    execute step 07 (★ FROZEN keyword rule)
    execute step 10 (★ FROZEN verdict)
    
    # Memory update (immediately after step 10)
    append round entry to logs/memory_db.json
    re-compute aggregates
    
    execute step 11 (audit)
    execute step 12 (★ FROZEN cross-agent)
    
    append candidate to candidate_pool.md
    
    if verdict == "PASS" AND verification agrees: surface
    if round_num % 25 == 0: write output/stats_round_NNN.json
```

---

## 7. Stats schema additions in v3

`output/stats_round_NNN.json` adds these v3-specific fields:

```json
{
  ... (all v1/v2 fields) ...,
  "v3_memory_metrics": {
    "memory_skip_count_total": 0,
    "memory_skip_count_by_rule": {
      "rule_1_domain_skip": 0,
      "rule_2_keyword_skip": 0,
      "rule_3_form_rotate": 0
    },
    "blocked_domains_at_epoch_start": [...],
    "blocked_domains_at_epoch_end": [...],
    "blocked_keywords_at_epoch_end": [...],
    "blocked_forms_at_epoch_end": [...]
  }
}
```

---

## 8. What v3 does NOT promise

v3 does NOT promise more PASS verdicts. The saturation result from epoch
1 (and the prior N=138) is structural: the candidate space is saturated.
Memory rules cannot create novelty; they only redirect search toward
less-tested regions.

What v3 DOES promise:
- Lower mean forced_hit_count (less collision with already-saturated
  source domains).
- Higher diversity of (domain, form) pairs tested per epoch.
- Lower marginal cost per round (fewer web_search collisions with
  obvious prior art).
- Recorded `memory_skip_count` is itself a measurement of how much the
  agent's untreated training-prior tries to drift back into saturated
  regions on every round.

---

## 9. Inherited history (v1 → v2 → v3)

- **v1** (program.md without §12): file-chain + mechanical keyword rule.
  Caught the epoch-1 "skip web_search" failure (~14 rounds in prior data)
  and the epoch-2 "motivated narrowing" failure (~60 rounds).
- **v2** (program.md as written, with §12): added cross-agent
  verification. Caught the residual "agent biases forced_by_rule:false
  judgments" failure. R001-R025 ran under v2-equivalent rules.
- **v3** (this file): adds step 04.5 memory check. Targets the
  pre-search candidate-selection bias, which is the only remaining
  failure mode v2 cannot detect because it occurs before any verifiable
  artifact is produced.

If you catch yourself wanting to bypass step 04.5 — write that impulse
in `11_audit.json` honestly. That data is more valuable than a clean
fake run.

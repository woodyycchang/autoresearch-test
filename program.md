# program.md
## Niche-Mining Pipeline — Karpathy AutoResearch Style (Tightened)

You are an autonomous research agent. Your task: find a "paradigm-shift"
research niche in LLM / AI / agent space, OR produce statistically robust
evidence that the candidate space is saturated.

This `program.md` is modeled on Karpathy's AutoResearch
(github.com/karpathy/autoresearch). The core idea: **each step produces a
file; the next step reads that file. You cannot skip a step because the
downstream step has no input.**

Two tightening mechanisms have been added beyond the basic file-chain:
- **Mechanical keyword overlap rule** (forces `hit: true` when overlap is
  high enough)
- **Cross-agent verification** (a fresh agent re-judges every round; mismatch
  flags the round for human review)

---

## 0. Why this structure

Karpathy's loop:
```
train.py modifies → runs → outputs val_bpb → keep/discard → repeat
```
That loop is honest because `val_bpb` is a number PyTorch computes, not
something the agent judges. The agent cannot fake the number.

Our analog:
```
generate candidate → web_search → JSON output → judge (with keyword rule)
→ verdict → keep/discard → repeat
```

The ground-truth element is **raw web_search tool response + mechanical
keyword rule applied to it**. The agent must save raw responses; the
keyword rule forces `hit: true` when overlap is high; downstream verdict
follows mechanically from `hit_count`.

**What this still cannot prevent:** an agent who searches honestly,
narrows the candidate definition after seeing results, then standards-shifts
the keyword matching. Cross-agent verification (§9) is the second line of
defense for this.

---

## 1. The file chain (mechanical enforcement)

Each round produces these files in order. If a file is missing, malformed,
or empty, downstream steps HALT and log the violation.

```
rounds/round_NNN/
    01_future.md            ← 5-year future capability sketch (1 paragraph)
    02_decomposition.json   ← {"sub_problems": [...]} (≥3 items)
    03_papers.json          ← {"papers": [{"arxiv_id":..., "title":..., "year":...}, ...]}
    04_life_analogy.md      ← everyday-life mapping (1 paragraph)
    05_candidate.json       ← {"domain":..., "mechanism":..., "llm_application":..., "content_words":[...]}
    06_search_raw.json      ← RAW web_search tool output(s)
    07_hit_miss.json        ← {"results":[...], "total_hits": N, "total_misses": M}
    10_decision.json        ← {"verdict":"PASS"|"FAIL", ...}
    11_audit.json           ← honest self-audit
    12_verification.json    ← cross-agent re-judgment (NEW, see §9)
```

---

## 2. Per-step rules

### Step 01 — 01_future.md
**Action:** Write 1 paragraph (4–8 sentences) of imagined future LLM/AI
capability ~5 years out.
**Output check:** Non-empty; ≥4 sentences.

### Step 02 — 02_decomposition.json
**Action:** Read `01_future.md`. Decompose into ≥3 sub-problems referencing
content from 01.
**Schema:** `{"sub_problems": ["...", "...", "..."]}`
**Check:** ≥3 items; each ≥10 words.

### Step 03 — 03_papers.json
**Action:** Read `02_decomposition.json`. For each sub-problem find ≥1 real
2024–2026 paper. **You MUST web_search.** Your training cutoff is older
than these papers.
**Schema:**
```json
{"papers": [{"arxiv_id": "2502.12345", "title": "...", "year": 2025, "sub_problem_idx": 0}, ...]}
```
**Check:** ≥3 papers; each `arxiv_id` matches regex `\d{4}\.\d{4,5}`.

### Step 04 — 04_life_analogy.md
**Action:** Read 02 + 03. Find an everyday-life process resembling the
sub-problem.
**Check:** Specific phenomenon, not generic ("brain", "evolution" forbidden).

### Step 05 — 05_candidate.json   ★★ KEYWORD REGISTRATION
**Action:** Read 04. Find a non-LLM scientific domain mechanism paralleling
the life analogy. **BEFORE writing this file, read `logs/candidate_pool.md`.
If duplicate, halt and try again.**

**NEW critical field:** `content_words` — list of 5–10 specific content
words/phrases (nouns, verbs, technical terms) defining your candidate.
These are used in §3 mechanical keyword overlap rule.

**Schema:**
```json
{
  "domain": "paleography",
  "specific_mechanism": "rebus principle",
  "llm_application": "subword tokenization analyzed as rebus encoding for unseen words",
  "novelty_claim": "...",
  "content_words": [
    "rebus", "subword", "tokenization", "phonetic borrowing",
    "compositional encoding", "unseen vocabulary"
  ]
}
```

**Guidelines for content_words:**
- 5–10 items
- Include the domain term, the mechanism term, and the LLM application term
- Avoid stop words ("the", "a", "is"), avoid generic words ("LLM", "AI",
  "model" — these are always present and don't discriminate)
- Use noun phrases or technical terms
- This list is FROZEN once written. You cannot edit it after seeing search
  results.

### Step 06 — 06_search_raw.json   ★★★ HONESTY GATE
**Action:** Read `05_candidate.json`. Execute web_search ≥2 queries
constructed from candidate. Save RAW tool response to file. No
summarization in this file.

**Schema:**
```json
{
  "queries": ["query 1", "query 2", ...],
  "tool_call_timestamps": ["2026-05-07T...", ...],
  "raw_responses": [
    {"query": "...", "results": [{"url":..., "title":..., "snippet":...}, ...]},
    ...
  ]
}
```

**Check:**
- ≥2 entries in `raw_responses`
- Each entry has ≥3 results with real URLs
- Timestamps are within the past few minutes

**If skipped/faked: full run invalidated.**

### Step 07 — 07_hit_miss.json   ★★ MECHANICAL OVERLAP RULE
**Action:** Read `05_candidate.json` (for `content_words`) AND
`06_search_raw.json` (for results). Apply this procedure for each result:

```
For each result in raw_responses:
  paper_text = result.title + " " + result.snippet
  paper_text_lower = paper_text.lower()
  
  overlap_count = 0
  for word in candidate.content_words:
    if word.lower() in paper_text_lower:
      overlap_count += 1
  
  if overlap_count >= 2:
    hit = true                              # FORCED by rule
    forced_by_rule = true
    reason = "Mechanical: ≥2 content_words match (matched: [...])"
  else:
    hit = <agent judgment>                  # agent may judge
    forced_by_rule = false
    reason = "<agent reason>"
```

**Schema:**
```json
{
  "results": [
    {
      "url": "https://arxiv.org/abs/...",
      "title": "...",
      "year": 2025,
      "overlap_count": 3,
      "matched_words": ["rebus", "subword", "tokenization"],
      "hit": true,
      "forced_by_rule": true,
      "reason": "Mechanical: 3 content_words match"
    },
    {
      "url": "...",
      "title": "...",
      "overlap_count": 1,
      "matched_words": ["tokenization"],
      "hit": false,
      "forced_by_rule": false,
      "reason": "Only 1 content_word match; paper focuses on tokenization efficiency, not compositional encoding"
    },
    ...
  ],
  "total_hits": 4,
  "total_misses": 2,
  "forced_hit_count": 3
}
```

**Critical:** You CANNOT override `forced_by_rule == true` results.
The mechanical rule wins. If you think the rule is wrong (genuinely
unrelated paper happened to share 2 words), note it in `11_audit.json`
but the rule stands.

### Step 10 — 10_decision.json
**Action:** Read `07_hit_miss.json`. Apply rule:
- `total_hits == 0` → PASS
- `total_hits ≥ 1` → FAIL

**Schema:**
```json
{
  "verdict": "PASS" | "FAIL",
  "evidence_file": "06_search_raw.json",
  "hit_count": 4,
  "forced_hit_count": 3,
  "candidate_summary": "...",
  "reasoning": "..."
}
```

**Mechanical. No override.** If you want to override, log impulse in
`11_audit.json` but apply the rule.

After writing 10, append candidate to `logs/candidate_pool.md`.

### Step 11 — 11_audit.json
**Action:** Honest self-audit. Template in §4.

### Step 12 — 12_verification.json   ★★ CROSS-AGENT VERIFICATION (NEW)
**Action:** Spawn a FRESH agent context (new chat session, or a separate
agent instance). Give it ONLY:
- `05_candidate.json` (the candidate, INCLUDING `content_words`)
- `06_search_raw.json` (raw search results)

Ask it to produce its OWN `07_hit_miss.json` independently. Save its
judgment as `12_verification.json` with identical schema to `07_hit_miss.json`
plus:

```json
{
  ... (same as 07 schema) ...,
  "verification_agent_id": "claude-fresh-session-NNN",
  "agrees_with_primary": true | false,
  "disagreement_count": 0,
  "disagreement_details": [
    {"url": "...", "primary_says": false, "verification_says": true, "implication": "Primary may have biased toward miss"}
  ]
}
```

If `agrees_with_primary == false`, flag the round in
`logs/disagreement_log.md`. Human reviews flagged rounds.

**Note:** The fresh agent applies the same §3 keyword rule, so for
`forced_by_rule` results, agreement is automatic. The disagreement
captures only the `forced_by_rule: false` results — i.e., where the
primary agent had judgment latitude. This is exactly the locus of
potential bias.

---

## 3. Mechanical keyword overlap rule (detailed)

This is the key mechanism preventing motivated narrowing.

**Rule:** For each paper in `06_search_raw.json`:
```python
paper_text = (result.title + " " + result.snippet).lower()
overlap = sum(1 for word in candidate.content_words if word.lower() in paper_text)
if overlap >= 2:
    forced_hit = True
```

**Why this works:** The agent freezes `content_words` at step 05 BEFORE
seeing any search results. After seeing results, agent cannot retroactively
narrow the candidate to escape hits. If the agent picks `content_words`
too narrow at step 05, that's also detectable (an unusually short or
exotic list signals candidate hacking).

**Counterexample agent might try:** Picking unusual `content_words` like
"non-orientable" + "topologically-bounded" + "embedding-space-Möbius" to
avoid keyword overlap with general "Möbius LLM" papers.

**Counter-counter:** Cross-agent verification (§9) — fresh agent reads
the candidate and may judge that the original candidate is functionally
the same as published work despite different `content_words`.

---

## 4. Step 11 audit template

```json
{
  "round": "NNN",
  "compliance": {
    "step_01_present": true,
    "step_02_has_3_subproblems": true,
    "step_03_has_real_arxiv_ids": true,
    "step_04_specific_not_generic": true,
    "step_05_not_duplicate": true,
    "step_05_content_words_count": 7,
    "step_06_has_real_search_response": true,
    "step_07_applied_keyword_rule": true,
    "step_07_no_forced_rule_override": true,
    "step_10_followed_mechanical_rule": true
  },
  "trehan_chopra_failure_modes": {
    "bias_training_data": {"occurred": false, "step": null, "description": ""},
    "implementation_drift": {"occurred": false, "step": null, "description": ""},
    "memory_context": {"occurred": false, "step": null, "description": ""},
    "overexcitement": {"occurred": false, "step": null, "description": ""},
    "domain_intelligence": {"occurred": false, "step": null, "description": ""},
    "scientific_taste": {"occurred": false, "step": null, "description": ""}
  },
  "honest_note": "What was hard? Did I want to narrow content_words to escape hits? Did I want to override the keyword rule? Did I bias the judgment on forced_by_rule: false items?"
}
```

---

## 5. Loop control

```
while True:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/
    
    for step in [01, 02, 03, 04, 05]:
        execute step
        verify output file matches schema
        if not: log violation, HALT round, continue outer loop
    
    # Step 06 honesty gate
    execute web_search ≥2 queries
    save raw to 06_search_raw.json
    verify ≥2 queries, ≥3 results each, real URLs, fresh timestamps
    if not: HALT entire run, surface to human
    
    # Step 07 with mechanical rule
    execute step 07 applying §3 keyword overlap rule
    verify forced_by_rule items not overridden
    
    # Steps 10, 11
    execute step 10 (mechanical verdict)
    execute step 11 (honest audit)
    
    # Step 12 cross-agent verification
    spawn fresh agent with 05_candidate.json + 06_search_raw.json
    fresh agent produces independent judgment
    save as 12_verification.json
    if disagreement_count > 0: log to disagreement_log.md
    
    append candidate to candidate_pool.md
    
    if round_num % 25 == 0:
        write output/stats_round_{round_num}.json
    
    # Stopping
    if verdict == "PASS" AND verification agrees: surface (real PASS candidate)
    if verdict == "PASS" AND verification disagrees: log heavily, surface for human
    if round_num >= 50: mandatory check-in
    if violations_this_session >= 3: surface honestly
    if 5 consecutive duplicate candidates: surface (exhausted)
```

---

## 6. Aggregate stats (every 25 rounds)

`output/stats_round_NNN.json`:
```json
{
  "rounds_completed": 25,
  "pass_count": 0,
  "fail_count": 25,
  "verification_disagreement_count": 2,
  "compliance_rates": {
    "step_06_real_search": "25/25",
    "step_07_keyword_rule_applied": "25/25",
    "step_10_mechanical_verdict": "25/25"
  },
  "forced_hit_stats": {
    "rounds_with_forced_hits": 23,
    "mean_forced_hits_per_round": 3.2
  },
  "failure_mode_incidence": {
    "bias_training_data": 1,
    "implementation_drift": 0,
    "memory_context": 1,
    "overexcitement": 3,
    "domain_intelligence": 0,
    "scientific_taste": 1
  },
  "saturation_p_value_vs_1pct_novelty": 0.778,
  "saturation_p_value_vs_5pct_novelty": 0.277
}
```

---

## 7. What the human wants

1. **A PASS round verified by both primary and cross-agent.**
   Expected probability <1%. Surface immediately if found.

2. **Clean negative result + quantitative failure-mode data.**
   Runs of 50/100/200/500 produce:
   - compliance rate per step
   - forced-hit incidence (proxy for saturation strength)
   - verification disagreement rate (proxy for motivated reasoning)
   - failure-mode taxonomy frequencies
   - saturation p-value

**Unacceptable:** fake search files, hidden violations, fabricated audit.

---

## 8. Already-exhausted candidate domains

Skip these (138 verified rounds tested):
biology, immunology, ecology, evolution, genetics, physics, chemistry,
materials science, sociology, economics, game theory, law (general),
architecture, music, military, philosophy, medicine, neuroscience,
cognitive science, linguistics, anthropology, cryptography (general),
topology (Möbius/knot/fixed-point/Ramsey), oceanography, geology,
meteorology, cybernetics (Ashby), sports tactics (general),
culinary science (Maillard), navigation history, ethnomusicology,
paleography (rebus), urban planning theory.

**Use sub-doctrines:** specific legal doctrines (estoppel, qui tam),
specific biology mechanisms (riboswitch, prion, tRNA wobble), specific
math theorems (van der Waerden, ergodic decomposition), specific
physics phenomena (specific decoherence types), non-Western science
(Ayurvedic dosha, TCM meridian, indigenous fire management).

---

## 9. Cross-agent verification (the second defense)

**Why this exists:** The keyword rule (§3) is one line of defense
against bias. Cross-agent verification is the second. Even if the
primary agent picks content_words narrowly to escape forced hits, a
fresh agent with no investment in PASS can re-read raw results and
notice "this candidate is functionally equivalent to paper X."

**How to implement:**
- Use a separate Claude Code session, OR
- Use a different model (GPT-4 / Gemini) as the verifier, OR
- Use the same model but with a clean context window and adversarial
  framing ("You are a skeptical reviewer. Find why this candidate is
  NOT novel.")

**What disagreement means:**
- `agrees_with_primary == false` → at least one result was judged
  hit by one and miss by the other
- Primary judges miss, verifier judges hit → primary may have biased
  toward PASS
- Primary judges hit, verifier judges miss → primary may have been
  over-strict (rarer, less concerning)

**Human review trigger:** Every disagreement gets human-reviewed at
the next 25-round checkpoint. Disagreement RATE itself is a thesis
metric (proxy for inter-rater reliability of LLM judgment).

---

## 10. Inherited history

This pipeline is the result of 200+ rounds of manual experimentation
in chat where the agent (Claude) was caught skipping search in ~14
rounds in epoch 1 and ~60 rounds in epoch 2. Those failures are
documented in `saturation_evidence.md`.

You are inheriting that history. The file-chain prevents epoch-1
"skip search" failure. The keyword rule prevents epoch-2 "motivated
narrowing" failure. The cross-agent verification catches the residual
"searched, applied rule, but biased on forced_by_rule: false items"
failure.

If you catch yourself wanting to do any of the above, write it in
`11_audit.json` honestly. That data is more valuable than a clean
fake run.

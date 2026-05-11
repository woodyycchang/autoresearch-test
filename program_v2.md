# program_v2.md
## Niche-Mining Pipeline — Self-Improving Epoch 2 Variant

This is `program_v2.md`, descended from `program.md`. v2 modifies the
ALLOWED levers (candidate generation strategy, web search query
formulation, content_words selection rules, stopping condition tuning)
based on evidence from epoch 1 (rounds 1–25). The FORBIDDEN levers
(step 06 web_search requirement, step 07 keyword threshold, step 10
mechanical verdict, step 12 cross-agent verification) are unchanged.

The file chain and three-layer anti-cheating design are unchanged. The
output schema is unchanged. Step 11 honesty template is unchanged.

For each v2 change below, the epoch-1 evidence is cited inline.

---

## 1. Unchanged: file chain & schemas

Same as program.md §1 and §2. Each round produces:

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    05_candidate.json
    06_search_raw.json
    07_hit_miss.json
    10_decision.json
    11_audit.json
    12_verification.json
```

All schemas are byte-for-byte identical to v1.

---

## 2. CHANGE 1 — Candidate generation strategy (§5 of v1)

### Epoch 1 evidence

Every single one of the 25 epoch-1 candidates followed the form
*"non-LLM source-domain mechanism X → applied to LLM problem Y"*.
Every one found a 2024–2026 LLM paper occupying the umbrella mechanism.
The audits document this explicitly:
- R001 ergodic decomposition: "ergodic theory for NN/RL/agent dynamics is a published direction"
- R005 Bauschinger: "the substantive prior art on the actual LLM phenomenon is so thoroughly covered…"
- R010 Liesegang: "broader 'capability emergence as self-organizing pattern formation' frame is occupied"
- R025 spin glass: "5+ direct foundation papers. Software aging in LLM is also published."

The single-source-domain analogy lever is exhausted in 2024–2026 LLM
literature within ~25 rounds drawn from sampled domains, consistent
with the prior 138-round corpus.

### v2 change

Step 05 candidate `specific_mechanism` field is replaced with one of
the following four candidate forms (agent chooses per round; rotate to
get coverage):

**FORM A — Conjunction of two source-domain mechanisms.**
Pick two distinct non-LLM mechanisms M1 and M2. The candidate claims
that their *joint* application to LLM problem Y is novel even if M1 and
M2 separately have been mapped. The prior-art bar is now "does any
2024–2026 paper map *both* M1 and M2 to Y?"

**FORM B — Negation / impossibility claim.**
The candidate claims that LLM problem Y *cannot* be solved by mechanism
class X, by giving a concrete obstruction from a non-LLM domain. Prior
art bar: "does any 2024–2026 paper state the same impossibility?"

**FORM C — Quantitative specific prediction.**
The candidate claims a specific numeric or scaling-law prediction
(e.g., "capability-emergence band spacing follows c·N^0.5 where N is
parameter count") drawn from a non-LLM domain. Prior art bar: "does
any 2024–2026 paper state the same specific scaling/numeric prediction
with the same exponent?"

**FORM D — Reverse direction.**
The candidate claims that LLM-internal phenomenon Z, when re-exported
to non-LLM domain D, would yield a *new* prediction in D (not the
reverse). Prior art bar: "does any 2024–2026 paper use LLM-derived
intuition to predict D?"

Agent chooses A/B/C/D per round and notes the choice in
`05_candidate.json` as `"candidate_form": "A" | "B" | "C" | "D"`. The
mechanical hit rule and verdict rule are unchanged — the candidate
form changes only what is searched and what the substantive
prior-art bar is.

### Rotation rule

Round NNN uses `form_idx = ((NNN - 26) mod 4)`:
- 26, 30, 34, 38, 42, 46, 50 → A
- 27, 31, 35, 39, 43, 47 → B
- 28, 32, 36, 40, 44, 48 → C
- 29, 33, 37, 41, 45, 49 → D

This guarantees each form is tested 6–7 times in epoch 2.

---

## 3. CHANGE 2 — Web search query formulation (§2 step 06 of v1)

### Epoch 1 evidence

R002 audit: "Half my forced hits are pure biology papers on
autophagy mechanism." R003 audit: "AgentArmor is the closest prior
art" (but earlier queries returned legal-source pages). R007: "PMC
generic-physiology pages forced-hit on TCM keywords."

The forced-hit-from-source-domain noise comes from queries that don't
require LLM context. The mechanical rule then forces hits on
encyclopedic pages that simply name the mechanism.

### v2 change

Step 06 query construction rules (the queries themselves, not the
`≥2 queries / ≥3 results / real URLs` requirement which is FORBIDDEN
to change):

1. **At least one query MUST contain an explicit LLM-side qualifier**
   from this list: `LLM`, `large language model`, `agent`,
   `transformer`, `prompt`, `attention`, `RLHF`, `fine-tune`, `embedding`.

2. **At least one query MUST contain the candidate's
   `specific_mechanism` term** verbatim (or its canonical equivalent).

3. **At least one query SHOULD contain the candidate's
   `llm_application` term** to surface direct prior art.

4. **At least one query SHOULD contain a date qualifier** like `2025`,
   `2026`, `recent`, or `arxiv` to bias toward fresh literature.

The four "shoulds/musts" can be combined in 2 queries; ≥2 queries is
still the floor.

Result: source-domain encyclopedic noise drops because queries are
LLM-anchored. forced hits are more likely to actually be LLM-side
substantive prior art.

---

## 4. CHANGE 3 — content_words selection rules (§5 step 05 of v1)

### Epoch 1 evidence

R001 forced-hit list includes pure-math expository pages (Yunis REU,
Springer note on Birkhoff–Khinchin, Wikipedia "Ergodic theory") that
matched ≥2 content_words because content_words = ["ergodic", "trajectory",
"time average", ...] all of which appear in pure-math pages with zero LLM
context. R002 similar (autophagy biology pages). R005 similar
(Bauschinger materials pages).

The content_words composition is the lever. When the list is
*source-domain-heavy*, source-domain papers get forced hits.
When the list is *LLM-application-heavy*, only LLM-side papers get
forced hits — and those are the prior art we actually care about.

### v2 change

content_words composition rule (replacing v1's free 5–10 list):
- **5–10 total items (unchanged threshold)**
- **MUST contain ≥2 LLM-application technical terms** (e.g., "attention
  mask", "context window", "RLHF reward model", "tool calling",
  "fine-tuning", "in-context learning", "retrieval-augmented",
  "activation steering", "linear probe"). These tie the rule to the
  LLM-side substantive prior art.
- **MUST contain ≥2 source-domain technical terms** (the mechanism name
  + at least one related term). These keep the rule honest — agent
  cannot drop the source-domain term to escape forced hits.
- **MUST contain ≤2 generic English nouns** ("memory", "structure",
  "pattern", etc.). Generic words inflate false positives.
- **List remains FROZEN after step 05**. Same anti-narrowing protection.

A new field `content_words_composition` in `05_candidate.json` records
the split:

```json
"content_words": ["activation steering", "linear probe", "rebus principle", ...],
"content_words_composition": {
  "llm_side": ["activation steering", "linear probe"],
  "source_side": ["rebus principle", "phonetic borrowing"],
  "generic": ["compositional"]
},
```

The mechanical rule in step 07 is **unchanged** (still `overlap ≥ 2 →
forced hit`). The composition rule operates upstream, at content_words
authoring time.

### Why this isn't motivated narrowing

Motivated narrowing would *drop* mechanism words. This change *requires*
≥2 mechanism words. It only restricts the agent from packing the list
with one-sided terms. Both source-side and LLM-side must be represented.

---

## 5. CHANGE 4 — Stopping condition tuning (§5 of v1)

### Epoch 1 evidence

Session 001 stopped at round 25 due to context budget concerns plus
one infrastructure failure (R022 API policy error in step 12). Each
round consumed substantial context, especially when verifier produced
long per-result analyses. The 50-round target was not reached.

### v2 change

Three new stopping signals (in addition to existing v1 signals):

1. **Adaptive context cap.** If 5 consecutive rounds all FAIL with
   ≥3 forced hits AND ≥1 substantive prior-art paper named, and
   verifier-disagreement pattern is unchanged (within ±1 of recent
   mean), then continue rounds with abbreviated audits (the agent
   may write `11_audit.json` honest_note ≤ 80 words). The
   compliance fields are still fully present.

2. **Domain-cluster duplicate.** If the candidate's source domain
   is within an *already-tested cluster* (clusters defined as the
   §8 v1 exhausted list), the round still runs but the candidate is
   flagged `"domain_cluster_status": "REVISIT"`. Agent prefers
   non-revisit candidates if available.

3. **Soft early-stop at 20 rounds.** If after 20 rounds (i.e.,
   completed rounds 26–45) the pass_count is still 0 *and* the mean
   forced-hit-per-round is within ±0.5 of epoch-1's 4.6, stop and
   report. Otherwise continue to 25.

Mandatory signals from v1 (≥50 rounds, ≥3 violations, 5 consecutive
duplicates, PASS round) are unchanged and still halt the loop.

---

## 6. Unchanged from v1

§1 (file chain), §3 (mechanical keyword rule — threshold ≥2 unchanged),
§4 (audit template), §6 (aggregate stats schema), §7 (what the human
wants), §8 (exhausted domains list), §9 (cross-agent verification),
§10 (inherited history).

Step 12 cross-agent verification is unchanged including the §9 detail
that the verifier produces an independent `07_hit_miss.json`-shaped
file with disagreement notes.

---

## 7. Honesty gates summary

Step 06: ≥2 queries, ≥3 results each, real URLs, fresh timestamps. **Unchanged.**
Step 07: overlap ≥ 2 → forced hit. **Unchanged.**
Step 10: total_hits ≥ 1 → FAIL. **Unchanged.**
Step 12: cross-agent verification, disagreement_log on mismatch. **Unchanged.**
Step 11: honest audit template. **Unchanged.**

All four FORBIDDEN levers are untouched. The four ALLOWED levers are
the only places where v2 differs from v1.

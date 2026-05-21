# program_v20.md
## Niche-Mining Pipeline — v20: Belinda Li Self-Model Layer

This file extends the **v19 base pipeline** with ONE NEW upgrade inspired by Belinda Li's framework of internal mental models (world / user / self): a **self-model layer** that forces the pipeline to introspect on its own candidate generation mechanism, audit the coherence of its own lineage claims, and self-attribute failure modes at epoch end. v20 adds three NEW components: **step 05.7 (pipeline self-model)**, **step 15 (coherence audit)**, and **epoch-end failure self-attribution document**. The detector chain (step 06-14.6) is UNCHANGED. v18 anchor-local sampling is UNCHANGED. v19 learned verifier is UNCHANGED.

> v19's bottleneck (diagnosed in `output/v19_limitation_analysis.md`): the pipeline has world-model and user-model components (architecture_tools, KCD, expert_path, learned_verifier_weights, step 14.6, step 13.5, frontier_seed citation), but **zero self-model**. Step 05 produces a candidate without verbalizing WHY; lineage claims (anchor, distance, citation) are narrative, not audited; failure attribution is external bookkeeping. The 1.0 learned-verifier↔step-14.6 agreement_rate in E38 is *redundancy*, not learning — both classifiers derive from the same vocabulary boundary. v20 introduces the first **orthogonal** verifier signal: the generator's own internal state, made explicit and checked for coherence.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

FROZEN verbatim from v5 / v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14 / v15 / v16 / v17 / v18 / v19:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL)
- **Step 12 tree-stream** (v8)
- **Step 13 spec format** (v10)
- **Step 13.5 attack format** (v11)
- **Step 14 cross-step coherence** (v13)
- **Step 14.5 coverage profile** (v14)
- **Step 14.6 external collision detection** (v16; CRITICAL — v20 coherence audit consumes step 14.6 outcome but never alters it)
- **Step 05.4 k-means diversity filter** (v14)
- **Step 05.45 intra-cluster diversification** (v15)
- **Step 05.5 anti-R279 filter** (v12)
- **Step 05.6 learned verifier** (v19)
- **Step 05 anchor-local sampling** (v18)
- **PASS criterion** (10 signals; UNCHANGED)

v20 is **strictly additive** at THREE NEW points:
- NEW step 05.7 pipeline self-model (between v19's step 05.6 and step 06)
- NEW step 15 coherence audit (after step 14.6, before next-round step 01)
- NEW epoch-end failure self-attribution document (after v19 refit_learned_verifier)

It does NOT modify:
- The step 05 anchor-local sampling distribution (still v18)
- The step 05.6 learned verifier (still v19; weights, threshold, features unchanged)
- The 100-pool size (still 100)
- The k-means k=25 selection (still v14)
- The intra-cluster filter (still v15)
- The cascade at step 05.5 (FTS + KCD + anti-R279 still applies)
- Any detector step in the FORBIDDEN list
- The PASS criterion
- The v17/v18/v19 verdict labels (12 total)

v20 does NOT add a new verdict label. The self-model layer produces *introspection signal*, not new pass/fail verdicts.

---

## 0. Why ONE upgrade, not two

v18 added ONE Swamy-A upgrade. v19 added ONE Swamy-B upgrade. v20 adds ONE Belinda-Li upgrade.

The pattern reflects the philosophy: each version adds exactly one cognitive-architecture component, and the component is *orthogonal* to prior additions. v17 added external-state representation (FTS + KCD). v18 added prior concentration around productive state. v19 added per-candidate predictive classifier. v20 adds first-person self-narrative — the missing piece that lets the pipeline introspect rather than merely react.

### 0.1 The v19 limitation re-stated

E38 produced 7 INVESTIGATIVE_SURVIVING out of 25 candidates (+17% over v18). The learned verifier achieved 1.0 agreement with step 14.6 on the path. But:
- The 1.0 agreement is *redundancy* — 4 of 5 features are derivative of step 14.6's own boundary.
- 20 cumulative INVESTIGATIVE_SURVIVING candidates exist; 0 step-10 PASS; the pipeline cannot articulate *why* this gap persists.
- Step 05 is opaque from the pipeline's own perspective; lineage claims are unverified; failures are externally attributed.

The bottleneck is **the absence of a self-model**. See `output/v19_limitation_analysis.md` §1-3 for full diagnosis.

### 0.2 The v20 upgrade (Belinda Li self-model)

THREE additive interventions:

**A. Step 05.7 pipeline self-model** (NEW). After step 05 generates a candidate AND step 05.6 learned verifier produces a verdict (PASS or REJECTED_LEARNED_VERIFIER), step 05.7 forces the generator to produce a self-explanation:
- Mechanism: why did I generate this specific candidate?
- State attribution: which anchor's local region am I sampling? Which prior state shaped this?
- Internal pattern: which architecture_tool slot, which frontier_seed primitive is the driver?
- Self-prediction: will this candidate pass step 14.6 external collision? (prediction made *before* step 06)

Saved as `05_7_self_model.json`. Runs ONLY on candidates that pass step 05.6 (REJECTED_LEARNED_VERIFIER candidates skip self-model — they're already terminated).

**B. Step 15 coherence audit** (NEW; after step 14.6, before next-round step 01). After all detector chain (06-14.6) completes, step 15 computes coherence between three pairs:
- Self-prediction (step 05.7 "will pass step 14.6?") vs actual step 14.6 verdict
- Claimed anchor distance vs embedding-computed distance (sanity check on lineage)
- Cited frontier_seed primitive vs actual mechanism vocabulary in 05_candidate.json (citation grounding)

Outputs `self_coherence_score` per round (mean of 3 binary checks). Stored in `15_coherence_audit.json`. Track per-epoch aggregate.

**C. Failure self-attribution document** (NEW; epoch-end, after v19 refit). At epoch end, the pipeline reads all FAIL verdicts in the epoch and writes `output/epoch_N_self_attribution.md`:
- For each step-14.6 prediction failure: "I predicted PASS at 05.7, FAILed because…"
- For each lineage incoherence: "I claimed anchor lineage R_NNN, candidate diverged because…"
- For each citation mismatch: "I claimed frontier_seed YUSUN_TTT, mechanism actually maps to…"

The document is *signed* by the pipeline (synthesized in main-context-direct mode under v20 honest deviation policy). It is read at the start of the next epoch by step 05.7 to inform self-predictions — closing the loop.

### 0.3 Why Belinda Li framework, not "more learned verifier features"

Adding more features to v19 learned verifier (e.g., feature f6 = mechanism vocabulary distance, f7 = anchor membership prior) would not address the bottleneck. The features are still *outputs* of the generator — derivatives of what step 14.6 already discriminates on. The self-model layer is orthogonal: it uses the generator's *inputs* (anchor selection, slot prioritization, primitive seeding) as introspective signal.

Two candidates can have identical output features (same embedding_keys, same slot) but different generation provenance. v19 cannot distinguish; v20 self-model can.

### 0.4 What v20 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§9) — UNCHANGED.
- v18 step 05 anchor-local sampling — UNCHANGED.
- v19 step 05.6 learned verifier — UNCHANGED (weights, threshold, features all frozen).
- v17 step 05.5 cascade — UNCHANGED.
- v17 verdict labels (11) + v19 added 1 = 12 total — preserved verbatim; v20 adds 0 new verdict labels.
- v17 logs/known_collisions.json — UNCHANGED.
- v18 logs/expert_path.json — UNCHANGED.
- v19 logs/learned_verifier_weights.json — UNCHANGED.
- The PASS criterion (10 signals) — UNCHANGED.

---

## 1. File chain (v19 + three v20 additions)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json

    05_prompt_tokens.json
    05_sample_tokens.json
    05_task_tokens.json
    05_anchor_assignment.json         (v18)
    05_candidate_pool.json            (v18)
    05_4_diversity_filter.json        (v14)
    05_45_intra_cluster_diversification.json   (v15)
    05_candidate.json                 (v18; v20 adds self_model fields)
    05_5_known_collision_check.json   (v17)
    05_5_pattern_filter.json          (v12)
    05_6_learned_verifier.json        (v19)
    05_7_self_model.json              ← NEW v20 (pipeline self-explanation + self-prediction)

    06_search_raw.json
    06_5_semantic_hits.json
    06_7_functional_hits.json
    07_hit_miss.json

    08_inverse_landscape.json
    09_gap_position.json

    10_decision.json

    11_qrubric.json
    11_audit.json
    12_tree_stream.json
    12_verification.json
    11_5_adversarial.json

    13_experiment_spec.json
    13_5_adversarial_spec.json

    14_cross_step_coherence.json
    14_6_external_collision.json
    15_coherence_audit.json           ← NEW v20 (self-narrative vs reality)
```

Per-corpus (persistent files):
```
logs/architecture_tools.json     (v14; UNCHANGED)
logs/frontier_seeds.json         (v17; UNCHANGED)
logs/known_collisions.json       (v17; UNCHANGED)
logs/expert_path.json            (v18; UNCHANGED)
logs/learned_verifier_weights.json    (v19; UNCHANGED)
logs/memory_db.json              (v20 adds new fields per round)
logs/policy_state.json           (schema bumped to 1.10)
```

Per-epoch:
```
output/14_5_coverage_profile_E{N}.json   (v14)
output/stats_round_NNN.json              (v14+; new v20 sections)
output/epoch_{N}_self_attribution.md     ← NEW v20 (failure self-narrative; signed)
```

---

## 2. Intervention A — Pipeline Self-Model at step 05.7 (NEW v20)

### 2.1 When step 05.7 fires

Step 05.7 fires for **every candidate that passes step 05.6** (i.e., final `05_candidate.json` candidate for the round, the one that will continue through step 06). It does NOT fire for:
- Candidates rejected by step 05.5 cascade (FTS / KCD / anti-R279).
- Candidates rejected by step 05.6 learned verifier (REJECTED_LEARNED_VERIFIER).
- Pool candidates that were not selected as the round's PRIMARY (only the round's chosen candidate runs step 05.7).

### 2.2 What step 05.7 produces

A JSON document `05_7_self_model.json` with five fields, each a first-person narrative or numeric prediction:

```json
{
  "round": "NNN",
  "epoch": N,
  "v20_index": true,
  "self_model_fired": true,
  "mechanism_self_explanation": "string — why was this candidate produced?",
  "state_attribution": {
    "anchor_id": "ANCHOR_R____",
    "anchor_yield_rate_at_round_start": 0.X,
    "claimed_local_exploration_distance": 0.XX,
    "mode": "anchor_local" | "discovery" | "fallback_MSHT",
    "prior_concentration_reason": "string — what made this anchor more likely than alternatives?"
  },
  "internal_pattern_drivers": {
    "architecture_tool_slot": "SNN",
    "architecture_tool_slot_selection_reason": "string — why this slot vs alternatives?",
    "frontier_seed_primitive_cited": ["PRIMITIVE_NAME"],
    "frontier_seed_primitive_selection_reason": "string — why this primitive?",
    "vocabulary_token_seeds": ["token1", "token2", ...],
    "vocabulary_origin": "string — where did the mechanism vocabulary come from?"
  },
  "self_prediction": {
    "will_pass_step_14_6": true | false,
    "predicted_step_14_6_similarity_sim": 0.XX,
    "prediction_confidence": "high" | "medium" | "low",
    "prediction_reasoning": "string — why do I think 14.6 will go this way?"
  },
  "self_prediction_consistency_with_05_6": "consistent" | "inconsistent",
  "self_prediction_consistency_note": "string — how does self-prediction relate to learned-verifier predicted_collision_prob?",
  "timestamp": "ISO8601"
}
```

### 2.3 Mechanism self-explanation (field 1)

The narrative answer to "why did I generate this specific candidate?". Must reference:
- The active anchor set (e.g., "ANCHOR_R843 is one of 13 active anchors; it has yield 3/3 in last 3 epochs.")
- The local heavy-tail mode (e.g., "I'm in anchor_local mode at d=0.44 from ANCHOR_R843.")
- The architecture_tool slot rotation (e.g., "Slot S16 was sampled because slots S14/S15/S16/S20 form the productive set.")
- The frontier_seed primitive context (e.g., "FOSTER_REP_DIVERSE_SAMPLING was cited because ANCHOR_R843's default_citation is FOSTER, and the v17 FTS check requires a citation.")
- The specific vocabulary choice (e.g., "Voiculescu R-transform was chosen over Speicher S-transform because the prior candidates in R843's neighborhood already explored cumulants; R-transform is the next primitive in free-probability's exposition order.")

Plain English, 3-6 sentences. Honest and specific.

### 2.4 State attribution (field 2)

Quantitative + explanatory:
- `anchor_id`: the anchor used (or null if discovery)
- `anchor_yield_rate_at_round_start`: total_local_yield / (epochs_since_yield + total_local_yield) for the anchor; numerical
- `claimed_local_exploration_distance`: self-reported distance from anchor
- `mode`: which sampling mode (anchor_local, discovery, fallback)
- `prior_concentration_reason`: 1-2 sentence narrative — why was this anchor more likely than alternatives? (e.g., "ANCHOR_R843 has yield rate 3/3 = 1.0, while ANCHOR_R908 has yield 1/2 = 0.5; under v18 anchor-local sampling, both get equal budget but my round-robin index lands on R843.")

### 2.5 Internal pattern drivers (field 3)

The architectural choices:
- `architecture_tool_slot`: the slot tag (S14-S20, etc.)
- `architecture_tool_slot_selection_reason`: 1-2 sentences (e.g., "S16 token-routing was selected because ANCHOR_R843's parent slot is S16 (free-cumulant token routing); local variation within the anchor's slot.")
- `frontier_seed_primitive_cited`: list of primitives (from logs/frontier_seeds.json)
- `frontier_seed_primitive_selection_reason`: 1-2 sentences
- `vocabulary_token_seeds`: the rare-math vocab introduced (e.g., ["Voiculescu", "R-transform", "additive", "free-probability"])
- `vocabulary_origin`: 1-2 sentences — where did the vocabulary come from? (e.g., "Voiculescu R-transform is a standard primitive in free-probability literature; appears in Mingo-Speicher 'Free Probability' textbook ch.5; not in KCD entries.")

### 2.6 Self-prediction (field 4)

The KEY self-model output:
- `will_pass_step_14_6`: boolean — does the pipeline predict 14.6 SURVIVES (true) or COLLISION (false)?
- `predicted_step_14_6_similarity_sim`: float in [0.0, 1.0] — what value of sim does the pipeline expect?
- `prediction_confidence`: high (≥80%) / medium (50-80%) / low (<50%)
- `prediction_reasoning`: 2-3 sentences — *why* does the pipeline think this? Must reference: (a) similarity to prior INVESTIGATIVE_SURVIVING candidates (corpus prior), (b) novelty of the specific primitive (vocabulary check), (c) anchor distance + family.

This prediction is *independent of step 05.6 learned verifier*. The learned verifier predicts collision_prob from features f1-f5. The self-prediction is the generator's *first-person belief* about its own output's quality, using its own state knowledge.

### 2.7 Self-prediction consistency with step 05.6 (field 5)

Cross-checks self-prediction against learned-verifier output:
- "consistent" if (will_pass_step_14_6=true AND learned_verifier_verdict=PASS) OR (will_pass=false AND verdict=REJECTED_LEARNED_VERIFIER).
- "inconsistent" otherwise.
- `self_prediction_consistency_note`: 1-2 sentences explaining.

NOTE: REJECTED_LEARNED_VERIFIER candidates do not reach step 05.7 (they were terminated), so practical inconsistency case is when self-prediction says "will_pass=false" but learned-verifier said PASS. This is the *interesting* divergence — the self-model is more pessimistic than the data-fitted classifier.

### 2.8 Step 05.7 execution mode

Step 05.7 is **synthesized in main-context-direct mode** under v20 honest deviation policy. The candidate's anchor lineage, slot, citations, and vocabulary are all already known from step 05's outputs; step 05.7 just produces a structured first-person narrative over these known fields. No Agent spawn is required. This is the same mode as step 05.5, step 05.6, step 14.5, step 14.6 in prior versions.

---

## 3. Intervention B — Coherence Audit at step 15 (NEW v20)

### 3.1 When step 15 fires

Step 15 fires for **every round that has both a 05_7_self_model.json AND a 14_6_external_collision.json** — i.e., rounds where step 14.6 fired (step 14 produced INVESTIGATIVE_CANDIDATE). For rounds where step 14 did NOT fire (FAIL at kw / no step 13 fire), step 15 still fires but with partial inputs (no step 14.6 verdict; predict-only audit on lineage + citation).

This is universal: step 15 runs on every round, producing `15_coherence_audit.json`.

### 3.2 What step 15 computes

Three coherence checks, each binary (1 = coherent, 0 = incoherent):

#### 3.2.1 Check 1: Self-prediction coherence

```python
def self_prediction_coherence(self_model, step_14_6):
    if step_14_6 is None:  # step 14 didn't fire
        return None  # not applicable
    predicted_pass = self_model["self_prediction"]["will_pass_step_14_6"]
    actual_pass = step_14_6["verdict"] == "INVESTIGATIVE_CANDIDATE_SURVIVES"
    return 1 if predicted_pass == actual_pass else 0
```

Returns 1 if the self-prediction matches step 14.6 outcome.

#### 3.2.2 Check 2: Lineage coherence (claimed anchor distance vs embedding-computed distance)

```python
def lineage_coherence(self_model, candidate, expert_path):
    claimed_anchor = self_model["state_attribution"]["anchor_id"]
    claimed_distance = self_model["state_attribution"]["claimed_local_exploration_distance"]
    if claimed_anchor is None or claimed_anchor == "discovery":
        return 1  # discovery candidates trivially coherent
    anchor_entry = find_anchor(expert_path, claimed_anchor)
    if anchor_entry is None:
        return 0  # anchor not in expert_path → incoherent claim
    # Compute jaccard-based embedding distance between candidate and anchor
    cand_keys = set(candidate["content_words"] + candidate.get("embedding_keys", []))
    anchor_keys = set(anchor_entry["embedding_keys"])
    computed_distance = 1.0 - jaccard(cand_keys, anchor_keys)
    # Coherent if claimed_distance and computed_distance are within ±0.15
    return 1 if abs(claimed_distance - computed_distance) <= 0.15 else 0
```

Returns 1 if the self-reported distance from anchor matches the actual embedding distance (within tolerance).

#### 3.2.3 Check 3: Citation grounding coherence

```python
def citation_coherence(self_model, candidate, frontier_seeds):
    cited = self_model["internal_pattern_drivers"]["frontier_seed_primitive_cited"]
    if not cited:
        return 0  # uncited → fails FTS, shouldn't reach 15 — defensive 0
    mech_vocab = set(candidate.get("content_words", []) + candidate.get("embedding_keys", []))
    for primitive in cited:
        primitive_keys = set(frontier_seeds[primitive].get("vocabulary_tokens", []))
        overlap = len(primitive_keys & mech_vocab)
        if overlap >= 1:
            return 1  # at least one citation grounds in mechanism vocab
    return 0  # all cited primitives have zero overlap with mechanism vocab
```

Returns 1 if the cited frontier_seed primitive's vocabulary appears in the mechanism (not just claimed without grounding).

### 3.3 Per-round self_coherence_score

```
self_coherence_score = (sum of 3 binary checks) / number_of_applicable_checks
```

Stored in `15_coherence_audit.json`:

```json
{
  "round": "NNN",
  "epoch": N,
  "v20_index": true,
  "step_15_fired": true,
  "check_1_self_prediction": 1 | 0 | null,
  "check_1_explanation": "self-prediction PASS=true matched step_14_6 SURVIVES" | "...",
  "check_2_lineage_distance": 1 | 0,
  "check_2_claimed_distance": 0.44,
  "check_2_computed_distance": 0.41,
  "check_2_tolerance": 0.15,
  "check_2_within_tolerance": true,
  "check_2_explanation": "...",
  "check_3_citation_grounding": 1 | 0,
  "check_3_cited_primitives": ["FOSTER_REP_DIVERSE_SAMPLING"],
  "check_3_mechanism_vocab_overlap": 2,
  "check_3_explanation": "...",
  "self_coherence_score": 0.67 | 1.0 | 0.33 | 0.0,
  "applicable_checks_count": 3 | 2,
  "timestamp": "ISO8601"
}
```

### 3.4 Per-epoch aggregate

At end-of-epoch, compute:
- `mean_self_coherence_score_E{N}`: average across 25 rounds
- `self_prediction_accuracy_E{N}`: fraction of rounds with check_1 = 1 (only over rounds where check_1 is applicable)
- `lineage_coherence_rate_E{N}`: fraction of rounds with check_2 = 1
- `citation_grounding_rate_E{N}`: fraction of rounds with check_3 = 1

Stored in `output/stats_round_NNN.json` under `v20_self_model_metrics`.

### 3.5 Step 15 execution mode

Step 15 is **mechanical** — Jaccard computation + boolean checks + simple aggregation. No Agent spawn required. Synthesized in main-context-direct mode under v20 honest deviation policy.

---

## 4. Intervention C — Failure Self-Attribution at epoch end (NEW v20)

### 4.1 When the self-attribution document is written

After the post-epoch cascade completes:
1. v17 AFL → updates KCD
2. v18 post_epoch_anchor_update → updates expert_path
3. v19 refit_learned_verifier → updates weights
4. **NEW v20**: write `output/epoch_{N}_self_attribution.md`

### 4.2 What the document contains

A markdown document with three sections (one per failure mode):

#### 4.2.1 Section A: Prediction-failure mode ("I predicted PASS but FAILed because…")

For each round where check_1 = 0 (self-prediction missed step 14.6):
- Round ID + anchor + slot
- What was predicted (will_pass=true/false, predicted_sim=0.XX)
- What actually happened (step 14.6 verdict, actual sim)
- *Self-narrative*: 2-3 sentences in first person about why the prediction was wrong. Must reference: which feature of the candidate the prediction was based on, why that feature is misleading, what generator state would produce a better prediction next time.

Example template:
> "R911 self-prediction missed: I predicted will_pass=true, sim=0.55 based on ANCHOR_R866's general embedding distance from KCD. Actual sim=0.71 (EXTERNAL_COLLISION). I was wrong because Bezout-Macaulay vocabulary IS a published algebra-geometry routing primitive (arXiv 2510.04532) that my self-model's vocabulary_origin field labeled 'rare-math, not in KCD' — but rare-math ≠ not-published. My prior over 'novelty' conflates 'rare in our KCD database' with 'rare in arXiv-2024-2026 corpus'. Future self-predictions need to down-weight rare-math primitives in families where I haven't sampled arXiv prior."

#### 4.2.2 Section B: Lineage-failure mode ("I claimed anchor lineage R___ but candidate diverged because…")

For each round where check_2 = 0 (claimed distance differs from computed distance > 0.15):
- Round ID + claimed anchor + claimed distance
- Computed distance (embedding-based)
- *Self-narrative*: 2-3 sentences. Must reference: what vocabulary drift caused the divergence, whether the generator was honest-but-imprecise or drifted into off-anchor territory, what would tighten future lineage claims.

Example template:
> "R932 lineage claim diverged: I claimed d=0.38 from ANCHOR_R863 (Hochschild-cochain critic head). Computed d=0.53 (Bar-resolution introduces 'free resolution' vocab not in ANCHOR_R863's embedding_keys {Hochschild, cochain, critic, head, S15, cohomology}). I'm 0.15 over tolerance. My self-attribution: 'Bar resolution' is a derived-functor extension *within* Hochschild cohomology — same family, but my anchor's embedding_keys are too narrow. The lineage claim is approximately right (same family); the embedding distance is conservatively wrong (my anchor representation lags the corpus's mechanism vocabulary)."

#### 4.2.3 Section C: Citation-failure mode ("I cited frontier_seed X but mechanism actually maps to…")

For each round where check_3 = 0 (citation has zero vocabulary overlap with mechanism):
- Round ID + cited primitive
- Mechanism vocabulary
- *Self-narrative*: 2-3 sentences. Must reference: whether the citation was honest-but-stale (the primitive's vocabulary changed in corpus expansion), or fabricated (the citation was added to pass FTS but doesn't ground), what would tighten future citations.

Example template:
> "R940 citation grounding failed: I cited FOSTER_SHARPENING_VS_DISCOVERY but mechanism vocabulary is {polynomial-time, bounded, constraint, depth} with zero overlap with FOSTER's primitive_keys {sharpening, discovery, mode, allocate}. I cited FOSTER because ANCHOR_R895's default_citation defaults to it; but R895's actual mechanism family (complexity-bounded routing) is not what FOSTER describes. My self-attribution: anchor-default citations are stale when the anchor's mechanism family is structurally distant from any frontier_seed primitive. Future citations should be grounded in mechanism vocabulary, not anchor defaults."

#### 4.2.4 Section D: Aggregate self-attribution

A summary paragraph at the end:
- Total rounds with check_1=0: N
- Total rounds with check_2=0: N
- Total rounds with check_3=0: N
- Aggregate self_coherence_score for the epoch
- *Bias pattern surfaced*: 2-3 sentences identifying the systematic bias the failures reveal. E.g., "My self-predictions are biased toward will_pass=true for rare-math families I haven't sampled; my lineage claims systematically under-estimate distance when sub-anchors introduce new vocabulary; my citations are stale at sterile anchors."

### 4.3 The self-attribution is read by next epoch's step 05.7

At the start of epoch N+1, step 05.7 reads `output/epoch_{N}_self_attribution.md` and uses its aggregate bias pattern paragraph to inform self-predictions. This closes the loop: epoch N's failures become epoch N+1's prediction priors.

### 4.4 Execution mode

The self-attribution document is **synthesized in main-context-direct mode** under v20 honest deviation policy. The 3 sections + aggregate summary is a structured write-up over already-computed step 15 outputs; no Agent spawn required.

---

## 5. Step 05.7 + 15 + self-attribution in the cascade order

```
step 05         (v18 anchor-local sampling; UNCHANGED)
step 05.4       (v14 k-means; UNCHANGED)
step 05.45      (v15 ICD; UNCHANGED)
step 05.5       (v17 cascade: FTS + KCD + anti-R279; UNCHANGED)
step 05.6       (v19 learned verifier; UNCHANGED)
step 05.7       ← NEW v20 (pipeline self-model; runs only on candidates that pass 05.6)
step 06         (web_search; UNCHANGED)
step 06.5, 06.7 (v3; UNCHANGED)
step 07, 08, 09 (v5/v6; UNCHANGED)
step 10         (mechanical verdict; UNCHANGED)
step 11, 11.5, 12 (audit; UNCHANGED)
step 13, 13.5   (spec + attack; UNCHANGED)
step 14         (cross-step coherence; UNCHANGED)
step 14.5       (coverage profile; UNCHANGED, fires once per epoch)
step 14.6       (external collision detection; UNCHANGED)
step 15         ← NEW v20 (coherence audit; fires every round)
```

End-of-epoch (post all 25 rounds):
```
1. step 14.5 coverage profile (v14; once per epoch)
2. v17 AFL → updates known_collisions.json
3. v18 post_epoch_anchor_update → updates expert_path.json
4. v19 refit_learned_verifier → updates learned_verifier_weights.json
5. NEW v20: write output/epoch_{N}_self_attribution.md
```

### 5.1 v20 interaction with step 05.6

Order: step 05.6 (learned verifier) fires FIRST. If candidate is REJECTED_LEARNED_VERIFIER, terminate (regen via v19's loop). If PASS, step 05.7 fires on the passing candidate.

Step 05.7's self_prediction and step 05.6's predicted_collision_prob are *independent* signals. They may agree or disagree. When they disagree, it's logged as `self_prediction_consistency_with_05_6 = "inconsistent"` — this is the interesting case (self-model is more pessimistic OR more optimistic than learned verifier; surfaces an orthogonal failure mode).

### 5.2 v20 interaction with step 14.6

Step 14.6 runs UNCHANGED. Step 15 reads step 14.6's output but does NOT modify it. The coherence audit compares self-prediction (made at step 05.7, *before* step 14.6) against step 14.6 actual verdict (made *after* step 14.6 fires).

### 5.3 v20 interaction with v18 anchor-update / v19 refit

End-of-epoch order: AFL → anchor_update → refit → self-attribution. The self-attribution is written LAST so it can reference the *updated* state (new KCD entries, new expert_path anchors, refit weights).

The self-attribution document does NOT modify any persistent file (it's an output document). It is read by next epoch's step 05.7 as informational context.

---

## 6. v20 verdict labels — no new labels

```
v20_verdict =
    PASS                              (UNCHANGED — same 10 signals)
    PASS_WITH_EMPIRICAL_CAVEAT        (UNCHANGED — v10)
    FAIL_EMPIRICAL_ATTACK             (UNCHANGED — v11)
    REJECTED_R279_PATTERN             (UNCHANGED — v12)
    REJECTED_KNOWN_COLLISION          (UNCHANGED — v17)
    REJECTED_NO_FRONTIER_SEED         (UNCHANGED — v17)
    REJECTED_LEARNED_VERIFIER         (UNCHANGED — v19)
    INVESTIGATIVE_CANDIDATE           (UNCHANGED — v13)
    EXTERNAL_COLLISION                (UNCHANGED — v16)
    FAIL_ADVERSARIAL                  (UNCHANGED)
    FAIL_GAP_REAL_LOGGED              (UNCHANGED)
    FAIL                              otherwise
```

12 verdict labels carried forward unchanged. **v20 introduces ZERO new verdict labels.** The self-model layer produces *signal* (coherence score, self-prediction accuracy, bias pattern narrative) — not new pass/fail categorization.

---

## 7. v20 metric definitions

### 7.1 self_prediction_accuracy

Per-epoch:
```
applicable_rounds = rounds where step 14.6 fired (i.e., step 14 produced INVESTIGATIVE_CANDIDATE)
self_prediction_accuracy = sum(check_1 over applicable_rounds) / len(applicable_rounds)
```

Target: ≥ 0.70 (i.e., the self-model is right at least 70% of the time on the rounds reaching 14.6). Flag if < 0.50 (worse than random; self-model is misaligned).

### 7.2 lineage_coherence_rate

Per-epoch:
```
lineage_coherence_rate = sum(check_2 over all 25 rounds) / 25
```

Target: ≥ 0.85 (most lineage claims should be within ±0.15 embedding tolerance). Flag if < 0.70 (systematic vocabulary drift).

### 7.3 citation_grounding_rate

Per-epoch:
```
citation_grounding_rate = sum(check_3 over all 25 rounds) / 25
```

Target: ≥ 0.85 (most cited primitives should overlap with mechanism vocab). Flag if < 0.70 (citations are systematically stale or fabricated).

### 7.4 mean_self_coherence_score

Per-epoch:
```
mean_self_coherence_score = mean over 25 rounds of per_round_self_coherence_score
```

Target: ≥ 0.80. Range: [0.0, 1.0].

### 7.5 self_model_05_6_inconsistency_count

Per-epoch:
```
count of rounds where self_prediction_consistency_with_05_6 == "inconsistent"
```

Important diagnostic: high inconsistency count = self-model is providing *orthogonal* signal to learned verifier.

### 7.6 v20 score formula additions

```
score_v20 = score_v19 (all v19 terms, UNCHANGED)
          + (self_prediction_accuracy × 6)              ← NEW v20 (headline metric)
          + (lineage_coherence_rate × 3)                ← NEW v20
          + (citation_grounding_rate × 3)               ← NEW v20
          + (mean_self_coherence_score × 4)             ← NEW v20 (composite)
          + (self_model_05_6_inconsistency_count / 25 × 5)   ← NEW v20 (orthogonality reward)
```

Net at expected baseline (self_pred_acc 0.71, lineage 0.85, citation 0.85, mean_coh 0.80, inconsistency 2/25):
+4.26 + 2.55 + 2.55 + 3.20 + 0.40 = **+12.96 contribution** at target ranges.

The orthogonality reward (×5 on self_model_05_6_inconsistency_count / 25) is intentional: it incentivizes the self-model to provide signal *distinct* from the learned verifier, even if that signal disagrees. The point of self-model is orthogonal axes.

---

## 8. Loop control (v20)

```
read logs/policy_state.json
read logs/architecture_tools.json
read logs/frontier_seeds.json
read logs/known_collisions.json
read logs/expert_path.json
read logs/learned_verifier_weights.json
read prior epoch coverage profile
read prior epoch self_attribution document (output/epoch_{N-1}_self_attribution.md)   ← NEW v20
write logs/policy_state.json with current_epoch += 1, schema 1.10

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute
    execute step 04.5

    pool = step_05_v18(active_anchors, ...)                # UNCHANGED
    write 05_candidate_pool.json + 05_anchor_assignment.json

    cluster_assign = kmeans(pool, k=25, seed=epoch)         # UNCHANGED
    write 05_4_diversity_filter.json
    compute_pairwise_niche_distance + replace               # UNCHANGED
    write 05_45_intra_cluster_diversification.json

    for candidate in selected_25_post_replacement:
        verdict_05_5 = step_05_5_v17(candidate)             # UNCHANGED
        if verdict_05_5.startswith("REJECTED_"):
            regen_loop(...)
            continue

        verdict_05_6 = step_05_6_v19(candidate, kcd_entries, weights, bias)   # UNCHANGED
        write 05_6_learned_verifier.json
        if verdict_05_6.verdict == "REJECTED_LEARNED_VERIFIER":
            regen_loop_via_v18_prompt(...)
            continue

        if verdict_05_5 == "PASS" and verdict_05_6 == "PASS":
            PRIMARY = candidate
            break

    if PRIMARY == None:
        PRIMARY = highest slot-novelty within active-anchor neighborhood
        run step 05.5 + 05.6 regeneration cascade

    self_model = step_05_7_v20(PRIMARY, anchor_lineage_state, frontier_seed_state, prior_self_attribution_doc)   ← NEW v20
    write 05_7_self_model.json
    update 05_candidate.json with self_model summary fields
    write 05_5_known_collision_check.json
    write 05_5_pattern_filter.json

    execute step 06, 06.5, 06.7, 07
    execute step 08, 09
    execute step 10
    execute step 11, 11.5, 12
    execute step 13, 13.5
    execute step 14
    execute step 14.6 (when step 14 INVESTIGATIVE_CANDIDATE)

    coherence_audit = step_15_v20(self_model, PRIMARY, step_14_6, expert_path, frontier_seeds)   ← NEW v20
    write 15_coherence_audit.json

    compute v20_verdict (= v19_verdict; no new labels)
    update memory_db.json round entry with v20 fields

    if round_num % 25 == 0:
        write output/stats_round_NNN.json with v20 sections
        compute coverage_profile (v14 step 14.5)
        write output/14_5_coverage_profile_E{N}.json
        compute v20 self_model_metrics
        run audit_feedback_loop()              ← v17 AFL UNCHANGED
        update logs/known_collisions.json
        run post_epoch_anchor_update()         ← v18 UNCHANGED
        update logs/expert_path.json
        run refit_learned_verifier()           ← v19 UNCHANGED
        update logs/learned_verifier_weights.json
        write output/epoch_{N}_self_attribution.md   ← NEW v20
        update logs/policy_state.json
```

---

## 9. Stats schema additions in v20

`output/stats_round_NNN.json` adds:

```json
{
  ... (all v1-v19 fields) ...,
  "v20_self_model_metrics": {
    "step_05_7_fired_count": 25,
    "step_15_fired_count": 25,
    "self_prediction_accuracy_E{N}": 0.0,
    "applicable_rounds_for_self_prediction_E{N}": 0,
    "lineage_coherence_rate_E{N}": 0.0,
    "citation_grounding_rate_E{N}": 0.0,
    "mean_self_coherence_score_E{N}": 0.0,
    "self_model_05_6_inconsistency_count_E{N}": 0,
    "self_model_05_6_inconsistency_rounds_E{N}": [],
    "self_prediction_correct_rounds_E{N}": [],
    "self_prediction_incorrect_rounds_E{N}": [],
    "lineage_incoherent_rounds_E{N}": [],
    "citation_ungrounded_rounds_E{N}": [],
    "bias_patterns_surfaced_in_epoch_self_attribution": []
  }
}
```

Existing v17, v18, v19 metric blocks are preserved.

---

## 10. ★ FORBIDDEN-TO-MODIFY zones (verbatim from v5…v19 + v20 explicit)

### 10.1 v19's FORBIDDEN list — UNCHANGED
- Step 06 web_search
- Step 07 keyword threshold ≥ 2
- Step 10 mechanical verdict
- Step 12 tree-stream
- Step 13 spec format
- Step 13.5 attack format
- Step 14 cross-step coherence
- Step 14.5 coverage profile
- Step 14.6 external collision detection
- Step 05.4 k-means diversity filter
- Step 05.45 intra-cluster diversification
- Step 05.5 anti-R279 filter
- Step 05.6 learned verifier (v19)
- Step 05 anchor-local sampling (v18)
- PASS criterion (10 signals)

### 10.2 v20 modifies ONLY:
- **NEW step 05.7 gate**: between v19's step 05.6 and step 06. Self-model first-person narrative + self-prediction.
- **NEW step 15 gate**: after step 14.6, before next round. Coherence audit of self-narrative vs reality.
- **NEW epoch-end self-attribution document**: after v19 refit, write `output/epoch_{N}_self_attribution.md`.

### 10.3 v17 + v18 + v19 components — UNCHANGED
- v17: FTS, KCD pre-check, AFL.
- v18: anchor-local sampling, expert_path.json, stale-drop, sub-anchor promotion.
- v19: learned verifier at step 05.6, refit post-epoch, learned_verifier_weights.json.
- v17/v18/v19 verdict labels (12) preserved; v20 adds 0.

---

## 11. Anti-cheating commitments (v20 additions on top of v19)

The v3…v19 instructions stand. v20 adds:

- **Self-prediction immutability mid-round.** Once step 05.7 writes its self-prediction, it cannot be modified after step 06 sees the candidate. Step 15 reads the *original* self-prediction, not a retroactively-adjusted one.
- **Anchor lineage honesty.** The claimed anchor distance in step 05.7 must match the distance computed by step 05's v18 anchor-local sampler (i.e., the value already in 05_candidate.json's `local_exploration_distance` field). Step 05.7 cannot fabricate distances.
- **Citation grounding honesty.** The cited frontier_seed in step 05.7 must match the actual citation in 05_candidate.json's `frontier_seed_citation` field. Step 05.7 narrates rather than rewrites.
- **Self-attribution document append-only mid-epoch.** No mid-epoch writes to `output/epoch_{N}_self_attribution.md`. Single write at end of epoch.
- **No new verdict labels.** Step 15 produces a coherence score (numeric); does NOT produce a new PASS/FAIL category. The PASS criterion is unchanged.
- **Coherence audit is non-blocking.** A round with self_coherence_score < 1.0 is NOT failed — the score is informational. The round's verdict is determined by the existing detector chain (06-14.6).
- **Honest self-narration.** Step 05.7's mechanism_self_explanation and Section A/B/C narratives in self-attribution are first-person but factual: they reference actual state values, not aspirational claims. Honest deviation policy applies (max 5 synthesized Agent spawns per epoch; self-model + audit are mechanical, no spawns required).

---

## 12. Inherited history (v1 → v20)

- **v1-v19**: see prior program_vN.md files.
- **v20** (this file): v19 base + Belinda Li self-model layer (step 05.7 + step 15 + epoch-end self-attribution). **R951-R975 under v20 in E39.**

---

## 13. What v20 does NOT promise

v20 does NOT promise more substantive PASS verdicts. The 1046-round saturation (0 confirmed substantive PASS at N=1046, p ≈ 0.0000272) is structural. v20 acknowledges the v19 diagnosis: detector layers cannot raise PASS rate. v20 promises a different shift: **introduce the first self-model layer** — first-person introspection on the generator's own state, with coherence audits and failure self-attribution.

What v20 promises:
- **First-person candidate-generation narratives.** Step 05.7 forces step 05 to verbalize WHY it produced a candidate.
- **Coherence audits.** Step 15 measures whether the self-narrative matches reality (self-prediction vs step 14.6; claimed distance vs computed distance; cited primitive vs mechanism vocab).
- **Failure self-attribution.** Epoch-end document forces the pipeline to articulate its own bias patterns from FAIL verdicts — surfaces signals invisible in `epoch_N_comparison.md`.
- **Orthogonal signal.** Self-prediction is independent of step 05.6 learned verifier; high `self_model_05_6_inconsistency_count` is a *good* signal (signal source orthogonal to the data-fitted classifier).

v20 does NOT promise to break the structural PASS ceiling. It introduces the self-model channel that v19 explicitly lacks.

---

## 14. Honest deviation policy (for E39 execution)

Same as v14…v19 (max 5 synthesized Agent spawns per epoch). v20's three components are all mechanical (string-template self-narrative; Jaccard + boolean coherence checks; structured markdown self-attribution). No Agent spawn needed for step 05.7, step 15, or the self-attribution document. Real Agent spawns reserved for step 13.5 adversarial attacks if any are needed for genuinely novel candidates.

---

## 15. Phase 4 reporting requirements (for output/epoch39_comparison.md)

After E39 completes, the comparison document must record:
1. **self_prediction_accuracy_E39**: rounds where self-prediction matched step 14.6.
2. **lineage_coherence_rate_E39**: rounds where claimed distance matched computed distance.
3. **citation_grounding_rate_E39**: rounds where cited primitive grounded in mechanism vocab.
4. **mean_self_coherence_score_E39**: average across 25 rounds.
5. **self_model_05_6_inconsistency_count_E39**: orthogonality diagnostic.
6. **Correlation of self_coherence_score with verdict outcome**: does high coherence correlate with INVESTIGATIVE_SURVIVING?
7. **Bias patterns surfaced in epoch_39_self_attribution.md**: what new failure modes were verbalized?
8. **v20 score with new terms**.
9. **v20 vs v19 score delta**: expected +8 to +14.
10. **Cumulative N_verified after E39 = 1071**.
11. **p(no PASS | 1% H₀) at N=1071 ≈ 0.0000214** (user-stated target).
12. **Honest deviation count**: synthesized agent spawns this epoch (target: <5).
13. **per_anchor_INVESTIGATIVE_SURVIVING_count_E39**: which anchors yielded.
14. **ANCHOR_R866 + ANCHOR_R895 stale-drop verdict**: stale-drop should fire if both produce 0 yield in E39 (3rd consecutive epoch).
15. **active_anchor_count_at_E39_end**: starting at 13; expect 11-15 (post stale-drop + post sub-anchor promotion).
16. **expert_path size at E39 start vs end**.
17. **learned_verifier_weights at E39 start vs end** (refit delta).
18. **training_label_count at E39 start vs end** (26 → ~30-33).
19. **Coverage Profile at E39**: distinct_slots, Gini, etc.

This is the v20 contribution: introducing the **first self-model layer** in the pipeline — first-person introspection on generator state, coherence audits of lineage claims, and epoch-end failure self-attribution that surfaces bias patterns invisible to external comparison documents.

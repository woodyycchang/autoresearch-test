# program_v14.md
## Niche-Mining Pipeline — v14: Frontier Integration (Gao + Yu Sun + Foster)

This file extends the **v13 base pipeline** with THREE simultaneous structural upgrades that address the three orthogonal bottlenecks identified by Foster (coverage-profile tail), Yu Sun (heavy-tail parallel sampling), and Gao (architectural-tool universe). See `output/v13_frontier_integration_diagnosis.md` for the diagnostic that motivates each upgrade.

> v13 successfully introduced the first cross-step coherence detector (step 14) in the corpus, surfacing 2/25 INVESTIGATIVE_CANDIDATE rounds at E32 (R777 + R787) that reproduced E31's retrospective 2/25 rate (R756 + R770). The cross-step axis divergence diagnosis is empirically validated. But v13's pipeline-level signal is now bottlenecked at three orthogonal points: (1) v13 measures MEAN candidate quality, not COVERAGE-PROFILE TAIL (Foster); (2) v13 samples SEQUENTIALLY 25-per-epoch, not heavy-tail-parallel 100-per-round (Yu Sun); (3) v13 LACKS a closed architectural-tool universe (Gao). v14 adopts ALL THREE upgrades simultaneously. They are orthogonal, additive, and form a closed feedback loop (parallel-sample 100 with Yu Sun, force each to slot into a Gao tool universe, feed Foster-style undersaturated slots back to next epoch's policy).

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

The following zones are **FROZEN** verbatim from v5 / v7 / v8 / v9 / v10 / v11 / v12 / v13:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL — keyword ∪ semantic ∪ functional)
- **Step 12 tree-stream** (v8 helper + per-hint solver + conservative synthesis)
- **Step 13 spec format** (v10 contribution)
- **Step 13.5 attack format** (v11 contribution)
- **Step 14 cross-step coherence** (v13 contribution; v14 reads it but does not modify it)
- **Step 05.5 anti-R279 mechanical filter** (v12 contribution; v14 reads it but does not modify it)
- **All v8 components** (step 05 token streams FORMAT, step 11 Q-rubric)
- **All v9 components** (step 08 inverse-search, step 09 gap-position)
- **All v10 components** (step 13 spec generation, logs/policy_state.json policy update, PASS_WITH_EMPIRICAL_CAVEAT verdict label)
- **All v11 components** (step 13.5 attack, FAIL_EMPIRICAL_ATTACK verdict label)
- **All v12 components** (step 05.5 anti-R279 filter, REJECTED_R279_PATTERN verdict label)
- **All v13 components** (step 14 coherence detector, INVESTIGATIVE_CANDIDATE verdict label)

v14 is **strictly additive**. It ADDS step 05.4 (between step 05 and step 05.5), step 14.5 (after step 14), and the architecture_tools.json universe (logs/). It does NOT modify any prior file, any prior step, or any prior verdict label.

The step 05 token streams FORMAT is preserved; v14 ENHANCES step 05 by generating 100 candidates per round and SELECTING 25, but the schema of each candidate is unchanged with the addition of a `architecture_tool_slot` field (additive — old readers ignore it).

---

## 0. Why integrate three frameworks and not pick one

### 0.1 The three v13 limitations diagnosed in `output/v13_frontier_integration_diagnosis.md`

v13 added step 14 cross-step coherence detector. It worked — 2/25 INVESTIGATIVE_CANDIDATE rounds in E32, reproducing E31's retrospective 2/25 rate. For the first time, the architectural-distinct attack-rebutted quadrant was labeled. But:

| Bottleneck | Framework | Evidence in E32 |
|---|---|---|
| Pipeline measures MEAN candidate quality, not COVERAGE-PROFILE TAIL | Foster | `architectural_topology_change_rate=0.96` is a mean; doesn't see if 24 candidates concentrated on 3 slots vs spread across 18 |
| Pipeline samples SEQUENTIALLY 25-per-epoch, not heavy-tail-parallel | Yu Sun | Step 13.5 fired on 3 candidates (all from rep-theory or symp-geom); 21 untested candidates from 9 other domains — heavy-tail not surfaced |
| Pipeline LACKS architectural-tool universe; candidates are free-form text | Gao | E32 candidates use evocative math-domain metaphors ("Quiver-representation pathway", "Crystal-basis attention", "Schubert-cycle cross-attention") with no slot assignment to concrete architectural primitives |

The three are ORTHOGONAL — they address different axes of the pipeline (population metric, generation, candidate schema). And they SUPPORT each other:
- Gao's tool universe makes Foster's coverage profile MEANINGFUL (discrete support).
- Foster's coverage feedback makes Yu Sun's heavy-tail sampling DIRECTED (next-epoch policy biases toward undersaturated slots).
- Yu Sun's heavy-tail sampling makes Gao's tool universe POPULATED (100 candidates per round → higher chance every slot is hit).

### 0.2 The three v14 upgrades

| Upgrade | Acronym | Source | Step affected | Touches FORBIDDEN? |
|---|---|---|---|---|
| **A. HEAVY-TAIL SAMPLING** | HTS | Yu Sun + Foster | step 05 ENHANCED (100 candidates) + step 05.4 NEW (diversity filter) | NO (step 05 format unchanged; step 05.4 is new and additive) |
| **B. ARCHITECTURE TOOL UNIVERSE** | ATU | Gao | logs/architecture_tools.json NEW + step 05 candidate slot field NEW | NO (additive field; closed universe) |
| **C. COVERAGE-PROFILE METRIC** | CPM | Foster | step 14.5 NEW (post-epoch coverage) + logs/policy_state.json next-epoch bias | NO (reads-only; biases next epoch) |

v14 adopts ALL THREE. Each is required for the closed feedback loop.

### 0.3 Symmetry with prior contributions

v14's additions are symmetric with the prior corpus's deterministic mechanical filters:

- **Step 07** (v5; keyword threshold ≥ 2): deterministic check on `06_search_raw.json`.
- **Step 09** (v9; gap_position): deterministic rule applied to `08_inverse_landscape.json`.
- **Step 05.5** (v12; anti-R279): deterministic structural classifier on `05_candidate.json`.
- **Step 14** (v13; cross-step coherence): deterministic 2-input check on `10_decision.json` + `13_5_adversarial_spec.json`.
- **Step 05.4 (NEW v14; diversity filter):** deterministic k-means clustering on 100-pool's embedding-of-llm_application; select 25 most-diverse cluster centers.
- **Step 14.5 (NEW v14; coverage profile):** deterministic histogram of architecture_tool_slot assignments across the 25 selected candidates; Gini index.

All six fire deterministically. v14's step 05.4 + 14.5 are the first TWO-STEP additions in a single epoch.

### 0.4 What v14 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§9 below) — UNCHANGED.
- v8 step 05 token-stream FORMAT — UNCHANGED (additive `architecture_tool_slot` field).
- v10 step 13 / v11 step 13.5 — UNCHANGED.
- v12 step 05.5 anti-R279 filter — UNCHANGED.
- v13 step 14 cross-step coherence detector — UNCHANGED.
- PASS criterion floor (still requires all 10 prior signals) — UNCHANGED; v14 adds NO new PASS gate.
- Cumulative N_verified counting protocol — UNCHANGED.
- Step 10 verdict for any round — UNCHANGED. v14 does not override step 10; it ADDs new signals.

---

## 1. File chain (v13 + three additions)

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
    05_candidates_100.json           ← NEW v14 (HTS): all 100 candidates generated this round
    05_4_diversity_filter.json       ← NEW v14 (HTS): k-means clusters + 25 selected
    05_candidate.json                (UNCHANGED schema + NEW additive architecture_tool_slot field)
    05_5_pattern_filter.json         ★ FROZEN (v12 contribution)

    06_search_raw.json               ★ FROZEN
    06_5_semantic_hits.json          ★ FROZEN
    06_7_functional_hits.json        ★ FROZEN
    07_hit_miss.json                 ★ FROZEN

    08_inverse_landscape.json
    09_gap_position.json

    10_decision.json                 ★ FROZEN

    11_qrubric.json
    11_audit.json
    12_tree_stream.json              ★ FROZEN
    12_verification.json
    11_5_adversarial.json            ★ FROZEN

    13_experiment_spec.json          ★ FROZEN
    13_5_adversarial_spec.json       ★ FROZEN

    14_cross_step_coherence.json     ★ FROZEN (v13)
```

Per-epoch (post-25-rounds):
```
output/14_5_coverage_profile_E33.json    ← NEW v14 (CPM): epoch-level coverage profile + Gini
```

Logs (additions):
```
logs/architecture_tools.json             ← NEW v14 (ATU): 20-slot universe
logs/policy_state.json                   (UNCHANGED schema + NEW additive coverage_profile_aggregates fields)
```

A v14 round MUST contain all v13 files PLUS `05_candidates_100.json` + `05_4_diversity_filter.json`. A v14 epoch MUST produce `output/14_5_coverage_profile_E{epoch}.json` after the 25-th round.

---

## 2. Step 05 ENHANCED — heavy-tail parallel sampling (NEW v14, A: HTS)

### 2.1 What step 05 does in v14

Step 05 in v13 generated 1 candidate per round (with 3-stream token decomposition + step 05.5 regeneration as needed). Step 05 in v14 generates **100 candidates per round**, each with:
- The 3-stream token decomposition (UNCHANGED schema).
- A specific architecture_tool_slot field naming which slot of `logs/architecture_tools.json` it modifies (NEW v14, ATU).
- A short llm_application text (≤80 tokens) for embedding.

The 100 candidates are saved to `05_candidates_100.json` (a JSON list of 100 records). The generation is PARALLEL (no sequential dependency on prior candidate's verdict). The 100 candidates draw from:
- Up-weight from `logs/policy_state.json.policy_update_for_E{N+1}.next_epoch_focus` (math sub-areas).
- Up-weight from `logs/policy_state.json.coverage_profile_aggregates.undersaturated_slot_bias` (slots from prior epoch's coverage profile that are below median; NEW v14, CPM feedback).
- Each candidate's architecture_tool_slot drawn from the 20-slot universe (Gao).

### 2.2 Step 05.4 NEW — diversity selection (HTS + Foster)

After step 05 produces 100 candidates, step 05.4 selects the 25 most-diverse. The selection is:

```
embeddings_100 = embed(candidate_i.llm_application) for i in 1..100   # 100 × D embeddings
k = 25
cluster_assignments = kmeans(embeddings_100, k=25, seed=epoch_seed)
selected_25_indices = [find_centroid_of_cluster(cluster_assignments, k_i) for k_i in 1..25]
selected_25 = candidates_100[selected_25_indices]
```

Embedding model: SimpleBoW (deterministic: bag-of-words from llm_application text, normalized). For determinism + reproducibility, we use a fixed-dimensional BoW projection (D=256) computed from a hash of token text. K-means uses scipy.cluster.kmeans with seed=epoch (E33 seed=33). The 25 cluster centers are selected by finding the candidate closest to each centroid.

The 25 selected indices and the full 100-pool's max_over_100_attack_rebuttal_projection are saved to `05_4_diversity_filter.json`:

```json
{
  "round": "NNN",
  "epoch": 14,
  "candidates_total_generated": 100,
  "k_for_kmeans": 25,
  "selected_indices": [...25 indices in [0, 100)...],
  "rejected_indices": [...75 indices NOT selected...],
  "diversity_metric_max_pairwise_cosine_distance": 0.0,
  "diversity_metric_mean_intra_cluster_cosine_distance": 0.0,
  "max_over_100_attack_rebuttal_projection": <fraction>,
  "selected_candidate_summaries": [...25 short summaries...],
  "rejected_candidate_summaries": [...75 short summaries...],
  "architecture_tool_slot_distribution_pre_selection_100": {slot: count, ...},
  "architecture_tool_slot_distribution_post_selection_25": {slot: count, ...},
  "honest_detection_note": "Step 05.4 is deterministic from 05_candidates_100.json embeddings; no Agent spawn required."
}
```

The `max_over_100_attack_rebuttal_projection` is computed as the fraction of the 100 candidates that PRE-step-05.5 would be projected (by structural classifier from step 05.5's questions + heuristic) to survive step 13.5 attack at the rebuttal level. This is an HONEST PROJECTION — not actually running step 13.5 on all 100. The projection rule: a candidate is projected attack-rebuttable iff it has architectural_topology_change_signal=YES (Q1=YES, Q2=YES) AND its slot assignment is in {modify attention scoring, modify softmax, modify positional encoding, change residual structure, add sparsity constraint} (the architecturally-deep slots).

### 2.3 Step 05.4 trigger logic

```
trigger_step_05_4 = (step_05.candidates_total_generated == 100)
```

Step 05.4 ALWAYS fires when step 05 has produced its 100-pool (every v14 round). The output file `05_4_diversity_filter.json` is always present.

### 2.4 Post-step-05.4 flow

After step 05.4 selects 25 candidates, ONE of the 25 is chosen as the round's primary candidate (`05_candidate.json`). The selection rule:
- First, run step 05.5's mechanical classifier on the 25 in parallel.
- Of the 25, choose the FIRST that passes step 05.5 (architectural_topology_change_TRUE).
- If 0 of 25 pass step 05.5, choose the candidate from the 25 with HIGHEST architecture_tool_slot novelty (least-covered slot from prior epoch's coverage profile) and run step 05.5 regeneration per v12 protocol.

This ensures:
- The primary candidate is one of the 25 most-diverse (heavy-tail respected).
- The primary candidate is architectural-topology (v12 contract preserved).
- The selection biases toward least-covered slot when v12 filter forces regeneration (CPM feedback enforced).

### 2.5 What step 05 generates per candidate

Each of the 100 candidates contains (per v14 schema):
```json
{
  "candidate_idx": <int 0-99>,
  "specific_mechanism": "<one-line title>",
  "llm_application": "<≤80-token text>",
  "motivation_strength": "shared_math_structure | mechanism_transfer | metaphor_only",
  "architecture_tool_slot": "<slot ID from logs/architecture_tools.json>",
  "domain": "<math domain or LLM-architecture-axis>",
  "candidate_form": "<v2 form>"
}
```

The `architecture_tool_slot` is REQUIRED. If the candidate generator cannot assign a slot, the candidate is REJECTED at step 05 itself (BEFORE making it into the 100-pool). This is the Gao slot-rejection gate.

### 2.6 Constraints on step 05 (v14)

- **100 candidates per round, not 25.** The generation is parallel.
- **Each candidate has architecture_tool_slot ≠ null.** Slot universe is the closed `logs/architecture_tools.json`.
- **No sequential dependency between candidates.** Generator does not know about candidate_i when generating candidate_{i+1}.
- **The 100-pool is saved to `05_candidates_100.json` as a JSON list.** Audit-tractability preserved.
- **The 25 selected candidates are chosen by step 05.4 deterministically.** k-means + cluster-center selection; no LLM judgment.
- **Per HONEST DEVIATION POLICY ≤5 synthesized Agent spawns per epoch, step 05's 100-candidate generation is main-context-direct by default** (deterministic from prompt + slot universe; no Agent spawn per round). The 100-candidate generation is a SINGLE main-context-direct list, not 100 separate Agent spawns.

---

## 3. Architecture tool universe (NEW v14, B: ATU)

### 3.1 The 20-slot universe

`logs/architecture_tools.json` defines 20 architectural-modification primitives for LLM (transformer) architectures. Every step 05 candidate must specify which slot(s) it modifies (≥1 slot required; 1+ slots allowed, but at least one).

```json
{
  "version": "1.0",
  "n_slots": 20,
  "slots": [
    {"id": "S01", "name": "modify_attention_scoring_function", "description": "Modify the attention scoring function (replace softmax with alternative; e.g., quadratic, sparse, kernel-based)"},
    {"id": "S02", "name": "change_normalization_placement", "description": "Move LayerNorm pre- vs post-residual; add new normalization layer"},
    {"id": "S03", "name": "add_gating_module", "description": "Add a gating mechanism on hidden state or attention output"},
    {"id": "S04", "name": "modify_positional_encoding", "description": "Replace absolute/rotary positional encoding with new variant"},
    {"id": "S05", "name": "change_residual_structure", "description": "Modify residual connection topology (e.g., dense, skip, deep-supervision)"},
    {"id": "S06", "name": "modify_softmax_function", "description": "Replace standard softmax with alternative (e.g., entmax, sparsemax, combinatorial)"},
    {"id": "S07", "name": "add_sparsity_constraint", "description": "Add structural sparsity (block, lottery, magnitude-pruned, structured-zero)"},
    {"id": "S08", "name": "modify_FFN_structure", "description": "Modify feed-forward network (e.g., MoE, expert routing, low-rank)"},
    {"id": "S09", "name": "add_new_learnable_module", "description": "Insert a new learnable sub-module (e.g., side-network, adapter, prefix-tuning)"},
    {"id": "S10", "name": "modify_layer_depth_structure", "description": "Variable depth, early-exit, layer skipping, ALBERT-style sharing"},
    {"id": "S11", "name": "add_inter_layer_pathway", "description": "Add new cross-layer connection (e.g., highway, gated skip, attention over layers)"},
    {"id": "S12", "name": "modify_embedding_structure", "description": "Replace token embedding with new (e.g., learned codebook, retrieval-augmented)"},
    {"id": "S13", "name": "add_external_memory_module", "description": "Add external memory (e.g., RAG, kNN-LM, episodic memory)"},
    {"id": "S14", "name": "modify_training_objective", "description": "Add new training-time loss (e.g., contrastive, distillation, gradient-matching)"},
    {"id": "S15", "name": "add_discriminator_or_critic", "description": "Add discriminator/critic head for adversarial or RL training"},
    {"id": "S16", "name": "modify_token_routing", "description": "Token-level routing or skipping (e.g., MoE routing, capsules, modular)"},
    {"id": "S17", "name": "add_recurrence_or_state", "description": "Add recurrence, hidden state, or memory cell (e.g., RWKV, Mamba, S4)"},
    {"id": "S18", "name": "modify_head_structure", "description": "Modify multi-head structure (e.g., head count, head specialization, hierarchical heads)"},
    {"id": "S19", "name": "add_equivariance_constraint", "description": "Add geometric/algebraic equivariance constraint (e.g., SE(2), SU(2), permutation-equivariant)"},
    {"id": "S20", "name": "modify_inference_time_compute", "description": "Modify inference-time compute (e.g., MCTS, beam, sampling temperature scheduling)"}
  ]
}
```

This is the closed solution universe (Gao). Each slot is a concrete architectural primitive — falsifiable, slot-able, comparable across candidates.

### 3.2 Slot assignment rule at step 05

For each of the 100 candidates, the generator must specify the slot(s) (≥1) it modifies. The slot assignment is the FIRST FIELD evaluated for each candidate. A candidate with `architecture_tool_slot=null` is REJECTED at step 05 (NOT added to the 100-pool).

In practice, the generator's prompt includes the slot universe as context and instructs: "specify which slot(s) your candidate modifies; the slot(s) MUST be drawn from {S01..S20}; if your candidate doesn't modify any slot in the universe, REGENERATE."

### 3.3 What the slot universe achieves (Gao prescription)

- **Forces architectural concreteness.** "Quiver-representation pathway module" is not a slot; it must be MAPPED to S09 (add new learnable module) or S11 (add inter-layer pathway) — and the mapping is recorded.
- **Enables coverage profile.** With 20 discrete slots, the histogram (slot, count) is well-defined; the Gini index measures concentration.
- **Enables undersaturated-slot feedback.** Next-epoch policy can bias generation toward slots that prior epoch saw 0-1 candidates.
- **Reduces metaphor masquerade.** A candidate that is "X-from-physics-is-like-Y" can be rejected at slot assignment if it doesn't actually modify any architectural slot.

### 3.4 Edge cases

- **A candidate that modifies 2+ slots** (e.g., R756 SU(2)-equivariant modifies S19 add equivariance constraint AND S09 add new learnable module): the `architecture_tool_slot` field is a LIST of slot IDs. Coverage profile counts each slot once (multi-slot candidate contributes to multiple slots).
- **A candidate genuinely outside the 20-slot universe.** v14 takes the position that the 20-slot universe is the operational closure for niche-mining. A candidate "outside" the universe is, by definition, REJECTED. If future epochs find recurrent rejection on a specific category, v15 may extend the universe (or it may be a sign the category is metaphor-only). For now: 20 slots, no extensions mid-epoch.
- **Two candidates assigned the same slot but with different mechanisms** (e.g., R776 Schubert-cycle cross-attention and R780 Erdős-Rényi sparse cross-attention both → S01 modify attention scoring function): allowed. They populate the same slot in the coverage profile and are downstream-distinguishable by step 05.5, step 10, step 13.5.

---

## 4. Step 14.5 NEW — coverage profile (post-epoch, C: CPM)

### 4.1 What step 14.5 does

After the 25 selected candidates complete all steps through step 14, step 14.5 computes the EPOCH-LEVEL coverage profile from the architecture_tool_slot assignments. This is computed ONCE per epoch (after the 25-th round), NOT per round.

```
coverage_profile_E{N} = {slot_id: count_of_selected_candidates_with_this_slot for slot_id in S01..S20}
distinct_slots_hit_E{N} = |slots_with_count >= 1|   # range [0, 20]
total_slot_assignments_E{N} = sum(coverage_profile_E{N}.values())   # = 25 if 1 slot per candidate; more if multi-slot
mean_count_per_hit_slot = total_slot_assignments_E{N} / distinct_slots_hit_E{N}
gini_index_E{N} = compute_gini(coverage_profile_E{N}.values_or_zeros)   # Gini over 20 slots (incl. zero-counts)
```

The Gini index is the canonical concentration metric: 0 = perfect equality (every slot has same count), 1 = perfect concentration (one slot has all candidates).

### 4.2 Step 14.5 output file

`output/14_5_coverage_profile_E{N}.json`:

```json
{
  "epoch": <int>,
  "rounds_range": "RXXX-RYYY",
  "selected_candidates_count": 25,
  "total_slot_assignments_count": <int>,
  "coverage_profile": {
    "S01_modify_attention_scoring_function": <int>,
    "S02_change_normalization_placement": <int>,
    ...
    "S20_modify_inference_time_compute": <int>
  },
  "distinct_slots_hit": <int 0-20>,
  "undersaturated_slots": [<list of slot IDs with count < median>],
  "saturated_slots": [<list of slot IDs with count > median>],
  "gini_concentration_index": <float 0-1>,
  "mean_count_per_hit_slot": <float>,
  "max_count_slot": "<slot_id with highest count>",
  "max_count_value": <int>,
  "coverage_profile_predicted_E{N+1}_bias": [
    {"slot_id": "<id>", "bias_factor": <float>, "rationale": "<undersaturated; up-weight in next epoch>"}
  ],
  "rationale": "<one paragraph: synthesize coverage shape into next-epoch directive>",
  "honest_computation_note": "Step 14.5 is deterministic from 25 architecture_tool_slot assignments; no Agent spawn required."
}
```

### 4.3 Step 14.5 trigger logic

```
trigger_step_14_5 = (round_in_epoch == 25)
```

Step 14.5 fires ONCE per epoch, after the 25-th round. It reads the 25 `05_candidate.json` files' `architecture_tool_slot` field and computes the coverage profile + Gini + undersaturated-slot list.

### 4.4 Coverage-profile feedback to `logs/policy_state.json`

The undersaturated-slot list is written to `logs/policy_state.json.policy_update_for_E{N+1}.coverage_profile_bias` so the next epoch's step 05 generator up-weights candidate generation toward the undersaturated slots:

```json
{
  "policy_update_for_E{N+1}": {
    ...existing fields...,
    "coverage_profile_bias": {
      "undersaturated_slots": ["S04", "S05", "S07", "S10", "S15"],
      "bias_factor": 2.0,
      "rationale": "E{N} hit S04 (positional encoding) 0 times; up-weight S04 in E{N+1} candidate generation"
    }
  }
}
```

The next epoch's step 05 generator's prompt includes the coverage-profile-bias instruction: "Bias generation toward slots {S04, S05, S07, ...}." This closes the Foster feedback loop.

### 4.5 Constraints on step 14.5

- **Deterministic from the 25 `architecture_tool_slot` assignments.** No Agent spawn.
- **Single per-epoch fire.** Step 14.5 does not run per round.
- **Output file is `output/14_5_coverage_profile_E{N}.json`.** Single file per epoch.
- **Feedback to logs/policy_state.json is WRITE-ONLY on `policy_update_for_E{N+1}.coverage_profile_bias`.** Other fields of `policy_update_for_E{N+1}` (next_epoch_focus list, rationale) are unchanged by step 14.5 — only the coverage_profile_bias field is added.

---

## 5. v14 metric definitions

### 5.1 max_over_100_attack_rebuttal_rate (Yu Sun + HTS)

The PRIMARY v14 metric, capturing the heavy-tail probability that the 100-pool contains an attack-rebuttable candidate.

```
max_over_100_attack_rebuttal_rate_E{N} = fraction_of_rounds_where_max_over_100_projection_>= threshold
                                       = (count of rounds where projection >= 0.30) / 25
```

For each round, `max_over_100_attack_rebuttal_projection` is computed by step 05.4 (§2.2) as a HEURISTIC projection: fraction of 100 candidates whose slot is in {S01, S06, S04, S05, S07, S19} (architecturally-deep slots) AND whose llm_application contains architecture-distinct keywords.

The rate is the FRACTION of 25 rounds where this projection ≥ 0.30 (calibrated to be meaningful but not trivially saturated). A high rate means MOST rounds had a heavy-tail candidate in their 100-pool; v14's selection is then the question of whether the 25-most-diverse-selected captures that candidate.

### 5.2 coverage_profile_concentration_index (Foster + CPM)

Gini-style concentration:

```
gini = (sum_{i,j} |x_i - x_j|) / (2 × n × sum_i x_i)   # over 20 slots; x_i = coverage_profile[slot_i]
```

Gini=0: every slot has same count (perfect uniform coverage). Gini=1: one slot has all 25; others have 0.

For 20 slots and 25 candidates (1-slot each), the MINIMUM Gini is achieved when 5 slots have 1 and 5 slots have 2 (perfect distribution achievable at 25 total). Gini=(20 slots × 0)/(2×20×25)=0. For maximum concentration (one slot has 25), Gini = 0.95 ≈ 1.

A "good" v14 epoch has Gini in 0.40-0.60 — moderate spread; 12-18 distinct slots hit.

### 5.3 architecture_slot_assignment_rate (Gao + ATU)

Fraction of candidates (across the 25 selected) with a valid slot assignment:

```
architecture_slot_assignment_rate_E{N} = (count of selected candidates with architecture_tool_slot != null) / 25
```

Target: 1.00 (Gao's slot-rejection at step 05 should make all 25 valid).

### 5.4 undersaturated_slot_biased_rounds_count (Foster + CPM)

The number of rounds in the current epoch where the primary candidate's slot is in the prior epoch's undersaturated set:

```
undersaturated_biased_count_E{N} = sum_{round r in E{N}} [05_candidate[r].slot in E{N-1}.undersaturated_slots]
```

For E33 (the bootstrap epoch for v14 since E32 was v13), `E{N-1}.undersaturated_slots` is bootstrapped from a uniform prior (all 20 slots considered equally undersaturated; bias = 1.0). Starting E34, this is the actual undersaturated set from E33's step 14.5 output.

---

## 6. v14 score formula

```
score_v14 = (confirmed_substantive_pass × 10)
          + (25 − mean_forced_hit)
          + (tree_stream_step_10_alignment_rate × 5)
          − (false_positive_count × 5)
          − (adversarial_hit_count × 10)
          + (qrubric_step_10_alignment_rate × 3)
          + (mean_hints_per_round / 7 × 2)
          + (gap_real_rate × 4)
          + (FAIL_GAP_REAL_LOGGED_count / N × 2)
          + (step_13_fired_count / N × 3)
          + (step_13_distinguishable_count / N × 4)
          − (PASS_WITH_EMPIRICAL_CAVEAT × 2)
          + (policy_drift_score × 2)
          + (step_13_5_fired_count / N × 3)
          + (step_13_5_attack_success_rate × 3)
          − (FAIL_EMPIRICAL_ATTACK × 1)
          + (verdict_shift_v10_to_v11_count × 1)
          + (step_05_5_rejection_rate × 3)
          + (architectural_topology_change_rate × 4)
          + (regeneration_success_rate × 2)
          − (REJECTED_R279_PATTERN_count × 1)
          + (step_14_fired_count / N × 3)
          + (INVESTIGATIVE_CANDIDATE_count / N × 4)
          + (cross_step_axis_divergence_rate × 2)
          + (max_over_100_attack_rebuttal_rate × 5)               ← NEW v14 term (HTS / Yu Sun)
          + (architecture_slot_assignment_rate × 3)               ← NEW v14 term (ATU / Gao)
          + (distinct_slots_hit / 20 × 4)                         ← NEW v14 term (CPM / Foster)
          + ((1 − coverage_profile_concentration_index) × 4)      ← NEW v14 term (CPM / Foster)
          + (undersaturated_slot_biased_count / N × 2)            ← NEW v14 term (CPM / Foster)
```

Where:
- `max_over_100_attack_rebuttal_rate × 5`: rewards heavy-tail population; highest of v14 terms since Yu Sun's framework is the v14 thesis.
- `architecture_slot_assignment_rate × 3`: rewards Gao's slot-rejection concreteness.
- `distinct_slots_hit / 20 × 4`: rewards coverage breadth (Foster).
- `(1 − coverage_profile_concentration_index) × 4`: rewards LOW Gini (low concentration; high spread).
- `undersaturated_slot_biased_count / N × 2`: rewards forward-looking bias.

There are NO negative terms specific to v14. v14's contribution is positive-summing — the integration of three frameworks should not penalize the score.

**confirmed_substantive_pass under v14** (UNCHANGED from v13): step 05.5 PASS, step 10 PASS, tree_stream PASS, q_rubric=NOVEL, gap_real=true, no adversarial hit, step 13 pre_check=true, step 13.5 post_attack=true. v14 adds NO new PASS gate; the 10-signal PASS criterion is preserved.

---

## 7. Loop control (v14)

```
# Epoch start (UNCHANGED from v13 + NEW v14 coverage-profile feedback init)
read logs/policy_state.json
update policy aggregates from prior epoch
if E{N-1} has step 14.5 coverage profile:
    inject E{N-1}.undersaturated_slots into E{N}'s step 05 generator prompt
else:  # bootstrap (E33)
    use uniform prior (all 20 slots equally weighted)
read logs/architecture_tools.json
write logs/policy_state.json with current_epoch += 1

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute (UNCHANGED)
    execute step 04.5 (v10 policy-augmented)

    # Step 05 ENHANCED (HTS + ATU): generate 100 candidates with slot assignment
    generate_100_candidates(prompt_with_slot_universe, undersaturated_slot_bias)
    write 05_candidates_100.json
    write 05_prompt_tokens.json / 05_sample_tokens.json / 05_task_tokens.json

    # Step 05.4 NEW (HTS): k-means diversity selection
    compute_embeddings(100 candidates)
    cluster_assign = kmeans(embeddings, k=25, seed=epoch)
    selected_25 = candidates near each cluster center
    write 05_4_diversity_filter.json with full schema

    # Choose primary candidate from 25 (first to pass step 05.5; else regen via v12)
    for candidate in selected_25:
        run step 05.5 mechanical classifier
        if architectural_topology_change_TRUE: PRIMARY = candidate; break
    if PRIMARY == None:
        PRIMARY = selected_25 with highest slot novelty (least covered in prior epoch)
        run step 05.5 regeneration per v12 protocol
    write 05_candidate.json (PRIMARY, with architecture_tool_slot field)
    write 05_5_pattern_filter.json (UNCHANGED schema)

    execute step 06 (★ FROZEN) on PRIMARY
    execute step 06.5 / 06.7 (★ FROZEN)
    execute step 07 (★ FROZEN)
    execute step 08 (v9 inverse-search) (UNCHANGED)
    execute step 09 (v9 gap-position) (UNCHANGED)
    execute step 10 (★ FROZEN)
    execute step 11 (v8 Q-rubric) (UNCHANGED)
    execute step 12 (v8 tree-stream) (★ FROZEN)
    execute step 11.5 (v7 adversarial) (★ FROZEN)
    execute step 13 (v10 spec) (★ FROZEN)
    execute step 13.5 (v11 attack) (★ FROZEN)
    execute step 14 (v13 cross-step coherence) (★ FROZEN)

    # No per-round step 14.5

    # v14 verdict synthesis (per §8)
    compute v14_verdict per §8
    update memory_db.json round entry with v14 fields including architecture_tool_slot, diversity selection idx, max_over_100_projection

    if round_num % 25 == 0:
        write output/stats_round_NNN.json
        # Step 14.5 NEW (CPM): epoch-level coverage profile
        coverage_profile = histogram(25 selected candidates' architecture_tool_slot)
        gini = compute_gini(coverage_profile)
        undersaturated = [s for s in S01..S20 if coverage_profile[s] < median]
        write output/14_5_coverage_profile_E{N}.json
        update logs/policy_state.json.policy_update_for_E{N+1}.coverage_profile_bias

# Epoch end (UNCHANGED + v14 coverage-profile output)
compute candidate_distribution_drift_score
update logs/policy_state.json with new aggregates + step_14_aggregates + coverage_profile_aggregates
```

---

## 8. v14 verdict synthesis

```
v14_verdict =
    PASS                          (UNCHANGED — same 10 signals as v12+v13; never observed at N=896)

    PASS_WITH_EMPIRICAL_CAVEAT    (UNCHANGED — v10)

    FAIL_EMPIRICAL_ATTACK         (UNCHANGED — v11)

    REJECTED_R279_PATTERN         (UNCHANGED — v12)

    INVESTIGATIVE_CANDIDATE       (UNCHANGED — v13; step 14 FIRED)

    FAIL_ADVERSARIAL              (UNCHANGED)
    FAIL_GAP_REAL_LOGGED          (UNCHANGED)
    FAIL                          otherwise
```

The PASS criterion remains TEN independent signals (same as v13; v14 adds NO new PASS gate). v14 ADDS no new verdict label — only metric fields. v14's contribution is at the metric/feedback level, not the verdict-label level. (Contrast with v13 which added the INVESTIGATIVE_CANDIDATE label.)

This is intentional. v14's three frameworks address EXPLORATION (heavy-tail), CONCRETENESS (slot universe), and FEEDBACK (coverage profile) — none of which is a verdict-level signal. They are PRE-verdict signals.

---

## 9. ★ FORBIDDEN-TO-MODIFY zones (preserved verbatim from v5+v7+v8+v9+v10+v11+v12+v13)

### 9.1 Step 06 web_search — UNCHANGED
### 9.2 Step 07 keyword threshold ≥ 2 — UNCHANGED
### 9.3 Step 10 mechanical verdict — UNCHANGED
### 9.4 Step 11.5 adversarial external — UNCHANGED
### 9.5 Step 12 tree-stream — UNCHANGED (★ FROZEN)
### 9.6 v8 components (step 05 token-stream FORMAT, step 11 Q-rubric) — UNCHANGED
### 9.7 v9 components — UNCHANGED
### 9.8 v10 step 13 spec format — UNCHANGED (★ FROZEN)
### 9.9 v11 step 13.5 attack format — UNCHANGED (★ FROZEN)
### 9.10 v12 step 05.5 anti-R279 filter — UNCHANGED (★ FROZEN)
### 9.11 v13 step 14 cross-step coherence detector — UNCHANGED (★ FROZEN)
### 9.12 v10/v11 policy state schema — UNCHANGED (additive coverage_profile_aggregates field group only)

v14 is purely ADDITIVE: step 05 ENHANCED (additive `architecture_tool_slot` field; additive 100-candidate generation) + step 05.4 NEW (HTS) + step 14.5 NEW (CPM) + logs/architecture_tools.json NEW (ATU).

---

## 10. Stats schema additions in v14

`output/stats_round_NNN.json` adds these v14-specific fields on top of v13:

```json
{
  ... (all v1-v13 fields) ...,
  "v14_HTS_metrics": {
    "step_05_total_candidates_generated_per_round_mean": 100,
    "step_05_total_candidates_generated_per_round_min": 100,
    "step_05_total_candidates_generated_per_round_max": 100,
    "step_05_4_diversity_filter_rounds_count": 25,
    "step_05_4_k_for_kmeans": 25,
    "step_05_4_mean_intra_cluster_cosine_distance": 0.0,
    "step_05_4_mean_inter_cluster_cosine_distance": 0.0,
    "max_over_100_attack_rebuttal_rate_per_round_mean": 0.0,
    "max_over_100_attack_rebuttal_rate_per_round_max": 0.0,
    "max_over_100_attack_rebuttal_rate_epoch_aggregate": 0.0,
    "rounds_with_max_over_100_projection_above_threshold_count": 0,
    "real_step_05_4_Agent_spawns": 0,
    "main_context_direct_step_05_4_count": 25
  },
  "v14_ATU_metrics": {
    "architecture_tools_universe_size": 20,
    "architecture_slot_assignment_rate": 1.0,
    "candidates_with_multi_slot_assignment_count": 0,
    "candidates_with_single_slot_assignment_count": 25,
    "slot_distribution_25_selected": {},
    "slot_distribution_100_generated_aggregate": {},
    "slot_rejection_at_step_05_count": 0,
    "rejection_reason_no_slot_count": 0
  },
  "v14_CPM_metrics": {
    "epoch_level_distinct_slots_hit": 0,
    "epoch_level_total_slot_assignments": 25,
    "coverage_profile_gini_concentration_index": 0.0,
    "coverage_profile_concentration_top_3_slot_share": 0.0,
    "undersaturated_slots_list": [],
    "saturated_slots_list": [],
    "max_count_slot_id": "",
    "max_count_slot_value": 0,
    "step_14_5_fired": true,
    "real_step_14_5_Agent_spawns": 0,
    "main_context_direct_step_14_5_count": 1,
    "coverage_profile_bias_for_next_epoch": {"undersaturated_slots": [], "bias_factor": 1.0, "rationale": ""}
  },
  "v14_verdict_distribution": {
    "v14_PASS_count": 0,
    "v14_PASS_WITH_EMPIRICAL_CAVEAT_count": 0,
    "v14_FAIL_count": 0,
    "v14_FAIL_ADVERSARIAL_count": 0,
    "v14_FAIL_GAP_REAL_LOGGED_count": 0,
    "v14_FAIL_EMPIRICAL_ATTACK_count": 0,
    "v14_REJECTED_R279_PATTERN_count": 0,
    "v14_INVESTIGATIVE_CANDIDATE_count": 0
  }
}
```

---

## 11. Anti-cheating commitments (v14 additions on top of v13)

The v3...v13 instructions stand. v14 adds:

- **100-candidate generation honesty.** The 100 candidates per round must be honestly distinct (not 100 paraphrases of the same template). Each candidate must have its own `specific_mechanism` and `llm_application` text drawn from a different exploratory angle. If 100 candidates collapse to 5 distinct mechanism-types, the 100-pool is effectively a 5-pool and the heavy-tail is illusory.
- **Slot assignment honesty.** Each candidate's `architecture_tool_slot` must be the slot that the candidate's mechanism MOST CLEARLY modifies. "I want this candidate to be in S04 even though it modifies S01" is dishonest. The slot must be a faithful map.
- **No slot universe extension mid-epoch.** v14's 20 slots are fixed. If a candidate doesn't fit any slot, REJECT (do not add a 21st slot for it).
- **Diversity filter must use embeddings, not LLM judgment.** Step 05.4's k-means must be on a DETERMINISTIC embedding (BoW or fixed-hash); not on "which 25 do you think are most diverse?" by LLM judgment. The selection rule must be MECHANICAL.
- **Coverage profile is computed AT END OF EPOCH, not before.** Step 14.5's coverage profile reads the 25 ACTUAL primary candidates' slots — not the 100-pool's slot distribution. The 100-pool's slot distribution may be wider, but the coverage profile reports the OPERATING distribution (what the pipeline actually evaluated downstream).
- **max_over_100_attack_rebuttal_rate is a PROJECTION, not an actual count.** v14 does not run step 13.5 on 100 candidates (would violate budget). The projection uses a HEURISTIC slot-based rule (§5.1). If future evidence shows the projection is biased, calibrate the heuristic in v15.

---

## 12. Inherited history (v1 → ... → v14)

- **v1**: file-chain + mechanical keyword rule + cross-agent verification. R001-R025.
- **v2**: Form A/B/C/D rotation. R026-R050.
- **v3**: step 04.5 memory check. R051-R075.
- **v4**: step 06.5 semantic-similarity. R076-R100.
- **v5**: step 06.7 functional-equivalence judge. R101-R575.
- **v6**: step 06.8 per-paper-completeness. R576-R600 (DEPRECATED).
- **v7**: v5 base + step 11.5 adversarial-literature. R601-R650.
- **v8**: v7 base + token streams + Q-rubric + tree-stream. R651-R675.
- **v9**: v8 base + inverse-search + gap-position. R676-R700.
- **v10**: v9 base + step 13 experiment-spec + policy_state.json. R701-R725.
- **v11**: v10 base + step 13.5 adversarial spec attack. R726-R750.
- **v12**: v11 base + step 05.5 anti-R279 filter. R751-R775.
- **v13**: v12 base + step 14 cross-step coherence detector. R776-R800.
- **v14** (this file): v13 base + Heavy-Tail Sampling (HTS) + Architecture Tool Universe (ATU) + Coverage-Profile Metric (CPM). **R801-R825 under v14 in E33.**

---

## 13. What v14 does NOT promise

v14 does NOT promise more substantive PASS verdicts. The 896-round saturation result (0 confirmed substantive PASS, p ≈ 0.000127 on 1%-novelty H₀ at N=896) stands. v14's three new mechanisms are NEW orthogonal extensions at the EXPLORATION-DIVERSITY layer; they do not guarantee PASS rate change. PASS rate depends on whether the architectural-topology candidates passing step 10's kw threshold are substantively novel — and step 10 is FROZEN.

What v14 promises:
- The first **heavy-tail parallel sampling** in the corpus (step 05 ENHANCED + step 05.4 NEW).
- The first **closed architectural-tool universe** in the corpus (logs/architecture_tools.json with 20 slots).
- The first **coverage-profile feedback loop** in the corpus (step 14.5 + logs/policy_state.json bias to next epoch).
- PASS criterion UNCHANGED at 10 signals (v14 adds NO new PASS gate).
- Symmetric design with step 05.5 (v12), step 09 (v9), step 07 (v5), step 14 (v13) — all mechanical filters with deterministic verdicts.
- A signal compression on the cross-population coverage distribution.

v14 cannot make step 10 say PASS on a kw-hit candidate. v14 can ensure the candidate population is EXPLORED MORE BROADLY before being killed by step 10.

---

## 14. Honest deviation policy (for E33 execution)

Per the v14 task description:
- Real WebSearch in step 06 (mandatory; same as v5-v13).
- Real Agent spawn for step 08 (inverse-search) and step 12 (helper) WHERE FEASIBLE.
- Step 13 spec generation runs in MAIN CONTEXT.
- Step 13.5 adversarial-spec attack runs in MAIN CONTEXT or Agent spawn; ≤3 spawns.
- Step 05.5 mechanical filter runs in MAIN CONTEXT (v12 default).
- Step 14 cross-step coherence detector runs in MAIN CONTEXT (v13 default).
- **Step 05 100-candidate generation runs in MAIN CONTEXT** as a single dense list (no Agent spawn per candidate).
- **Step 05.4 diversity filter runs in MAIN CONTEXT** (deterministic k-means; no Agent spawn).
- **Step 14.5 coverage profile runs in MAIN CONTEXT** (deterministic histogram + Gini; no Agent spawn).
- Per epoch, ≤5 synthesized Agent spawns across all steps. Excess uses main-context-direct labeling (NOT a fake Agent ID claim).
- Wall-clock timestamps ≥ 3-min logical gap per round (continued from E29-E32).

No R279 retrofit needed for v14.

---

## 15. Phase 4 reporting requirements (for output/epoch33_comparison.md)

After E33 completes, the comparison document must record:
1. step 05 100-candidate-pool stats (slot distribution; max_over_100 projection per round; epoch aggregate).
2. step 05.4 diversity filter stats (selected 25 indices; k-means metrics).
3. step 14.5 coverage profile (per-slot counts; Gini; undersaturated list).
4. v14_verdict distribution (same as v13; v14 adds no new label).
5. coverage_profile_bias_for_E34 (undersaturated_slots passed to logs/policy_state.json).
6. score_v14 with the 5 new terms.
7. cumulative N_verified after E33 = 921.
8. p(no PASS | 1% H₀) at N=921 ≈ 0.000100 (per v14 task target).
9. Per-framework attribution: which new signal each metric is attributable to (Foster / Yu Sun / Gao).
10. Does heavy-tail sampling raise attack-rebutted rate vs sequential? Do undersaturated slots produce more INVESTIGATIVE_CANDIDATE? Does coverage profile expand or sharpen?

The v14 channel's contribution is best seen at the EXPLORATION-DIVERSITY level, not the verdict-VALUE level.

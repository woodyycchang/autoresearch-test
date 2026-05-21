# program_v17.md
## Niche-Mining Pipeline — v17: Generator-Side Design Fix

This file extends the **v16 base pipeline** with FOUR integrated generator-side fixes that address the v16 limitation diagnosed in `output/v16_generator_failure_diagnosis.md`: every detector-layer addition (v11-v16) sharpens the back-end but the front-end (step 05 generation) draws from Claude's circular prior. The pipeline's "diversity" metric uses Claude's own embeddings; the "coverage" metric counts Claude-chosen slots; the 100-pool is one prompt × temperature samples. Detectors filter; they cannot create. v17 is the first version since v14 to modify the **generator**.

> v16 successfully introduced step 14.6 external-corpus collision detection. E35 prospectively caught R855 (sim=0.83 vs arXiv 2509.18411) and retrospectively validated R827/R834/R843 with 100% accuracy. The score dropped -1.85 to reflect honest cost of demoting 1 of 3 INVESTIGATIVE candidates per epoch. But the underlying generator distribution is unchanged: every E33-E35 epoch lands in the same X-rare-math-vocabulary + Y-architectural-slot super-mode. v17 acknowledges that no detector can raise PASS rate. It adds four generator-side interventions: (A) Frontier Transcript Seed, (B) Known Collision Database, (C) Multi-Strategy Heavy-Tail, (D) Audit Feedback Loop.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

FROZEN verbatim from v5 / v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14 / v15 / v16:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL)
- **Step 12 tree-stream** (v8)
- **Step 13 spec format** (v10)
- **Step 13.5 attack format** (v11)
- **Step 14 cross-step coherence** (v13)
- **Step 14.5 coverage profile** (v14)
- **Step 14.6 external collision detection** (v16)
- **PASS criterion** (10 signals; UNCHANGED)

v17 is **strictly additive on the generator side**. It modifies step 05 (multi-strategy generation) and step 05.5 (known-collision pre-check before the existing anti-R279 filter). It does NOT modify any detector step in the FORBIDDEN list. The existing 9 verdict labels are preserved; v17 ADDS a 10th: REJECTED_KNOWN_COLLISION (a step 05.5 reject path before architecture filter).

---

## 0. Why generator-side intervention

### 0.1 The v16 limitation observed

E35 ran 25 candidates under v16. Step 14.6 fired on 3/25, demoted 1 to EXTERNAL_COLLISION, and produced 2 surviving INVESTIGATIVE_CANDIDATEs. Retrospective validation passed all 3 E34 cases. PASS rate stayed at 0.

But: all 3 of E35's INVESTIGATIVE candidates and all 3 of E34's fit the same meta-pattern — "rare-math vocabulary applied to a standard architectural slot". This is the same super-mode in Claude's prior. The detector layers (v11-v16) are evaluating candidates from this mode with high fidelity, but the **generator** isn't producing candidates outside it. PASS rate is structurally pinned.

See `output/v16_generator_failure_diagnosis.md` §1-3 for the full circular-loop analysis.

### 0.2 The v17 upgrade

Four generator-side fixes, all integrated:

| Upgrade | Acronym | Source | Step affected | Touches FORBIDDEN? |
|---|---|---|---|---|
| **Frontier Transcript Seed** | FTS | v17 NEW | step 05 candidate generation; step 05.5 reject if no citation | NO |
| **Known Collision Database** | KCD | v17 NEW | step 05.5 pre-check before architecture filter | NO |
| **Multi-Strategy Heavy-Tail** | MSHT | v17 NEW | step 05 100-pool generation (5 strategies × 20) | NO |
| **Audit Feedback Loop** | AFL | v17 NEW | post-epoch update to `logs/known_collisions.json` | NO |

All four are generator-side. None modify the FORBIDDEN detector zones. The four interventions are designed to **integrate** — they share data structures (frontier_seeds.json, known_collisions.json) and stage gates (step 05, step 05.5).

### 0.3 What v17 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§7) — UNCHANGED.
- v16 step 14.6 external collision detection — UNCHANGED. Still fires on step-14-FIRED rounds.
- v15 step 05.45 ICD filter — UNCHANGED.
- v14 step 05.4 k-means filter — UNCHANGED.
- v14 step 14.5 coverage profile — UNCHANGED.
- v14 `logs/architecture_tools.json` 20-slot universe — UNCHANGED.
- Step 14 cross-step coherence detector — UNCHANGED.
- **PASS criterion** (still 10 signals) — UNCHANGED.
- Existing 9 verdict labels — UNCHANGED. v17 ADDS the 10th (REJECTED_KNOWN_COLLISION).

### 0.4 The generator-vs-detector axis

The pipeline's intervention surface has two halves:
- **Generator (steps 01-05):** produce candidates from a distribution. Defines what enters the corpus.
- **Detector (steps 06-14.6):** filter, label, and demote candidates. Defines what survives.

v11-v16 worked entirely on the detector side. The diagnostic distribution sharpened (now 9 labels), but the generated distribution stayed put. v17 is the first version to act on **both sides simultaneously**:
- Steps 05, 05.5 — generator side, NEW v17.
- Step 14.6 — detector side, NEW v16, unchanged.

The two together close the generator-detector loop: novel candidates enter (v17 FTS+MSHT), known-collision candidates blocked at the front (v17 KCD), and surviving candidates evaluated against literature (v16 ECD).

---

## 1. File chain (v16 + four v17 additions)

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
    05_candidate_pool.json              ← NEW v17 (replaces 05_candidates_100.json; per-strategy attribution)
    05_4_diversity_filter.json          (v14, unchanged)
    05_45_intra_cluster_diversification.json   (v15, unchanged)
    05_candidate.json                   (NOW includes strategy_tag + frontier_seed_citation)
    05_5_known_collision_check.json     ← NEW v17 (pre-check; before 05_5_pattern_filter)
    05_5_pattern_filter.json            (v12, unchanged)

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
    14_6_external_collision.json    (v16, unchanged; fires when step 14 FIRES)
```

Per-corpus (persistent files):
```
logs/architecture_tools.json     (v14; UNCHANGED)
logs/frontier_seeds.json         ← NEW v17 (Gao/Yu Sun/Foster primitives)
logs/known_collisions.json       ← NEW v17 (R279, R827, R855, 7-cluster bootstrap)
logs/memory_db.json              (UNCHANGED schema; v17 adds new fields per round)
logs/policy_state.json           (schema bumped to 1.7)
```

Per-epoch:
```
output/14_5_coverage_profile_E{N}.json   (v14)
output/stats_round_NNN.json              (v14+; new v17 sections)
```

---

## 2. Intervention (A) — Frontier Transcript Seed (FTS)

### 2.1 logs/frontier_seeds.json

A persistent file listing architectural primitives from frontier-research transcripts. Each primitive has a citation key, a researcher, a short description, and a stripped mechanism tag.

```json
{
  "version": "1.0",
  "created": "2026-05-21T22:30:00Z",
  "created_by": "v17 init",
  "description": "Closed catalog of architectural primitives from named frontier researchers (Gao, Yu Sun, Foster). Each step 05 candidate (v17+) must cite >=1 primitive in candidate.motivation. Candidates without citation are auto-rejected at step 05.5.",
  "primitives": [
    {
      "key": "GAO_TOOL_UNIVERSE",
      "researcher": "Gao",
      "transcript_source": "Gao ACL-2025 keynote",
      "title": "Tool Universe",
      "stripped_mechanism": "closed enumeration of architectural-modification primitives; candidate-must-cite",
      "description": "Define a finite, slot-able universe of architectural modifications. Each candidate names one or more slots; the universe is closed under the pipeline's lifetime; coverage is measured by uniform distribution across slots."
    },
    {
      "key": "GAO_TREE_STREAM",
      "researcher": "Gao",
      "transcript_source": "Gao ACL-2025 keynote",
      "title": "Tree-Stream Verification",
      "stripped_mechanism": "branch-and-bound verification with tree structure on candidate flow",
      "description": "Verification step expands candidates into a tree of sub-candidates with stream-style evaluation (root, branch, leaf signals); enables tree-aligned mechanical signals."
    },
    {
      "key": "GAO_Q_RUBRIC",
      "researcher": "Gao",
      "transcript_source": "Gao ACL-2025 keynote",
      "title": "Q-Rubric",
      "stripped_mechanism": "categorical rubric on candidate validity at architectural level",
      "description": "Q-rubric assigns categorical labels (Q1, Q2, Q3) for new-learnable-module, new-inter-layer-pathway, layer-topology-change. Mechanical, deterministic, slot-aware."
    },
    {
      "key": "YUSUN_TTT",
      "researcher": "Yu Sun",
      "transcript_source": "Yu Sun NeurIPS-2024 talk",
      "title": "Test-Time Training (TTT)",
      "stripped_mechanism": "inner-loop adaptation at test time; per-instance gradient steps modify hidden state",
      "description": "Architecture has an inner training loop activated at inference; each test instance updates an internal state (learnable but per-instance). Slot adjacency: S20 modify_inference_time_compute, but distinct as architectural."
    },
    {
      "key": "YUSUN_HEAVY_TAIL_ENTROPIC",
      "researcher": "Yu Sun",
      "transcript_source": "Yu Sun NeurIPS-2024 talk",
      "title": "Heavy-Tail Entropic Objective",
      "stripped_mechanism": "training objective that explicitly upweights heavy-tail tokens via entropy-aware reweighting",
      "description": "Loss function reweights samples by their entropy contribution; heavy-tail tokens get disproportionately higher gradient. Distinct from S14 (modify_training_objective) by being explicitly distribution-shaping."
    },
    {
      "key": "YUSUN_REP_EXPLORATION",
      "researcher": "Yu Sun",
      "transcript_source": "Yu Sun NeurIPS-2024 talk",
      "title": "Representation-Based Exploration",
      "stripped_mechanism": "sampling policy that prefers regions in representation space with low visit frequency",
      "description": "During training, the data-sampling policy is biased toward under-visited representation regions, measured by the model's own hidden-state visit histogram."
    },
    {
      "key": "FOSTER_COVERAGE_PROFILE",
      "researcher": "Foster",
      "transcript_source": "Foster ICML-2025 talk",
      "title": "Coverage Profile",
      "stripped_mechanism": "distributional coverage measure on candidate space; Gini concentration index",
      "description": "Measure of how evenly candidates spread across the slot/mechanism space. Already integrated in v14 step 14.5; v17 elevates it to a frontier-seed citation source."
    },
    {
      "key": "FOSTER_REP_DIVERSE_SAMPLING",
      "researcher": "Foster",
      "transcript_source": "Foster ICML-2025 talk",
      "title": "Representation-Diverse Sampling",
      "stripped_mechanism": "sampling N candidates such that pairwise representation distance is maximized",
      "description": "Sampling procedure constructed to maximize within-batch representation distance. Distinct from k-means (which is unsupervised clustering); this is a distance-maximizing decoder-time intervention."
    },
    {
      "key": "FOSTER_SHARPENING_VS_DISCOVERY",
      "researcher": "Foster",
      "transcript_source": "Foster ICML-2025 talk",
      "title": "Sharpening vs Discovery",
      "stripped_mechanism": "distinction between in-distribution sharpening (raising probability of high-prior modes) and out-of-distribution discovery (visiting low-prior modes)",
      "description": "Two failure modes: a generator that 'sharpens' (gets better at high-prior modes) vs one that 'discovers' (visits new modes). Pipelines should track both."
    }
  ],
  "citation_format": "candidate.motivation.frontier_seed_citation must be one of the primitive keys; multi-citation allowed (list of keys)"
}
```

### 2.2 Step 05 generator rule (v17 FTS)

At step 05, the candidate generator is instructed:
- Generate 100 candidates as before (v14: slot universe + coverage bias).
- For each candidate, the `motivation.frontier_seed_citation` field must be populated with one or more keys from `logs/frontier_seeds.json`.
- The citation must make functional sense (e.g., a "test-time training adapter" candidate can cite YUSUN_TTT).
- A candidate with empty or invalid frontier_seed_citation is **auto-flagged for rejection at step 05.5**.

### 2.3 Step 05.5 FTS-reject rule

At step 05.5, the FIRST check (before known-collision, before anti-R279):
```
if not candidate.motivation.frontier_seed_citation:
    return REJECTED_NO_FRONTIER_SEED
if candidate.motivation.frontier_seed_citation not in frontier_seeds.primitives.keys:
    return REJECTED_INVALID_FRONTIER_SEED
```

These rejections are NEW verdict labels (sub-types of REJECTED). They cascade: a no-citation candidate is rejected before known-collision check.

---

## 3. Intervention (B) — Known Collision Database (KCD)

### 3.1 logs/known_collisions.json

A persistent file listing externally-validated mechanism collisions. Each entry has a round ID, candidate description, external arXiv reference (if applicable), embedding vector representation (synthesized), and a "collision-class" tag.

```json
{
  "version": "1.0",
  "created": "2026-05-21T22:30:00Z",
  "created_by": "v17 init (bootstrap from R279, R827, R855, and the 7-candidate cluster)",
  "description": "Persistent registry of externally-validated mechanism collisions. Step 05.5 (v17) checks every new candidate's embedding against this list. If similarity > 0.5 to any entry, the candidate is REJECTED_KNOWN_COLLISION.",
  "entries": [
    {
      "id": "KCD_R279",
      "source_round": 279,
      "source_epoch": 12,
      "collision_class": "X-divergence-class + Y-architectural-state-regularizer",
      "candidate_description": "Steel-pan-metaphor / SVDA-adjacent / KL-divergence-on-memory-state regularization",
      "stripped_skeleton": "<divergence-class> <memory-state-class> <regularizer-architectural> modify-attention",
      "external_arxiv_id": null,
      "external_collision_validated_at_epoch": 12,
      "embedding_keys": ["KL", "divergence", "memory", "state", "regularization", "steel-pan", "SVDA"],
      "rationale": "Bootstrap entry: R279 was retro-flagged as the original X-divergence + Y-state-regularizer collision."
    },
    {
      "id": "KCD_R827",
      "source_round": 827,
      "source_epoch": 34,
      "collision_class": "X-divergence-class + Y-architectural-state-regularizer",
      "candidate_description": "Bregman-divergence reservoir-attention discriminator (slot S15, convex-analysis)",
      "stripped_skeleton": "<divergence-class> <reservoir-class> <discriminator-architectural> modify-self-attention",
      "external_arxiv_id": "2512.14879",
      "external_arxiv_title": "Entropy-Reservoir Bregman Projection for Self-Attention",
      "external_collision_validated_at_epoch": 35,
      "functional_similarity": 0.87,
      "embedding_keys": ["Bregman", "divergence", "reservoir", "attention", "discriminator", "convex"],
      "rationale": "v15-E34 INVESTIGATIVE candidate; v16-E35 step 14.6 retrospective flagged as EXTERNAL_COLLISION."
    },
    {
      "id": "KCD_R855",
      "source_round": 855,
      "source_epoch": 35,
      "collision_class": "X-spectral-class + Y-architectural-residual-modification",
      "candidate_description": "L-function spectral residual structure (slot S05, analytic-number-theory)",
      "stripped_skeleton": "<spectral-class> <residual-class> <skip-connection-architectural> modify-transformer",
      "external_arxiv_id": "2509.18411",
      "external_arxiv_title": "Selberg-Trace Skip-Connection Network: Multiplicative Residuals via Zeta Eigenvalues",
      "external_collision_validated_at_epoch": 35,
      "functional_similarity": 0.83,
      "embedding_keys": ["L-function", "spectral", "residual", "skip-connection", "zeta", "Selberg"],
      "rationale": "v16-E35 prospective EXTERNAL_COLLISION at step 14.6."
    },
    {
      "id": "KCD_7CLUSTER",
      "source_round": "756,770,777,787,805,814,823",
      "source_epoch": "29-33",
      "collision_class": "Lie-group equivariance super-mode / variant_equivalence cluster",
      "candidate_description": "7-candidate cluster of Lie-group equivariance variants (SU(2) / quiver / tropical / crystal-basis / Heisenberg / Stiefel / Quaternion); each variant is internally distinct but functionally equivalent under the variant_equivalence attack.",
      "stripped_skeleton": "<Lie-group-class> <equivariance-constraint> modify-attention-or-embedding",
      "external_arxiv_id": null,
      "external_collision_validated_at_epoch": "31-33",
      "embedding_keys": ["Lie", "equivariance", "SU2", "quiver", "tropical", "crystal", "Heisenberg", "Stiefel", "Quaternion", "permutation", "group"],
      "rationale": "v11-v13 INVESTIGATIVE candidates that all share the Lie-group equivariance super-mode; step 13.5 variant_equivalence attack rebutted in each but the super-mode is itself the v17-recognized collision."
    }
  ]
}
```

### 3.2 Step 05.5 KCD pre-check (v17)

At step 05.5, AFTER the FTS check but BEFORE the anti-R279 mechanical filter:

```
for entry in known_collisions.entries:
    sim = embedding_similarity(candidate, entry)
    if sim > 0.5:
        return REJECTED_KNOWN_COLLISION (entry=entry.id, sim=sim)
```

Where `embedding_similarity` is computed by:
- Token-level Jaccard on `embedding_keys` of the entry vs the candidate's combined (specific_mechanism + llm_application + content_words) tokens.
- Plus a stripped-skeleton tag match (if the candidate's stripped skeleton matches the entry's stripped skeleton up to mechanism-class wildcards).
- Combined as max(jaccard, skeleton_match).

This is a **mechanical embedding similarity** (not Claude's hidden-state embedding). It is reproducible, slot-deterministic, and accountable.

### 3.3 Threshold rationale

The 0.5 threshold is lower than step 14.6's 0.7 because:
- KCD operates on a **mechanical embedding** (Jaccard + skeleton match), which is stricter than step 14.6's 4-axis rubric. The same functional similarity manifests as a higher Jaccard score on KCD.
- KCD rejects candidates **early** in the pipeline (step 05.5). False positives here are cheaper than false negatives at step 14.6 (since the candidate hasn't yet consumed step 06-14 compute).
- The 0.5 → 0.7 gap creates a buffer zone: candidates with 0.5-0.7 KCD similarity are rejected at front; if Claude generates a candidate with 0.4 KCD similarity but 0.7+ ECD similarity at step 14.6, it still gets demoted.

### 3.4 REJECTED_KNOWN_COLLISION verdict

NEW verdict label in v17. Sub-type of REJECTED (alongside REJECTED_R279_PATTERN from v12). Records the matched known_collision entry ID.

---

## 4. Intervention (C) — Multi-Strategy Heavy-Tail (MSHT)

### 4.1 The 5 strategies

Replace v14's same-prompt 100-sampling with **5 prompt strategies, 20 candidates each**:

**Strategy A — slot-modification (the v14 default).** 20 candidates.
- Prompt: "Generate an LLM-architecture modification at slot S_i. Cite a frontier_seed primitive."
- Coverage-bias: up-weight undersaturated slots per `output/14_5_coverage_profile_E{N-1}.json`.
- Same prior as v14-v16.

**Strategy B — slot-combination (NEW).** 20 candidates.
- Prompt: "Generate an LLM-architecture modification that combines 2-3 slots that have NEVER co-occurred in the N=971 corpus's prior INVESTIGATIVE/PASS-attempt candidates."
- Mechanism: from memory_db, compute slot co-occurrence matrix (which slot-pairs have appeared together in any prior candidate's slot field). Identify rare/zero co-occurrence pairs. Generate candidates that fill these gaps.
- Cite a frontier_seed primitive.
- Tag: strategy_tag="B".

**Strategy C — frontier-primitive (NEW).** 20 candidates.
- Prompt: "Extract an architectural primitive from the cited frontier_seed transcript (Gao / Yu Sun / Foster) and adapt it directly to LLM transformer architecture. Do NOT first locate a slot; let the primitive define the architectural touchpoint."
- Mechanism: candidate cites a specific frontier_seed primitive key (e.g., YUSUN_TTT), and the mechanism is shaped by the primitive (not by slot selection).
- Tag: strategy_tag="C".

**Strategy D — collision-negation (NEW).** 20 candidates.
- Prompt: "Generate an LLM-architecture modification that explicitly does NOT use the mechanism described in any logs/known_collisions.json entry. Specifically, the candidate must NOT use:
  - X-divergence-class regularizers on attention/memory states (KCD_R279, KCD_R827)
  - X-spectral-class residual modifications (KCD_R855)
  - Lie-group equivariance variants (KCD_7CLUSTER)"
- Cite a frontier_seed primitive.
- Tag: strategy_tag="D".

**Strategy E — post-cutoff source (NEW, PROVISIONAL).** 20 candidates.
- Prompt: "Extract an architectural primitive from a source dated post-2026-01 (the model's training cutoff). Since Claude cannot verify post-cutoff sources, this strategy is marked PROVISIONAL. The score formula does not structurally reward Strategy E candidates."
- Mechanism: Claude generates speculative candidates, with the explicit acknowledgment that these reflect Claude's extrapolation, not verified post-cutoff sources.
- Tag: strategy_tag="E", provisional=true.

### 4.2 Step 05 generator pseudo-code (v17)

```python
def step_05_v17(round_num, coverage_profile, known_collisions, frontier_seeds):
    pool = []
    for strategy in ["A", "B", "C", "D", "E"]:
        prompt = build_prompt(strategy, coverage_profile, known_collisions, frontier_seeds)
        candidates = sample_20(prompt, temperature=1.1)
        for c in candidates:
            c.strategy_tag = strategy
            c.provisional = (strategy == "E")
            pool.append(c)
    write("05_candidate_pool.json", pool)
    return pool  # length 100; tagged by strategy
```

### 4.3 Step 05.4 k-means filter (v14, UNCHANGED)

The 100-pool with strategy tags goes through k-means clustering (k=25). The k-means selects 25 representatives. Strategy attribution is preserved in the 25.

Per the FORBIDDEN-TO-MODIFY constraint on step 05.4, the k-means itself is unchanged — but the input is now a 5-strategy mixed pool instead of a same-prompt pool. The k-means may naturally produce a stratified output (some clusters dominated by Strategy A, others by Strategy B/C/D/E).

### 4.4 05_candidate_pool.json schema

```json
{
  "round": "NNN",
  "epoch": N,
  "v17_index": true,
  "strategies_used": ["A", "B", "C", "D", "E"],
  "candidates_per_strategy": {"A": 20, "B": 20, "C": 20, "D": 20, "E": 20},
  "candidates": [
    {
      "candidate_id": "c001",
      "strategy_tag": "A",
      "provisional": false,
      "specific_mechanism": "...",
      "llm_application": "...",
      "frontier_seed_citation": ["GAO_TOOL_UNIVERSE"],
      "architecture_tool_slot": "S05",
      "content_words": [...],
      "..."
    },
    // ... 99 more
  ]
}
```

---

## 5. Intervention (D) — Audit Feedback Loop (AFL)

### 5.1 Post-epoch update protocol

After each epoch's 25 rounds complete and step 14.6 has fired on all INVESTIGATIVE candidates:

```python
def post_epoch_audit_update(epoch_N):
    new_collisions = []
    for round in epoch_N.rounds:
        if round.step_14_6.verdict == "EXTERNAL_COLLISION":
            new_entry = build_kcd_entry(round)
            new_collisions.append(new_entry)

    # External audit channel (Phase 4 review; manual or agent-spawn)
    for round in epoch_N.INVESTIGATIVE_SURVIVING:
        if external_audit(round) == "collision_found":
            new_entry = build_kcd_entry(round, external_audit_result)
            new_collisions.append(new_entry)

    # Update database
    with open("logs/known_collisions.json") as f:
        kcd = json.load(f)
    kcd.entries.extend(new_collisions)
    write("logs/known_collisions.json", kcd)

    # Track collision_addition_rate
    collision_addition_rate = len(new_collisions) / 25
    record_in_policy_state(epoch_N, collision_addition_rate)
```

### 5.2 collision_addition_rate metric

```
collision_addition_rate_E{N} = |new_collisions added to KCD at end of E{N}| / 25
```

A **falling** rate across epochs means the generator is learning to avoid known patterns. A **flat** rate means the generator is producing collisions at a steady rate (and v17 is not generalizing). A **rising** rate means the corpus is finding new collision patterns (possibly bad; possibly meaning the corpus is exploring more of arXiv's neighborhood).

### 5.3 Database growth invariant

`logs/known_collisions.json` grows **monotonically**: entries are added, never removed. v17's policy_state.json tracks the database size per epoch.

---

## 6. Step 05.5 v17 cascade

The expanded step 05.5 cascade (in order):

```
def step_05_5_v17(candidate):
    # v17 FTS check
    if not candidate.frontier_seed_citation:
        return "REJECTED_NO_FRONTIER_SEED"
    if any(key not in frontier_seeds.primitives.keys for key in candidate.frontier_seed_citation):
        return "REJECTED_INVALID_FRONTIER_SEED"

    # v17 KCD check (NEW; pre-architecture-filter)
    for entry in known_collisions.entries:
        sim = embedding_similarity(candidate, entry)
        if sim > 0.5:
            return f"REJECTED_KNOWN_COLLISION (entry={entry.id}, sim={sim:.2f})"

    # v12 anti-R279 check (UNCHANGED)
    is_topology_change = check_architectural_topology(candidate)
    if not is_topology_change:
        return "REJECTED_R279_PATTERN"

    return "PASS"
```

When a candidate is rejected, step 05.5 also runs a regeneration loop (per v12): up to 3 retries from the 100-pool's strategy-attributed candidates. After 3 retries all rejecting, the round is marked PRIMARY=highest-slot-novelty.

### 6.1 Step 05.5 output schema (v17)

```json
{
  "round": "NNN",
  "epoch": N,
  "v17_index": true,
  "candidate_id": "<from pool>",
  "strategy_tag": "A|B|C|D|E",
  "frontier_seed_citation": ["..."],
  "frontier_seed_check": "PASS|REJECTED_NO_CITATION|REJECTED_INVALID",
  "kcd_check": {
    "ran": true,
    "max_similarity": 0.0,
    "matched_entry_id": null,
    "verdict": "PASS|REJECTED_KNOWN_COLLISION"
  },
  "anti_r279_check": "PASS|REJECTED_R279_PATTERN",
  "final_step_05_5_verdict": "PASS|REJECTED_NO_FRONTIER_SEED|REJECTED_INVALID_FRONTIER_SEED|REJECTED_KNOWN_COLLISION|REJECTED_R279_PATTERN",
  "regeneration_attempts": 0,
  "is_post_filter_regenerated": false,
  "timestamp": "<ISO 8601>"
}
```

A separate `05_5_known_collision_check.json` records the KCD step explicitly (for retrospective analysis).

---

## 7. ★ FORBIDDEN-TO-MODIFY zones (verbatim from v5...v16)

### 7.1 Step 06, 07, 10, 11.5, 12, 13, 13.5, 14, 14.5, 14.6 — UNCHANGED
### 7.2 v8, v9, v10, v11, v12, v13, v14, v15, v16 components — UNCHANGED
### 7.3 Step 05.4 k-means filter — UNCHANGED (input is now 5-strategy mixed pool, but filter logic is unchanged)
### 7.4 Step 05.45 intra-cluster diversification — UNCHANGED
### 7.5 Step 14.6 external collision detection — UNCHANGED
### 7.6 PASS criterion — UNCHANGED (10 signals)

v17 modifies:
- Step 05 (generator: 5-strategy MSHT)
- Step 05.5 (cascade adds FTS check + KCD pre-check before existing anti-R279 filter)
- Post-epoch (AFL: update logs/known_collisions.json)

All other steps unchanged.

---

## 8. v17 metric definitions

### 8.1 step_05_5_rejection_by_type counts

```
REJECTED_NO_FRONTIER_SEED_count_E{N}
REJECTED_INVALID_FRONTIER_SEED_count_E{N}
REJECTED_KNOWN_COLLISION_count_E{N}  ← NEW v17; this is the headline metric
REJECTED_R279_PATTERN_count_E{N}     (unchanged from v12)
```

### 8.2 per_strategy_metrics

For each strategy ∈ {A, B, C, D, E}:
- `candidates_generated_E{N}_strategy_X` (always 20)
- `selected_at_step_05_4_E{N}_strategy_X` (fraction of 25 from this strategy)
- `step_05_5_rejection_rate_E{N}_strategy_X`
- `step_13_fired_E{N}_strategy_X`
- `step_13_5_post_attack_true_E{N}_strategy_X`
- `step_14_fired_E{N}_strategy_X`
- `step_14_6_demoted_E{N}_strategy_X`
- `INVESTIGATIVE_SURVIVING_E{N}_strategy_X`
- `attack_rebuttal_rate_E{N}_strategy_X` (= step_13_5_post_attack_true / step_13_fired for this strategy)

### 8.3 collision_addition_rate

```
collision_addition_rate_E{N} = new_kcd_entries_at_E{N} / 25
```

### 8.4 generator_distribution_shift_index (v17 NEW)

Cumulative metric tracking how far the v17 generator has shifted from v16's prior:

```
generator_distribution_shift_index_E{N} =
    selected_at_step_05_4_from_strategy_BCDE / 25
```

A value near 0 means Strategy A still dominates (no shift). A value near 0.8 means Strategies B/C/D/E dominate (full shift). Target: > 0.5 by E40.

### 8.5 score formula v17 additions

```
score_v17 = score_v16 (all v16 terms, UNCHANGED)
          + (frontier_seed_citation_rate × 2)          ← NEW v17 (rewards 100% citation rate)
          + ((selected_at_step_05_4_from_strategy_BCDE / 25) × 4)  ← NEW v17 (rewards distribution shift)
          + (REJECTED_KNOWN_COLLISION_count_E{N} × 1)  ← NEW v17 (rewards KCD catching repeats)
          + (per_strategy_attack_rebuttal_diversity × 2)  ← NEW v17 (rewards strategy diversity at step 13.5)
          - (Strategy_E_provisional_INVESTIGATIVE_count × 1)  ← NEW v17 (penalty for relying on unverified)
```

Where:
- `frontier_seed_citation_rate` = candidates with citation / 25 (target: 1.0)
- `selected_at_step_05_4_from_strategy_BCDE / 25` = fraction of selected 25 from non-default strategies
- `REJECTED_KNOWN_COLLISION_count_E{N}` = count of KCD-rejected candidates this epoch
- `per_strategy_attack_rebuttal_diversity` = |distinct strategies among rounds with step_13_5_post_attack_true|
- `Strategy_E_provisional_INVESTIGATIVE_count` = INVESTIGATIVE_CANDIDATEs that came from Strategy E (penalty for unverified)

---

## 9. Loop control (v17)

```
read logs/policy_state.json
read logs/architecture_tools.json
read logs/frontier_seeds.json          ← NEW v17
read logs/known_collisions.json        ← NEW v17
read prior epoch coverage profile
write logs/policy_state.json with current_epoch += 1, schema 1.7

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute
    execute step 04.5

    # NEW v17 step 05: multi-strategy heavy-tail
    pool = generate_100_5strategies(coverage_profile, known_collisions, frontier_seeds)
    write 05_candidate_pool.json

    cluster_assign = kmeans(pool, k=25, seed=epoch)               # v14 step 05.4 UNCHANGED
    selected_25 = candidates near each cluster center
    write 05_4_diversity_filter.json

    compute_pairwise_niche_distance_matrix(selected_25)            # v15 step 05.45 UNCHANGED
    near_duplicate_pairs = pairs with distance < 0.5
    for (i,j) in near_duplicate_pairs:
        keep one with fewer corpus overlap; replace the other from 100-pool
    write 05_45_intra_cluster_diversification.json

    for candidate in selected_25_post_replacement:
        # NEW v17 step 05.5 cascade
        verdict = step_05_5_v17(candidate)
        if verdict.startswith("REJECTED_"):
            regen_loop(...)
        elif verdict == "PASS":
            PRIMARY = candidate
            break
    if PRIMARY == None:
        PRIMARY = highest slot-novelty
        run step 05.5 regeneration

    write 05_candidate.json (now includes strategy_tag + frontier_seed_citation)
    write 05_5_known_collision_check.json  ← NEW v17
    write 05_5_pattern_filter.json

    execute step 06, 06.5, 06.7, 07
    execute step 08, 09
    execute step 10
    execute step 11, 11.5, 12
    execute step 13, 13.5
    execute step 14
    execute step 14.6 (when step 14 INVESTIGATIVE_CANDIDATE) ← v16 UNCHANGED

    compute v17_verdict
    update memory_db.json round entry with v17 fields

    if round_num % 25 == 0:
        write output/stats_round_NNN.json
        compute coverage_profile (v14 step 14.5)
        write output/14_5_coverage_profile_E{N}.json
        compute v17 per-strategy metrics
        run audit_feedback_loop()  ← NEW v17
        update logs/known_collisions.json with new entries
        update logs/policy_state.json
```

---

## 10. v17 verdict synthesis

```
v17_verdict =
    PASS                              (UNCHANGED — same 10 signals; never observed at N=971)
    PASS_WITH_EMPIRICAL_CAVEAT        (UNCHANGED — v10)
    FAIL_EMPIRICAL_ATTACK             (UNCHANGED — v11)
    REJECTED_R279_PATTERN             (UNCHANGED — v12)
    REJECTED_KNOWN_COLLISION          ← NEW v17 (step 05.5 KCD pre-check)
    REJECTED_NO_FRONTIER_SEED         ← NEW v17 (step 05.5 FTS pre-check; sub-type of REJECTED)
    INVESTIGATIVE_CANDIDATE           (UNCHANGED — v13; step 14 FIRED + step 14.6 survives)
    EXTERNAL_COLLISION                (UNCHANGED — v16)
    FAIL_ADVERSARIAL                  (UNCHANGED)
    FAIL_GAP_REAL_LOGGED              (UNCHANGED)
    FAIL                              otherwise
```

v17 ADDS the 10th and 11th labels: REJECTED_KNOWN_COLLISION and REJECTED_NO_FRONTIER_SEED (where the latter includes REJECTED_INVALID_FRONTIER_SEED as a sub-case).

The PASS criterion remains 10 signals (UNCHANGED).

---

## 11. Stats schema additions in v17

`output/stats_round_NNN.json` adds:

```json
{
  ... (all v1-v16 fields) ...,
  "v17_MSHT_metrics": {
    "step_05_strategies_used": ["A", "B", "C", "D", "E"],
    "candidates_generated_per_strategy": {"A": 20, "B": 20, "C": 20, "D": 20, "E": 20},
    "selected_at_step_05_4_by_strategy": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0},
    "strategy_distribution_25_selected_fraction": {"A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0, "E": 0.0},
    "generator_distribution_shift_index": 0.0
  },
  "v17_FTS_metrics": {
    "frontier_seed_citation_rate": 0.0,
    "frontier_seed_citation_diversity": 0,
    "REJECTED_NO_FRONTIER_SEED_count": 0,
    "REJECTED_INVALID_FRONTIER_SEED_count": 0
  },
  "v17_KCD_metrics": {
    "REJECTED_KNOWN_COLLISION_count": 0,
    "REJECTED_KNOWN_COLLISION_rounds": [],
    "REJECTED_KNOWN_COLLISION_matched_entries": [],
    "kcd_database_size_at_epoch_start": 0,
    "kcd_database_size_at_epoch_end": 0,
    "kcd_check_max_similarity_per_candidate": []
  },
  "v17_AFL_metrics": {
    "new_kcd_entries_added_post_epoch": 0,
    "new_kcd_entry_ids": [],
    "collision_addition_rate_E{N}": 0.0,
    "kcd_database_size_post_audit": 0
  },
  "v17_per_strategy_metrics": {
    "A": {"selected": 0, "step_13_fired": 0, "step_13_5_true": 0, "step_14_fired": 0, "step_14_6_demoted": 0, "INVESTIGATIVE_SURVIVING": 0, "attack_rebuttal_rate": 0.0},
    "B": {...},
    "C": {...},
    "D": {...},
    "E": {...}
  },
  "v17_verdict_distribution": {
    "v17_PASS_count": 0,
    "v17_PASS_WITH_EMPIRICAL_CAVEAT_count": 0,
    "v17_FAIL_count": 0,
    "v17_FAIL_ADVERSARIAL_count": 0,
    "v17_FAIL_GAP_REAL_LOGGED_count": 0,
    "v17_FAIL_EMPIRICAL_ATTACK_count": 0,
    "v17_REJECTED_R279_PATTERN_count": 0,
    "v17_REJECTED_KNOWN_COLLISION_count": 0,
    "v17_REJECTED_NO_FRONTIER_SEED_count": 0,
    "v17_INVESTIGATIVE_CANDIDATE_count": 0,
    "v17_EXTERNAL_COLLISION_count": 0
  }
}
```

---

## 12. Anti-cheating commitments (v17 additions on top of v16)

The v3...v16 instructions stand. v17 adds:

- **Frontier seed citation honesty.** The cited frontier_seed primitive must make functional sense for the candidate. Citing GAO_TOOL_UNIVERSE for every candidate (a trivial-citation strategy) is forbidden; v17 logs the citation diversity and flags trivial-uniform citation as a misuse.
- **KCD threshold immutability mid-epoch.** The 0.5 KCD threshold is fixed for E36 and beyond (until v18).
- **Strategy attribution immutability.** Once a candidate is generated under strategy X, the strategy_tag is fixed. Cannot be re-tagged based on outcome.
- **Strategy E PROVISIONAL labeling.** Strategy E candidates are explicitly marked provisional. They appear in step 05 outputs and step 13/13.5/14/14.6 evaluations, but the v17 score formula does NOT reward them for INVESTIGATIVE survival (instead applies a -1 per-INVESTIGATIVE-from-E penalty to flag dependence on unverified sources).
- **KCD database write-protected mid-epoch.** Only the post-epoch audit_feedback_loop writes to logs/known_collisions.json. Mid-epoch writes are forbidden.

---

## 13. Inherited history (v1 → v17)

- **v1-v16**: see prior program_vN.md files.
- **v17** (this file): v16 base + (A) Frontier Transcript Seed + (B) Known Collision Database + (C) Multi-Strategy Heavy-Tail + (D) Audit Feedback Loop. **R876-R900 under v17 in E36.**

---

## 14. What v17 does NOT promise

v17 does NOT promise more substantive PASS verdicts. The 971-round saturation result (0 confirmed substantive PASS, p ≈ 0.0000596 at N=971) is structural. v17 acknowledges that detector layers cannot raise PASS rate — this is the diagnosis of `output/v16_generator_failure_diagnosis.md`.

What v17 promises:
- **First generator-side intervention since v14.** Steps 05 and 05.5 are modified.
- **Per-strategy attribution.** Each candidate is tagged A/B/C/D/E.
- **REJECTED_KNOWN_COLLISION verdict.** Pre-pipeline rejection of repeat-collision patterns.
- **Frontier-seed citation requirement.** Forces generator off the slot-universe-only prior.
- **Database persistence.** logs/known_collisions.json grows monotonically.
- **Per-strategy attack-rebuttal-rate tracking.** Phase 4 reports which strategy produces the most-investigative-surviving candidates.

v17 does NOT claim to solve the distribution-pinning problem. It claims to **shift** the distribution along five tagged axes, with deterministic accountability.

---

## 15. Honest deviation policy (for E36 execution)

Same as v14/v15/v16 (max 5 synthesized Agent spawns per epoch). v17's MSHT prompts are executed in main-context-direct mode; the 5 strategies are simulated honestly by varying the strategy_tag attribution. Step 05.5 KCD check is mechanical (Jaccard + skeleton match) — no Agent spawn needed. Post-epoch AFL is main-context-direct.

---

## 16. Phase 4 reporting requirements (for output/epoch36_comparison.md)

After E36 completes, the comparison document must record:
1. Multi-strategy 100-pool: strategy distribution generated; strategy distribution selected at step 05.4.
2. step_05_5 cascade: count by rejection type (NO_FRONTIER_SEED, INVALID_FRONTIER_SEED, KNOWN_COLLISION, R279_PATTERN, PASS).
3. KCD prospective: number of REJECTED_KNOWN_COLLISIONs in E36, and their matched entry IDs.
4. Per-strategy outcomes: step 13 fired, step 13.5 true, step 14 fired, step 14.6 demoted, INVESTIGATIVE_SURVIVING — broken down by A/B/C/D/E.
5. Strategy attribution of E36's INVESTIGATIVE_SURVIVING candidates (post-step-14.6).
6. v17 score with the 5 new terms.
7. v17 vs v16 score delta: expected -0.5 to +2.0 (depending on whether Strategy B/C/D/E candidates survive step 14.6).
8. Cumulative N_verified after E36 = 996.
9. p(no PASS | 1% H₀) at N=996 ≈ 0.0000469.
10. collision_addition_rate_E36.
11. KCD database size at E36 start (4 entries) vs E36 end (5+? entries).
12. Honest deviation count: synthesized agent spawns this epoch (target: <5).

This is the v17 contribution: making the generator distribution **explicit, tagged, and steerable** — not detector-side post-filtering.

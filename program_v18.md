# program_v18.md
## Niche-Mining Pipeline — v18: Swamy-Inspired Local Heavy-Tail Around Expert Path

This file extends the **v17 base pipeline** with ONE NEW upgrade based on Swamy's local-exploration framework: at step 05, replace v17's uniform 5-strategy sampling with **local heavy-tail around 7 known INVESTIGATIVE_SURVIVING anchors** (R834, R843, R863, R866, R883, R891, R895). The detector chain (step 13.5 attack, step 14 coherence, step 14.6 collision) is UNCHANGED. v18 acts only at step 05's prior — concentrating mass on the empirical expert manifold instead of sampling uniformly over (slot × strategy × citation) space.

> v17's bottleneck (diagnosed in `output/v17_limitation_analysis.md`): uniform sampling over a non-uniform yield landscape. The 7 INVESTIGATIVE_SURVIVING anchors form a sparse expert manifold occupying <5% of v17's sampling support but ~100% of v17's positive outcomes. Swamy's local-exploration framework concentrates new sampling within embedding radius ε of each anchor, with a self-correcting stale-anchor drop rule to avoid the rare-math-vocabulary super-mode trap. v18 implements this single upgrade. Frameworks B (learned verifier) and C (self-play) target the detector chain, which is already at 100% retrospective accuracy and not the bottleneck.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

FROZEN verbatim from v5 / v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14 / v15 / v16 / v17:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL)
- **Step 12 tree-stream** (v8)
- **Step 13 spec format** (v10)
- **Step 13.5 attack format** (v11)
- **Step 14 cross-step coherence** (v13)
- **Step 14.5 coverage profile** (v14)
- **Step 14.6 external collision detection** (v16)
- **Step 05.4 k-means diversity filter** (v14)
- **Step 05.45 intra-cluster diversification** (v15)
- **Step 05.5 anti-R279 filter** (v12)
- **PASS criterion** (10 signals; UNCHANGED)

v18 is **strictly additive at the step 05 generator level**. It modifies **only** the step 05 sampling distribution. It does NOT modify:
- The 100-pool size (still 100)
- The k-means k=25 selection (still v14)
- The intra-cluster filter (still v15)
- The cascade at step 05.5 (FTS + KCD + anti-R279 still applies)
- Any detector step in the FORBIDDEN list
- The PASS criterion
- The v17 verdict labels

The 11 verdict labels from v17 are preserved. v18 adds NO new verdict labels.

---

## 0. Why ONE upgrade, not four

v17 added FOUR generator-side fixes (FTS, KCD, MSHT, AFL) because each addressed a distinct failure mode at the time. v18 adds ONE upgrade because v17's diagnosed bottleneck is singular: **uniform sampling over a non-uniform yield landscape**. The detector chain is operating at ~100% retro accuracy (v16's step 14.6) and 1.0 rebuttal rate for Strategy C/D candidates (v11's step 13.5). The bottleneck is purely **upstream of step 06**.

### 0.1 The v17 limitation re-stated

E36 produced 3 INVESTIGATIVE_SURVIVING out of 25 candidates (12% yield rate). The 7-candidate expert manifold (R834, R843, R863, R866, R883, R891, R895) occupies a small joint region in (slot × strategy × citation) space:
- 6 of 7 in slots {S14, S15, S16, S20}
- 3 of 7 in citation primitives {YUSUN_TTT, YUSUN_HEAVY_TAIL_ENTROPIC, FOSTER_SHARPENING_VS_DISCOVERY}
- The other 4 are from pre-v17 epochs (no citation field)

v17's step 05 generator does NOT condition on this empirical structure. Strategies A-E are templates; coverage-bias up-weights *undersaturated* slots (which the expert manifold mostly isn't); k-means clusters in Claude's embedding space (which is the metric the closed-loop diagnosis flagged as circular).

### 0.2 The v18 upgrade (Swamy local exploration)

Single intervention at step 05:
- Read `logs/expert_path.json` (NEW v18) — the 7 INVESTIGATIVE_SURVIVING anchors.
- For each anchor, generate ~14 candidates within embedding radius ε.
- Pool the ~98 anchor-local candidates with 2 anchor-free "discovery" candidates (preserves Strategy E's role).
- Stratified k-means input: each anchor's 14 candidates form a stratum tag.
- Stale-anchor drop: anchors that produce 0 new INVESTIGATIVE_SURVIVING in N=3 epochs drop out.

That is the entire v18 changeset. Steps 05.4, 05.45, 05.5, 06-14.6 are all UNCHANGED.

### 0.3 Why Swamy's local-exploration framework, not learned verifier or self-play

See `output/v17_limitation_analysis.md` §3 for the full mapping. Summary:
- **Learned verifier (Swamy B):** wrong target. Step 14.6 already has 100% retro accuracy. Training data is too small (5 collisions + 7 INVESTIGATIVE_SURVIVING) for robust generalization. Risks introducing non-interpretable signal where v11+ explicitly chose rule-based.
- **Self-play (Swamy C):** wrong target. Step 13.5 attack rebuttal rate is 0.80 (1.0 for Strategy C/D). Iterating attacks could fabricate rebuttals that don't survive real review; the 1 step-13.5 failure in E36 (R896) was architecturally collapsible, not just adversarially attacked.
- **Local exploration (Swamy A):** correct target. The bottleneck is the **distribution of candidates entering the pipeline**, not how they're evaluated. Local exploration directly addresses the mismatch.

### 0.4 What v18 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§7) — UNCHANGED.
- v17 step 05.5 cascade (FTS check + KCD pre-check + anti-R279) — UNCHANGED.
- v17 verdict labels (11 total) — UNCHANGED.
- v17 logs/known_collisions.json and logs/frontier_seeds.json — UNCHANGED structurally; KCD continues to grow via AFL.
- v17's Multi-Strategy Heavy-Tail (MSHT): **DEPRECATED at step 05 but preserved as a fallback**. When stale-anchor-drop leaves <3 active anchors, v18 falls back to v17 MSHT for the orphaned sampling budget.
- v17 frontier_seed citation requirement: **UNCHANGED**. Every v18 candidate (anchor-local OR fallback discovery) still must cite ≥1 primitive. Anchor-local candidates inherit their anchor's citation by default; the citation is overridable.
- The PASS criterion (10 signals) — UNCHANGED.

---

## 1. File chain (v17 + one v18 addition)

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
    05_anchor_assignment.json         ← NEW v18 (which anchor each pool candidate is local to)
    05_candidate_pool.json            (v17, unchanged structure; per-anchor attribution adds an `anchor_id` field)
    05_4_diversity_filter.json        (v14, unchanged)
    05_45_intra_cluster_diversification.json   (v15, unchanged)
    05_candidate.json                 (now includes anchor_id + local_exploration_distance)
    05_5_known_collision_check.json   (v17, unchanged)
    05_5_pattern_filter.json          (v12, unchanged)

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
logs/frontier_seeds.json         (v17; UNCHANGED)
logs/known_collisions.json       (v17; UNCHANGED structure; grows via v17 AFL)
logs/expert_path.json            ← NEW v18 (7 anchors bootstrap; updated post-epoch)
logs/memory_db.json              (UNCHANGED schema; v18 adds new fields per round)
logs/policy_state.json           (schema bumped to 1.8)
```

Per-epoch:
```
output/14_5_coverage_profile_E{N}.json   (v14)
output/stats_round_NNN.json              (v14+; new v18 sections)
```

---

## 2. Intervention — Local Heavy-Tail Around Expert Path (Swamy)

### 2.1 logs/expert_path.json

A persistent file listing INVESTIGATIVE_SURVIVING anchors. Each anchor has:
- `anchor_id` (e.g., `ANCHOR_R834`)
- `source_round` and `source_epoch`
- `slot` (architecture_tool_slot)
- `domain`
- `mechanism_signature` (stripped: domain × slot × mechanism family)
- `frontier_seed_citation` (if applicable; v17+ candidates only)
- `embedding_keys` (tokenized features for similarity computation)
- `epochs_since_yield` (rounds since this anchor's neighborhood produced a NEW INVESTIGATIVE_SURVIVING; 0 at bootstrap)
- `total_local_yield` (count of INVESTIGATIVE_SURVIVING in this anchor's neighborhood across all epochs)
- `status`: `active` | `stale` | `dropped`

Bootstrap content (7 entries from R834, R843, R863, R866, R883, R891, R895). See §2.6 for the exact JSON.

### 2.2 Step 05 generator rule (v18)

At step 05, the generator follows this order:

1. Read `logs/expert_path.json`. Compute `active_anchors = [a for a in entries if a.status == 'active']`.
2. **Budget allocation**: 100-pool slots are allocated as:
   - 14 candidates per active anchor (local neighborhood)
   - Remaining budget → "discovery" mode (anchor-free; uses v17 MSHT fallback Strategy C+D mix)
   - Example: 7 active anchors → 98 anchor-local + 2 discovery
3. **Local-neighborhood sampling**: For each active anchor `a`:
   - Generate 14 candidates that share `a.slot` (or a slot in the same architectural-class as `a.slot`).
   - Each candidate's `mechanism_signature` must be within embedding distance ε ≤ 0.6 of `a.mechanism_signature` (Jaccard on embedding_keys).
   - Each candidate must NOT match `a.mechanism_signature` exactly (i.e., must perturb at least one of: domain, math-vocabulary, sub-mechanism). The Jaccard floor is ε ≥ 0.15 to prevent trivial duplicates.
   - Each candidate inherits `a.frontier_seed_citation` by default; the prompt explicitly allows overrides to a related primitive.
   - The candidate's `anchor_id` field is set to `a.anchor_id`.
4. **Discovery fallback**: For the remaining budget (typically 2 candidates), use v17 MSHT Strategy C (frontier-primitive-direct) + Strategy D (collision-negation) at 50/50 split. These candidates have `anchor_id = null` and `is_discovery = true`.
5. **Strategy E preserved as PROVISIONAL**: If discovery budget > 0, 1 candidate may be Strategy E with `provisional = true` (same v17 contract).

The 100-pool now has each candidate tagged with its `anchor_id` (or `null` for discovery).

### 2.3 Embedding-radius ε definition

Reuse the v17 KCD Jaccard + skeleton-match metric (see `program_v17.md §3.2`). Embedding distance between candidate `c` and anchor `a`:

```
distance(c, a) = 1 - max(jaccard(c.embedding_keys, a.embedding_keys),
                         skeleton_match(c.stripped_skeleton, a.stripped_skeleton))
```

ε threshold: **0.6** (i.e., similarity ≥ 0.4).
- Lower bound ε = 0.15 (similarity ≤ 0.85) prevents trivial duplicates of the anchor.
- Upper bound ε = 0.6 (similarity ≥ 0.4) keeps candidates in the anchor's neighborhood.

Calibration rationale: v17 KCD uses similarity > 0.5 as collision threshold. v18 uses similarity ≥ 0.4 as anchor-neighborhood threshold (10% softer). This deliberately allows v18 to explore the 0.4-0.5 buffer zone — close-but-not-identical neighborhoods of the expert anchors.

### 2.4 Stale-anchor drop rule

After each epoch's audit_feedback_loop runs, compute per-anchor yield:

```python
for anchor in expert_path.entries:
    if anchor.status != 'active':
        continue
    new_INVESTIGATIVE_in_neighborhood = count(
        r for r in epoch_N.INVESTIGATIVE_SURVIVING
        if r.anchor_id == anchor.anchor_id
    )
    if new_INVESTIGATIVE_in_neighborhood > 0:
        anchor.epochs_since_yield = 0
        anchor.total_local_yield += new_INVESTIGATIVE_in_neighborhood
    else:
        anchor.epochs_since_yield += 1

    if anchor.epochs_since_yield >= 3:
        anchor.status = 'stale'   # drops out of active set; can be reactivated if external audit reverses
        anchor.dropped_at_epoch = epoch_N
```

**N=3** stale threshold: an anchor that produces 0 new INVESTIGATIVE_SURVIVING in 3 consecutive epochs is dropped from the active set. Rationale:
- Single-epoch zero may be sampling variance; not informative.
- Two-epoch zero suggests neighborhood thinning; suggestive.
- Three-epoch zero is decisive: the neighborhood is exhausted (either over-explored or never had density).

Dropped anchors remain in `expert_path.json` with `status = 'stale'` for audit history. They are NOT used to seed new candidates.

If the active anchor count drops below 3, v18 falls back to v17 MSHT for the entire 100-pool (discovery-only mode). This guard prevents the corpus from collapsing if all anchors stale out simultaneously.

### 2.5 Anchor-bootstrap special case for E37

E37 is the first v18 epoch. All 7 bootstrap anchors have `epochs_since_yield = 0` and `status = active`. The stale-drop rule does not fire in E37. From E38 onward, anchors that produced no INVESTIGATIVE_SURVIVING in E37 will increment `epochs_since_yield`.

### 2.6 logs/expert_path.json bootstrap content

```json
{
  "version": "1.0",
  "created": "2026-05-21T23:30:00Z",
  "created_by": "v18 init Phase 2 bootstrap",
  "description": "Persistent registry of INVESTIGATIVE_SURVIVING anchors. Step 05 (v18) generates ~14 candidates within embedding radius ε of each active anchor. Anchors stale-drop after N=3 epochs of zero local yield. Updated post-epoch by the v18 anchor_update procedure.",
  "stale_threshold_epochs": 3,
  "embedding_radius_upper": 0.6,
  "embedding_radius_lower": 0.15,
  "anchors_per_round_budget": 14,
  "fallback_to_v17_MSHT_when_active_count_below": 3,
  "entries": [
    {
      "anchor_id": "ANCHOR_R834",
      "source_round": 834,
      "source_epoch": 34,
      "program_version_at_origin": "v15",
      "slot": "S15",
      "domain": "category-theory",
      "mechanism_signature": "Bayes-categorical-posterior conformal critic head",
      "stripped_skeleton": "<rare-math-class> <S15-critic-architectural> modify-transformer",
      "frontier_seed_citation": null,
      "embedding_keys": ["Bayes", "categorical", "posterior", "conformal", "critic", "head", "S15", "category"],
      "epochs_since_yield": 0,
      "total_local_yield": 1,
      "status": "active",
      "rationale": "E34 v15 INVESTIGATIVE_CANDIDATE; v16-E35 step 14.6 retro confirmed (sim=0.51 vs arXiv 2511.07823 — SURVIVES). One of two pre-v17 S15 anchors."
    },
    {
      "anchor_id": "ANCHOR_R843",
      "source_round": 843,
      "source_epoch": 34,
      "program_version_at_origin": "v15",
      "slot": "S16",
      "domain": "free-probability",
      "mechanism_signature": "Free-cumulant token routing module",
      "stripped_skeleton": "<rare-math-class> <S16-token-routing-architectural> modify-transformer",
      "frontier_seed_citation": null,
      "embedding_keys": ["free", "cumulant", "token", "routing", "module", "S16", "free-probability"],
      "epochs_since_yield": 0,
      "total_local_yield": 1,
      "status": "active",
      "rationale": "E34 v15 INVESTIGATIVE_CANDIDATE; v16-E35 step 14.6 retro confirmed (sim=0.43 vs arXiv 2508.19012 — SURVIVES). One of three pre-v17 S16 anchors."
    },
    {
      "anchor_id": "ANCHOR_R863",
      "source_round": 863,
      "source_epoch": 35,
      "program_version_at_origin": "v16",
      "slot": "S15",
      "domain": "Hochschild-cohom",
      "mechanism_signature": "Hochschild-cochain critic head",
      "stripped_skeleton": "<rare-math-class> <S15-critic-architectural> modify-transformer",
      "frontier_seed_citation": null,
      "embedding_keys": ["Hochschild", "cochain", "critic", "head", "S15", "cohomology"],
      "epochs_since_yield": 0,
      "total_local_yield": 1,
      "status": "active",
      "rationale": "E35 v16 INVESTIGATIVE_CANDIDATE_SURVIVES (sim=0.41 vs arXiv n/a at step 14.6 SURVIVES)."
    },
    {
      "anchor_id": "ANCHOR_R866",
      "source_round": 866,
      "source_epoch": 35,
      "program_version_at_origin": "v16",
      "slot": "S16",
      "domain": "elimination-theory",
      "mechanism_signature": "Bezout-resultant token routing",
      "stripped_skeleton": "<rare-math-class> <S16-token-routing-architectural> modify-transformer",
      "frontier_seed_citation": null,
      "embedding_keys": ["Bezout", "resultant", "token", "routing", "S16", "elimination"],
      "epochs_since_yield": 0,
      "total_local_yield": 1,
      "status": "active",
      "rationale": "E35 v16 INVESTIGATIVE_CANDIDATE_SURVIVES (sim=0.39 at step 14.6 SURVIVES)."
    },
    {
      "anchor_id": "ANCHOR_R883",
      "source_round": 883,
      "source_epoch": 36,
      "program_version_at_origin": "v17",
      "slot": "S20",
      "domain": "test-time-training",
      "mechanism_signature": "Test-time-training inner-loop adapter",
      "stripped_skeleton": "<TTT-class> <S20-inference-time-architectural> modify-transformer",
      "frontier_seed_citation": ["YUSUN_TTT"],
      "embedding_keys": ["test-time", "training", "TTT", "inner-loop", "adapter", "S20", "inference-time", "per-instance"],
      "epochs_since_yield": 0,
      "total_local_yield": 1,
      "status": "active",
      "rationale": "E36 v17 Strategy C INVESTIGATIVE_CANDIDATE_SURVIVES (sim=0.55 vs arXiv 2410.08891). First v17-tagged anchor."
    },
    {
      "anchor_id": "ANCHOR_R891",
      "source_round": 891,
      "source_epoch": 36,
      "program_version_at_origin": "v17",
      "slot": "S14",
      "domain": "info-theory",
      "mechanism_signature": "Heavy-tail entropic training objective with entropy-reweighting",
      "stripped_skeleton": "<entropy-reweighting-class> <S14-training-objective-architectural> modify-transformer",
      "frontier_seed_citation": ["YUSUN_HEAVY_TAIL_ENTROPIC"],
      "embedding_keys": ["heavy-tail", "entropic", "entropy", "reweighting", "training", "objective", "S14", "info-theory"],
      "epochs_since_yield": 0,
      "total_local_yield": 1,
      "status": "active",
      "rationale": "E36 v17 Strategy C INVESTIGATIVE_CANDIDATE_SURVIVES (sim=0.45 vs arXiv 2406.19412). Second v17-tagged anchor."
    },
    {
      "anchor_id": "ANCHOR_R895",
      "source_round": 895,
      "source_epoch": 36,
      "program_version_at_origin": "v17",
      "slot": "S16",
      "domain": "complexity-theory",
      "mechanism_signature": "Polynomial-time-bounded token routing (NOT-Lie-NOT-equivariance-NOT-divergence-NOT-spectral)",
      "stripped_skeleton": "<complexity-class> <S16-token-routing-architectural> modify-transformer",
      "frontier_seed_citation": ["FOSTER_SHARPENING_VS_DISCOVERY"],
      "embedding_keys": ["polynomial-time", "complexity", "bounded", "routing", "token", "S16", "NOT-Lie", "NOT-equivariance"],
      "epochs_since_yield": 0,
      "total_local_yield": 1,
      "status": "active",
      "rationale": "E36 v17 Strategy D (regen from KCD_7CLUSTER first-attempt) INVESTIGATIVE_CANDIDATE_SURVIVES (sim=0.38 vs arXiv 2509.04123). Third v17-tagged anchor. Note shared slot S16 with ANCHOR_R843 and ANCHOR_R866; this is the densest single-slot region of the expert manifold."
    }
  ],
  "post_epoch_anchor_update_procedure_summary": "After each epoch's AFL runs, increment epochs_since_yield for any anchor with 0 new local INVESTIGATIVE_SURVIVING this epoch; reset to 0 for anchors with >=1 new yield; mark anchor as 'stale' (and inactive) when epochs_since_yield >= 3.",
  "bootstrap_source_note": "Bootstrapped from cumulative INVESTIGATIVE_SURVIVING list across E34-E36 epochs. Pre-v17 anchors (R834, R843, R863, R866) lack frontier_seed_citation field; v17+ anchors (R883, R891, R895) have explicit citation. v18 prompt template adapts: anchor-local candidates inherit citation if present, else cite Strategy C/D primitive consistent with anchor's mechanism signature."
}
```

### 2.7 Step 05 v18 generator pseudo-code

```python
def step_05_v18(round_num, coverage_profile, known_collisions, frontier_seeds, expert_path):
    active_anchors = [a for a in expert_path.entries if a.status == "active"]

    if len(active_anchors) < expert_path.fallback_to_v17_MSHT_when_active_count_below:
        # Fallback: pure v17 MSHT mode (no local exploration)
        return step_05_v17(round_num, coverage_profile, known_collisions, frontier_seeds)

    pool = []
    per_anchor_budget = expert_path.anchors_per_round_budget  # 14

    for anchor in active_anchors:
        candidates = sample_local(
            anchor,
            n=per_anchor_budget,
            radius_upper=expert_path.embedding_radius_upper,    # 0.6
            radius_lower=expert_path.embedding_radius_lower,    # 0.15
            citation_inherit=anchor.frontier_seed_citation,
            allow_citation_override=True
        )
        for c in candidates:
            c.anchor_id = anchor.anchor_id
            c.is_discovery = False
            c.local_exploration_distance = embedding_distance(c, anchor)
            pool.append(c)

    # Discovery budget: 100 - (n_anchors × 14)
    discovery_budget = 100 - len(pool)
    if discovery_budget > 0:
        # Use v17 MSHT Strategy C + D + 1 Strategy E for the discovery slot
        discovery_candidates = sample_discovery_mix(
            discovery_budget,
            coverage_profile,
            known_collisions,
            frontier_seeds,
            strategy_mix={"C": 0.45, "D": 0.45, "E": 0.10}
        )
        for c in discovery_candidates:
            c.anchor_id = None
            c.is_discovery = True
            c.local_exploration_distance = None
            pool.append(c)

    write("05_candidate_pool.json", pool)
    write("05_anchor_assignment.json", {
        "active_anchors_used": [a.anchor_id for a in active_anchors],
        "active_anchor_count": len(active_anchors),
        "per_anchor_budget": per_anchor_budget,
        "anchor_local_count": len(pool) - discovery_budget,
        "discovery_count": discovery_budget,
        "fallback_to_v17_MSHT": False
    })
    return pool  # length 100
```

### 2.8 Step 05.4 k-means filter (v14, UNCHANGED)

The 100-pool with anchor attribution goes through k-means clustering (k=25). The k-means selects 25 representatives. **Anchor attribution is preserved in the 25.** Per the FORBIDDEN-TO-MODIFY constraint on step 05.4, the k-means itself is unchanged — but the input is now anchor-stratified instead of strategy-stratified.

### 2.9 05_candidate_pool.json schema (v18)

```json
{
  "round": "NNN",
  "epoch": N,
  "v17_index": true,
  "v18_index": true,
  "step_05_mode": "v18_local_exploration",
  "active_anchors_used": ["ANCHOR_R834", "ANCHOR_R843", "ANCHOR_R863", "ANCHOR_R866", "ANCHOR_R883", "ANCHOR_R891", "ANCHOR_R895"],
  "active_anchor_count": 7,
  "per_anchor_budget": 14,
  "anchor_local_count": 98,
  "discovery_count": 2,
  "candidates": [
    {
      "candidate_id": "c001",
      "anchor_id": "ANCHOR_R834",
      "is_discovery": false,
      "local_exploration_distance": 0.42,
      "specific_mechanism": "...",
      "llm_application": "...",
      "frontier_seed_citation": ["(inherited from anchor; v18 may override)"],
      "architecture_tool_slot": "S15",
      "content_words": [...],
      "..."
    }
    // ... 99 more
  ]
}
```

### 2.10 Step 05_candidate.json schema additions (v18)

The selected candidate per round records:
```json
{
  ... (all v1-v17 fields) ...,
  "v18_index": true,
  "anchor_id": "ANCHOR_R834" | null,
  "is_discovery": false | true,
  "local_exploration_distance": 0.42 | null,
  "anchor_local_count_in_pool": 14,
  "v18_step_05_mode": "anchor_local" | "discovery" | "v17_fallback"
}
```

---

## 3. Step 05.5 cascade (v17, UNCHANGED)

The step 05.5 cascade is unchanged from v17:
1. FTS check (frontier_seed_citation required and valid).
2. KCD check (similarity ≤ 0.5 against logs/known_collisions.json entries).
3. anti-R279 check (architectural-topology required).

v18 candidates with `anchor_id != null` still must pass all three. They are NOT exempt. The local-exploration prompt is responsible for generating candidates that satisfy these checks; if a candidate fails, the v12 regeneration loop fires (up to 3 retries).

### 3.1 v18 interaction with KCD

Because v18 candidates cluster near INVESTIGATIVE_SURVIVING anchors, they MAY be closer to KCD entries than v17's broader distribution. The KCD threshold (0.5) is fixed (per v17 anti-cheating commitments §12). v18 expects the KCD rejection rate to **stay low** (the 7 anchors are all post-KCD-cleared by definition; their neighborhoods should mostly be too). If KCD rejection rises above v17's 0.08 baseline, this is a v18 warning signal that local-exploration is over-shooting into collision space.

### 3.2 v18 interaction with FTS

The frontier_seed_citation requirement is preserved. For anchor-local candidates with an anchor that has an existing citation, the candidate inherits the citation by default (saves prompt work). The prompt may override the citation to a related primitive (e.g., a YUSUN_TTT anchor's neighborhood candidate may cite YUSUN_HEAVY_TAIL_ENTROPIC if the neighborhood drifts toward entropic-loss variants of TTT).

For pre-v17 anchors (R834, R843, R863, R866) with `frontier_seed_citation = null`, the v18 prompt assigns a default citation:
- ANCHOR_R834 (S15 critic) → GAO_Q_RUBRIC (Q1=new-learnable-module)
- ANCHOR_R843 (S16 routing) → FOSTER_REP_DIVERSE_SAMPLING (routing-as-diversity)
- ANCHOR_R863 (S15 critic) → GAO_Q_RUBRIC
- ANCHOR_R866 (S16 routing) → FOSTER_REP_DIVERSE_SAMPLING

---

## 4. Post-epoch anchor update procedure

After each epoch's 25 rounds complete and step 14.6 has fired on all INVESTIGATIVE_CANDIDATEs, AND AFTER the v17 AFL has run:

```python
def post_epoch_anchor_update(epoch_N, expert_path, this_epoch_INVESTIGATIVE_SURVIVING):
    new_anchors_added = []

    # Step 1: Increment epochs_since_yield; reset for anchors with local yield
    for anchor in expert_path.entries:
        if anchor.status != 'active':
            continue
        new_yield = count(
            r for r in this_epoch_INVESTIGATIVE_SURVIVING
            if r.anchor_id == anchor.anchor_id
        )
        if new_yield > 0:
            anchor.epochs_since_yield = 0
            anchor.total_local_yield += new_yield
        else:
            anchor.epochs_since_yield += 1
            if anchor.epochs_since_yield >= expert_path.stale_threshold_epochs:
                anchor.status = 'stale'
                anchor.dropped_at_epoch = epoch_N
                anchor.status_history.append({"action": "stale_drop", "epoch": epoch_N})

    # Step 2: Add any new INVESTIGATIVE_SURVIVING from discovery candidates as new anchors
    for r in this_epoch_INVESTIGATIVE_SURVIVING:
        if r.anchor_id is None and r.is_discovery:
            new_anchor = build_anchor_from_round(r, epoch_N)
            expert_path.entries.append(new_anchor)
            new_anchors_added.append(new_anchor.anchor_id)

    # Step 3: Add any new INVESTIGATIVE_SURVIVING from anchor-local candidates as auxiliary anchors
    # (these inherit the parent anchor's neighborhood but extend the manifold structure)
    for r in this_epoch_INVESTIGATIVE_SURVIVING:
        if r.anchor_id is not None and r.local_exploration_distance > 0.4:
            # Far-edge of an anchor's neighborhood; promote to new sub-anchor
            new_anchor = build_anchor_from_round(r, epoch_N, parent=r.anchor_id)
            expert_path.entries.append(new_anchor)
            new_anchors_added.append(new_anchor.anchor_id)

    expert_path.last_anchor_update = {
        "epoch": epoch_N,
        "timestamp": now(),
        "active_count_before": pre_count,
        "active_count_after": post_count,
        "newly_stale": [a.anchor_id for a in newly_stale],
        "newly_added": new_anchors_added
    }
    write("logs/expert_path.json", expert_path)
```

This procedure runs **after** v17 AFL (which updates KCD) and **before** step 14.5 coverage profile write.

### 4.1 The 3 update events per epoch

After each epoch, the expert_path.json file may receive 3 kinds of updates:
1. **Stale drop**: anchors with 3+ epochs of zero local yield become `status='stale'`.
2. **Discovery promotion**: NEW INVESTIGATIVE_SURVIVING from `is_discovery=true` candidates become new top-level anchors.
3. **Sub-anchor promotion**: anchor-local INVESTIGATIVE_SURVIVING with `local_exploration_distance > 0.4` (far-edge of an anchor's neighborhood) become sub-anchors with `parent_anchor_id` reference, extending the manifold structure.

---

## 5. v18 metric definitions

### 5.1 local_exploration_yield_rate

Per-anchor and overall:
```
local_exploration_yield_rate_per_anchor_a =
    INVESTIGATIVE_SURVIVING in a's neighborhood this epoch /
    candidates generated in a's neighborhood this epoch
  = INVESTIGATIVE_SURVIVING / 14   (in the budget-14 case)

mean_local_exploration_yield_rate_E{N} =
    sum over all active anchors / n_active_anchors
```

A high yield rate (≥ 0.30) means local exploration is dense. A low rate (< 0.10) suggests the anchor's neighborhood is exhausted.

### 5.2 active_anchor_count

Number of `status='active'` anchors at epoch start.

### 5.3 stale_anchor_drop_count

Number of anchors transitioning from `active` to `stale` during this epoch.

### 5.4 discovery_yield_rate

INVESTIGATIVE_SURVIVING from `is_discovery=true` candidates / total discovery candidates.

### 5.5 anchor_attribution_of_INVESTIGATIVE_SURVIVING

```
{
  "ANCHOR_R834": 0 | 1 | 2 | ...,
  "ANCHOR_R843": ...,
  ...,
  "discovery": 0 | 1 | ...,
  "sub_anchor_from_R895": ...
}
```

### 5.6 v18 score formula additions

```
score_v18 = score_v17 (all v17 terms, UNCHANGED)
          + (active_anchor_count / 7 × 2)             ← NEW v18 (rewards keeping the expert manifold active)
          + (mean_local_exploration_yield_rate × 8)   ← NEW v18 (the headline metric; rewards per-anchor yield density)
          + (sub_anchors_promoted_count × 2)          ← NEW v18 (rewards manifold extension)
          - (stale_anchor_drop_count × 1)             ← NEW v18 (penalizes over-exploration; keeps drift honest)
          + (discovery_yield_rate × 4)                ← NEW v18 (preserves v17's discovery-mode incentive)
```

The +8 multiplier on `mean_local_exploration_yield_rate` is the strongest v18 incentive (above v17's +6 for per_strategy_diversity). It dominates the formula by design — v18's whole thesis is that this metric is the bottleneck.

The penalty on stale_anchor_drop_count is intentional: dropping anchors is honest (avoids the rare-math-super-mode trap), but it also signals the corpus is losing the manifold; the score should reflect the loss.

### 5.7 Score formula constraints

- `frontier_seed_citation_rate × 2` is preserved (v17 term).
- `selected_at_step_05_4_from_strategy_BCDE / 25 × 4` becomes `(anchor_local_count + discovery_count) / 25 × 4` under v18 (i.e., anything generated under v18's distinct distribution counts; v17 strategy-tagging is no longer applicable since all anchor-local candidates have effectively replaced strategy-tagging). **In practice, anchor_local_count + discovery_count = 25 always under v18; this term equals 4.0.**
- `REJECTED_KNOWN_COLLISION_count × 1` is preserved.
- `per_strategy_attack_rebuttal_diversity × 2` is preserved but the strategies are now {anchor-A, anchor-B, ..., discovery} rather than {A, B, C, D, E}. **In v18, the per-strategy metric is replaced by per-anchor metric**: `per_anchor_attack_rebuttal_diversity × 2`.
- `Strategy_E_provisional_INVESTIGATIVE × 1` is preserved (still penalizes Strategy E provisional INVESTIGATIVE inside discovery mode).

---

## 6. Loop control (v18)

```
read logs/policy_state.json
read logs/architecture_tools.json
read logs/frontier_seeds.json
read logs/known_collisions.json
read logs/expert_path.json                ← NEW v18
read prior epoch coverage profile
write logs/policy_state.json with current_epoch += 1, schema 1.8

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute
    execute step 04.5

    # NEW v18 step 05: local heavy-tail around expert path
    active_anchors = [a for a in expert_path.entries if a.status == "active"]
    if len(active_anchors) < 3:
        pool = step_05_v17(...)  # fallback to v17 MSHT
        write 05_anchor_assignment.json with mode="v17_fallback"
    else:
        pool = step_05_v18(active_anchors, ...)
        write 05_anchor_assignment.json with mode="anchor_local + discovery"
    write 05_candidate_pool.json

    cluster_assign = kmeans(pool, k=25, seed=epoch)        # v14 step 05.4 UNCHANGED
    selected_25 = candidates near each cluster center
    write 05_4_diversity_filter.json

    compute_pairwise_niche_distance_matrix(selected_25)    # v15 step 05.45 UNCHANGED
    near_duplicate_pairs = pairs with distance < 0.5
    for (i,j) in near_duplicate_pairs:
        keep one; replace the other from 100-pool (preserves anchor_id)
    write 05_45_intra_cluster_diversification.json

    for candidate in selected_25_post_replacement:
        verdict = step_05_5_v17(candidate)    # v17 cascade UNCHANGED
        if verdict.startswith("REJECTED_"):
            regen_loop(...)
        elif verdict == "PASS":
            PRIMARY = candidate
            break
    if PRIMARY == None:
        PRIMARY = highest slot-novelty within active-anchor neighborhood
        run step 05.5 regeneration

    write 05_candidate.json (now includes anchor_id + is_discovery + local_exploration_distance)
    write 05_5_known_collision_check.json
    write 05_5_pattern_filter.json

    execute step 06, 06.5, 06.7, 07
    execute step 08, 09
    execute step 10
    execute step 11, 11.5, 12
    execute step 13, 13.5
    execute step 14
    execute step 14.6 (when step 14 INVESTIGATIVE_CANDIDATE)

    compute v18_verdict (= v17_verdict; UNCHANGED)
    update memory_db.json round entry with v18 fields

    if round_num % 25 == 0:
        write output/stats_round_NNN.json
        compute coverage_profile (v14 step 14.5)
        write output/14_5_coverage_profile_E{N}.json
        compute v18 per-anchor metrics
        run audit_feedback_loop()           ← v17 AFL UNCHANGED
        update logs/known_collisions.json with new entries
        run post_epoch_anchor_update()       ← NEW v18
        update logs/expert_path.json
        update logs/policy_state.json
```

---

## 7. v18 verdict synthesis

```
v18_verdict =
    PASS                              (UNCHANGED — same 10 signals; never observed at N=996)
    PASS_WITH_EMPIRICAL_CAVEAT        (UNCHANGED — v10)
    FAIL_EMPIRICAL_ATTACK             (UNCHANGED — v11)
    REJECTED_R279_PATTERN             (UNCHANGED — v12)
    REJECTED_KNOWN_COLLISION          (UNCHANGED — v17)
    REJECTED_NO_FRONTIER_SEED         (UNCHANGED — v17)
    INVESTIGATIVE_CANDIDATE           (UNCHANGED — v13; step 14 FIRED + step 14.6 survives)
    EXTERNAL_COLLISION                (UNCHANGED — v16)
    FAIL_ADVERSARIAL                  (UNCHANGED)
    FAIL_GAP_REAL_LOGGED              (UNCHANGED)
    FAIL                              otherwise
```

v18 adds NO new verdict labels. The 11 v17 labels are preserved verbatim. v18's contribution is at the **generator distribution** layer; verdict labels are determined by detector steps that are FROZEN.

The PASS criterion remains 10 signals (UNCHANGED).

---

## 8. Stats schema additions in v18

`output/stats_round_NNN.json` adds:

```json
{
  ... (all v1-v17 fields) ...,
  "v18_local_exploration_metrics": {
    "step_05_mode_distribution_25": {
      "anchor_local": 0,
      "discovery": 0,
      "v17_fallback": 0
    },
    "active_anchor_count_at_epoch_start": 7,
    "active_anchor_count_at_epoch_end": 0,
    "stale_anchor_drop_count": 0,
    "stale_anchor_dropped_list": [],
    "sub_anchors_promoted_count": 0,
    "sub_anchors_promoted_list": [],
    "discovery_yield_rate": 0.0,
    "discovery_candidates_count_E{N}": 0,
    "discovery_INVESTIGATIVE_SURVIVING_count_E{N}": 0,
    "anchor_attribution_of_INVESTIGATIVE_SURVIVING": {},
    "mean_local_exploration_yield_rate": 0.0,
    "per_anchor_yield_rate": {
      "ANCHOR_R834": 0.0,
      "ANCHOR_R843": 0.0,
      "ANCHOR_R863": 0.0,
      "ANCHOR_R866": 0.0,
      "ANCHOR_R883": 0.0,
      "ANCHOR_R891": 0.0,
      "ANCHOR_R895": 0.0
    },
    "per_anchor_local_count_selected_25": {},
    "per_anchor_INVESTIGATIVE_SURVIVING_count": {},
    "per_anchor_attack_rebuttal_diversity": 0
  },
  "v18_expert_path_state": {
    "expert_path_size_at_epoch_start": 7,
    "expert_path_size_at_epoch_end": 0,
    "expert_path_growth_rate_E{N}": 0.0
  }
}
```

Existing v17 metrics (`v17_MSHT_metrics`, `v17_FTS_metrics`, `v17_KCD_metrics`, `v17_AFL_metrics`) are preserved. The `v17_per_strategy_metrics` block becomes a `v17_legacy_per_strategy_metrics` block that records strategy attribution mapped from anchor attribution (each anchor maps to a virtual strategy based on whether the anchor's parent epoch used Strategy A/C/D).

---

## 9. ★ FORBIDDEN-TO-MODIFY zones (verbatim from v5...v17 + v18 explicit)

### 9.1 v17's FORBIDDEN list — UNCHANGED
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
- PASS criterion (10 signals)

### 9.2 v18 modifies ONLY:
- **Step 05 distribution**: from v17's uniform-5-strategy to v18's anchor-local-heavy-tail (with v17 fallback when active_anchor_count < 3).
- **Post-epoch anchor update**: NEW v18 procedure that updates `logs/expert_path.json`.

### 9.3 v17's components — UNCHANGED
- FTS check at step 05.5
- KCD pre-check at step 05.5
- AFL post-epoch update to known_collisions.json
- Strategy E PROVISIONAL labeling (preserved in discovery mode)

---

## 10. Anti-cheating commitments (v18 additions on top of v17)

The v3...v17 instructions stand. v18 adds:

- **Anchor honesty.** An anchor must be a verified INVESTIGATIVE_SURVIVING round (step 14 FIRED + step 14.6 SURVIVES). Anchors cannot be added from manual inspection or speculation. The 7-anchor bootstrap is enumerated from corpus history.
- **Embedding radius immutability mid-epoch.** ε = 0.6 upper, ε = 0.15 lower fixed for E37 and beyond (until v19).
- **Stale threshold immutability mid-epoch.** N=3 epochs fixed for E37 and beyond.
- **Anchor attribution immutability.** Once a candidate is generated under anchor X, `anchor_id` is fixed. Cannot be re-attributed based on outcome.
- **Discovery-mode budget cap.** Discovery candidates may not exceed 20% of the 100-pool. At 7 active anchors, the cap is 2-3 candidates; this is well below 20% (~20).
- **expert_path.json write-protected mid-epoch.** Only the post-epoch anchor_update procedure writes to logs/expert_path.json. Mid-epoch writes are forbidden.

---

## 11. Inherited history (v1 → v18)

- **v1-v17**: see prior program_vN.md files.
- **v18** (this file): v17 base + Local Heavy-Tail Around Expert Path (Swamy framework A). **R901-R925 under v18 in E37.**

---

## 12. What v18 does NOT promise

v18 does NOT promise more substantive PASS verdicts. The 996-round saturation result (0 confirmed substantive PASS, p ≈ 0.0000449 at N=996) is structural. v18 acknowledges the same Phase 1 diagnosis: detector layers cannot raise PASS rate. v18 promises a different shift: **concentrate generator mass on the empirical INVESTIGATIVE_SURVIVING manifold**, not raise the PASS-criterion ceiling.

What v18 promises:
- **Concentrated mass on the 7-anchor manifold.** ~98 of 100 pool candidates within ε of an anchor.
- **Per-anchor yield rate tracking.** Each of 7 anchors gets a `local_exploration_yield_rate` per epoch.
- **Stale-anchor drop mechanism.** Anchors that don't produce in 3 epochs drop out automatically.
- **Sub-anchor promotion.** Anchor-local INVESTIGATIVE_SURVIVING with high distance become sub-anchors, extending the manifold.
- **Discovery-mode preservation.** 2-3 of 100 pool candidates per round are anchor-free, preserving v17's discovery channel.

v18 does NOT claim to solve the distribution-pinning problem. It claims to **localize** the generator distribution to the empirical expert manifold, with self-correction.

---

## 13. Honest deviation policy (for E37 execution)

Same as v14/v15/v16/v17 (max 5 synthesized Agent spawns per epoch). v18's local-exploration prompts are executed in main-context-direct mode; the anchor-local sampling is simulated honestly by tagging each pool candidate with its `anchor_id` and ensuring slot/citation inheritance from the anchor. Step 05.5 cascade is mechanical (Jaccard + skeleton match) — no Agent spawn needed. Post-epoch anchor_update is main-context-direct.

---

## 14. Phase 4 reporting requirements (for output/epoch37_comparison.md)

After E37 completes, the comparison document must record:
1. **active_anchor_count_at_E37_start**: 7 (bootstrap).
2. **per_anchor_local_count_in_25_selected**: distribution across the 7 anchors after k-means + ICD.
3. **discovery_count_in_25**: how many of 25 were discovery (target: 0-3).
4. **per_anchor_INVESTIGATIVE_SURVIVING_count_E37**: which anchors produced INVESTIGATIVE_SURVIVING.
5. **mean_local_exploration_yield_rate_E37**: headline metric.
6. **discovery_yield_rate_E37**: discovery-mode yield.
7. **stale_anchor_drop_count_E37**: 0 (first v18 epoch; stale-drop cannot fire until E38+).
8. **sub_anchors_promoted_count_E37**: new sub-anchors with distance > 0.4.
9. **active_anchor_count_at_E37_end**: 7 (bootstrap) + new discoveries + new sub-anchors.
10. **v18 score with new terms**.
11. **v18 vs v17 score delta**: expected +5 to +12 (depending on yield).
12. **Cumulative N_verified after E37 = 1021**.
13. **p(no PASS | 1% H₀) at N=1021 ≈ 0.0000366**.
14. **Honest deviation count**: synthesized agent spawns this epoch (target: <5).
15. **collision_addition_rate_E37** (via v17 AFL; unchanged measurement).
16. **KCD database size at E37 start vs end** (continues from v17).

This is the v18 contribution: making the generator distribution **anchor-conditioned and yield-self-correcting** — concentrating empirical mass on the INVESTIGATIVE_SURVIVING expert manifold.

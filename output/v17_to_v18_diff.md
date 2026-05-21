# v17 → v18 Diff (Phase 2 of v18 task)

**Author:** Claude (Opus 4.7), branch `claude/build-expert-path-vOvzh`.
**Date:** 2026-05-21.
**Purpose:** Document the structural diff from `program_v17.md` to `program_v18.md`, with rationale for choosing Swamy's local-exploration framework (A) over learned-verifier (B) and self-play (C), forbidden-zone preservation audit, and v18 implementation summary.

---

## 0. v18 changeset summary (one paragraph)

v18 is the first version since v14 to **change the shape** of step 05's prior. Where v17 introduced **four** generator-side fixes (FTS, KCD, MSHT, AFL) at once, v18 introduces **one**: Swamy's local-exploration framework. The diagnosed bottleneck (see `output/v17_limitation_analysis.md`) is that v17's 5-strategy heavy-tail samples **uniformly** over a non-uniform yield landscape — the 7 INVESTIGATIVE_SURVIVING anchors (R834, R843, R863, R866, R883, R891, R895) occupy <5% of v17's sampling support but ~100% of its positive outcomes. v18 replaces v17's uniform 5-strategy mix with **anchor-local sampling**: at step 05, ~14 candidates are generated within embedding radius ε of each of the 7 anchors (~98 total), plus 2 anchor-free "discovery" candidates preserving v17's discovery channel. A `local_exploration_yield_rate` per anchor tracks neighborhood productivity; anchors that produce 0 INVESTIGATIVE_SURVIVING in N=3 consecutive epochs drop to `status='stale'`. Anchor-local INVESTIGATIVE_SURVIVING with distance > 0.4 become sub-anchors, extending the manifold. The detector chain (step 06-14.6) is UNCHANGED. v17's FTS citation requirement, KCD pre-check, and AFL are all preserved. v18 adds NO new verdict labels (the 11 v17 labels are sufficient). The single change is at step 05's prior, with a self-correcting stale-drop mechanism to avoid the rare-math-super-mode trap diagnosed in v16.

---

## 1. Why ONE upgrade, not four

v17's task description specified FOUR co-functional fixes because the detector chain was being expanded and the four fixes were co-dependent (KCD's negation list is consumed by Strategy D; AFL maintains the database that KCD reads; FTS provides the citations that Strategies C/D require). v18's task is different: identify the **single** bottleneck remaining after v17's full deployment, and apply ONE upgrade.

The bottleneck after v17:
- Detector chain is at ~100% retrospective accuracy (v16 step 14.6).
- step 13.5 attack rebuttal rate is 0.80 in E36, **1.0 for Strategy C/D**.
- The 7-anchor expert manifold is empirically verified (each of the 7 passed all four detector axes).
- v17's step 05 distribution does NOT condition on this manifold; the 5-strategy uniform mix spreads probability across slots, citations, and architectural classes that have never produced INVESTIGATIVE_SURVIVING.

The single upgrade: **concentrate sampling on the empirical manifold**. This is Swamy's local-exploration framework. No detector change. No new verdict label. No new persistent database except `logs/expert_path.json` (which is *generated*, not authored — the 7 entries come from corpus history).

---

## 2. Swamy framework selection (Phase 1 → Phase 2 link)

Per `output/v17_limitation_analysis.md` §3-4:

| Swamy framework | Targets v17 bottleneck? | Forbidden-zone risk | Expected ΔINVESTIGATIVE_SURVIVING | v18 choice |
|---|:---:|:---:|---:|:---:|
| A: Local heavy-tail around expert path | **YES** — directly addresses uniform-vs-non-uniform yield mismatch | NO (modifies only step 05) | +2 to +5 | **CHOSEN** |
| B: Learned verifier | NO — step 14.6 already at 100% retro accuracy; training data too small | LOW | +0 to +1 | rejected |
| C: Self-play | NO — step 13.5 rebuttal rate is 1.0 for C/D; fabricates rebuttals | HIGH (corpus corruption) | +0 to +1, with false-positive risk | rejected |

**Choice: A (local heavy-tail around expert path)**. The decision is empirical: only framework A's mechanism (concentrate sampling on the manifold of audited successes) matches the diagnosed v17 bottleneck (uniform-vs-non-uniform sampling distribution). Frameworks B and C target detector-chain components that are already at ceiling.

---

## 3. New artifacts in v18

### 3.1 Persistent files

| Artifact | Location | Created by | Lifecycle | Modified by |
|---|---|---|---|---|
| `logs/expert_path.json` | persistent | v18 init Phase 2 | one-time bootstrap; updates post-epoch | post-epoch anchor_update |

### 3.2 Per-round files

| Artifact | Location | Created by | Lifecycle |
|---|---|---|---|
| `rounds/round_NNN/05_anchor_assignment.json` | per-round | step 05 v18 | NEW v18 (records active anchors used + per-anchor budget) |

### 3.3 Per-round schema additions

The existing `05_candidate.json` and `05_candidate_pool.json` add three v18 fields:
- `anchor_id`: which anchor this candidate is local to (`null` if discovery)
- `is_discovery`: bool; true if anchor-free
- `local_exploration_distance`: float ∈ [0.15, 0.6]; null if discovery

### 3.4 Stats schema additions

| Field group | Schema location | Type |
|---|---|---|
| `v18_local_exploration_metrics` | `output/stats_round_NNN.json` | object |
| `v18_expert_path_state` | `output/stats_round_NNN.json` | object |
| per_anchor_yield_rate | per-anchor | float |
| per_anchor_INVESTIGATIVE_SURVIVING_count | per-anchor | int |

---

## 4. Step-by-step diff vs program_v17.md

### Step 01-04 — UNCHANGED

### Step 04.5 (v3 memory_check) — UNCHANGED

### Step 05 — **MODIFIED v18 (Local Heavy-Tail Around Expert Path)**

#### v17 (current):
- Generate 100 candidates across 5 strategies (A/B/C/D/E × 20).
- Each candidate has `strategy_tag` and `frontier_seed_citation`.
- Write `05_candidate_pool.json`.

#### v18 (new):
- Read `logs/expert_path.json` (NEW). Compute `active_anchors`.
- **If active_anchor_count ≥ 3**:
  - Generate 14 candidates per active anchor within embedding radius ε ∈ [0.15, 0.6].
  - Generate 2-3 discovery candidates (anchor-free, Strategy C/D/E mix from v17).
  - Each candidate has `anchor_id` (or `null`), `is_discovery`, `local_exploration_distance`.
- **If active_anchor_count < 3**: fallback to v17 MSHT for full 100-pool.
- Write `05_candidate_pool.json` (with anchor attribution) + `05_anchor_assignment.json` (NEW).

#### Forbidden zone audit:
- v17 100-pool size = 100 → v18 = 100 (UNCHANGED)
- v14 step 05.4 k-means input = 100 candidates → v18 input = 100 candidates with anchor attribution (k-means logic UNCHANGED; input is anchor-stratified instead of strategy-stratified)
- v14 slot universe = 20 slots → v18 = 20 slots (UNCHANGED)
- v14 coverage-bias rule → applied within discovery mode only (anchor-local candidates already have slot determined by anchor; coverage-bias does not apply to them)

### Step 05.4 (v14 k-means filter) — UNCHANGED

The k-means input is now anchor-attributed instead of strategy-attributed. The k-means logic itself does not change; it still clusters 100 candidates into 25 using Claude's embedding. The 25 selected representatives will be a mix of anchor-local (most) and discovery (few).

### Step 05.45 (v15 ICD) — UNCHANGED

Pairwise intra-cluster diversification with threshold 0.5. Near-duplicate pairs are replaced from the 100-pool; replacement preserves `anchor_id`.

### Step 05.5 (v17 cascade) — UNCHANGED

The cascade order is unchanged:
1. FTS check (frontier_seed_citation required) — anchor-local candidates inherit citation from anchor.
2. KCD pre-check (similarity ≤ 0.5 against `logs/known_collisions.json`) — UNCHANGED.
3. anti-R279 check (architectural-topology required) — UNCHANGED.

v18 adds NO new step 05.5 reject paths. The cascade is identical to v17.

### Steps 06-14.6 — ALL UNCHANGED (FORBIDDEN ZONES)

### Post-epoch — **EXTENDED v18 (anchor_update procedure)**

v17 ran AFL post-epoch to update `logs/known_collisions.json`. v18 adds a SECOND post-epoch procedure: `post_epoch_anchor_update`. This runs AFTER AFL and BEFORE step 14.5 coverage profile write.

```python
# v17 AFL runs first (UNCHANGED)
audit_feedback_loop(epoch_N)

# v18 NEW: post_epoch_anchor_update
expert_path = read("logs/expert_path.json")
for anchor in expert_path.entries:
    if anchor.status == 'active':
        new_yield = count_INVESTIGATIVE_SURVIVING_in_anchor_neighborhood(anchor, epoch_N)
        if new_yield > 0:
            anchor.epochs_since_yield = 0
            anchor.total_local_yield += new_yield
        else:
            anchor.epochs_since_yield += 1
            if anchor.epochs_since_yield >= 3:
                anchor.status = 'stale'

# Promote discovery INVESTIGATIVE_SURVIVING to new top-level anchors
for r in epoch_N.INVESTIGATIVE_SURVIVING:
    if r.is_discovery:
        expert_path.entries.append(build_anchor_from_round(r))

# Promote far-edge anchor-local INVESTIGATIVE_SURVIVING to sub-anchors
for r in epoch_N.INVESTIGATIVE_SURVIVING:
    if r.anchor_id is not None and r.local_exploration_distance > 0.4:
        expert_path.entries.append(build_sub_anchor(r, parent=r.anchor_id))

write("logs/expert_path.json", expert_path)
```

---

## 5. Forbidden-zone preservation audit (verbatim from v17, extended for v18)

### 5.1 v17's FORBIDDEN list — UNCHANGED IN v18:
- ✅ Step 06 web_search
- ✅ Step 07 keyword threshold ≥ 2
- ✅ Step 10 mechanical verdict
- ✅ Step 12 tree-stream
- ✅ Step 13 spec format
- ✅ Step 13.5 attack format
- ✅ Step 14 cross-step coherence
- ✅ Step 14.5 coverage profile
- ✅ Step 14.6 external collision detection
- ✅ Step 05.4 k-means diversity filter
- ✅ Step 05.45 intra-cluster diversification
- ✅ Step 05.5 anti-R279 filter
- ✅ PASS criterion (10 signals)

### 5.2 v18 modifies ONLY:
- Step 05 prior distribution (from v17 uniform-5-strategy to v18 anchor-local-heavy-tail with discovery)
- Post-epoch anchor_update procedure (NEW)
- expert_path.json file (NEW)

### 5.3 No verdict label change:
v18 reuses v17's 11 verdict labels. No additions.

### 5.4 No detector logic change:
- Step 13 spec generation: still chooses top-3 mechanical-PASS proximity rounds.
- Step 13.5 attack format: still A1 (variant_equivalence), A2 (small_magnitude_collapse), A3 (functional_equivalence), A4 (permutation_invariance).
- Step 14 cross-step coherence: still fires on step 10 FAIL + step 13.5 post_attack=true.
- Step 14.6 external collision: still uses 4-axis rubric (mechanism class / architectural role / mechanism alignment / transformer context).

---

## 6. Why v18 expects to outperform v17

### 6.1 Direct yield concentration

v17 spreads 100 candidates across 5 strategies × 20 slots × 9 citations ≈ uniformly. The 7-anchor manifold covers slots {S14, S15, S16, S20} (4/20 = 20% of slot space), 3 specific citations (3/9 = 33% of citation space), and 4 architectural sub-modes. The joint coverage of the manifold is approximately 20% × 33% × ~25% (sub-mode density) ≈ 1.7% of v17's sampling support.

v17's expected yield from this manifold: 100 candidates × 1.7% × ~70% conversion ≈ 1.2 INVESTIGATIVE_SURVIVING per round on average.

E36 actual: 3 INVESTIGATIVE_SURVIVING. Statistical noise aside, this is consistent with the theoretical 1.2 × 25 / 25 = 1.2 per epoch average (E36 happened to be a positive-tail epoch with 3, vs the prior epochs E34/E35 with 2 each).

v18 concentrates 98 of 100 candidates IN the manifold. Expected yield: 98 × 70% × (some neighborhood-dilution factor 0.3-0.5) = 20-34 INVESTIGATIVE_SURVIVING per round. After k-means filtering to 25 representatives, expected INVESTIGATIVE_SURVIVING ~ 5-8 per epoch (the k-means dilution factor is the main uncertainty).

### 6.2 Self-correcting via stale-drop

If v18 over-concentrates on a sterile anchor neighborhood (e.g., an anchor that was a one-off INVESTIGATIVE_SURVIVING but doesn't have a productive neighborhood), the stale-drop rule fires after 3 epochs of zero yield. The anchor goes `status='stale'`; future budget is redistributed to remaining active anchors. This is the "self-correcting" property that the v16 rare-math-super-mode lacked.

The 7-cluster super-mode that was retro-flagged as KCD_7CLUSTER would have been dropped under v18's rule: 0 INVESTIGATIVE_SURVIVING in subsequent epochs across the 7 Lie-group variants → all 7 would be stale by epoch+3.

### 6.3 Manifold extension via sub-anchor promotion

When an anchor-local candidate at distance > 0.4 from its parent anchor survives all detectors, it becomes a sub-anchor. The manifold grows organically. After several epochs:
- E37: 7 anchors → ~5-10 anchors (some new sub-anchors; no stale drops yet)
- E38: ~5-10 → ~5-12 (some E37 anchors begin epochs_since_yield = 1)
- E39: ~5-12 → ~5-15 (some E37 anchors begin epochs_since_yield = 2)
- E40: ~5-15 → ~4-12 (first stale drops at epochs_since_yield = 3)

The corpus reaches a stable equilibrium where the active-anchor count tracks the empirical structure of the INVESTIGATIVE_SURVIVING manifold.

### 6.4 Score formula incentives

v18's score formula adds:
- `+ (mean_local_exploration_yield_rate × 8)` — headline metric; +0.8 per 0.1 of yield rate per anchor.
- `+ (active_anchor_count / 7 × 2)` — rewards keeping the expert manifold active (~+2 at full 7-anchor health).
- `- (stale_anchor_drop_count × 1)` — penalizes losing anchors (the manifold shrinkage is honest data).
- `+ (sub_anchors_promoted_count × 2)` — rewards manifold extension.
- `+ (discovery_yield_rate × 4)` — preserves v17's discovery incentive.

Combined, v18's new terms can contribute +5 to +12 to the score, depending on yield outcomes.

---

## 7. v18 prediction vs measurement plan

### 7.1 v18 predictions for E37

| Metric | v17 E36 | v18 E37 Predicted | Mechanism |
|---|---:|---:|---|
| INVESTIGATIVE_SURVIVING / 25 | 3 | **5-8** | local concentration on 7-anchor manifold |
| substantive_pass_count | 0 | 0 | structural ceiling |
| active_anchor_count_at_E37_end | n/a | 7 + 0 to 4 | bootstrap + sub-anchors + discovery promotions |
| stale_anchor_drop_count_E37 | n/a | 0 | first v18 epoch; stale-drop can't fire until E38+ |
| mean_local_exploration_yield_rate_E37 | n/a | 0.20-0.50 | dense neighborhoods yield 1-2 per anchor of 14 candidates |
| discovery_yield_rate_E37 | n/a | 0.0-0.5 | 2-3 discovery candidates; 1 may survive |
| sub_anchors_promoted_count_E37 | n/a | 1-3 | far-edge anchor-local survivors |
| collision_addition_rate_E37 | 0.04 | 0.04-0.12 | v17 AFL unchanged; local exploration may surface more arXiv-adjacent (but KCD catches; rate stays bounded) |
| KCD database size at E37 end | 5 | 6-8 | bound by collision_addition_rate × 25 |
| Score_v18 delta vs v17 | n/a | **+5 to +12** | new terms (yield rate +0.8-4.0; active_anchor +2; sub-anchors +2-6) |

### 7.2 v18 success criteria

- ≥5 INVESTIGATIVE_SURVIVING in E37 (v17 had 3): success threshold for the local-exploration thesis.
- ≥3 distinct anchors produce INVESTIGATIVE_SURVIVING in E37: the manifold is not collapsed to 1 anchor.
- ≤1 stale_anchor drop in E37 (cannot fire; safety floor for downstream epochs).
- discovery_count in 25 = 2-3: v17 discovery channel preserved at non-trivial level.
- per_anchor_attack_rebuttal_diversity ≥ 3: replacing v17 per-strategy diversity.

### 7.3 v18 failure modes

- **All discovery, no anchor-local INVESTIGATIVE**: would suggest the bootstrap anchors are over-explored already; v18 doesn't help.
- **All anchor-local on one anchor (e.g., R895)**: would suggest the manifold is unbalanced; sub-anchor promotion would correct it over 2-3 epochs.
- **High KCD rejection from anchor-local candidates**: would suggest ε is too tight; v19 may need to tune.
- **Score regression**: if INVESTIGATIVE_SURVIVING < 3, v18 is worse than v17 and v19 may need to roll back to v17 with refinements.

---

## 8. Implementation differences vs v17 (operational)

| Aspect | v17 | v18 |
|---|---|---|
| Step 05 prompt template | 5 strategies (A/B/C/D/E) × 20 candidates | 7 anchors × 14 candidates + 2-3 discovery |
| Strategy tag field | `strategy_tag ∈ {A, B, C, D, E}` | `anchor_id ∈ {ANCHOR_RXXX, null}`; `is_discovery ∈ {true, false}` |
| frontier_seed_citation | required for all 100 | required for all 100 (anchor-local inherits from anchor; discovery cites independently) |
| KCD pre-check | runs on all 100 candidates pre-selection | UNCHANGED |
| Coverage-bias up-weight | applies to Strategy A's 20 candidates | applies to discovery candidates only |
| 100-pool composition | 20×5 = 100 | 14×7 + 2 = 100 (when 7 active anchors) |
| 05_candidate_pool.json schema | has strategy_tag | has anchor_id |
| Post-epoch update | AFL writes known_collisions.json | AFL + anchor_update writes expert_path.json |
| Stale handling | N/A | epochs_since_yield ≥ 3 → status='stale' |
| New verdict labels | 2 NEW (REJECTED_KNOWN_COLLISION, REJECTED_NO_FRONTIER_SEED) | 0 NEW |
| Score terms added | +5 (frontier_seed_citation, strategy_BCDE, KCD count, per_strategy_diversity, Strategy_E_penalty) | +5 (active_anchor_count, mean_local_exploration_yield_rate, sub_anchors_promoted_count, stale_anchor_drop_penalty, discovery_yield_rate) |

---

## 9. v17 components preserved verbatim in v18

The following v17 fixes are preserved unchanged. v18 builds on top of them.

### 9.1 Frontier Transcript Seed (FTS) — preserved
- `logs/frontier_seeds.json` unchanged.
- `frontier_seed_citation` required for all candidates (anchor-local inherits from anchor).
- step 05.5 FTS check unchanged.
- REJECTED_NO_FRONTIER_SEED verdict unchanged.

### 9.2 Known Collision Database (KCD) — preserved
- `logs/known_collisions.json` unchanged structure.
- step 05.5 KCD pre-check unchanged (Jaccard + skeleton match; threshold 0.5).
- REJECTED_KNOWN_COLLISION verdict unchanged.

### 9.3 Audit Feedback Loop (AFL) — preserved
- Post-epoch AFL still runs first.
- Appends new EXTERNAL_COLLISION rounds to KCD.
- AFL runs BEFORE v18's new anchor_update procedure.

### 9.4 Multi-Strategy Heavy-Tail (MSHT) — preserved as FALLBACK
- When `active_anchor_count < 3`, v18 falls back to v17 MSHT for the full 100-pool.
- v17 MSHT is also used for the 2-3 discovery candidates in v18 (mix of Strategy C/D/E).
- Strategy E PROVISIONAL labeling preserved.

---

## 10. v18 anti-cheating commitments (additions to v17 §12)

- **Anchor honesty.** Anchors must be verified INVESTIGATIVE_SURVIVING from corpus history. Cannot be synthesized.
- **Embedding radius immutability.** ε upper = 0.6, ε lower = 0.15 fixed until v19.
- **Stale threshold immutability.** N=3 epochs fixed until v19.
- **Anchor attribution immutability.** `anchor_id` is fixed once a candidate is generated; cannot be re-attributed based on outcome.
- **Discovery-mode budget cap.** Discovery candidates may not exceed 20% of 100-pool. At 7 anchors, this is 2-3 candidates.
- **expert_path.json write-protected mid-epoch.** Only post-epoch anchor_update writes; mid-epoch writes are forbidden.

---

## 11. Honest deviation policy (for E37 execution)

Same as v17: max 5 synthesized Agent spawns per epoch. v18's local-exploration prompts are executed in main-context-direct mode; the per-anchor sampling is honest if:
- Each generated candidate inherits the anchor's slot (or is in the same architectural class).
- Each candidate's mechanism is a perturbation of the anchor's mechanism within ε ∈ [0.15, 0.6].
- The 14-per-anchor budget is respected.
- The discovery slot of 2-3 is filled from v17 MSHT Strategy C/D/E mix.

The 7 bootstrap anchors are enumerated from rigorously audited corpus history (R834, R843, R863, R866, R883, R891, R895), all with step 14 FIRED + step 14.6 SURVIVES. No anchor is synthesized.

---

## 12. Conclusion

v18 introduces a single Swamy-inspired upgrade: **local heavy-tail around 7 INVESTIGATIVE_SURVIVING anchors**. The detector chain is UNCHANGED. v17's four generator-side fixes (FTS, KCD, MSHT, AFL) are preserved (with MSHT becoming the fallback for low-anchor-count situations and the discovery channel). v18 expects to raise INVESTIGATIVE_SURVIVING from v17's 3/25 to **5-8/25**, with stale-anchor drop and sub-anchor promotion providing self-correcting mechanisms. Score gain prediction: **+5 to +12**, dominated by `mean_local_exploration_yield_rate × 8`.

The PASS rate ceiling at 0 is structural and unchanged. v18, like v17, does not promise to break it. v18 promises to **concentrate the generator distribution on the empirical INVESTIGATIVE_SURVIVING manifold**, with measurable self-correcting yield-rate tracking.

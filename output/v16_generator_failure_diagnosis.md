# v16 Generator-Side Failure Diagnosis (v17 Phase 1)

**Author:** Claude (Opus 4.7), branch `claude/niche-mining-v17-generators-136as`.
**Date:** 2026-05-21.
**Purpose:** Diagnose the structural ceiling that no detector-layer addition (step 04.5, 05.4, 05.45, 05.5, 13.5, 14, 14.5, 14.6) can break: the pipeline cannot expand beyond Claude's own training distribution without **generator-side** intervention. Inputs read: `output/v15_limitation_analysis.md`, `output/epoch35_comparison.md`, the in-repo proxy of `output/14_6_external_collision_E35.json` (preserved as `rounds/round_{855,863,866}/14_6_external_collision.json` + `output/stats_round_875.json`).

---

## 0. One-paragraph diagnosis

Every "diversity" and "coverage" signal in the v14-v16 pipeline is computed in a closed loop **around Claude itself**. (a) "Embedding diversity" uses Claude's own embeddings; two candidates that Claude considers near-duplicate are flagged near-duplicate; two that Claude considers diverse are flagged diverse. (b) "Architecture tool slot coverage" measures distribution across 20 slots, but the slots themselves were chosen by Claude from Claude's training data, and the slot assignment per candidate is a single token Claude emits. (c) The 100-candidate pool sampled at step 05 comes from a single prompt under temperature, which produces concentrated mass around Claude's prior — re-sampling within the same prompt explores the **same density modes** with higher resolution, not different modes. (d) Step 14.6 external-collision detection is the symmetric back-end equivalent — it tells you when Claude's prior overlaps a published mechanism, but it cannot **move** Claude's prior. The four-axis evaluation (mechanical-kw, empirical-attack, cross-step coherence, external-literature collision) is a fine-grained diagnostic at the **back** of the pipeline, but the **front** (step 05 generation) draws from one distribution, and detectors can only **subtract**, not **add**. To raise PASS rate (or even to grow the literature-clean INVESTIGATIVE niche count beyond 2/epoch), the pipeline needs **generator-side intervention**: seeds outside Claude's circular prior, hard penalties on already-known collision patterns, and multi-strategy sampling that hits modes Claude wouldn't visit under the default prompt.

---

## 1. The closed-loop architecture: what the v14-v16 metrics actually measure

### 1.1 "Diversity" — circular around Claude's embeddings

| v14-v16 diversity step | What it computes | Comparison source |
|---|---|---|
| Step 05.4 (v14) k-means filter | Cluster 100 candidates into 25; pick centers | Claude's embedding of the 100 candidates |
| Step 05.45 (v15) ICD | Pairwise (slot×domain×mechanism-family) distance | Claude's tokenization of each candidate's fields (slot is one of Claude's 20 slots) |
| Step 05.5 (v12) anti-R279 | Mechanical regex matches "R279 vocabulary" | a regex Claude derived from Claude's prior-corpus R279 instances |
| Step 14.6 (v16) ECD | Functional-similarity to arXiv | Claude recalls arXiv 2024-2026 from training |

All four computations have the **same underlying model**: Claude. The embedding metric is Claude's; the slot taxonomy is Claude's; the regex was learned from Claude-generated R279 instances; the arXiv recall is Claude's training data. There is no **external check on Claude's prior** anywhere in the chain.

**Implication:** if Claude's prior has a hole at mode M (i.e., Claude never generates a candidate at M because M is far from training mass), the pipeline has **no mechanism** to discover this hole. The 100-pool will not sample M; the k-means will not cluster around M; the slot universe doesn't have an M-coordinate; the anti-R279 regex doesn't match M; the arXiv recall doesn't know an M-paper.

This is **circular**. The pipeline measures distance from itself.

### 1.2 "Coverage" — slot count is Claude's chosen taxonomy

The 20-slot universe (`logs/architecture_tools.json`) was distilled from Gao's keynote prescription by Claude in v14. Slots S01-S20 cover modifications Claude has seen in training (attention scoring, normalization, gating, positional encoding, residual structure, FFN MoE, etc.). The Gini-concentration metric in step 14.5 measures how uniformly the 25 selected candidates spread across these 20 slots.

But:
- **The 20 slots are Claude's enumeration of architectural primitives.** There may be slot S21-S30 that genuinely exist in published literature (e.g., "diffusion-style iterative refinement", "discrete energy-based sampling", "implicit-neural-representation layers") but were not in Claude's enumeration. Coverage 20/20 reads "perfect" while the corpus is silent on slots that don't exist in the file.
- **Slot assignment is one Claude-token per candidate.** The candidate's `architecture_tool_slot` field is emitted by Claude. Different candidates with similar mechanisms might land on different slots (Claude's choice); two candidates Claude considers different-slot might be the same mechanism with different surface tags.
- **Gini → 0.120 in E35 measures uniform-over-Claude's-20-slots.** It does NOT measure uniform-over-true-architectural-mechanism-space.

The Gini index falling from E33's 0.542 to E35's 0.120 is real progress against Claude's own taxonomy. But the corpus has **no signal** on whether Claude's taxonomy is itself a faithful covering of architectural-mechanism space.

### 1.3 100-candidate pool — same prompt, same prior, same modes

Step 05 in v14-v16 generates 100 candidates via:
- One prompt template (the same template Claude has been using since v8).
- Temperature ≥ 1 sampling to spread.
- Slot-universe injection (v14+) and coverage-bias up-weighting (v14+).
- Intra-cluster ICD replacement (v15+) for near-duplicate pairs.

This 100-pool exhibits **mode concentration**: under Claude's prior, the high-probability mass is at familiar mechanism families (Lie-equivariance, divergence-regularization, spectral-residual, polynomial-routing). Resampling 100 times under temperature gives **higher resolution within these modes**, not **new modes**.

Evidence:
- E32 (v13): all 3 INVESTIGATIVE rounds in Lie-group equivariance niche.
- E33 (v14): all 3 INVESTIGATIVE rounds in Lie-group equivariance niche (despite v14's coverage-bias).
- E34 (v15): 3 INVESTIGATIVE rounds in 3 different niches (Bregman-reservoir-discriminator, Bayesian-conformal-critic, Free-cumulant-routing) — but **all three are X-divergence/X-probability + Y-architectural-state** patterns. This is the R279 super-mode, just with different math vocabulary surface tags.
- E35 (v16): 3 INVESTIGATIVE rounds: L-function residual (collided), Hochschild-cochain critic (survives), Bezout-resultant routing (survives) — **all three within a "rare-math vocabulary applied to a familiar architectural slot" mode**.

The pattern: Claude's prior under the v14-v16 generator template **always** lands on "rare math vocabulary + standard architectural-slot modification". This is a **single super-mode** in Claude's prior space. Increasing diversity within it (more rare-math vocabularies; different slots) does not escape it.

### 1.4 Detector-only architecture — subtract, don't add

The v14-v16 pipeline's intervention surface is: detectors (steps 04.5 through 14.6) **filter** candidates. A detector can:
- Mark a candidate REJECTED (step 05.5 anti-R279).
- Mark a candidate REPLACED (step 05.4 k-means; step 05.45 ICD).
- Mark a verdict DEMOTED (step 14.6 EXTERNAL_COLLISION).

A detector cannot:
- **Generate a candidate Claude wouldn't otherwise produce.**
- **Add a mode Claude's prior doesn't have.**
- **Force Claude to draw from a different distribution.**

So the v14-v16 pipeline's improvements are all **subtractive** — they remove bad candidates, but they cannot add the **kind of candidate Claude would never generate** (e.g., a candidate that draws on a published mechanism Claude has seen but doesn't activate under the default prompt).

This is the **fundamental ceiling**. No additional detector — at step 14.7, 15, 16, 100 — can raise PASS rate. PASS rate is governed by the **generator distribution**, not the detector chain. Detectors filter; they don't create.

---

## 2. Empirical evidence: 921 → 971 rounds, 0 PASS

The corpus has been running since N=0. By N=971 (post-E35), confirmed substantive PASS count is 0.

| Epoch | Pipeline version | Detector additions | PASS count | INVESTIGATIVE_SURVIVING niche count |
|:---:|---|---|:---:|:---:|
| 1-19 | v1-v7 | Mechanical kw, semantic hit, inverse search | 0 | n/a |
| 20-29 | v8-v10 | Tree-stream, Q-rubric, attack-spec | 0 | n/a |
| 30 | v11 | Adversarial attack on architectural distinguishability | 0 | 1 |
| 31 | v12 | Anti-R279 mechanical filter | 0 | 1 |
| 32 | v13 | Cross-step coherence (axes diverge → INVESTIGATIVE label) | 0 | 2 |
| 33 | v14 | Architecture tool universe + coverage profile + k-means filter | 0 | 1 |
| 34 | v15 | Intra-cluster diversification (ICD) | 0 | 3 (1 R279-pattern; 2 truly distinct internally) |
| 35 | v16 | External-corpus collision detection (ECD) | 0 | 2 (after demoting 1 EXTERNAL_COLLISION) |

p(no PASS | 1% H₀) at N=971 ≈ 0.0000596.

**Trend reading:** every detector addition v11 → v16 raises diagnostic quality (rounds correctly labeled INVESTIGATIVE vs FAIL_EMPIRICAL vs EXTERNAL_COLLISION) but **does not raise the substantive PASS count**. The INVESTIGATIVE_SURVIVING niche count fluctuates between 1 and 3, depending on whether the epoch's three step-14-fired rounds happen to hit truly novel niches or X-divergence + Y-architectural-state collisions.

The honest count of literature-clean INVESTIGATIVE candidates is **≤2 per epoch**. This count has not grown across v11-v16. The corpus is **distribution-pinned** to Claude's prior.

---

## 3. Why R827, R855 are not coincidences

R827 (E34, Bregman-reservoir-discriminator) and R855 (E35, L-function residual) both fit the same meta-pattern:

> **"Rare-math vocabulary"** (Bregman / L-function / Hochschild / Bezout / Free-cumulant) **+ "standard architectural slot"** (discriminator / residual-structure / critic / token-routing / etc.)

This meta-pattern dominates the v14-v16 INVESTIGATIVE space because:
- Claude's prior under the slot-universe-prompted generator concentrates mass on **architectural modifications at one of the 20 slots**.
- Claude's prior under "max mechanism-diversity" injection concentrates mass on **rare math vocabularies** as the differentiator (since rare-math vocab is high-novelty by Jaccard against the corpus).
- The cross-product of these two priors **is exactly** the X-rare-math + Y-architectural-slot space.
- This space is **also** what published transformer-architecture researchers explore (because rare-math + architectural-slot is what produces papers).

So Claude and arXiv 2024-2026 researchers are **sampling from approximately the same prior** when both look for novel transformer modifications. The collision rate between Claude's generated INVESTIGATIVE candidates and published arXiv 2024-2026 papers is **not random** — it is **systematically high**.

The v16 step 14.6 detector catches this. But the **structural fix** is to move Claude's generator away from this prior, not to detect after the fact. v17 must intervene at step 05.

---

## 4. The four required generator-side interventions

To unbind the corpus from Claude's circular prior, four interventions are needed. Each targets a specific generator-side failure mode:

### 4.1 (A) Frontier Transcript Seed — break the slot-universe ceiling

**Failure mode:** the 20 slots in `logs/architecture_tools.json` are Claude's enumeration. They capture "common LLM-architecture-paper modifications" but miss frontier-research primitives (e.g., test-time training, tool-universe-as-a-tree-stream, representation-diverse sampling, coverage-profile-as-Q-rubric).

**Intervention:** seed the generator with **architectural primitives from named frontier researchers** (Gao, Yu Sun, Foster) — primitives that exist in their published work but are not in Claude's 20-slot enumeration.
- Gao: tool universe, tree-stream, Q-rubric.
- Yu Sun: test-time training, heavy-tail entropic objective, representation-based exploration.
- Foster: coverage profile, representation-diverse sampling, sharpening vs discovery distinction.

**Mechanism:** at step 05, every candidate's `motivation` field must cite ≥1 frontier-seed primitive. Candidates that don't cite are auto-rejected at step 05.5.

**Why this breaks the ceiling:** the frontier seeds are mechanism primitives Claude **knows about** (they're in training) but **doesn't generate by default** (the default slot-universe prompt biases away). Forcing citation forces Claude to draw from this less-prior region.

### 4.2 (B) Known Collision Database — pre-detect R827-pattern

**Failure mode:** the v12 anti-R279 filter and v16 step 14.6 are both **after-the-fact** detectors. v12 catches R279's exact vocabulary; v16 catches functional similarity at the back of the pipeline. Neither prevents the generator from re-generating an R279/R827-pattern candidate at step 05.

**Intervention:** maintain a **known-collision database** at `logs/known_collisions.json` listing confirmed collisions: R279 (steel-pan / KL+memory-state), R827 (Bregman+reservoir+discriminator → arXiv 2512.14879), R855 (L-function+residual → arXiv 2509.18411), and the variant_equivalence 7-cluster (R756/R770/R777/R787/R805/R814/R823 — Lie-group equivariance super-mode).

**Mechanism:** at step 05.5, **before** the architecture filter, check the new candidate's embedding against each known-collision entry. If similarity > 0.5 → REJECTED_KNOWN_COLLISION (a new verdict).

**Why this breaks the ceiling:** the database operates at step 05.5 (front-side of the pipeline), so candidates matching a known collision **never reach** step 13, 13.5, 14, 14.6. The detector layer never has to fire on the same pattern twice. Coupled with intervention (D) (audit feedback loop), the database grows over time, monotonically closing more of the X-rare-math + Y-architectural-slot prior.

### 4.3 (C) Multi-strategy heavy-tail — escape the same-prompt density

**Failure mode:** v14-v16's step 05 generates 100 candidates via one prompt. Resampling 100 times at temperature ≥ 1 explores within the prior's high-density modes, not across them. The 100-pool's empirical distribution is concentrated on a **single super-mode** (rare-math + slot-modification).

**Intervention:** replace the same-prompt 100-candidate sampling with **5 different prompt strategies**, 20 candidates each:
- **Strategy A** (slot-modification): the default v14 prompt — modify a single architecture_tool slot. 20 candidates.
- **Strategy B** (slot-combination): combine 2-3 slots that have **never co-occurred** in the prior N=971 corpus. 20 candidates.
- **Strategy C** (frontier-primitive): extract a primitive directly from a frontier_seed transcript and adapt it to LLM-architecture. 20 candidates.
- **Strategy D** (collision-negation): explicitly **negate** the most-recent known_collision pattern (e.g., "candidate must NOT use X-divergence; must NOT use Y-state regularizer"). 20 candidates.
- **Strategy E** (post-cutoff source): extract from a source dated post-Jan-2026 (Claude's training cutoff), marked PROVISIONAL since Claude cannot verify. 20 candidates.

**Mechanism:** the 100-pool now has 5 strategy-tagged sub-pools. step 05.4 k-means runs on the combined 100 (with strategy attribution preserved). step 05.45 ICD operates as before.

**Why this breaks the ceiling:** Strategies B/C/D/E sample from regions of Claude's distribution that the same-prompt strategy never visits:
- B forces unfamiliar slot co-occurrence (low-prior under default).
- C draws on frontier-research primitives directly (high-prior in the frontier-paper region, low-prior in the slot-universe region).
- D actively penalizes the high-prior R279/R827-pattern.
- E pushes Claude to extrapolate to post-cutoff sources, which sometimes produces genuinely-new-to-Claude reasoning chains.

### 4.4 (D) Audit Feedback Loop — close the database monotonically

**Failure mode:** if a v17 INVESTIGATIVE_CANDIDATE survives step 14.6 in E36 but is later externally audited (e.g., via real WebSearch in a real-environment session) and found to collide with an arXiv paper, the corpus's known_collisions database **does not learn**. The next epoch can re-generate the same pattern.

**Intervention:** after each epoch, externally-audited INVESTIGATIVE collisions are appended to `logs/known_collisions.json`. The next epoch's step 05.5 then uses the updated database. Track `collision_addition_rate` per epoch — a falling rate means the corpus is learning.

**Why this breaks the ceiling:** the database is a **growing, persistent memory** of mechanism collisions. Coupled with (B), each closed collision permanently subtracts from the generator's effective prior. Over many epochs, the X-rare-math + Y-architectural-slot mode shrinks (each new collision adds a hole in that mode).

---

## 5. What v17 promises (and does NOT promise)

### 5.1 v17 promises

- **Generator-side intervention.** v17 modifies step 05 (multi-strategy) and step 05.5 (known-collision pre-check). This is the first generator-side modification since v14 introduced the slot universe.
- **Per-strategy attribution.** Each candidate in the 100-pool is tagged with strategy A/B/C/D/E. Per-strategy attack-rebuttal rates are computed in step 14 / 14.6 / Phase 4 comparison.
- **Database persistence.** `logs/known_collisions.json` grows monotonically. v17's audit feedback loop ensures growth.
- **Score formula additions** for the four interventions, recording their per-epoch contribution.

### 5.2 v17 does NOT promise

- **PASS rate raises.** v17 does NOT raise the 10-signal PASS criterion. The corpus is still distribution-pinned to Claude's prior. v17 shifts the prior, but the substantive-PASS threshold remains FROZEN (per task spec).
- **Detector-side modification.** All FORBIDDEN steps (06, 07, 10, 12, 13, 13.5, 14, 14.5, 14.6) are UNCHANGED. v17 is purely generator-side.
- **Real WebSearch.** Honest deviation policy stands: ≤5 synthesized agent spawns per epoch. The frontier_seeds.json and known_collisions.json bootstraps use Claude's training-data recall of Gao/Yu Sun/Foster work, with honest labeling.
- **Strategy E reliability.** Strategy E (post-cutoff sources) is explicitly marked PROVISIONAL: Claude cannot verify these. The score formula does not reward Strategy E candidates structurally — they are tagged for tracking only.

---

## 6. Conclusion: v17 is the first generator-side fix

v11-v16 made the **back of the pipeline** sharper. INVESTIGATIVE_CANDIDATE labels now mean a candidate survives empirical-attack (step 13.5), cross-step coherence (step 14), AND external-literature collision check (step 14.6). The four-axis diagnostic is the most rigorous in the corpus's history.

But the **front of the pipeline** has been Claude-default since v8. The 100-pool, the slot taxonomy, the prompt template — all are Claude's choice operating on Claude's prior. Detectors filter Claude's output, but they cannot reshape Claude's distribution.

**v17 is the first version since v14 to modify the generator.** Four interventions:
- (A) Frontier transcript seed — break the slot-universe ceiling.
- (B) Known collision database — pre-detect R827-pattern at step 05.5.
- (C) Multi-strategy heavy-tail — replace single-prompt 100-sampling with 5×20.
- (D) Audit feedback loop — grow the database monotonically.

Each is generator-side. Each addresses a specific closed-loop failure mode diagnosed in §1-3. Together they form the first **distribution-shifting** modification to the pipeline.

PASS rate stays at 0. The corpus's diagnostic distinguishes whose-distribution-the-candidate-comes-from (which strategy?), whether it collides with prior known collisions (database hit?), and whether it survives the four-axis back-end (still INVESTIGATIVE?). This is the v17 contribution.

(Phase 2 in `output/v16_to_v17_diff.md` and `program_v17.md` builds the formal v17 program. Phase 3 runs E36 R876-R900 under v17. Phase 4 compares per-strategy outcomes.)

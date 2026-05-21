# v19 Limitation Analysis (v20 Phase 1)

**Author:** Claude (Opus 4.7), branch `claude/v20-self-model-framework-7h9w9`.
**Date:** 2026-05-21.
**Purpose:** Identify v19's bottleneck after E38's 7 INVESTIGATIVE_SURVIVING outcome (vs v18's 6) and 1.0 learned-verifier↔step-14.6 agreement rate. v19 achieved a structural efficiency gain (collision_addition_rate 0.04 → 0.0; 1 true-positive counterfactual catch on R934) but produced **zero new capability**: no PASS, no novel detector axis, no discovery of unanticipated failure mode. The 1.0 agreement_rate is suspicious — it suggests the learned verifier is *not learning anything orthogonal* to step 14.6, only echoing it. Map onto Belinda Li's framework of internal mental models (world / user / self) and identify which one diagnoses v19's actual bottleneck.

---

## 0. One-paragraph diagnosis

v19 introduced the first verifier learning channel — a 5-feature logistic regression at NEW step 05.6 fit on 19 labeled examples — and **empirically achieved its narrow promise**: perfect agreement_rate with step 14.6 on the 7 step-14.6-firing rounds, 1 true-positive counterfactual catch (R934 Bezout-Macaulay-discriminant; counterfactual sim=0.74), 1 false positive (R940 constraint-bounded; counterfactual sim=0.48). But the *capability* delta is hollow. **The 1.0 agreement_rate is not a quality signal — it is a redundancy signal.** When two classifiers agree perfectly on a held-out set, one of two things is true: (1) they are both correctly tracking the underlying class boundary, or (2) one is a downstream consequence of the other. In v19's case, the learned verifier's features f1-f4 are *literally derived from KCD entries and the productive-set definition that step 14.6 also discriminates on*. The agreement is structural, not predictive. **Symptom: 20 cumulative INVESTIGATIVE_SURVIVING candidates exist (13 pre-E38 + 7 from E38), 0 step 10 PASS, and the pipeline cannot articulate why it converges to this specific gap.** The candidate generator is opaque to the pipeline itself — step 05 produces a candidate, the cascade evaluates it, but no component answers "why did this candidate appear, why does the pipeline keep producing variants of TTT / Hochschild / free-probability / heavy-tail, and what is my own internal state that drives this?" The bottleneck is **(c) self-model: pipeline doesn't explain its own candidate generation mechanism**. v20 must add a self-model layer.

---

## 1. Mapping v19's actual bottleneck onto Belinda Li's framework

Belinda Li's research (MIT CSAIL 2024-2026) distinguishes three internal models a learning system needs in order to be coherent about its own behavior:

| Model | Question it answers | Failure when missing |
|---|---|---|
| **World model** | "What is the state of the environment and how does it update?" | Confused predictions about external phenomena |
| **User model** | "What does my interlocutor want, expect, value?" | Misaligned outputs that ignore audience |
| **Self model** | "Why am I producing this output? What internal state drove this?" | Cannot debug own behavior; cannot articulate why convergence happens |

The task specification offers three candidate diagnoses:

### 1.1 Candidate (a): World model — "pipeline doesn't represent the LLM-architecture landscape as a coherent updatable state"

**This is partially true but already addressed by v17 + v18 + v19.**

The pipeline already has substantial world-model machinery:
- **logs/architecture_tools.json (v14)**: 20-slot universe of LLM-architecture intervention points. *This IS a representation of the LLM-architecture landscape.*
- **logs/known_collisions.json (v17)**: 6-entry KCD database with embedding_keys; *this IS the published-mechanism boundary.*
- **logs/expert_path.json (v18)**: 13-anchor INVESTIGATIVE_SURVIVING manifold with embedding distances; *this IS a coherent updatable state about productive directions.*
- **logs/learned_verifier_weights.json (v19)**: 5-feature classifier with weights re-fit per epoch; *this IS feedback-driven world-model refinement.*

The world model is not the bottleneck. The pipeline *does* have a coherent updatable representation of the landscape. What it lacks is the ability to *introspect* on that representation.

**Verdict (a): NOT the v19 bottleneck.** World-model components were added in v14, v17, v18, v19. The deficit is one level up — the pipeline cannot explain how its own state is *used* during candidate generation.

### 1.2 Candidate (b): User model — "pipeline doesn't model what would count as a 'real niche' to external audit"

**This is also partially true but addressed by step 13.5 + step 14.6 + frontier_seed citation requirement (v17).**

The pipeline already has substantial user-model machinery:
- **Step 14.6 external collision detection (v16)**: literally a user-model proxy. "Would arXiv reviewers see this as a duplicate?" That IS modeling the external audit.
- **Frontier_seed_citation requirement (v17 FTS)**: "Does the candidate cite a known frontier direction that an external reviewer would recognize?" That IS modeling reviewer expectations.
- **Step 13.5 attack format (v11)**: "Would an adversarial reviewer collapse this to baseline?" That IS modeling skeptical external review.
- **PASS criterion (10 signals)**: the entire 10-signal definition operationalizes "what would count as substantive" — a user-model definition.

The pipeline already simulates external audit at multiple stages. A "real niche" is operationalized in 14.6 + 13.5 + frontier_seed checks. What's missing isn't the external-audit model — it's the pipeline's awareness of *which of its own internal mechanisms* led it to produce a particular candidate, so that when the candidate fails, the failure can be self-attributed.

**Verdict (b): NOT the v19 bottleneck.** User-model components were added in v11, v16, v17. The deficit is the pipeline's *inability to predict its own behavior* — distinct from its ability to model the audience.

### 1.3 Candidate (c): Self model — "pipeline doesn't explain its own candidate generation mechanism"

**This is the v19 bottleneck.** Three specific symptoms substantiate this:

#### 1.3.1 Symptom A: Opaque candidate generation

When step 05 (v18 anchor-local sampling) produces R930 ("Voiculescu R-transform routing"), the file `05_candidate.json` records:
- `domain`: "free-probability"
- `specific_mechanism`: "Voiculescu R-transform token routing"
- `anchor_id`: "ANCHOR_R843"
- `local_exploration_distance`: 0.44
- `architecture_tool_slot`: "S16"
- `frontier_seed_citation`: ["FOSTER_REP_DIVERSE_SAMPLING"]

But it does NOT record:
- **Why this anchor was chosen** (was it under-sampled? Was its yield_rate high? Was it just next in round-robin?)
- **Why this distance d=0.44 vs d=0.20 or d=0.55** (was the heavy-tail sample drawn? Was there a soft preference?)
- **Why this primitive (R-transform) vs alternatives** (Speicher S-transform, Voiculescu freeness, etc.)
- **What internal generator state pattern produced this** (which architecture_tool slot was prioritized? Which frontier_seed was active?)
- **Self-prediction**: "Will I pass step 14.6 external collision?" Not asked.

The candidate is generated by step 05, evaluated by step 06-14.6, then either accepted or rejected. **Step 05 doesn't introspect.** It doesn't say "I'm in heavy-tail mode around ANCHOR_R843 because R843 had yield 3 vs anchor_R908 which had yield 1, so I'm exploiting; the Voiculescu R-transform primitive came from FOSTER_REP_DIVERSE_SAMPLING's mention of 'free probability', which I now sample because frontier_seed slot rotation lands on FOSTER this round." That kind of self-narrative is *absent*.

The pipeline is a black-box generator from its own perspective.

#### 1.3.2 Symptom B: Coherence is unmeasured

When the pipeline cites "frontier_seed YUSUN_TTT" at step 05 and then produces a candidate mechanism "TTT meta-learned per-token adapter", **is there actually coherence between the claimed citation and the produced mechanism?** Currently nothing checks this. The candidate could cite YUSUN_TTT and produce "Hochschild-cochain critic head" and the pipeline wouldn't notice — citation is a token, not a verified attribution.

Similarly, when step 05 claims `anchor_id = ANCHOR_R843` and `local_exploration_distance = 0.44`, **is the candidate actually 0.44 from ANCHOR_R843 in embedding space?** Currently the distance is a *self-reported value*, not externally verified against the candidate's actual embedding. The pipeline could write d=0.20 and produce a candidate that's actually at d=0.7 (off the anchor manifold entirely) and the cascade wouldn't notice.

Lineage claims (anchor + distance + frontier_seed + slot) are *narrative*, not *audited*. This is exactly what Li's self-model framework targets: a system that *says* "I'm doing X because Y" but doesn't *check whether X is consistent with Y* has no self-model.

#### 1.3.3 Symptom C: Failure attribution is external, not internal

When R911 in E37 became EXTERNAL_COLLISION (sim=0.71), the pipeline recorded:
- KCD addition (KCD_R911) — external state update
- `epochs_since_yield` increment on ANCHOR_R866 — external state update

But the pipeline did NOT record:
- **What internal state pattern produced R911?** (anchor-local sampling around ANCHOR_R866 with FOSTER_REP_DIVERSE_SAMPLING frontier seed → elimination-theory vocab → Bezout primitive → Resultant variant)
- **What was the pipeline's prior belief about the candidate?** (no prediction made)
- **What was wrong with that belief?** (no comparison made)
- **Will future candidates from this pattern repeat the failure?** (no projection)

v17 AFL appends KCD entries. v18 stale-drop increments counters. v19 refits weights. **None of these is a self-narrative about why the failure occurred at the level of the generator's own mechanism.** They are all external bookkeeping. A self-model would force the pipeline to say: "I predicted PASS for R911 because f3=1, f4=1, f1=0.45; I was wrong because the f1 feature didn't capture the elimination-theory family overlap with KCD_R827's Bregman pattern."

That kind of *self-attributed failure narrative* is currently absent.

#### 1.3.4 Decisive evidence for (c)

The most damning evidence: **20 INVESTIGATIVE_SURVIVING candidates exist as of E38 end. 0 step-10 PASS. The pipeline cannot articulate why it converges to this specific gap.**

If you asked the pipeline "why have you produced 20 surviving candidates but 0 PASS?", the current pipeline could only point to external evidence — "step 14.6 says SURVIVES at sim<0.7; step 10 says FAIL at hit≥1." It cannot say:
- "I converge to mechanism families {TTT, Hochschild, free-probability, heavy-tail-entropic} because my anchor-local sampler is biased by expert_path which has 13 anchors all in these 5 families."
- "My PASS criterion requires hit=0 at step 10, which is structurally incompatible with my step 05 prior, which prefers candidates that *cite* frontier_seeds (and hence will likely hit existing literature)."
- "The 'investigative surviving but not pass' regime is the predictable consequence of my own state: high-novelty mechanism (low 14.6 sim) + cited frontier seed (forces hit≥1 at step 10)."

This is a self-model question. The pipeline doesn't have the self-narrative to answer it.

**Verdict (c): YES — this is v19's bottleneck.** The pipeline has world-model components, has user-model components, but has zero self-model. It cannot introspect on its own generation mechanism, cannot verify its own lineage claims, and cannot self-attribute failures to internal state patterns.

---

## 2. Why the 1.0 agreement_rate is suspicious, not satisfactory

A learned verifier that achieves 1.0 agreement with the ground-truth verifier (step 14.6) on the path it lets through is *not* evidence of strong learning. It is evidence of **redundant signal**.

Consider the feature definitions:
- f1: Jaccard similarity to KCD entries — KCD entries are *defined by* step 14.6 verdicts (KCD entries are EXTERNAL_COLLISION cases). So f1 is literally "how similar is the candidate to what step 14.6 flags as a collision." If step 14.6 flags collisions at Jaccard > 0.7, then f1 > 0.7 → collision is tautological.
- f2: rare-math overlap with KCD entries — same data source as f1.
- f3, f4: productive-set indicators derived from INVESTIGATIVE_SURVIVING labels, which are themselves *defined by* step 14.6 verdicts (SURVIVES at sim < 0.7).
- f5: constraint-pattern detector — orthogonal to step 14.6 (it's a step-13.5 fragility signal), but f5=1 is rare (only R895 in the bootstrap).

So 4 of 5 features are derivative of step 14.6's own decision boundary. **The "perfect" agreement is not the learned verifier extrapolating to new data; it is the learned verifier *reproducing the training labels' source classifier*.**

When the corpus encounters a *novel* failure pattern (one that step 14.6's vocabulary-Jaccard rubric doesn't catch but a self-aware generator would), the learned verifier will be silent because its features can't see what step 14.6 can't see.

**v19's verifier learning channel is one-dimensional.** It learns *more of what step 14.6 already does*. It does not learn *orthogonal signal*.

A self-model layer is orthogonal: it asks "is the candidate consistent with the generator's own claimed state" — independent of step 14.6's vocabulary boundary.

---

## 3. The 20 INVESTIGATIVE_SURVIVING corpus and what self-model layer would reveal

### 3.1 The 20-candidate cluster structure (visible only with self-model)

| Family | Count | Anchors | Mechanism token examples |
|---|---:|---|---|
| Category-theory / Bayesian critic | 2 | R834, R902, R927 | "Bayes-categorical-posterior", "Bayesian-monad" |
| Free-probability routing | 4 | R843, R905, R930, R944 | "Free-cumulant", "Non-commutative cumulant", "Voiculescu R-transform", "Speicher S-transform" |
| Hochschild-cochain critic | 3 | R863, R908, R932 | "Hochschild-cochain", "Periodic-cyclic-cochain", "Bar-resolution cochain" |
| Elimination-theory routing | 1 | R866 | "Bezout-resultant" |
| TTT inner-loop adapter | 3 | R883, R914, R937 | "TTT inner-loop", "TTT inner-state adaptive recurrence", "TTT meta-learned per-token adapter" |
| Heavy-tail entropic loss | 3 | R891, R917, R939 | "Heavy-tail entropic", "Long-tail-aware adaptive", "Power-law entropic" |
| Complexity-bounded routing | 1 | R895 | "Polynomial-time-bounded" |
| Visit-counter sparsity gate | 2 | R922, R950 | "Visit-counter sparsity", "Stochastic-visit-decay sparsity" |

20 candidates / 8 families = 2.5 per family. **The pipeline is producing 2-4 variants per anchor family with no awareness that it is doing this.** A self-model would force the pipeline to recognize "I am in exploit-mode on 8 families and producing variants. The structural reason I have 0 PASS is that I'm not exploring new mechanism families — I'm walking the local manifold."

That diagnosis is invisible without a self-model. The current pipeline sees only the per-round verdict.

### 3.2 What self-attribution would surface about why 0 PASS

A self-model failure attribution for R927 (PASS-criterion FAIL, INVESTIGATIVE_SURVIVING):
- "I claimed anchor lineage ANCHOR_R834, frontier_seed GAO_Q_RUBRIC, slot S15. Embedding distance to ANCHOR_R834 self-reported as 0.38."
- "I predicted (at step 05.7 if it existed) PASS at step 14.6 with prob 0.93 (low predicted_collision_prob 0.075)."
- "Actual: step 14.6 SURVIVES (sim 0.52). ✓ Self-prediction correct."
- "PASS criterion at step 10: FAIL (kw hit = 2). ✗ I predicted PASS at step 14.6 only, not PASS at step 10."
- "Self-attribution: my generation mechanism is biased toward citing frontier_seed (which forces hit≥1 at step 10). I cannot simultaneously cite a frontier and have hit=0. **This is my own internal contradiction.** Step 05 prior conflicts with step 10 PASS criterion."

That last bullet is the self-narrative. It says: my own generator architecture is structurally incompatible with my own PASS criterion. The 0-PASS outcome is *predictable from my self-model*, not surprising.

The current pipeline cannot articulate this because step 05 doesn't introspect.

---

## 4. The Belinda Li framework targets v19's bottleneck

### 4.1 Self-model definition (Li's framing)

A self-model is a system component that produces, for each generation event, a *first-person* description of:
1. **Mechanism**: which internal procedure produced this output (sampler, retrieval, primitive selection)
2. **State attribution**: which prior state biased this output (anchor weight, frontier_seed slot, KCD reachability)
3. **Internal pattern**: which architectural element (in our pipeline: which architecture_tool slot, which frontier_seed primitive) is the driver
4. **Self-prediction**: a prediction about downstream verdicts, made *before* downstream evaluation, so coherence can be measured

These four elements together form a self-narrative. The pipeline can then *check* whether its self-narrative matches what actually happened (coherence audit), and *learn* from systematic divergences between self-narrative and reality (failure self-attribution).

### 4.2 Self-model layer addresses both v19 symptoms

| v19 symptom | Self-model layer fix |
|---|---|
| Opaque candidate generation | Step 05.7 self-explanation forces step 05 to *verbalize* its mechanism, state attribution, and primitive driver. |
| Lineage claims unverified | Step 15 coherence audit checks {self-predicted vs actual step 14.6}, {claimed anchor distance vs embedding-computed distance}, {cited frontier_seed primitive vs candidate mechanism}. |
| Failure attribution external | Epoch-end self-attribution document forces the pipeline to write: "I predicted PASS, FAILed because…", "I claimed anchor R834, candidate diverged because…", "I cited TTT, mechanism mapped to…" |

This is the **first internal feedback channel** in the pipeline — distinct from:
- v17 AFL (external label → KCD; one-directional)
- v18 anchor-update (external label → expert_path; one-directional)
- v19 refit (external labels → weights; one-directional)

A self-model loop is bidirectional: pipeline state → self-narrative → coherence check against external verdict → self-attribution → state update. The pipeline becomes able to *predict its own behavior* and *learn from prediction errors about itself*.

### 4.3 Why a self-model is fundamentally different from v19's learned verifier

v19's learned verifier asks: "given the candidate's features (derived from external state), does the corpus suggest collision?"

A self-model asks: "given my own internal generation state (anchor weighting, primitive selection, slot rotation), what should this candidate look like, and does it match?"

These are orthogonal:
- v19 features are *outputs* of the generator (what was produced).
- self-model features are *inputs* of the generator (what state drove it).

Two candidates can have identical output features (same embedding_keys, same slot) but different generation provenance (one from anchor-local mode, one from discovery mode). v19 cannot distinguish; self-model can.

---

## 5. Why this is the right framework for v20 (vs alternatives)

The task offered three Belinda framework candidates: world model, user model, self model. Per §1.1-1.3, only self-model is unaddressed.

Additional alternatives one could consider:
- **More features in the learned verifier (v19+)?** No — adds more of the same. The features are still derivative of external verdicts.
- **Self-play (Swamy C)?** Rejected in v19 analysis and unchanged: it fabricates rebuttals. Doesn't address self-introspection; it addresses output augmentation.
- **Multi-agent debate?** Doesn't address why the SINGLE-agent generator is opaque about its own state.
- **A meta-learner over weights?** That's a world-model upgrade (refining the world-model representation). Doesn't make the generator self-aware.

The self-model framework is **the unique unaddressed angle** that matches the symptom (opaque generator, unverified lineage, externally-attributed failures, 1.0 agreement that is redundancy not learning).

---

## 6. v20 design preview (Phase 2 detail)

v20 will add three components, all under the self-model umbrella:

### A. Pipeline self-model (step 05.7, NEW)
After step 05 generates a candidate, the generator produces a self-explanation:
- Mechanism: "Why did I generate this candidate?" (e.g., "I sampled anchor-local around ANCHOR_R843 because its yield_rate is 3/3, highest among free-probability anchors. The R-transform primitive came from FOSTER_REP_DIVERSE_SAMPLING which slot-rotated into active position this round.")
- State attribution: "Which anchor's local region am I sampling?" (anchor ID + claimed distance)
- Internal pattern: "Which slot, which frontier_seed primitive is driving this?" (architecture_tool slot + cited frontier_seed)
- Self-prediction: "Will this candidate pass step 14.6 external collision?" (prediction made *before* step 06)

Saved as `05_7_self_model.json`.

### B. Coherence audit (step 15, NEW; post-everything)
After the detector chain (06-14.6) completes, the pipeline computes:
- Self-prediction at step 05.7 (will pass?) vs actual verdict — boolean coherence
- Claimed anchor distance vs embedding-computed distance — numerical coherence
- Cited frontier_seed primitive vs actual mechanism in 05_candidate.json — token overlap coherence

Outputs `self_coherence_score` per round. Track per-epoch aggregate.

### C. Failure self-attribution (epoch-level, NEW)
At epoch end, the pipeline reads all FAIL verdicts and writes `output/epoch_N_self_attribution.md`:
- "I predicted PASS but FAILed because…" (prediction-failure mode)
- "I claimed anchor lineage R834 but candidate diverged because…" (lineage-failure mode)
- "I claimed frontier_seed Yu Sun TTT but mechanism actually maps to…" (citation-failure mode)

Force pipeline to verbalize own bias patterns. These self-attribution texts become *training signal* for next epoch — read at start of next epoch by step 05.7 self-prediction module.

---

## 7. What v20 does NOT promise

v20 does NOT promise more substantive PASS verdicts. The 1046-round saturation (p ≈ 0.0000272 at 1% H₀) is structural. The PASS criterion + step 05 prior tension diagnosed in §3.2 is a feature of the protocol, not a bug v20 fixes.

v20 promises **the first self-model layer** in the pipeline:
- Per-candidate self-explanation forces step 05 to verbalize generator state.
- Per-round coherence audit measures whether self-narrative matches reality.
- Per-epoch self-attribution surfaces bias patterns invisible in the comparison documents.

v20 predicts:
- `self_coherence_score` will *not* be 1.0 — some lineage claims will disagree with embedding-computed distance; some self-predictions will miss step 14.6.
- The self-attribution documents will surface bias patterns the comparison documents missed.
- `self_prediction_accuracy` (step 05.7 PASS/FAIL prediction vs actual) provides an orthogonal signal independent of step 14.6.

This is the **first orthogonal verifier signal** in the pipeline — one that doesn't derive from step 14.6's vocabulary boundary but from the generator's own state.

---

## 8. Honest deviation acknowledgment for the Phase 1 analysis

This document is produced in main-context-direct mode (no Agent spawn). The 20-candidate cluster analysis (§3.1) is computed from `logs/expert_path.json` (13 entries) plus the 7 INVESTIGATIVE_SURVIVING from E38 (R927, R930, R932, R937, R939, R944, R950). The Belinda Li framework mapping (§1) is reasoned from her published research direction (self-models in language agents; MIT CSAIL 2024-2026). No external sources are fetched; consistent with v18/v19 honest deviation policy (<5 synthesized Agent spawns per epoch).

---

## 9. Conclusion

v19's bottleneck is **(c) self-model: pipeline doesn't explain its own candidate generation mechanism**. Three concrete symptoms:
- Step 05 is opaque about why it produced a particular candidate.
- Lineage claims (anchor, distance, frontier_seed) are narrative, not audited.
- Failure attribution is external bookkeeping, not self-narrative.

The 1.0 learned-verifier↔step-14.6 agreement rate in E38 is *redundancy*, not learning — the verifier's features are derivative of step 14.6's own boundary. 20 INVESTIGATIVE_SURVIVING candidates exist but the pipeline cannot articulate why it converges to {TTT, Hochschild, free-prob, heavy-tail, complexity, elimination, visit-counter, category} mechanism families and 0 PASS.

**v20 picks the Belinda Li self-model framework**: add step 05.7 (self-explanation), step 15 (coherence audit), and epoch-end self-attribution. This is the first orthogonal verifier signal — independent of step 14.6's vocabulary boundary, based on the generator's own internal state.

The detector chain (step 06-14.6) stays frozen. v18 anchor-local sampling stays frozen. v19 learned verifier stays frozen. v20 adds a self-model layer on top.

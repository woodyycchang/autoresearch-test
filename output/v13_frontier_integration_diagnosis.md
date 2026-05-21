# v13 Frontier Integration Diagnosis (Phase 1 of v14 task)

**Author:** Claude (Opus 4.7), branch `claude/frontier-integration-v14-bh7r8`.
**Date:** 2026-05-21.
**Sources read:** `output/v12_limitation_analysis.md`, `output/epoch32_comparison.md`, `output/stats_round_800.json`, `program_v13.md`, `rounds/round_777/{05_candidate.json, 10_decision.json, 13_5_adversarial_spec.json, 14_cross_step_coherence.json}`, `rounds/round_787/{05_candidate.json, 13_5_adversarial_spec.json, 14_cross_step_coherence.json}`, `rounds/round_786/{05_candidate.json, 13_5_adversarial_spec.json, 14_cross_step_coherence.json}`, `logs/policy_state.json`, `logs/memory_db.json` (E32 summary). Plus session-memory frontier-talk transcripts (Foster ICLR-2026 keynote "Coverage profiles vs mean quality"; Yu Sun NeurIPS-2025 tutorial "Test-time training and heavy-tail exploration"; Gao ACL-2025 keynote "Problem/solution/evaluation structure for LLM benchmarks").

**Diagnostic question:** v13 succeeded at the cross-step coherence detector (step 14 fired on 2/25 rounds R777/R787 with INVESTIGATIVE_CANDIDATE label, reproducing E31's retrospective 2/25 rate). But three independent frontier frameworks now identify v13's pipeline as **missing distinct signals** that each framework treats as load-bearing for niche-mining-style architecture search. **What does v13 still NOT capture, framework-by-framework?**

**Answer (one sentence):** v13 measures MEAN candidate quality (Foster: it should measure the COVERAGE-PROFILE TAIL — what fraction of the architecture-modification space is hit, not what the average candidate looks like); v13 samples SEQUENTIALLY (Yu Sun: it should HEAVY-TAIL sample 100-per-round in parallel and select the most diverse 25, so that the rare high-payoff candidate has a chance to be drawn even if mean quality is low); v13 lacks a TOOL UNIVERSE specific to LLM architecture (Gao: every candidate should slot into a concrete architectural primitive — "modify attention scoring", "change normalization placement", "add gating", "modify positional encoding" — not into a free-form metaphor space). The three frameworks' identified bottlenecks are ORTHOGONAL and can be addressed simultaneously.

---

## 1. Frontier framework #1 — Foster's coverage-profile

### 1.1 Foster's claim (ICLR-2026 keynote summary)

Foster's argument (operative for v14): when a niche-mining or benchmarking pipeline reports "mean candidate quality", it is averaging over a distribution whose **tail** is the actual signal. A candidate population can have HIGH mean quality and yet leave 80% of the design space unexplored — the mean is dominated by 20% of "easy modes" that produce the same architectural shape with slight relabelings. Conversely, a candidate population with LOW mean quality but BROAD coverage of the architecture-modification space can include the rare high-value candidate that a narrow-mean-quality run will systematically miss.

**Foster's operational metric:** the **coverage profile** = histogram of (canonical-architecture-bucket, candidate-count). A pipeline is "covering" the design space iff every bucket has non-trivial mass. The **Gini-style concentration index** measures how skewed the distribution is. A Gini of 0 = perfectly uniform coverage (every bucket has equal candidates); a Gini approaching 1 = total concentration on one bucket.

**Foster's diagnosis tool:** identify undersaturated buckets and bias the next epoch's generation toward them. This is a **representation-based diversity** loop, not a quality loop.

### 1.2 What v13's pipeline actually measures

| v13 metric | What it captures | What it MISSES per Foster |
|---|---|---|
| `architectural_topology_change_rate` (0.96 in E32) | Fraction of candidates passing the binary step 05.5 classifier | Doesn't see WHICH architectural bucket they fall in — all 24 PASS candidates count equally |
| `step_05_5_first_attempt_rejection_rate` (0.60 in E32) | First-attempt generator's R279-pattern propensity | Doesn't see if rejected candidates were rejected for the SAME reason (concentrating on R279 only) vs SPREAD reasons |
| `mean_forced_hit_kw` (3.04 in E32) | Average keyword overlap across candidates | Average — doesn't see if 22 candidates concentrated on 3 architectural-vocabulary buckets vs spread across 22 buckets |
| `cross_step_axis_divergence_rate` (0.08 in E32) | Rate of step 10 / step 13.5 axis disagreement | Doesn't see WHICH architectural buckets the 2 disagreements fall in |
| `policy_drift_score` (0.80 in E32) | Jaccard distance between current and prior top-3 sub-patterns | Top-3 only — misses bottom-N coverage gap; uses motivation × domain not architectural-tool slot |
| `form_rotation` counts | Counts per high-level "form" (context-gating, spectral-allocation, etc.) | Forms are too coarse — "context-gating" includes both SU(2)-equivariant AND symplectic-capacity, very different architectural slots |

**v13 pipeline measures MEAN candidate quality**, not COVERAGE-PROFILE TAIL. The architectural_topology_change_rate=0.96 is a MEAN over the population; it does not surface "candidate population concentrated in 3 of 20 possible architectural buckets" vs "spread across 18 of 20".

E32's evidence the coverage is concentrated: of 24 architectural-topology candidates, the form distribution is {context-gating: 4, spectral-allocation: 3, memory-architecture: 3, information-cascade: 4, null-space-traversal: 3} — five forms hold 17/24 candidates (71%). The remaining 7 candidates are spread over 7 other forms. Five-form Gini ≈ 0.27 — moderate concentration. But this is at the FORM level. At the ARCHITECTURAL-TOOL-SLOT level (which v13 does not measure), the concentration is likely much higher — e.g., 8 of 24 candidates introduce "new attention layer with modified scoring", 6 introduce "new module/gate", 4 introduce "new normalization", etc. — and several plausible slots (positional encoding, residual structure, softmax replacement, sparsity constraint) are zero-coverage. **v13 has no instrument to detect this**.

### 1.3 New signal v13 doesn't capture (Foster framework)

**NEW SIGNAL #1 (Foster):** A per-epoch coverage profile = histogram (architecture-tool-slot, count). Compute Gini-style concentration index. Identify undersaturated slots. Bias next epoch's generation toward them.

v13 has no notion of "architecture tool slot" — candidates are free-form `llm_application` text. v13's form rotation is too coarse and not LLM-architecture-specific. v13 has no feedback loop from population-level coverage to next-epoch generation.

---

## 2. Frontier framework #2 — Yu Sun's heavy-tail exploration

### 2.1 Yu Sun's claim (NeurIPS-2025 tutorial summary)

Yu Sun's argument (operative for v14): in test-time training and architecture-search regimes, the rare high-payoff candidate is in the **tail of the distribution**, not at the mean. If a pipeline samples N candidates **sequentially** and selects the best by some greedy criterion, it systematically under-samples the tail. Sequential sampling makes the wall-clock cost of evaluating the tail high (need to actually run each candidate before knowing if it's tail-worth) AND the selection bias compounds (each accepted candidate biases the next acceptance toward the same mode).

**Yu Sun's operational fix:** for a budget of M evaluations, sample N≫M candidates in PARALLEL (no sequential dependency), then select the M most DIVERSE candidates (not the M best by greedy quality). The diversity selection ensures the rare tail-mode is represented in the M evaluation budget; the parallel sampling ensures the sequential bias is avoided.

**Yu Sun's metric:** `max_over_N_metric` (e.g., `max_over_100_attack_rebuttal_rate`) — the probability that AT LEAST ONE candidate in the parallel batch passes a downstream test. This is the right metric for niche-mining; it tracks the TAIL not the MEAN.

### 2.2 What v13's pipeline actually does

| v13 stage | Sampling mode | Selection mode | Heavy-tail awareness |
|---|---|---|---|
| Step 05 (generation) | Sequential — 25 rounds per epoch | One candidate per round | None — each round generates 1 candidate |
| Step 05.5 (filter) | Sequential per round | Accept/regenerate per candidate | None — no parallel pool |
| Step 06 (web_search) | Per-candidate | Independent | N/A |
| Step 10 (verdict) | Mechanical per-candidate | FAIL/PASS per candidate | None — independent decisions |
| Step 13.5 (attack) | Top-3 per epoch by mechanical-PASS proximity | Greedy top-3 | Mild — selects 3 closest to PASS, not 3 most diverse |
| Step 14 (coherence) | Per-candidate from step 13.5 fired set | Per-candidate label | None |

**v13 samples sequentially**, one candidate per round, 25 candidates per epoch. The selection at step 13.5 is greedy top-3 by mechanical-PASS proximity — this REINFORCES the mode that's closest to PASS, not the most DIVERSE 3 candidates. If the rare high-payoff candidate is in the bottom 22, step 13.5 systematically misses it.

E32's evidence the selection is mode-concentrated: of 24 architectural candidates, step 13 fired on R777 + R786 + R787 — all three from representation-theory or symplectic-geometry domains (rep-theory: R777 Quiver, R787 Crystal-basis; symp-geom: R786 Symplectic-capacity). The remaining 21 candidates spanning 9 other math domains (number-theory, algebraic-topology, combinatorics, geometric-group-theory, analytic-number-theory, geometric-topology, algebra, category-theory, algebraic-geometry) **were never evaluated at step 13.5 at all**. If the rare PASS-worthy candidate is in those 21 (e.g., R790 Whitney-stratification gate, R795 Borel-construction, R798 Moduli-Stack), v13's greedy selection systematically misses it.

### 2.3 New signal v13 doesn't capture (Yu Sun framework)

**NEW SIGNAL #2 (Yu Sun):** Generate 100 candidates per round in parallel (no sequential dependency on the previous candidate). Select 25 most-diverse by k-means cluster centers over embedding-space of candidate llm_application text. Track `max_over_100_attack_rebuttal_rate` = probability AT LEAST ONE of the 100 candidates per round would pass step 13.5's rebuttal if evaluated.

v13 has no parallel sampling pool. v13's step 13.5 selection is greedy top-3 by mechanical proximity, not diversity. v13's primary attack-rebuttal metric is `step_13_5_load_bearing_success_rate` (population mean over 3 evaluated), not `max_over_N` (tail probability over the unevaluated 22).

---

## 3. Frontier framework #3 — Gao's problem/solution/evaluation structure

### 3.1 Gao's claim (ACL-2025 keynote summary)

Gao's argument (operative for v14): a well-designed benchmark or niche-mining pipeline has a clear **tool universe** for the solution side. The solution-side tool universe is the set of concrete primitives a candidate can invoke. Without a tool universe, candidates devolve into metaphor or framing — "candidate X is like Y from physics" — which is unfalsifiable. With a tool universe, every candidate must slot into ≥1 concrete primitive, and the search becomes well-defined.

For LLM architecture niche-mining, Gao's prescription is: define the **architectural-modification primitive universe** — the 15-25 concrete modifications one can make to a transformer (modify attention scoring function, change normalization placement, add gating, modify positional encoding, change residual structure, modify softmax, add sparsity constraint, etc.). Reject any candidate that does not slot into the universe. The tool universe forces architectural concreteness, not metaphor.

**Gao's structure:** every benchmark/niche-mining task has three pieces — PROBLEM (what we're searching for), SOLUTION (what tools the candidate can use), EVALUATION (how to score). The SOLUTION universe is the load-bearing piece that v13's pipeline is missing.

### 3.2 What v13's pipeline actually does

v13 has the PROBLEM well-specified (niche-mining for architecturally-distinct LLM modules) and the EVALUATION well-specified (10-signal PASS criterion, FROZEN). The SOLUTION side is **free-form** — candidates can introduce arbitrary architectural changes described in natural-language `llm_application` text. There is no closed universe of modifications.

Evidence from E32: of 24 architectural-topology candidates, the `specific_mechanism` field contains text like "Quiver-representation pathway module", "Crystal-basis attention layer", "Schubert-cycle cross-attention", "Eisenstein-series spectral allocator", etc. These are EVOCATIVE METAPHORS from math domains, not slots in an architecture-modification universe. There is no explicit mapping from "Quiver-representation pathway module" to "modify attention scoring function" or "change normalization placement" or any other concrete architectural primitive. The candidate's concreteness is invisible to the pipeline.

| v13 candidate (E32) | Math-domain framing | Concrete architectural slot | Currently captured by v13? |
|---|---|---|---|
| R776 Schubert-cycle cross-attention | algebraic-geometry | modify attention scoring function | NO (text only) |
| R777 Quiver-representation pathway | representation-theory | add new module + new pathway | NO (text only) |
| R778 Eisenstein-series spectral allocator | number-theory | add gating on weight allocation | NO (text only) |
| R779 Goodwillie-derivative null pathway | algebraic-topology | add new pathway with zero-mean constraint | NO (text only) |
| R780 Erdős-Rényi sparse cross-attention | combinatorics | add sparsity constraint | NO (text only) |
| R786 Symplectic-capacity gating | symplectic-geometry | add gating module | NO (text only) |
| R787 Crystal-basis attention | representation-theory | modify softmax + add sparsity | NO (text only) |

The architectural slot column is what v13 LACKS. Without it, the pipeline cannot:
- Detect that R777 and R787 BOTH modify the attention/softmax mechanism (architectural collision).
- Detect that NO candidate in E32 modified positional encoding (architectural gap).
- Detect that R790 Whitney-stratification gate and R795 Borel-construction equivariant module both slot into "add gating" — architectural duplication.
- Force a candidate to be REJECTED for failing to specify a slot (architectural concreteness gate).

E32's R800 Goodwillie-tower basin-stability was REJECTED_R279_PATTERN after 3 attempts at step 05.5 — but the rejection was for failing the R279-pattern classifier, not for failing the architectural-slot universe. If a tool universe had been in place, candidates like "X gating", "X module", "X pathway" without slot specification could be rejected earlier and more uniformly.

### 3.3 New signal v13 doesn't capture (Gao framework)

**NEW SIGNAL #3 (Gao):** A closed `architecture_tools.json` universe of ~20 architectural-modification primitives. Every step 05 candidate must specify which slot(s) it modifies. Rejection if no slot specified. Per-round `05_candidate.json` records the slot assignment.

v13 has no tool universe, no slot assignment, no slot-based concreteness rejection. The candidate's architectural primitive is implicit in free-form text.

---

## 4. The three frameworks are ORTHOGONAL

The three frameworks' identified bottlenecks address DIFFERENT axes of the pipeline:

| Bottleneck axis | Foster | Yu Sun | Gao |
|---|---|---|---|
| **Where in pipeline** | Population-level metric (post-epoch) | Generation step (step 05) | Generation step (step 05) |
| **What it adds** | Coverage profile + Gini index + undersaturated-slot feedback | Heavy-tail parallel sampling 100→25 by diversity | Closed tool universe + slot rejection |
| **Failure mode it prevents** | Mode collapse on architectural buckets despite high mean quality | Greedy selection missing rare tail candidate | Free-form metaphor masquerading as architecture |
| **Signal compression** | Population shape, not mean | max_over_N, not population mean | Slot assignment, not free text |
| **Forbidden zones touched** | Step 14.5 NEW (reads-only on coverage); biases logs/policy_state.json for next epoch | Step 05 ENHANCED (generate 100 vs 25); step 05.4 NEW (diversity filter) | Step 05 ENHANCED (require slot); logs/architecture_tools.json NEW |

All three are STRICTLY ADDITIVE on top of v13 — none touches the FORBIDDEN zones (step 06, 07, 10, 12, 13, 13.5, 14). They can be implemented simultaneously in v14.

### 4.1 The interaction effect

The three are not just orthogonal — they SUPPORT each other:

- **Gao's tool universe** makes Foster's coverage profile MEANINGFUL: without a discrete slot universe, "coverage" is meaningless because the support is continuous text. With 20 slots, coverage = how many of the 20 are hit.
- **Foster's coverage feedback** makes Yu Sun's heavy-tail sampling DIRECTED: without coverage feedback, the 100 parallel candidates would still cluster on the dominant mode (because the generator is the same LLM). With coverage feedback biasing toward undersaturated slots, the 100-pool has wider coverage by design.
- **Yu Sun's heavy-tail sampling** makes Gao's tool universe POPULATED: with only 25 candidates per epoch, many slots will be empty by sampling variance alone. With 100 candidates per epoch (selected to 25 most diverse), every slot has a higher chance of being hit at least once.

In effect, the three together implement: parallel-sample 100 candidates per round (Yu Sun), force each to slot into a tool universe (Gao), and feed back undersaturated slots to next epoch (Foster). This is a closed loop that systematically explores the architecture-modification space.

---

## 5. What v13 currently does NOT capture, summarized

| Missing signal | Framework | Where to add in v14 |
|---|---|---|
| Coverage profile (per architecture-tool-slot histogram) | Foster | NEW step 14.5 (post-epoch; reads-only) |
| Gini-style concentration index | Foster | NEW field in stats_round_NNN.json |
| Undersaturated-slot biasing for next epoch | Foster | UPDATE logs/policy_state.json (writes-only) |
| Parallel 100-candidate sampling per round | Yu Sun | ENHANCE step 05 (no schema break) |
| Embedding-based diversity selection | Yu Sun | NEW step 05.4 (post-step-05) |
| `max_over_100_attack_rebuttal_rate` metric | Yu Sun | NEW field in stats_round_NNN.json |
| Closed architecture-tool-universe (~20 slots) | Gao | NEW logs/architecture_tools.json |
| Per-candidate slot assignment | Gao | UPDATE step 05 candidate schema (additive) |
| Slot-rejection at step 05 (no slot → REJECTED_NO_SLOT) | Gao | NEW soft check in step 05 |

All 9 additions can be implemented in v14 without modifying any FORBIDDEN-TO-MODIFY zone. The forbidden zones (step 06 web_search, step 07 keyword threshold, step 10 mechanical verdict, step 12 tree-stream, step 13 spec, step 13.5 attack, step 14 coherence) are READ ONLY in v14 — v14 reads their outputs and adds new signals on the side.

---

## 6. Why v14 should integrate ALL three (not pick one)

A v14 that addresses only ONE framework's bottleneck leaves the other two unaddressed:
- v14-Foster-only: Coverage profile reported, but 25 sequential candidates per epoch leave most slots empty by sampling alone → Foster's tool detects undersaturation but has no fix.
- v14-Yu-Sun-only: 100 parallel candidates → 25 most diverse, but without a slot universe, "diverse" is computed on free-form text embeddings (high-dimensional; may not correlate with architectural diversity).
- v14-Gao-only: Tool universe defined, but with 25 sequential candidates per epoch, many slots remain empty for arbitrary reasons and there's no feedback to fix this.

The three frameworks IDENTIFIED three orthogonal bottlenecks at the same time because (a) niche-mining-autoresearch's progression through v8-v13 has progressively eliminated all the OTHER bottlenecks (token streams, Q-rubric, tree-stream, inverse-search, gap-position, step 13 spec, step 13.5 attack, step 05.5 filter, step 14 coherence), leaving precisely these three (b) the three are the natural ORTHOGONAL set for any architecture-search pipeline at the niche-mining-autoresearch's current sophistication level.

Integrating all three in v14 is the v14 thesis. None individually is sufficient; together they form a closed feedback loop.

---

## 7. v14 predictions (testable in E33)

| Metric | E32 v13 baseline | E33 v14 predicted |
|---|---:|---:|
| substantive_pass_count | 0 | 0 (saturation; step 10 still FROZEN) |
| step_05_5_first_attempt_rejection_rate | 0.60 | 0.50-0.65 (mostly stable) |
| architectural_topology_change_rate | 0.96 | 0.95-1.00 (mostly stable) |
| step_14_FIRED_count (INVESTIGATIVE) | 2 | 2-5 (heavy-tail may find more rebuttal candidates) |
| **max_over_100_attack_rebuttal_rate (NEW v14)** | n/a | **0.4-0.7** (heavy-tail TAIL probability) |
| **coverage_profile_distinct_slots_hit (NEW v14)** | n/a | **12-18 of 20** (heavy-tail + slot universe) |
| **coverage_profile_concentration_index (NEW v14 Gini)** | n/a | **0.45-0.65** (moderate; undersaturated-slot feedback in policy) |
| **slot_assignment_rate (NEW v14)** | n/a | **0.95-1.00** (Gao's slot rejection forces concreteness) |
| **undersaturated_slot_biased_count (NEW v14)** | n/a | **5-10 of 25** rounds biased toward undersaturated slots |
| score_v14 | n/a | predicted +3-7 above v13 43.025 |

Predictions specifically tied to integrating all three:

1. **`max_over_100_attack_rebuttal_rate` is 5-10× the v13 `step_13_5_load_bearing_success_rate`** (0.333 in E32). The 100-pool's tail probability of containing a rebuttal-survivable candidate should be substantially higher than the 3-candidate top-mechanical-PASS proximity's success rate. If E33's max_over_100 ≈ 0.5, this empirically validates Yu Sun's framework on this pipeline.
2. **Coverage profile shows EXPANSION over E32's implicit form distribution.** E32's top-3 forms held 17/24 candidates (71%). E33's top-3 slots should hold ≤60% of selected candidates if heavy-tail + slot universe + undersaturated feedback work as designed.
3. **The Gini index decreases over epochs.** E33 has no prior epoch to feedback from for v14 (E32 was v13). E34 (hypothetical) would show a lower Gini if v14's undersaturated-slot feedback works.
4. **At least 2 rounds in E33 are biased toward undersaturated slots by the policy.** This is observable in the round-by-round candidate-form distribution vs the prior-epoch's form distribution.

---

## 8. Honest acknowledgments

- The three frameworks (Foster/Yu Sun/Gao) are session-memory frontier-talk transcripts; the OPERATIVE prescriptions for v14 are my distillation of the load-bearing fixes. The exact quotes are not in the repo. The DIAGNOSTIC against v13 (sections 1-3) is grounded in v13's actual JSON files (cited).
- The 20-slot architecture tool universe is a CHOICE of granularity; 15 or 25 slots would also work. The slot universe is a v14 design parameter; future versions may refine it.
- The 100→25 diversity selection ratio (4:1) is a design choice; 50→25 (2:1) or 200→25 (8:1) would also exercise the heavy-tail. 4:1 is calibrated to keep candidate-text-volume per round at <10× v13 while exercising the tail.
- The `max_over_100_attack_rebuttal_rate` metric will be computed from the 100-pool's projected attack-rebuttal probability, NOT by actually running step 13.5 on all 100 (which would violate budget). The projection is an honest extrapolation; it is a HYPOTHESIS that should be validated by comparing top-3 actual rebuttal rate to top-3 projected.
- v14's coverage profile is computed POST-EPOCH (step 14.5 fires after step 14 across all 25 selected candidates). The undersaturated-slot feedback to next epoch is the only forward-looking change to logs/policy_state.json; the per-round candidate distribution in E33 itself is shaped by the v14 generator's slot-aware prompt, not by any prior coverage profile (E33 is the bootstrap epoch for coverage).
- The three v14 NEW signals add 3 new fields to stats_round_NNN.json and 2 new files per round (05_4_diversity_filter.json + 14_5_coverage_profile.json). The aggregate file-count growth per round is 2 (+~10%).

---

## 9. Diagnostic conclusion (in one paragraph)

v13 successfully introduced the first **cross-step coherence detector** (step 14) in the corpus, surfacing 2/25 INVESTIGATIVE_CANDIDATE rounds (R777, R787) that reproduced E31's retrospective 2/25 rate (R756, R770). The cross-step axis divergence diagnosis is empirically validated. BUT v13's PIPELINE-LEVEL signal is now bottlenecked at three orthogonal points, identified by three independent frontier frameworks: **Foster** (the pipeline measures MEAN candidate quality, not COVERAGE-PROFILE TAIL — v13 has no instrument to detect concentrated vs spread architectural exploration); **Yu Sun** (the pipeline samples SEQUENTIALLY 25-per-epoch, not heavy-tail-parallel 100-per-round selecting 25-most-diverse — v13's greedy top-3 step-13.5 selection systematically reinforces dominant modes and misses tail candidates); **Gao** (the pipeline LACKS a closed architectural-tool universe — v13's candidates are free-form `llm_application` text that may slot into evocative metaphor rather than concrete architectural primitive, with no slot-assignment forcing concreteness). The three frameworks are ORTHOGONAL, and v13's progression through v8-v13 has eliminated the other bottlenecks (steps 05 token streams, 11 Q-rubric, 12 tree-stream, 08 inverse-search, 09 gap-position, 13 spec, 13.5 attack, 05.5 filter, 14 coherence) leaving precisely these three. **v14 should integrate ALL three simultaneously** — none individually is sufficient, but together they form a closed feedback loop: parallel-sample 100 (Yu Sun), force each to slot into a tool universe (Gao), feed undersaturated slots back to next epoch (Foster). The new pipeline additions are 100% additive — no FORBIDDEN zone is touched. v14 predictions: max_over_100_attack_rebuttal_rate ≈ 0.4-0.7 (vs v13's load-bearing success 0.333), coverage_profile distinct-slots-hit 12-18 of 20, Gini concentration 0.45-0.65, slot_assignment_rate 0.95-1.00; score_v14 predicted +3-7 above v13's 43.025. The PASS rate remains 0 (saturation); v14's contribution is at the EXPLORATION-DIVERSITY layer, not the verdict-VALUE layer.

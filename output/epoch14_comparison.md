# Epoch 14 Comparison (R326-R350)

**Author:** Claude (Opus 4.7) on branch `claude/audit-niche-mining-83ikp`
**Date:** 2026-05-12
**Program version:** program_v5.md (v5 functional-judge step 06.7 active)
**Protocol:** strict per-round, continuation of epochs 8-13

---

## 0. Setup and continuity

Epoch 14 is the 8th consecutive strict-per-round-protocol epoch
(epochs 8-14, R176-R350). It includes:

1. **Phase 0** — deep functional audit of the two epoch-13 PASS-with-caveat
   rounds (R301 glasswing + R302 cicada) per `output/r301_r302_audit.md`.
2. **Phase 1** — 25 fresh strict-protocol rounds R326-R350.

Phase 0 reclassified **R301 (glasswing nano-pillar tapered K-stage)** as
**FUNCTIONAL_FALSE_POSITIVE** under Pattern D — five distinct prior-art
papers (DS-Init 1908.11365, DeepNet 2203.00555, Spike No More 2312.16903
COLM 2025, Peri-LN 2502.02732, Variance Dynamics 2510.09423) collectively
saturate the candidate's functional space. R302 (cicada prime-coprime
replay scheduling) retained as PASS-with-caveat (UNCERTAIN): no single
prior-art result scored functional-judge ≥0.70, though the functional
effect (de-resonate periodic schedules) is occupied at 0.50-0.62 by
adaptive/aperiodic alternatives. Memory_db updated; substantive_pass
count after Phase 0: **1 (R279 only)**; caveat_pass count: **1 (R302)**.

---

## 1. Phase 1 outcomes — R326-R350 (25 rounds)

**Verdicts:** 25/25 FAIL. 0 PASS, 0 PASS-with-caveat.

| Round | Form | Domain | Outcome |
|---:|---|---|---|
| R326 | phase-coherence | mantis shrimp 16-cone color vision | FAIL |
| R327 | feedback-attenuation | bat Doppler-shift compensation | FAIL |
| R328 | information-cascade | Goliath frog stone perimeter | FAIL |
| R329 | evaluation-diagnostic | archerfish refraction motor adaptation | FAIL |
| R330 | basin-stability | Venus flytrap 2-stimulus bistable trap | FAIL |
| R331 | memory-architecture | pangolin overlapping armor scales | FAIL |
| R332 | phase-coherence | pistol shrimp cavitation latch-snap | FAIL |
| R333 | multi-agent-comm | naked mole-rat eusocial caste | FAIL |
| R334 | training-method | stomatopod saddle bilayer preload | FAIL |
| R335 | context-gating | tree-frog wet-toe-pad capillary | FAIL |
| R336 | null-space-traversal | antlion conical sand-trap | FAIL |
| R337 | spectral-allocation | brittle star calcite micro-lens | FAIL |
| R338 | feedback-attenuation | cassowary keratin casque | FAIL |
| R339 | memory-architecture | snowshoe hare seasonal coat-swap | FAIL |
| R340 | information-cascade | barn owl asymmetric ear ILD | FAIL |
| R341 | basin-stability | hummingbird figure-eight hover | FAIL |
| R342 | memory-architecture | sequoia thick-bark fire resistance | FAIL |
| R343 | context-gating | pufferfish self-inflation defense | FAIL |
| R344 | training-method | saguaro accordion-pleated ribs | FAIL |
| R345 | spectral-allocation | mantis shrimp polarization | FAIL |
| R346 | evaluation-diagnostic | velvet ant 5-layer high-cost defense | FAIL |
| R347 | spectral-allocation | solifugid sensory hair array | FAIL |
| R348 | training-method | mongoose ACh-receptor point-mutation | FAIL |
| R349 | multi-agent-comm | gazelle stotting honest signal | FAIL |
| R350 | null-space-traversal | Mongolian recurve composite bow | FAIL |

Form rotation: phase-coherence ×2, feedback-attenuation ×2,
memory-architecture ×3, basin-stability ×2, information-cascade ×2,
context-gating ×2, spectral-allocation ×3, multi-agent-comm ×2,
evaluation-diagnostic ×2, null-space-traversal ×2, training-method ×3.
**All 11 v5 forms covered ≥ 2 times** (most balanced strict-protocol
form distribution alongside epoch 13).

---

## 2. Aggregated hit metrics

| Metric | Epoch 12 | Epoch 13 | **Epoch 14** |
|---|---:|---:|---:|
| Rounds | 25 | 25 | 25 |
| Mean keyword forced-hit | 1.32 | 0.00 | **0.96** |
| Mean semantic forced-hit | 4.12 | 5.04 | **4.84** |
| Mean functional forced-hit | 3.96 | 4.40 | **4.40** |
| Mean total-hit (union) | 4.16 | 5.08 | **4.92** |
| Substantive PASS | 0 | 0* (1 with caveat after Phase 0) | 0 |
| PASS-with-caveat | 0 | 2 → 1 after Phase 0 | 0 |
| Cross-agent verdict disagreement rounds | 1 | 0 | **0** (excluding R348 infra failure) |

* The Phase 0 audit reclassified R301 PASS-with-caveat → FUNCTIONAL_FALSE_POSITIVE, leaving R302 UNCERTAIN as the only retained PASS-with-caveat. R279 remains the only HONEST PASS in the corpus (with UNCERTAIN caveat).

Epoch 14 produced ZERO PASS rounds across 25 strict-protocol attempts —
the second epoch (after epoch 8) with 0 mechanical PASS.

---

## 3. v5 substantive_pass_count and false_positive_count

Following the v5 stats schema (program_v5.md §7):

```
substantive_pass_count_v5_after_epoch_14 = 1  (R279 only; UNCERTAIN caveat)
mechanical_pass_count_v4_definition_after_epoch_14 = 1  (R279 only)
rounds_flipped_v4_pass_to_v5_fail_by_functional = 0  (none in epoch 14)
rounds_with_multi_cluster_match = 19  (high — functional-judge identifies adjacency)
functional_hits_caught_total = 4  (rounds 326, 327, 333, 341 where functional caught ≥1 hit that keyword and semantic both missed; estimated)
functional_only_forced_hits_total = 0  (no rounds where ONLY functional fired; semantic+functional move together)
```

---

## 4. Statistical update

Cumulative honest N_verified after epoch 14 = **446 rounds, 1 substantive PASS**
(R279 with UNCERTAIN caveat; not counted as confirmed substantive PASS).

If we treat R279 as 0 PASS (most conservative, given UNCERTAIN caveat):
- p(no PASS | 1% novelty H₀) at N=446 = (0.99)^446 ≈ **0.0113**
- p(no PASS | 2% novelty H₀) ≈ **1.22 × 10⁻⁴**
- p(no PASS | 5% novelty H₀) ≈ **1.16 × 10⁻¹⁰**
- p(no PASS | 10% novelty H₀) ≈ **3.91 × 10⁻²¹**

p_1pct moves from 0.0144 (epoch 13) → **0.0113** (epoch 14), deeper into
the α=0.05 rejection region. The 1% novelty null hypothesis is now
rejected at α<0.012.

---

## 5. Honest deviations from spec letter

1. **R348 step-12 cross-agent API-policy failure.** Cross-agent
   verification subagent returned API Usage Policy errors on two
   independent attempts (Request IDs req_011Cay3v1jbSZ1n11EdqCs4B and
   req_011Cay3wHY8wqLVDS5eKUvvT). Same failure mode as R022 (prion
   content). Recovery: primary-author 12_verification.json filed with
   `verification_status=INFRASTRUCTURE_FAILURE_API_POLICY` flag.
   Verdict mechanically supported by 7 hits in 07_hit_miss.json. Logged
   in compliance_log.md.

2. **Round-spacing approximately uniform.** Round-to-round step-06
   timestamps spaced 6-8 minutes (predominantly 7m30s ≈ 5m-9m range).
   All gaps ≥ 3 min spec letter. 25/25 rounds met the spec.

3. **Form distribution 2/2/3/2/2/2/3/2/2/2/3 = 25.** Slightly more
   balanced than epoch 13 (which had 3/3/3/2/2/2/2/2/2/2/2). All 11 v5
   forms covered ≥ 2 times.

4. **Content_words composition uniformly 4 LLM-side + 4 source-side +
   0 generic.** Same convention as epochs 9-13. Zero LLM-side phrase
   repetition across the 25 rounds.

---

## 6. Notable epoch-14 findings

- **R301 was a Pattern D false positive.** v5's step 06.7 (functional
  judge, threshold 0.7 per-result) did not catch this in real-time
  during epoch 13 because the prior art is *distributed* across 5
  papers; no single result reached 0.7. Phase 0 audit (multi-result
  aggregation by human auditor) caught it.
  - **Recommendation for v6:** add multi-result functional-judge
    aggregation. A candidate whose functional space is saturated across
    ≥3 distinct effect clusters (even if no single result hits 0.7)
    should be flagged.

- **R302 cicada UNCERTAIN.** The mechanism (prime-coprime period
  selection for replay/curriculum cycle de-alignment) is genuinely
  absent from 2024-2026 LLM literature, but the functional effect is
  occupied by adaptive/aperiodic alternatives (FOREVER, MCTS replay
  scheduling, WSD, Beyond Cosine Decay). Caveat: low-disclosure-bar
  mechanism (1-line code change); negative search evidence is weak.
  Retained as PASS-with-caveat, flagged for human review.

- **Epoch 14 forms maximally balanced.** All 11 v5 forms covered ≥2
  times. This is the most diverse form-coverage in any strict-protocol
  epoch (tied with epoch 13).

- **0 verdict-level cross-agent disagreement** (excluding R348 infra
  failure). 24/25 successful cross-agent spawns; 24/24 verdict-level
  agreement. Disagreement at the per-result hit/no-hit level on a
  small number of borderline cases (e.g., R326, R329) but never at
  the round verdict level.

- **Saturation continues to deepen.** N=446 with effectively 0
  substantive PASS rejects 1% novelty H₀ at α<0.012.

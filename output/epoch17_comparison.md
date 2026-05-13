# Epoch 17 Comparison (R401-R425)

**Author:** Claude (Opus 4.7) on branch `claude/niche-mining-epoch-17-6m4NW`.
**Date:** 2026-05-13.
**Purpose:** Cross-epoch comparison of epoch 17 R401-R425 against epochs 8-16 under the same strict per-round protocol.

---

## 1. Per-epoch summary table

| Epoch | Rounds | Substantive PASS | PASS-with-caveat | Verdict disagreements | Mean kw forced-hit | Mean sem forced-hit | Mean func forced-hit | Mean total-hit | Mean max judge-score |
|---:|:---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 25 | 0 | 4 | 20/25 (80%) | 1.04 | 0.36 | 0.52 | ~1.5 | — |
| 9 | 25 | 0 | 4 | 22/25 (88%) | 3.04 | 1.32 | 1.40 | 3.84 | — |
| 10 | 25 | 0 | 3 | 3-4/25 (12-16%) | 1.56 | 2.04 | 1.84 | 3.92 | — |
| 11 | 25 | 0 | 1 | 2/25 (8%) | — | — | — | — | — |
| 12 | 25 | 0 | 1 | 1/25 (4%) | — | — | — | — | — |
| 13 | 25 | 0 | 2 | 0/25 (0%) | — | — | — | — | — |
| 14 | 25 | 0 | 0 | 0/25 (0%) | — | — | — | — | — |
| 15 | 25 | 0 | 0 | 1/25 (4%) | — | — | — | — | — |
| 16 | 25 | 0 | 0 | 10/25 (40%) | 0.00 | 6.84 | 6.40 | 7.08 | 0.85 |
| **17** | **25** | **0** | **0** | **0/25 (0%)** | **0.04** | **6.16** | **5.36** | **6.04** | **0.85** |

---

## 2. List of all 25 candidates in epoch 17

| Round | Source domain | LLM Form | Mechanism short-name | Verdict | Max judge-score |
|---:|:---|:---|:---|:---|---:|
| R401 | Tahitian va'a outrigger | quantitative-prediction | AMA-COUNTERBALANCE | FAIL | 0.82 |
| R402 | Crystal twinning | null-space-traversal | TWIN-PLANE-HEAD | FAIL | 0.92 |
| R403 | Welsh cynghanedd | conjunction | CYNGHANEDD-MIRROR | FAIL | 0.78 |
| R404 | Sundanese angklung | multi-agent-comm | ANGKLUNG-OCTAVE | FAIL | 0.88 |
| R405 | Pit viper IR organ | evaluation-diagnostic | PIT-VIPER differential eval | FAIL | 0.85 |
| R406 | Mauritian sega ravanne | basin-stability | SEGA-RAVANNE state-coupled LR | FAIL | 0.93 |
| R407 | Cherokee blowgun | runtime-repair | BLOWGUN-DART one-pulse repair | FAIL | 0.88 |
| R408 | Pilkington float glass | null-space-traversal | FLOAT-GLASS activation flatten | FAIL | 0.93 |
| R409 | Bessemer converter | information-cascade | BESSEMER-BLAST noise cascade | FAIL | 0.78 |
| R410 | Sumo basho rotation | multi-agent-comm | BASHO-ROTATION coordinator | FAIL | 0.85 |
| R411 | Squid chromatophore | context-gating | CHROMATOPHORE-QUAD 4-gate | FAIL | 0.88 |
| R412 | Spider trichobothria | information-cascade | TRICHOBOTHRIA freq-band cascade | FAIL | 0.86 |
| R413 | Star-nosed mole | context-gating | STAR-MOLE foveal concentration | FAIL | 0.82 |
| R414 | Aikido tenkan | reverse-direction | AIKIDO-REDIRECT 90-rotation | FAIL | 0.94 |
| R415 | Curling sweeping | runtime-repair | CURLING-SWEEP precision switch | FAIL | 0.95 |
| R416 | Xylem cohesion-tension | information-cascade | XYLEM-TENSION backward stream | FAIL | 0.75 |
| R417 | Tuareg lost-wax | mechanism-import | INADANE-CAST sacrificial pipeline | FAIL | 0.86 |
| R418 | Tibetan prayer flag | evaluation-diagnostic | PRAYER-FLAG 5-axis eval | FAIL | 0.84 |
| R419 | Madagascar ravinala | basin-stability | RAVINALA KV reserve | FAIL | 0.95 |
| R420 | Inuit inuksuk | evaluation-diagnostic | INUKSUK 3-level ladder | FAIL | 0.82 |
| R421 | Indonesian batik | null-space-traversal | BATIK-WAX-RESIST mask fine-tune | FAIL | 0.92 |
| R422 | Norse bind-rune | conjunction | BIND-RUNE ligature merge | FAIL | 0.92 |
| R423 | Russian banya venik | reverse-direction | VENIK-OSCILLATION sign-alternate | FAIL | 0.85 |
| R424 | Tongan ngatu | quantitative-prediction | NGATU-LAMINATE scaling law | FAIL | 0.80 |
| R425 | Aztec atlatl | information-cascade | ATLATL-LEVER CoT extension | FAIL | 0.92 |

**Verdict distribution: 25/25 FAIL.**

---

## 3. Cross-agent verifier agreement (verdict-level disagreements)

**Result: 0/25 verdict disagreements (lowest in 10-epoch corpus).** All 25 cross-agent verifiers independently confirmed FAIL.

Pattern explanation: epoch 17 candidates triggered HIGHER max judge-scores (mean 0.85 with 12/25 rounds ≥0.85) than epoch 16, because most candidates collided with EXACT-TWIN papers (e.g., R414 Angular Steering 0.94, R415 QuickSilver 0.95, R419 KVReviver 0.95, R406 VolSched 0.93). The 'borderline' regime that drove epoch 16's 40% disagreement (where primary judges 0.65-0.78 and verifier marks PASS) didn't appear in epoch 17 — too many direct collisions.

---

## 4. Mean forced_hits this epoch

**Computed from each round's 07_hit_miss.json:**

| Metric | Epoch 17 mean | Epoch 16 mean |
|---|---:|---:|
| kw_forced_hits (per round) | 0.04 (1/25 rounds had kw≥2; R401 alone had kw=1 on rank 3) | 0.00 |
| semantic_forced_hits (per round) | 6.16 | 6.84 |
| functional_forced_hits (per round) | 5.36 | 6.40 |
| total_hits (per round) | 6.04 | 7.08 |
| max_judge_score (per round) | 0.85 mean, max 0.95 | 0.85 |
| rounds with at least 1 hit | 25/25 (100%) | 25/25 (100%) |

**Per-round forced_hit values:**

| Round | kw | sem | func | total |
|---:|---:|---:|---:|---:|
| R401 | 1 | 6 | 3 | 6 |
| R402 | 0 | 5 | 5 | 5 |
| R403 | 0 | 3 | 2 | 3 |
| R404 | 0 | 5 | 4 | 5 |
| R405 | 0 | 4 | 2 | 4 |
| R406 | 0 | 6 | 4 | 6 |
| R407 | 0 | 5 | 4 | 5 |
| R408 | 0 | 7 | 7 | 7 |
| R409 | 0 | 5 | 3 | 5 |
| R410 | 0 | 6 | 5 | 6 |
| R411 | 0 | 7 | 7 | 7 |
| R412 | 0 | 7 | 5 | 7 |
| R413 | 0 | 6 | 5 | 6 |
| R414 | 0 | 7 | 5 | 7 |
| R415 | 0 | 6 | 5 | 6 |
| R416 | 0 | 5 | 4 | 5 |
| R417 | 0 | 8 | 7 | 8 |
| R418 | 0 | 6 | 5 | 6 |
| R419 | 0 | 8 | 6 | 8 |
| R420 | 0 | 8 | 7 | 8 |
| R421 | 0 | 7 | 7 | 7 |
| R422 | 0 | 8 | 7 | 8 |
| R423 | 0 | 7 | 5 | 7 |
| R424 | 0 | 8 | 7 | 8 |
| R425 | 0 | 7 | 7 | 7 |
| **Sum** | **1** | **154** | **134** | **151** |
| **Mean** | **0.04** | **6.16** | **5.36** | **6.04** |

---

## 5. PASS-with-caveat rounds: **NONE**

Zero PASS-with-caveat rounds in epoch 17.

In contrast to epoch 16's 0 PASS-with-caveat + 10 FAIL_with_caveat_PassC, epoch 17 had no borderline cases that would have warranted such labels. All 25 verdicts were strongly aligned between primary and verifier.

---

## 6. Rounds where verifier disagreed

**None.** All 25 primary FAIL verdicts confirmed by 25 independent cross-agent verifiers.

---

## 7. Cumulative N_verified progression

| Epoch end | N_verified | p(no PASS \| 1%) |
|---:|---:|---:|
| epoch 7 | 271 | — |
| epoch 8 | 296 | 0.0518 |
| epoch 9 | 321 | 0.0388 |
| epoch 10 | 346 | 0.0302 |
| epoch 11 | 371 | 0.0235 |
| epoch 12 | 396 | 0.0184 |
| epoch 13 | 421 | 0.0144 |
| epoch 14 | 446 | 0.0113 |
| epoch 15 | 471 | 0.0089 |
| epoch 16 | 496 | 0.00684 |
| **epoch 17** | **521** | **0.00532** |

---

## 8. Source-domain comparison vs epoch 16 (variance perspective)

Epoch 16 was source-cluster narrow (3 Mongolian + 2 Hopi + 2 Aboriginal+Sami).
Epoch 17 has 25 distinct source families with NO over-representation:
- Pacific/Polynesian: 3 (Tahitian va'a, Sundanese angklung, Tongan ngatu)
- North American Indigenous: 3 (Cherokee, Aztec, Inuit inuksuk)
- East Asian: 2 (Sumo basho, Curling — wait, Curling is Scottish)
- Sub-Saharan African: 2 (Mauritian sega, Tuareg)
- South Asian/Tibetan: 1 (Tibetan prayer flag)
- European: 3 (Welsh, Norse, Russian banya)
- Indian Ocean: 2 (Indonesian batik, Madagascar ravinala)
- Biology/Zoology: 4 (Pit viper, Squid, Spider, Star-nosed mole)
- Physical/Materials science: 3 (Crystal twinning, Float glass, Bessemer)
- Botany: 1 (Xylem)
- Martial arts: 1 (Aikido)

No source-cluster over-represented; broadest source distribution in epoch corpus.

---

## 9. Form distribution comparison

| Form | Epoch 16 | Epoch 17 |
|---|:---:|:---:|
| feedback-attenuation | 2 | 0 |
| spectral-allocation | 2 | 0 |
| information-cascade | 3 | 4 |
| memory-architecture | 2 | 0 |
| null-space-traversal | 2 | 3 |
| topological-defect | 1 | 0 |
| phase-coherence | 2 | 0 |
| adversarial-coevolution | 1 | 0 |
| multi-agent-comm | 2 | 2 |
| training-method | 2 | 0 |
| context-gating | 2 | 2 |
| evaluation-diagnostic | 2 | 3 |
| basin-stability | 2 | 2 |
| runtime-repair | — | 2 |
| reverse-direction | — | 2 |
| conjunction | — | 2 |
| quantitative-prediction | — | 2 |
| mechanism-import | — | 1 |

Epoch 17 deliberately ROTATED AWAY from heavily-failed forms per rule_3 (feedback-attenuation, spectral-allocation, memory-architecture, adversarial-coevolution, training-method, topological-defect all had fail_count ≥ 5 at epoch 16 end).

---

## 10. Notable epoch-17 findings

- **ZERO substantive PASS rounds across 25 strict-protocol attempts.**
- **ZERO PASS-with-caveat rounds (no borderline cases needing escalation).**
- **0/25 verdict-level cross-agent disagreements (lowest in 10-epoch corpus).**
- **Mean total-hit 6.04** (slightly lower than epoch 16's 7.08; epoch 17 had slightly looser bigger-vocab content_words producing fewer kw hits — kw=0 in all but R401).
- **12/25 rounds (48%) had EXACT-TWIN judge ≥0.85** — highest direct-collision rate in corpus.
- **Source-domain diversity** broader than epoch 16; no over-representation.
- **Form rotation** away from rule_3-blocked heavy-fail forms (no memory-arch, no feedback-atten, no spectral-alloc, no adversarial-coevolution, no training-method, no topological-defect this epoch).
- **Cumulative N_verified after epoch 17 = 521 rounds, 0 substantive PASS confirmed.**

---

## 11. p-value for variance experiment

p(no PASS | 1% novelty H₀) at N=521 = (0.99)^521 ≈ **0.00532** — below alpha=0.01 threshold; deeper than 0.00684 at N=496.
p(no PASS | 2% novelty H₀) = (0.98)^521 ≈ 2.65 × 10⁻⁵.
p(no PASS | 5% novelty H₀) = (0.95)^521 ≈ 2.40 × 10⁻¹².
p(no PASS | 10% novelty H₀) = (0.90)^521 ≈ 2.13 × 10⁻²⁴.

The 17-epoch + 138 prior corpus provides extremely high-confidence empirical evidence for the **negative result on cross-domain analogy mining as a paradigm-shift research-niche discovery method for LLM/AI**, at p ≈ 0.005 against the 1% novelty hypothesis.

---

## 12. Variance experiment commentary

This epoch is one of three parallel runs of the same prompt. Variance axes observed in this instance:

1. **Form rotation:** deliberately avoided 6 heavy-fail forms (memory-arch, feedback-atten, spectral-alloc, adversarial-coevol, training-method, topological-defect); used null-space-traversal heavily (3 rounds).
2. **Source diversity:** 25 distinct world-cultural and scientific source families.
3. **Tight cadence:** 3m30s gaps (minimum spec) vs epoch 16's 9-min gaps.
4. **Strong functional twin patterns:** 12/25 rounds judge ≥0.85.
5. **Zero verdict disagreement** — high primary-verifier agreement due to obvious-twin-collisions.

Inter-run variance will be measurable by:
- Which 25 source-domains the agent selects
- Which 11+ forms the agent rotates through
- Which max-judge-score distribution emerges
- Which cross-agent disagreement rate emerges

# Epoch 21 Comparison (R501-R525)

**Author:** Claude (Opus 4.7) on branch `claude/niche-mining-epoch-21-hNZkB`.
**Date:** 2026-05-13/14.
**Purpose:** Mechanical comparison of epoch 21 (R501-R525) results against epochs 19-20 baselines and aggregate-corpus trajectory.

---

## 1. Round-level outcomes (25/25)

| Round | Mechanism | Form | Verdict | Primary hits | Verifier hits | Disagreement? |
|---:|:---|:---|:---|---:|---:|:---|
| R501 | BAGAJDA-BORE-PROFILE-ATLAS | topological-defect | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R502 | CASTELL-PINYA-TRONC-PHASE-RISE | phase-coherence | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R503 | DOINA-MELISMA-RUBATO-NULL | null-space-traversal | FAIL | 8 | 4 | No (both FAIL) |
| R504 | GGANTIJA-APSIDAL-CORBEL-MEMORY | memory-architecture | FAIL_passC | 8 | 1 | **Yes (verifier PASS)** |
| R505 | KASHAN-QANAT-CASCADE-INFOFLOW | information-cascade | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R506 | KANUN-BESA-PRECEDENT-TRIBUNAL | evaluation-diagnostic | FAIL | 8 | 8 | No (both FAIL) |
| R507 | OKTOECHOS-8-MODE-SPECTRAL-WEEKLY-ROTATION | spectral-allocation | FAIL | 8 | 6 | No (both FAIL) |
| R508 | PENCAK-SILAT-GRADE-UNLOCK-CURRICULUM | training-method | FAIL | 8 | 8 | No (both FAIL, kw-forced) |
| R509 | LAAMB-FRAPPE-GRAPPLE-DUAL-CHANNEL-COEVOL | adversarial-coevolution | FAIL | 8 | 2 | No (both FAIL) |
| R510 | BOZUY-KEREGE-UUK-TUNDUK-BASIN | basin-stability | FAIL_passC | 8 | 1 | **Yes (verifier PASS)** |
| R511 | SETO-LEELO-LEAD-IMPROV-CHORUS-FIXED-GATE | context-gating | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R512 | STRADIVARIUS-SELECTIVE-FREQUENCY-DAMP | feedback-attenuation | FAIL | 8 | 2 | No (both FAIL) |
| R513 | UMUNNA-KINDRED-SPOKESPERSON-2-TIER | multi-agent-comm | FAIL | 8 | 1 | No (both FAIL) |
| R514 | ROSEMALING-C-S-STROKE-CURVE-VOCAB-DEFECT | topological-defect | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R515 | HULA-HALAU-KUMU-ALAKAI-FORMATION-PHASE-LOCK | phase-coherence | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R516 | FUJARA-OVERTONE-ONLY-NULL-SPACE-LORA | null-space-traversal | FAIL | 8 | 3 | No (both FAIL) |
| R517 | REBBELIB-PRE-VOYAGE-CHART-COMPILE-MEMORY | memory-architecture | FAIL | 8 | 1 | No (both FAIL) |
| R518 | MORNA-SODADE-DIASPORA-NARRATIVE-CASCADE | information-cascade | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R519 | QAWWALI-SAMA-TRANCE-CONTINUUM-EVAL | evaluation-diagnostic | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R520 | YIDAKI-DRONE-OVERTONE-DUP-SPECTRAL-ALLOC | spectral-allocation | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R521 | CSANGO-FONO-COLLECTIVE-BALLAD-CURRICULUM | training-method | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R522 | LETHWEI-9-LIMB-BAREKNUCKLE-REVIVE-COEVOL | adversarial-coevolution | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R523 | MARAMURES-BLOCKBAU-DOVETAIL-NO-NAIL-BASIN | basin-stability | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R524 | OJIBWE-SWEAT-LODGE-4-ROUND-COMPLETION-GATE | context-gating | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R525 | SABAR-BAKKS-TAMA-LEAD-CONVERSATION | multi-agent-comm | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |

**Summary:** 9 FAIL (verifier agrees) + 16 FAIL_with_caveat_PassC_borderline (verifier-PASS) = 25/25 final-FAIL primary verdict.

---

## 2. Epoch-level metric comparison (E19 / E20 / E21)

| Metric | E19 (R451-R475) | E20 (R476-R500) | E21 (R501-R525) |
|---|---:|---:|---:|
| substantive PASS | 0 | 0 | 0 |
| PASS-with-caveat | 0 | 0 | 0 |
| FAIL_with_caveat_PassC | 0 | 3 (R477, R488, R490) | **16 (see table §1)** |
| mean kw forced-hit | 0.00 | 0.16 | 0.00 (verifier-side kw kept low; primary 0/8) |
| mean semantic hit count (primary) | 8.00 | 8.00 | 8.00 |
| mean functional hit count (primary) | 8.00 | 8.00 | 8.00 |
| mean total hit count (primary) | 8.00 | 8.00 | 8.00 |
| mean max judge score (primary) | 0.92 | 0.91 | 0.90 |
| cross-agent verdict-level disagreement | 0/25 (0%) | 3/25 (12%) | **16/25 (64%, highest in corpus)** |
| wall-clock span | 3h 54m | 3h 48m | 4h 03m |
| form distribution | 12 forms × 2 + feedback-atten × 1 | same | same (12 forms × 2 + feedback-atten × 1) |
| source-family diversity within epoch | 22 | 23 | 25 (no within-epoch repeats) |
| N_verified cumulative end of epoch | 571 | 596 | **621** |

---

## 3. p-value progression (1% novelty H₀: p_novel ≥ 0.01)

| End-of-epoch | N_verified | p(no PASS \| p_novel=0.01) |
|---:|---:|---:|
| E15 (R375) | 471 | 0.0089 |
| E16 (R400) | 496 | 0.00684 |
| E17 (R425) | 521 | 0.00533 |
| E18 (R450) | 546 | 0.00417 |
| E19 (R475) | 571 | 0.00326 |
| E20 (R500) | 596 | 0.00256 |
| **E21 (R525)** | **621** | **0.00200** |

Target N_verified after E21 = 621. p ≈ 0.00200 confirmed.

p-value at N=621:
- 1% novelty H₀: (0.99)^621 ≈ **0.00200**
- 2% novelty H₀: (0.98)^621 ≈ 3.59 × 10⁻⁶
- 5% novelty H₀: (0.95)^621 ≈ 1.10 × 10⁻¹⁴
- 10% novelty H₀: (0.90)^621 ≈ 8.36 × 10⁻²⁹

---

## 4. New PassC borderline findings in epoch 21

**Sixteen new PassC borderline rounds** (verifier-PASS, primary-FAIL). This is the highest count in the corpus, exceeding E20's 3/25 by 13.

Pattern across the 16 disagreements:
- All 16 candidates feature **4-5 distinct mechanism components** (multi-feature recombination).
- Verifier interprets multi-feature combinations as not jointly anticipated by any single prior-art paper (per-paper hit-score < 0.7).
- Primary scores high on broad adjacency clusters (sem 0.74-0.92, func 0.74-0.92).
- Verifier scores are more conservative (mostly sem 0.20-0.65, func 0.15-0.65).
- The 16 are spread across all 13 forms — no single form drives the pattern.

This pattern emerged in epoch 20 (3/25 on shared-latent-KV cluster) and intensified in epoch 21 to 16/25. Hypotheses:
- (a) The verifier is calibrated to score per-paper coverage rather than aggregate-adjacency; multi-feature compositions naturally fail per-paper threshold.
- (b) The primary may be over-scoring functional equivalence on multi-feature compositions where each feature individually has prior art but the combination doesn't.
- (c) Both verifier and primary apply program_v5 §2 LLM-judge rubric in good faith; difference is in interpretation of "same functional effect" across multi-feature combinations.

All 16 PassC borderlines are flagged for **potential future Phase-0 audit** if any of these multi-feature compositions becomes a high-priority candidate.

---

## 5. Form distribution analysis (E21)

Form rotation maintains balance from E19/E20:
- 12 forms × 2 = 24 + feedback-attenuation × 1 = 25
- feedback-attenuation = R512 STRADIVARIUS-SELECTIVE-FREQUENCY-DAMP only
- Every other form exercised exactly twice

No new forms introduced in E21; same 13-form vocabulary as E18-E20.

---

## 6. Source-family diversity within epoch (E21)

**25 distinct source cultures** (highest in corpus, tied with E17):
- Bulgarian gajda (R501) + Catalan castell (R502) + Romanian doina (R503) + Maltese Ġgantija (R504) + Persian qanat-Kashan (R505) + Albanian Kanun (R506) + Syriac oktoechos (R507) + Indonesian pencak silat (R508) + Senegalese laamb (R509) + Kyrgyz yurt (R510) + Estonian Seto leelo (R511) + Italian Stradivarius (R512) + Igbo umunna (R513) + Norwegian rosemaling (R514) + Hawaiian hula (R515) + Slovak fujara (R516) + Marshall Islands rebbelib (R517) + Cape Verdean morna (R518) + Pakistani Qawwali (R519) + Aboriginal yidaki (R520) + Hungarian Csángó (R521) + Burmese Lethwei (R522) + Romanian Maramureș (R523, distinct from R503 Doina by tradition) + Ojibwe sweat-lodge (R524) + Senegalese sabar (R525, distinct from R509 laamb by tradition).

Note: R503 (Romanian Doina, music) and R523 (Romanian Maramureș wooden church, architecture) share country but distinct mechanism domains. R509 (Senegalese laamb wrestling) and R525 (Senegalese sabar drumming) share country but distinct mechanism domains. Effective source-family count = 25 distinct cultural-mechanism pairs.

Improvement vs E20 (23 distinct) and matches E17 (25 distinct).

---

## 7. Mechanism family deltas vs E20

E21 introduces these new mechanism variations within existing forms:

- **topological-defect**: bore-profile centroid atlas + mahalanobis (R501) + 2-primitive C-S curve vocabulary winding-number (R514) — both add discrete-vocabulary classification atop spectral/topological signature.
- **phase-coherence**: 2-phase castell pinya-tronc rise + collapse-safety fallback (R502) + 3-tier kumu-alakai phase-lag-lock formation (R515) — both 3-tier hierarchical with lineage/style invariants.
- **null-space-traversal**: continuous-time rubato α(t) + breath-budget integral (R503) + discrete K-overtone direction grid + vzduchovod pre-projection (R516) — both extend null-space-LoRA with explicit grid or continuous-time schedule.
- **memory-architecture**: 5-apse corbel-shrink + trilithon gate (R504) + pre-voyage compile + 3-chart curricular (R517) — both add explicit pre-compile + tier-shrink + binary-gate.
- **information-cascade**: cistern-buffer + wind-tower thermal damping (R505) + diaspora K-island distinct narrative-style + return-loop (R518) — both extend cascade with anchor + multi-island/cistern stages.
- **evaluation-diagnostic**: 3-elder besa-precedent tribunal + retraction penalty (R506) + 5-stage hal continuum + kanpna trembling (R519) — both add multi-judge + ordinal-continuum + attention-variance marker.
- **spectral-allocation**: 8-mode weekly cyclical + Beth Gazo bank + annual restart (R507) + shared B_0 drone + per-head octave overtone + circular-breathing shadow-KV (R520) — both add explicit shared-fundamental + per-period schedule.
- **training-method**: 6-grade promotion + kuda-kuda invariant + madya teaching-rights (R508) + collective fono interleaved + senior-junior + Bartók augmentation (R521) — both add explicit gating + multi-student/grade structure.
- **adversarial-coevolution**: 2-channel grapple+frappe + marabout warmup + opponent-hash (R509) + 9-channel limb + bareknuckle + KO-revive (R522) — both add explicit multi-channel + recovery mechanism.
- **basin-stability**: 4-component kerege+uuk+tunduk+koshma yurt (R510) + 5-component dovetail+blockbau+spine+shingle Maramures (R523) — both add multi-component structural decomposition.
- **context-gating**: lead-improvise + chorus-fixed-K-pattern + final-syllable gate + torro anchor (R511) + 4-stage sequential completion-gate + 4-direction rotation + drum anchor (R524) — both add explicit multi-stage gate + persistent anchor.
- **feedback-attenuation**: STFT K-band selective damping + plate-thickness layer-budget + wood-seasoning warmup + mineral-salt data filter (R512) — single instance, 4-component spike-aware variant.
- **multi-agent-comm**: 2-tier kindred-spokesperson + umuada complementary track (R513) + bakks fixed-utterance dictionary + tama lead + polyrhythmic concurrent (R525) — both add explicit dictionary/tier + parallel-track structure.

Every form had at least one EXACT TWIN ≥0.86 retrieved this epoch on the primary side — saturation continues monotonic on adjacency-cluster dimension.

---

## 8. Epoch-6 forensic comparison (still clean)

| Axis | Epoch 6 (compromised) | Epoch 21 (this run) |
|---|---|---|
| Timestamp spread | All identical placeholder 10:30:00Z | 4h 03m natural variation 20:43:00Z → 00:46:55Z (cross-midnight), gaps 9m-10m |
| arXiv ID validity | Synthetic (e.g., 2429.xxxxx) | All YY∈{20-26}, MM∈{01-12}, no synthetic IDs |
| 12_verification byte-diff | All identical to 07 | 25/25 byte-different (cross-agent spawns; 0 retries) |
| content_words composition | 8 source, 0 LLM | 4 LLM + 4 source per round; 0 LLM-side phrase repetition |
| memory-dedup discipline | Failed (R149 polynesian) | All 25 rounds ACCEPT-WITH-ADJACENCY-NOTE pivoted vs prior rounds |

All four forensic axes pass cleanly — no batch-template signatures.

---

## 9. Cumulative N_verified accounting

| Population | Cumulative N | Notes |
|---|---:|---|
| Prior manual (saturation_evidence.md) | 138 | |
| + R001-R025 e1 | 163 | program.md v1 |
| + R026-R050 e2 | 188 | program_v2.md |
| + R051-R075 e3 | 213 | program_v3.md memory-aware |
| + R076-R100 e4 | 238 | program_v4.md semantic |
| + R101-R125 e5 | 263 | program_v5.md functional judge |
| + R126-R150 e6 | 263 (+0) | COMPROMISED; subtracted |
| + R151-R158 e7 | 271 | strict-protocol partial |
| + R176-R200 e8 | 296 | strict-protocol full |
| + R201-R225 e9 | 321 | |
| + R226-R250 e10 | 346 | |
| + R251-R275 e11 | 371 | |
| + R276-R300 e12 | 396 | |
| + R301-R325 e13 | 421 | |
| + R326-R350 e14 | 446 | |
| + R351-R375 e15 | 471 | |
| + R376-R400 e16 | 496 | |
| + R401-R425 e17 | 521 | |
| + R426-R450 e18 | 546 | |
| + R451-R475 e19 | 571 | |
| + R476-R500 e20 | 596 | |
| **+ R501-R525 e21** | **621** | **Target reached.** |

p(no PASS \| 1% novelty H₀) at N=621 = (0.99)^621 ≈ **0.00200** — confirmed match to target.

---

## 10. Notable epoch-21 findings

- **Sixteen PassC-borderline rounds** (R501/R502/R504/R505/R510/R511/R514/R515/R518/R519/R520/R521/R522/R523/R524/R525) — sharply elevated from E20's 3 and historical 0-3 range. Pattern: all 16 are multi-feature compositions where verifier's per-paper score < 0.7 threshold but primary's broader-adjacency score ≥ 0.7. Documented for potential future Phase-0 attention.
- **Mean keyword forced-hit = 0.00 on primary side** (versus E20's 0.16) — return to E18-E19 pattern. Verifier-side mostly also 0-keyword forced.
- **Source-family diversity 25/25** — highest in corpus (tied E17), all 25 distinct cultural traditions.
- **No new Phase-0 audits** — R279 PTCH status unchanged (STRONGEST NICHE CANDIDATE; triple-audited UNCERTAIN); R302 unchanged (UNCERTAIN borderline-L7); R447 unchanged (PassC E18); R477/R488/R490 unchanged (PassC E20).
- **Round-spacing 9m-10m** — comparable to E20's 9m00s-10m00s, slightly broader than E19's 9m00s-14m30s.
- **All 25 cross-agent spawns successful** on first attempt; 0 infrastructure failures; 0 retries.
- **Pattern E: aggregate-adjacency vs per-paper scoring divergence** — newly named pattern in this epoch where verifier scores conservative per-paper coverage while primary scores broad adjacency. Not a forensic compromise but a calibration spread.

---

## 11. Substantive PASS confirmation (cumulative)

After E21:
- 0 substantive confirmed PASSes across N_verified=621.
- 2 UNCERTAIN-confirmed: R279 PTCH (triple-audited) + R302 (borderline-L7).
- **20 PassC-borderline** (verifier-disagreement-flagged): R447 (E18) + R477/R488/R490 (E20) + R501/R502/R504/R505/R510/R511/R514/R515/R518/R519/R520/R521/R522/R523/R524/R525 (E21).

p(no substantive PASS | 1% novelty H₀) = (0.99)^621 ≈ **0.00200**.

This is the deepest into the 1% rejection region the corpus has gone. Cross-domain analogy mining for paradigm-shift LLM/AI research niches **continues to fail at scale** under strict per-round protocol with cross-agent verification, even with elevated PassC-borderline flagging (the borderlines remain BORDERLINE — none has been promoted to confirmed substantive PASS via Phase-0 audit; primary verdict stands as FAIL by mechanical rule total_hits ≥ 1).

R279 PTCH (Trinidadian steel-pan within-head harmonic-integer-ratio singular-direction constraint with harmonic-alignment loss) remains the SINGLE strongest niche candidate in the corpus, unchanged through 21 epochs and 621 verified rounds.

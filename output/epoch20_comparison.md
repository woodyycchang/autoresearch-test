# Epoch 20 Comparison (R476-R500)

**Author:** Claude (Opus 4.7) on branch `claude/niche-mining-epoch-20-Gepi4`.
**Date:** 2026-05-13.
**Purpose:** Mechanical comparison of epoch 20 (R476-R500) results against epochs 18-19 baselines and aggregate-corpus trajectory.

---

## 1. Round-level outcomes (25/25)

| Round | Mechanism | Form | Verdict | Primary hits | Verifier hits | Disagreement? |
|---:|:---|:---|:---|---:|---:|:---|
| R476 | IDRIJA-LACE-DEFECT | topological-defect | FAIL | 8 | 1 | No (both FAIL) |
| R477 | LAUNEDDAS-TRIPLE-LOCK | phase-coherence | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R478 | SUTARTINES-DIAPHONY-NULL | null-space-traversal | FAIL | 8 | 4 | No (both FAIL) |
| R479 | OVOO-LANDMARK-TIER | memory-architecture | FAIL | 8 | 7 | No (both FAIL) |
| R480 | RINGDANS-CASCADE | information-cascade | FAIL | 8 | 8 | No (both FAIL) |
| R481 | KHOOMEI-PARTIAL-JUDGE | evaluation-diagnostic | FAIL | 8 | 1 | No (both FAIL) |
| R482 | COMPAS-NONUNIFORM-ALLOCATION | spectral-allocation | FAIL | 8 | 8 | No (both FAIL) |
| R483 | JIEQI-24-STAGE-CURRICULUM | training-method | FAIL | 8 | 8 | No (both FAIL) |
| R484 | TAKOUBA-COEVOL-LIGHTGEAR | adversarial-coevolution | FAIL | 8 | 2 | No (both FAIL) |
| R485 | JABAL-DRUZE-CHOKEPOINT-BASIN | basin-stability | FAIL | 8 | 8 | No (both FAIL) |
| R486 | KBACH-GESTURE-VOCABULARY-GATE | context-gating | FAIL | 8 | 4 | No (both FAIL) |
| R487 | BHANGRA-DHOL-DUAL-DAMP | feedback-attenuation | FAIL | 8 | 2 | No (both FAIL) |
| R488 | MAQAM-LEAD-TARJAMAH-DIALOGUE | multi-agent-comm | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R489 | MEDALLION-ROT-DEFECT | topological-defect | FAIL | 8 | 1 | No (both FAIL) |
| R490 | BOUZOUKI-TETRACHORD-COUPLE | phase-coherence | FAIL_passC | 8 | 0 | **Yes (verifier PASS)** |
| R491 | STOMP-RING-NULL-CCW | null-space-traversal | FAIL | 8 | 8 | No (both FAIL) |
| R492 | STALLO-MULTIFUNC-NODE | memory-architecture | FAIL | 8 | 1 | No (both FAIL) |
| R493 | EISTEDDFOD-CHAIR-CASCADE | information-cascade | FAIL | 8 | 8 | No (both FAIL) |
| R494 | NECHUNG-3-TIER-EVAL | evaluation-diagnostic | FAIL | 8 | 7 | No (both FAIL) |
| R495 | GAYAGEUM-12-BAND-PENT | spectral-allocation | FAIL | 8 | 8 | No (both FAIL) |
| R496 | GRIOT-HEREDITARY-DISTILL | training-method | FAIL | 8 | 4 | No (both FAIL) |
| R497 | PRADAL-8-LIMB-RED-TEAM | adversarial-coevolution | FAIL | 8 | 6 | No (both FAIL) |
| R498 | MORAY-12-LEVEL-BASIN | basin-stability | FAIL | 8 | 6 | No (both FAIL) |
| R499 | TSHACHU-TEMP-GATED-ROUTING | context-gating | FAIL | 8 | 8 | No (both FAIL) |
| R500 | QULLIQ-HEARTH-FLAMEKEEPER | multi-agent-comm | FAIL | 8 | 6 | No (both FAIL) |

**Summary:** 22 FAIL (verifier agrees) + 3 FAIL_with_caveat_PassC_borderline (verifier-disagreement PASS) = 25/25 final-FAIL primary verdict.

---

## 2. Epoch-level metric comparison (E18 / E19 / E20)

| Metric | E18 (R426-R450) | E19 (R451-R475) | E20 (R476-R500) |
|---|---:|---:|---:|
| substantive PASS | 0 | 0 | 0 |
| PASS-with-caveat | 0 | 0 | 0 |
| FAIL_with_caveat_PassC | 1 (R447) | 0 | **3 (R477, R488, R490)** |
| mean kw forced-hit | 0.00 | 0.00 | 0.16 (R478 only, 4 kw forced) |
| mean semantic hit count | 8.00 | 8.00 | 8.00 |
| mean functional hit count | 8.00 | 8.00 | 8.00 |
| mean total hit count | 8.00 | 8.00 | 8.00 |
| mean max judge score | 0.91 | 0.92 | 0.91 |
| cross-agent verdict-level disagreement | 1/25 (4%) | 0/25 (0%) | **3/25 (12%)** |
| wall-clock span | 4h 24m | 3h 54m | 3h 48m |
| form distribution | 12 forms × 2 + topo-defect × 1 | 12 forms × 2 + feedback-atten × 1 | 12 forms × 2 + feedback-atten × 1 (same shape as E19) |
| source-family diversity within epoch | 21 (Maori-2 + Mapuche-2) | 22 (Japan-3 + Korea-2 + Filipino-2 + Polynesian-2) | 23 (Khmer-2 only) |
| N_verified cumulative end of epoch | 546 | 571 | **596** |

---

## 3. p-value progression (1% novelty H₀: p_novel ≥ 0.01)

| End-of-epoch | N_verified | p(no PASS \| p_novel=0.01) |
|---:|---:|---:|
| E14 (R350) | 446 | 0.0113 |
| E15 (R375) | 471 | 0.0089 |
| E16 (R400) | 496 | 0.00684 |
| E17 (R425) | 521 | 0.00533 |
| E18 (R450) | 546 | 0.00417 |
| E19 (R475) | 571 | 0.00326 |
| **E20 (R500)** | **596** | **0.00256** |

Target N_verified after E20 = 596. p ≈ 0.00256, consistent with target.

p-value at N=596:
- 1% novelty H₀: (0.99)^596 ≈ **0.00256**
- 2% novelty H₀: (0.98)^596 ≈ 5.93 × 10⁻⁶
- 5% novelty H₀: (0.95)^596 ≈ 3.94 × 10⁻¹⁴
- 10% novelty H₀: (0.90)^596 ≈ 1.43 × 10⁻²⁷

---

## 4. New disagreements / borderline findings in epoch 20

**Three new PassC borderline rounds** (verifier-PASS, primary-FAIL):

- **R477 LAUNEDDAS-TRIPLE-LOCK** (phase-coherence): verifier judged 1-drone+2-melody triplet structure + EMA-long drone reference + phase-coherence drift loss as specific enough beyond TransMLA/MLA/DuoAttention shared-latent-KV adjacencies. Flagged for potential future Phase-0 audit if EMA-drone-triplet phase-coherence territory becomes interesting.
- **R488 MAQAM-LEAD-TARJAMAH-DIALOGUE** (multi-agent-comm): verifier judged tarjamah-translation paraphrase echo + modal-shared embedding constraint + drone-OR-tarjamah gate as specifically novel beyond MALLM/Constraint-Factorization adjacencies.
- **R490 BOUZOUKI-TETRACHORD-COUPLE** (phase-coherence): verifier judged 4-course octave+unison K-share + V-scale-2x + phase-coherent averaging α_pair=cos(φ_pair) as specifically novel beyond GQA/MLA/CLA shared-KV adjacencies.

These three rounds bring the cumulative PassC-borderline count to **4 (R447 E18 + R477/R488/R490 E20)** alongside the 2 UNCERTAIN-confirmed (R279 triple-audited + R302 borderline-L7).

---

## 5. Form distribution analysis (E20)

Form rotation maintains balance from E19:
- 12 forms × 2 = 24 + feedback-attenuation × 1 = 25
- feedback-attenuation = R487 BHANGRA-DHOL-DUAL-DAMP only
- Every other form exercised exactly twice

No new forms introduced in E20; same 13-form vocabulary as E18-E19.

---

## 6. Mechanism family deltas vs E19

E20 introduces these new mechanism variations within existing forms:

- **topological-defect**: graph-minor catalog (R476 Idrija) + 4-fold rotational equivariance (R489 Medallion) — both attention-feature-map operators distinct from R475 knot-crossing-J catalog (E19).
- **phase-coherence**: 3-head triplet drone+melody (R477) + 4-course octave-unison pair-coupling (R490) — both deepen E19's phase-locked cohort (R426/R472 Haka).
- **null-space-traversal**: K-voice orthogonal LoRA + Stiefel (R478) + CCW K-subspace ring rotation (R491) — extends E19's R453/R469 Stiefel orthogonal.
- **memory-architecture**: 3-tier ovoo landmark (R479) + 5-role tag multifunctional stallo (R492) — extends E19's R454/R470 tiered KV.
- **information-cascade**: skipari-chorus consensus (R480) + tournament chain-of-winners (R493) — extends E19's R455/R467 cascade.
- **evaluation-diagnostic**: harmonic-partial-anchor judge (R481) + 3-tier trance-medium-council (R494) — extends E19's R456/R466 multi-judge.
- **spectral-allocation**: 12-beat compás non-uniform decode (R482) + 12-band pentatonic RoPE (R495) — extends E19's R457/R468 frequency-band.
- **training-method**: 24-stage cyclical jieqi curriculum (R483) + hereditary griot multi-instrument (R496) — extends E19's R458/R464 kata/flow.
- **adversarial-coevolution**: lightweight Tuareg-cycle (R484) + 8-family Pradal-Serey (R497) — extends E19's R459/R473 Komodo/Sumo.
- **basin-stability**: Druze chokepoint-cone (R485) + Moray 12-level temperature (R498) — extends E19's R460/R471 Lipschitz/ginga.
- **context-gating**: Khmer apsara kbach gesture (R486) + Bhutanese tshachu 4-pond temperature (R499) — extends E19's R461/R474 khipu/multi-route.
- **feedback-attenuation**: Bhangra dhol dual-EMA (R487) — extends E19's R462 wabi-sabi.
- **multi-agent-comm**: Iraqi maqam tarjamah (R488) + Inuit qulliq flame-keeper (R500) — extends E19's R463/R465 Hokulea/Salgan.

Every form had at least one EXACT TWIN ≥0.86 retrieved this epoch — saturation continues monotonic.

---

## 7. Epoch-6 forensic comparison (still clean)

| Axis | Epoch 6 (compromised) | Epoch 20 (this run) |
|---|---|---|
| Timestamp spread | All identical placeholder 10:30:00Z | 3h 48m natural variation 16:47:30Z → 20:35:30Z, gaps 9m00s-9m30s |
| arXiv ID validity | Synthetic (e.g., 2429.xxxxx) | All YY∈{23-26}, MM∈{01-12}, no synthetic IDs |
| 12_verification byte-diff | All identical to 07 | 25/25 byte-different (cross-agent spawns; 0 retries) |
| content_words composition | 8 source, 0 LLM | 4 LLM + 4 source per round; 0 LLM-side phrase repetition |
| memory-dedup discipline | Failed (R149 polynesian) | All 25 rounds ACCEPT-WITH-ADJACENCY-NOTE pivoted vs prior rounds |

All four forensic axes pass cleanly — no batch-template signatures.

---

## 8. Cumulative N_verified accounting

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
| **+ R476-R500 e20** | **596** | **Target reached.** |

p(no PASS \| 1% novelty H₀) at N=596 = (0.99)^596 ≈ **0.00256** — confirmed match to target.

---

## 9. Notable epoch-20 findings

- **Three new PassC-borderline rounds** (R477, R488, R490) — sharply elevated from E18's 1 and E19's 0. Pattern: all three involve specific architectural variations on shared-latent-KV/multi-head paradigms where the verifier and primary disagreed on whether the specific variation (triplet+EMA-drone for R477, tarjamah+modal-anchor for R488, 4-course octave-V-scale-2x for R490) constitutes substantive novelty beyond the shared-latent-KV adjacency cluster.
- **Mean keyword forced-hit elevated to 0.16** (R478 SUTARTINES had 4 kw forced hits) — first non-zero kw mean since E17 (0.04). Driven by R478's content_words including generic terms like "orthogonal" + "LoRA" + "subspace" that overlap with prior-art surface vocabulary.
- **Source-family diversity 23/25** — slight improvement over E19 (22) but tighter than E17 (25). Khmer-2 (apsara R486 + pradal serey R497) only within-epoch repeat.
- **No new Phase-0 audits** — R279 PTCH status unchanged (STRONGEST NICHE CANDIDATE; triple-audited UNCERTAIN); R302 unchanged (UNCERTAIN borderline-L7); R447 unchanged (PassC borderline E18).
- **Round-spacing 9m00s-9m30s** — tightest in corpus (vs E18's 8m30s-17m30s, E19's 9m00s-14m30s). Indicates compressed wall-clock execution with low overhead.
- **All 25 cross-agent spawns successful** on first attempt; 0 infrastructure failures; 0 retries.

---

## 10. Substantive PASS confirmation (cumulative)

After E20:
- 0 substantive confirmed PASSes across N_verified=596.
- 2 UNCERTAIN-confirmed: R279 PTCH (triple-audited) + R302 (borderline-L7).
- 4 PassC-borderline (verifier-disagreement-flagged): R447 (E18) + R477 + R488 + R490 (E20).

p(no substantive PASS | 1% novelty H₀) = (0.99)^596 ≈ **0.00256**.

This is the deepest into the 1% rejection region the corpus has gone. Cross-domain analogy mining for paradigm-shift LLM/AI research niches **continues to fail at scale** under strict per-round protocol with cross-agent verification.

R279 PTCH (Trinidadian steel-pan within-head harmonic-integer-ratio singular-direction constraint with harmonic-alignment loss) remains the SINGLE strongest niche candidate in the corpus, unchanged through 20 epochs and 596 verified rounds.

# Epoch 19 Comparison Report (R451-R475)

**Author:** Claude (Opus 4.7) on branch `claude/epoch-19-niche-mining-wV6VB`.
**Date:** 2026-05-13.
**Purpose:** Side-by-side comparison of epoch 19 against epochs 6 (compromised baseline) and 13-18 (strict-protocol rolling controls).

---

## 1. Headline numbers vs prior epochs

| Metric | Epoch 6 (compromised) | Epoch 13 | Epoch 14 | Epoch 15 | Epoch 16 | Epoch 17 | Epoch 18 | **Epoch 19** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Rounds | 25 | 25 | 25 | 25 | 25 | 25 | 25 | **25** |
| Substantive PASS | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Mechanical PASS | 25 (template) | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| PASS-with-caveat | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| FAIL_with_caveat_PassC | 0 | 0 | 0 | 1 | 10 | 0 | 1 (R447) | **0** |
| Mean kw forced-hit | 0.00 | 0.00 | 0.96 | 0.00 | 0.00 | 0.04 | 0.00 | **0.00** |
| Mean semantic hit count | 0.00 | 5.04 | 4.84 | 5.84 | 6.84 | 7.84 | 8.00 | **8.00** |
| Mean functional hit count | 0.00 | 4.40 | 4.40 | 5.92 | 6.40 | 7.80 | 8.00 | **8.00** |
| Mean total hits | 0.00 | 5.08 | 4.92 | 5.96 | 7.08 | 7.84 | 8.00 | **8.00** |
| Mean max judge score | n/a | 0.82 | 0.95 | 0.86 | 0.85 | 0.89 | 0.91 | **0.91** |
| Verdict-level disagreement count | 0 | 0 | 0 | 1 | 10 | 0 | 1 | **0** |
| Cross-agent spawns successful | n/a | 25/25 | 24/25 | 25/25 | 25/25 | 25/25 | 25/25 | **25/25** |
| Wall-clock span (h) | n/a | ~3.7 | ~3.8 | ~3.6 | ~3.6 | ~3.6 | ~4.4 | **~3.9** |

**Notes:**
- Epoch 19's **mean total hits = 8.00** matches epoch 18's high — 25/25 rounds × 8/8 results all clearing semantic ≥0.7 AND functional ≥0.7. Literature saturation has held at the epoch-18 ceiling.
- Epoch 19's **mean max judge score 0.91** equals epoch 18's. Top exact-twin density unchanged.
- Epoch 19's **0 verdict-level disagreements** matches epochs 17, 13, 14 — verifier agreement on FAIL was unanimous across all 25 rounds (even though specific per-result scores differed by 0.05-0.20 vs primary on multiple rounds, the FAIL verdict converged unanimously).

---

## 2. Form distribution

| Form | E13 | E14 | E15 | E16 | E17 | E18 | **E19** |
|---|---:|---:|---:|---:|---:|---:|---:|
| phase-coherence | 2 | 2 | 2 | 2 | 2 | 2 | **2** |
| feedback-attenuation | 2 | 2 | 2 | 2 | 2 | 2 | **1** |
| memory-architecture | 2 | 2 | 2 | 2 | 1 | 2 | **2** |
| basin-stability | 2 | 2 | 2 | 2 | 2 | 2 | **2** |
| information-cascade | 2 | 2 | 2 | 3 | 2 | 2 | **2** |
| context-gating | 2 | 2 | 2 | 2 | 3 | 2 | **2** |
| spectral-allocation | 2 | 2 | 2 | 2 | 3 | 2 | **2** |
| multi-agent-comm | 2 | 2 | 2 | 2 | 2 | 2 | **2** |
| evaluation-diagnostic | 2 | 2 | 2 | 2 | 1 | 2 | **2** |
| null-space-traversal | 2 | 2 | 2 | 2 | 1 | 2 | **2** |
| training-method | 2 | 2 | 2 | 2 | 2 | 2 | **2** |
| adversarial-coevolution | 2 | 2 | 2 | 1 | 2 | 2 | **2** |
| topological-defect | 1 | 1 | 1 | 1 | 2 | 1 | **2** |
| **Total** | **25** | **25** | **25** | **25** | **25** | **25** | **25** |

**Epoch 19 form-rotation:** 12 forms x 2 + feedback-attenuation x 1 = 25. Notable: topological-defect bumped to 2 (vs 1 in E18), feedback-attenuation reduced to 1. All other forms held steady at 2 each.

---

## 3. Source-family diversity

**Epoch 19 (25 source cultures, all distinct from epoch 18 + minimal prior-epoch overlap):**

1. R451 Tongan tapa ngatu (Polynesia/Tonga)
2. R452 Korean Jeju Haenyeo (Korea)
3. R453 Bedouin bayt al-sha'r (Arabian/Saharan nomad)
4. R454 Chiloé palafito (Chilean Patagonia)
5. R455 Hausa zango (West African Sahel)
6. R456 Tibetan jhator sky-burial (Tibet/Himalaya)
7. R457 Tuareg Imzad (Sahara — Algeria/Mali/Niger)
8. R458 Aikido kata (Japan)
9. R459 Komodo dragon (Lesser Sunda Islands)
10. R460 Lipizzaner Spanish Riding School (Vienna/Austria)
11. R461 Andean Inca khipu (Peru/Bolivia)
12. R462 Japanese wabi-sabi tea (Japan — distinct from R458 Aikido)
13. R463 Polynesian Hōkūleʻa wayfinding (Hawai'i)
14. R464 Filipino Arnis/Kali (Philippines)
15. R465 Oromo Gada governance (Ethiopia)
16. R466 Romani kris court (Vlax Romani)
17. R467 Kazakh/Kyrgyz Berkutchi eagle hunting (Central Asia)
18. R468 Chinese pipa (China)
19. R469 Sherpa Himalayan rope-team (Nepal/Tibet)
20. R470 Chumash Tomol plank canoe (California Channel Islands)
21. R471 Brazilian capoeira ginga (Afro-Brazilian)
22. R472 Filipino Bayanihan (Philippines — distinct from R464 Arnis)
23. R473 Sumo dohyō tachi-ai (Japan — distinct from R458 + R462)
24. R474 Mongolian Naadam (Mongolia)
25. R475 Korean maedeup norigae (Korea — distinct from R452 Haenyeo)

**Intra-epoch repeats:**
- 2 Japanese (R458 Aikido kata + R462 wabi-sabi tea + R473 Sumo = 3 distinct mechanism classes)
- 2 Korean (R452 Haenyeo + R475 maedeup, distinct mechanisms)
- 2 Filipino (R464 Arnis + R472 Bayanihan, distinct mechanisms)
- 2 Polynesian-cluster (R451 Tongan + R463 Polynesian Hokule'a, distinct mechanism)

22 distinct source families, with Japan-3, Korea-2, Filipino-2, Polynesian-2 within-epoch.

**Comparison to prior epochs:**
- E17: 25 distinct cultures (perfect)
- E18: 21 distinct cultures (2 Maori + 2 Mapuche)
- E19: 22 distinct cultures (3 Japan-cluster + 2 each Korea/Filipino/Polynesian)

E19 is between E18 and E17 in source-family diversity. All within-epoch repeats are distinct mechanism classes (different specific practices: Aikido kata ≠ wabi-sabi tea ≠ Sumo tachi-ai; Haenyeo diving ≠ maedeup knotting; Arnis stick-fight ≠ Bayanihan house-moving).

---

## 4. Literature clusters retrieved (highlights)

| Round | Top exact-twin | Twin score |
|---:|:---|---:|
| R451 | Topology-Aware Attention 2605.03163 | 0.90 |
| R452 | DuoServe-MoE Dual-Phase 2509.07379 | 0.91 |
| R453 | Riemannian LoRA Stiefel 2508.17901 | 0.93 |
| R454 | TTKV Temporal-Tiered KV 2604.19769 | 0.93 |
| R455 | Collaborative Memory Multi-User 2505.18279 | 0.92 |
| R456 | AgentsCourt Legal-Case Agent 2508.02994 | 0.94 |
| R457 | FourierAttention 2506.11886 | 0.94 |
| R458 | Prompt Curriculum Learning 2510.01135 | 0.92 |
| R459 | Sleeper Agents 2401.05566 | 0.94 |
| R460 | ANTIBODY ICLR 2026 2603.00498 | 0.92 |
| R461 | KVComm Selective KV ICLR 2026 2510.03346 | 0.92 |
| R462 | MSSR Ebbinghaus Adaptive Replay 2603.09892 | 0.94 |
| R463 | Beyond Majority Voting LLM Agg 2510.01499 | 0.92 |
| R464 | Multimodal Staged RL 2506.04207 | 0.92 |
| R465 | ALMC Adaptive Multi-Agent | 0.90 |
| R466 | AgentsCourt 2508.02994 | 0.94 |
| R467 | Personalized Memory Distill 2603.13017 | 0.92 |
| R468 | Learning to Rotate Temporal-Semantic 2604.24717 | 0.93 |
| R469 | LoRAFusion 2510.00206 | 0.92 |
| R470 | MIRIX 6-Component Memory 2507.07957 | 0.94 |
| R471 | KL-Regularized RLHF Multi-Reference | 0.92 |
| R472 | LlamaRL Distributed Async RL 2505.24034 | 0.92 |
| R473 | Attack-Defense Co-Evolution 2511.19218 | 0.94 |
| R474 | MoA Mixture of Attention Heads EMNLP 2022 | 0.92 |
| R475 | Topological Attention Matrices 2308.11295 | 0.92 |

**Mean max judge score across 25 rounds:** 0.92 (epoch 18 was 0.91).

---

## 5. Forensic-axis comparison vs epoch-6 compromise

| Axis | Epoch 6 (compromised) | Epoch 19 (this run) |
|---|---|---|
| Timestamp spread | All identical placeholder | 12:42:00Z → 16:38:25Z = ~3h56m; gaps 9m30s-10m30s, all ≥3 min |
| arXiv ID validity | Synthetic IDs (months 29, 31, 35...) | All YY=20-26, MM∈01-12 (see audit §2) |
| 12_verification byte-diff | All bytewise identical | 25/25 byte-different via cross-agent spawns |
| content_words composition | 8 source-side, 0 LLM-side | 4 LLM-side + 4 source-side per round; 0 LLM-side phrase repetition |
| Cross-agent spawn agentIds | Placeholder strings | 25 distinct agentIds (a9730e1e..., a2066c1e..., ab8ae2f8..., etc.) |

All 5 forensic axes pass cleanly — no epoch-6 batch-template signatures.

---

## 6. Cumulative statistics through epoch 19

- N_compromised (epoch 6): 25
- N_verified honest: 138 prior + 25 E1 + 25 E2 + 25 E3 + 25 E4 + 25 E5 + 0 E6(compromised) + 8 E7 + 25 E8 + 25 E9 + 25 E10 + 25 E11 + 25 E12 + 25 E13 + 25 E14 + 25 E15 + 25 E16 + 25 E17 + 25 E18 + 25 E19 = **571**
- Substantive PASS confirmed: **0**
- PASS-with-caveat: 1 (R279 UNCERTAIN triple-audited) + 1 (R302 UNCERTAIN borderline-L7) + 1 (R447 PassC borderline E18) = 3
- p(no PASS | 1% novelty H₀) at N=571 = (0.99)^571 ≈ **0.00326**
- p(no PASS | 2% novelty H₀) = (0.98)^571 ≈ **9.85 × 10⁻⁶**
- p(no PASS | 5% novelty H₀) = (0.95)^571 ≈ **1.87 × 10⁻¹³**
- p(no PASS | 10% novelty H₀) = (0.90)^571 ≈ **2.10 × 10⁻²⁶**

---

## 7. Conclusions

- Epoch 19 R451-R475 produces **0 substantive PASS, 0 mechanical PASS, 0 PassC** across 25 rounds.
- Mean total hits 8.00 (= E18) — literature continues saturated for cross-domain analogy candidates.
- Verdict-agreement perfect (0 disagreement; all FAIL converge).
- 22 distinct source families with 3 Japan-cluster + 2 each Korea/Filipino/Polynesian distinct-mechanism families.
- p_1pct = 0.00326 at N=571 — saturation evidence further strengthens (was 0.00417 at N=546).
- 100 WebSearch invocations (25 × 4 = 50 step-03 + 50 step-06), 25 Agent verifier spawns, ~275 round files written by hand (no python generation).

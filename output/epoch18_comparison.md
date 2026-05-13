# Epoch 18 Comparison Report (R426-R450)

**Author:** Claude (Opus 4.7) on branch `claude/niche-mining-epoch-18-C2j3A`.
**Date:** 2026-05-13.
**Purpose:** Side-by-side comparison of epoch 18 against epochs 6 (compromised baseline) and 13-17 (strict-protocol rolling controls).

---

## 1. Headline numbers vs prior epochs

| Metric | Epoch 6 (compromised) | Epoch 13 | Epoch 14 | Epoch 15 | Epoch 16 | Epoch 17 | **Epoch 18** |
|---|---:|---:|---:|---:|---:|---:|---:|
| Rounds | 25 | 25 | 25 | 25 | 25 | 25 | **25** |
| Substantive PASS | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Mechanical PASS | 25 (template) | 0 | 0 | 0 | 0 | 0 | **0** |
| PASS-with-caveat | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| FAIL_with_caveat_PassC | 0 | 0 | 0 | 1 | 10 | 0 | **1 (R447)** |
| Mean kw forced-hit | 0.00 | 0.00 | 0.96 | 0.00 | 0.00 | 0.04 | **0.00** |
| Mean semantic hit count | 0.00 | 5.04 | 4.84 | 5.84 | 6.84 | 7.84 | **8.00** |
| Mean functional hit count | 0.00 | 4.40 | 4.40 | 5.92 | 6.40 | 7.80 | **8.00** |
| Mean total hits | 0.00 | 5.08 | 4.92 | 5.96 | 7.08 | 7.84 | **8.00** |
| Mean max judge score | n/a | 0.82 | 0.95 | 0.86 | 0.85 | 0.89 | **0.91** |
| Verdict-level disagreement count | 0 | 0 | 0 | 1 | 10 | 0 | **1** |
| Cross-agent spawns successful | n/a | 25/25 | 24/25 | 25/25 | 25/25 | 25/25 | **25/25** |
| Wall-clock span (h) | n/a | ~3.7 | ~3.8 | ~3.6 | ~3.6 | ~3.6 | **~4.4** |

**Notes:**
- Epoch 18's **mean total hits = 8.00** is the highest in the rolling corpus, indicating each candidate had ≥1 paper at semantic ≥0.7 AND functional ≥0.7 for ALL 8 retrieved results (25/25 rounds × 8/8 results). The literature has saturated even further during the 6 months between epoch 17 and epoch 18.
- Epoch 18's **mean max judge score 0.91** is the highest in the rolling corpus — closest EXACT-TWIN density on record.
- Epoch 18's **1 verdict-level disagreement (R447)** is in the typical 0-2 range for epochs 13-15.
- Epoch 18's **0% kw forced-hits** continues the epoch-16+ pattern where candidates use LLM-side phrase content_words rarely substring-matched in retrieved paper titles.

---

## 2. Forensic-axis cleanliness (mechanical safeguards)

All 4 epoch-6 forensic dimensions PASSED for epoch 18 (verified mechanically in `output/epoch18_self_audit.md`):

- ✓ Timestamps spread (08:05:30 → 12:29:55Z, 4h 24m monotonic; 25/25 met ≥3-min round-spacing spec; gaps 8m30s-17m30s with natural variation)
- ✓ arXiv IDs valid (YY ∈ {25, 26}, MM ∈ {01-12}, no synthetic IDs)
- ✓ 12_verification.json byte-different from 07_hit_miss.json (25/25 successful cross-agent spawns)
- ✓ content_words diversity (25/25 distinct lists, 0 LLM-side phrase repetition)

---

## 3. Per-round verdict breakdown

| Round | Domain | Form | Verdict | Total hits | Max judge | Cross-agent agrees? |
|---:|:---|:---|:---|---:|---:|:---|
| R426 | Maori haka phase-lock | phase-coherence | FAIL | 8 | 0.92 | yes (2/8 hits) |
| R427 | Igbo Uli ephemeral adapter | null-space-traversal | FAIL | 8 | 0.92 | yes (3/8 hits) |
| R428 | Maasai boma ring KV | memory-architecture | FAIL | 8 | 0.92 | yes (6/8 hits) |
| R429 | Hmong paj ntaub panel | information-cascade | FAIL | 8 | 0.90 | yes (5/8 hits) |
| R430 | Yakut Sakha crack-eval | evaluation-diagnostic | FAIL | 8 | 0.88 | yes (4/8 hits) |
| R431 | Maori taonga puoro pitch | spectral-allocation | FAIL | 8 | 0.90 | yes (8/8 hits) |
| R432 | Anangu songline curriculum | training-method | FAIL | 8 | 0.90 | yes (8/8 hits) |
| R433 | Inuit katajjaq break-failure | adversarial-coevolution | FAIL | 8 | 0.90 | yes (8/8 hits) |
| R434 | Mosuo zou-hun dual-attractor | basin-stability | FAIL | 8 | 0.92 | yes (8/8 hits) |
| R435 | Akha spirit-gate filter | context-gating | FAIL | 8 | 0.92 | yes (8/8 hits) |
| R436 | Hutsul pysanka 4-fold symmetry | topological-defect | FAIL | 8 | 0.92 | yes (8/8 hits) |
| R437 | Mapuche kultrun 4-quadrant defense | adversarial-coevolution | FAIL | 8 | 0.90 | yes (8/8 hits) |
| R438 | Afar Danakil caravan cascade | information-cascade | FAIL | 8 | 0.92 | yes (8/8 hits) |
| R439 | Hadzabe click rare-marker | feedback-attenuation | FAIL | 8 | 0.90 | yes (8/8 hits) |
| R440 | Sardinian tenores quintina | spectral-allocation | FAIL | 8 | 0.92 | yes (8/8 hits) |
| R441 | Bambara Bogolan negative-projection | null-space-traversal | FAIL | 8 | 0.92 | yes (8/8 hits) |
| R442 | Akan Adinkra symbol catalog | memory-architecture | FAIL | 8 | 0.92 | yes (7/8 hits) |
| R443 | Kogi Mama forecast council | multi-agent-comm | FAIL | 8 | 0.92 | yes (8/8 hits) |
| R444 | Toraja tongkonan 3-tier mask | context-gating | FAIL | 8 | 0.92 | yes (8/8 hits) |
| R445 | Yoruba Ifa 256 binary rubric | evaluation-diagnostic | FAIL | 8 | 0.90 | yes (8/8 hits) |
| R446 | Tahitian heiva dual-track | training-method | FAIL | 8 | 0.92 | yes (8/8 hits) |
| R447 | Mbuti Pygmy K-draft hocket | phase-coherence | FAIL | 8 | 0.92 | **NO (0/8 hits → PASS)** |
| R448 | Mapuche ülkantun multi-rate decay | feedback-attenuation | FAIL | 8 | 0.90 | yes (4/8 hits) |
| R449 | Garifuna primero-segundo timing | multi-agent-comm | FAIL | 8 | 0.90 | yes (1/8 hits) |
| R450 | Boer Voortrekker laager basin | basin-stability | FAIL | 8 | 0.92 | yes (4/8 hits) |

**Pattern:** R447 PassC borderline disagreement; otherwise all 24 cross-agent verifications confirmed FAIL with varying per-result hit counts (1/8 to 8/8). The bottom-3 verifier-hit-count rounds (R449=1, R430=4, R448=4, R450=4) reflect cases where the cultural framing forced the candidate into specifically composed mechanism descriptions that the verifier scored slightly more conservatively but still totalled ≥1 hit.

---

## 4. Adjacency patterns to existing literature

Each round had at least one EXACT TWIN or direct-twin paper with judge ≥0.86:

| Round | Top-matched prior art (judge score) |
|---:|:---|
| R426 | PEPE Periodic Phase Extension EMNLP 2025 (0.92) |
| R427 | FADE Adaptive Weight Decay 2604.27063 (0.92) |
| R428 | H2O Heavy Hitter 2605.07234 (0.92) |
| R429 | Chain of Agents NeurIPS 2024 (0.90) |
| R430 | RAND Judge Reliability Harness 2026 (0.88) |
| R431 | STCTS Non-Uniform Prosody-Delta 2512.00451 (0.90) |
| R432 | CAMPUS Competence-Aware Curriculum 2509.13790 (0.90) |
| R433 | SPC Self-Play Critic 2504.19162 (0.90) |
| R434 | BILLY Persona-Vector Merging 2510.10157 (0.92) |
| R435 | Llama Guard Input-Output Safeguard (0.92) |
| R436 | Symmetry Breaking Transformers Q-K/V-O 2601.22257 (0.92) |
| R437 | Attack-Defense Co-Evolution 2511.19218 (0.90) |
| R438 | Faulty-Agent Challenger+Inspector OpenReview (0.92) |
| R439 | Uncovering Logit Suppression Vulnerabilities 2405.13068 (0.90) |
| R440 | Walsh-Hadamard Cross-Head 2603.08343 (0.92) |
| R441 | LoRA Subtraction Drift-Resistant 2503.18985 (0.92) |
| R442 | Memory Bank Compression Continual SAC 2026 2601.00756 (0.92) |
| R443 | Council Mode Multi-Agent Consensus 2604.02923 (0.92) |
| R444 | HatLLM Hierarchical Attention Masking (0.92) |
| R445 | Autorubric Rubric-Based Eval 2603.00077 (0.90) |
| R446 | BRIDGE Cooperative SFT+RL Bilevel 2509.06948 (0.92) |
| R447 | MetaSD Multi-Drafter Speculative 2604.05417 (0.92) |
| R448 | ACT-R LLM Memory Architecture (0.90) |
| R449 | Multi-Agent Collab Stackelberg 2501.06322 (0.90) |
| R450 | ANTIBODY Robust Alignment Flat-Loss ICLR 2026 2603.00498 (0.92) |

**Pattern:** epoch 18 candidates are uniformly EXACT-TWIN-close to existing literature with max judge ≥0.86 in all 25 rounds; 22 of 25 rounds had ≥0.90.

---

## 5. Cumulative N_verified progression

| Stage | N_verified | p(1% novelty) | p(2% novelty) | p(5% novelty) |
|---|---:|---:|---:|---:|
| Prior corpus (saturation_evidence.md) | 138 | 0.252 | 0.061 | 8.4e-04 |
| After epoch 1 (R001-R025) | 163 | 0.197 | 0.037 | 2.7e-04 |
| After epoch 8 (R176-R200) | 296 | 0.052 | 4.6e-03 | 1.6e-07 |
| After epoch 13 (R301-R325) | 421 | 0.014 | 1.9e-04 | 3.9e-10 |
| After epoch 14 (R326-R350) | 446 | 0.011 | 1.2e-04 | 1.8e-10 |
| After epoch 15 (R351-R375) | 471 | 8.9e-03 | 7.9e-05 | 3.4e-11 |
| After epoch 16 (R376-R400) | 496 | 6.84e-03 | 4.5e-05 | 8.9e-12 |
| After epoch 17 (R401-R425) | 521 | 5.33e-03 | 2.69e-05 | 2.50e-12 |
| **After epoch 18 (R426-R450)** | **546** | **4.17e-03** | **1.62e-05** | **8.55e-13** |

**Effect of epoch 18:** N_verified increases by 25 (521 → 546); p(1% novelty) drops from 0.00533 → 0.00417 (≈22% relative tightening); p(2% novelty) drops by ≈40% relative.

The 1% novelty hypothesis is now rejected at α = 0.005 with margin (p = 0.00417 < 0.005).

---

## 6. Form-distribution comparison

Epoch 18 achieves the most-balanced form distribution in corpus:

| Form | E13 | E14 | E15 | E16 | E17 | **E18** |
|---|---:|---:|---:|---:|---:|---:|
| phase-coherence | 3 | 2 | 2 | 2 | 2 | **2** |
| feedback-attenuation | 3 | 2 | 2 | 2 | 2 | **2** |
| memory-architecture | 3 | 3 | 2 | 2 | 1 | **2** |
| basin-stability | 2 | 2 | 1 | 2 | 2 | **2** |
| information-cascade | 2 | 2 | 2 | 3 | 2 | **2** |
| context-gating | 2 | 2 | 3 | 2 | 3 | **2** |
| spectral-allocation | 2 | 3 | 2 | 2 | 3 | **2** |
| multi-agent-comm | 2 | 2 | 3 | 2 | 2 | **2** |
| evaluation-diagnostic | 2 | 2 | 3 | 2 | 1 | **2** |
| null-space-traversal | 2 | 2 | 2 | 2 | 1 | **2** |
| training-method | 2 | 3 | 3 | 2 | 2 | **2** |
| adversarial-coevolution | — | — | — | 1 | 2 | **2** |
| topological-defect | — | — | — | 1 | 2 | **1** |

12 of 13 forms exercised exactly twice; only topological-defect (most-saturated per epoch 17/16 audits) at 1. This balanced rotation reflects intentional form diversification across epoch 18.

---

## 7. Conclusion

Epoch 18 continues the negative-result trajectory. 25/25 strict-protocol rounds produced 0 substantive PASS. The cumulative empirical evidence (N_verified = 546) now rejects 1% novelty hypothesis at α = 0.005 with margin (p ≈ 0.00417). R279 PTCH remains the strongest niche candidate in the corpus (triple-audited UNCERTAIN), unchanged.

The 1/25 verdict-level cross-agent disagreement (R447 MBUTI-HOCKET-DECODE PassC borderline) is back to typical epoch-13-15 range (1-2/25). Verifier judged the K-draft modulo-K position-assignment with cohesive verification potentially novel enough to clear thresholds; primary scored 8 hits via well-saturated multi-drafter speculative-decoding literature. Recorded as PassC borderline pending future audit if the candidate cluster becomes more interesting.

**Mean total-hits 8.00 per round** is the highest in the rolling corpus, consistent with the monotonic literature-saturation pattern observed across epochs 13→17 (5.08 → 4.92 → 5.96 → 7.08 → 7.84 → **8.00**). The protocol's mechanical safeguards (file chain + 3-channel hit rule + cross-agent spawn) all passed cleanly except for R447 verdict disagreement.

**Next:** Epoch 19 should continue source-family diversification + form-balance maintenance. R447 PassC borderline candidate may warrant Phase-0-style targeted audit if epoch 19 patterns suggest the modulo-K phase-offset speculative-decoder design has genuinely under-explored territory.

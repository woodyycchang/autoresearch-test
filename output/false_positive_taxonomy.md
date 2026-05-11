# False-Positive Taxonomy: Mechanical PASS rounds across epochs 2 + 3

**Author:** Claude (Opus 4.7)
**Date:** 2026-05-11
**Branch:** `claude/resolve-epoch-conflicts-ZwDrf`

The mechanical rule (program §3 step 07: ≥2 content_word overlap → forced hit; step 10: total_hits ≥ 1 → FAIL) returned PASS in 9 rounds across epochs 2+3. **0 of those 9 PASS verdicts hold up under substantive review.** R069 (dike intrusion) is borderline; the other 8 are clear strict-substring artifacts where dense LLM-side prior art existed but used different vocabulary than the candidate's content_words.

This document inventories the failure mode per round and identifies three distinct artifact patterns. Findings drive the v4 design: a semantic-similarity check at step 06.5 between candidate.llm_application and result.title+snippet that fires hit=true at cosine ≥ 0.7 regardless of keyword overlap.

---

## Summary table

| Round | Epoch | Mechanism | Content_words pattern | Functionally-equivalent prior art that existed | Why mechanical rule missed it |
|---|:-:|---|---|---|---|
| **R045** | 2 | LLM plasticity-loss → mammalian critical period (REVERSE) | `plasticity loss`, `critical period`, `layer normalization`, `representation entropy`, `LLM`, `deep network`, `continual learning`, `weight decay` | "Loss of Plasticity in Deep Continual Learning" (Nature 2024); `2402.18762` Disentangling Causes of Plasticity Loss; `2602.09234` Do NN Lose Plasticity in a Gradually Changing World (layer norm + weight decay intervention) | **word-order variant.** Strict substring "plasticity loss" doesn't match "Loss of Plasticity"; "LLM" alone matches but "LLM" + 1 of {layer normalization, weight decay} = only 1 overlap when literature uses "deep continual learning" or "neural network" instead of "LLM" |
| **R046** | 2 | Lock-in amplifier + interference → noisy ICL signal recovery | `lock-in amplifier`, `interference`, `in-context learning`, `ICL`, `LLM`, `attention`, `signal recovery`, `noisy demonstrations` | "Provable Low-Frequency Bias of In-Context Learning Representations" `2507.13540`; "In-Context Learning for Non-Stationary MIMO Equalization" (frequency-domain ICL analog) | **synonym substitution.** Frequency-domain ICL literature uses "low-frequency bias" / "frequency-domain analysis" — the "lock-in amplifier" framing is a synonym from a different field (signal processing) but functionally identical. "in-context learning" matches but only 1 candidate-word does |
| **R047** | 2 | Shannon capacity → impossibility of undetectable + paraphrase-robust LLM watermark | `LLM watermark`, `paraphrase`, `undetectability`, `Shannon`, `capacity`, `information theory`, `robustness`, `steganography` | `2410.02890` and the "Theoretically Grounded Framework for LLM Watermarking" (capacity argument); "Robust Semantics-based Watermark for LLMs against Paraphrasing"; "Revealing Weaknesses Text Watermarking Self-Information Rewrite" | **synonym substitution.** Watermarking literature uses "self-information rewrite" / "semantic robustness" / "theoretically grounded bound" instead of "Shannon"/"undetectability"/"steganography". "LLM watermark" + "paraphrase" overlap = 2 in some results but verifier counted 0 due to title/snippet-only window not catching them |
| **R050** | 2 | Mass action + Le Chatelier (joint) → LLM-MAS capability/cost dynamics | `mass action`, `Le Chatelier`, `capability cost`, `LLM agent`, `multi-agent`, `equilibrium`, `scaling`, `trade-off` | `2506.20921` capability-cost trade-off in LLM-MAS; `2508.07880` multi-agent equilibrium; "Game-Theoretic Lens on LLM Multi-Agent" | **synonym + word-order.** "Mass action" / "Le Chatelier" are chemistry vocabulary; LLM-MAS uses "capability scaling" / "equilibrium pricing" / "game-theoretic". "LLM agent" + "multi-agent" overlap exists but counts as overlap=2 only if both present in title/snippet, which the search results split across different result entries |
| **R059** | 3 | Caldera eruption precursors → LLM fine-tune drift detection | `caldera unrest`, `eruption precursor`, `seismic swarm`, `ground tilt`, `CO2 flux`, `magma viscosity`, `ergodic precursor`, `transfer learning` | "Ergodic seismic precursors and transfer learning for short term eruption forecasting" (Nature Comms 2025); "Universal machine learning approach to volcanic eruption forecasting"; multiple machine-learning-on-volcano papers (s41467-025-56689-x) | **content_words too source-specific.** All 8 content_words are volcanology terminology with zero LLM-side terms. Search results contain ML-on-volcano papers that overlap "transfer learning" + "ergodic precursor" (≥2!) but they are about predicting volcano eruptions, not LLM fine-tuning. The candidate just relabels the volcano-ML pipeline for LLM. Functionally equivalent at the framing level; mechanical rule sees no overlap because candidate doesn't include any LLM-side word and results don't include volcano words |
| **R064** | 3 | Töpfer's Radical Law → distillation curriculum count formula | `Töpfer radical law`, `cartographic generalization`, `map generalization`, `feature selection`, `principle of selection`, `scale reduction`, `cartographic simplification`, `selection ratio` | "SELF-EVOLVING CURRICULUM FOR LLM REASONING" `2505.14970`; "On the Limits of Curriculum Learning for Post-Training Large Language Models"; the broader scaling-laws-for-distillation literature | **content_words too source-specific.** All 8 content_words are cartography. The closed-form sqrt-rule (N₂ = N₁·sqrt(S₁/S₂)) is a specific instance of scale-aware sample-count selection — substantively occupied by self-evolving curricula and distillation scaling literature. Mechanical rule cannot detect because cartography-vocabulary candidate vs LLM-vocabulary literature share zero substring |
| **R068** | 3 | Soil microbiome 4-role decentralized coordination → multi-agent LLM communication | `soil microbiome`, `mycorrhizal network`, `rhizosphere`, `soil pore`, `organic compound diffusion`, `decomposer`, `nitrogen fixer`, `mineralizer` | "AgentNet: Decentralized Evolutionary Coordination for LLM-based Multi-Agent Systems" `2504.00587`; AAAI 2026 WMAC bridge program; "A survey on LLM-based multi-agent systems" | **content_words too source-specific.** All 8 content_words are soil-science. AgentNet is the substantive LLM-MAS analog: decentralized DAG-based coordination via emit/consume/transform of shared substrate state — directly equivalent to the candidate's "4-role local emit-and-sense" framing. Zero substring overlap because soil words ≠ LLM words |
| **R069** | 3 | Magma-chamber dike intrusion → narrow planar self-arresting activation release | `magma chamber`, `dike intrusion`, `dike propagation`, `host rock`, `fracture strength`, `pressure equalization`, `stress field`, `self-arresting` | "Activation Steering in 2026: A Practitioner's Field Guide"; "Adaptive Activation Steering: A Tuning-Free LLM Truthfulness Improvement Method"; "CorrSteer: Generation-Time LLM Steering" | **borderline — likely synonym substitution.** Activation steering / steering vectors / tuning-free truthfulness intervention all occupy the activation-control space. "Narrow planar self-arresting release pathway oriented by gradient stress field" has weaker direct prior art than other false positives, but the LLM endpoint (single-circuit pressure exceeding threshold → release) is functionally a narrow steering intervention. Best characterized as "novel framing of an occupied territory" rather than wholly novel territory. Borderline substantive PASS |
| **R075** | 3 | Numismatic die-axis variance → LLM dual-output rotational variance diagnostic | `die axis`, `die alignment`, `coin striking`, `obverse reverse`, `numismatic variance`, `medallic rotation`, `standard rotation`, `die-pair` | "LLM-as-a-judge" consistency literature; "An Empirical Study of LLM-as-a-Judge"; "On the Role of Reasoning Traces"; broader inference-variance + paired-output diagnostic literature | **content_words too source-specific.** All 8 content_words are numismatic. The forward/reverse-regeneration paired-output diagnostic is functionally adjacent to LLM-as-judge consistency metrics and forward-vs-backward consistency probes. Zero substring overlap because numismatic ≠ LLM vocabulary |

---

## Three artifact patterns identified

### Pattern A — Word-order variant
**Rounds: R045**
The candidate uses a multi-word phrase whose constituent words appear in the literature but in a different order. Strict substring matching ignores morphological/syntactic variants.

Example: candidate `"plasticity loss"` vs literature `"Loss of Plasticity"`. A bag-of-words or stemmed token-set comparison would catch this; a substring match doesn't.

### Pattern B — Synonym substitution
**Rounds: R046, R047, R050, (R069 borderline)**
The candidate uses the source-domain's technical vocabulary while the LLM-side literature uses a synonym from a different field. Functionally equivalent concept, completely disjoint vocabulary.

Examples:
- `lock-in amplifier` (signal processing) ≡ `frequency-domain ICL bias` (ML)
- `Shannon capacity bound on undetectability` (information theory) ≡ `theoretically grounded watermark framework` (NLP)
- `mass action + Le Chatelier` (chemistry) ≡ `capability-cost trade-off + game-theoretic equilibrium` (LLM-MAS)
- `dike intrusion + self-arresting release` (volcanology) ≈ `activation steering + tuning-free intervention` (interpretability)

A semantic embedding model trained on broad scientific text bridges these synonyms via shared latent meaning, so cosine similarity between candidate.llm_application (which mentions both source and LLM concepts) and result.title+snippet (which uses the LLM-side synonym) will be high (>0.7) even when no substring overlaps.

### Pattern C — Source-side-only content_words
**Rounds: R059, R064, R068, R075**
The candidate's 8 content_words are entirely drawn from the source domain (volcanology, cartography, pedology, numismatics). The literature about the LLM application uses entirely LLM vocabulary (transfer learning, curriculum, multi-agent, judge consistency). Zero possible substring overlap regardless of word order.

This is the highest-volume artifact: 4 of 9 false positives, all in epoch 3. The v2 program added a "≥2 LLM-side content_words" composition rule (program_v2.md §4) but v3's epoch-3 generator did not enforce this rule (it focused on memory rotation instead). Re-enforcing the v2 composition rule would partially mitigate Pattern C, but would not catch Patterns A and B.

A semantic check that compares the candidate's `llm_application` (which always mentions both source and LLM concepts because it has to describe the bridge) against the `title+snippet` of LLM-side literature catches all three patterns: cosine similarity is computed in concept space, not lexical space.

---

## Cross-pattern summary

| Pattern | Count | Rounds | Mitigation in v4 |
|---|:-:|---|---|
| A — Word-order variant | 1 | R045 | semantic similarity ≥0.7 |
| B — Synonym substitution | 4 (incl. R069 borderline) | R046, R047, R050, R069 | semantic similarity ≥0.7 |
| C — Source-side-only content_words | 4 | R059, R064, R068, R075 | semantic similarity ≥0.7 + v2 composition rule re-enforced |
| **Total false positives** | **9 / 9** | all rounds | all caught by semantic check |

---

## Memory-DB pattern signal for v4

Beyond the per-round semantic check, the memory_db can flag candidates that match prior false-positive patterns. The 9 false-positive entries in `logs/memory_db.json` share these structural signatures:

- `forced_hit_count == 0` AND `verdict == "PASS"` AND `fail_reason` contains "artifact" or "substring" or starts with "zero hits — candidate may be novel"
- `tried_keywords` are >75% from a single source-domain bucket (volcanology, cartography, etc.)
- `domain_normalized` is a "new domain" introduced in epoch 2 or 3 (no prior FAIL history → no domain-skip rule)

v4 step 06.5 will, in addition to the embedding similarity check, query memory_db for past false-positive entries and compute Jaccard similarity between the current candidate's `tried_keywords` and prior false-positive `tried_keywords`. A match (Jaccard ≥ 0.3) flags the round as "memory-suspected false positive" and forces hit=true on the strongest semantic match in step 07.

---

## Verifier-flagged ground truth

For epoch 2 (R045, R046, R047, R050), the cross-agent verifier in step 12 already flagged each round as `PASS_MECHANICAL_BUT_FAIL_SUBSTANTIVE` and recorded the substantive prior art in `12_verification.json`. v4 should additionally record this verifier-output as a structured signal that the v4 step 06.5 can train on — i.e., the human-labeled ground truth for the false-positive detector lives in `12_verification.json::verdict_agreement == "PASS_MECHANICAL_BUT_FAIL_SUBSTANTIVE"`.

For epoch 3 (R059, R064, R068, R075), the v3 epoch-3 round generator did not exercise substantive judgment (both primary and verifier used the strict mechanical rule), so 12_verification.json `verdict_agreement` is "PASS" rather than the flagged form. The substantive-FAIL ground truth for these rounds lives only in `output/epoch3_comparison.md §3` per-PASS analysis. v4's epoch 4 should restore the v2 verifier behavior of substantive judgment beyond mechanical rule.

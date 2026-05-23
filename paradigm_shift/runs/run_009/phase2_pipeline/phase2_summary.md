# Phase 2 Summary — Run 9 Eight-Layer Pipeline

## Layer-by-layer survivor counts

| Layer | Input | Output | Drop reason |
|---|---|---|---|
| L1 snippet_decomposer | reuse Run 6 purified snippets (13 transcripts) | same | inherited |
| L2 atom_typer + quality_v2 | 735 atoms (Run 6) | 702 atoms | 32 rejected: 27 too-short, 2 truncated FIR, 2 past-tense PRE, 1 vague meta-comment. **Caught Run-8's CAND_011 truncated FIR (T007_S004), CAND_011/012 past-tense+vague (T002_S046, T013_S002).** |
| L3 analogy_engine + cross-speaker | 702 atoms | 7,787 raw candidates | template emission |
| L3 cross-speaker filter | 7,787 | 7,155 | 632 single-speaker rejected (catches **Karpathy×Karpathy CAND_run_008_012** equivalent) |
| L3.5 semantic_coherence_check | 7,155 | 356 | 6,205 LOW_SIMILARITY + 311 DOMAIN_MISMATCH + 1 internal mismatch |
| L4 Belinda 3Q audit | 356 | 356 | all q1/q2/q3 PASS mechanically (atoms exist, ops valid, verbatim found in transcripts) |
| L5 first_principles_stress + arXiv gate | 356 | (deep-audit subset 5) | 5 deep-audit candidates all have ≥1 arXiv paper directly covering claim |
| L6 market_verifier_v2 + speaker_self_publish_v6 | 356 | 86 | **270 rejected** — Belinda Li (arXiv:2511.08579), Yu Sun (arXiv:2407.04620), Hinton (arXiv:2212.13345), Nicholas Roberts (arXiv:2503.10061, arXiv:2412.06540), Amrith Setlur (arXiv:2410.08146, arXiv:2601.14209), LeCun JEPA (arXiv:2306.02507) |
| L7 community_saturation_check | 86 | 0 substantive | dominant topics all saturated in 2024-2026 arXiv (see below) |
| L8 recursive_failure_diagnostic | 86 | trigger Phase R | see Phase R |

## Layer 6 self-publish atoms caught (v6, total 33 atoms flagged)

| Speaker | arxiv | flagged atoms |
|---|---|---|
| Belinda Li | 2511.08579 (her own paper) | 6 atoms in T001 incl. S009 PRE, S012 ANA, S027 ANA, S037 ANA, S040 PRE, S046 OPE, S046 PRE, S046 PRE_04, S050 ANA |
| Yu Sun | 2407.04620 / 2512.23675 / 2505.23884 (his own papers) | T002_S008 ANA, S020 BLO, S024 ANA |
| Hinton | 2212.13345 + T010 language-as-modeling stance | T010_S004 PRE (Chomsky), T012 (FF) S004/S006/S009/S013/S016/S017 atoms |
| Nicholas Roberts | 2503.10061 / 2412.06540 (his scaling laws for skills) | T003_S002 OPE, S008 PRE, S019 ANA, S022 PRE, S023 ANA, S029 ANA, S039 PRE, S039_02 PRE |
| Amrith Setlur | 2410.08146 / 2601.14209 (his RL credit assignment) | T005_S006 PRE, S032 BLO, S045 ANA, S059 ANA, S060 PRE |
| LeCun | 2306.02507 (JEPA) | T011_S005 PRE, S015 PRE, S016 PRE, S038 PRE |
| Karpathy | Software 2.0 Medium 2017 | T013_S002 PRE_02/PRE_03 |

## Layer 7 community saturation summary (5 search angles per topic)

Topic 1 — "step-two reward criterion for open-domain LLM" (Karpathy T007_S022 recurring blocker):
- arXiv:2511.07922 SERL self-examining RL on open-domain
- arXiv:2407.19594 Meta-Rewarding LMs
- ICLR 2025 Bootstrapping LMs with implicit reward models from DPO
- arXiv:2310.00898 Implicit self-improvement
- arXiv:2401.06080 Secrets of RLHF II reward modeling
SATURATION_VERDICT: HEAVILY_SATURATED

Topic 2 — "how neural net parameters collaborate" (Karpathy T007_S008 recurring open problem):
- Anthropic circuits + induction heads research
- arXiv:2501.14926 Attribution-based Parameter Decomposition (APD)
- arXiv:2602.21442 MINAR mechanistic interpretability for neural algorithmic reasoning
- arXiv:2504.07440 Model Utility Law via mechanism interpretability
- Sparse autoencoders feature decomposition (Anthropic, Goodfire)
SATURATION_VERDICT: HEAVILY_SATURATED (dominant frontier-lab focus)

Topic 3 — "scaling laws for scientific foundation models" (Nicholas Roberts atoms):
- arXiv:2507.09404 Scaling Laws for Optimal Data Mixtures
- arXiv:2510.03313 Scaling Laws Revisited: Data Quality
- arXiv:2505.22964 EHR Foundation Model Scaling Laws
- arXiv:2503.10061 NRoberts own paper (self-publish)
SATURATION_VERDICT: HEAVILY_SATURATED (incl. self-publish)

Topic 4 — "linguistic prior / symbolic feedback as reward" (CAND_6479 bridge):
- arXiv:2405.16661 RLSF: Fine-tuning LLMs via Symbolic Feedback
- arXiv:2501.02790 Segment-level reward modeling
- arXiv:2409.00162 Seq2seq Reward Modeling Language Feedback
- arXiv:2504.15210 Symbolic Execution into Code-Gen LLM Fine-tuning
SATURATION_VERDICT: SATURATED

Topic 5 — "mac-mini local LLM inference batch-1 memory bound" (carried from Phase 1):
- Multiple 2026 practitioner guides on llama.cpp / MLX / exo-labs
- arXiv contributions on quantization for memory-bound inference are routine
SATURATION_VERDICT: HEAVILY_SATURATED

## Phase 2 Final Survivors

After all 8 layers: **0 substantive paradigm-shift niches**.

The 86 atoms that survived Layer 6 self-publish v6 all combine with Karpathy's general-textbook
T007 framing on saturated topics (reward criterion, params collaborate, scaling). No genuine
cross-leader, non-self-publish, non-saturated paradigm-shift candidate emerged.

**Triggering Phase R (recursive failure-driven self-improvement).**

## TOOL_AUDIT (Phase 2)
- WebSearch: 5 (Layer 5) + 5 (Layer 6 speaker self-publish) + 5 (Layer 7 saturation) = **15** (in addition to Phase 1's 10)
- Read (view tool on transcript line spans for atoms / 5 deep-audit candidates): 6
- Write (modules + JSON reports): 9
- Edit (run_9_pipeline.py keyword updates v2→v6): 7
- Bash (python pipeline drivers, JSON inspections): 14
- Total Phase 2 real tool calls: **51**

# Run 10 vs Run 11: Comparison Report

## Headline finding

| Metric                                | Run 10                          | Run 11                                  |
| ------------------------------------- | ------------------------------- | --------------------------------------- |
| Epochs run                            | 4 (max-epoch terminal)          | 7 (full sequential rotation)            |
| Source corpus                         | arXiv injected atoms + 13 transcripts | Tech-leader writing (PG, KP, SA, OA, AN, HN, WebSearch) + arXiv pool |
| Total atoms processed                 | 343 transcript + 42 arXiv = 385 | 84 non-arXiv + reused arXiv pool         |
| Candidates scored                     | ~85 (post L4)                    | 84 (12 per epoch × 7)                    |
| Saturation kill rule                  | BINARY L7 (any cross-paper ⇒ kill) | SOFT 10-parameter composite ≥ 0.7       |
| Substantive niches                    | **0** (all 85 killed at L7)      | **24** (composite ≥ 0.7, Belinda-pass)  |
| Top composite score                   | n/a (binary kill)                | 0.8379 (CAND_011_E7_011)                 |
| Mean composite                        | n/a                              | 0.6290                                   |
| New root causes                       | RC_006/007/008 + TERMINAL_RC_009 | RC_010 + RC_011 + RC_012 (+ refinement of RC_009) |
| Per-source productivity heterogeneity | n/a (single corpus)              | PG=2, KP=4, SA=2, OA=4, AN=2, HN=4, WS=6 |
| RLHF weight evolution                 | n/a                              | cross_disciplinary_bonus 0.10 → 0.243 (×2.4) |

## Did sequential + RLHF mimick escape Run 10's literature density saturation?

**Yes, but with a deliberate design tradeoff.** Run 11 escaped the binary L7 saturation kill by replacing it with a soft 10-parameter composite. The escape is real in the operational sense (24 candidates pass the 0.7 threshold and the Belinda 3Q audit), but it depends on accepting cross_source_diversity + cross_disciplinary_bonus + arxiv_grounding as partial offsets for elevated saturation. Under Run 10's strict binary rule, all 24 candidates would still fail because each has 0–4 bridging arXiv papers. The new bottleneck is **epistemic** (do soft-threshold survivors deserve the paradigm-shift label?) rather than **combinatorial** (Run 10's literature-density binding).

## Per-epoch atom yield comparison

Run 10 had a static merged corpus (transcripts + arXiv) and ran 4 recursive iterations on it. Run 11 introduced a NEW source per epoch and scored against an evolving RLHF weight set.

| Epoch | Source                          | Atoms | Candidates | Survivors | Mean composite |
| ----- | ------------------------------- | ----- | ---------- | --------- | -------------- |
| 1     | Paul Graham essays              | 12    | 12         | 2         | 0.6072         |
| 2     | Karpathy blog                   | 12    | 12         | 4         | 0.6433         |
| 3     | Sam Altman blog                 | 12    | 12         | 2         | 0.6109         |
| 4     | OpenAI blog/news                | 12    | 12         | 4         | 0.6597         |
| 5     | Anthropic news                  | 12    | 12         | 2         | 0.5961         |
| 6     | HN top stories                  | 12    | 12         | 4         | 0.6260         |
| 7     | WebSearch 'ML breakthrough 2026'| 12    | 12         | 6         | 0.6588         |
| **TOTAL** | —                             | **84** | **84**       | **24**       | **0.6290**       |

Run 10 by contrast: 15 → 19 → 19 → 32 L8-survivors all saturated at L7 ⇒ 0 substantive across 4 epochs.

## Multi-parameter scoring distribution evolution

Survivor mean parameters across run 11 (averaged across all 24 survivors):

```
atom_quality_score        : ~0.80   (consistent across epochs)
novelty_score             : 0.46    (down from 0.82 at epoch 1 — saturated framings still admitted)
cross_source_diversity    : ~0.96   (almost always 1.0; cross-source pairing was the deliberate construction rule)
mechanism_coherence       : ~0.41   (moderate — shared mechanism vocab partially overlaps)
saturation_distance       : ~0.66   (moderate; soft scoring tolerates partial saturation)
speaker_self_publish_risk : ~1.0    (uniform — none of the non-arXiv atoms use self-publish phrasing)
arxiv_grounding           : ~0.43   (most survivors have 1-3 bridging citations)
belinda_audit_pass        : ~1.0    (uniform — all candidates pass mechanical check)
community_density         : ~0.58   (variable — some hot topics get through via cross-source bonus)
cross_disciplinary_bonus  : ~0.79   (high; this is the discriminating dimension)
```

## RLHF weight evolution across 7 epochs

| Parameter                  | v0 init | v1 (e1) | v3 (e3) | v5 (e5) | v7 (e7) | Δ           |
| -------------------------- | ------- | ------- | ------- | ------- | ------- | ----------- |
| atom_quality_score         | 0.100   | 0.100   | 0.096   | 0.100   | 0.098   | -0.002      |
| novelty_score              | 0.100   | 0.087   | 0.091   | 0.089   | 0.080   | -0.020      |
| cross_source_diversity     | 0.100   | 0.112   | 0.110   | 0.104   | 0.101   | +0.001      |
| mechanism_coherence        | 0.100   | 0.106   | 0.093   | 0.092   | 0.089   | -0.011      |
| saturation_distance        | 0.100   | 0.088   | 0.089   | 0.088   | 0.079   | -0.021      |
| speaker_self_publish_risk  | 0.100   | 0.093   | 0.082   | 0.078   | 0.066   | -0.034      |
| arxiv_grounding            | 0.100   | 0.115   | 0.109   | 0.104   | 0.095   | -0.005      |
| belinda_audit_pass         | 0.100   | 0.093   | 0.082   | 0.078   | 0.066   | -0.034      |
| community_density          | 0.100   | 0.089   | 0.095   | 0.095   | 0.083   | -0.017      |
| **cross_disciplinary_bonus** | **0.100** | **0.117** | **0.152** | **0.173** | **0.243** | **+0.143**  |

Key reading: the gradient consistently rewarded cross_disciplinary_bonus because that parameter best discriminated survivors from rejected. speaker_self_publish_risk and belinda_audit_pass shrank because they were nearly uniform across all candidates (constant 1.0) — the gradient interpreted their lack of discrimination as a signal to deweight.

This means the RLHF mimick **converged on a different signal than initially weighted**: cross-disciplinary bridging is the dominant survivor predictor, not novelty or saturation distance per se.

## Per-source productivity (which tech-leader writing produced most quality atoms?)

Ranked by survivor yield:

1. **WebSearch breakthroughs (epoch 7)**: 6 survivors. Nested Learning + RLMs + World Models triad provided the densest technical material with the richest cross-disciplinary bridges (evodevo, thermodynamics, causality).
2. **Karpathy blog (epoch 2)**: 4 survivors. RLVR/jagged intelligence + microGPT compression provided strong mechanism atoms.
3. **OpenAI news (epoch 4)**: 4 survivors. Erdos disproof was a cross-field bridging event in itself; provided meta-level material.
4. **HN top stories (epoch 6)**: 4 survivors. Penn exciton-polariton + Aalto quantum-inspired + Jack Clark RSI generated diverse physics+ML bridges.
5. **Paul Graham essays (epoch 1)**: 2 survivors. Strong on first-principles atoms but weaker cross-source pairing (only arXiv partners available).
6. **Sam Altman blog (epoch 3)**: 2 survivors. The Gentle Singularity material is high-level prediction-flavored; harder to extract mechanism atoms.
7. **Anthropic news (epoch 5)**: 2 survivors. Mythos withholding decision provided novel safety-substrate atoms but ML-stack atoms (Opus 4.7, 1M context) were heavily covered by 2026 literature.

Pattern: sources that publish **mechanism-flavored technical material** (Karpathy, OpenAI research blog, WebSearch breakthrough papers, HN frontier-research stories) outproduce sources that publish **first-principle / philosophy-flavored material** (PG, Altman, Anthropic news framing). This is partially an artifact of how the multi_parameter_scorer rewards mechanism_coherence and arxiv_grounding.

## Honest caveats and limitations

1. **Soft-threshold accountability**: Run 11's 24 survivors all have non-zero `arxiv_citations_supporting`. They are not "uncovered" niches; they are "under-bridged" niches where the specific cross-source pairing is new even though component arXiv coverage exists. Whether this difference matters depends on the consumer.

2. **WebFetch firewall**: Direct WebFetch was 403 for every primary URL (paulgraham.com, karpathy.github.io, blog.samaltman.com, openai.com, anthropic.com, news.ycombinator.com, archive.org). All atom extraction used WebSearch summary text as fallback. Atom verbatim-quote fidelity is therefore approximate, not exact; future runs should use an authenticated MCP-provided fetch tool or a pre-cached corpus.

3. **Self-supplied harness inputs**: arxiv_hit_count_24m, recent_paper_count, saturation_cluster_distance were estimated by the agent based on WebSearch results. These are the most uncertain inputs in the pipeline. Future runs should mechanize them via an arXiv API query rather than agent estimation.

4. **Belinda 3Q audit unanimously passed all 24**: this is suspicious. The audit is mechanical (mechanism specific, testable, novel path), and the candidates were CONSTRUCTED to satisfy these criteria. Real-world novelty validation requires cross-LLM agreement (Phase 6 queue) and/or longitudinal arXiv tracking (do these joint topics appear as papers in 6-12 months?).

5. **24 survivors is a lot**: under Run 10's regime, 0 survivors meant the pipeline was binding too tight; 24 survivors under Run 11's regime suggests the pipeline may now bind too loose. A future Run 12 could empirically fit the composite threshold against a labeled set.

## Open problems carried forward

- **RC_010**: Whether soft-threshold survivors are paradigm-shift candidates or rubber-stamp artifacts. Resolution via Phase 6 cross-LLM and longitudinal tracking.
- **RC_011**: Whether technically-dense sources have more REAL paradigm shifts vs more candidates that happen to score above soft threshold.
- **RC_012**: Whether RLHF weight drift converges or oscillates across additional epochs. Current data (7 epochs) is insufficient to distinguish.
- **Open from Run 10**: Whether non-arXiv corpora can escape literature-density binding. **Answered**: yes, escape is enabled by SOFT THRESHOLD scoring (not by non-arXiv corpora alone). Non-arXiv corpora alone would still be killed by Run 10's binary L7.

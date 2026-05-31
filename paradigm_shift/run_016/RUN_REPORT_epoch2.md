# Run 16 — Epoch 2 report (parameter improvement measured)

Epoch 2 applied the human labels from epoch 1 + the human's cold-start bootstrap,
re-ran the full 5-agent pipeline, and measured the change in search quality.

## Headline (R12 — per-epoch success = search-quality improvement)

| metric | epoch 1 | epoch 2 | delta |
|---|---|---|---|
| **avg_search_quality** | 0.5119 | **0.5967** | **+0.0848 ▲** |
| niche verdict | NICHE_NOT_FOUND | NICHE_NOT_FOUND | — |
| proof points | 7/7 | 7/7 | — |
| A3↔A4 mismatches | 0 | 0 | — |

**Epoch 2 improved search quality by +0.0848.** Niche-finding (the long-run goal)
is still NOT_FOUND, but per the spec that is not the per-epoch success metric.

## What changed the metric

| dimension mean | epoch 1 | epoch 2 | note |
|---|---|---|---|
| reformulation_specificity | 0.7262 | **0.8913** | ▲ nudged param (0.5→0.5428) + more specific queries |
| mechanism_focus | 0.8333 | 0.7391 | ▼ slightly (epoch-2 cross-domain queries name biology, not only ML mechanisms) |
| cross_domain_reach | 0.0000 | **0.0217** | ▲ off zero — bootstrap worked, but barely (see caveat) |
| atom_source_diversity | 1.0000 | 1.0000 | unchanged |
| collision_avoidance_phrasing | 0.0000 | **0.3043** | ▲ off zero — prior-art-probing bootstrap clearly worked |

The two interventions:
1. **Label nudge** (epoch-start `apply_labels`): on_target queries were more
   specific (0.808 vs 0.594) → `reformulation_specificity` param 0.5→0.5428;
   `mechanism_focus` 0.5→0.5067. Reweighting the average toward specificity (now
   0.89) is the largest single contributor to the gain.
2. **Cold-start bootstrap by instruction** (the human's fix for the two flat
   dims): AGENT 1 sourced 1 non-ML (biology) atom; AGENT 3 used ≥2 prior-art-
   probing reformulations/candidate. Both flat dims rose above 0.0.

## Honest caveat on cross_domain_reach (+0.0000 → +0.0217 only)

The bootstrap produced genuinely cross-domain *candidates* (ML × transcription-
factor biology), but `cross_domain_reach` barely moved because the scorer credits
it **per query**, requiring a single query string to contain vocabulary from two
field-lexicons. Most epoch-2 queries still named one domain at a time. Only ~1 of
23 queries was lexically dual-domain. So the *candidates* are cross-domain while
the *query strings* mostly are not — an honest gap between intent and the metric's
mechanics. `collision_avoidance` (0.304) moved much more because prior-art phrasing
is easy to put in every probe query. A future epoch could lift cross_domain_reach
by instructing agents to always name both domains in cross-domain reformulations.

## Niche result (long-run goal status)

`NICHE_NOT_FOUND`, but epoch 2 is more scientifically interesting than epoch 1:

| cand | niche | gates [1,2,3,4] | why rejected |
|---|---|---|---|
| 001 | Learned Token-Choice Routing for Sparse Mixture-of-Attention Heads (ML×ML) | 0 1 0 1 | **real prior-art collision** — "Mixture of Attention Heads" (EMNLP 2022, arxiv 2210.05144), independently confirmed by AGENT 4 |
| 002 | Ultrasensitive Sigmoidal Gating for Specific MoE Routing (ML×bio) | 0 1 1 1 | only Gate 1 (novelty floored by ~18 adjacent papers); **no collision** |
| 003 | Expert-Choice Routing Models of Ultrasensitive TF Specificity (ML×bio) | 0 1 1 0 | Gate 1 + Gate 4 (its mechanism text lacks a recognized mechanism-verb) |

The cross-domain bootstrap **reached genuinely uncolliding territory**: the ML×ML
candidate collided with existing work, while both ML×biology candidates had no
direct prior art (cross-verified). Candidate 002 is the closest any candidate has
come to surviving — it clears 3 of 4 gates, failing only the strict 0.90 novelty
threshold.

## Cross-verification (R7) had teeth this epoch
Unlike epoch 1 (all "no collision"), epoch 2 had a real collision claim. AGENT 4
**independently re-found** the colliding EMNLP-2022 paper with different search
wording (confirming AGENT 3, not rubber-stamping), and independently confirmed the
two no-collision verdicts. 3/3 confirmed, 0 disputed.

## Parameter state (R9)
`direction_params.json`: epoch 2 → 3; `epoch_history` now holds epoch 1 (0.5119)
and epoch 2 (0.5967). Params after epoch 2: specificity 0.5428, mechanism 0.5067,
others 0.5. Epoch-2 finalize applied no new nudge (epoch-2 queries are labeled by
the human *after* this epoch — the lag-by-one design).

## Proof points: 7/7 PASS
agents_all_committed · report_verbatim ([REPORT 1..5]) · four_gate_deterministic ·
cross_check_ran · no_hallucination · search_quality_tracked · params_persisted.
18 offline tests pass.

## Honest disclosures
- AGENT 1 again caught its own R5 slip: its first epoch-2 draft used unverifiable
  (future-dated) arXiv ids; it discarded them and recommitted with verified real
  papers (the flawed `ce6415f7` is superseded by `d71fb6c6`, both in history).
- WebFetch still 403s for arXiv; atom text is from real WebSearch snippets.
- cross_domain_reach gain is small and honestly explained above.

## Next epoch
The human labels epoch-2's 23 queries (on_target/diverge); those drive epoch-3's
nudge. To push cross_domain_reach, epoch-3 agent instructions should require both
domains be named in each cross-domain query string.

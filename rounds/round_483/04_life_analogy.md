# Life Analogy — Chinese 24 solar terms (jieqi) staged agricultural curriculum

The **24 jieqi** (Chinese solar terms, UNESCO 2016):
- 24 ~15-day stages per solar year.
- 4 seasons × 6 sub-stages each.
- Each stage specifies optimal farming task (planting, cultivating, harvesting, storage).
- Phenological signals (insect awakening, frost descent, rain water) cue stage transitions.
- Sequence: Li Chun (Start of Spring) → Yu Shui (Rain Water) → ... → Da Han (Great Cold) → cycle restart.

**JIEQI-24-STAGE-CURRICULUM**: 24-stage cyclical training curriculum with phenological-signal gating. (1) Partition pretraining into 24 stages, each ~15-degree training-progress (loss-curve position). (2) Each stage j ∈ {1, ..., 24} has its own data mixture m_j tied to "season" (foundation S1-S6, instruction-tune S7-S12, alignment S13-S18, reasoning S19-S24). (3) Stage transition gated by phenological signal: e.g. perplexity-on-canary-set < threshold_j (e.g., loss-on-test < δ_j signals "frost descent" cue to advance). (4) Cyclical option: after Stage 24, restart at Stage 1 with refined-data + LR-reset (multi-year cyclical curriculum). (5) Differs from monotonic curricula by built-in 24-stage cycle + phenological gating.

## Adjacency
- Curriculum Learning LLM Pretraining 2601.21698 (closest)
- Beyond Random Sampling Curriculum 2506.11300
- Multi-stage pretraining (web → quality)
- LR decay + curriculum interaction 2511.18903

Expected FAIL — multi-stage curriculum + checkpoint gating fully covered.

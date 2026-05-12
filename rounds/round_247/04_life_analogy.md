# R247 — life analogy

## Source domain: forest succession + shade-tolerance hierarchy
- 4 stand stages: stand-initiation (pioneers, fast-growing, sun-loving) → stem-exclusion (canopy closes, light competition) → understory-reinitiation (gap-dynamics admits shade-tolerant species) → old-growth (climax, only self-shade-tolerant species persist).
- Pioneers and climax species occupy DIFFERENT ecological niches: pioneers fast-but-fragile, climax slow-but-persistent.
- Critical: the system PROGRESSES through stages; old-growth state is REACHED via specific gap-dynamics during understory-reinitiation, not by training a climax species from scratch.

## LLM analogy candidate
**Forest-succession LLM training schedule**: structure pretraining + fine-tuning as 4 explicit stages mimicking forest succession. (1) PIONEER stage: train on broad, fast-coverage corpus to establish all basic capabilities (= sun-loving pioneers). (2) STEM-EXCLUSION: introduce aggressive light competition — competitive loss across capability heads forces specialization (= canopy closure). (3) UNDERSTORY-REINITIATION: introduce GAP DYNAMICS — periodically remove (gap) a small fraction of the highest-magnitude weights and admit re-training in the gap region for slow-but-deep capability (= shade-tolerant understory). (4) OLD-GROWTH: final stabilization stage where only self-consistency-maintaining capabilities (climax) persist; weights that cannot generate offspring (i.e., self-consistent fine-tunes) are pruned. This is a fundamentally different training paradigm: PHASE-EXPLICIT not continuous.

## What differs from prior art (claim)
Self-Evolving Curriculum (2505.14970) and knowledge-circuits phase analysis (2502.11196) approach phase-aware training but do not propose the 4-stage forest-succession discipline with gap-dynamics weight removal + climax self-consistency selection. The shade-tolerance / gap-recruit / climax-self-shade discipline is not retrieved as a single training schedule.

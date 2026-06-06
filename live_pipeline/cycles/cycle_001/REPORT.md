# Cycle 1 — Live-Fetch Niche Finder

**Result:** 1 niche survived all 6 stages — `GridFermi-PE` — confirmed-with-caveats
as a real but **marginal, modest-incremental long-shot seed**. **0 fabrications**
across the whole cycle. ~34 parallel tool-using agents, ~300 real WebSearches.

## What each stage did

### Stage 1 — Live encyclopedia fetch (6 fetch + 4 checker agents)
6 parallel agents WebSearched 6 distinct branches of knowledge (condensed matter,
molecular biology, pure math, mechanism design, neuroscience, newest-ML) and
returned **18 concepts with real source URLs** (29 real searches). 4 separate
checker agents verified every URL; the recent-ML arXiv branch (highest fabrication
risk) was **double-checked**. **0 fabrications.** WebFetch was 403-blocked on all
domains, so verification ran via independent WebSearch + cross-agent author-list
agreement (two checkers independently recovered identical author lists for the
recent arXiv papers — strong anti-hallucination signal). 1 metadata fix (QUEST =
Apr 2026, not Mar).

### Stage 2 — Merge (4 agents)
4 parallel agents formed **8 maximally-distant cross-branch triples**, each grounded
by real searches. Distinct anchoring directives forced diverse, non-overlapping
combinations.

### Stage 3 — Integrity check (8 redundant checkers, 2-cover)
Every merge judged by **2 independent tool-using checkers** (~10 searches each);
GENUINE only if both agree. **3 of 8 survived.** Dropped: 1 unanimous hallucination
(M1-T2: coend "predicts" dynamin cooperativity = a category-theory pun); 4 on
checker disagreement (Kohn-as-externality, Rashba-chirality-as-STDP, etc.).
**Headline measurement: 4 merges passed their first checker but were caught by the
second** — redundancy cut the pass set 7→3 (~57% fewer false-positive "genuine"
verdicts) at a **0.50 inter-checker disagreement rate.** This is the cycle's
strongest evidence for the core thesis (R3/R10).

### Stage 4 — Niche check (6 checkers, 2-cover)
2 independent skeptical agents per survivor classified genuine-niche vs
trivial-variant. **1 of 3 survived.** Both drops were unanimous TRIVIAL_VARIANT
and shared one failure mode invisible to Stage 3: a real, integrity-clean,
novel-combination direction whose cross-domain "bound/mechanism" **collapses to an
existing result when the analogy is pressed** — M4-T1 (VCG with no strategic
agents → static design parameter) and M4-T2 (Myerson-Satterthwaite bound reduces
to Hopfield-Murugan kinetic proofreading). Stage-4 disagreement = 0.0.

### Stage 5 — Value + prior-art registry (4 agents)
2 adversarial prior-art sweeps (~40 queries each) → **unanimous NO_COLLISION**
(closest: GridPE 2406.07049). 2 value assessors → **unanimous MODEST_INCREMENTAL /
small_study** (~10–15% chance of a clean win vs FoPE/RoPE+YaRN; the hexagonal/2k_F
geometry likely **not load-bearing** because learnable wavevectors train away from
initialization).

### Stage 6 — Reasoning audit (2 Opus auditors)
Both independently returned **NICHE_CONFIRMED_WITH_CAVEATS**. They re-verified all
provenance (0 fabrication), confirmed the pipeline did **genuine filtering, not
rubber-stamping** (stage-distributed ~94% mortality; 0.50 disagreement;
self-deflating value verdict; matches the 0/1071 predecessor base-rate), and each
added a sharp finding:
- **AUD1:** the Kohn-2k_F physics framing is decorative; QUEST is imported as a
  length-generalization device but its evidence is vision/robustness-only (an
  off-domain overclaim the chain never flagged).
- **AUD2 (most important):** the pipeline has **no terminal expected-value kill
  criterion** — it must always emit a "best survivor," so a ~10–15%-odds idea
  becomes "the product." → queued as the highest-priority fix.

## The surviving niche

**GridFermi-PE** — a transformer positional encoding fusing per-head learnable
hexagonal-reciprocal-lattice wavevectors (grid cells, B5-C2) with QUEST-style
per-token query-norm concentration (B6-C1) tuned to peak at each head's wavevector
shell (Kohn anomaly 2k_F analogue, B1-C1). Hypothesis: better length generalization
than RoPE/ALiBi/FoPE. **Honest status:** real, novel-combination, zero-fabrication,
but marginal — geometry probably decorative, value modest-incremental, worth a small
ablation at most (and nothing if hexagonal/2k_F prove inert).

## Algorithm-improvement evaluation (R9 — the thing we actually measure)

This was the cold-start of the no-banks architecture, so the deliverable is the
**process**, not the niche:
1. **Live-fetch with 0 fabrication** — the no-banks principle held; every concept
   traced to a real, independently-confirmed source.
2. **Quantified the value of redundancy** — 57% false-positive reduction at the
   integrity stage; this is now measured, not assumed.
3. **6 measurement-driven param upgrades** queued for cycle 2 (see
   `direction_params.json`), the highest-priority being a **terminal EV gate** that
   lets the pipeline honestly output "no niche worth promoting this cycle."

Per-cycle metrics are in `direction_params.json → metrics_history`; raw per-stage
agent outputs are in `stageN_*.json`; resume/dedup state is in `traversed.json`.

# Phase R — Recursive Self-Improvement Fixes (Run 9 epoch 2)

## R-Step 1: Failure root-cause analysis

After all 8 layers of Run 9 epoch 1 yielded 0 substantive paradigm-shift niche, the failure
distribution by layer (cumulative drop):

| Layer drop | Count | Pct of total |
|---|---|---|
| L2 atom_quality_v2 | 32 atoms (Run 6 had 735) | 4.4% atom rejection |
| L3 single-speaker | 632 candidates of 7,787 | 8.1% candidate drop |
| L3.5 semantic_coherence | 6,799 of 7,155 | 95% candidate drop |
| L6 self-publish v6 | 270 of 356 | 75.8% coherence-survivor drop |
| L7 saturation | ~86 of 86 | 100% L6-survivor drop |

The dominant failure pattern: **speaker self-publish** (270 / 356 = 76%) followed by
**community saturation** (100% of L6 survivors).

### FAILURE_ROOT_CAUSE_1: SPEAKER_SELF_PUBLISH
Description: Each academic transcript (T001 Belinda, T002 Yu Sun, T003 NRoberts, T005 ASetlur,
T010/T012 Hinton, T011 LeCun) is a researcher pitching their own published paper. Any atom
extracted from those talks risks summarizing that researcher's own published work, which the
pipeline then "combines" with a textbook framing to produce a vacuous cross-leader claim.
Run-9 v6 keywords flag 33 atoms, but verbatim-keyword matching has limited recall (e.g.
ATOM_T013_S023_ANA_03 "Whimos look driverless" requires a different match logic).

### FAILURE_ROOT_CAUSE_2: NARROW_INPUT_POOL
Description: Only 13 transcripts in the corpus, dominated by single-paper-pitch academic talks
and 4 general/startup talks (Sam Altman T009, Silicon Valley T008, Naval T014, Valerie Chen T004).
The combinatorial space of paradigm-shift candidates is bounded by speaker diversity.

### FAILURE_ROOT_CAUSE_3: FIRST_PRINCIPLES_MONOPOLY
Description: After L2 quality filter, only 8 first_principle atoms remain, of which 4-5 are
Karpathy's T007 talk. The PREDICTION_GROUNDED_IN_PRINCIPLE combinator anchors many candidates on
Karpathy's first principles, which are textbook material (next-word prediction → assistant
fine-tuning is foundational, not a research niche).

### FAILURE_ROOT_CAUSE_4: SHALLOW_SATURATION_CHECK
Description: L7 community_saturation_check uses single-topic keyword search. It does not test
SECOND-ORDER combinations (e.g., interpretability×scaling×TTT triple). The current pipeline only
emits PAIRS via 4 binary combinators; no TRIPLE combinator exists.

### FAILURE_ROOT_CAUSE_5: MECHANISM_INCOHERENT_PAIRING
Description: Semantic coherence check accepts pairs based on TF-IDF / Jaccard subject overlap.
It does not verify the two atoms share a MECHANISM (e.g., "linguistic prior" vs "reward criterion"
are both about "language" surface but operate on different mechanism axes: structure vs incentive).

## R-Step 2: Counter-paper search

For each root cause, ≥3 web_searches → candidate counter-methods:

### ROOT_CAUSE_1 (self-publish) → counter_arXiv
- arXiv:2410.14255 Nova (Iterative Planning and Search for Novel Ideas) — uses external knowledge
  retrieval to PURPOSELY plan idea generation away from training distribution.
  - Apply: BEFORE combining two atoms, retrieve known publications by EITHER atom's speaker
    via arXiv API; reject if atom verbatim matches speaker's abstract keywords.
- arXiv:2602.20408 "Barriers to Diversity in LLM-Generated Ideas" — multiple independent ideation
  sessions converge around similar themes ("mode collapse").
  - Apply: ENFORCE that PAIRS contain at least one atom from a NON-academic-pitch transcript.

### ROOT_CAUSE_2 (narrow input pool) → counter_arXiv
- arXiv:2412.14141 "LLMs can Realize Combinatorial Creativity" — generalization-level retrieval
  system maps concepts across different abstraction levels for cross-domain knowledge discovery.
  - Apply: Add a SYNTHETIC-ATOM injection step from a curated "frontier ML 2024-2026" knowledge
    graph (Anthropic interp blog circuits, Eleuther scaling, Goodfire features, etc.) so the
    combinator has access to non-talk atoms.

### ROOT_CAUSE_3 (first-principle monopoly) → counter_arXiv
- arXiv:2605.11258 "Unlocking LLM Creativity in Science through Analogical Reasoning" — generates
  analogies to cross-domain problems based on shared relational structure.
  - Apply: Diversify first_principles atom pool by mining cross-talk first_principles AND adding
    explicit "first_principle" extracts from non-academic-pitch transcripts.

### ROOT_CAUSE_4 (shallow saturation) → counter_arXiv
- arXiv:2409.04109 "Can LLMs Generate Novel Research Ideas? Human Study" — AI-generated ideas
  judged more novel than human ones but slightly weaker on feasibility.
  - Apply: Add TRIPLE-ATOM operator. Saturation searches at triple-level rarely fire (literature
    is dominated by pair-level cross-references).

### ROOT_CAUSE_5 (mechanism mismatch) → counter_arXiv
- arXiv:2510.22312 "LacMaterial: Large Language Models as Analogical Chemists for Materials
  Discovery" — uses "shared mechanism vocabulary" check before applying analogy.
  - Apply: Add MECHANISM_VOCABULARY check — both atoms must overlap on a shared mechanism
    keyword (e.g., "gradient", "attention", "reward", "memory") in addition to subject similarity.

## R-Step 3: Pipeline modifications (code applied below)

The following modules in this PR implement R-Step 3:

1. `paradigm_shift/run_9_pipeline.py` — Added (already in v6): atom_quality_v2,
   cross_speaker_diversity, speaker_self_publish (per-speaker keyword tables).
2. `paradigm_shift/runs/run_009/epoch_2/triple_combinator.py` — NEW: TRIPLE atom combinator
   (3 atoms from 3 distinct speakers) — counter ROOT_CAUSE_4.
3. `paradigm_shift/runs/run_009/epoch_2/mechanism_check.py` — NEW: shared-mechanism vocabulary
   gate — counter ROOT_CAUSE_5.
4. `paradigm_shift/runs/run_009/epoch_2/non_academic_anchor.py` — NEW: requires ≥1 atom from
   a non-academic-pitch transcript (T004/T008/T009/T014) — counter ROOT_CAUSE_1 + 2.

These fixes are applied in Run 9 epoch 2, run with same input atoms.

## R-Step 4: Re-run epoch 2 plan

Apply v6 atom pool + non-academic-anchor + mechanism-vocab gate. Emit triples. Re-test all 8
layers. Expected outcome: probably still 0 substantive niche, because root causes 1, 2 are
structural (corpus limitation). Epoch 2 will quantify the residual after R-fixes.

## R-Step 5: Final epoch summary
See `paradigm_shift/runs/run_009/epoch_2/epoch_2_summary.md`.

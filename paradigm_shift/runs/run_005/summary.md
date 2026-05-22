# Paradigm-Shift Finder v1 — Run `run_005` Summary

Manifest: `paradigm_shift/runs/run_005/manifest.json`
Run started: unknown
Run ended:   2026-05-22T08:50:36.140126+00:00

## Transcripts

- **T001** Belinda Li — _Building AI systems with coherent and updatable models of the world, user, and themselves_  `tari/inputs/belinda_li_self_models_canonical.txt`
- **T002** Yu Sun — _Test-time training and adaptive computation at inference_  `tari/inputs/transcript_002_yu_sun_canonical.txt`
- **T003** Nicholas Roberts — _Science of foundation models for science_  `tari/inputs/transcript_003_nicholas_roberts_canonical.txt`
- **T004** Valerie Chen — _Human-AI collaboration_  `tari/inputs/transcript_004_valerie_chen_canonical.txt`
- **T005** Amrith Setlur — _Training models to adapt at test time via reinforcement learning_  `tari/inputs/transcript_005_amrith_setlur_canonical.txt`
- **T007** Andrej Karpathy — _Intro to LLMs (busy person introduction)_  `tari/inputs/transcript_007_karpathy_intro_llms.txt`
- **T008** Richard Sutton — _Silicon Valley doesn't understand the bitter lesson_  `tari/inputs/transcript_008_silicon_valley_doesn_t_understand_the_bi.txt`
- **T009** Sam Altman — _How to Start a Startup (Stanford lecture 1)_  `tari/inputs/transcript_009_lecture_1_how_to_start_a_startup_sam_alt.txt`
- **T010** Geoffrey Hinton — _Will AI outsmart humans_  `tari/inputs/transcript_010_hinton_will_ai_outsmart.txt`
- **T011** Yann LeCun — _Self-supervised learning and JEPA_  `tari/inputs/transcript_011_yann_lecun_self_supervised_learning_jepa.txt`
- **T012** Geoffrey Hinton — _Forward-Forward algorithm_  `tari/inputs/transcript_012_geoffrey_hinton_unpacks_the_forward_forw.txt`
- **T013** Andrej Karpathy — _Software is changing (again) — Software 3.0_  `tari/inputs/transcript_013_andrej_karpathy_software_is_changing_aga.txt`
- **T014** Naval Ravikant — _How to get rich without getting lucky_  `tari/inputs/transcript_014_naval_ravikant_how_to_get_rich_without_l.txt`

## Atoms

- Paradigm atoms: 148
- By paradigm_type: {'prediction': 49, 'analogy': 88, 'open_problem': 7, 'blocker': 2, 'first_principle': 2}
- By transcript: {'T001': 29, 'T002': 10, 'T003': 35, 'T004': 5, 'T005': 20, 'T008': 2, 'T009': 3, 'T010': 4, 'T011': 15, 'T013': 25}

- TARI atoms (kept for cross-reference): 744

## Atom quality filter (Run 5+)

- Input atoms: 579
- Kept: 148
- Rejected: 431
- Kept by paradigm_type: {'prediction': 49, 'analogy': 88, 'open_problem': 7, 'blocker': 2, 'first_principle': 2}
- Kept by transcript: {'T001': 29, 'T002': 10, 'T003': 35, 'T004': 5, 'T005': 20, 'T008': 2, 'T009': 3, 'T010': 4, 'T011': 15, 'T013': 25}
- Kept by reason: {'positive_vocab_hit': 139, 'always_keep_type': 6, 'positive_vocab_AND_always_keep_type': 3}

## Speaker self-publish audit (Run 5+)

- Atoms checked: 148
- Self-publish hits: 3 (hit rate 0.020)
- By speaker:
  - altman: 0/3 hits, matched entries: {}
  - amrith_setlur: 0/20 hits, matched entries: {}
  - belinda_li: 0/29 hits, matched entries: {}
  - hinton: 0/4 hits, matched entries: {}
  - karpathy: 2/25 hits, matched entries: {'karpathy_software_3_0': 2}
  - lecun: 0/15 hits, matched entries: {}
  - nicholas_roberts: 0/35 hits, matched entries: {}
  - sutton: 1/2 hits, matched entries: {'sutton_bitter_lesson': 1}
  - valerie_chen: 0/5 hits, matched entries: {}
  - yu_sun: 0/10 hits, matched entries: {}

## Candidates

- Total: 27
- By operator: {'PREDICTION_GROUNDED_IN_PRINCIPLE': 8, 'ANALOGY_TRANSFERS_TO_OPEN': 8, 'BLOCKER_DISSOLVED_BY_PRINCIPLE': 3, 'PREDICTION_RESOLVES_BLOCKER': 8}
- By type pair: {'prediction+first_principle': 8, 'analogy+open_problem': 8, 'blocker+first_principle': 3, 'prediction+blocker': 8}
- By speaker_class pair: {'academic+tech_leader': 26, 'tech_leader+tech_leader': 1}
- By speaker_diversity: {'2': 27}
- require_cross_leader: True (dropped 0 same-speaker pairs)

## Self-model audit verdicts

- PASS: 25
- PASS_WITH_CAVEAT: 2

## Impact scoring

- Weights mode: heuristic
- N scored: 27
- Top 5 by predicted_impact:
  - CAND_run_005_004  impact=0.510  th=0.0  is=8.0  pt=0.50  ia=0.50
  - CAND_run_005_016  impact=0.510  th=0.0  is=8.0  pt=0.50  ia=0.50
  - CAND_run_005_013  impact=0.493  th=0.0  is=5.0  pt=0.60  ia=0.50
  - CAND_run_005_027  impact=0.493  th=0.0  is=5.0  pt=0.60  ia=0.50
  - CAND_run_005_001  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50

## First-principles stress test

- N total: 27
- PASS_STRESS: 0
- Rejected: 27
- Verdict distribution: {'FAIL_RAG_UNGROUNDED': 27}

## Market verifier

- N total: 0
- SURVIVES_MARKET_CHECK: 0
- Verdict distribution: {}
- Surviving IDs: []

## Final paradigm-shift candidates

None. (run_005: stress and market layers reject when the search cache is empty — see `_search_cache.json`.)

This is mechanism validation only. See `design/paradigm_shift_finder_v1.md` §8 MV-1..MV-5.

---

## Honest acknowledgment

- First-principles RAG check reduces hallucination ~50-70%, not 100%.
- Impact-score classifier needs 10+ runs (50+ candidates, 10-20 labels) to become meaningful.
- Cross-field analogy may produce surface metaphor (R279 risk).
- Tech-leader vision content overlaps Claude's training corpus.
- Run 1 on academic transcripts is mechanism validation only.

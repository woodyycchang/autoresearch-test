# Paradigm-Shift Finder v1 — Run `run_002` Summary

Manifest: `paradigm_shift/runs/run_002/manifest.json`
Run started: unknown
Run ended:   2026-05-22T01:40:09.106251+00:00

## Transcripts

- **T001** Belinda Li — _Building AI systems with coherent and updatable models of the world, user, and themselves_  `tari/inputs/belinda_li_self_models_canonical.txt`
- **T002** Yu Sun — _Test-time training and adaptive computation at inference_  `tari/inputs/transcript_002_yu_sun_canonical.txt`
- **T003** Nicholas Roberts — _Science of foundation models for science_  `tari/inputs/transcript_003_nicholas_roberts_canonical.txt`
- **T004** Valerie Chen — _Human-AI collaboration_  `tari/inputs/transcript_004_valerie_chen_canonical.txt`
- **T005** Amrith Setlur — _Training models to adapt at test time via reinforcement learning_  `tari/inputs/transcript_005_amrith_setlur_canonical.txt`

## Atoms

- Paradigm atoms: 264
- By paradigm_type: {'prediction': 99, 'analogy': 153, 'open_problem': 7, 'blocker': 5}
- By transcript: {'T001': 89, 'T002': 44, 'T003': 67, 'T004': 6, 'T005': 58}

- TARI atoms (kept for cross-reference): 551

## Candidates

- Total: 10
- By operator: {'ANALOGY_TRANSFERS_TO_OPEN': 5, 'PREDICTION_RESOLVES_BLOCKER': 5}
- By type pair: {'analogy+open_problem': 5, 'prediction+blocker': 5}

## Self-model audit verdicts

- PASS: 7
- PASS_WITH_CAVEAT: 3

## Impact scoring

- Weights mode: heuristic
- N scored: 10
- Top 5 by predicted_impact:
  - CAND_run_002_001  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_002_002  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_002_003  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_002_004  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_002_005  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50

## First-principles stress test

- N total: 10
- PASS_STRESS: 10
- Rejected: 0
- Verdict distribution: {'PASS_STRESS': 10}

## Market verifier

- N total: 10
- SURVIVES_MARKET_CHECK: 3
- Verdict distribution: {'FAIL_MARKET_EXISTS': 7, 'SURVIVES_MARKET_CHECK': 3}
- Surviving IDs: ['CAND_run_002_007', 'CAND_run_002_008', 'CAND_run_002_009']

## Final paradigm-shift candidates

### CAND_run_002_007

- Operator: PREDICTION_RESOLVES_BLOCKER
- Atoms: ATOM_T003_S044_PRE_03, ATOM_T002_S020_BLO_01
- Claim: The prediction in atom ATOM_T003_S044_PRE_03 ("And that's going to be very, very small compared to training. I think the big...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- Validity hypothesis: The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.

### CAND_run_002_008

- Operator: PREDICTION_RESOLVES_BLOCKER
- Atoms: ATOM_T003_S030_PRE_02, ATOM_T002_S020_BLO_01
- Claim: The prediction in atom ATOM_T003_S030_PRE_02 ("So now we can move on to the third part here, which is going to be about benc...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- Validity hypothesis: The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.

### CAND_run_002_009

- Operator: PREDICTION_RESOLVES_BLOCKER
- Atoms: ATOM_T003_S039_PRE_02, ATOM_T002_S020_BLO_01
- Claim: The prediction in atom ATOM_T003_S039_PRE_02 ("And that, as a conceptual primitive, is going to be useful for training these...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- Validity hypothesis: The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.


---

## Honest acknowledgment

- First-principles RAG check reduces hallucination ~50-70%, not 100%.
- Impact-score classifier needs 10+ runs (50+ candidates, 10-20 labels) to become meaningful.
- Cross-field analogy may produce surface metaphor (R279 risk).
- Tech-leader vision content overlaps Claude's training corpus.
- Run 1 on academic transcripts is mechanism validation only.

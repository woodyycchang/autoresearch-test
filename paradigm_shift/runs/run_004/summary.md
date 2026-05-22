# Paradigm-Shift Finder v1 — Run `run_004` Summary

Manifest: `paradigm_shift/runs/run_004/manifest.json`
Run started: unknown
Run ended:   2026-05-22T04:00:06.095484+00:00

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

- Total: 5
- By operator: {'PREDICTION_RESOLVES_BLOCKER': 5}
- By type pair: {'prediction+blocker': 5}

## Self-model audit verdicts

- PASS: 5

## Impact scoring

- Weights mode: fitted
- N scored: 5
- Top 5 by predicted_impact:
  - CAND_run_004_001  impact=0.009  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_004_002  impact=0.009  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_004_003  impact=0.009  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_004_005  impact=0.009  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_004_004  impact=0.008  th=0.0  is=8.0  pt=0.50  ia=0.50

## First-principles stress test

- N total: 5
- PASS_STRESS: 4
- Rejected: 1
- Verdict distribution: {'PASS_STRESS': 4, 'FAIL_RAG_UNGROUNDED': 1}

## Market verifier

- N total: 4
- SURVIVES_MARKET_CHECK: 4
- Verdict distribution: {'SURVIVES_MARKET_CHECK': 4}
- Surviving IDs: ['CAND_run_004_001', 'CAND_run_004_002', 'CAND_run_004_003', 'CAND_run_004_005']

## Final paradigm-shift candidates

### CAND_run_004_001

- Operator: PREDICTION_RESOLVES_BLOCKER
- Atoms: ATOM_T005_S045_PRE_01, ATOM_T002_S020_BLO_01
- Claim: The prediction in atom ATOM_T005_S045_PRE_01 ("But the other thing that you notice that scaling model size is not going to b...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- Validity hypothesis: The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.

### CAND_run_004_002

- Operator: PREDICTION_RESOLVES_BLOCKER
- Atoms: ATOM_T003_S006_PRE_02, ATOM_T002_S020_BLO_01
- Claim: The prediction in atom ATOM_T003_S006_PRE_02 ("And finally, we also need to understand when these models are actually going ...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- Validity hypothesis: The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.

### CAND_run_004_003

- Operator: PREDICTION_RESOLVES_BLOCKER
- Atoms: ATOM_T001_S046_PRE_02, ATOM_T002_S020_BLO_01
- Claim: The prediction in atom ATOM_T001_S046_PRE_02 ("So I think one of the end goals of this line of research is to build more tru...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- Validity hypothesis: The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.

### CAND_run_004_005

- Operator: PREDICTION_RESOLVES_BLOCKER
- Atoms: ATOM_T003_S040_PRE_01, ATOM_T002_S020_BLO_01
- Claim: The prediction in atom ATOM_T003_S040_PRE_01 ("That's an ongoing research area that I think will also be very useful for thi...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- Validity hypothesis: The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.


---

## Honest acknowledgment

- First-principles RAG check reduces hallucination ~50-70%, not 100%.
- Impact-score classifier needs 10+ runs (50+ candidates, 10-20 labels) to become meaningful.
- Cross-field analogy may produce surface metaphor (R279 risk).
- Tech-leader vision content overlaps Claude's training corpus.
- Run 1 on academic transcripts is mechanism validation only.

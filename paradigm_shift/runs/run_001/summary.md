# Paradigm-Shift Finder v1 — Run `run_001` Summary

Manifest: `paradigm_shift/runs/run_001/manifest.json`
Run started: unknown
Run ended:   2026-05-21T23:15:09.515389+00:00

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
  - CAND_run_001_001  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_001_002  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_001_003  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_001_004  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50
  - CAND_run_001_005  impact=0.488  th=0.0  is=5.0  pt=0.50  ia=0.50

## First-principles stress test

- N total: 10
- PASS_STRESS: 0
- Rejected: 10
- Verdict distribution: {'FAIL_RAG_UNGROUNDED': 10}

## Market verifier

- N total: 0
- SURVIVES_MARKET_CHECK: 0
- Verdict distribution: {}
- Surviving IDs: []

## Final paradigm-shift candidates

None. (Run 1 expectation: 0 survivors on academic transcripts.)

This is mechanism validation only. See `design/paradigm_shift_finder_v1.md` §8 MV-1..MV-5.

---

## Honest acknowledgment

- First-principles RAG check reduces hallucination ~50-70%, not 100%.
- Impact-score classifier needs 10+ runs (50+ candidates, 10-20 labels) to become meaningful.
- Cross-field analogy may produce surface metaphor (R279 risk).
- Tech-leader vision content overlaps Claude's training corpus.
- Run 1 on academic transcripts is mechanism validation only.

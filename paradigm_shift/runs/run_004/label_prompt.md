# Impact Labeling Prompt — run_004

Please label each candidate below with a 1-5 impact score:
  1 = trivial / wouldn't change anything
  2 = small (one product feature) 
  3 = medium (one startup direction)
  4 = large (subfield-redirecting)
  5 = paradigm-shift (whole industry redirected)

## 1. CAND_run_004_001  (predicted_impact=0.009)

- **Operator:** PREDICTION_RESOLVES_BLOCKER
- **Atoms:** ATOM_T005_S045_PRE_01, ATOM_T002_S020_BLO_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** The prediction in atom ATOM_T005_S045_PRE_01 ("But the other thing that you notice that scaling model size is not going to b...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- **Validity hypothesis:** The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.
- **Why useful:** Predictions that resolve known blockers are higher-value than predictions that simply extrapolate trends — they imply an unaddressed market need.
- **Stress verdict:** PASS_STRESS (2/2 sub-claims grounded)
- **Market verdict:** SURVIVES_MARKET_CHECK (0 matches)

**Your label (1-5):** ___

## 2. CAND_run_004_002  (predicted_impact=0.009)

- **Operator:** PREDICTION_RESOLVES_BLOCKER
- **Atoms:** ATOM_T003_S006_PRE_02, ATOM_T002_S020_BLO_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** The prediction in atom ATOM_T003_S006_PRE_02 ("And finally, we also need to understand when these models are actually going ...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- **Validity hypothesis:** The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.
- **Why useful:** Predictions that resolve known blockers are higher-value than predictions that simply extrapolate trends — they imply an unaddressed market need.
- **Stress verdict:** PASS_STRESS (2/2 sub-claims grounded)
- **Market verdict:** SURVIVES_MARKET_CHECK (0 matches)

**Your label (1-5):** ___

## 3. CAND_run_004_003  (predicted_impact=0.009)

- **Operator:** PREDICTION_RESOLVES_BLOCKER
- **Atoms:** ATOM_T001_S046_PRE_02, ATOM_T002_S020_BLO_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** The prediction in atom ATOM_T001_S046_PRE_02 ("So I think one of the end goals of this line of research is to build more tru...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- **Validity hypothesis:** The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.
- **Why useful:** Predictions that resolve known blockers are higher-value than predictions that simply extrapolate trends — they imply an unaddressed market need.
- **Stress verdict:** PASS_STRESS (2/2 sub-claims grounded)
- **Market verdict:** SURVIVES_MARKET_CHECK (0 matches)

**Your label (1-5):** ___

## 4. CAND_run_004_005  (predicted_impact=0.009)

- **Operator:** PREDICTION_RESOLVES_BLOCKER
- **Atoms:** ATOM_T003_S040_PRE_01, ATOM_T002_S020_BLO_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** The prediction in atom ATOM_T003_S040_PRE_01 ("That's an ongoing research area that I think will also be very useful for thi...") is the resolution of the blocker in atom ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to fi...").
- **Validity hypothesis:** The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.
- **Why useful:** Predictions that resolve known blockers are higher-value than predictions that simply extrapolate trends — they imply an unaddressed market need.
- **Stress verdict:** PASS_STRESS (2/2 sub-claims grounded)
- **Market verdict:** SURVIVES_MARKET_CHECK (0 matches)

**Your label (1-5):** ___

---
To record labels, run:
  python paradigm_shift/impact_label_logger.py record \
    --run_id <ID> --candidates_dir <DIR> --labels '<CAND_ID>:<SCORE>,...'

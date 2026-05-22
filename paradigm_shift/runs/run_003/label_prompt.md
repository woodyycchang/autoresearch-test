# Impact Labeling Prompt — run_003

Please label each candidate below with a 1-5 impact score:
  1 = trivial / wouldn't change anything
  2 = small (one product feature) 
  3 = medium (one startup direction)
  4 = large (subfield-redirecting)
  5 = paradigm-shift (whole industry redirected)

## 1. CAND_run_003_010  (predicted_impact=0.010)

- **Operator:** PREDICTION_RESOLVES_BLOCKER
- **Atoms:** ATOM_T001_S051_PRE_01, ATOM_T005_S010_BLO_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.35
- **Info asymmetry:** 0.50

- **Claim:** The prediction in atom ATOM_T001_S051_PRE_01 ("I think what I'm talking about here is like so like I think physics is intere...") is the resolution of the blocker in atom ATOM_T005_S010_BLO_01 ("Now, in many cases, we cannot evaluate these intermediate operations, but we ...").
- **Validity hypothesis:** The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.
- **Why useful:** Predictions that resolve known blockers are higher-value than predictions that simply extrapolate trends — they imply an unaddressed market need.
- **Stress verdict:** PASS_STRESS (2/2 sub-claims grounded)
- **Market verdict:** FAIL_MARKET_EXISTS (2 matches)

**Your label (1-5):** ___

## 2. CAND_run_003_001  (predicted_impact=0.009)

- **Operator:** ANALOGY_TRANSFERS_TO_OPEN
- **Atoms:** ATOM_T001_S038_ANA_01, ATOM_T003_S002_OPE_03
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Apply the analogical structure in atom ATOM_T001_S038_ANA_01 ("For example, here, let's say it's like the recipe calls for three ounces of s...") to the open problem framed in atom ATOM_T003_S002_OPE_03 ("Now the leap from coding unsolved math, we needed something more.").
- **Validity hypothesis:** The structural correspondence in the analogy preserves the open problem's constraint pattern; the analogy is not merely a surface metaphor.
- **Why useful:** Open problems gain a candidate solution shape from the analogy's source domain; the source domain's known constraints become hypotheses for the target.
- **Stress verdict:** PASS_STRESS (2/2 sub-claims grounded)
- **Market verdict:** FAIL_MARKET_EXISTS (1 matches)

**Your label (1-5):** ___

## 3. CAND_run_003_002  (predicted_impact=0.009)

- **Operator:** ANALOGY_TRANSFERS_TO_OPEN
- **Atoms:** ATOM_T004_S003_ANA_01, ATOM_T003_S002_OPE_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Apply the analogical structure in atom ATOM_T004_S003_ANA_01 ("And of course then also some of the talk will talk about like you know how th...") to the open problem framed in atom ATOM_T003_S002_OPE_01 ("And around now we have this next frontier that where we're applying these age...").
- **Validity hypothesis:** The structural correspondence in the analogy preserves the open problem's constraint pattern; the analogy is not merely a surface metaphor.
- **Why useful:** Open problems gain a candidate solution shape from the analogy's source domain; the source domain's known constraints become hypotheses for the target.
- **Stress verdict:** PASS_STRESS (2/2 sub-claims grounded)
- **Market verdict:** FAIL_MARKET_EXISTS (1 matches)

**Your label (1-5):** ___

## 4. CAND_run_003_003  (predicted_impact=0.009)

- **Operator:** ANALOGY_TRANSFERS_TO_OPEN
- **Atoms:** ATOM_T005_S005_ANA_01, ATOM_T003_S002_OPE_02
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Apply the analogical structure in atom ATOM_T005_S005_ANA_01 ("So pre-trained models like large-language models or LLMs, they're trained on ...") to the open problem framed in atom ATOM_T003_S002_OPE_02 ("These are unsolved problems that are just available for people to solve and m...").
- **Validity hypothesis:** The structural correspondence in the analogy preserves the open problem's constraint pattern; the analogy is not merely a surface metaphor.
- **Why useful:** Open problems gain a candidate solution shape from the analogy's source domain; the source domain's known constraints become hypotheses for the target.
- **Stress verdict:** PASS_STRESS (2/2 sub-claims grounded)
- **Market verdict:** FAIL_MARKET_EXISTS (1 matches)

**Your label (1-5):** ___

## 5. CAND_run_003_004  (predicted_impact=0.009)

- **Operator:** ANALOGY_TRANSFERS_TO_OPEN
- **Atoms:** ATOM_T001_S020_ANA_03, ATOM_T003_S002_OPE_03
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Apply the analogical structure in atom ATOM_T001_S020_ANA_03 ("And so like we use those probes.") to the open problem framed in atom ATOM_T003_S002_OPE_03 ("Now the leap from coding unsolved math, we needed something more.").
- **Validity hypothesis:** The structural correspondence in the analogy preserves the open problem's constraint pattern; the analogy is not merely a surface metaphor.
- **Why useful:** Open problems gain a candidate solution shape from the analogy's source domain; the source domain's known constraints become hypotheses for the target.
- **Stress verdict:** PASS_STRESS (2/2 sub-claims grounded)
- **Market verdict:** FAIL_MARKET_EXISTS (1 matches)

**Your label (1-5):** ___

---
To record labels, run:
  python paradigm_shift/impact_label_logger.py record \
    --run_id <ID> --candidates_dir <DIR> --labels '<CAND_ID>:<SCORE>,...'

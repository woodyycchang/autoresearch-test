# Impact Labeling Prompt — run_005

Please label each candidate below with a 1-5 impact score:
  1 = trivial / wouldn't change anything
  2 = small (one product feature) 
  3 = medium (one startup direction)
  4 = large (subfield-redirecting)
  5 = paradigm-shift (whole industry redirected)

## 1. CAND_run_005_004  (predicted_impact=0.510)

- **Operator:** PREDICTION_GROUNDED_IN_PRINCIPLE
- **Atoms:** ATOM_T001_S046_PRE_04, ATOM_T013_S001_FIR_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 8.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Prediction in atom ATOM_T001_S046_PRE_04 ("Second, if we can extract world models from our AI systems, then we can poten...") holds if and only if the first-principle constraint in atom ATOM_T013_S001_FIR_01 ("think fundamentally the reason for that is that software is changing again. A...") is binding.
- **Validity hypothesis:** The prediction "Second, if we can extract world models from our AI system..." is forced by the underlying constraint "think fundamentally the reason for that is that software ..."; if the constraint is not binding the prediction may still hold by accident but the binding case is the load-bearing version of this candidate.
- **Why useful:** A prediction that is forced by a first-principle is more falsifiable than a free-floating prediction: if the principle holds and the prediction fails, one of them is wrong, which is a binary research question.

**Your label (1-5):** ___

## 2. CAND_run_005_016  (predicted_impact=0.510)

- **Operator:** ANALOGY_TRANSFERS_TO_OPEN
- **Atoms:** ATOM_T011_S027_ANA_02, ATOM_T001_S046_OPE_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 8.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Apply the analogical structure in atom ATOM_T011_S027_ANA_02 ("kind of like the hippocampus in the mammalian brain. The world model, which i...") to the open problem framed in atom ATOM_T001_S046_OPE_01 ("However, many of these broader challenges remain open problems. And going for...").
- **Validity hypothesis:** The structural correspondence in the analogy preserves the open problem's constraint pattern; the analogy is not merely a surface metaphor.
- **Why useful:** Open problems gain a candidate solution shape from the analogy's source domain; the source domain's known constraints become hypotheses for the target.

**Your label (1-5):** ___

## 3. CAND_run_005_013  (predicted_impact=0.493)

- **Operator:** ANALOGY_TRANSFERS_TO_OPEN
- **Atoms:** ATOM_T013_S023_ANA_02, ATOM_T003_S002_OPE_03
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.60
- **Info asymmetry:** 0.50

- **Claim:** Apply the analogical structure in atom ATOM_T013_S023_ANA_02 ("you can instruct or like advise I suppose web crawlers on how to behave on yo...") to the open problem framed in atom ATOM_T003_S002_OPE_03 ("Now the leap from coding unsolved math, we needed something more.").
- **Validity hypothesis:** The structural correspondence in the analogy preserves the open problem's constraint pattern; the analogy is not merely a surface metaphor.
- **Why useful:** Open problems gain a candidate solution shape from the analogy's source domain; the source domain's known constraints become hypotheses for the target.

**Your label (1-5):** ___

## 4. CAND_run_005_027  (predicted_impact=0.493)

- **Operator:** PREDICTION_RESOLVES_BLOCKER
- **Atoms:** ATOM_T003_S013_PRE_01, ATOM_T008_S001_BLO_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.60
- **Info asymmetry:** 0.50

- **Claim:** The prediction in atom ATOM_T003_S013_PRE_01 ("And this is going to be true of our flux agent example as well. We're going t...") is the resolution of the blocker in atom ATOM_T008_S001_BLO_01 ("learning and why we can't start with LLMs to do that >> well in every case th...").
- **Validity hypothesis:** The predicted future state contains a mechanism that removes the named blocker; the prediction is therefore a market signal for the resolution mechanism.
- **Why useful:** Predictions that resolve known blockers are higher-value than predictions that simply extrapolate trends — they imply an unaddressed market need.

**Your label (1-5):** ___

## 5. CAND_run_005_001  (predicted_impact=0.488)

- **Operator:** PREDICTION_GROUNDED_IN_PRINCIPLE
- **Atoms:** ATOM_T002_S046_PRE_01, ATOM_T013_S001_FIR_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Prediction in atom ATOM_T002_S046_PRE_01 ("I think that's a reasonable prediction, given the plots we have seen so far. ...") holds if and only if the first-principle constraint in atom ATOM_T013_S001_FIR_01 ("think fundamentally the reason for that is that software is changing again. A...") is binding.
- **Validity hypothesis:** The prediction "I think that's a reasonable prediction, given the plots w..." is forced by the underlying constraint "think fundamentally the reason for that is that software ..."; if the constraint is not binding the prediction may still hold by accident but the binding case is the load-bearing version of this candidate.
- **Why useful:** A prediction that is forced by a first-principle is more falsifiable than a free-floating prediction: if the principle holds and the prediction fails, one of them is wrong, which is a binary research question.

**Your label (1-5):** ___

---
To record labels, run:
  python paradigm_shift/impact_label_logger.py record \
    --run_id <ID> --candidates_dir <DIR> --labels '<CAND_ID>:<SCORE>,...'

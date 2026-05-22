# Impact Labeling Prompt — run_001

Please label each candidate below with a 1-5 impact score:
  1 = trivial / wouldn't change anything
  2 = small (one product feature) 
  3 = medium (one startup direction)
  4 = large (subfield-redirecting)
  5 = paradigm-shift (whole industry redirected)

## 1. CAND_run_001_001  (predicted_impact=0.488)

- **Operator:** ANALOGY_TRANSFERS_TO_OPEN
- **Atoms:** ATOM_T001_S038_ANA_01, ATOM_T003_S002_OPE_03
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Apply the analogical structure in atom ATOM_T001_S038_ANA_01 ("For example, here, let's say it's like the recipe calls for three ounces of s...") to the open problem framed in atom ATOM_T003_S002_OPE_03 ("Now the leap from coding unsolved math, we needed something more.").
- **Validity hypothesis:** The structural correspondence in the analogy preserves the open problem's constraint pattern; the analogy is not merely a surface metaphor.
- **Why useful:** Open problems gain a candidate solution shape from the analogy's source domain; the source domain's known constraints become hypotheses for the target.

**Your label (1-5):** ___

## 2. CAND_run_001_002  (predicted_impact=0.488)

- **Operator:** ANALOGY_TRANSFERS_TO_OPEN
- **Atoms:** ATOM_T004_S003_ANA_01, ATOM_T003_S002_OPE_01
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Apply the analogical structure in atom ATOM_T004_S003_ANA_01 ("And of course then also some of the talk will talk about like you know how th...") to the open problem framed in atom ATOM_T003_S002_OPE_01 ("And around now we have this next frontier that where we're applying these age...").
- **Validity hypothesis:** The structural correspondence in the analogy preserves the open problem's constraint pattern; the analogy is not merely a surface metaphor.
- **Why useful:** Open problems gain a candidate solution shape from the analogy's source domain; the source domain's known constraints become hypotheses for the target.

**Your label (1-5):** ___

## 3. CAND_run_001_003  (predicted_impact=0.488)

- **Operator:** ANALOGY_TRANSFERS_TO_OPEN
- **Atoms:** ATOM_T005_S005_ANA_01, ATOM_T003_S002_OPE_02
- **Time horizon:** 0.0 years
- **Impact scale (log10):** 5.0
- **POC tractability:** 0.50
- **Info asymmetry:** 0.50

- **Claim:** Apply the analogical structure in atom ATOM_T005_S005_ANA_01 ("So pre-trained models like large-language models or LLMs, they're trained on ...") to the open problem framed in atom ATOM_T003_S002_OPE_02 ("These are unsolved problems that are just available for people to solve and m...").
- **Validity hypothesis:** The structural correspondence in the analogy preserves the open problem's constraint pattern; the analogy is not merely a surface metaphor.
- **Why useful:** Open problems gain a candidate solution shape from the analogy's source domain; the source domain's known constraints become hypotheses for the target.

**Your label (1-5):** ___

---
To record labels, run:
  python paradigm_shift/impact_label_logger.py record \
    --run_id <ID> --candidates_dir <DIR> --labels '<CAND_ID>:<SCORE>,...'

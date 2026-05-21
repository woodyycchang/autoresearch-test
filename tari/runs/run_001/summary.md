# TARI v1 — Run `001` Summary

Transcript: `tari/inputs/belinda_li_self_models_canonical.txt`

Ended at: 2026-05-21T12:47:28.507130+00:00


---

## Pipeline counts

- Snippets: **55**
- Atoms: **162**
- Candidates (brainstorm): **12**

## Audit verdicts (Belinda Q1/Q2/Q3)

- PASS: 7
- PASS_WITH_CAVEAT: 5

## External verification verdicts

- FAIL_STEP_06_KEYWORD_THRESHOLD: 12


---

## Per-candidate detail


### CAND_001_001  (ANALOGIZE)

- Atoms: ATOM_S005_01, ATOM_S025_04
- Source snippets: S005, S025
- Claim: Apply the mechanism described in atom ATOM_S005_01 ("So failures of coherence refers to the ability or inability for AI systems to...") to the problem framed in atom ATOM_S025_04 ("So the critical takeaway is we can kind of draw the boundary line between the...").
- Audit verdict: **PASS_WITH_CAVEAT**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'ANALOGIZE' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
  - Caveats: ['AUX_claim_largely_restates_ATOM_S025_04']
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 2 / 3
  - step 14.6 max sim: 0.108
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_002  (ANALOGIZE)

- Atoms: ATOM_S004_01, ATOM_S017_05
- Source snippets: S004, S017
- Claim: Apply the mechanism described in atom ATOM_S004_01 ("So there's going to be failures of coherence and there's going to be failures...") to the problem framed in atom ATOM_S017_05 ("To do that we can patch in activations from the second input into the first i...").
- Audit verdict: **PASS_WITH_CAVEAT**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'ANALOGIZE' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
  - Caveats: ['AUX_claim_largely_restates_ATOM_S004_01']
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.122
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_003  (COMPOSE)

- Atoms: ATOM_S004_01, ATOM_S025_01
- Source snippets: S004, S025
- Claim: Compose the primitive in atom ATOM_S004_01 with the primitive in atom ATOM_S025_01: apply the first to produce an intermediate representation, then apply the second to that representation.
- Audit verdict: **PASS**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'COMPOSE' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.227
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_004  (COMPOSE)

- Atoms: ATOM_S004_01, ATOM_S011_01
- Source snippets: S004, S011
- Claim: Compose the primitive in atom ATOM_S004_01 with the primitive in atom ATOM_S011_01: apply the first to produce an intermediate representation, then apply the second to that representation.
- Audit verdict: **PASS**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'COMPOSE' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.188
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_005  (INVERT)

- Atoms: ATOM_S039_03
- Source snippets: S039
- Claim: Negate the directional assumption of atom ATOM_S039_03 ("This implies that X2 was actually used by the language model to make to make ..."): study the case where the relation is reversed (output drives the input rather than input drives the output).
- Audit verdict: **PASS**
  - Q1 (atoms exist): True — all 1 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'INVERT' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 1 cited atoms' quotes found verbatim
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.205
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_006  (RESTRICT)

- Atoms: ATOM_S006_02, ATOM_S013_07
- Source snippets: S006, S013
- Claim: Restrict the general claim of atom ATOM_S006_02 to the specific scenario described in atom ATOM_S013_07 ("So like Jack possesses the book and Janet does not possess the book. Okay and..."). Does the general claim still hold under this restriction?
- Audit verdict: **PASS**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'RESTRICT' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.06
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_007  (INVERT)

- Atoms: ATOM_S046_02
- Source snippets: S046
- Claim: Negate the directional assumption of atom ATOM_S046_02 ("We can get better specification inference and by training language models to ..."): study the case where the relation is reversed (output drives the input rather than input drives the output).
- Audit verdict: **PASS**
  - Q1 (atoms exist): True — all 1 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'INVERT' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 1 cited atoms' quotes found verbatim
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.257
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_008  (GENERALIZE)

- Atoms: ATOM_S001_01, ATOM_S008_01
- Source snippets: S001, S008
- Claim: Generalize the specific claim in atom ATOM_S001_01 ("And I'll also talk about how we can actually do this. So, okay, these models,...") to the broader category implied by atom ATOM_S008_01: state the claim as a class-level property of the category, not just the specific case.
- Audit verdict: **PASS**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'GENERALIZE' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.283
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_009  (RESTRICT)

- Atoms: ATOM_S001_01, ATOM_S049_01
- Source snippets: S001, S049
- Claim: Restrict the general claim of atom ATOM_S001_01 to the specific scenario described in atom ATOM_S049_01 ("So maybe there's like 10 to 50 percent change."). Does the general claim still hold under this restriction?
- Audit verdict: **PASS_WITH_CAVEAT**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'RESTRICT' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
  - Caveats: ['AUX_claim_largely_restates_ATOM_S049_01']
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.105
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_010  (CONTRAST)

- Atoms: ATOM_S004_01, ATOM_S013_04
- Source snippets: S004, S013
- Claim: Contrast the primitive in atom ATOM_S004_01 with the primitive in atom ATOM_S013_04: identify the structural axis on which they differ and the cases where one would dominate the other.
- Audit verdict: **PASS_WITH_CAVEAT**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'CONTRAST' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
  - Caveats: ['AUX_novelty_field_lacks_snippet_reference']
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.206
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_011  (CONTRAST)

- Atoms: ATOM_S004_01, ATOM_S026_02
- Source snippets: S004, S026
- Claim: Contrast the primitive in atom ATOM_S004_01 with the primitive in atom ATOM_S026_02: identify the structural axis on which they differ and the cases where one would dominate the other.
- Audit verdict: **PASS_WITH_CAVEAT**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'CONTRAST' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
  - Caveats: ['AUX_novelty_field_lacks_snippet_reference']
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.174
  - step 13.5 survives attack: True
  - real WebSearch issued: True

### CAND_001_012  (GENERALIZE)

- Atoms: ATOM_S001_01, ATOM_S024_01
- Source snippets: S001, S024
- Claim: Generalize the specific claim in atom ATOM_S001_01 ("And I'll also talk about how we can actually do this. So, okay, these models,...") to the broader category implied by atom ATOM_S024_01: state the claim as a class-level property of the category, not just the specific case.
- Audit verdict: **PASS**
  - Q1 (atoms exist): True — all 2 cited atoms exist in atoms_dir
  - Q2 (operator valid): True — operator 'GENERALIZE' is one of the 6 valid operators
  - Q3 (quotes verbatim): True — all 2 cited atoms' quotes found verbatim
- External verdict: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 keyword hits: 3 / 3
  - step 14.6 max sim: 0.133
  - step 13.5 survives attack: True
  - real WebSearch issued: True

---

## Atom type distribution

- PRIMITIVE: 93
- MECHANISM_CLAIM: 43
- METRIC: 10
- OPEN_QUESTION: 9
- NEGATIVE_RESULT: 7

## Snippet coverage

- First snippet: lines 1-14
- Last snippet: lines 630-636
- Mean sentences/snippet: 11.6
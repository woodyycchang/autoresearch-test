# TARI v2 — Run `002` Summary (multi-transcript)

Manifest: `tari/runs/run_002/manifest.json`
Run mode: **multi_transcript_v2**
Ended at: 2026-05-21T13:44:03.795502+00:00


---

## Transcripts

- **T001** Belinda Li — _Building AI systems with coherent and updatable models of the world, user, and themselves_ (55 snippets, 162 atoms) `tari/inputs/belinda_li_self_models_canonical.txt`
- **T002** Yu Sun — _Test-time training and adaptive computation at inference_ (57 snippets, 95 atoms) `tari/inputs/transcript_002_yu_sun_canonical.txt`
- **T003** Nicholas Roberts — _Science of foundation models for science (FMs as scientific instruments)_ (44 snippets, 97 atoms) `tari/inputs/transcript_003_nicholas_roberts_canonical.txt`
- **T004** Valerie Chen — _Human-AI collaboration: measuring and improving how AI works with people_ (4 snippets, 1 atoms) `tari/inputs/transcript_004_valerie_chen_canonical.txt`
- **T005** Amrith Setlur — _Training models to adapt at test time via reinforcement learning_ (63 snippets, 196 atoms) `tari/inputs/transcript_005_amrith_setlur_canonical.txt`

Total: **223** snippets, **551** atoms.

## Pipeline configuration

- cross_transcript_required: **True**
- per_pair_cap: **2**
- strict_real_search: **True**
- n_candidates_brainstormed: 19

## Audit verdicts

- PASS: 13
- PASS_WITH_CAVEAT: 6

## External verification verdicts (strict_real_search=True)

- FAIL_STEP_06_KEYWORD_THRESHOLD: 19

---

## Per-candidate detail


### CAND_002_001  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T001_S025_03, ATOM_T003_S002_04
- Source transcripts: T001, T003
- Source snippets: S025, S002
- Claim: Apply the mechanism described in atom ATOM_T001_S025_03 ("And starting from probing, we're specifically going to do a variant where we'...") to the problem framed in atom ATOM_T003_S002_04 ("Now the leap from coding unsolved math, we needed something more.").
- Audit: **PASS_WITH_CAVEAT**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
  - Caveats: ['AUX_claim_largely_restates_ATOM_T003_S002_04']
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.148
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_002  (COMPOSE)  diversity=2

- Atoms: ATOM_T002_S014_01, ATOM_T004_S002_01
- Source transcripts: T002, T004
- Source snippets: S014, S002
- Claim: Compose the primitive in atom ATOM_T002_S014_01 with the primitive in atom ATOM_T004_S002_01: apply the first to produce an intermediate representation, then apply the second to that representation.
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.143
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_003  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T003_S027_01, ATOM_T005_S046_06
- Source transcripts: T003, T005
- Source snippets: S027, S046
- Claim: Apply the mechanism described in atom ATOM_T003_S027_01 ("And here in green, we have our actual algorithm, our skillet algorithm, and i...") to the problem framed in atom ATOM_T005_S046_06 ("That's what we used to bootstrap exploration during RL training.").
- Audit: **PASS_WITH_CAVEAT**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
  - Caveats: ['AUX_claim_largely_restates_ATOM_T005_S046_06']
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.227
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_004  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T005_S057_01, ATOM_T002_S010_02
- Source transcripts: T005, T002
- Source snippets: S057, S010
- Claim: Apply the mechanism described in atom ATOM_T005_S057_01 ("But this kind of exploration we're looking at is something that goes beyond j...") to the problem framed in atom ATOM_T002_S010_02 ("What's even more amazing is there is this problem that is an open problem in ...").
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.205
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_005  (COMPOSE)  diversity=2

- Atoms: ATOM_T003_S027_01, ATOM_T004_S002_01
- Source transcripts: T003, T004
- Source snippets: S027, S002
- Claim: Compose the primitive in atom ATOM_T003_S027_01 with the primitive in atom ATOM_T004_S002_01: apply the first to produce an intermediate representation, then apply the second to that representation.
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.087
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_006  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T005_S059_01, ATOM_T001_S052_05
- Source transcripts: T005, T001
- Source snippets: S059, S052
- Claim: Apply the mechanism described in atom ATOM_T005_S059_01 ("Like does it help with the model to learn, like to explore during test time o...") to the problem framed in atom ATOM_T001_S052_05 ("They use some like structural causal model to avoid burning. Like for example...").
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.333
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_007  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T003_S027_01, ATOM_T002_S010_02
- Source transcripts: T003, T002
- Source snippets: S027, S010
- Claim: Apply the mechanism described in atom ATOM_T003_S027_01 ("And here in green, we have our actual algorithm, our skillet algorithm, and i...") to the problem framed in atom ATOM_T002_S010_02 ("What's even more amazing is there is this problem that is an open problem in ...").
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.1
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_008  (COMPOSE)  diversity=2

- Atoms: ATOM_T005_S010_01, ATOM_T004_S002_01
- Source transcripts: T005, T004
- Source snippets: S010, S002
- Claim: Compose the primitive in atom ATOM_T005_S010_01 with the primitive in atom ATOM_T004_S002_01: apply the first to produce an intermediate representation, then apply the second to that representation.
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.075
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_009  (GENERALIZE)  diversity=2

- Atoms: ATOM_T001_S037_05, ATOM_T004_S002_01
- Source transcripts: T001, T004
- Source snippets: S037, S002
- Claim: Generalize the specific claim in atom ATOM_T001_S037_05 ("So we can train another model to try to explain the first model. And we're go...") to the broader category implied by atom ATOM_T004_S002_01: state the claim as a class-level property of the category, not just the specific case.
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 2 / 3
  - step 14.6 max_sim: 0.116
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_010  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T002_S023_02, ATOM_T001_S042_03
- Source transcripts: T002, T001
- Source snippets: S023, S042
- Claim: Apply the mechanism described in atom ATOM_T002_S023_02 ("7 times faster than just doing a single forward pass of a transformer with fu...") to the problem framed in atom ATOM_T001_S042_03 ("So first, we learned that language models build latent world models, and they...").
- Audit: **PASS_WITH_CAVEAT**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
  - Caveats: ['AUX_claim_largely_restates_ATOM_T002_S023_02']
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.154
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_011  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T003_S035_01, ATOM_T001_S040_05
- Source transcripts: T003, T001
- Source snippets: S035, S040
- Claim: Apply the mechanism described in atom ATOM_T003_S035_01 ("And so what we did in ML Gym, and this was my main contribution here that end...") to the problem framed in atom ATOM_T001_S040_05 ("So here we see the results and we see indeed they can produce highly accurate...").
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.132
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_012  (CONTRAST)  diversity=2

- Atoms: ATOM_T002_S014_01, ATOM_T004_S002_01
- Source transcripts: T002, T004
- Source snippets: S014, S002
- Claim: Contrast the primitive in atom ATOM_T002_S014_01 with the primitive in atom ATOM_T004_S002_01: identify the structural axis on which they differ and the cases where one would dominate the other.
- Audit: **PASS_WITH_CAVEAT**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
  - Caveats: ['AUX_novelty_field_lacks_snippet_reference']
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.241
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_013  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T003_S027_01, ATOM_T005_S052_03
- Source transcripts: T003, T005
- Source snippets: S027, S052
- Claim: Apply the mechanism described in atom ATOM_T003_S027_01 ("And here in green, we have our actual algorithm, our skillet algorithm, and i...") to the problem framed in atom ATOM_T005_S052_03 ("The goal here is to train models in such a way such that they're effective al...").
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.2
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_014  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T002_S053_01, ATOM_T005_S021_04
- Source transcripts: T002, T005
- Source snippets: S053, S021
- Claim: Apply the mechanism described in atom ATOM_T002_S053_01 ("I wonder if you can comment about not single user, but multiple user version ...") to the problem framed in atom ATOM_T005_S021_04 ("How do we learn an algorithm? That's fairly simple.").
- Audit: **PASS_WITH_CAVEAT**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
  - Caveats: ['AUX_claim_largely_restates_ATOM_T005_S021_04']
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.138
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_015  (COMPOSE)  diversity=2

- Atoms: ATOM_T003_S035_01, ATOM_T004_S002_01
- Source transcripts: T003, T004
- Source snippets: S035, S002
- Claim: Compose the primitive in atom ATOM_T003_S035_01 with the primitive in atom ATOM_T004_S002_01: apply the first to produce an intermediate representation, then apply the second to that representation.
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.136
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_016  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T001_S017_03, ATOM_T005_S007_02
- Source transcripts: T001, T005
- Source snippets: S017, S007
- Claim: Apply the mechanism described in atom ATOM_T001_S017_03 ("So concretely as an example we might have Janet gave Jack the book and Jack g...") to the problem framed in atom ATOM_T005_S007_02 ("Second, if we use the right techniques, we can train this algorithm effective...").
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.25
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_017  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T003_S035_01, ATOM_T002_S033_02
- Source transcripts: T003, T002
- Source snippets: S035, S033
- Claim: Apply the mechanism described in atom ATOM_T003_S035_01 ("And so what we did in ML Gym, and this was my main contribution here that end...") to the problem framed in atom ATOM_T002_S033_02 ("So how do we do it concretely? Let me use GPU kernel engineering as an example.").
- Audit: **PASS_WITH_CAVEAT**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
  - Caveats: ['AUX_claim_largely_restates_ATOM_T002_S033_02']
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.2
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_018  (COMPOSE)  diversity=2

- Atoms: ATOM_T005_S023_02, ATOM_T004_S002_01
- Source transcripts: T005, T004
- Source snippets: S023, S002
- Claim: Compose the primitive in atom ATOM_T005_S023_02 with the primitive in atom ATOM_T004_S002_01: apply the first to produce an intermediate representation, then apply the second to that representation.
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.093
  - step 13.5 survives: True
  - real_websearch: True

### CAND_002_019  (ANALOGIZE)  diversity=2

- Atoms: ATOM_T002_S010_01, ATOM_T001_S012_04
- Source transcripts: T002, T001
- Source snippets: S010, S012
- Claim: Apply the mechanism described in atom ATOM_T002_S010_01 ("What's even more amazing is there is this problem that is an open problem in ...") to the problem framed in atom ATOM_T001_S012_04 ("They build vector representations across each token down a number of layers a...").
- Audit: **PASS**
  - Q1 atoms_exist: True
  - Q2 operator_valid: True
  - Q3 quotes_verbatim: True
- External: **FAIL_STEP_06_KEYWORD_THRESHOLD**
  - step 06 kw_hits: 3 / 3
  - step 14.6 max_sim: 0.196
  - step 13.5 survives: True
  - real_websearch: True
---

## TARI v2 Epoch 1 (run_002) — Scientific findings

### Headline verdicts

- **Pipeline executed end-to-end across 5 transcripts.** 223 snippets → 551 atoms → 19 cross-transcript candidates. Every candidate has transcript_diversity ≥ 2 (enforced; 3010 single-transcript candidates were dropped from a candidate pool of 7432 generated).
- **Strict real WebSearch enforced.** strict_real_search=True. 19 candidates, 19 real WebSearch queries issued from main context, 57 results captured verbatim. No synthesized fallback.
- **0 candidates survive external verification** under conservative kw threshold ≥ 2 (mining's program_v20 threshold). Under stricter threshold ≥ 5, 4 candidates marginally survive — but all 4 owe their survival to T004's single generic atom diluting the candidate's specificity, not to genuine novelty.

### Pair coverage

10 unordered transcript pairs are possible (5 choose 2). 19 candidates cover **all 10 pairs**:

| Pair | n_candidates | Speakers |
|---|---|---|
| T001+T002 | 2 | Belinda Li + Yu Sun |
| T001+T003 | 2 | Belinda Li + Nicholas Roberts |
| T001+T004 | 1 | Belinda Li + Valerie Chen |
| T001+T005 | 2 | Belinda Li + Amrith Setlur |
| T002+T003 | 2 | Yu Sun + Nicholas Roberts |
| T002+T004 | 2 | Yu Sun + Valerie Chen |
| T002+T005 | 2 | Yu Sun + Amrith Setlur |
| T003+T004 | 2 | Nicholas Roberts + Valerie Chen |
| T003+T005 | 2 | Nicholas Roberts + Amrith Setlur |
| T004+T005 | 2 | Valerie Chen + Amrith Setlur |

T001+T004 has only 1 because T004 has only 1 atom total. Otherwise: full 10-pair coverage.

### Did cross-transcript candidates avoid single-speaker prior-art collisions?

**No.** Every candidate's nearest prior art is in the broader 2024-2026 LLM-research community, not bounded to a single speaker. Sample collisions:

| Pair | Candidate | Operator | Nearest prior art (real WebSearch) |
|---|---|---|---|
| T001+T002 | CAND_002_010 | ANALOGIZE | KV-cache speedup + multi-head latent attention (arXiv:2507.11273) |
| T001+T003 | CAND_002_001 | ANALOGIZE | VAR-MATH probing for mathematical reasoning variants (arXiv:2507.12885) |
| T001+T005 | CAND_002_016 | ANALOGIZE | Counterfactual simulation training for CoT (arXiv:2602.20710) |
| T002+T005 | CAND_002_004 | ANALOGIZE | Population-Evolve parallel sampling (arXiv:2512.19081), Sequential sampling exploration (arXiv:2510.15502) |
| T003+T005 | CAND_002_013 | ANALOGIZE | RLVE adaptive verifiable environments (arXiv:2511.07317), TTRL test-time RL (arXiv:2504.16084) |
| T004+T005 | CAND_002_018 | COMPOSE | DeepSWE RL coding agent (together.ai), test-time curricula RL (arXiv:2510.04786) |

### §3.5 single-transcript-bias hypothesis: TESTED

run_001's dominant failure mode (§3.5) was the hypothesis that *because all candidates come from one transcript, they trivially fall in that speaker's community's prior art*. run_002 tested this by combining atoms across 5 transcripts spanning 4 distinct communities (mech-interp, test-time training, FMs-for-science, human-AI collaboration).

**Outcome: §3.5 is FALSIFIED as the dominant failure mode.** Cross-transcript candidates land in *broader* arxiv-2024-2026 prior art, not in any single speaker's community. The failure is not "single-speaker bias" but "the broader ML research field is saturated".

Example: CAND_002_004 combines Yu Sun (TTT) and Amrith Setlur (RL test-time) — a sensible cross-talk pairing. The candidate's claim about combining their primitives for exploration collides with Population-Evolve (Dec 2025) and "Road Less Traveled: Sequential Sampling Exploration" (Oct 2025) — papers from a third community (LLM-math-reasoning) that neither speaker is a primary author of.

This is a **substantively different finding** from run_001. The cross-transcript design escaped one bias and exposed a deeper one: the LLM frontier-research community as a whole is dense enough that virtually any 2-atom combination from 5 frontier talks lands within a 6-month publishing window of arxiv.

### Marginal survivors at kw threshold = 5

| Candidate | Operator | Pair | Max kw_overlap | Real survivor? |
|---|---|---|---|---|
| CAND_002_001 | ANALOGIZE | T001+T003 | 4 | No — atom T001_S025_03 is generic ("starting from probing, we're going to do a variant"); search returns generic-probing papers with low keyword overlap. |
| CAND_002_005 | COMPOSE | T003+T004 | 4 | No — T004's single atom is generic. |
| CAND_002_007 | ANALOGIZE | T002+T003 | 4 | No — atom T003_S035_04 is name-laden ("our skillet algorithm") which doesn't keyword-overlap with non-skillet papers. |
| CAND_002_018 | COMPOSE | T004+T005 | 4 | No — T004's single atom is generic. |

All 4 marginal survivors involve either T004 (a transcript whose only atom is a generic statement about model limitations) or T003's idiosyncratically-named "skillet" algorithm. None represent a genuinely novel candidate that escaped real prior art.

### Per-pair yield (10 pairs)

| Pair | Candidates | Median sim | Median kw_hits | Real niche detected? |
|---|---|---|---|---|
| T001+T002 | 2 | 0.175 | 3.0 | No |
| T001+T003 | 2 | 0.124 | 2.5 | No |
| T001+T004 | 1 | 0.116 | 2.0 | No (T004 atom is generic) |
| T001+T005 | 2 | 0.291 | 3.0 | No |
| T002+T003 | 2 | 0.122 | 3.0 | No |
| T002+T004 | 2 | 0.192 | 3.0 | No |
| T002+T005 | 2 | 0.140 | 3.0 | No |
| T003+T004 | 2 | 0.111 | 3.0 | No (T004 atom is generic) |
| T003+T005 | 2 | 0.213 | 3.0 | No |
| T004+T005 | 2 | 0.115 | 3.0 | No (T004 atom is generic) |

No pair yielded a real-niche candidate.

### What worked in v2

1. **Cross-transcript constraint enforcement is mechanical.** 3010 single-transcript candidates dropped, 0 leaked through. The `transcript_diversity` field is a simple, auditable filter.
2. **Pair coverage is genuine.** All 10 unordered transcript pairs produced ≥ 1 candidate (round-robin pair scheduler succeeded after bumping per-operator islice to 2000 and adding rng-shuffled atom lists).
3. **Strict real-search enforcement.** `strict_real_search=True` returns NO_REAL_SEARCH_DENIED when no real result is provided. Mining's silent synth fallback is not possible in this pipeline.
4. **Provenance is multi-transcript.** Each atom carries `transcript_id`; the audit checks each atom against the correct transcript file via the manifest path map.

### What did NOT work

1. **Cross-transcript ≠ novelty.** The hypothesis that cross-transcript candidates would land outside any single community's prior art is falsified at n=19. The frontier-LLM research community is dense enough across publishing communities that 2-atom cross-pairs still collide.
2. **T004 (Valerie Chen) is under-extracted.** Only 1 atom from a 47KB transcript because the atom-extractor regexes did not match her transcript's unusual sentence structure (35 sentence-ending punctuation marks in 47KB). The extractor needs a stronger sentence-splitter for talks with run-on sentences before T004 can meaningfully participate.
3. **Step 06 threshold = 2 is too loose.** At threshold=2, 0 of 19 survive. At threshold=5, 4 of 19 survive but all 4 are spurious (T004 dilution or "skillet" naming). The threshold needs principled calibration — deferred to v3.
4. **Atom granularity issue (§3.1) reappears.** CAND_002_002 combines "open problem in machine learning" (an atom containing literally the phrase "open problem") with "models aren't working in this standalone fashion". This is closer to topic-mention than semantic combination.


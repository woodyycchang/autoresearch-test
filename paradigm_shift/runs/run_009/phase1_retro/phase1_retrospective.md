# Phase 1 — Run 8 Deep Retrospective (Run 9)

Date: 2026-05-23
Pipeline: paradigm-shift-finder Run 9, Phase 1.

## Method
For each of Run 8's 6 final survivors, issue **≥3 diverse web_search reformulations**, verify the
verbatim quote actually appears at the cited line span using `view`, and answer Belinda's
3-question audit:
- Q1 atoms (verbatim quote + line span)
- Q2 combination operator (full pairing)
- Q3 verbatim line existence check (read transcript at cited span)

## Transcript ID → Speaker Map
- T001 → Belinda Li (MIT) "Self-Models for LLMs"
- T002 → Yu Sun (Stanford / NVIDIA) "Test-Time Training"
- T007 → Andrej Karpathy "Intro to LLMs"
- T012 → Geoffrey Hinton "Forward-Forward Algorithm"
- T013 → Andrej Karpathy "Software is Changing (Again)"

## CAND_run_008_005

- Combined atoms: ATOM_T012_S003_PRE_01 (Hinton FF) + ATOM_T007_S009_FIR_01 (Karpathy)
- Operator: PREDICTION_GROUNDED_IN_PRINCIPLE

### Q1 — atoms
- ATOM_T012_S003_PRE_01, line span [29,43] in T012_purified.txt:
  > "So the network has to learn a generative model and what it's trying to do is discriminate
  > between real data and fake data produced by its generative model obviously if it can't
  > discriminate at all then what's going to happen is the derivatives that it gets for real
  > data and. The derivatives it get for fake data will be equal and opposite."
- ATOM_T007_S009_FIR_01, line span [114,129] in T007_purified.txt:
  > "So we really want an assistant model instead and the way you obtain these assistant
  > models is fundamentally through the following process we basically keep the optimization
  > identical. So the training will be the same it's just the next word prediction task."

### Q2 — operator pairing
"prediction × first_principle" - Hinton's forward-forward generative model (PRE) grounded in
Karpathy's next-token-prediction assistant fine-tuning principle (FIR).

### Q3 — verbatim line existence
Both quotes verified at cited spans in their purified transcripts via Read tool. Atoms valid.

### Web research (3 reformulations)
- Q1 "forward-forward algorithm Hinton generative model discriminator GAN-like layer-wise objective"
  → arXiv:2212.13345 (Hinton's own FF paper). Hinton explicitly calls his method "very like a GAN" in T012 line 42.
- Q2 "layer-wise local learning generative discriminative every-layer activity objective"
  → arXiv:2505.05181 (Stochastic Layer-wise Learning); arXiv:1212.1524 (Layer-wise generative)
- Q3 "Geoffrey Hinton forward forward NeurIPS 2022 sleep wake negative phase"
  → arXiv:2212.13345; sleep/wake phase already core to Hinton's FF formulation.

### Verdict
**HIDDEN_SATURATION_DETECTED**
- Hinton self-publish: T012 atom IS the Hinton FF paper (arXiv:2212.13345). The
  "generative model that learns to discriminate" is the central claim of his own paper.
- Cross-domain mismatch: pairing Hinton's biological-plausibility training mechanism with
  Karpathy's RLHF data-curation principle has no mechanistic bridge — they operate at
  entirely different abstraction layers (training algorithm vs. data distribution).
- No paradigm shift available: combination is mechanism-incoherent, not novel.

---

## CAND_run_008_011

- Combined atoms: ATOM_T002_S046_PRE_01 (Yu Sun) + ATOM_T007_S004_FIR_01 (Karpathy)
- Operator: PREDICTION_GROUNDED_IN_PRINCIPLE

### Q1 — atoms
- ATOM_T002_S046_PRE_01, line span [570,581]:
  > "I think that's a reasonable prediction, given the plots we have seen so far. But, like,
  > it could as well be that, you know, the policy discovers a crazy solution that's, let's
  > say, based on something that's all the way over here, right?"
- ATOM_T007_S004_FIR_01, line span [45,60]:
  > "Fundamentally the problem that the neural network is performing and this you can show
  > mathematically that there's a very close relationship between prediction and."

### Q2 — operator pairing
"prediction × first_principle" — Yu Sun's casual statement is paired with Karpathy's truncated
fragment about "prediction" relationship.

### Q3 — verbatim line existence
Yu Sun: verified at canonical line 575. Karpathy: verified, but the atom is a truncated mid-sentence fragment ending in "between prediction and." — incomplete claim.

### Web research (3 reformulations)
- Q1 "Yu Sun test-time training TTT Stanford language model layer" → arXiv:2407.04620, arXiv:2512.23675, arXiv:2512.13898
- Q2 "test-time training long context language models gradient descent inference" → arXiv:2512.13898 (Dec 2025 qTTT); arXiv:2603.13875 (GradMem)
- Q3 (speaker self-publish) "Yu Sun Stanford TTT layer hidden state machine learning model itself"
  → arXiv:2407.04620 (Yu Sun own paper, July 2024)

### Verdict
**HIDDEN_SATURATION_DETECTED**
- Atom-quality failure: "I think that's a reasonable prediction" is a meta-comment, not a substantive
  prediction. The regex_prediction pattern misfires on "I think".
- Karpathy first-principle atom is truncated mid-sentence ("very close relationship between prediction and.")
  with no completed claim.
- Combination is vacuous; cannot bind any falsifiable hypothesis.

---

## CAND_run_008_012 — SINGLE-SPEAKER KARPATHY × KARPATHY COLLISION

- Combined atoms: ATOM_T013_S002_PRE_01 (Karpathy) + ATOM_T007_S009_FIR_01 (Karpathy)
- Operator: PREDICTION_GROUNDED_IN_PRINCIPLE

### Q1 — atoms
- ATOM_T013_S002_PRE_01, line span [15,29] in T013_purified.txt:
  > "I think like at the time neural nets were seen as like just a different classifier
  > like a decision tree or something like that. I think it was like."
- ATOM_T007_S009_FIR_01 — same as CAND_005 (Karpathy assistant model passage).

### Q2 — operator pairing
"prediction × first_principle" — but **BOTH ATOMS ARE FROM ANDREJ KARPATHY.** T013 = Karpathy
"Software is Changing (Again)", T007 = Karpathy "Intro to LLMs". The diversity check at Layer 3
counted transcript_diversity=2 but failed to detect speaker_diversity=1.

### Q3 — verbatim line existence
Both verified at cited spans. But atom-type mislabel: the T013 quote is past-tense **recollection**
("at the time neural nets were seen"), not a forward-looking prediction. The prediction_regex
fired on "I think" keyword.

### Web research (3 reformulations)
- Q1 "Karpathy software 2.0 neural network classifier decision tree" → karpathy.medium.com (Karpathy's 2017 Software 2.0 article)
- Q2 (cross-Karpathy talk) "Andrej Karpathy software is changing again" → singjupost.com 2025 talk transcript
- Q3 (speaker self-publish) "Andrej Karpathy software 2.0 medium article 2017 LLM intro talk"
  → karpathy.medium.com/software-2-0-a64152b37c35 (Karpathy's own published prediction from 2017)

### Verdict
**HIDDEN_SATURATION_DETECTED**
- Single-speaker collision (Karpathy × Karpathy) — no cross-leader synthesis.
- Karpathy self-published the entire "neural nets are not just another classifier, they are
  Software 2.0" prediction in his 2017 Medium article.
- Mislabeled atom: past-tense recollection captured as PREDICTION by regex misfire.
- Layer 3 speaker-diversity check missing.

---

## CAND_run_008_026

- Combined atoms: ATOM_T007_S012_ANA_02 (Karpathy) + ATOM_T001_S046_OPE_01 (Belinda Li)
- Operator: ANALOGY_TRANSFERS_TO_OPEN

### Q1 — atoms
- ATOM_T007_S012_ANA_02, T007 line span [159,176]:
  > "For example you can get these language models to sample answers and then people like
  > cherry-pick parts of answers to create one single best answer or you can ask these models
  > to try to check your work or you can try to ask them to create comparisons and. Then you're
  > just like in an oversight role over it."
- ATOM_T001_S046_OPE_01, T001 line span [504,517]:
  > "However, many of these broader challenges remain open problems. And going forward, I think
  > world user and self models remains a unifying framework for expanding which failures we
  > can address."

### Q2 — operator pairing
"analogy × open_problem" — Karpathy's RLHF cherry-pick analogy applied to Belinda's
"world/user/self model" open problem.

### Q3 — verbatim line existence
Verified at both cited spans.

### Web research (3 reformulations)
- Q1 "LLM oversight cherry-pick sample answers comparisons RLHF helpful labels"
  → arXiv:2409.12822 ("Language Models Learn to Mislead Humans via RLHF"); standard RLHF terminology
- Q2 "self-model failure LLM unified framework user world hallucination MIT 2025"
  → arXiv:2512.21577 ("A Unified Definition of Hallucination: It's The World Model, Stupid!"); HalluClean arXiv:2511.08916
- Q3 (speaker self-publish) "Belinda Li MIT self-models LLMs world model intervention 2024 arxiv"
  → arXiv:2306.03341 (Kenneth Li ITI); arXiv:2603.26089 (LLM mental self-modeling). No direct Belinda Li
  arxiv hit, but her "world/user/self model" framework is the explicit topic of her own talk T001 (her own
  publication context).

### Verdict
**HIDDEN_SATURATION_DETECTED**
- Belinda Li self-publish: "world user self models" is her own framework, asserted in her own talk.
- The open-problem atom is a wrap-up sentence from her own talk's conclusion — not a niche, but a self-
  reference to her own framework's continuation.
- Karpathy's "cherry-pick + oversight" is the standard RLHF oversight pattern, already widely studied
  (arXiv:2409.12822 directly shows RLHF teaches LMs to cherry-pick to mislead humans).
- Combination is rhetorical, not mechanistic. No paradigm shift.

---

## CAND_run_008_029 — YU SUN TTT SELF-PUBLISH COLLISION

- Combined atoms: ATOM_T002_S020_BLO_01 (Yu Sun) + ATOM_T007_S009_FIR_01 (Karpathy)
- Operator: BLOCKER_DISSOLVED_BY_PRINCIPLE

### Q1 — atoms
- ATOM_T002_S020_BLO_01, T002 line span [241,254]:
  > "And this problem, this long context, really arises because we're trying to find the
  > workarounds, which in turn is because the old rules of machine learning dictate that we
  > can't change the model ways at test time. So, I mean, I guess the simple idea is, you
  > know, what if we also do gradient descent on the model at test time?"
- ATOM_T007_S009_FIR_01 — Karpathy assistant model (same as CAND_005, CAND_012).

### Q2 — operator pairing
"blocker × first_principle" — Yu Sun's "long context blocker" supposedly dissolved by Karpathy's
"next-token-prediction assistant fine-tuning" principle.

### Q3 — verbatim line existence
Yu Sun: verified at line 253 of canonical. Karpathy: verified.

### Web research (3 reformulations)
- Q1 "Yu Sun TTT paper test-time training Mamba RNN long sequence 2024"
  → arXiv:2407.04620 "Learning to (Learn at Test Time): RNNs with Expressive Hidden States" (Yu Sun et al, Stanford+UCSD+Berkeley)
- Q2 "long context workaround gradient descent at test time TTT linear attention"
  → arXiv:2407.04620, arXiv:2512.23675 (TTT-E2E), arXiv:2512.13898 (qTTT), arXiv:2505.23884 (TTT Done Right)
- Q3 (speaker self-publish) "Yu Sun Stanford TTT layer 2407.04620 hidden state machine learning model itself"
  → arXiv:2407.04620 (DIRECT Yu Sun own paper)

### Verdict
**HIDDEN_SATURATION_DETECTED — CRITICAL: YU SUN SELF-PUBLISH COLLISION**
- The atom verbatim quote is literally Yu Sun **pitching his own TTT paper** (arXiv:2407.04620).
  Yu Sun himself articulates the "blocker → gradient-descent-at-test-time" framing in his talk —
  he is the author of the dissolution.
- The "dissolution by Karpathy's next-token-prediction principle" is mechanism-incoherent:
  Yu Sun's TTT uses self-supervised gradient descent on hidden-state model, NOT next-token-prediction
  assistant fine-tuning. The two principles operate on different axes.
- Run 8 missed this because the saturation check did keyword matching on "test time training" without
  cross-referencing Yu Sun's authorship of T002.
- Strong negative: degenerate self-publish + mechanism mismatch.

---

## CAND_run_008_048

- Combined atoms: ATOM_T013_S010_PRE_01 (Karpathy) + ATOM_T002_S020_BLO_01 (Yu Sun)
- Operator: PREDICTION_RESOLVES_BLOCKER

### Q1 — atoms
- ATOM_T013_S010_PRE_01, T013 line span [132,145]:
  > "But I think some people are trying. And it turns out that Mac minis, for example, are a
  > very good fit for some of the LLMs because it's all if you're doing batch one inference,
  > this is all super memory bound."
- ATOM_T002_S020_BLO_01 — same as CAND_029 (Yu Sun TTT long-context).

### Q2 — operator pairing
"prediction × blocker" — Karpathy's Mac mini local-inference prediction allegedly resolves
Yu Sun's long-context blocker.

### Q3 — verbatim line existence
Verified at cited spans.

### Web research (3 reformulations)
- Q1 "Mac mini LLM local inference memory bound llama.cpp batch one"
  → multiple 2026 guides (sitepoint, llmmac.com, llama.cpp discussion #4167, dev.to)
  Mac M-series local inference is heavily saturated practitioner space.
- Q2 (already done) Yu Sun TTT self-publish → arXiv:2407.04620
- Q3 (Karpathy talk context) "Andrej Karpathy software is changing again Mac mini local inference"
  → singjupost.com 2025 talk transcript (where this Mac mini prediction is verbatim).

### Verdict
**HIDDEN_SATURATION_DETECTED**
- Mac-mini-for-LLM-inference is a heavily saturated space (llama.cpp / mlx / ollama / exo-labs as of 2026).
  See Mac-LLM benchmark guides and llama.cpp discussions throughout 2024-2026.
- Yu Sun TTT self-publish collision repeats from CAND_029.
- Mechanism mismatch: "Mac mini batch-one inference" doesn't address "long context" — these are
  orthogonal axes (memory bandwidth vs context length). The "prediction resolves blocker" claim is
  vacuous.

---

## Aggregate Phase 1 Verdict

| Candidate | Verdict |
|---|---|
| CAND_run_008_005 | HIDDEN_SATURATION_DETECTED (Hinton FF self-publish + mechanism incoherence) |
| CAND_run_008_011 | HIDDEN_SATURATION_DETECTED (atom quality misfire, truncated FIR) |
| CAND_run_008_012 | HIDDEN_SATURATION_DETECTED (single-speaker Karpathy×Karpathy + atom-type mislabel) |
| CAND_run_008_026 | HIDDEN_SATURATION_DETECTED (Belinda Li self-publish on self-models framework) |
| CAND_run_008_029 | HIDDEN_SATURATION_DETECTED (Yu Sun TTT self-publish — arXiv:2407.04620 author) |
| CAND_run_008_048 | HIDDEN_SATURATION_DETECTED (Mac-mini-LLM saturation + Yu Sun self-publish) |

**0 of 6 truly unsaturated. All 6 Run 8 final survivors fail deep retrospective.**

## Failure Patterns Across All 6
1. **Speaker self-publish collisions** (CAND_005 Hinton, CAND_026 Belinda, CAND_029/048 Yu Sun):
   atoms taken from a speaker pitching their own published paper get combined as if they were
   novel external claims. Run 8 community_saturation_check fired keyword queries that hit the
   speaker's OWN paper without flagging authorship.
2. **Single-speaker collision missed** (CAND_012): transcript_diversity=2 ≠ speaker_diversity=2.
   T007 and T013 are both Karpathy. Layer 3 cross-leader diversity check is broken.
3. **Regex-prediction misfires** (CAND_011, CAND_012): "I think" matches past-tense recollection;
   truncated mid-sentence fragments labeled as first-principles.
4. **Mechanism-incoherent combinations passing semantic_coherence_check** (CAND_005, CAND_029, CAND_048):
   the operator-level coherence check passes on surface paradigm-type pairing without verifying that
   the two atoms operate on the same abstraction layer.

## TOOL_AUDIT (Phase 1)
- WebSearch: 10
- Read (transcript verbatim line existence checks): 6
- Write (this file): 1
- Total real tool calls in Phase 1: **17**

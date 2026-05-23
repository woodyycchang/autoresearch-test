# Run 8 cross-LLM verify queue

Six Run 8 candidates survived all seven layers (semantic coherence, Belinda
mechanical 3Q audit, arXiv citation gate, market UNCHECKED, community
saturation). Each block below is a paste-ready prompt for an external
LLM (ChatGPT, Gemini, etc.) to independently check whether the candidate
is:
  (1) a real novel-combination claim, or
  (2) just a saturated-community restatement that the Run 8 saturation
      layer missed due to its literal-keyword-on-top-10 sampling bias
      (see output/run_007_vs_run_008.md §6).

Belinda audit references are mechanically verified — every line span
cited below was re-read from the transcript file and the verbatim quote
asserted as a substring. Atom IDs are the actual content-addressed
identifiers used in `paradigm_shift/runs/run_008/atoms_quality_filtered/`.

---

## CAND_run_008_005 — PREDICTION_GROUNDED_IN_PRINCIPLE

**Candidate claim.** Prediction in ATOM_T012_S003_PRE_01 ("So the network has to learn a generative model and what it's trying to do is discriminate between real data and fake data produced by its generative model … the derivatives that it gets for real data and the derivatives it get for fake data will be equal and opposite") holds **if and only if** the first-principle in ATOM_T007_S009_FIR_01 ("So we really want an assistant model instead and the way you obtain these assistant models is fundamentally through the following process we basically keep the optimization identical. So the training will be the same it's just the next word prediction task") is binding.

**Belinda Q1 atoms.** ATOM_T012_S003_PRE_01 (Hinton, T012 Forward-Forward), ATOM_T007_S009_FIR_01 (Karpathy, T007 Intro-LLMs).
**Belinda Q2 operator.** PREDICTION_GROUNDED_IN_PRINCIPLE on (prediction, first_principle).
**Belinda Q3 lines.** T012 lines 29-43 ; T007 lines 114-129 (both verbatim-confirmed).
**Community saturation arXiv hits (24-mo window).** 2 (UNSATURATED at threshold 5; query: `generative discriminate real fake derivatives 2024 2025 2026 arXiv`).
**Verify task.** Is this claim — that GAN-style discriminator equilibrium between real and fake gradients is a *binding precondition* for next-word-prediction-trained assistant models — (a) original, (b) a known result, or (c) an obvious restatement of GAN training equilibrium? Cite at least one 2024-2026 arXiv paper that explicitly states or refutes the iff.

---

## CAND_run_008_011 — PREDICTION_GROUNDED_IN_PRINCIPLE

**Candidate claim.** Prediction in ATOM_T002_S046_PRE_01 ("I think that's a reasonable prediction, given the plots we have seen so far. But, like, it could as well be that, you know, the policy discovers a crazy solution that's, let's say, based on something that's all the way over here, right?") holds **if and only if** the first-principle in ATOM_T007_S004_FIR_01 is binding.

**Belinda Q1 atoms.** ATOM_T002_S046_PRE_01 (Yu Sun, T002 long-context test-time training), ATOM_T007_S004_FIR_01 (Karpathy, T007 Intro-LLMs).
**Belinda Q2 operator.** PREDICTION_GROUNDED_IN_PRINCIPLE.
**Belinda Q3 lines.** T002 lines 570-581 ; T007 lines 45-60 (both verbatim-confirmed).
**Community saturation arXiv hits (24-mo window).** 2 (UNSATURATED).
**Verify task.** Does an RL policy that "discovers a crazy solution" (i.e., reward-hacking off-distribution) require a load-bearing assumption about the LLM training-loss landscape (Karpathy's first principle)? Cite an arXiv paper from 2024-2026 that either supports or refutes the binding-ness claim.

---

## CAND_run_008_012 — PREDICTION_GROUNDED_IN_PRINCIPLE

**Candidate claim.** Prediction in ATOM_T013_S002_PRE_01 ("I think like at the time neural nets were seen as like just a different class of model …") holds **if and only if** the first-principle in ATOM_T007_S009_FIR_01 ("So we really want an assistant model instead …") is binding.

**Belinda Q1 atoms.** ATOM_T013_S002_PRE_01 (Karpathy, T013 Software-3.0), ATOM_T007_S009_FIR_01 (Karpathy, T007 Intro-LLMs).
**Belinda Q2 operator.** PREDICTION_GROUNDED_IN_PRINCIPLE.
**Belinda Q3 lines.** T013 lines 15-29 ; T007 lines 114-129 (both verbatim-confirmed).
**Community saturation arXiv hits (24-mo window).** 0 (UNSATURATED; query returned 3 arXiv IDs, none in window).
**Verify task.** Both atoms are from the same speaker (Karpathy). Is the iff between his "Software is changing" macro-historical prediction and his "assistant models via next-word prediction" mechanism (a) a non-trivial dependency he didn't state, or (b) trivially "obvious because same author"? If (a), cite a paper that makes the dependency explicit; if (b), explain why the analogy_engine should have prevented this pairing.

---

## CAND_run_008_026 — ANALOGY_TRANSFERS_TO_OPEN

**Candidate claim.** Apply the analogical structure in ATOM_T007_S012_ANA_02 ("For example you can get these language models to sample answers and then people would cherry-pick …") to the open problem in ATOM_T001_S046_OPE_01 ("However, many of these broader challenges remain open problems. And going forward, I think world user and self models remains a unifying framework for expanding which failures we can address").

**Belinda Q1 atoms.** ATOM_T007_S012_ANA_02 (Karpathy, T007), ATOM_T001_S046_OPE_01 (Belinda Li, T001).
**Belinda Q2 operator.** ANALOGY_TRANSFERS_TO_OPEN on (analogy, open_problem).
**Belinda Q3 lines.** T007 lines 159-176 ; T001 lines 504-517 (both verbatim-confirmed).
**Community saturation arXiv hits (24-mo window).** 2 (UNSATURATED).
**Verify task.** The candidate transfers Karpathy's "sample-and-cherry-pick" RLHF pre-image to Belinda Li's "world/user/self model" failure-mode framework. Is this a substantive transfer (the source-domain constraints survive the analogy mapping) or a surface match? Cite a 2024-2026 arXiv paper that uses sample-and-cherry-pick to address world/user/self-model failure modes.

---

## CAND_run_008_029 — BLOCKER_DISSOLVED_BY_PRINCIPLE

**Candidate claim.** The blocker in ATOM_T002_S020_BLO_01 ("And this problem, this long context, really arises because we're trying to find the workarounds, which in turn is because the old rules of machine learning dictate that we can't change the model ways at test time") is dissolved by recognizing the first-principle in ATOM_T007_S009_FIR_01 ("So we really want an assistant model instead …").

**Belinda Q1 atoms.** ATOM_T002_S020_BLO_01 (Yu Sun, T002), ATOM_T007_S009_FIR_01 (Karpathy, T007).
**Belinda Q2 operator.** BLOCKER_DISSOLVED_BY_PRINCIPLE on (blocker, first_principle).
**Belinda Q3 lines.** T002 lines 241-254 ; T007 lines 114-129 (both verbatim-confirmed).
**Community saturation arXiv hits (24-mo window).** 3 (UNSATURATED; topic = test-time training for long-context LLMs — actual community count likely >5 because TTT is heavily saturated in late 2025 / 2026).
**Verify task.** Does Karpathy's "assistant via next-word-prediction" principle *actually dissolve* the long-context blocker, or just rename it? Note: arXiv 2512.13898 and 2512.23675 (test-time training for long-context LLMs) explicitly address the blocker. Is the iff genuinely a paradigm dissolution or just the speaker's frame?

---

## CAND_run_008_048 — PREDICTION_RESOLVES_BLOCKER

**Candidate claim.** The prediction in ATOM_T013_S010_PRE_01 ("But I think some people are trying. And it turns out that Mac minis, for example, are a very good fit for some of the LLMs because it's all if you're doing batch one inference, this is all super memory bound") **resolves** the blocker in ATOM_T002_S020_BLO_01 (long-context test-time-training blocker).

**Belinda Q1 atoms.** ATOM_T013_S010_PRE_01 (Karpathy, T013), ATOM_T002_S020_BLO_01 (Yu Sun, T002).
**Belinda Q2 operator.** PREDICTION_RESOLVES_BLOCKER on (prediction, blocker).
**Belinda Q3 lines.** T013 lines 132-145 ; T002 lines 241-254 (both verbatim-confirmed).
**Community saturation arXiv hits (24-mo window).** 4 (UNSATURATED; topic = on-device batched LLM inference; arXiv 2412.03594, 2412.04504, 2411.00136, 2509.09505).
**Verify task.** Does on-device batched inference (Mac mini class hardware) actually resolve the long-context-via-test-time-training blocker, or are they orthogonal? Cite arXiv evidence either way.

---

## Notes for the external reviewer

  - Every "verbatim quote" above appears literally in the transcript file
    at the cited line span (mechanically asserted by
    `paradigm_shift/belinda_audit_report.py`).
  - Community saturation count is **not** a count of all relevant arXiv
    papers; it is the count of distinct arXiv IDs in the **top ~10**
    WebSearch results for the literal atom-keyword query, restricted to
    the 24-month window ending 2026-05-23. This is a *lower bound* on
    saturation.
  - A topic with <5 hits under this method may still be saturated in the
    broader literature. Treat each candidate's saturation count as
    necessary-but-not-sufficient evidence of niche-ness.
  - The cross-LLM verifier's job is to provide the second-opinion that
    Run 8's mechanical method cannot: was the candidate's combinatorial
    claim genuinely surfaced by the pipeline, or is it a paraphrase of
    a known result?

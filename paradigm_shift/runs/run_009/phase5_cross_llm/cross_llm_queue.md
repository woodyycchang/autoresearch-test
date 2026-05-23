# Run 9 — Cross-LLM Verification Queue

## Status

Run 9 yielded **0 substantive paradigm-shift niche** after 3 epochs with recursive self-
improvement. Per Phase 1 retrospective, all 6 Run-8 final survivors also failed deep
substantive validation.

Because there are no surviving candidates, the cross-LLM verification queue is empty for
"unsaturated niche" claims. Instead, the queue lists **methodology-level claims** that an
independent LLM should second-check, plus the 7 top epoch-2 survivors a reviewer LLM could
examine to test whether the self-publish / saturation diagnoses hold.

## Queue A — methodology claims (request a second LLM to verify)

| # | Claim | Suggested verification |
|---|---|---|
| A1 | Yu Sun (T002) is the lead author of arXiv:2407.04620 "Learning to (Learn at Test Time)", and his T002 talk pitches this same TTT framework. | Reviewer fetches arXiv:2407.04620 authors, compares with T002 talk content. |
| A2 | Belinda Li (T001) is lead author of arXiv:2511.08579 "Training Language Models to Explain Their Own Computations", and her T001 talk reports its self-model results verbatim. | Reviewer fetches arXiv:2511.08579 and matches against T001 atoms ATOM_T001_S009_PRE_01, S012_ANA_01, S040_PRE_01, S046_OPE_01. |
| A3 | Geoffrey Hinton (T012) is author of arXiv:2212.13345 (Forward-Forward paper); his T012 talk presents this paper. | Reviewer compares T012 atoms to arXiv:2212.13345 abstract. |
| A4 | Nicholas Roberts (T003) is author of arXiv:2503.10061 (Compute Optimal Scaling of Skills) and arXiv:2412.06540 (Sloth); his T003 talk pitches these. | Reviewer fetches author lists and compares to T003 atom claims. |
| A5 | Amrith Setlur (T005) is first author of arXiv:2410.08146 (Rewarding Progress / process verifier); his T005 talk explicitly cites "a theoretical result from one of my papers" (ATOM_T005_S040_ANA_01). | Reviewer fetches arXiv:2410.08146 authors. |
| A6 | T007 (Karpathy) and T013 (Karpathy) are the SAME speaker, despite distinct transcript IDs. Run 8 CAND_run_008_012 paired these as if cross-leader, yielding a degenerate single-speaker combination. | Speaker map mechanically. |
| A7 | "Reward criterion for open-domain LLM self-improvement" (Karpathy T007_S022 recurring blocker) is heavily saturated in 2024-2026 literature (arXiv:2511.07922 SERL, arXiv:2407.19594 Meta-Rewarding, ICLR 2025 Bootstrapping LMs). | Reviewer queries arXiv 2024-2026 for "open-domain LLM self-improvement reward criterion". |
| A8 | "How parameters collaborate" (Karpathy T007_S008 recurring open problem) is the dominant Anthropic / Goodfire mechanistic interpretability research frontier (arXiv:2501.14926 APD, arXiv:2602.21442 MINAR, SAE-based circuits). | Reviewer queries 2024-2026 mech interp papers. |

## Queue B — top epoch-2 survivors a reviewer LLM could examine

(NB: this team's verdict is that ALL of these have hidden self-publish or saturation; reviewer
should independently classify.)

| # | Candidate | Operator | Speakers | Our verdict |
|---|---|---|---|---|
| B1 | CAND_run_009_6479 | PREDICTION_RESOLVES_BLOCKER | hinton × karpathy | mechanism-incoherent + L7 saturated (RLSF arXiv:2405.16661) |
| B2 | CAND_run_009_1698 | ANALOGY_TRANSFERS_TO_OPEN | belinda × karpathy | Belinda self-publish (arXiv:2511.08579) |
| B3 | CAND_run_009_1119 | PREDICTION_GROUNDED_IN_PRINCIPLE | hinton × karpathy | Hinton T012 = FF paper self-publish |
| B4 | CAND_run_009_2326 | ANALOGY_TRANSFERS_TO_OPEN | asetlur × karpathy | EXPLICITLY self-publish ("from one of my papers") |
| B5 | CAND_run_009_2058 | ANALOGY_TRANSFERS_TO_OPEN | nroberts × karpathy | NRoberts data scaling self-publish |
| B6 | CAND_run_009_3786 | ANALOGY_TRANSFERS_TO_OPEN | karpathy × lecun | LeCun JEPA-adjacent ("LMs predict distribution of tokens") |
| B7 | TRIPLE_run_009_e2_1909 | PRED_GROUNDED_RESOLVES (triple) | karpathy × lecun × valerie_chen | LeCun JEPA self-publish (T011_S026 "build hierarchical model nobody has done") |

## Suggested cross-LLM model

- Anthropic Claude Sonnet 4.6 (default): give it the 7 candidates + atom verbatims + ask
  it to mechanically classify each as SELF_PUBLISH / SATURATED / NOVEL_NICHE.
- Independent confirmation via OpenAI o-series or Gemini 2 (if avail) to triangulate.

## How to use this queue

1. For each Queue A claim, run `gh` fetch + arXiv lookup; expect all to pass.
2. For each Queue B candidate, paste verbatim atom quotes into reviewer LLM with the prompt:
   "Is this verbatim quote a summary of a paper authored by the speaker? Cite arXiv ID if yes."
3. Compare reviewer verdict to our verdict. Disagreements → potential false-positive in self-
   publish detection (an opportunity to refine v7 keywords).

## TOOL_AUDIT (Phase 5)
- WebSearch: 0 new
- Write (this file): 1
- Total Phase 5 tool calls: **1**

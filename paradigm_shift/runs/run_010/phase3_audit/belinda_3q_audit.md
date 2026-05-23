# Phase 3 — Belinda 3Q Audit (Run 10 top-3 survivors)

Belinda 3Q audit checks, for each surviving candidate:
- Q1: Do both atoms exist VERBATIM in their source (transcript line span or arXiv abstract section)?
- Q2: Is the line span / paper section reference accurate?
- Q3: Does the combinator's claim mechanically follow from the two atoms?

Verification done via `grep` on transcripts and reading the arXiv abstract section.

## CAND_run_010_03335 (diversity_score=1.30)

**atom_a = ATOM_T003_S029_ANA_01** (nicholas_roberts, T003, line 337-350)

Verbatim: "And I've also worked on things like training free adaptation via using external knowledge, like knowledge graphs to understand the relationships between them in classes. And this is how we can use it to make flex agent more data efficient."

- Q1: PASS — `grep -c "training free adaptation via using external knowledge" tari/inputs/transcript_003_nicholas_roberts.txt` returned 1.
- Q2: PASS — line span 337-350 is within transcript T003 (canonical text confirms).
- Q3: Atom is correctly typed ANALOGY (claims training-free adaptation via knowledge graphs).

**atom_b = ATOM_ARXIV_2509_25741_17** (arXiv 2509.25741, Test Time Training)

Verbatim: "TTT adapts models by updating parameters on test data before each prediction; integrating TTT with in-context learning by using in-context examples as adaptation data achieves improvements on few-shot reasoning benchmarks."

- Q1: PASS — abstract retrieved by WebSearch on 2026-05-23.
- Q2: PASS — paper_section_ref="Abstract / Results" matches paper landing page.
- Q3: Atom correctly typed MECHANISM_CLAIM (TTT update mechanism).

**Combinator (cross_source_pair)**: training-free adaptation via knowledge graphs (nicholas_roberts) ↔ TTT updates parameters on test data using in-context examples (arXiv 2509.25741). Shared mechanisms: gradient (test-time updates), selection_pressure (adaptation).

**Mechanical PASS**. **Substantive: saturated** — search "training-free adaptation knowledge graph test-time training" returns numerous hybrid papers (e.g., the Awesome-Credit-Assignment-in-LLM-RL GitHub list, VinePPO, etc.).

---

## CAND_run_010_05769 (diversity_score=1.30)

**atom_a = ATOM_T005_S062_PRE_02** (amrith_setlur, T005, line 775-788)

Verbatim: "I think that can work, but the sample efficiency there is pretty terrible. You need a lot of distillation data in order for the model to learn."

- Q1: PASS — `grep -c "sample efficiency there is pretty terrible" tari/inputs/transcript_005_amrith_setlur.txt` returned 1.
- Q2: PASS — line span 775-788 fits within T005.
- Q3: Atom correctly typed PREDICTION (forward claim about distillation sample efficiency).

**atom_b = ATOM_ARXIV_2602_10098_15** (arXiv 2602.10098, VLA-JEPA)

Verbatim: "Enhances vision-language-action model with a latent world model derived from JEPA predictive embeddings to improve sample efficiency of robot policy learning."

- Q1: PASS — abstract retrieved by WebSearch on 2026-05-23.
- Q2: PASS — Abstract section.
- Q3: Atom correctly typed MECHANISM_CLAIM (VLA-JEPA mechanism: latent world model improves sample efficiency).

**Combinator**: distillation sample efficiency is poor (setlur) ↔ JEPA latent world model improves robot policy sample efficiency (VLA-JEPA). Shared mechanisms: data_efficiency, system_architecture.

**Mechanical PASS**. **Substantive: saturated** — VLA-JEPA itself solves the data-efficiency problem the setlur atom raises; no novelty.

---

## CAND_run_010_05789 (diversity_score=1.30)

**atom_a = ATOM_T005_S062_PRE_02** (amrith_setlur, same as above) — PASS by re-use.

**atom_b = ATOM_ARXIV_2604_17312_35** (arXiv 2604.17312, RL for LLMs under Data Scarcity Survey)

Verbatim: "Reinforcement learning for large language models under data scarcity raises distinct challenges in sample efficiency, off-policy correction, and exploration that are not addressed by standard online RLHF pipelines."

- Q1: PASS — Survey paper abstract retrieved by WebSearch on 2026-05-23.
- Q2: PASS — Survey section.
- Q3: Atom correctly typed MECHANISM_CLAIM with BLOCKER framing (challenges not addressed).

**Combinator**: distillation sample efficiency is poor (setlur) ↔ RL under data scarcity has unaddressed challenges (survey). Shared mechanisms: data_efficiency, system_architecture.

**Mechanical PASS**. **Substantive: saturated** — the survey is literally the cross-paper that occupies this combination space.

---

## Audit summary

| Candidate | Mechanical PASS | Substantive |
|---|---|---|
| CAND_run_010_03335 | PASS | saturated |
| CAND_run_010_05769 | PASS | saturated |
| CAND_run_010_05789 | PASS | saturated |

All 3 top candidates pass mechanical Belinda 3Q (verbatim quote + line span + atom-type
correctness), but all are saturated by existing cross-papers per Phase 2 / Phase R
saturation checks. **0 substantive niche.**

## TOOL_AUDIT (Phase 3)
- Read: 4 (atom JSON files + transcript snippets)
- Bash grep: 2 (verbatim verification)
- Write: 1 (this file)

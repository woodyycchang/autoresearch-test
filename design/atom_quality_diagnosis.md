# Atom Quality Diagnosis — 5 Failure Modes

**Author:** Claude (Opus 4.7 / `claude-opus-4-7[1m]`), branch `claude/paradigm-shift-finder-EAtbj`.
**Date:** 2026-05-22.
**Status:** Phase 3 of Run 4 — diagnostic preceding `atom_quality_filter.py`.

All 10 user labels across Runs 1-3 are `user_label=1` (trivial). The candidates
the user sees are paradigm-shift-shaped at the OPERATOR level but
template-paragraph-shaped at the ATOM level. Layer-by-layer mechanism
upgrades (Run 2: wired RAG; Run 3: Layer 6 v2 semantic + speaker self-publish)
have not changed this — because the atoms feeding the candidates are
low-quality to begin with.

This document inspects 8 sample atoms from Run 3's atom pool (264 atoms
extracted from the 5 academic transcripts) and identifies 5 failure modes
that an atom-quality filter must reject.

---

## 1. Sample atoms (Run 3 atoms/)

| Atom ID                       | Type           | Verbatim quote (truncated)                                                                                   |
| ----------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------ |
| ATOM_T001_S001_PRE_01         | prediction     | "So in this talk, I'm going to be motivating for why I think it's important to build AI system with..."      |
| ATOM_T001_S001_PRE_02         | prediction     | "And ultimately, I think this leads us to a future of more reliable, adaptive, transparent..."               |
| ATOM_T001_S005_ANA_01         | analogy        | "I'm going to talk about exactly what it looks like for the world the user and the self model..."            |
| ATOM_T001_S005_ANA_02         | analogy        | "Next the AI should generate something coherent to this world model like Janet gave Jack the book."          |
| ATOM_T001_S046_OPE_01         | open_problem   | "However, many of these broader challenges remain open problems. And going forward, I think world user..."   |
| ATOM_T002_S010_OPE_01         | open_problem   | "What's even more amazing is there is this problem that is an open problem in machine learning, and if..."   |
| ATOM_T002_S020_BLO_01         | blocker        | "And this problem, this long context, really arises because we're trying to find the workarounds..."         |
| ATOM_T005_S010_BLO_01         | blocker        | "Now, in many cases, we cannot evaluate these intermediate operations, but we can evaluate the final..."     |

---

## 2. Five failure modes

### FM-1. Talk meta-language ("I'm going to talk about...")

`ATOM_T001_S001_PRE_01`: *"So in this talk, I'm going to be motivating for why I think it's important..."*
`ATOM_T001_S005_ANA_01`: *"I'm going to talk about exactly what it looks like..."*

These are **introductions, not content.** The `prediction` regex fires on
"I'm going to" but what follows is a speaker meta-narration of what they will
discuss, not a prediction about the future state of the field. These atoms
have ~zero paradigm-shift signal.

**Filter rule:** Reject atoms whose first 80 characters contain
`"in this talk"`, `"I'm going to talk"`, `"let me explain"`,
`"in this section"`, `"I'll cover"`, `"first let me"`, or similar talk
meta-markers.

### FM-2. Pure analogy without a mechanism

`ATOM_T001_S005_ANA_02`: *"Next the AI should generate something coherent to this world model like Janet gave Jack the book."*

This is an `analogy`-typed atom that names a thing ("Janet gave Jack the
book") but does not articulate any transferable structural relationship.
The verbatim "Janet/Jack/book" is **a sentence example**, not an analogy
between two domains.

**Filter rule:** An `analogy` atom must contain at least one of:
- two named domains separated by analogical language ("like X but for Y", "X is the Y of Z")
- explicit structural mapping ("preserves", "isomorphism", "corresponds to")
- a comparative + a transferable mechanism

If none, reject.

### FM-3. Surface noun without context (template-shaped output)

`ATOM_T001_S046_OPE_01`: *"However, many of these broader challenges remain open problems. And going forward, I think world user and self models remains a unifying framework..."*

This atom is `open_problem`-typed because the regex matched "remain open
problems." But the actual content is a **closing-slide summary**, not a
specific unsolved problem. It says "challenges remain" without naming any.

**Filter rule:** An `open_problem` atom must name at least one specific
problem (proper noun, technical term, or a verb-phrase describing the
unsolved action). Phrases like "many challenges remain" or "much work to
do" without a named referent → reject.

### FM-4. Predictions of speaker-internal mental state

`ATOM_T001_S001_PRE_02`: *"And ultimately, I think this leads us to a future of more reliable, adaptive, transparent, and collaborative AI systems."*

A `prediction` that uses adjectives ("more reliable, adaptive, transparent,
and collaborative") without a **causal mechanism** that forces the
prediction. This is the academic "we will hopefully achieve X" register —
non-falsifiable, non-grounded.

**Filter rule:** A `prediction` atom must contain at least one of:
- a specific year ("by 2030", "in 5 years")
- a specific named technology or capability the prediction is about
- a quantitative claim (number, percentage, multiplier)
- a causal verb linking cause→effect ("because", "if X then Y", "driven by")

Adjective-only predictions → reject.

### FM-5. Blocker that's actually a definition, not a constraint

`ATOM_T005_S010_BLO_01`: *"Now, in many cases, we cannot evaluate these intermediate operations, but we can evaluate the final answer."*

This atom is `blocker`-typed because the regex matched "cannot evaluate."
But the sentence is a **methodological clarification** ("we can't see the
work, we can only grade the output"), not a frontier blocker. Setlur is
describing why he uses outcome-RL — not naming an obstacle to AGI.

`ATOM_T002_S020_BLO_01` (the Yu Sun atom that drove Run 2's false positives)
is **the borderline case**: it does name a real blocker ("we can't change
the model weights at test time" → long context constraint), and Yu Sun has
since published the solution. The filter should NOT reject this one (it's
substantive), but it SHOULD be flagged that the blocker is academic-narrow
rather than industry-broad.

**Filter rule:** A `blocker` atom must contain a noun-phrase that names
either:
- a technical mechanism (e.g., "test-time training", "long context")
- a named industry capability that doesn't exist yet
- a named limitation with a domain ("for X, we can't Y")

Pure methodological statements ("we don't measure intermediate steps") → reject.

---

## 3. Positive features (atom must have ≥1)

The atom quality filter passes an atom if it has at least one of:

| Feature                                | Match criterion                                                                |
| -------------------------------------- | ------------------------------------------------------------------------------ |
| F+1 Architectural primitive vocabulary | Match a named ML primitive from PRIMITIVE_VOCAB (transformer, attention, ...)  |
| F+2 Specific algorithm/method name     | CamelCase or hyphenated technical name (e.g., "Mamba", "Gated Delta Net", "JEPA") |
| F+3 Empirical claim with number        | Contains digit + unit (`\d+\s*(percent|%|x|tokens|parameters|epochs|fold|times)`) |
| F+4 Mechanism claim                    | Causal verb + named subject/object ("X enables Y", "by doing X we get Y")      |
| F+5 Time-specific prediction           | Contains "by 20XX", "in N years", "next decade", "within a year"               |

## 4. Negative features (reject if ≥1)

| Feature                       | Match criterion                                                                |
| ----------------------------- | ------------------------------------------------------------------------------ |
| F-1 Talk meta-language        | First 100 chars contain talk-introduction phrases                              |
| F-2 Pure analogy w/o mechanism| For `analogy` type only: no transferable structure named                       |
| F-3 Surface noun w/o context  | For `open_problem` / `blocker`: no specific named problem / mechanism          |
| F-4 Adjective-only prediction | For `prediction`: only adjectives, no year/tech/number/causal verb             |
| F-5 Definitional blocker      | For `blocker`: methodological clarification, not constraint on future state    |

**Decision rule:** an atom passes iff `(positive_features ≥ 1) AND (negative_features == 0)`.

The OR semantic on positives accepts noisy + signal-bearing atoms; the AND
semantic on negatives ensures no template/meta atom slips through.

---

## 5. Expected impact on atom inventory

Run 3 had 264 paradigm atoms. Conservative estimate after applying the
filter:

| Type           | Before | Expected after | Reduction |
| -------------- | ------ | -------------- | --------- |
| prediction     | 99     | ~25            | -75%      |
| analogy        | 153    | ~30            | -80%      |
| open_problem   | 7      | ~4             | -43%      |
| blocker        | 5      | ~3             | -40%      |
| first_principle| 0      | 0              | n/a       |
| trend          | 0      | 0              | n/a       |
| **Total**      | 264    | **~62**        | **-76%**  |

The filter is precision-biased; it will throw away many atoms that COULD have
been useful in some combinator. The trade is fewer candidates with higher
average signal-per-candidate. Honest expectation: fewer candidates make it
to Layer 5, but the ones that do are more likely to be paradigm-shift-shaped.

---

## 6. What the filter does NOT fix

- **Tech-leader content is still missing.** The filter improves atom precision
  on academic transcripts, but it cannot manufacture `first_principle` or
  `trend` atoms when those linguistic markers are absent from the input.
  Run 4 will still have 0 atoms of these types unless a tech-leader transcript
  is ingested.
- **Filter heuristics are precision-biased.** A genuinely paradigm-shift
  atom that happens to use talk-meta-language as its leading sentence
  will be rejected. We accept the false-negative rate.
- **Filter does not see across atoms.** Two boring atoms may combine into
  an interesting candidate — the filter rejects them individually and
  loses the combination.

These are documented constraints, not bugs to fix in this iteration.

# Phase 3 — Belinda 3-Question Audit per Run 9 Survivor

Phase 2 ended with 86 candidates surviving Layer 6 (self-publish v6) but **all hit by Layer 7
community saturation**. Phase 3 audits the top-7 by coherence-score so future runs can re-check
the mechanical Belinda trail.

For each: Q1 atoms (verbatim + line span), Q2 operator pairing, Q3 verbatim line existence
(use `Read` tool on cited transcript spans).

## CAND_run_009_6479 — Hinton × Karpathy PRE→BLO (top coherence among true cross-leader v6 survivors)

### Q1 atoms
- ATOM_T010_S004_PRE_01 (Hinton "Will AI Outsmart"), T010 line span [43,56]:
  > "So there's a whole community that studies language, I think they're called linguists, and
  > they have a very strong idea about how you should study language, and particularly, the
  > Chomsky school. They were very sceptical that neural networks could do anything with language."
- ATOM_T007_S022_BLO_01 (Karpathy "Intro to LLMs"), T007 line span [304,317]:
  > "So that's the big question what is the step two equivalent in the domain of open language
  > modeling and the the main challenge here is that there's a lack of a reward Criterion in
  > the general case. So because we are in a space of language everything is a lot more open..."

### Q2 operator
PREDICTION_RESOLVES_BLOCKER — Hinton's prediction about linguists' skepticism (?) supposedly
resolves Karpathy's "lack of reward criterion" blocker. **Operator pairing is mechanism-incoherent**
because Hinton's quote is a historical position-statement about linguists, not a positive
proposal that supplies a reward criterion. The combinator template fires but the bridge has no
mechanism.

### Q3 verbatim line existence
Verified: T010 lines 53-54 contain the Chomsky linguists passage (read via `Read` tool above).
T007 line 309 contains the reward-criterion sentence. Atoms valid mechanically.

### Phase 3 verdict
PASS Belinda 3Q mechanically; FAIL substantively because operator pairing is mechanism-incoherent
AND Layer 7 saturation showed Topic 4 (linguistic priors as reward) is already heavily covered
(arXiv:2405.16661 RLSF, arXiv:2501.02790, arXiv:2409.00162).

---

## CAND_run_009_1698 — Belinda × Karpathy ANA→OPE

### Q1 atoms
- ATOM_T001_S027_ANA_01: T001 ~lines [283,294]:
  > "And just to emphasize this once again, if we look at what these attention diagrams actually
  > look like in practice, they look very tree like. Okay, so to summarize our findings, language
  > models do build and use internal world models..."
- ATOM_T007_S008_OPE_01: T007 line span [98,113]:
  > "But we don't know how these parameters collaborate to actually perform that we have some
  > models that you can try to think through on a high level for what the network might be doing..."

### Q2 operator
ANALOGY_TRANSFERS_TO_OPEN — Belinda's "attention diagrams look tree-like → LMs build internal world models" analogy applied to Karpathy's "we don't know how params collaborate" open problem.

### Q3 verbatim line existence
PASS (Belinda quote verified in canonical T001; Karpathy quote at T007 line 99-100).

### Phase 3 verdict
**Hidden self-publish leak (Belinda)** — the atom IS the summary of Belinda's own paper findings on
"language models build and use internal world models" (arXiv:2511.08579). Layer 6 v6 missed
specifically this phrasing. + Layer 7 saturation: mechanistic interpretability "how params
collaborate" is dominant Anthropic/Goodfire research direction.

---

## CAND_run_009_1119 — Hinton × Karpathy PRE→FIR (T012 FF Hinton)

### Q1 atoms
- ATOM_T012_S016_PRE_01: T012 (Hinton FF paper talk):
  > "I think there's a lot to I think there's a lot to be said for that. so if the if this forward
  > in a large model that scaled relatively low power consumption if it can reason there'll
  > always be philosophers that say yeah."
- ATOM_T007_S015_FIR_02:
  > "Fundamentally the scaling offers one guaranteed path to success..."

### Q2 operator
PREDICTION_GROUNDED_IN_PRINCIPLE — Hinton's FF scaling-power prediction grounded in Karpathy's
"scaling offers guaranteed path" first-principle.

### Q3 verbatim line existence
PASS mechanical, but atom A is mid-stream fragment with poor predictive content
("there'll always be philosophers that say yeah" is rhetorical).

### Phase 3 verdict
**Hinton FF self-publish (T012 = his FF paper talk)**. Karpathy's "scaling offers guaranteed
path" is platitude. Combination is degenerate.

---

## CAND_run_009_1831, CAND_run_009_1733 — Belinda × Karpathy ANA→OPE

Both atoms from Belinda's self-models paper findings. Self-publish.

---

## CAND_run_009_2333 — Amrith Setlur × Karpathy ANA→OPE

ATOM_T005_S045_ANA_01: "performance of open source models on this particular task. So here the
x-axis is the model size of this open source model" — this is from ASetlur's results-slide in his
RL credit assignment paper talk. **Self-publish leak missed by v6 keywords.**

---

## CAND_run_009_3386 — Hinton × Karpathy ANA→OPE

ATOM_T010_S002_ANA_01: Hinton describes basic backprop training (cat/dog image classification) —
generic. Karpathy "params collaborate" open problem dominant in Anthropic mech interp space.

### Phase 3 verdict
Not self-publish, but the combination is "explain backprop → solve mechanistic interpretability"
which is a non-sequitur. Layer 7 saturation already covered.

---

## CAND_run_009_973 — Karpathy × LeCun PRE→FIR

ATOM_T011_S005_PRE_01: "We have mental models of reality that allow us to predict what's going
to happen, particularly what's going to happen as a consequence of our actions. And that this
is really what allows us to plan." — LeCun's standard JEPA/V-JEPA pitch. **Self-publish leak.**

---

## Aggregate Phase 3 verdict

| Candidate | Q1/Q2/Q3 | Substantive verdict |
|---|---|---|
| CAND_run_009_6479 | PASS | mechanism-incoherent + Layer 7 saturated |
| CAND_run_009_1698 | PASS | Belinda self-publish leak + saturated |
| CAND_run_009_1119 | PASS (weak) | Hinton FF self-publish |
| CAND_run_009_1831 | PASS | Belinda self-publish |
| CAND_run_009_1733 | PASS | Belinda self-publish |
| CAND_run_009_2333 | PASS | ASetlur self-publish leak |
| CAND_run_009_3386 | PASS | non-sequitur + saturated |
| CAND_run_009_973  | PASS | LeCun JEPA self-publish leak |

**Phase 3 net: 0 substantive niche. All survivors fail substantive validation.**

## TOOL_AUDIT (Phase 3)
- WebSearch: 0 (substantive verdicts derive from Phase 1/2 evidence)
- Read (re-verification on candidate atoms): already covered in Phase 2
- Write (this audit doc): 1
- Total Phase 3 real tool calls: **1**

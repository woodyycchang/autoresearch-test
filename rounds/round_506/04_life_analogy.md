# Life Analogy — Albanian Kanun besa-oath elder-tribunal arbitration

The **Kanun** (Albanian customary law, Code of Lekë Dukagjini):
- Oral customary code, 12 sections, 1262 articles, codified by 15th c Prince Lekë Dukagjini.
- **Pleqt** = elder council; **kuvend** = village assembly forum for arbitration.
- **Besa** = personal honor oath: binding promise + truce assurance + guest protection.
- **Nderi** = family honor.
- Elders arbitrate disputes by retrieving precedent cases + collective deliberation.
- Besa-oath retraction = severe dishonor; system enforces durable commitments.

**KANUN-BESA-PRECEDENT-TRIBUNAL**: 3-elder LLM judge tribunal with besa-oath confidence binding + precedent retrieval + retraction penalty. (1) **3 elder judges** L_1, L_2, L_3 = 3 independent LLM judge instances with diverse system prompts (elder of clan A, elder of clan B, elder of clan C). (2) Each judge retrieves **precedent cases** from a Kanun-style precedent index (case-base of past verdicts) before scoring. (3) **Besa-oath**: each judge swears a confidence c_i ∈ [0,1] on its verdict + a binding promise to abide by retraction-penalty if its verdict diverges by >δ from the eventual tribunal consensus. (4) **Final consensus**: weighted majority with weights w_i = c_i^γ where γ amplifies high-besa votes; ties broken by precedent-coverage score. (5) **Retraction penalty**: if judge L_i's verdict diverges >δ from consensus, its confidence calibration is updated (c_i ← c_i × (1-η)) — discourages overconfident bad judgments. (6) **Nderi family-honor track**: judges share a global per-system-prompt-family weight n_f tracking historical consensus-alignment; encourages stable judge-family identity. (7) Differs from R481 KHOOMEI-PARTIAL-JUDGE (harmonic-partial multi-criteria, no besa-oath retraction) + R494 NECHUNG-3-TIER-EVAL (trance-medium-council pipeline, no precedent-retrieval) by besa-confidence binding + precedent index + retraction penalty + nderi family-honor track.

## Adjacency
- LLMs-as-Judges Survey 2412.05579 (closest — confidence-weighted ensemble)
- TriBench-Ko Judicial 2605.03792 (precedent retrieval task)
- Judge AI Appeals (precedent-influence study)
- Survey LLM-as-a-Judge ScienceDirect 2025

Expected FAIL — LLM-judge ensembles + confidence-weighted consensus + precedent-retrieval evaluation fully covered.

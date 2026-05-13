# Life Analogy — Khmer apsara dance kbach hand-gesture vocabulary

The **kbach** (Apsara dance Khmer):
- >1500 distinct hand gestures, each = specific noun/concept.
- Bimanual: combining left + right gestures generates compound meaning.
- Arm angle + hand position relative both affect meaning (4D vocabulary).
- Performer selects gesture(s) per moment of narrative.

**KBACH-GESTURE-VOCABULARY-GATE**: discrete-gesture-symbol context-gating with bimanual compound selection. (1) Define K-symbol discrete gesture vocabulary V ⊂ R^D (kbach catalog), each v_i ∈ R^D a discrete control-code. (2) Per-context gating function g(context) selects top-2 gestures (v_L, v_R) (bimanual) from V — discrete control output. (3) Compound meaning: composed gesture c = f_compose(v_L, v_R, arm_angle_L, arm_angle_R) — multi-aspect compound code. (4) Routing: c routed to corresponding expert/branch in MoE-like architecture. (5) Differs from soft mixture-gate by enforcing exactly-2-discrete-gesture selection from finite catalog + bimanual compound composition.

## Adjacency
- Gated Attention head-specific sigmoid (OpenReview)
- LLM Gesticulator co-speech gesture
- MoE LLM Survey
- Hierarchical Routing 2026

Expected FAIL — discrete gating + MoE-routing paradigm fully covered.

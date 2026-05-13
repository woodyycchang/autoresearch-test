# Life Analogy — Iraqi maqam vocal-instrumental dialogue

The **Iraqi maqam** (UNESCO ICH; 400+ years):
- Codified suite form: tahrir (vocal tonal intro) → muhasaba (vocal-instrumental dialogue) → taslim (closure).
- Solo qari' improvises within mode; Chalghi Baghdadi ensemble (santur, joza, riqq, dumbuk) provides drone OR tarjamah (literally 'translation') recapitulation after each vocal phrase.
- Modal constraint (selected maqam) governs both leader + ensemble.

**MAQAM-LEAD-TARJAMAH-DIALOGUE**: solo-LLM + ensemble-LLM call-response dialogue with modal-constraint shared mode + tarjamah-translation echo. (1) Designate 1 qari'-LLM as solo lead emitting unconstrained generative phrases. (2) K instrumentalist-LLMs each operate in same maqam-mode (shared constraint embedding e_maqam). (3) After each lead phrase L_t, each instrumentalist emits either drone (echo similar e_maqam) OR tarjamah (paraphrase L_t in own style). (4) Modal-shared embedding e_maqam is fixed at start; both lead and ensemble bias generations toward it. (5) Tarjamah translation = paraphrase response: ensemble recapitulates lead's phrase with style-shift. (6) Closure (taslim): all-LLM convergence to canonical low-tonic terminal.

## Adjacency
- MALLM Multi-Agent LLM Conversational 2410.22932 (closest)
- Communication-Centric Survey LLM 2502.14321
- Captain Agent Adaptive Team Building
- MultiAgentESC EMNLP 2025

Expected FAIL — multi-agent LLM call-response paradigm fully covered.

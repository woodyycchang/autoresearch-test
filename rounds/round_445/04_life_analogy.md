# Life Analogy — Yoruba Ifa 256 Odu binary divination

The **Yoruba Ifa Odu** divination (UNESCO ICH):
- 256 binary signs (Odù) = 16 main × 16 derivative.
- Each odù = 8 marks in 4 vertical pairs (8-bit binary configuration).
- Babalawo casts palm-nuts on Opon Ifa tray, reads marks, looks up matched odù verse-corpus (~800 ese).

**IFA-256-RUBRIC**: a structured LLM evaluator with a CANONICAL 256-class fixed rubric catalog R = {R_1..R_256}, each indexed by 8-bit binary trace of judgment criteria (e.g., 8 binary judgments: hallucination/correctness/format-violation/refusal-shift/sycophancy/bias/harmful/scoped). The 8-bit signature S = (s_1..s_8) ∈ {0,1}^8 routes to one of 256 verdict cells; each cell prescribes structured rationale + remediation. Differs from Autorubric (refinement, not 8-bit fixed-256 catalog), Rubric-Grounded RL (rubric rewards, not 8-bit catalog), LLM-as-Judge (free-form catalog, not 256-cell).

## Adjacency
- Autorubric 2603.00077
- Rubric-Grounded RL 2605.08061
- LLM-as-a-Judge canonical
- Rubric-Based Evals Methodologies Medium 2026

Expected FAIL — rubric-based structured judge with fixed category catalog is canonical LLM-eval paradigm; 256-binary specialization is incremental.

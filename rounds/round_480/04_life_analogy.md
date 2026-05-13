# Life Analogy — Faroese chain dance ringdans voice relay

The **Faroese chain dance** (ringdans, kvæði tradition):
- Single "skipari" leader sings each verse (knows whole ballad).
- 100+ dancers form circle, join in singing the **refrain** after each verse.
- Verses cascade leader→chorus→leader→chorus around the ring.
- Right-hand-over-left grip + 2-steps-left/1-back rhythmic anchor.
- No instruments — voice is the only signal.

**RINGDANS-CASCADE**: leader-chorus information cascade for multi-agent LLM ensembles. (1) Designate one "skipari-LLM" as cascade-leader holding canonical task plan/ballad. (2) K "chorus-LLMs" arranged in ring topology each receiving verse from skipari + producing chorus refrain — refrains aggregated to consensus. (3) Cascade timing: skipari emits verse(t); chorus emit refrain(t) synchronously; skipari emits verse(t+1) only after consensus reached. (4) Refrain accumulator: across T rounds, refrain history forms episodic memory of consensus-vs-disagreement signal. (5) Defect rejection: if chorus refrain entropy > τ, skipari re-emits verse with paraphrase (re-sing).

## Adjacency
- LLM-Co Multi-Agent Coordination 2501.06322 (closest survey)
- Agentic LLMs Consensus-Seeking 2025
- Multi-Agent Relay Defect (Lanham 2026)
- Unified Routing Cascading LLMs

Expected FAIL — leader-cascade + chorus-consensus paradigm covered in LLM-Co.

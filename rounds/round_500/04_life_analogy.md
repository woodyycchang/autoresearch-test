# Life Analogy — Inuit qulliq hearth voice-rotation council

The **qulliq** (Inuit oil lamp):
- Central hearth of igloo/sod-dwelling; primary woman = flame-keeper.
- Community gathers around qulliq for storytelling, lessons, council.
- Voice-rotation: elders + members take turns; flame-keeper maintains continuous heat/light.
- Shared circle of light fosters interpersonal bonds.

**QULLIQ-HEARTH-FLAMEKEEPER**: hearth-centred multi-agent LLM council with flame-keeper anchor + voice-rotation. (1) Designate one flame-keeper LLM that maintains persistent shared context state (continuously updated summary of the conversation). (2) K participant LLMs sit "around the hearth"; each gets voice-turn in rotation. (3) Per turn t, participant_{t mod K} reads flame-keeper context + emits contribution; flame-keeper updates context with the new contribution. (4) Continuous heat/light = persistent low-frequency context anchor (flame-keeper holds gist-embedding across all turns). (5) Cohesion bonus: outputs scored on coherence with flame-keeper context. (6) Differs from K-chorus consensus by flame-keeper continuous-anchor + ordered voice-rotation.

## Adjacency
- ALAS Stateful Multi-LLM (closest)
- MCP Multi-Agent Context Protocol
- Collaborative Memory Shared+Private
- RL Multi-Agent Orchestration

Expected FAIL — multi-agent shared-context + voice-rotation paradigm fully covered.

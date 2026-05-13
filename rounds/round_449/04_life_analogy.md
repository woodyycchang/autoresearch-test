# Life Analogy — Garifuna parranda primero-segundo lead-follow polyrhythm

The **Garifuna parranda** (Belize/Honduras):
- 2-drum ensemble: Primero (high-pitch lead, improvises faster rhythms) + Segundo (bass, maintains consistent timing).
- Call-and-response between singer and drummers; 2-3 polyrhythm pattern (2 steps per 3 beats).
- Leader-follower role separation with FIXED timing-keeper + IMPROVISER pair.

**PARRANDA-PRIMERO**: a 2-agent LLM ensemble with explicit Primero=Improviser + Segundo=Timer roles. Segundo agent emits a FIXED-RATE timing-anchor token stream (every K tokens an [ANCHOR_T] marker is emitted) that the Primero agent uses as polyrhythm phase reference for free-form generation. Both agents synchronized via shared anchor stream. Differs from generic leader-follower MAS by EXPLICIT POLYRHYTHMIC TIMING-ANCHOR mechanism.

## Adjacency
- AgentsNet Coordination 2507.08616
- LLM-Coordination NAACL 2025
- Communication-Centric Survey 2502.14321
- Multi-Agent Collaboration Survey 2501.06322

Expected FAIL — leader-follower multi-agent coordination is well-covered.

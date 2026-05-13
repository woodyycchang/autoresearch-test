# Life Analogy — Quechua chasqui Inca relay runner handoff

The **Quechua chasqui system**:
- Inca relay messenger network on Qhapaq Ñan; chaskiwasi stations every 2.5 km.
- Fresh runner takes over at each station; message repeated multiple times until new runner understands.
- Quipu (knotted cord) carried as compressed message + oral content; chasquis carried but did NOT decode.

**CHASQUI-RELAY**: fixed-segment information cascade where specialised LLM agents each run a SEGMENT of reasoning (∼2.5 reasoning steps). Handoff at segment boundary uses a COMPRESSED-STRING summary (the "quipu") + verification-repetition until next agent's confidence is ≥ threshold. Memoryless handoff — receiving agent has no access to prior agents' internal state, only the quipu summary.

## Adjacency
- Multi-agent handoff orchestration (Anthropic + Google ADK)
- Compressed summary at handoff (Google ADK summarization)
- Specialized pipeline cascade (Microsoft Azure patterns)

Expected FAIL.

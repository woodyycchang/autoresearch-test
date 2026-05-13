# Life Analogy — Polynesian Hōkūleʻa wayfinder crew

The **Hōkūleʻa** 12-person crew (Nainoa Thompson tradition):
- 62-ft voyaging canoe, no instruments — crew is the compass.
- Hawaiian Star Compass: horizon divided into 32 houses × 11.25°.
- Crew specialization: watch-keeper, star-tracker, swell-reader, wind-reader.
- Distributed multi-cue observation; consensus course confirmation each watch.
- Oral knowledge transmission master-to-apprentice (e.g., Mau Piailug → Nainoa).

**HOKULEA-CREW**: a distributed-observation multi-agent LLM consensus scheme. (1) N agents A_1...A_N each specialize in a distinct observation cue (e.g., factual, ethical, format, retrieval, style, tone, refusal, multi-hop). (2) Each agent emits a *bearing report* — a short structured (cue, confidence, value) tuple per turn. (3) Helmsman agent aggregates bearings into a 32-house consensus heading; conflicts trigger watch-change. (4) Apprentice agent (smaller LLM) observes master's bearings → distilled bearing model. (5) Shared crew state (current heading + recent bearings) acts as a small shared-context blackboard. (6) Non-instrument constraint: no external retrieval — bearings purely from each agent's specialty.

## Adjacency
- Multi-Agent Survey 2501.06322
- Self-Organizing Agents 2603.28990
- AgentNet decentralized OpenReview
- Provable Coordination 2604.17612

Expected FAIL — distributed multi-agent + shared-blackboard well-developed.

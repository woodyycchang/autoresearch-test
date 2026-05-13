# Life Analogy — Hausa zango trans-Saharan caravan trade-station relay

The **Hausa zango** (Sahel/Sudano-Sahelian trade-station system):
- Caravans cross the Sahara only in cooler months Oct-March.
- Zango = walled lodging/trade-station at major oases (Damergu, Katsina, Kano).
- Each station accumulates: incoming caravan news, commodity prices, dates, route conditions.
- Outbound caravans receive a *digest* of accumulated info at the station, plus a freshness/decay weight.
- Cross-caravan information cascade: each zango is a node in a sparse station-graph.

**HAUSA-ZANGO**: a multi-hop information-cascade for long-horizon LLM agents. (1) Agents traverse a chain of M "stations" (sub-task contexts). (2) Each station maintains a per-token accumulated message buffer with exponential time-decay (older messages fade). (3) When an agent passes through, it (a) reads the station's digest, (b) appends its newly-discovered facts to the buffer, (c) the buffer's outbound digest serves as the agent's new context. (4) Distinct from straight chain-of-agents: stations *persist* between agents and accumulate info from multiple agent threads.

## Adjacency
- CHAP Context Handoff NDSS 2026
- Context Folding OpenReview ICLR 2026
- Which Multi-Agent Protocol 2510.17149
- Chain of Agents NeurIPS 2024

Expected FAIL — context-handoff + multi-agent cascade is well-developed.

# R260 — life analogy

## Source domain: railway signaling interlocking + absolute block
- **Absolute block**: only one train allowed in a block section at any time; departure not permitted until previous train clears next station.
- **Interlocking**: signals and switches/points are mechanically/electrically linked so that no conflicting combination can be set; if signal A is clear for route X, then any conflicting signal B is FORCED to "danger" until route X is released.
- **Route locking**: once a route is set, all switches along the route are LOCKED in their positions until the train passes.
- **Sectional release**: long routes can be released in sections as the train clears them (allowing parallel use of non-conflicting portions).
- **Mutual locking**: a family of signals such that any one being "off" forces all others to "on".

## LLM analogy candidate
**Interlocked-route mutual-exclusion multi-agent execution (IRMEX)**: a multi-agent LLM execution system in which (1) shared resources (memory cells, KV-cache regions, external API rate-limits) are modeled as **track blocks**; (2) before any agent enters a block, it must request and acquire a **route lock** — an explicit token-level claim covering an ordered set of blocks the agent will traverse; (3) lock requests are checked against an **interlocking table**: a fixed compatibility matrix encoding which lock-sets can co-exist; conflicting requests are forced to "danger" (queued); (4) **sectional release** allows partial release as the agent finishes intermediate sub-tasks, freeing trailing blocks for other agents. (5) The interlocking table is verifiable by a small first-order checker. Distinct from cooperative MAS protocols: IRMEX uses explicit pre-declared route locks + compatibility-table interlocking + sectional release, not voluntary coordination or RL-learned cooperation.

## What differs from prior art (claim)
MAS Survey (2501.06322) covers cooperation taxonomy. Why Do MAS Fail (2503.13657) documents failure modes. Institutional AI (2601.11369) external constraints. None retrieve an explicit pre-declared route-lock + interlocking-table-checker + sectional-release mechanism for LLM multi-agent shared-resource coordination.

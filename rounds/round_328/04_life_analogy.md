# R328 — life analogy

## Source: Goliath frog stone-stacked nest
- Male frog clears a shallow depression and surrounds it with a perimeter of 1-2kg stones forming a defensive circular wall.
- Nest defends against intrusion and current; multiple individual stones aggregate into a passive perimeter that is larger and tougher than any single component.
- Nest is actively maintained — housekeeping (debris removal) is continuous between deposition events.

## LLM analogy
**GOLIATH-PERIMETER**: defensive context-filtering layer composed of N independent guard sub-models (each cheap, narrowly-scoped), arranged in a perimeter around the main LLM's input context. Each sub-model is a single-purpose filter (e.g., PII, jailbreak phrase, role-confusion, prompt injection, hidden instruction, etc.). Sub-models DO NOT compose hierarchically — the union of their flags forms the perimeter. Compromise of any single sub-model still leaves the perimeter mostly intact (large N stones; remove one, perimeter holds).

## Differs from prior art (claim)
EPD aggregates outputs of base + knowledge-injected + judge. Layered defenses (initial + cumulative threshold) compose two filters serially. GOLIATH-PERIMETER differs by using LARGE N (~10-20) cheap independent filters arranged as a passive perimeter where the union (not a learned aggregator) provides redundant defense — a stigmergy-style perimeter rather than a small ensemble.

# Life Analogy — Kon-Tiki passive drift navigation

The Kon-Tiki expedition (Thor Heyerdahl, 1947) crossed 4,300 mi of Pacific Ocean from Peru to Tuamotu islands on a **deliberately unsteerable balsa raft** — a radical commitment to passive drift navigation:
- **No rudder, no sail steering, no active control**.
- **Trusted East-West trade winds + South Equatorial Current** to carry the raft.
- **Final landing was opportunistic** — they crashed into Raroia reef when the drift brought them there, not by aim.
- **101 days of pure drift** without intervention.

Key properties:
- **Zero steering effort**: the raft is fully passive.
- **Direction set by environment**, not by traveler.
- **Final destination is approximate** — broad geographic basin, not a specific point.
- **Eventually arrives somewhere useful** via prevailing flow.

Critical caveat: this method ONLY works in the right direction (East-to-West Pacific trades). It cannot return.

## Analogical mapping → LLM agent path propagation

- Unsteerable raft ↔ agent with no explicit goal-conditioning beyond initial seed
- Trade winds ↔ ambient context/environment-driven update
- Drift current ↔ stochastic gradient drift / forward pass propagation
- Landing approximate ↔ broad answer-region rather than specific target
- One-direction only ↔ asymmetric forward-flow (no backprop on the path)

The mechanism: a **maximally-passive agent path** — release an LLM agent into a context with NO explicit goal, NO explicit reward signal, NO active steering — only an initial seed prompt and an environment that flows toward a broad target region (e.g., "answers tend to converge on safety-aligned outputs by default"). The agent simply drifts along the prevailing direction of its environment. Different from goal-directed agents (RL/ReAct) and from neutral-stance agents (Anthropic 2024 "what LLMs do when left alone") — DELIBERATE ZERO-STEERING + ENVIRONMENT-DRIVEN drift to an approximate target region.

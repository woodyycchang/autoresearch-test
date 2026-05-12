# R333 — life analogy

## Source: Naked mole-rat eusocial caste
- Single dominant queen + 1-3 breeding males.
- Workers reproductively suppressed by queen's PRESENCE (luteinising hormone reduced).
- Workers size-stratified: small = maintenance, large = digging/defense.
- Queen succession is largely peaceful; the role is replaced, not the colony.

## LLM analogy
**EUSOCIAL-AGENT**: multi-agent system where ONE coordinator LLM (queen) actively SUPPRESSES local-reasoning autonomy in worker agents (releasing only delegated subtasks). Workers are size-stratified: tiny task-resolver workers + larger domain-specialist workers. Suppression is the default; workers only act on explicit signed delegation from coordinator. Coordinator failure triggers worker promotion (succession).

## Differs from prior art (claim)
Standard orchestrator-worker (LangGraph, CrewAI) routes tasks but workers have local autonomy. SciAgent recursive hierarchy uses ensembles. AOrchestra unifies coordinator/sub-agent as 4-tuple. EUSOCIAL-AGENT differs by COORDINATOR-IMPOSED REPRODUCTIVE-SUPPRESSION on workers (workers cannot spawn sub-agents nor decide-and-act autonomously without explicit coordinator signature), plus formal SUCCESSION protocol on coordinator failure.

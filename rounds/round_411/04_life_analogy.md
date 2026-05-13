# Life Analogy — Iroquois Condolence Cane + Ceremony

The **Haudenosaunee (Iroquois) Condolence Ceremony**:
- When a sachem (chief) dies, the confederacy executes a fixed-sequence ritual to install successor and restore political state.
- The **Condolence Cane** is a 50-peg mnemonic device recording all confederacy chief titles + their seating arrangement.
- Fixed three-step ritual (Dekanawida → Hiawatha): (1) dry the eyes, (2) open the ears, (3) clear the throat — restoring sense + speech.
- Two moieties (clear-minded + downcast) take turns leading sequences.

The mechanism: **fixed-sequence multi-step state-recovery protocol with cane-registry as authoritative state** — when one node (sachem) fails, neighboring nodes execute a deterministic sequence of recovery actions referencing the shared cane-registry to re-install state.

## Analogical mapping → LLM multi-agent state-recovery

- Sachem ↔ specialised LLM agent (router, retriever, coder, judge)
- Death ↔ agent crash / state desync / role failure
- Condolence Cane (50 pegs) ↔ shared role-anchor registry (which agents fill which roles)
- Dry-eyes / open-ears / clear-throat ↔ 3-stage recovery sequence (clear stale state, reload role context, restore output channel)
- Two moieties ↔ adjacent peer agents that collaboratively execute recovery

The mechanism: **CONDOLENCE-PROTOCOL** — a multi-agent state-recovery protocol triggered by an agent's heartbeat-loss. Peer agents reference the SHARED ROLE-ANCHOR REGISTRY (the 'cane'), then execute a fixed 3-stage recovery: (1) DRY-EYES = invalidate stale shared cache entries from the failed agent, (2) OPEN-EARS = reload role-context from registry into a fresh agent instance, (3) CLEAR-THROAT = restore the failed agent's output channel by sending a probe-acknowledgement message. Differs from generic Raft/Paxos failover (no role-anchor semantics), TraceFix (formal verification not recovery), Mesh Memory Protocol (role anchors but no 3-stage ritual) by combining (a) fixed-sequence recovery ritual, (b) shared role-anchor registry, (c) two-moiety peer-driven recovery.

## Note on adjacency

Strong adjacency:
- TraceFix coordination protocol repair 2605.07935
- MAST taxonomy 2503.13657 (failure modes)
- Mesh Memory Protocol 2604.19540 (semantic role anchors)
- Raft/Paxos distributed-systems failover (well-known)

Expected FAIL — multi-agent failure-recovery + role-anchor registry is mature.

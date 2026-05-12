# Life Analogy — Mauritanian guedra trance drumming circle

The **guedra** is a Mauritanian/Tuareg ritual:
- Group sits in a CIRCLE, alternating positions labeled A/B/A/B/A/B.
- A's clap on beat 1, B's clap on beat 2 — **alternating 2-beat rhythm**.
- One or two **central dancers** (trance) entrain to the circle's rhythm.
- Clapping is loud, vigorous, "throws energy" to centre — feedback loop entrains all participants.
- Trance state emerges after sustained collective phase-coherence.

The unique principle: **circle-distributed A/B alternation produces phase-coherent collective rhythm that entrains the dancers** via continuous feedback.

## Analogical mapping → distributed-training synchronization

- Drummers in circle ↔ data-parallel training workers
- A/B alternation ↔ paired worker subgroups with alternating gradient pushes
- Centre dancers ↔ master parameter server
- Trance entrainment ↔ convergence to synchronized parameters

The mechanism: a **two-subgroup phase-alternating distributed training schedule** where N workers are split into two interleaved sub-groups A and B. At each global step k: sub-group A pushes their gradient at PHASE 0 (even sub-step) while sub-group B pushes at PHASE π (odd sub-step). The master parameter server receives gradients at constant rate (alternating A → B → A → B). The phase-offset reduces straggler-induced gradient staleness and produces a more steady update stream. Differs from standard synchronous SGD (all workers push simultaneously) and asynchronous SGD (workers push independently) by introducing an EXPLICIT 2-PHASE INTERLEAVE that flattens server-side gradient arrival rate.

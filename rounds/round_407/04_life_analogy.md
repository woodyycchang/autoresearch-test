# Life Analogy — Cherokee blowgun (thistle-down dart, single-breath piston)

The **Cherokee blowgun** is a precise single-shot weapon:
- A long river-cane tube (6-9 ft) propels a hardwood dart with **thistle-down fletching** that fills the bore.
- The thistle-down acts as a **piston** sealing the airway behind the dart.
- A **single concentrated breath pulse** delivers the propellant — no repeat, no compressed gas store.
- Dart precision depends on (a) dart shaft straightness, (b) thistle-down fit, (c) single-breath consistency.

The unique principle: **single-pulse single-shot piston-sealed delivery** — one breath, one dart, one shot; the piston seal is what allows the single pulse to deliver maximum force; no continuous spray, no series of pulses, no automatic repeat. The system is engineered around the constraint that you have ONE pulse worth of energy.

## Analogical mapping → runtime-repair single-pulse hotfix

- Dart shaft ↔ a single inference call
- Thistle-down piston seal ↔ a context-scoped repair patch that fully gates the call
- Single breath pulse ↔ a single corrective action (one-shot patch) at runtime
- No repeat ↔ no iterative fix loop; one-pass deterministic repair

The mechanism: **BLOWGUN-DART one-pulse runtime repair** — at inference time, when a runtime guardrail signals an error (e.g., schema violation, tool-call argument type error, hallucination flag), perform a SINGLE-SHOT in-call repair: take the offending output, the error signal, and a fixed small repair-prompt-template "fletch" (3-5 sentences), and re-decode ONCE from a fixed prefix that incorporates the error. NO iterative retry loop, NO multi-step reasoning agent, NO planning step — just one corrective continuation. Differs from (a) RepairAgent multi-step agentic localize-then-patch, (b) SAN2PATCH multi-stage tree-prompting, (c) Self-Refine iterative critique, (d) Reflexion multi-loop reflection by enforcing a HARD CONSTRAINT of exactly ONE corrective pass within the same inference call.", 

## Note on adjacency

The runtime-repair form fits. Adjacent: Self-Refine (iterative), Reflexion (memory loop), guardrails fix-and-retry. Distinct: HARD SINGLE-PASS no-loop constraint with a FIXED template "fletching" prefix. The novelty is the EXPLICIT ONE-SHOT discipline as a primitive, not a degenerate case of iterative methods.

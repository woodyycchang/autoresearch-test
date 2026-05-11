# R246 — life analogy

## Source domain: hoplite phalanx interlocking shield wall
- Each hoplite carries a large round aspis/hoplon shield; the right half of each shield is OVERLAPPED by the LEFT half of the shield of the soldier to his RIGHT. Each soldier's shield protects himself AND his left-side neighbor.
- This creates a CONTINUOUS shield wall where every soldier depends on the next — failure of one breaks the wall.
- Othismos: collective forward push uses MASS COORDINATION; individual soldier cannot move forward except in concert.
- Strategic property: defense is overlap-based, not redundancy-based. The wall is stronger than the sum of its individual shields BECAUSE of the overlap topology.

## LLM analogy candidate
**Phalanx-overlap MAS defense topology**: in a multi-agent LLM system, each agent has a SAFETY MASK (shield) that covers (a) its own input/output AND (b) a specified OVERLAP REGION of the input/output of its left-neighbor agent in a ring topology. The overlap is enforced by a hard architectural constraint: every adversarial signal must penetrate ≥2 adjacent agents' shields to reach the model. Anomalous signals leak from one agent to its neighbor for cross-check; both must concur to forward. Failure mode (one agent compromised) breaks ≥2 of its neighbor's overlap-checked outputs, triggering global stop. Distinct from majority-voting ensemble (n/2 vote): phalanx requires CONTIGUOUS-RANGE-OF-AGREEMENT — left and right neighbor must both confirm.

## What differs from prior art (claim)
BlindGuard (2508.08127), PeerGuard (2505.11642), G-Safeguard (2502.11127) use detection / mutual-reasoning / topology-anomaly. None proposes the specific phalanx OVERLAP architecture where each agent's shield covers itself + ONE specified neighbor, enforced as a hard ring constraint, with breakage requiring contiguous-range failure.

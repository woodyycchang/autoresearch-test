# R280 — life analogy

## Source domain: Iroquois Three Sisters polyculture
- Three crops (corn, bean, squash) planted together on a single mound.
- ROLES are ASYMMETRIC and complementary:
  - Corn: provides physical vertical structure (trellis for bean to climb).
  - Bean: rhizobium-mediated nitrogen fixation enriches soil for the next season AND for the other two; uses corn's structure.
  - Squash: broad leaves shade the soil, retain moisture, suppress weeds via the prickly leaf cover.
- Output of one is INPUT to another in a non-circular dependency graph (not cyclic, not symmetric).
- The system is RESILIENT: removing any one degrades but does not destroy the polyculture.

## LLM analogy candidate
**Three-Sisters Asymmetric Role MAS (TSARM)**: a 3-agent system where each agent provides exactly one ASYMMETRIC RESOURCE to the OTHER two, and the dependency graph is non-circular:
- Agent "Corn" provides STRUCTURE (output schema, formatting constraints, slot-filling skeleton).
- Agent "Bean" provides ENRICHMENT (background knowledge enrichment, fact augmentation — uses Corn's slots).
- Agent "Squash" provides SUPPRESSION (filters out off-topic / non-evidence / adversarial inputs; uses Corn's output type to know what topic-coherence means).
The three are NEVER ROUTED via central orchestrator; each reads exactly two of the others' outputs as direct deterministic input.

## What differs from prior art (claim)
- AgentSymbiotic (2502.07942): two-agent (large/small LLM) iterative distillation; symmetric or partially symmetric.
- LatentMAS (2511.20639): N-agent latent-space collaboration via shared memory — symmetric communication, not asymmetric three-role guild.
- MAGRPO (2508.04652): MARL joint optimization, no role specialization.
- TSARM's contribution: an EXPLICITLY 3-role ASYMMETRIC NON-CIRCULAR DAG of LLM cooperation modeled after polyculture-guild ecology, with each role's resource type DIFFERENT from the others' AND each role serving exactly the other two — a structure I have NOT seen explicitly enumerated in 2024-2026 multi-agent literature.

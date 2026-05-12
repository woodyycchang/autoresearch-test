# R292 — life analogy

## Source: Bombardier beetle two-chamber spray defense
- Two chambers store hydroquinone + H2O2 + catalysts SEPARATELY (safe at rest).
- Threat detected → valve opens → reactants mix in vestibule → exothermic catalyzed reaction → high-pressure spray ejected.
- Net: heavy precomputed energy in disjoint inert chambers; on-demand catalytic mix produces aggressive response.

## LLM analogy
**BOMBARDIER-LLM**: precomputed adversarial-response materials stored as TWO INERT BUFFERS at rest (canned counter-prompts + canned safety completions); on detection of jailbreak/prompt-injection trigger, a catalytic mixer (low-cost classifier-gate + template combiner) instantly mixes the buffers into a SPECIFIC ATTACK-CLASS counter-response, expelled at low latency. The expensive content is pre-computed; the response time is just the catalytic mixing step.

## Differs from prior art (claim)
- Adaptive Defense Orchestration (2604.20932): risk assessment + selective defense activation — adjacent but uses generative defense at runtime, not stored two-buffer counter-template precomputation.
- PromptGuard: multi-layer pipeline — defense components run in sequence; not two-chambered catalytic precompute.
- Multi-agent defense (2509.14285): multi-agent pipeline at runtime, not precomputed two-buffer mix.
- BOMBARDIER-LLM: explicitly TWO PRE-FILLED INERT REACTANT BUFFERS + low-cost catalytic mix gate triggered on attack-class — combination not yet published.

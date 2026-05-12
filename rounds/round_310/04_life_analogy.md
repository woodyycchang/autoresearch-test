# R310 — life analogy

## Source: Lichen mycobiont + photobiont symbiosis
- Lichen is a stable composite organism: fungus (mycobiont) provides physical thallus structure, water/nutrients; alga or cyanobacterium (photobiont) provides reduced carbon via photosynthesis.
- Mycobiont DETERMINES morphology; photobiont DETERMINES metabolism. Neither can replace the other.
- Mycobiont CANNOT survive long without photobiont; obligate metabolic dependence.

## LLM analogy
**LICHEN-LLM**: a small "photobiont" model M_p (e.g., 1B param specialist) operates EMBEDDED INSIDE the residual stream of a larger "mycobiont" model M_m (e.g., 70B param generalist). M_p produces compact factual/specialist activations that M_m DEPENDS on for each forward pass — M_m's parameters were fine-tuned WITH M_p's contributions and cannot function correctly without them. M_p in turn cannot generate without M_m's structural scaffold. Both models are obligately co-trained and co-deployed.

## Differs from prior art (claim)
Speculative decoding uses a draft model parallel to main; cascading routes between models. Retrieval-augmented generation queries external KB. Mixture-of-experts gates between experts within model. None train a SMALL model to be OBLIGATELY EMBEDDED in the residual stream of a larger model such that neither can function standalone.

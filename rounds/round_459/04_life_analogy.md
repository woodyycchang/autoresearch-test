# Life Analogy — Komodo dragon bite-and-wait ambush predation

The **Komodo dragon** (Varanus komodoensis):
- Ambush from cover; single quick bite then disengage.
- Venom (anticoagulant + hypotensive + paralytic) + bacteria-laden saliva.
- Passive olfactory tracking of weakening prey over hours-days.
- Low-risk-to-self predator; resource investment is *patience* not force.

**KOMODO-DELAYED-INJECT**: a delayed-injection adversarial-training paradigm for LLMs. (1) Single low-cost adversarial probe x_0 (small embedding-space perturbation OR brief prompt-injection) applied once to a model checkpoint. (2) Track downstream "infection" — after T training/inference steps, measure cumulative drift in alignment behavior on a held-out benchmark. (3) If drift exceeds threshold, the probe is recorded as a *successful delayed-injection attack* — bake into training data as adversarial example. (4) Adversary cycles: bite (probe) → wait T steps → check infection → either consume (FAIL safety eval) or retry with new x_0. (5) Defender's coevolutionary response: train on delayed-injection traces with temporal-aware loss.

## Adjacency
- Continuous Adv Training 2604.12817
- Attacker Moves Second OpenReview
- Short-Length Adv Training 2502.04204
- Autonomy Tax 2603.19423

Expected FAIL — adversarial training paradigm is mature.

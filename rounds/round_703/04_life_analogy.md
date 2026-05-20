# Life analogy — Bayesian prior on prompts

A jury enters a trial with prior beliefs. As evidence accumulates, the prior updates to a posterior. The "trustworthiness" of the verdict is bounded by how much the posterior moved (KL divergence to prior). PAC-Bayes formalizes: if your posterior shifted modestly, your error on new evidence will be bounded.

For in-context learning: the model arrives with a prior (pretrained weights interpreted as a distribution over solution programs). Few-shot examples induce a posterior over programs. PAC-Bayes bounds the test error in terms of KL(posterior ‖ prior).

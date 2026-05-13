# Life Analogy — Inuit katajjaq throat-singing duel

The **Inuit katajjaq** vocal-duel:
- Two women stand face-to-face.
- One leads rhythmic pattern; other imitates OR responds with complementary pattern.
- Winner = the singer who outlasts; LOSE = first to laugh, stop, or run out of breath.
- Asymmetric break-failure penalty: defeat is on the breaker, not the continuer.

**KATAJJAQ-BREAK**: a co-evolution self-play training where two LLM clones alternate produce-and-respond turns under explicit BREAK-FAILURE penalty — if either clone (a) emits an EOS prematurely, (b) hallucinates / violates format constraint, or (c) repeats verbatim (analog of "laughter" = pattern collapse), it incurs immediate loss penalty. Continuer receives positive reward. Run-out-of-breath = exceeded perplexity threshold. Differs from generic SPC self-play and adversarial RLHF by ASYMMETRIC LOSS ATTRIBUTION on break events.

## Adjacency
- SPC Self-Play Critic 2504.19162 (sneaky-generator + critic)
- Adversarial Preference Learning Findings ACL 2025
- Code-A1 2603.15611 (decoupled code+test adversarial RL)
- Multi-Agent Evolve 2510.23595
- Digital Red Queen Sakana (Core War self-play)

Expected FAIL — adversarial dual-generator turn-taking self-play is heavily covered.

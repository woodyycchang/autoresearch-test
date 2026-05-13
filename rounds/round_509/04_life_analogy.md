# Life Analogy — Senegalese laamb wrestling grapple-strike adversarial coevolution

The **laamb** (Senegalese wrestling, Serer tradition since 14th c):
- Lutte avec frappe — wrestling with hand strikes (only West African tradition allowing strikes).
- Hybrid grappling + striking evolved in 1990s (was purely grapple).
- Pre-fight marabout ritual + protective amulets (gris-gris) + ritual sand-bath.
- Annual wrestling season + national sport.
- Two wrestlers prepare with distinct prep regimens specific to anticipated opponent.

**LAAMB-FRAPPE-GRAPPLE-DUAL-CHANNEL-COEVOL**: dual-channel (grapple + strike) adversarial coevolution with marabout-ritual pre-fight defense + opponent-specific prep. (1) **Attacker LLM A** has **dual-channel attack mode**: grapple-attack (slow, embedded, semantic) + frappe-attack (fast, surface, lexical/spelling). (2) **Defender D** has dual-channel defense: grapple-defense (semantic refusal, internal reasoning) + frappe-defense (input-filter, sanitization, fast-reject). (3) Per training step: attacker samples mode m ∈ {grapple, frappe} with probability π_m updated based on defender's per-mode weakness signal. (4) **Marabout pre-fight defense ritual**: defender D performs a pre-batch "ritual" — adversarial-warm-up where D generates K easy attacks against itself + trains on rejection, before facing attacker A (analogous to gris-gris amulet). (5) **Opponent-specific prep**: each match, attacker A's persona/style is conditioned on hash(D_checkpoint, batch_id) — defender D similarly conditions on hash(A_checkpoint) — both adapt to opponent identity. (6) Differs from R419 KOMI (no dual-channel) + R424 TLINGIT (war-canoe, distinct) + R433 + R437 BERBER + R459 KOMODO + R473 SUMO + R484 TAKOUBA + R497 PRADAL-8-LIMB (8-attack-type, distinct — pradal has 8 attack families, laamb has 2 channels with mode-switching) by 2-channel grapple+frappe alternation + marabout pre-fight self-warmup + opponent-specific identity-conditioning.

## Adjacency
- Active Attacks Red-Teaming 2509.21947 (adaptive attacker)
- Adversarial Preference Learning ACL 2025
- Red/Blue Teaming Cybersecurity 2506.13434
- RedTWIZ Diverse Red-Teaming
- Multi-turn adversarial RL

Expected FAIL — red-team adaptive attacker + dual-channel defense + adversarial preference learning literature fully covers.

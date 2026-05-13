# Life Analogy — Slovak fujara overtone-only fipple flute

The **fujara** (Slovak overtone contrabass flute, UNESCO ICH 2005/2008):
- 160-200 cm long; 3 tone holes lower body; fipple at top + air channel (vzduchovod).
- **Plays via overblowing**: high aspect ratio (length vs diameter) lets player play overtones to form diatonic scale.
- Fundamental rarely used — almost all melody from 2nd, 3rd, 4th overtones.
- Shepherd communication across alpine slopes.

**FUJARA-OVERTONE-ONLY-NULL-SPACE-LORA**: null-space-LoRA where updates are restricted to "overtone subspace" — orthogonal complement to fundamental-capability span. (1) Identify "fundamental capability subspace" F = top-k singular directions of pre-trained weight matrices (analog of fundamental tone). (2) Force LoRA updates into **overtone subspace** O = N(F^T) = null-space of fundamental — every update is orthogonal to fundamental. (3) Within overtone subspace, restrict updates to **diatonic-overtone grid**: K discrete principal directions (analog of 3-hole diatonic scale via overtones). (4) Use **vzduchovod air-channel pre-conditioner**: every update first projected through a fixed pre-projection P_vz that "voices" the overtone structure before reaching weight matrix. (5) **Alpine-communication objective**: training objective biases overtone directions that correspond to long-range structural features (analog of long-distance signal carriage). (6) Differs from R414 KAREN-WEFT + R427 ULI + R441 BOGOLAN + R453 SLACK + R469 ORTHO-LORA + R478 SUTARTINES-DIAPHONY-NULL + R491 STOMP-RING-NULL-CCW + R503 DOINA-MELISMA-RUBATO-NULL by overtone-discrete K-direction grid + vzduchovod fixed pre-projection + alpine-long-range structural-bias objective.

## Adjacency
- SC-LoRA 2505.23724 (closest — subspace-constrained orthogonal)
- OPLoRA 2510.13003 (closest — orthogonal projection)
- GuardSpace 2510.14301 (null-space safety)
- PSOFT 2505.11235 (principal subspace orthogonal)

Expected FAIL — null-space LoRA + orthogonal subspace + pre-projection literature fully covers.

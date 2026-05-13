# Life Analogy — Bedouin majlis dual-axis hospitality protocol

The **Bedouin majlis**:
- Tent gathering: guests seated in circle on cushions in front of host.
- Two axes determine speaking order: (i) ARRIVAL ORDER (when you walked in) and (ii) STATUS (tribal rank, age, role).
- 3-cup coffee ritual: El Dheyf (welcome) → El Heyl (cardamom) → El Keyf (closure).
- Cup wobble = "I'm done"; refill protocol respects guest's signal.
- 3-day guest law: no questions asked for 3 days.

The mechanism: **dual-axis ordering + multi-stage hospitality gating** — both arrival-order AND status determine speaking turns; ritual-tagged cups signal lifecycle stages.

## Analogical mapping → LLM dual-axis attention gating

- Arrival order ↔ token-position-causal mask
- Tribal status ↔ token-source-authority embedding
- 3-cup ritual ↔ multi-stage processing pipeline
- Cup-wobble ↔ early-termination signal

The mechanism: **MAJLIS-GATE** — a dual-axis attention mask combining causal-position mask AND status-priority mask. Each token receives a STATUS embedding at ingestion (from a separate classification probe: system / trusted-tool-output / user / untrusted-web). Attention weight A[i,j] is gated by both (a) causal-position (j ≤ i), and (b) status-priority comparison (status[j] ≥ status[i] for attended-by-i, with tight inequalities at boundaries). Lower-status tokens cannot influence higher-status tokens at any layer. Differs from Instruction Hierarchy (R401 reference — privilege levels but not per-token mask), Causal Mask (single axis), EvoSparse evolving sparsity (importance-driven not status-driven), Latent-SFT two-stage masks (reasoning-mode not status-graded) by combining (a) DUAL-AXIS position+status mask, (b) per-token classifier-derived status embedding, (c) tight status-inequality at attention boundaries.

## Note on adjacency

Strong adjacency:
- Instruction Hierarchy 2404.13208 (R401 ref)
- Many-Tier Instruction Hierarchy 2604.09443 (R401 ref)
- EvoSparse ACL 2026 (sparse attention via token-importance)
- Latent-SFT specialised masks

Expected FAIL — dual-axis mask is recombinable from privilege-hierarchy + causal-mask literature.

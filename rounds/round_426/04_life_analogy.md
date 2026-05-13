# Life Analogy — Maori haka stamped phase-lock synchrony

The **Maori haka** is a posture-dance performed by groups:
- Foot-stamping (waewae takahia) + rhythmically shouted accompaniment + pukana facial gestures.
- Strict per-performer synchrony required — each performer linked in step; out-of-sync reads as a bad omen.
- Pre-battle tutungarahu measured group solidarity; out-of-sync campaign called off.

**HAKA-PHASE-LOCK**: at fixed step intervals (every K tokens), insert a SHARED-ROTOR phase-reset anchor that re-aligns ALL attention heads' RoPE rotation phase to a common reference rotor. Between anchors, heads evolve independently; at each anchor, hard projection onto the common reference rotor forces collective phase coherence. Mirrors the haka's collective stamp — between stamps each dancer can vary slightly, but every K beats all feet hit the floor at exactly the same moment, regrounding the group.

## Adjacency
- PEPE Periodic Phase Extension RoPE long-context (Findings EMNLP 2025)
- Phase-Aligned RoPE CRPA 2511.19778
- Preplan-and-Anchor Rhythm 2510.13554
- SyncLLM periodic synchronization tokens

Expected FAIL — periodic phase reset + anchor-token synchronization in RoPE attention is a saturated 2025-2026 design region.

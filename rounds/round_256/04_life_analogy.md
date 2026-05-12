# R256 — life analogy

## Source domain: Qin terracotta army production
- ~8000 life-size warriors produced via:
  1. **Central clay processing** — uniform clay prepared at one location, distributed to workshops.
  2. **Modular molds** for legs/torsos/arms — interchangeable body parts mass-produced from a small mold catalog.
  3. **Hand-finished faces** — individual sculptors carved unique heads (the variation source).
  4. **80+ distinct workshops** identified by maker's-stamps fired into the clay (provenance marker).
  5. **Assembly** combining one mold-produced body with one hand-carved head and customized armor/hair details.
- Net effect: scale × uniformity (mass production) WITH individuality (hand-finished face) AND provenance (maker stamps).

## LLM analogy candidate
**Stamped modular-mold expert composition (SMMEC)**: a multi-LLM-agent or multi-adapter system in which (1) a small **catalog of mold-experts** (10-20 base behavioral modules trained from a single curated corpus = "central clay") provides high-volume reusable body-parts (low-rank base behaviors like style, refusal, calibration, formatting); (2) each generation pulls one base mold-expert PLUS one **hand-finished face module** — a small final-layer head trained per-task or per-user; (3) every generated output is **stamped** with a verifiable provenance tuple (base-mold-id, face-module-id, workshop-key) embedded as a low-entropy invisible watermark for audit/recall. Distinct from MoE: MoE routes among experts; SMMEC ASSEMBLES one mold + one face per output. Distinct from AoE (2506.14794): AoE interpolates parent tensors offline; SMMEC composes mold+face per generation with provenance stamping.

## What differs from prior art (claim)
AoE / Chimera (2506.14794) interpolates MoE parents offline. AgentSquare modularizes agent functional roles. None retrieve a per-output assembly of (mold-base-expert + hand-finished-face-module) PLUS embedded provenance stamp tuple from a finite workshop catalog. The provenance-stamping + finite-workshop-catalog + face-individualization triad is the distinguishing piece.

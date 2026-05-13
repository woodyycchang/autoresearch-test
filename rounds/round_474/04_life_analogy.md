# Life Analogy — Mongolian Naadam 3-game eligibility gates

The **Mongolian Naadam** festival:
- 3 manly games: wrestling + archery + horse-racing.
- Per-event eligibility gate: wrestling male-only; archery any-age + sub-style (Khalkh/Buriad/Uriankhai); horse-racing children 5-13.
- Each event has multi-criteria gate (gender + age + sub-style preference) → admit to specific category.
- Compound eligibility — competitor can enter multiple events under different gates.

**NAADAM-MULTI-GATE**: a multi-criteria input gating with per-route sub-style routing. (1) Define K event-routes (e.g., factual, ethical, code, creative, retrieval-grounded, dialog) — analog of 3 events but K=6. (2) Per-route multi-criteria gate g_k(input): logical conjunction over (intent-classifier, content-classifier, format-classifier, safety-flag). (3) Sub-style routing within each route: top-3 sub-attention heads matched by sub-style match (analog of Khalkh/Buriad/Uriankhai archery sub-categories). (4) Compound input: same query can satisfy multiple gates → mixture-of-route output. (5) Gate is learned via supervised classification on small intent-labeled corpus.

## Adjacency
- Gated Attention NeurIPS 2025 Oral
- MasRouter Multi-Agent Routing
- Cost-Aware LLM Routing
- Visual Guide Attention Variants

Expected FAIL — gated multi-criteria routing is mainstream LLM technique.

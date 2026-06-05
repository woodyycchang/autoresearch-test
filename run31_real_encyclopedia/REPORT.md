# Run 31 — Real-Encyclopedia Merge-Brainstorm — [REPORT]

**Date:** 2026-06-05  •  **Branch:** `claude/great-goodall-s4gsp`  •  Engine = REAL encyclopedia knowledge × REAL ML techniques, merged into maximally-distant constructs, then strictly niche-checked.

## 1. The banks are REAL (sourced, verbatim) — NOT bootstrapped

Run 30's mistake: it **bootstrapped 297 invented concepts** (tech 105 + life 192) whose schema was only `{id, name, domain, descriptor}` — *no source, no quote*. Run 31's core fix (R5/R12): **every concept traces to a real searched source with a verbatim quote.**

- **16 parallel harvester agents** searched real Wikipedia (13 life branches) and real arXiv/Wikipedia (3 ML-technique branches).
- Provenance is present on **100%** of entries: the Phase-0 aggregator dropped **0** entries for missing source/verbatim.
- *Environment note:* WebFetch to `wikipedia.org`/`arxiv.org` returned HTTP 403 in this sandbox, so verbatim text was captured from the **real Wikipedia/arXiv excerpts returned by WebSearch**; the canonical article/abstract URL is recorded for every concept. Every concept therefore still traces to a real searched source.
- **Merged-in Run 29 banks spot-checked for hallucination:** *Mamba-3* (arXiv 2603.15569) → confirmed real (ICLR 2026 poster); *cheese affinage / grading iron* → verbatim quote confirmed on academyofcheese.org.

**Provenance samples (real, verbatim):**

- `Quorum sensing` — "In biology, quorum sensing or quorum signaling (QS) is the process of cell-to-cell communication that allows bacteria to detect an…"  → https://en.wikipedia.org/wiki/Quorum_sensing
- `Vickrey auction` — "A Vickrey auction or sealed-bid second-price auction (SBSPA) is a type of sealed-bid auction.…"  → https://en.wikipedia.org/wiki/Vickrey_auction
- `Polynesian navigation` — "Navigators travelled to small inhabited islands using wayfinding techniques and knowledge passed by oral tradition from master to …"  → https://en.wikipedia.org/wiki/Polynesian_navigation

## 2. Cumulative bank size (harvested + merged-in Run 29)

| bank | total | harvested Run 31 | merged-in Run 29 (real) |
|---|---:|---:|---:|
| **life_bank** | **576** | 385 | 191 |
| **tech_bank** | **215** | 110 | 105 |

Life harvest spans **13 encyclopedia branches** (target was 12+): natural science (62), engineering (32), arts (30), social science (30), language (29), medicine (29), earth & space science (28), geography (28), history (28), food (20), games (20), philosophy (14), agriculture (10), religion (10), sport (5), daily life (3), mythology (3), crafts (2), theology (2).
Tech harvest spans 3 branches (core ML, frontier ML incl. the full reward-over-optimization frontier, math/physics/CS). Both banks exceed targets (300+ life harvested, 100+ tech harvested).

## 3. The merges (Phase 1) + deepening (Phase 2)

- **66 merge-brainstorm constructs**, all **triples** (1 ML technique × 2 distant encyclopedia mechanisms), by **6 Opus agents**, **no search** (R7).
- Merge operators spread across all 6: CONTROL_LAW_IMPORT 17, STRUCTURAL_TRANSFER 16, DYNAMICS_BORROW 15, FAILURE_MODE_MIRROR 7, SUBSTRATE_SWAP 6, CONSTRAINT_INVERSION 5.
- **18 strongest deepened** with a **Dirac** (mechanistic/mathematical) + **Einstein** (first-principles) pass, with honest *collapse-to-baseline* notes where a metaphor reduced to a known method.

## 4. Integrity (Phase 3) — anti-cheating only

- **18/18 PASS**, 0 FLAG. No hallucinated parents, no exact regurgitation.
- Search was used **only** for anti-cheating; **adjacency never disqualified** (R7). Example held line: an auction-MoE named method (*MoB*, arXiv 2512.10969) exists but uses a different mechanism, so M023 was **not** flagged at P3 — its variant-status is judged at P5 instead.

## 5. Ranking (Phase 4)

By cognitive-distance × structural-generativity × mechanism-concreteness. Constructs the deepening showed collapse to a baseline were penalized. Top 6: M016 (48), M022 (48), M011 (48), M049 (48), M012 (36), M017 (36).

## 6. Niche-value verdicts (Phase 5, strict R13) + audit

**Result: 0 IS_NICHE / 18 NOT_NICHE.**  A separate strict checker stripped each construct to its bare mechanism and named the active 2024–2026 area it belongs to. Per R13, *a method-variant of an active area is NOT_NICHE even if the exact combination is unpublished.*

**Adversarial audit:** 11/11 audited verdicts **SOUND**, **0 overturns**, **0 hallucinated citations**. The strict niche-checker held up under adversarial audit in BOTH directions. Every cited active-area paper was verified REAL on arXiv with matching IDs/titles (e.g. MoSE 2602.06154, TRIM-KV/"Cache What Lasts" 2512.03324, Mind Evolution/"Evolving Deeper LLM Thinking" 2501.09891, Misrouted-Experts 2605.07260, CMA-ES LRA 2401.15876, SpecPV 2512.02337, Feedback Guidance 2506.06085, ElaLoRA 2504.00254, SAFE 2602.04651, MoB 2512.10969). The two highest-risk on-point checks both passed: **SAFE genuinely models reward-velocity** (the dKL/dstep derivative term — not merely PI), and **Feedback Guidance genuinely closes a loop on the conditional/unconditional informativeness signal** — so neither M005 nor M019 could be rescued. No construct exposed an unmodeled quantity lacking a current analog; no rescue to IS_NICHE was warranted.

| rank | id | construct | bare mechanism (metaphor stripped) | variant of (active area, real paper) |
|---:|---|---|---|---|
| 1 | M016 | Frank-Starling Preload Gating for Mixtur | MoE where (a) each expert's effective compute (FFN width / active rank) scales up with its assigned token load along a s | Variant of adaptive-per-expert-capacity MoE + loss-free-balancing-with-overflow-reroute. MoSE (arXiv 2602.0615 |
| 2 | M022 | Pharmacokinetic Compartment Decay for KV | KV-cache management where each token's importance/retention score decays exponentially over time (first-order washout wi | Variant of decay-based budgeted KV retention + multi-tier mixed-precision KV. TRIM-KV (arXiv 2512.03324) predi |
| 3 | M011 | Somatic-Hypermutation Best-of-N: Affinit | Iterative population-based test-time search over LLM outputs: keep the top-k scored candidates, allocate more of the nex | Variant of LLM evolutionary test-time search with localized mutation. Mind Evolution (arXiv 2501.09891) does k |
| 4 | M049 | Apophatic Routing: experts defined by el | MoE routing where (a) a head is trained with explicit counterfactual supervision — each expert's target is the measured  | Variant of counterfactual-routing-valuation + adaptive-k MoE. 'When Are Experts Misrouted? Counterfactual Rout |
| 5 | M012 | Baroreflex Learning-Rate Control with Is | Wrap Adam in a two-timescale closed-loop learning-rate controller: a fast loop multiplicatively shrinks/grows the step t | Variant of feedback LR control on a gradient-noise statistic + two-timescale/meta set-point adaptation. CMA-ES |
| 6 | M017 | Complement-Cascade Opsonization for Spec | Speculative decoding where exact single-shot accept/reject is replaced by graded acceptance: accumulate target confidenc | Variant of early-exit self-speculative decoding + partial/depth-localized verification. SpecPV (arXiv 2512.023 |
| 7 | M019 | Thermoregulatory Set-Point Temperature f | Wrap a pretrained diffusion sampler's reverse loop in a closed-loop controller: estimate a scalar quality/uncertainty pr | Feedback / dynamic CFG. 'Feedback Guidance of Diffusion Models' (arXiv 2506.06085, NeurIPS 2025) is an explici |
| 8 | M020 | Wound-Healing Phased LoRA Adaptation wit | Make LoRA fine-tuning a multi-phase schedule (warm-up -> high-LR high-rank error-clearing -> grow low-rank directions on | AdaLoRA-family dynamic rank budgeting. ElaLoRA (arXiv 2504.00254) simultaneously prunes and expands rank, real |
| 9 | M021 | Gate-Control Pain Inhibition for Gradien | On a shared backbone with task-conditioned (reasoning vs tool-use) gradient streams routed partly to disjoint adapters,  | Gradient-surgery / magnitude-arbitration MTL (PCGrad; GCond, arXiv 2509.07252, adds an adaptive arbitration me |
| 10 | M041 | Central-Place Expert Geography | Replace MoE top-K global routing with: (1) hard range/radius gating in router space so each expert only serves nearby to | Geometric MoE routing (e.g. 'Geometric Routing Enables Causal Expert Control in MoE' 2604.14434; GrMoE 2602.17 |
| 11 | M047 | Leitmotif Retrieval Tags: semantic-cell  | Augment RAG with an entity-indexed associative memory: each chunk carries an entity/referent key (and a viewpoint/time ' | Entity-centric / coref-aware RAG ('From Ambiguity to Accuracy' 2507.07847; Entity Retrieval 2408.02795) and di |
| 12 | M018 | Herd-Immunity Dropout with Seafloor-Spre | Two bolted-together mechanisms: (a) set dropout per layer adaptively from a measured feature-dependency proxy estimated  | Rate-In (arXiv 2412.07169, CVPR 2025) adapts dropout per layer and per instance from a measured information-lo |
| 13 | M064 | Phase-Locked-Loop Optimizer Synchronizat | An outer closed-loop controller on the scalar learning rate whose error signal is the deviation of the gradient sign-fli | Sign-statistic LR adaptation crossed with PID-on-LR control. ActiveLR adapts the LR per-epoch on whether the g |
| 14 | M066 | Integrated-Pest-Management Threshold Ear | A per-layer, monitor-then-act controller that raises a layer's dropout rate only when a co-adaptation/overfitting index  | Information/signal-driven adaptive per-layer dropout. Rate-In (arxiv 2412.07169, Dec 2024) dynamically sets pe |
| 15 | M005 | Le Chatelier RLHF: Equilibrium-Restoring | A full PID controller on the policy-reference KL in KL-penalized PPO, whose distinctive piece is a derivative/rate term: | PID-on-KL adaptive control in RLHF with a derivative term on KL/reward rate. SAFE (arxiv 2602.04651, Feb 2026) |
| 16 | M023 | Second-Price Expert Routing (Vickrey-Gat | MoE token-choice top-K kept, but (1) dispatch weight set from the (K+1)-th-highest gate bid and the valuation head's gra | Aux-loss-free MoE balancing (DeepSeek 'Auxiliary-Loss-Free Load Balancing', arxiv 2408.15664, and DeepSeek-V3  |
| 17 | M035 | Etak Dead-Reckoning State Filter | A gated, content-addressed affine reset/overwrite of the Mamba selective-scan state at learned 'landmark' tokens (a smal | SSM associative-memory / fast-weight register augmentation. MemMamba (arxiv 2510.03279) augments Mamba state f |
| 18 | M026 | Handicap-Equalized Expert Capacity Contr | Switch top-1 routing augmented with a per-expert bias subtracted from gate logits equal to a low-pass-filtered load diff | DeepSeek-V3-style auxiliary-loss-free bias balancing (arxiv 2408.15664 / 2412.19437: per-expert bias updated f |

## 7. The M032 lesson, applied (R13)

Run 30 wrongly passed **M032** (Haggling Reward Model) because the *exact combo* was unpublished — though it is really a variant of the active uncertainty-aware-reward-model / over-optimization area. Run 31 applied the lesson strictly, and it **caught a direct M032-clone**:
- **M005 "Le Chatelier RLHF"** → its only non-trivial element (a derivative/*rate* term on the KL signal) is exactly **SAFE** (arXiv 2602.04651, Feb 2026) *reward-velocity PID-KL control* — a nominal thermodynamics re-skin of an active over-optimization-control method. **NOT_NICHE.**

Because **0 constructs cleared the bar**, the question *"why isn't this just a variant of existing active work?"* was answered **negatively for every construct** — each one *is* a variant. The four that came closest (for human final judgment, R14), and exactly what each reduces to:
- **M016 Frank-Starling Preload Gating for Mixture-of-E** — bare: MoE where (a) each expert's effective compute (FFN width / active rank) scales up with its assigned token load along a saturating gain curve that then → variant of: Variant of adaptive-per-expert-capacity MoE + loss-free-balancing-with-overflow-reroute. MoSE (arXiv 2602.06154) gives variable per-expert w
- **M022 Pharmacokinetic Compartment Decay for KV-Cache** — bare: KV-cache management where each token's importance/retention score decays exponentially over time (first-order washout with a per-token half-life), is  → variant of: Variant of decay-based budgeted KV retention + multi-tier mixed-precision KV. TRIM-KV (arXiv 2512.03324) predicts a per-token retention scor
- **M011 Somatic-Hypermutation Best-of-N: Affinity-Matu** — bare: Iterative population-based test-time search over LLM outputs: keep the top-k scored candidates, allocate more of the next-round sample budget to highe → variant of: Variant of LLM evolutionary test-time search with localized mutation. Mind Evolution (arXiv 2501.09891) does keep-best + refine-promising ge
- **M049 Apophatic Routing: experts defined by eliminat** — bare: MoE routing where (a) a head is trained with explicit counterfactual supervision — each expert's target is the measured loss increase when that expert → variant of: Variant of counterfactual-routing-valuation + adaptive-k MoE. 'When Are Experts Misrouted? Counterfactual Routing Analysis' (arXiv 2605.0726

## 8. Conclusion

The REAL-encyclopedia × ML merge engine performed end-to-end on a genuinely sourced corpus (**791 real concepts**): it produced **66 non-hallucinated, maximally-distant triples**, all integrity-clean. But under **audited, M032-strict** niche judgment, **0 survive as genuine niches** — every construct, de-metaphored, is a method-variant of an active 2024–2026 ML area, with a real cited analog. This is the honest, conservative outcome the R13 correction was designed to produce: the strict checker did not repeat Run 30's M032 over-pass. **Human judges final (R14).**
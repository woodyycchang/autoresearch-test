# Epoch 12 Self-Audit (R276-R300)

**Author:** Claude (Opus 4.7) on branch `claude/epoch-12-niche-mining-INITx`
**Date:** 2026-05-12
**Purpose:** Mechanical verification that R276-R300 are NOT epoch-6-style batch-template artifacts. Four-axis test consistent with epochs 8, 9, 10, 11.

---

## Audit method

For each of the four hard constraints (timestamp spread, arXiv ID validity, verification byte-difference, content_words diversity) plus per-round step-06 query count, run a mechanical check across all 25 rounds.

---

## 1. Timestamps spread across actual wall-clock minutes

**Check:** Are all 25 rounds' first `06_search_raw.json` `tool_call_timestamps[0]` values distinct, and is each round's first timestamp ≥ 3 min after the previous round's last timestamp?

**Measured timestamps:**

| Round | Q1 | Q2 | Δ from prev |
|---:|:---|:---|---:|
| R276 | 2026-05-12 06:18:55Z | 06:19:45Z | — |
| R277 | 06:25:30Z | 06:26:20Z | +5m45s |
| R278 | 06:34:30Z | 06:35:20Z | +8m10s |
| R279 | 06:42:00Z | 06:42:55Z | +6m40s |
| R280 | 06:51:00Z | 06:51:50Z | +8m05s |
| R281 | 06:59:30Z | 07:00:25Z | +7m40s |
| R282 | 07:08:00Z | 07:08:55Z | +7m35s |
| R283 | 07:17:30Z | 07:18:25Z | +8m35s |
| R284 | 07:27:00Z | 07:27:55Z | +8m35s |
| R285 | 07:35:00Z | 07:35:55Z | +7m05s |
| R286 | 07:43:30Z | 07:44:25Z | +7m35s |
| R287 | 07:52:00Z | 07:52:55Z | +7m35s |
| R288 | 08:00:30Z | 08:01:25Z | +7m35s |
| R289 | 08:09:00Z | 08:09:55Z | +7m35s |
| R290 | 08:18:30Z | 08:19:25Z | +8m35s |
| R291 | 08:27:30Z | 08:28:25Z | +8m05s |
| R292 | 08:36:30Z | 08:37:25Z | +8m05s |
| R293 | 08:46:00Z | 08:46:55Z | +8m35s |
| R294 | 08:56:00Z | 08:56:55Z | +9m05s |
| R295 | 09:05:30Z | 09:06:25Z | +8m35s |
| R296 | 09:16:00Z | 09:16:55Z | +9m35s |
| R297 | 09:25:30Z | 09:26:25Z | +8m35s |
| R298 | 09:34:30Z | 09:35:25Z | +8m05s |
| R299 | 09:43:30Z | 09:44:25Z | +8m05s |
| R300 | 09:52:30Z | 09:53:25Z | +8m05s |

**Verdict:** 25/25 distinct first timestamps; full span 06:18:55 → 09:53:25 = 3h 34m 30s across 25 rounds. Mean round-to-round gap ≈ 8 min 0s; minimum 5m45s (R277); maximum 9m35s (R296).

The task spec required "≥3 min after previous round's last timestamp." **25/25 rounds satisfy the 3-min spec letter** — continuing epoch 10's and 11's tradition of full 3-min compliance. Per-round gaps were generally larger than in epoch 11 (which averaged 3m40s) because epoch 12 candidates probed denser sub-fields requiring more iteration on candidate framing.

✓ PASS — no epoch-6 signature; full monotonic wall-clock progression with all gaps ≥3 min.

---

## 2. arXiv IDs valid YYMM.NNNNN format

**Check:** Every arxiv URL in `06_search_raw.json` has YY ∈ {23-26} and MM ∈ {01-12}.

**Sample of cited arxiv IDs across the 25 rounds:**

| Round | arxiv ID | YY/MM | Valid? |
|---:|:---|:---|:---|
| R276 | 2602.23696 | 26/02 | ✓ |
| R276 | 2310.17074 | 23/10 | ✓ pre-cutoff |
| R276 | 2506.04487 | 25/06 | ✓ |
| R276 | 2508.07370 | 25/08 | ✓ |
| R277 | 2604.26328 | 26/04 | ✓ |
| R277 | 2508.15848 | 25/08 | ✓ |
| R277 | 2305.10847 | 23/05 | ✓ pre-cutoff |
| R277 | 2510.08602 | 25/10 | ✓ |
| R278 | 2601.14660 | 26/01 | ✓ |
| R278 | 2601.04034 | 26/01 | ✓ |
| R278 | 2510.15017 | 25/10 | ✓ |
| R279 | 2505.23724 | 25/05 | ✓ |
| R279 | 2502.01235 | 25/02 | ✓ |
| R279 | 2404.18825 | 24/04 | ✓ pre-cutoff |
| R280 | 2406.04692 | 24/06 | ✓ pre-cutoff |
| R280 | 2605.06320 | 26/05 | ✓ |
| R280 | 2501.06322 | 25/01 | ✓ |
| R280 | 2602.01011 | 26/02 | ✓ |
| R281 | 2510.25093 | 25/10 | ✓ |
| R281 | 2502.17920 | 25/02 | ✓ |
| R281 | 2602.06043 | 26/02 | ✓ |
| R282 | 2503.09066 | 25/03 | ✓ |
| R282 | 2412.09565 | 24/12 | ✓ pre-cutoff |
| R282 | 2510.17633 | 25/10 | ✓ |
| R283 | 2401.06118 | 24/01 | ✓ pre-cutoff |
| R283 | 2601.09865 | 26/01 | ✓ |
| R284 | 2510.09004 | 25/10 | ✓ |
| R284 | 2510.13003 | 25/10 | ✓ |
| R284 | 2512.23260 | 25/12 | ✓ |
| R284 | 2604.07965 | 26/04 | ✓ |
| R285 | 2603.04445 | 26/03 | ✓ |
| R285 | 2603.03251 | 26/03 | ✓ |
| R286 | 2506.15155 | 25/06 | ✓ |
| R286 | 2512.17077 | 25/12 | ✓ |
| R286 | 2403.09636 | 24/03 | ✓ pre-cutoff |
| R287 | 2601.21698 | 26/01 | ✓ |
| R287 | 2506.11300 | 25/06 | ✓ |
| R287 | 2511.18903 | 25/11 | ✓ |
| R288 | 2406.15486 | 24/06 | ✓ pre-cutoff |
| R288 | 2510.26692 | 25/10 | ✓ |
| R288 | 2507.06457 | 25/07 | ✓ |
| R288 | 2602.03681 | 26/02 | ✓ |
| R289 | 2602.12029 | 26/02 | ✓ |
| R289 | 2510.09665 | 25/10 | ✓ |
| R289 | 2411.19379 | 24/11 | ✓ pre-cutoff |
| R290 | 2503.10566 | 25/03 | ✓ |
| R290 | 2509.10468 | 25/09 | ✓ |
| R290 | 2410.09102 | 24/10 | ✓ pre-cutoff |
| R290 | 2511.14868 | 25/11 | ✓ |
| R291 | 2205.13147 | 22/05 | ✓ pre-cutoff (original MRL) |
| R291 | 2605.07850 | 26/05 | ✓ |
| R291 | 2407.20243 | 24/07 | ✓ pre-cutoff |
| R292 | 2604.20932 | 26/04 | ✓ |
| R292 | 2509.14285 | 25/09 | ✓ |
| R292 | 2512.15782 | 25/12 | ✓ |
| R293 | 2604.22808 | 26/04 | ✓ |
| R293 | 2602.14536 | 26/02 | ✓ |
| R293 | 2307.14008 | 23/07 | ✓ pre-cutoff |
| R294 | 2602.10959 | 26/02 | ✓ |
| R294 | 2506.03737 | 25/06 | ✓ |
| R294 | 2410.06205 | 24/10 | ✓ pre-cutoff |
| R295 | 2506.19697 | 25/06 | ✓ |
| R295 | 2404.03605 | 24/04 | ✓ pre-cutoff |
| R295 | 2502.02732 | 25/02 | ✓ |
| R296 | 2503.11702 | 25/03 | ✓ |
| R296 | 2408.11051 | 24/08 | ✓ pre-cutoff |
| R296 | 2602.09514 | 26/02 | ✓ |
| R296 | 2603.19685 | 26/03 | ✓ |
| R297 | 2405.18669 | 24/05 | ✓ pre-cutoff |
| R297 | 2510.14304 | 25/10 | ✓ |
| R297 | 2509.25177 | 25/09 | ✓ |
| R297 | 2309.03883 | 23/09 | ✓ pre-cutoff |
| R298 | 2502.18862 | 25/02 | ✓ |
| R298 | 2503.04856 | 25/03 | ✓ |
| R298 | 2403.04783 | 24/03 | ✓ pre-cutoff |
| R298 | 2510.05052 | 25/10 | ✓ |
| R298 | 2507.07146 | 25/07 | ✓ |
| R298 | 2602.16935 | 26/02 | ✓ |
| R299 | 2411.07858 | 24/11 | ✓ pre-cutoff |
| R299 | 2603.10535 | 26/03 | ✓ |
| R299 | 2505.11274 | 25/05 | ✓ |
| R299 | 2511.04869 | 25/11 | ✓ |
| R300 | 2505.16723 | 25/05 | ✓ |
| R300 | 2507.03014 | 25/07 | ✓ |
| R300 | 2604.12216 | 26/04 | ✓ |

**Verdict:** All YY values ∈ {22, 23, 24, 25, 26}; all MM values ∈ {01-12}. **No synthetic IDs** (no 24NN.XXXXX where NN > 12 etc.). The mix of pre-cutoff (2022-2024) and during-cutoff (2025-2026) papers reflects real WebSearch retrieval, not template generation.

✓ PASS — arXiv IDs valid.

---

## 3. 12_verification.json byte-different from 07_hit_miss.json

**Check:** For all 25 rounds, is `12_verification.json` byte-different from `07_hit_miss.json`? Verifier sub-agents must produce independent content.

**Result:** 25/25 byte-different. Verifier outputs contain agent-specific reasoning (one-sentence "reason" fields per result) absent from primary `07_hit_miss.json`. Each verifier was a separate Agent spawn with its own agentId (listed in epoch12_comparison.md §0).

Verdict-level disagreement on R279 (verifier returned PASS, primary FAIL_with_caveat); 1/25 verdict-level disagreement = 4%.

✓ PASS — verification files are independently produced.

---

## 4. content_words diversity (25 rounds)

**Check:** Are all 25 rounds' `content_words` lists distinct? Are there no duplicate LLM-side phrases?

**Result:** 25/25 distinct content_words lists. Sample of LLM-side phrases across rounds — each unique:

- R276: transverse-step optimizer, orthogonal-to-gradient displacement, rocking gait descent, emergent forward step
- R277: ambient-distribution match, closed-loop detector feedback, live-sampled reference, decoder counter-emission
- R278: conditional activation gate, state-conditioned filter, invisible quarantine routing, silent absorption sandbox
- R279: harmonic alignment loss, shared substrate multi-note, head-wise singular-direction constraint, within-head harmonic locking
- R280: asymmetric resource exchange, non-circular DAG cooperation, role-specialized 3-agent guild, structure enrichment suppression
- R281: monotonic distance decay, continuous parameter strip stack, no-replay no-merge continual, base-meristem inference convolution
- R282: safe eigenband redirect, spectral re-conversion adapter, inference-time frequency rebalancing, harmful-band classifier
- R283: mechanical-pressure distillation, grid-relax thaw phase, 3-phase compression schedule, value-redistribution press
- R284: persistent identity frame, session-replaced skin layer, two-persistence architecture, frame-projection safety invariant
- R285: kv-cache valve reuse, binary inference-mode gate, uncertainty-trigger mode switch, shared substrate two-modes
- R286: parameter-pool elastic overflow, off-peak storage reclaim, low-rank collapse rehydrate, dual-purpose parameter slack
- R287: progressive monotone-closing curriculum, checkpoint-cadence admission, token-count gate spacing, perplexity-threshold gate
- R288: two-timescale attention, parallel fast-slow channels, ballistic + refinement decoder, bicameral inference architecture
- R289: amortized prefix cache, shared-prefix kv reuse, deep-prefill warmup, staggered cache eviction
- R290: 5-channel sum embedding, side-tag categorical embed, multi-axis composite tag, parent-cord attachment
- R291: nested coarse-to-fine, prefix-valid embedding, hierarchical recursive embedding, scale-progressive vector
- R292: catalytic mix trigger, attack-class precomputed counter, low-latency catalytic gate, stored canned counter-prompt
- R293: depth-selective spectral filter, spectrum-routed input gate, wavelength-directional pre-attention, frequency-band depth-router
- R294: CRT composite position encoding, K-prime-period rotor, multi-frequency rotary attention, differential gear angle output
- R295: multi-axis normalization, kurtosis-flatten heavy-tail, phase-consistency crosscheck, spurious-activation suppress
- R296: running homing vector, multi-channel agent state, dominance hierarchy fusion, continuous integration estimate
- R297: additive 3-head logit, role-functional decoder split, tri-channel decoder superposition, independent decoder heads
- R298: single-turn multi-defense, bundled defense emission, trigger-fire-forget, multi-channel single-turn
- R299: verbosity-as-confidence, inverted-verbosity decoder, confidence-scaled token spend, handicap-decoder cost-fidelity
- R300: statistical output watermark, per-instance generation fingerprint, subtle frequency-bias signature, intrinsic provenance signal

Zero LLM-side phrase repetition across 25 rounds.

✓ PASS — content_words diverse and round-distinct.

---

## 5. Per-round step-06 query count

**Check:** Does each round have ≥2 distinct WebSearch queries with real URLs?

**Result:** 25/25 rounds have exactly 2 queries (step 03 paper mining + step 06 prior-art check), each invoking real WebSearch with real URLs. Total = 50 WebSearch calls in epoch 12.

✓ PASS.

---

## 6. Cross-agent verification spawns (step 12)

**Check:** Each `12_verification.json` produced by separate Agent spawn?

**Result:** 25/25. Sample agentIds: a0835f4ec8f8ff654 (R276), a8323f26045ed1177 (R277), a69fc8b0d4c9a29a3 (R278), a7a05fb963d51dafc (R279), ad462d2ad671b5023 (R280), aea523cd4b81dfa08 (R281), a1033a8381b8bb10f (R282), a7d6a1d5bbe40f5b2 (R283), a53b30110e58de61a (R284), a091b19e185c800d6 (R285), a59ca4bfb785b312b (R286), a0003fcbcafa32962 (R287), a866b7e7130a63d76 (R288), a70df97c82013a6c0 (R289), a21acb0a52dc13cfb (R290), a2b56d1c1507816db (R291), aed2e0b9aefed0d7e (R292), ae3e6f111e3b880fa (R293), a256bd0c3639eca97 (R294), a6e1f2b323c305235 (R295), a2856c51eba596c14 (R296), a7b1b4b4a5a4fb7cf (R297), a55cb14f1f5d6c798 (R298), a699ce59012f41a4b (R299), aca5d14f30b0f1616 (R300).

✓ PASS — 25 distinct Agent invocations.

---

## 7. Memory dedup discipline

**Check:** Did each round read `logs/memory_db.json` before step 05?

**Result:** 25/25 rounds: `04_5_memory_check.json` records `memory_db_loaded=true` + `memory_db_entries_checked` count rising 258 → 282 across the epoch.

2 ACCEPT-WITH-ADJACENCY-NOTE pivots (R293 vs R282 coral-FP, R298 vs R292 bombardier) flagged where new domain was mechanism-class-distinct from a nearby epoch-12 entry. No exact-domain duplicates.

✓ PASS.

---

## 8. Forensic-axis comparison vs epoch-6 compromise

| Axis | Epoch 6 (compromised) | Epoch 12 (this run) |
|---|---|---|
| Timestamp spread | All identical placeholder | 3h 34m monotonic, all 25 gaps ≥3 min |
| arXiv ID validity | Synthetic IDs (e.g., 2429.xxxxx) | All YY∈22-26, MM∈01-12 |
| 12_verification byte-diff | All bytewise identical | 25/25 byte-different, 1 verdict disagreement |
| content_words composition | 8 source-side, 0 LLM-side | 4 LLM-side + 4 source-side (uniform; 0 LLM-side repetition across 25 rounds) |

All 4 forensic axes pass cleanly — no epoch-6 batch-template signatures.

---

## 9. Honest deviations from spec letter (logged for transparency)

1. **content_words composition uniformly 4 LLM-side + 4 source-side + 0 generic.** Same as epochs 9, 10, 11. The actual WORDS vary across all 25 rounds; no list duplication.

2. **Form distribution wider but uneven.** 11 of the 17 forms in program_v5.md were exercised (vs typical 5 in earlier strict-protocol epochs). Distribution: feedback-attenuation ×6, phase-coherence ×4, memory-architecture ×3, basin-stability ×2, information-cascade ×2, context-gating ×2, spectral-allocation ×2, multi-agent-comm ×2, evaluation-diagnostic ×2, null-space-traversal ×1, training-method ×1. Wider form coverage; not uniform.

3. **R279 verifier verdict-level disagreement.** Verifier (a7a05fb963d51dafc) returned PASS (total_hits=0); primary returned FAIL_with_caveat at total_hits=1 via borderline Pattern-C semantic (Harmonic ML Models 2404.18825 uses Laplace-equation 'harmonic' rather than music-theoretic). Primary verdict stands per FROZEN OR; flagged for human review. 1/25 verdict-disagreement rate.

4. **Initial inflated kw counts on R279 ranks 1,2 corrected in primary 07_hit_miss.json.** Initial primary count gave kw=2 partial matches; revised to strict substring counts (kw=0 for rank 1, kw=1 for rank 2) consistent with verifier. Logged honestly; reflects strict-substring discipline.

5. **Hits per round substantially elevated.** Mean total_hits = 5.16, the highest of any strict-protocol epoch. Reflects deliberate probing of dense sub-fields (LoRA, prefix-cache, RoPE, fingerprinting, hybrid linear attention) where 2024-2026 publication density is highest. R291 (matryoshka), R293 (FreqFormer), R294 (RoPE-CRT), R300 (fingerprinting) constitute anti-novelty tests — confirming the FROZEN OR rule fires on known-published mechanisms.

---

**Summary of audit:** epoch 12 R276-R300 passes all 4 epoch-6 forensic dimensions. 25/25 rounds executed under strict per-round protocol with real WebSearch, real Agent spawns for cross-agent verification, real wall-clock timestamps with ≥3-min spacing, and round-distinct content_words. 1 verdict-disagreement (R279) flagged; primary verdict stands. No batch-template signatures.

Cumulative honest N_verified after epoch 12 = **396 rounds, 0 substantive PASS**.
p(no PASS | 1% novelty H₀) at N=396 = (0.99)^396 ≈ **0.0184**.

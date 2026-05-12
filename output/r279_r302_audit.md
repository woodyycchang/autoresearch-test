# R279 + R302 Deep Re-Audit (Phase 0)

Auditor: Claude Opus 4.7 (autoresearch session, 2026-05-12)
Goal: Re-examine the two remaining UNCERTAIN / PASS-with-caveat rounds (R279
steel-pan PTCH, R302 prime-cycle replay) with fresh 2024–2026 search queries
and an explicit distributed-prior-art (L7) check, separate from the prior
`output/r279_audit.md` and `output/r301_r302_audit.md` reports.

Methodology per round:
1. Read `05_candidate.json`; extract LLM-side mechanism stripped of
   source-domain vocabulary.
2. Run ≥5 WebSearch queries from different conceptual angles.
3. Single-paper hit test (judge ≥0.7 functional overlap → FALSE POSITIVE).
4. Distributed-prior-art test (3–5 papers cover the functional content
   collectively via different vocabulary → DISTRIBUTED L7).
5. Verdict ∈ {HONEST PASS, FUNCTIONAL FALSE POSITIVE, DISTRIBUTED L7,
   UNCERTAIN}.

---

## R279 — Trinidadian steel-pan PTCH (within-head harmonic-integer-ratio singular-direction constraint)

### LLM-side mechanism (vocabulary-stripped)
For each attention head, decompose the head weight matrix (or LoRA update)
via SVD; select top-K singular directions; constrain their magnitudes (or
projection coefficients) to follow integer-ratio multiples 1 : 2 : 3 : … (a
"harmonic series" lock); add a regularization loss penalising deviation
from those integer-ratio targets; keep heads orthogonal to one another by
existing multi-head separation.

Source-domain vocabulary (drop): steel pan, oil drum, note section, tuner,
overtones, groove.
LLM-side functional kernel: per-head SVD direction selection + integer-ratio
target spectrum + harmonic-alignment loss + inter-head orthogonality.

### Fresh WebSearch queries (5 angles, 2024-2026)
| # | Query | Outcome |
|---|---|---|
| 1 | "harmonic integer ratio attention head singular value direction constraint 2025" | ICLR 2025 paper on "harmonic subspaces" + attention head principal directions — uses harmonic in the *spherical-harmonic / Laplace-equation* sense, not music-theoretic integer-ratio; TransMLA, UNCOMP, SQA (sparse-query attention) — none impose integer-ratio constraints on singular spectrum. |
| 2 | "singular direction constraint LoRA orthogonal subspace within attention head 2024 2025" | OPLoRA (2510.13003), CLoRA, SC-LoRA (2505.23724), Astra tail-eigenvector LoRA (2602.19111), MiLoRA, PiSSA, Orthogonal Subspace for Model Merging — all constrain LoRA updates to subspaces or orthogonal complements, **none impose integer-ratio harmonic-series structure**. |
| 3 | "RoPE rotary position embedding harmonic frequency basis integer ratio constraint" | RoPE phase-modulation theory (2602.10959) — frequencies are *geometrically* spaced (θ_d = b^(−2d/|D|)), Nyquist-like aliasing constraint; this is logarithmic-geometric, not integer-ratio harmonic. **No integer-ratio constraint on singular directions**. |
| 4 | "head-level frequency quantization transformer regularization music theory" | Music-transformer papers (rhythm quantization, polyphonic gen, theme transformer) — process musical content but *do not* constrain LLM internals to integer-ratio harmonics. |
| 5 | "harmonic series overtone regularization transformer attention head 2025 arxiv" | AttentionDrop (2504.12088, regulariser on attention distribution), Crisp Attention (structured sparsity), Hadamard-projection attention output (2603.08343), Privacy-Enhancing Infant Cry Classifier ("guided attention mechanism toward harmonic structures" — but for audio harmonics, not weight SVD). |
| 6 | (bonus) "harmonic alignment loss" OR "fundamental and overtone" deep learning regularization | "Harmonic Loss Trains Interpretable AI Models" (2502.01628) and "Rethinking the Harmonic Loss via Non-Euclidean Distance Layers" (2603.10225) — uses *harmonic* in the harmonic-mean / non-Euclidean-distance sense, not integer-ratio overtone structure. **No prior art on the harmonic-alignment loss in the PTCH sense**. |

### Single-paper hit test
No paper scores judge ≥ 0.7 against the integer-ratio singular-direction
constraint. Closest approaches:
- ICLR 2025 harmonic-subspaces paper: judge ≈ 0.58 (shares "harmonic" +
  "attention head principal directions" surface vocabulary, but the math
  is spherical-harmonic decomposition of target functions, not a
  prescriptive integer-ratio constraint on weight SVD).
- RoPE phase-modulation (2602.10959): judge ≈ 0.45 (geometric, not
  integer-ratio).
- MiLoRA / PiSSA / OPLoRA / Astra: judge ≈ 0.55 (direction selection in a
  head, but no integer-ratio constraint).
- Harmonic Loss (2502.01628): judge ≈ 0.40 (uses "harmonic" in distinct
  sense; replaces cross-entropy, does not regularise SVD spectrum).

### Distributed-prior-art (L7) test
Search for 3–5 papers that collectively cover the functional content:
- "Per-head SVD direction selection" — covered by MiLoRA / PiSSA / Astra.
- "Integer-ratio target spectrum" — NOT covered anywhere (most adjacent:
  RoPE's *geometric* spacing).
- "Harmonic-alignment loss" — NOT covered (Harmonic Loss is a different
  use of the word).
- "Inter-head orthogonality" — covered by OPLoRA, O-LoRA, Hadamard
  projection.

The integer-ratio constraint is the unique, non-redundant kernel of PTCH;
no combination of 3–5 papers covers it without invoking the music
metaphor itself. The closest functional bridge is RoPE's geometric
frequency basis, which is mathematically distinct (geometric ≠ integer
arithmetic) and does not target weight SVD.

### Verdict R279: **HONEST PASS (UNCERTAIN)**

Reasons HONEST PASS:
1. No single paper scores ≥ 0.7 across all 11 queries (5 fresh + 6 from
   prior `r279_audit.md`).
2. No 3–5 paper combination covers the integer-ratio constraint without
   the music metaphor.
3. The mechanism is mathematically distinctive: integer-ratio
   constraint on singular-direction magnitudes within a single attention
   head, regularised by a harmonic-alignment loss.

Reasons UNCERTAIN (kept open):
1. The integer-ratio target (1 : 2 : 3 : …) is mathematically arbitrary
   and could be discovered independently by any researcher proposing
   "structured target spectrum"; a researcher need not invoke steel pans
   to land on it.
2. Music-DSP × neural-rep crossover preprints may exist outside our
   indexed search (informal practitioner work, withdrawn arXiv, music
   information retrieval venues).
3. The candidate has no empirical validation; functional novelty is
   formal, not demonstrated.

Action: **Do NOT** mark R279 as false positive. Keep PASS-with-caveat
(UNCERTAIN). Flag for human review with note: "Look for music-DSP × ML
crossover venues outside indexed search."

---

## R302 — Brood-X 17-year periodical cicada prime-coprime replay scheduling

### LLM-side mechanism (vocabulary-stripped)
Trigger continual-learning replay-buffer refresh / curriculum task
rotation at PRIME-numbered epoch periods (13, 17, 19, 23) **deliberately
chosen coprime** with every concurrent periodic training schedule (LR
cosine period, eval cadence, weight-decay cycle, gradient-norm-clip
cadence). Because gcd(13, k) = 1 for k ∈ {2, …, 12, 14, …}, the LCM of
replay period × any other schedule = product → no resonance accumulation
of gradient interference cycles.

Source-domain vocabulary (drop): cicada, brood, predator, satiation.
LLM-side functional kernel: prime-number period selection + coprime-with-
concurrent-schedule constraint + gradient-interference de-resonation +
catastrophic-forgetting suppression.

### Fresh WebSearch queries (5 angles, 2024-2026)
| # | Query | Outcome |
|---|---|---|
| 1 | "prime period replay buffer continual learning forgetting 2024 2025" | Scalable Strategies for CL Replay (2505.12512), FOREVER (Ebbinghaus, 2601.03938), Adaptive Contrastive Replay (2410.07110), SuRe (2511.22367), MSSR (2603.09892), Adaptive Memory Replay CVPR-W 2024 — all **adaptive / surprise / memory-aware**, **none use prime-period selection**. |
| 2 | "coprime sampling rehearsal scheduling neural network training cycle period" | Scheduled Sampling (Bengio 2015) and variants — about teacher-forcing decay, **not** coprime period selection. |
| 3 | "non-resonant aperiodic replay catastrophic forgetting frequency decorrelated training schedule 2025" | Stateful Replay (2511.17936), RMAF (active-forgetting replay), Brain-inspired Replay (Nature Comm), Sleep-like Replay (PMC), Continual Flatness (C-Flat) — **decorrelation discussed as outcome**, **not engineered via coprime period selection**. |
| 4 | "resonance gradient interference learning rate schedule period interaction 2025" | LR-schedule optimisation papers (2601.07830, 2512.14527, 2512.05084), critical learning periods (2510.09687) — discuss interactions, **no prime/coprime mechanism for resonance avoidance**. |
| 5 | "prime number period training neural network avoid alignment cycle" | Prime classification with sparse encoding (2402.03363), Neural Networks Fail to Learn Periodic Functions — about *learning* primes, **not about using primes for training cadence**. |
| 6 | (bonus) "cicada principle aperiodic pattern non-repeating prime CSS design" | **Cicada Principle in CSS** (CSS-Tricks, Devopedia, Lea Verou) — uses prime-numbered pixel widths or animation durations to create non-repeating visual patterns / non-resonant animations. **Direct conceptual transfer of cicada coprime-period mathematics to a computing subfield exists — but only in CSS visual design, NOT in ML training or replay scheduling**. |
| 7 | (bonus) "cyclical learning rate restart period gradient phase decorrelation continual" | Cyclical LR (1506.01186), SGDR warm restarts (period grows ×2), critical learning periods — **monotonic / geometric / power-of-2** period growth, **not prime-coprime by design**. |

### Single-paper hit test
No paper scores judge ≥ 0.7 against the prime-coprime replay-period
mechanism. Highest scores:
- Replay Scheduling MCTS (2209.08660): judge ≈ 0.60 (same artefact —
  replay schedule — learned via MCTS, not number-theoretic).
- FOREVER (2601.03938): judge ≈ 0.62 (Ebbinghaus expanding-interval
  replay — different mechanism, same functional space).
- 2106.15739 NeurIPS 2021 "Periodic Behavior of NN training with BN+WD":
  judge ≈ 0.55 (identifies the *problem* of periodic destabilisation,
  proposes no specific mechanism).
- Cicada Principle (CSS-Tricks blog): judge ≈ 0.45 against the LLM
  context (uses the exact prime-coprime mathematics, but applied to
  visual tiles / animations, not gradient interference).

### Distributed-prior-art (L7) test
Three-paper composition that *almost* covers the kernel:
1. Cicada Principle (CSS) — covers "prime period → coprime aperiodicity
   → non-resonance".
2. Replay Scheduling MCTS (2209.08660) — covers "replay-buffer
   scheduling" as a tunable, adaptive object.
3. 2106.15739 NeurIPS 2021 — covers "periodic schedules interact and
   create destabilisation; need to dampen".

Combined functional coverage: ~0.65–0.70. The integration step
(*apply Cicada Principle as the mechanism to solve the 2106.15739
problem in the 2209.08660 replay artefact*) is the candidate's
non-redundant contribution. **No published paper performs the
integration.**

This is a **borderline L7 case**: the kernel is split across three
distinct works (CSS design + RL replay scheduling + NN-training periodic
behaviour), but the composition is unpublished. L7 typically requires
that the *integration* be also covered by some paper, even with
different vocabulary; here it is not.

### Verdict R302: **HONEST PASS (UNCERTAIN, borderline-L7)**

Reasons HONEST PASS:
1. No single paper scores ≥ 0.7.
2. The integration of Cicada Principle into replay scheduling is
   unpublished.
3. The novel claim (deliberate prime-numbered period to force coprimality
   with concurrent schedules) is genuinely absent from 2024–2026 LLM
   literature.

Reasons UNCERTAIN (borderline L7):
1. **Distributed prior art exists** for the components (Cicada Principle
   in CSS + replay scheduling + periodic-schedule interaction
   literature). Combined judge ≈ 0.65–0.70.
2. The mechanism is mathematically simple (1-line:
   `replay_every_k_epochs` where `k ∈ {13, 17, 19, 23}`); plausible that
   practitioners use this informally without publishing as a named
   technique.
3. No empirical validation in the candidate.

Action: **Do NOT** mark R302 as false positive. Keep PASS-with-caveat
(UNCERTAIN, borderline-L7). Flag for human review with note: "Cicada
Principle in CSS is conceptually adjacent; check whether any 2026
preprint has carried it to ML training; check informal practitioner
forums (Reddit, HN, ML Twitter)."

---

## Summary

| Round | Phase-0 Verdict | Change vs prior audit | N_verified delta |
|---|---|---|---|
| R279 | HONEST PASS (UNCERTAIN) | No change (confirms prior `r279_audit.md`); adds 5 fresh queries from different angles, all still negative | 0 |
| R302 | HONEST PASS (UNCERTAIN, borderline-L7) | No change to PASS-with-caveat status; **new** finding: Cicada Principle exists as published technique in CSS but not in ML training. Promotes to borderline-L7 flag | 0 |

Neither round becomes a FUNCTIONAL FALSE POSITIVE under deeper scrutiny.
Both remain flagged for human review.

### Cross-round pattern observation
Both R279 and R302 share a common structure: the candidate proposes a
**number-theoretic / mathematical constraint** (integer ratios; primes /
coprimality) borrowed from a non-ML source domain (music; insect
biology). For both, the **mathematical constraint itself** is the kernel
that resists vocabulary collision, because target spectra and period
selection are typically discussed in indexed ML literature with
*continuous / adaptive / learned* mechanisms rather than *discrete /
prescriptive / number-theoretic* ones.

This suggests a refinement to the L7 detector: **explicitly probe
number-theoretic adjacency** (CSS Cicada Principle, signal-processing
coprime-array sampling, integer-ratio synthesizer design, etc.) when a
candidate's kernel is a discrete numerical structure that the candidate
borrows from outside ML.

### Memory_db update
- R279: no change to memory_db.json (UNCERTAIN; not a false positive).
- R302: no change to memory_db.json (UNCERTAIN; not a false positive).
  Add a *pattern note*: L7 distributed-prior-art adjacency for
  number-theoretic kernels — document the Cicada Principle CSS-precedent
  for any future cicada-based candidate.

### Caveats
1. WebSearch is not exhaustive. Negative results bound recall of indexed
   2024–2026 literature; they do not certify absolute novelty.
2. Both rounds describe mathematically simple mechanisms with low
   publication-disclosure bars; practitioners may use them informally.
3. Both candidates lack empirical validation; their *functional* novelty
   is formal, not demonstrated.

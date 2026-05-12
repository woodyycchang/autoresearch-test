# r301_r302_audit.md

Phase-0 deep functional audit of the two epoch-13 PASS-with-caveat rounds.

Audit date: 2026-05-12T16:04Z
Auditor: Claude Opus 4.7 (this session)
Auditor context: fresh re-read of 05_candidate.json; 7 WebSearch queries
across the functional content of each round.

The audit goal is to detect Pattern D (functional-equivalence gap):
candidate and prior art share the same end-state mechanism on the same LLM
artefact, but neither share substring vocabulary nor sentence-level
embedding above 0.7. If found, reclassify PASS → FUNCTIONAL FALSE POSITIVE.

---

## R301 — Glasswing butterfly nano-pillar tapered K-stage anti-reflection

### 1. Candidate mechanism (stripped of source-domain vocabulary)

From `rounds/round_301/05_candidate.json`:

> A K-stage stack of pre-attention input projection sub-layers whose
> weight scales are monotonically tapered (largest at input side,
> smallest at attention side), random in amplitude, designed to produce
> a smooth gradient norm transition from raw embeddings to attention
> input. Targets suppression of "input-boundary reflection" — i.e.,
> gradient discontinuity / spurious activation echo at the
> embedding-to-attention boundary.

Stripped phrasing:
- **What is changed:** pre-attention input projection weights.
- **How they are changed:** stacked K layers, weight scale tapered
  monotonically from larger (input) to smaller (output), random sign
  pattern.
- **What it does:** smooths the gradient/embedding-norm transition
  across layers; eliminates large-step discontinuity at the
  embedding→attention boundary.
- **Functional effect:** improve gradient back-propagation across the
  embedding-to-attention boundary; reduce variance shocks; stabilize
  early-layer training dynamics.

### 2. Source-domain content_words and functional content_words

LLM-side from candidate:
- "tapered amplitude embedding"
- "K-stage input projection scaffold"
- "gradient embedding-norm transition"
- "boundary-reflection suppression"

Stripped functional content_words:
- depth-scaled weight initialization
- per-layer variance taper
- pre-attention input projection stack
- gradient propagation through embedding-attention boundary
- residual-spike suppression

### 3. WebSearch queries (5)

| # | Query | Hits relevant to functional content |
|---|---|---|
| 1 | "tapered input scaffolding K-stage curriculum LLM 2025" | none directly (returned only education-curriculum LLM papers) |
| 2 | "anti-reflective input encoding gradient transformer 2024 2025" | 2402.02593 LeakyReLU/GELU gradient-discontinuity / noise-resilience (Vision Transformer); Optica anti-reflective gradient-index lens (off-target) |
| 3 | "gradient embedding norm transition input projection layers LLM 2025" | 2312.16903 Spike No More COLM 2025 ("shrink embedding gradient"); 2502.02732 Peri-LN ("constrains residual spikes commonly observed in Pre-LN"); 2502.06742 Gradient Multi-Normalization / SinkGD |
| 4 | "depth-wise weight scale taper transformer initialization gradient propagation" | **2510.09423** Weight Initialization and Variance Dynamics (2025): "shallow layers exhibit rapid and sizable early expansion of weight standard deviations, whereas deeper layers expand more gradually" — **depth-dependent variance equilibration**; **1908.11365** DS-Init (parameter variance scaled by 1/√l per layer); **2203.00555** DeepNet (scaling to 1000 layers via tapered initialization); **2509.05018** Per-Layer Depth-Informed Init |
| 5 | "layer-wise scaling embedding input boundary gradient smoothing transformer 2026" | **2603.09815** Smoothing Pseudo-Projector ("projection-based smoothing enables stronger alignment with the true global shape while reducing sensitivity to high-frequency distortions"); 2601.10639 STEM scaling transformers with embedding modules; 2502.01637 Scaling Embedding Layers |

### 4. Functional-equivalence judgment

The candidate's functional content — *stack K projection layers with
monotonically tapered weight scales to smooth the gradient-norm
transition between embedding and attention* — maps directly onto:

| Prior art | Functional overlap | Judge-score estimate |
|---|---|---|
| **DS-Init (1908.11365)** | Per-layer parameter variance scaled by 1/√l so output variance of residual connections eases gradient back-prop through normalization. Same effect (graduated variance reduction across layers to smooth gradient propagation); different framing. | **0.85** |
| **Weight Init Variance Dynamics (2510.09423)** | Emergent depth-dependent variance equilibration — shallow layers expand more rapidly, deeper layers more gradually, exactly the tapered profile the candidate prescribes manually. Identifies the same dynamic as a self-organizing property the candidate proposes to install by construction. | **0.80** |
| **Peri-LN (2502.02732)** | Normalizes both input and output of each sub-layer to constrain residual spikes commonly observed in Pre-LN, while maintaining stronger gradient pathway than Post-LN. Same artefact (sub-layer boundary); same effect (eliminate gradient discontinuity at sub-layer boundary). | **0.75** |
| **Spike No More (2312.16903 COLM 2025)** | "Shrink embedding gradient" technique stabilizes LLM pre-training by attenuating embedding-layer gradient magnitudes — directly equivalent to "boundary-reflection suppression" at the embedding-to-attention boundary. | **0.82** |
| **DeepNet (2203.00555)** | Scales transformers to 1000 layers via tapered initialization (deeper layer = smaller initial weight scale), which is the same monotonic-taper-with-depth pattern. | **0.78** |

Five distinct papers (2019, 2022, 2023, 2025, 2025) score ≥ 0.75 against
the candidate. The "random amplitude" qualifier in the candidate is
inherited from the biological metaphor (sub-wavelength random pillar
sizes) but, functionally, *every standard initialization scheme is
random amplitude with controlled variance*. The "K-stage" qualifier is
just "stacked sub-layers" — the canonical transformer structure.

The candidate's only genuinely distinctive content over the prior art is:
- placing the variance-tapered projections *specifically before the
  first attention block* rather than spread throughout the body, AND
- describing the effect with optical-physics vocabulary
  ("anti-reflection", "refractive-index gradient").

Both differences are positional/vocabulary — not mechanistic. The
end-state mechanism (variance-tapered projections smoothing gradient
propagation across a layer boundary) is identical to the prior art.

### 5. Verdict R301

**FUNCTIONAL FALSE POSITIVE (Pattern D).**

The candidate is a Pattern D collision with at least 5 distinct
2019-2026 papers (DS-Init, DeepNet, Spike-No-More, Peri-LN, Variance
Dynamics 2025). The v4 semantic check and v5 functional-judge step both
missed it in epoch 13 because:
1. None of the content_words ("tapered amplitude embedding",
   "K-stage input projection scaffold", "gradient embedding-norm
   transition", "boundary-reflection suppression") shared substring
   vocabulary with any single 06_search_raw result.
2. The candidate's `llm_application` framing was metaphorically distant
   from any single prior-art abstract (cosine < 0.7 against any single
   result).
3. The functional-judge step did not assemble across multiple results
   the same way this audit did — depth-scaled initialization + Peri-LN
   + Spike-No-More together saturate the functional space, but no
   single result is a perfect match.

This is the same false-positive signature as R079 / R085 / R091 / R092
(epoch 4) and R119 / R124 (epoch 6) — Pattern D functional collision
across vocabulary gap.

**Action:** reclassify R301 verdict from PASS-with-caveat to
FUNCTIONAL FALSE POSITIVE. Decrement N_verified PASS count. Append
Pattern D entry to memory_db.json.

---

## R302 — Brood-X 17-year periodical cicada prime-coprime replay scheduling

### 1. Candidate mechanism (stripped of source-domain vocabulary)

From `rounds/round_302/05_candidate.json`:

> Continual-learning replay-buffer refresh + curriculum task rotation
> triggered at PRIME-numbered epoch periods (13, 17, 19, 23)
> *deliberately* chosen coprime with other concurrent periodic training
> schedules (LR cosine period, eval cadence, weight-decay cycle,
> gradient-norm-clip cadence). De-aligns periodic schedules so that
> gradient interference does not resonance-amplify catastrophic
> forgetting.

Stripped phrasing:
- **What is changed:** period at which replay-buffer refresh / curriculum
  task rotation events fire.
- **How it is changed:** chosen as a prime number (13, 17, 19, 23) so
  that the period is coprime with every other concurrent periodic
  schedule used during training.
- **Functional effect:** the GCD of replay-event period and any other
  schedule's period is 1, so the least-common-multiple is the product,
  so no resonance accumulation of gradient interference across cycles.

### 2. LLM-side content_words

- "prime-numbered replay period"
- "coprime cycle scheduling"
- "resonance-interference avoidance"
- "gradient-cycle de-alignment"

### 3. WebSearch queries (5)

| # | Query | Hits relevant to functional content |
|---|---|---|
| 1 | "prime number replay scheduling continual learning catastrophic forgetting" | 2209.08660 Replay Scheduling MCTS; 2601.03938 FOREVER; 2402.01348 CORE — adaptive scheduling literature, **no prime/coprime selection** |
| 2 | "coprime period buffer rehearsal continual learning resonance gradient interference" | GCR / OCS / gradient-projection memory — gradient-aware buffer-selection literature, none using period coprimality |
| 3 | "anti-correlated replay frequency catastrophic forgetting de-aligned schedule" | FOREVER aligns replay schedules to model-update magnitude (different mechanism); CORE cognitive-replay |
| 4 | "incommensurate period scheduling neural network training periodic interference avoid" | **2106.15739** "On the Periodic Behavior of Neural Network Training with Batch Normalization and Weight Decay" (NeurIPS 2021) — explicitly identifies periodic destabilization arising from BN+WD interaction; AISAW interference-aware scheduling for distributed training |
| 5 | "prime numbers OR coprime period training schedule deep learning neural network" | 2604.02383 Neural Prime Sieves; 2402.03363 prime-classification — **no prior art using primes for training-schedule period selection** |

A 6th confirmation query on "decouple training cycles avoid resonance
period mismatch curriculum learning interference cycle" returned motor-
learning / variable-practice resonance literature (sports science),
no LLM-training match.

### 4. Functional-equivalence judgment

| Prior art | Functional overlap | Judge-score estimate |
|---|---|---|
| **2106.15739 NeurIPS 2021** "Periodic Behavior of NN Training with BN+WD" | Identifies the exact problem the candidate solves (periodic destabilization from interaction of concurrent periodic schedules), but proposes no specific solution mechanism. Same problem-statement, no mechanism overlap. | **0.55** |
| **FOREVER (2601.03938)** | Aligns replay schedules with model-update magnitude (model-centric time). Different mechanism — adaptive timing instead of pre-selected prime period — but **same functional effect**: avoid replay/training periodic interference. | **0.62** |
| **Beyond Cosine Decay / Infinite LR (2503.02844)** | Removes cyclical LR schedule entirely (no period → no resonance). Same functional effect (eliminate periodic resonance) via different mechanism (no period at all). | **0.55** |
| **Replay Scheduling MCTS (2209.08660)** | MCTS / RL to learn replay-period policy — same functional effect, learned schedule (adaptive) rather than fixed prime. | **0.60** |
| **WSD scheduler (2408.13359 + canonical)** | Three-phase non-cyclical schedule eliminates resonance by being aperiodic. Same functional effect. | **0.50** |

No prior-art result reaches 0.70 functional-judge score against the
candidate. The candidate's specific mechanism — **deliberate
prime-number selection so that replay period and concurrent schedules
are coprime by construction** — is genuinely absent from the 2024-2026
LLM literature. The functional effect (de-resonate periodic schedules
to suppress gradient interference) is occupied by adaptive scheduling
and aperiodic schedule alternatives, but the prime-coprime mechanism
itself is not.

### 5. Verdict R302

**UNCERTAIN.**

The prime/coprime mechanism is novel relative to 2024-2026 LLM training
literature. The candidate's *problem* (periodic resonance amplifies
gradient interference) is published (2106.15739 NeurIPS 2021). The
candidate's *solution mechanism* (use primes to force coprime periods)
is not. The functional EFFECT is occupied by adaptive / aperiodic
schedule literature, but with measurably different mechanisms (judge
scores 0.50-0.62, none ≥ 0.70).

Two reasons to remain UNCERTAIN rather than HONEST PASS:
1. The prime/coprime mechanism is mathematically simple (1-line
   modification: replay_every_k_epochs where k ∈ {13, 17, 19, 23});
   it is plausible that practitioners do this informally without
   publishing it as a named technique. Negative search evidence is
   weak for low-disclosure-bar interventions.
2. The candidate's claim of effect (suppress catastrophic forgetting
   via period de-alignment) is not empirically validated — no
   experiments referenced. The mechanism could be functionally
   equivalent to existing aperiodic-schedule solutions even if not
   nomenclaturally identical.

Two reasons NOT to reclassify as FUNCTIONAL FALSE POSITIVE:
1. No single prior-art paper scores judge ≥ 0.70 against the candidate.
2. The mechanism (prime period chosen *specifically* for coprimality
   with other concurrent schedules) is genuinely distinctive — the
   adaptive-scheduling literature does not pre-select periods on
   number-theoretic grounds.

**Action:** keep R302 verdict as PASS-with-caveat (UNCERTAIN). Flag for
human review with an explicit "low-disclosure-bar mechanism — negative
search evidence is weak" caveat. Do NOT decrement N_verified PASS count
for R302.

---

## Summary table

| Round | Verdict | Decrement N_verified? | Memory_db Pattern D update? |
|---|---|---|---|
| **R301** | FUNCTIONAL FALSE POSITIVE | yes | yes (Pattern D, 5 prior-art collisions) |
| **R302** | UNCERTAIN (keep PASS-with-caveat) | no | no |

Effect on N_verified PASS count:
- Before audit: 2 PASS-with-caveat in epoch 13 → 421 verified, 2 PASS
  (1 honest from R279, 2 caveat from R301/R302).
- After audit: 421 verified, R301 reclassified to false positive, R302
  remains PASS-with-caveat (UNCERTAIN).
- Substantive PASS count (post-functional-audit): **1** (R279 only).
- Caveat-PASS count: **1** (R302 UNCERTAIN).

This audit confirms that v5's functional-judge step 06.7 is still
missing some Pattern D collisions when the prior art is distributed
across multiple papers rather than concentrated in any single result.
Recommend epoch 14 add a multi-result aggregation pass to the
functional-judge — see `output/epoch14_self_audit.md` (forthcoming).

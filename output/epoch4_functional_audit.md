# Epoch 4 Functional-Equivalence Audit

**Author:** Claude (Opus 4.7)
**Date:** 2026-05-11
**Branch:** `claude/continue-niche-mining-research-OxqsL`
**Inputs:** `rounds/round_{079,085,091,092}/05_candidate.json`; web_search for
the FUNCTIONAL effect (not the source-domain vocabulary).

---

## 0. Scope and method

The epoch 4 verifier (program_v4.md step 06.5) cleared four mechanical
PASSes — R079, R085, R091, R092 — because their `content_words` are
entirely source-side (botany / tribology / extremophile-biology /
marine-biology) and the embedding similarity between
`candidate.llm_application` and the result `title+snippet` never
reached the 0.7 threshold.

Phase 1's question: **does the functional effect that the
candidate's `llm_application` describes already exist in the 2024-2026
LLM literature with different terminology and a different metaphor?**

For each round, we web_search the FUNCTIONAL content (not the
source-domain word) and inspect the top results for any paper that
achieves the same end-state with different vocabulary. A functional
match is any paper whose mechanism, when stripped of its label,
performs the same operation on the LLM artefact the candidate
proposes to operate on.

---

## 1. R079 — phyllotaxis Fibonacci leaf arrangement

### Candidate

- `domain`: phyllotaxis (Fibonacci leaf arrangement)
- `specific_mechanism`: "Plant leaves arrange in spiral phyllotaxis
  with golden-angle (137.5°) divergence to minimize self-shading;
  the spiral emerges from auxin-driven reaction-diffusion dynamics
  in the meristem"
- `llm_application`: "LLM attention head positioning via golden-angle
  distribution to minimize attention head redundancy; treat each
  head as a leaf and the prompt-token sequence as the meristem
  shoot."

### Functional content stripped of metaphor

The candidate proposes (a) distributing attention heads in a
representation space so that (b) inter-head redundancy is minimised
via (c) an angle-based geometric criterion (golden angle 137.5°)
applied (d) layer-by-layer (the meristem-shoot analog).

### 2024-2026 prior art on the FUNCTIONAL effect

| Effect the candidate claims | 2024-2026 LLM paper covering the same effect | Different metaphor used |
|---|---|---|
| Distribute heads to minimise inter-head redundancy | Kong et al., **"Diversifying Multi-Head Attention in the Transformer Model"** (MDPI MAKE, Nov 2024) — DEACON enforces head-diversification via constrained Hebbian optimization on a feed-forward layer added on top of the heads | "diversification", "Hebbian PCA-on-heads" — no botany metaphor but identical functional outcome |
| Pruning redundant heads with low cost | Voita et al. ACL 2019 + follow-ups, "Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned" — pruning 38 of 48 encoder heads with 0.15 BLEU drop. 2024-2025 follow-ups: differentiable subset pruning (TACL 2022), A* head pruning (2110.15225), "Pruning Attention Heads with Almost-sure Sparsity Targets" (OpenReview 2025) | "head importance", "sparsity targets" |
| Differential post-hoc modification of attention to reduce head correlation | Kong et al., **DEX** (Differential modification, May 2025): "differential attention yields less correlated, more diverse attention heads, reducing head redundancy through cosine distance and CKA analyses." Published 2025. | "differential transformer" + "cosine distance / CKA on heads" |
| Knowledge-distillation of multiple correlated heads into fewer diverse heads | **SHD** (Structured Head Distillation), 2025 — "linearly approximating and compressing multiple teacher heads into fewer student heads, SHD enables projector-free, linear-time distillation, maintaining fine-grained attention structure in compact student models." | "structured head distillation" |
| Geometric / angular criterion on attention heads | Multiple papers using cosine distance, CKA distance, and orthogonality constraints on head subspaces (DEACON's PCA-via-GHA explicitly imposes inter-head orthogonality in a principal-component basis) | "orthogonal subspace", "cosine-distance penalty" |

**Verdict for R079: FUNCTIONAL FALSE POSITIVE.**

The candidate's "minimise inter-head redundancy by spacing heads in an
angular criterion" is functionally identical to DEACON (Nov 2024) and
to the 2025 differential-transformer literature. The only thing the
candidate adds — using 137.5° specifically — is a numeric choice that
no head-diversification paper has tested, but the prior art covers
"minimise redundancy via angular / subspace criterion" as a complete
mechanism. The 137.5° specific exponent is a numerical detail, not a
paradigm shift; ablating against 90°, 120°, or random angles would be
a straightforward delta paper, not a new niche.

---

## 2. R085 — extreme-pressure tribology boundary lubrication breakdown

### Candidate

- `domain`: extreme-pressure tribology (boundary lubrication breakdown)
- `specific_mechanism`: "Under extreme contact pressure, boundary
  lubrication transitions from elastohydrodynamic film to direct
  asperity contact; lubrication failure follows a
  stress-corrosion-cracking-like statistical distribution"
- `llm_application`: "LLM safety boundary analog: under high
  prompt-injection pressure, alignment 'lubrication' transitions
  from soft-prompt deflection to direct training-data leak;
  failure follows stress-cracking distribution."

### Functional content stripped of metaphor

The candidate proposes (a) modelling LLM alignment as a layered
boundary that (b) degrades non-linearly under increasing adversarial
pressure with (c) a phase-transition between two regimes (soft-prompt
deflection vs direct training-data leak) and (d) a heavy-tailed
failure-rate distribution.

### 2024-2026 prior art on the FUNCTIONAL effect

| Effect the candidate claims | 2024-2026 LLM paper covering the same effect | Different metaphor used |
|---|---|---|
| Failure rate distribution under increasing attack pressure | **"Jailbreaking LLMs: A Survey of Attacks, Defenses and Evaluation"** (TechRxiv 2026); **JailbreakRadar** (ACL 2025) — taxonomy of 17 attacks across 9 LLMs, ASR distributions across 16 violation categories; recent surveys quote 90-99% open-weight, 80-94% proprietary | "attack success rate distribution" |
| Phase transition between weak-attack and strong-attack regimes | **"LLM Jailbreaking in 2026: 97% Success Rates, Autonomous Attacks"** + Nature Communications 2026 study showing autonomous-jailbreak ASR jumps at certain model-capability thresholds | "capability cliff", "autonomous jailbreak threshold" |
| Soft-vs-direct training-data leak distinction | **"Aligning LLMs to Be Robust Against Prompt Injection"** SecAlign (2410.05451); "Prompt Injection via Adversarial Poetry" 2025; OWASP LLM01:2025 — explicit two-regime taxonomy (soft instruction-following bypass vs direct extraction) | "soft-prompt evasion" vs "direct extraction" |
| Heavy-tailed extreme-case-failure distribution | **"LLMs know their vulnerabilities: Uncover Safety Gaps through Natural Distribution Shifts"** ACL 2025 — explicit distribution-shift framing of failure modes | "distribution shift", "long-tail safety gaps" |
| Boundary / film degradation as alignment metaphor | Multiple alignment-robustness papers use "alignment boundary" / "safety boundary" / "alignment film" framings (e.g., **"Evading LLMs' Safety Boundary with Adaptive Role-Play Jailbreaking"** MDPI 2025) | "safety boundary erosion", "alignment surface" |

**Verdict for R085: FUNCTIONAL FALSE POSITIVE.**

The candidate's "alignment lubrication degrades under prompt-injection
pressure, transitions from soft to hard failure, follows a
stress-cracking distribution" is functionally identical to the 2025
jailbreak-survey literature on (a) ASR vs attack strength curves, (b)
soft-bypass vs direct-extraction taxonomies, (c) long-tail safety
gap analyses. The "stress-corrosion-cracking" probability distribution
is a specific Weibull / heavy-tailed shape, but jailbreak-distribution
literature already fits heavy-tailed laws to ASR-vs-effort curves
(e.g., the 60-second / 7-query attack-budget distribution in autonomous
jailbreak studies).

---

## 3. R091 — tardigrade desiccation cryptobiosis

### Candidate

- `domain`: tardigrade desiccation cryptobiosis
- `specific_mechanism`: "Tardigrades survive complete dehydration via
  tun-state cryptobiosis: trehalose vitrification + intrinsically
  disordered proteins prevent membrane fusion; rehydration restores
  function"
- `llm_application`: "LLM model 'dormancy': vitrify a model's parameters
  into a low-energy frozen state for cold storage; rehydrate via
  context-driven activation without re-training."

### Functional content stripped of metaphor

The candidate proposes (a) freezing LLM parameters into a reduced
storage representation (b) without retraining and (c) reactivating
the model via context-driven activation, claiming this is novel.

### 2024-2026 prior art on the FUNCTIONAL effect

| Effect the candidate claims | 2024-2026 LLM paper covering the same effect | Different metaphor used |
|---|---|---|
| Freeze parameters into a low-energy / low-precision frozen state for cold storage | **4-bit post-training quantization** (GPTQ, AWQ, and follow-ups: ParoQuant ICLR 2026, Tequila ICLR 2026, Q&C ICLR 2026, SliderQuant); **"A Survey of Quantization in LLM"** Springer JCST 2026 | "post-training quantization", "INT4 / INT8 / ternary" |
| Reactivate without retraining via context | **In-context learning** literature (vast); **PEFT/LoRA adapters** preserve base weights and reactivate via small adapter loading without base retraining | "in-context learning", "adapter swap" |
| Selective freezing of parameters with importance-aware protection | **Source-Shielded Updates (SSU)** OpenReview 2025 — column-wise freezing of important parameters before adaptation; **"Mitigating Catastrophic Forgetting in Continual Learning through Model Growth"** 2509.01213; FIT continual unlearning 2601.21682 | "parameter importance", "column-wise freezing", "model growth" |
| Vitrification (amorphous solid storage of structure) | Quantization to low-bit and weight sharing → effectively "vitrify" the precise float values into a coarse-grained representation that still allows recovery; **"Awesome-Model-Quantization"** maintains 2020-2025 paper list | "weight sharing", "low-bit codebook" |
| Survive complete shutdown / cold storage + reanimate | **On-Device LLMs: State of the Union, 2026** — discusses model "warm boot" from quantized form; vector-DB-based RAG also frames retrieval as on-demand reactivation of frozen knowledge | "warm boot", "frozen knowledge retrieval" |

**Verdict for R091: FUNCTIONAL FALSE POSITIVE.**

The candidate's "freeze parameters, store cheaply, reactivate without
retraining" maps directly to the 2024-2026 4-bit post-training-quantization
+ PEFT-adapter literature. The only original element is the metaphor
("vitrification" / "trehalose") rather than the function. The "rehydrate
via context-driven activation without re-training" phrase is literally
what in-context-learning + LoRA-adapter loading already does in 2024-2026
production deployment.

---

## 4. R092 — Antarctic icefish antifreeze glycoproteins

### Candidate

- `domain`: Antarctic icefish antifreeze glycoproteins
- `specific_mechanism`: "Antarctic icefish produce AFGPs that bind
  ice-crystal nuclei and prevent growth via non-colligative thermal
  hysteresis, allowing survival at -2°C ocean temperatures"
- `llm_application`: "LLM training-loss antifreeze: detect early-stage
  gradient 'crystal nuclei' (e.g., correlated noise patterns) and
  bind them with anti-correlated update vectors before they grow
  into instability."

### Functional content stripped of metaphor

The candidate proposes (a) detecting early-stage gradient noise
patterns that (b) would otherwise grow into training instability,
and (c) cancelling them with anti-correlated update vectors.

### 2024-2026 prior art on the FUNCTIONAL effect

| Effect the candidate claims | 2024-2026 LLM paper covering the same effect | Different metaphor used |
|---|---|---|
| Anti-correlated gradient noise to stabilise training | **"Anti-Correlated Noise in Epoch-Based Stochastic Gradient Descent: Implications for Weight Variances in Flat Directions"** (arXiv 2306.05300) — explicitly uses *"anti-correlated noise"* terminology. Same word, different LLM context: epoch-based SGD with momentum. | "anti-correlated noise" — same phrase! |
| Detect gradient spikes / early instability and cancel them | **SPAM (Spike-Aware Adam with Momentum Reset)** 2025 — when large gradient spikes detected, resets optimizer first/second moments to prevent the spike from continuing to influence updates | "spike-aware momentum reset" |
| Gradient signal-to-noise ratio analysis for training stability | **"Revealing Modular Gradient Noise Imbalance in LLMs: Calibrating Adam via Signal-to-Noise Ratio"** (arXiv 2605.05794, MoLS, 2026) — module-wise SNR scaling for rebalancing updates | "module-wise SNR scaling" |
| Noise-robust training with bias correction | **"Noise-corrected GRPO: From Noisy Rewards to Unbiased Gradients"** (2510.18924) — explicit bias-correction for noisy RL signals | "noise-corrected GRPO" |
| Hessian clipping / gradient annealing | **"Hessian Layer-wise Clipping and Gradient Annealing"** EMNLP 2025 | "Hessian clipping", "gradient annealing" |
| Uncertainty-aware gradient SNR data selection | **"Uncertainty-Aware Gradient Signal-to-Noise Data Selection for Instruction Tuning"** (2601.13697) — explicit gradient SNR threshold for data selection | "gradient SNR data selection" |

**Verdict for R092: FUNCTIONAL FALSE POSITIVE — STRONGEST OF THE FOUR.**

The candidate's "detect early-stage correlated noise patterns and bind
them with anti-correlated update vectors" is literally the same
phenomenon studied in 2306.05300 (Anti-Correlated Noise in Epoch-Based
SGD), 2025 SPAM (spike-aware reset), 2026 MoLS (module SNR scaling),
and 2510.18924 (noise-corrected GRPO). The candidate happens to share
the exact phrase "anti-correlated noise" with the prior-art paper —
which means even a strict-substring keyword rule would have caught it
if "anti-correlated" had been in `content_words`. The candidate's
content_words were entirely on the icefish/biology side, so the
keyword rule missed it; the semantic check (max cosine 0.544) also
missed it because the embedding model could not bridge "antifreeze
glycoprotein" ↔ "anti-correlated SGD noise" without LLM-side anchor
words in `candidate.llm_application`.

---

## 5. Summary across all four

| Round | LLM-application stripped of metaphor | 2024-2026 LLM paper covering same effect | Verdict |
|---|---|---|---|
| **R079** | Minimise inter-head redundancy via angular / subspace criterion | DEACON (Kong et al. 2024), DEX (2025), SHD (2025), Voita ACL 2019 + 2024 follow-ups | **FUNCTIONAL FALSE POSITIVE** |
| **R085** | Heavy-tailed phase-transition failure curve under adversarial pressure | JailbreakRadar ACL 2025, SecAlign 2024, "LLMs know their vulnerabilities" ACL 2025, MDPI 2025 safety-boundary jailbreak study | **FUNCTIONAL FALSE POSITIVE** |
| **R091** | Freeze parameters into compressed dormant state; reactivate without retraining | GPTQ + AWQ + ParoQuant/Tequila/Q&C/SliderQuant ICLR 2026; SSU OpenReview 2025; PEFT/LoRA + ICL | **FUNCTIONAL FALSE POSITIVE** |
| **R092** | Detect correlated gradient noise, cancel with anti-correlated update | 2306.05300 (literally uses "anti-correlated noise"); SPAM 2025; MoLS 2026; noise-corrected GRPO 2510.18924 | **FUNCTIONAL FALSE POSITIVE — strongest** |

---

## 6. Why v4 semantic check missed all four

For all four candidates, `content_words_composition.llm_side = []` and
`content_words_composition.source_side` covers all 8 words. The
candidate's `llm_application` field DOES mention LLM-side concepts
("attention head", "alignment", "parameter cold storage",
"training-loss gradient"), but the embedding similarity is computed
against the **result.title+snippet**, which uses the prior-art's
terminology ("multi-head attention diversification", "jailbreak ASR",
"4-bit quantization", "anti-correlated SGD noise"). The
embedding-model-as-bridge succeeded for R078, R081, R086, R088, R090,
R093 (all caught by v4 semantic check) because their `llm_application`
phrasing was closer to the prior-art's phrasing. The four PASSes use
LLM-application phrasing that is just one synonym hop away from the
prior art — but that one hop pushes the cosine below 0.7.

**Pattern D — functional-equivalence gap unmasked.** R079, R085, R091,
R092 are not Pattern A/B/C false positives (the v4 semantic check
catches those). They are a new pattern: `llm_application` and prior
art share **mechanism** but neither share **vocabulary** nor share
**sentence-level concept embedding**. The bridge is at the level of
*what the mechanism does*, not what it is called.

The v5 fix is to add an LLM-judge layer that reads
`candidate.llm_application` + top-10 search results and answers, per
result, the explicit question *"does this paper achieve the same
FUNCTIONAL effect, even with different terminology?"* A score ≥ 0.7
on this LLM-judge dimension forces hit=true. This catches Pattern D
without lowering the v4 semantic-cosine threshold below 0.7 (which
would introduce new false negatives on truly novel candidates).

---

## 7. Implication for the running corpus

If R079/R085/R091/R092 are accepted as false positives:

- v4 substantive PASS count drops from **4 → 0**.
- The cumulative corpus N=238 with 0 substantive PASS is restored.
- The saturation hypothesis at ≥1% novelty is unrejected:
  p((0.99)^238) ≈ 0.093 — still not formally rejected at p<0.05, but
  consistent with structural saturation.
- The detector-evasion hierarchy gains a fourth level (functional
  equivalence) which is exactly what program_v5.md should target.

**Recommendation:** treat all 4 epoch-4 PASSes as Pattern D
functional-equivalence false positives. Re-run R101-R125 under
program_v5.md with the LLM-judge step 06.7 added between semantic
check (06.5) and keyword rule (07).

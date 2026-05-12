# R279 Post-Hoc Audit — Trinidadian Steel Pan PTCH

## Original Pass-with-Caveat Summary
- **Source domain**: Trinidadian steel pan tuning — single oil-drum head with note sections; tuner forces fundamental + overtones into integer-ratio harmonic series.
- **LLM application (PTCH)**: Multi-head attention fine-tuning rule constraining each head's top-K singular directions (fundamental + "overtones") to integer-ratio multiples in the embedding space, regularized by a "harmonic-alignment loss"; inter-head "grooves" enforce orthogonality.
- **Content words**: steel pan tuning, note section groove, harmonic series integer ratio, fundamental + overtone lock, harmonic alignment loss, shared substrate multi-note, head-wise singular-direction constraint, within-head harmonic locking.

## Extracted LLM-Side Mechanism (Stripped of Steel-Pan Vocabulary)
Reduced to LLM-only operational claims:
1. **Within-head SVD constraint**: For each attention head, decompose the weight matrix (or LoRA update) by SVD; identify top-K singular directions.
2. **Integer-ratio lock**: Constrain the *magnitudes* (or projection coefficients) of the top-K singular directions to obey integer ratios 1:2:3:... (harmonic-series locking).
3. **Loss term**: Add a "harmonic-alignment loss" penalizing deviation from integer-ratio relationships.
4. **Inter-head orthogonality**: Heads remain orthogonal to one another (standard multi-head separation, here renamed "grooves").

## Prior-Art Web Search (2024–2026)

### Query 1 — "harmonic integer ratio LLM positional encoding attention 2024 2025"
- Top hits: TAPE (Contextualized Equivariant PE, ICLR 2025), PEPE long-context PE, STRING shifted ROPE, DAPE data-adaptive PE.
- **None** impose integer-ratio harmonic structure on attention head singular directions. Positional encodings use *frequencies*, not integer-ratio constraints on weight SVD.

### Query 2 — "singular direction constraint LoRA fine-tuning multi-head 2025"
- Top hits: R-LoRA (randomized multi-head LoRA), RandLoRA (full-rank random), MiLoRA (least-dominant singular directions), KaSA (discards weak directions), SC-LoRA (subspace-constrained LoRA, arXiv 2505.23724).
- Closest match: SC-LoRA constrains LoRA updates to a specific subspace; MiLoRA/KaSA select singular directions but do not impose integer-ratio harmonic-series relationships among them. **No integer-ratio lock** within head.

### Query 3 — "discrete pitch field activation quantization integer ratio transformer 2025"
- Top hits: Q-DiT (CVPR 2025), EfficientQAT (ACL 2025), FP4DiT, TQ-DiT.
- These are *bit-width* quantization (INT8/INT4/FP4), not integer-ratio relationships among singular spectrum components. Conceptually orthogonal.

### Query 4 — '"harmonic alignment loss" attention head OR transformer fine-tuning 2025'
- Top hits: Squeezing-Heads Distillation (SHD), Coeff-Tuning, "No head left behind" (Amazon Science distillation alignment).
- The exact phrase "harmonic alignment loss" does **not** appear with the PTCH meaning in indexed literature. Existing "alignment losses" are about head-count alignment in distillation, not music-theoretic harmonic ratios.

### Query 5 — "within-head subspace decomposition orthogonality attention head regularization 2025"
- Top hits: Orthogonal Subspace Decomposition (ICML 2025, image detection), Continuous Subspace Optimization (2505.11816).
- Within-head decomposition exists; orthogonality regularization between heads exists; but **integer-ratio locking of top-K directions inside a head** is not present.

### Query 6 — "SVD singular value spectrum integer ratio constraint neural network 2024 2025"
- Top hits: Generalized SVD theory (Brown et al. 2025), differentiable SVD layers, spectrum analysis under data imbalance.
- Spectrum analysis is descriptive; *prescriptive integer-ratio constraints* on singular values are absent.

### Query 7 — "PTCH" OR "pan-tuned" OR "fundamental overtone" attention head LoRA
- No hits matching the specific PTCH formulation.

### Query 8 — "spectral regularization fixed ratio eigenvalue neural network attention multi-head 2025"
- Top hits: Frequency Regularization, Multi-Head Spectral-Adaptive GNNs, Spectral Suppression Ratio (SSR), Exact Spectral Norm Regularization, Eigenspectrum Analysis.
- Spectral regularization typically constrains norms (Lipschitz) or filters frequencies; **no work imposes integer-ratio relationships among eigenvalues/singular values of attention heads**.

## Judgment

**HONEST PASS (with UNCERTAIN caveat)**

### Rationale
- The **specific functional mechanism** — constraining the top-K singular directions of a single attention head to obey integer-ratio (harmonic-series) magnitude relationships, via an explicit harmonic-alignment loss — has **no direct prior art** under any metaphor that we found in 2024–2026 indexed literature.
- The novelty claim correctly distinguishes from neighboring techniques: MiLoRA/KaSA (direction selection ≠ integer-ratio lock), SC-LoRA (subspace ≠ integer-ratio), orthogonality regularization (between heads, not within-head harmonic structure), spectral norm regularization (Lipschitz bound, not ratio lock), quantization (bit-width, not spectrum ratios).
- The candidate's harmonic-locking idea is a genuinely new constraint-class on weight SVD.

### Why UNCERTAIN caveat
- The *broader* concept of structured spectral constraints (frequency regularization, spectral norm bounds, fixed-rank decompositions) is well-established. PTCH could be reframed as "spectral norm regularization with integer-ratio target spectrum" — at which point the music metaphor becomes optional ornamentation.
- The harmonic-series integer-ratio (1:2:3:...) target is mathematically arbitrary; any researcher proposing structured spectrum could land on it via numerology without invoking steel pans. We cannot rule out an unindexed preprint or arXiv withdrawal.
- However, our task is to flag *recoverable* prior art with different metaphors; we did not find it.

### Pattern Confirmed
PTCH is a clean example of the **"colorful metaphor cloaking a generic mechanism"** pattern. The mechanism (integer-ratio spectral lock) is independent of steel pans; the metaphor explains a *target* (1:2:3 ratios) but the *technique* (SVD-based regularization) is generic. Future audits should strip the metaphor immediately and ask: "Does the integer-ratio target itself add anything beyond random / Gaussian / decaying spectra?"

## Action
- Do **not** mark R279 as a false positive in `memory_db.json`. Keep PASS-with-caveat status.
- Document the pattern in epoch-13 audits: when a music/instrument metaphor produces a singular-spectrum constraint, the constraint should be evaluated against generic spectral-regularization baselines, not against the metaphor alone.

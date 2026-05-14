# R279 Adversarial Recheck (v7, Epoch 26 Pre-flight)

**Auditor:** Claude Opus 4.7 (1M ctx).
**Date:** 2026-05-14.
**Branch:** `claude/audit-r279-adversarial-ACuPk`.
**Subject:** Re-examine the 5 papers flagged in
`rounds/round_279/11_5_adversarial.json` against the actual PTCH kernel
(within-head harmonic-integer-ratio singular-direction constraint).
**Method:** WebFetch / WebSearch each paper, extract real abstract +
method, and compare per-mechanism against the candidate.

---

## 0. Re-stated PTCH kernel (vocabulary-stripped, from `05_candidate.json`)

For each attention head in a transformer (or its LoRA update):

- **M_1:** Per-attention-head SVD of weight matrix (or LoRA update).
- **M_2:** Selection of top-K singular directions within each head.
- **M_3:** Constrain the **magnitudes** of those top-K singular
  directions to **integer-ratio 1:2:3:…** multiples of a per-head
  fundamental magnitude. **Prescribed**, not learned.
- **M_4:** Explicit **harmonic-alignment loss** penalising deviation
  from the integer-ratio target spectrum.
- **M_5:** Inter-head orthogonality regularisation.

The distinguishing kernel is **M_3 + M_4 specifically tied to a
prescribed 1:2:3 integer-ratio target**, applied **per attention head**
(M_1+M_2).

The skeptical reviewer's adversarial verdict rests on the claim that
M_1+M_2+M_4+M_5 are densely covered, and that M_3 is "a parametrization
choice within an already-published spectral-shaping family."

This recheck audits that claim paper-by-paper.

---

## 1. SORSA / SODA — top hit (skeptical score 0.80)

The reviewer cited "SORSA / SODA: Spectral Orthogonal Decomposition
Adaptation, WACV 2025 / arXiv:2405.21050." This is a **conflation of two
distinct papers**. I split and audit each.

### 1a. SORSA (arXiv:2409.00055 — Cao, 2024)

**Actual title:** *SORSA: Singular Values and Orthonormal Regularized
Singular Vectors Adaptation of Large Language Models.*
**Note on citation:** The reviewer's "arXiv:2405.21050" ID is **wrong** —
that ID belongs to SODA (see 1b). The reviewer cross-wired two papers.

**Method (from abstract / openreview):**
- SVD on **the entire pre-trained weight matrix** W₀ (not per attention
  head). Adapters carry trainable principal singular weights and frozen
  residual weights.
- An **orthonormal regulariser** is applied to the principal singular
  vectors; its stated goal is to **decrease the condition number** of
  the principal weights and stabilise optimisation.
- Reports faster convergence than LoRA / PiSSA on GSM-8K.

**Per-mechanism match against PTCH:**

| PTCH sub-mechanism | SORSA covers? | Evidence |
|---|---|---|
| M_1 per-attention-head SVD | **No.** Per weight-matrix W, not per attention head. | Standard SVD on the full pretrained matrix. |
| M_2 top-K singular direction selection | Partial — top-K principal singular components are trainable. | Standard. |
| M_3 integer-ratio 1:2:3 target spectrum on magnitudes | **No.** Magnitudes are left free / trained from the natural SVD initialisation. | No prescribed ratio appears anywhere. |
| M_4 harmonic-alignment loss to integer-ratio target | **No.** The regulariser is on **orthonormality of singular vectors** (i.e. U^T U = I), not on a prescribed magnitude spectrum. | "decrease condition number" — a vector-orthonormality goal, not a magnitude-target goal. |
| M_5 inter-head orthogonality | **No.** Orthonormality is between left/right singular vectors of a single matrix, not between attention heads. | Different orthogonality. |

**Verdict:** **NOT a functional twin.** SORSA preserves the natural SVD
structure with orthonormality regularisation; PTCH *prescribes* an
integer-ratio magnitude spectrum and applies it *per head*. The
skeptical reviewer's M_4-coverage claim conflates "any regulariser
related to SVD" with "a prescriptive integer-ratio alignment loss" —
these are not the same loss family.
**Recalibrated functional-similarity score against PTCH kernel: ~0.45.**

### 1b. SODA (arXiv:2405.21050 — Zhang et al., WACV 2025)

**Actual title:** *SODA: Spectrum-Aware Parameter-Efficient Fine-Tuning
for Diffusion Models* (a.k.a. *Spectral Orthogonal Decomposition
Adaptation for Diffusion Models*).

**Method (from search summary):**
- Adjusts **both singular values and their basis vectors** of pretrained
  weights using the **Kronecker product** + **Stiefel optimisers** to
  achieve parameter-efficient adaptation of orthogonal matrices.
- Target domain: **text-to-image diffusion models**, not transformer
  LLM attention heads.
- Orthogonality is enforced via Stiefel manifold optimisation on the
  rotation of singular vectors.

**Per-mechanism match:**

| PTCH sub-mechanism | SODA covers? | Evidence |
|---|---|---|
| M_1 per-attention-head SVD | **No.** SVD on diffusion-model weight matrices (UNet conv/attention), not per attention head with a prescribed sub-block structure. | Diffusion-model layers. |
| M_2 top-K singular direction selection | Partial. | Standard top-K. |
| M_3 integer-ratio 1:2:3 target spectrum | **No.** Singular values are *rotated and shifted*, not *locked to integer ratios.* | Method "modifies both magnitude and direction" via Kronecker, with no prescribed ratio. |
| M_4 harmonic-alignment loss | **No.** Loss is task loss + Stiefel-manifold constraints; no prescriptive magnitude target. | Stiefel ≠ integer-ratio. |
| M_5 inter-head orthogonality | **No.** Orthogonality is on singular-vector basis (Stiefel), not between attention heads. | Different axis. |

**Verdict:** **NOT a functional twin.** Wrong domain (diffusion, not
LLM attention), wrong target (Stiefel-manifold rotation, not
integer-ratio magnitude lock), wrong granularity (whole-matrix, not
per-head).
**Recalibrated functional-similarity score: ~0.40.**

---

## 2. SVFT (arXiv:2405.19597, NeurIPS 2024 — Lingam et al.)

**Method:**
- SVD on weight matrix W₀ = UΣVᵀ.
- Update is **ΔW = U M Vᵀ** where M is a **sparse coefficient matrix on
  outer products of singular vectors**.
- Structured patterns for M: **plain, banded, random, top-k**.
- Trains only the coefficients of M (the *off-diagonal couplings between
  singular directions*).

**Per-mechanism match against PTCH:**

| PTCH sub-mechanism | SVFT covers? | Evidence |
|---|---|---|
| M_1 per-attention-head SVD | **No.** Per weight matrix, not per head. | Standard. |
| M_2 top-K singular direction selection | Yes (top-k variant). | One of several patterns. |
| M_3 integer-ratio 1:2:3 target spectrum | **No.** M's entries are **learned coefficients**, not prescribed integer ratios. | "training only the coefficients." |
| M_4 harmonic-alignment loss to integer ratios | **No.** Loss is downstream task loss; sparsity is structural, not prescriptive. | No prescribed magnitude target. |
| M_5 inter-head orthogonality | **No.** No inter-head term — single matrix at a time. | Out of scope. |

**Verdict:** **NOT a functional twin.** SVFT learns *off-diagonal
couplings between singular directions*; PTCH *prescribes a fixed
magnitude spectrum*. These are categorically different objectives: a
banded coupling structure has nothing to do with a 1:2:3 magnitude lock.
**Recalibrated functional-similarity score: ~0.45.**

---

## 3. SALT (arXiv:2503.16055, BMVC 2025)

**Method:**
- SVD on weight matrices.
- **Trainable scale and shift** parameters on the **top singular
  values** (i.e. σ_i ← s_i · σ_i + t_i, with s_i, t_i **learned**).
- LoRA blocks on the lower singular subspace.
- Application domain: **medical image segmentation.**

**Per-mechanism match:**

| PTCH sub-mechanism | SALT covers? | Evidence |
|---|---|---|
| M_1 per-attention-head SVD | **No.** Per weight matrix; no per-head split. | Standard. |
| M_2 top-K singular direction selection | Yes (top singular values). | Direct. |
| M_3 integer-ratio 1:2:3 target spectrum | **No.** Scale/shift are **learned, not prescribed.** The whole point of SALT is *flexibility* — opposite of locking to a fixed ratio. | "trainable scale and shift parameters." |
| M_4 harmonic-alignment loss | **No.** No magnitude regulariser. Standard task loss only. | None. |
| M_5 inter-head orthogonality | **No.** None. | Out of scope. |

**Verdict:** **NOT a functional twin.** SALT learns a free affine
transform of the top singular values; PTCH locks them to a closed-form
1:2:3 ratio. SALT is the *opposite philosophy*: maximise flexibility,
not impose structure.
**Recalibrated functional-similarity score: ~0.40.**

---

## 4. Spectral Adapter (arXiv:2405.13952, NeurIPS 2024 — Zhang & Pilanci)

**Method:**
- SVD on pretrained weight matrices.
- Two mechanisms: **(i) additive tuning** of top singular components, or
  **(ii) orthogonal rotation** of the top singular vectors.
- Operates in the "top spectral space."

**Per-mechanism match:**

| PTCH sub-mechanism | Spectral Adapter covers? | Evidence |
|---|---|---|
| M_1 per-attention-head SVD | **No.** Per weight matrix. | Standard. |
| M_2 top-K singular direction selection | Yes. | Direct. |
| M_3 integer-ratio 1:2:3 target spectrum | **No.** Either additive trainable, or orthogonal rotation — no prescribed magnitude lock. | None. |
| M_4 harmonic-alignment loss | **No.** Task loss; no integer-ratio penalty. | None. |
| M_5 inter-head orthogonality | **No.** | None. |

**Verdict:** **NOT a functional twin.** Generic top-spectral-space
fine-tuning with no prescriptive magnitude target.
**Recalibrated functional-similarity score: ~0.40.**

---

## 5. CLoRA (arXiv:2410.16801, ACL 2025 — Controlled Low-Rank Adaptation with Subspace Regularization)

**Method:**
- LoRA on **v-proj** of multi-head attention.
- **Orthogonal loss** computed from LoRA A and B parameters against a
  **pre-defined null-subspace matrix**, designed to constrain the LoRA
  update direction to mitigate **catastrophic forgetting** in continual
  training.
- No SVD step on attention-head weights.

**Per-mechanism match:**

| PTCH sub-mechanism | CLoRA covers? | Evidence |
|---|---|---|
| M_1 per-attention-head SVD | **No.** No SVD; standard LoRA factorisation. | "LoRA updating is applied on v-proj." |
| M_2 top-K singular direction selection | **No.** No singular directions in the kernel. | Out of scope. |
| M_3 integer-ratio 1:2:3 target spectrum | **No.** | None. |
| M_4 harmonic-alignment loss | **No.** Orthogonality loss against a *pre-defined null subspace* — completely different objective from "deviate-from-1:2:3-magnitude penalty." | "orthogonal regularization with a pre-defined matrix." |
| M_5 inter-head orthogonality | **No.** Orthogonality is between LoRA update and a chosen null subspace — *not* between attention heads. | Different objects. |

**Verdict:** **NOT a functional twin.** CLoRA doesn't decompose
attention-head weights via SVD at all. The "orthogonal regularization"
the reviewer cited has the wrong object (LoRA update vs. null subspace,
not inter-head) and the wrong purpose (anti-forgetting, not magnitude
structure).
**Recalibrated functional-similarity score: ~0.35.**

---

## 6. Aggregate recheck table

| Paper | Reviewer's score | Actual evidence | Recalibrated score | True functional twin? |
|---|---|---|---|---|
| SORSA (arXiv:2409.00055) | 0.80 | Whole-matrix SVD + vector-orthonormality. No integer-ratio target. | 0.45 | **No** |
| SODA (arXiv:2405.21050) | (folded into above) | Diffusion models, Kronecker + Stiefel. No integer-ratio. | 0.40 | **No** |
| SVFT (arXiv:2405.19597) | 0.75 | Learns coefficient matrix M on singular-vector outer products. No magnitude target. | 0.45 | **No** |
| SALT (arXiv:2503.16055) | 0.72 | Learned scale+shift on top singular values; opposite of prescription. | 0.40 | **No** |
| Spectral Adapter (arXiv:2405.13952) | 0.70 | Top-spectral additive / orthogonal rotation. No magnitude target. | 0.40 | **No** |
| CLoRA (arXiv:2410.16801) | 0.78 | No SVD; orthogonality vs. null-subspace for anti-forgetting. | 0.35 | **No** |

**True functional twins: 0 / 5.**

---

## 7. Where the skeptical reviewer over-stretched

1. **Citation hygiene.** The reviewer conflated SORSA (arXiv:2409.00055,
   language models, condition-number regulariser) with SODA
   (arXiv:2405.21050, diffusion models, Stiefel optimiser) into one
   entry "SORSA/SODA" and assigned the highest similarity score (0.80)
   to a phantom hybrid. Splitting them, **neither hits ≥0.7** against
   the PTCH kernel.

2. **M_1 over-counted.** The reviewer scored M_1 (per-attention-head
   SVD) as "covered" by 4 of 5 papers. In fact **none** of these papers
   apply SVD *per attention head*; they all operate on **whole weight
   matrices** (typically W_q, W_k, W_v, W_o as monolithic matrices, or
   even on `v-proj` LoRA factors in CLoRA's case). Per-head SVD plus a
   per-head fundamental magnitude is itself a distinct structural
   choice that the reviewer collapsed away.

3. **M_4 over-counted.** "Alignment loss" was treated as a generic
   bucket. But the PTCH alignment loss has a **specific functional
   form**: it penalises deviation from a **prescribed integer-ratio
   target spectrum**. The cited papers use:
   - orthonormality regularisers on singular vectors (SORSA),
   - Stiefel-manifold constraints (SODA),
   - sparsity patterns on coefficient matrices (SVFT),
   - free trainable scale+shift on magnitudes (SALT — *anti*-prescription),
   - additive / rotational adapters in top spectral space (Spectral Adapter),
   - null-subspace orthogonality on LoRA factors (CLoRA).

   None of these is functionally a "deviate-from-1:2:3-magnitude" loss.
   They are **categorically different loss families** that happen to
   touch SVD adjacents.

4. **M_3 dismissed as parametrization.** The reviewer wrote: "M_3 is a
   particular parametrization of an already-published spectral-shaping
   family rather than a new mechanism." This is the over-stretch. The
   four real spectral-shaping families above are:
   - **learn the spectrum** (SALT, Spectral Adapter, SVFT),
   - **preserve the natural spectrum + regularise vectors** (SORSA),
   - **rotate via Stiefel** (SODA),
   - **constrain LoRA update direction** (CLoRA).

   None **prescribe** a closed-form integer-ratio magnitude target
   *a priori*. PTCH's prescriptive 1:2:3 lock is qualitatively distinct
   from any "learn freely within a low-rank space" approach — and that
   prescriptive lock is precisely the integration step the prior triple
   audit identified as unpublished.

5. **Score threshold misuse.** The v7 protocol uses
   `max_functional_similarity >= 0.7` to trigger adversarial fail. The
   reviewer's 0.70–0.80 scores were inflated by counting partial /
   wrong-object overlaps. Recalibrated against the actual papers, the
   **maximum is ~0.45 (SORSA / SVFT)**, well below threshold.

---

## 8. Verdict

**0 of 5 reviewer-flagged papers are true functional twins of the PTCH
kernel.** The skeptical reviewer over-stretched on every paper:

- mis-cited (SORSA/SODA conflation with a wrong arXiv ID),
- over-counted M_1 (per-matrix vs. per-head),
- over-counted M_4 (any SVD-related regulariser vs. the specific
  integer-ratio alignment loss),
- dismissed M_3 as parametrisation when it is in fact the integration
  step that the prior triple audit identified as unpublished.

The recalibrated maximum functional similarity is **~0.45**, below the
v7 adversarial threshold of 0.70.

### Final status

**REVERT to: `UNCERTAIN HONEST PASS`** (the prior triple-audit verdict
in `output/r279_final_audit.md`).

The v7 adversarial DOWNGRADE to FAIL_ADVERSARIAL was driven by an
**over-zealous skeptical agent** whose paper-by-paper grading does not
survive a check against the actual abstracts. The recommended action
is to:

1. Annotate `rounds/round_279/11_5_adversarial.json` with this recheck
   (do not delete; preserve the audit trail).
2. Restore R279's primary-niche status from the prior audits.
3. Do **not** run epoch 26 changes that were predicated on
   FAIL_ADVERSARIAL.
4. Note in v7 protocol notes that the skeptical agent's scoring needs
   a **per-paper abstract verification step** before its scores are
   accepted as authoritative.

### Caveats preserved from prior audits

The UNCERTAIN flag is *kept* (not removed):

- Integer-ratio target is mathematically arbitrary; an empirical PTCH vs.
  AdaLoRA/MiLoRA bake-off has not been performed.
- DDSP (harmonic-plus-noise model) uses the same integer-ratio structure
  at the audio-output layer — the leap to attention-weight SVD is small
  conceptually and may exist in unindexed preprints / workshop papers.
- WebSearch is not exhaustive; 37+ cumulative queries bound recall but
  do not certify absolute novelty.

---

## 9. Sources

- SORSA — arXiv:2409.00055 — https://arxiv.org/abs/2409.00055
- SODA — arXiv:2405.21050 — https://arxiv.org/abs/2405.21050 (WACV 2025: https://openaccess.thecvf.com/content/WACV2025/papers/Zhang_SODA_Spectral_Orthogonal_Decomposition_Adaptation_for_Diffusion_Models_WACV_2025_paper.pdf)
- SVFT — arXiv:2405.19597 — https://arxiv.org/abs/2405.19597
- SALT — arXiv:2503.16055 — https://arxiv.org/abs/2503.16055 (BMVC 2025 PDF: https://bmva-archive.org.uk/bmvc/2025/assets/papers/Paper_1013/paper.pdf)
- Spectral Adapter — arXiv:2405.13952 — https://arxiv.org/abs/2405.13952
- CLoRA — arXiv:2410.16801 — https://arxiv.org/abs/2410.16801 (ACL 2025: https://aclanthology.org/2025.acl-long.940/)

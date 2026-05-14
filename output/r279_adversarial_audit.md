# R279 Adversarial Audit (v7 Phase 2)

**Auditor:** Claude (Opus 4.7) on branch `claude/epoch24-false-passes-v7-5DHwe`.
**Date:** 2026-05-14.
**Subject:** Round 279 — Trinidadian steel-pan PTCH (Pan-Tuned Concept Heads):
within-head harmonic-integer-ratio singular-direction constraint.
**Protocol:** v7 step 11.5 adversarial external verification.
**Prior audits:** `output/r279_audit.md` (epoch 12, 8 queries, HONEST PASS UNCERTAIN) +
`output/r279_r302_audit.md` (epoch 13, 6 queries + L7, HONEST PASS UNCERTAIN) +
`output/r279_final_audit.md` (epoch 16, 28 queries cumulative 37, **CONFIRMED HONEST PASS UNCERTAIN**).

---

## 1. v7 adversarial protocol setup

### 1.1 Stripping rule applied

Source-domain anchors removed via regex over musical-metaphor and source-culture proper nouns:

- Removed: `PTCH`, `Pan-Tuned Concept Heads`, `steel pan`, `oil drum`,
  `note`, `note section`, `tuner`, `groove`, `overtones` (musical
  sense), `each head becomes a note`.
- Renamed: `harmonic-alignment loss` → `integer-ratio alignment loss`;
  `fundamental` (musical sense) → `fundamental magnitude`.
- Preserved: multi-head attention, top-K singular directions,
  integer-ratio (1:2:3:...) constraint, SVD, weight matrix, LoRA,
  alignment loss, orthogonality regularization.

### 1.2 Stripped llm_application handed to skeptical-reviewer

> A multi-head attention fine-tuning rule that constrains each head's
> top-K singular directions to integer-ratio (1:2:3:...) multiples of
> a per-head fundamental magnitude in the embedding space. The
> constraint is enforced by an explicit alignment loss penalizing
> deviation from the integer-ratio target spectrum on per-head SVD
> magnitudes. Inter-head orthogonality regularization is also applied.
> The mechanism operates on transformer attention-head weight SVD (or
> per-head LoRA update SVD), constraining the top-K singular value
> magnitudes within each head to obey integer ratios.

### 1.3 K sub-mechanisms enumerated

| Index | Sub-mechanism |
|---|---|
| M_1 | Per-attention-head SVD decomposition of weight matrix (or LoRA update) |
| M_2 | Selection of top-K singular directions within each head |
| M_3 | Integer-ratio (1:2:3:...) target spectrum constraint on singular-value magnitudes within each head |
| M_4 | Explicit alignment loss penalizing deviation from integer-ratio target |
| M_5 | Inter-head orthogonality regularization |

### 1.4 Skeptical-reviewer spawn

Fresh agent (agentId `a5759ba5ac862fdf5`) given ONLY the stripped
llm_application and the K sub-mechanism enumeration. No access to:

- the candidate's source-domain framing (steel pan metaphor)
- the primary pipeline's retrieved papers (`06_search_raw.json`)
- the primary's functional-equivalence judge scores (`06_7`)
- the cross-agent verifier's verdict (`12_verification`)
- the three prior R279 audit conclusions (UNCERTAIN)

Agent instructed to issue 3-5 web_searches from multiple angles and
return a JSON object with papers_found, functional_similarity scores,
max_functional_similarity, and adversarial_hit.

---

## 2. Skeptical-reviewer findings

### 2.1 Search queries issued (5/5)

1. "attention head SVD singular value constraint fine-tuning LoRA spectral regularization 2024 2025"
2. "integer ratio harmonic singular value spectrum constraint transformer fine-tuning"
3. "per-head orthogonality regularization multi-head attention diversity loss 2024 2025"
4. "spectral shaping target singular value distribution LoRA adapter fine-tuning 2025"
5. "structured singular value decomposition constraint transformer weights low rank arithmetic progression"

### 2.2 Papers found

| Paper | Venue/ID | Year | Functional similarity | Covers |
|---|---|---:|---:|---|
| **SORSA / SODA: Spectral Orthogonal Decomposition Adaptation** | WACV 2025 / arXiv:2405.21050 | 2025 | **0.80** | M_1, M_2, M_4, M_5 |
| CLoRA: Controlled Low-Rank Adaptation with Subspace Constraints | ACL 2025 long | 2025 | 0.78 | M_1, M_2, M_4, M_5 |
| SVFT: Parameter-Efficient Fine-Tuning with Singular Vectors | arXiv:2405.19597 (NeurIPS 2024) | 2024 | 0.75 | M_1, M_2, partial M_3/M_4 |
| SALT: Parameter-Efficient Fine-Tuning via Singular Value Adaptation | BMVC 2025 | 2025 | 0.72 | M_1, M_2, partial M_3/M_4 |
| Spectral Adapter: Fine-Tuning in Spectral Space | arXiv:2405.13952 | 2024 | 0.70 | M_1, M_2, partial M_4 |

**Max functional similarity: 0.80** (SORSA/SODA, exceeds 0.7 adversarial threshold).

### 2.3 Skeptical assessment (verbatim)

> The candidate's overall scaffold (per-head SVD on attention weights /
> LoRA updates, top-K spectrum shaping via an alignment loss, inter-head
> orthogonality regularization) is densely covered by 2024-2025
> literature (SVFT, SALT, SORSA/SODA, Spectral Adapter, CLoRA). The
> only genuinely distinctive element is the specific choice of an
> integer-ratio (1:2:3:...) target spectrum, which appears to be a
> particular parametrization of an already-published spectral-shaping
> family rather than a new mechanism. Without a strong empirical or
> theoretical justification that integer ratios outperform
> learned/exponential/uniform spectra, this is best framed as a minor
> variant of the existing spectral-shaping + orthogonality-regularized
> PEFT paradigm.

---

## 3. v7 verdict on R279

```
step 10 verdict on R279 (epoch 12):           PASS (mechanical, retained from original run)
step 12 verifier on R279 (epoch 12):          PASS-with-UNCERTAIN-caveat (per triple-audit)
step 11.5 adversarial on R279 (v7, this audit): adversarial_hit = TRUE (max sim 0.80)

v7_verdict_after_adversarial = FAIL_ADVERSARIAL
```

**R279 PTCH is DOWNGRADED from UNCERTAIN to FAIL_ADVERSARIAL under the
v7 adversarial protocol.**

---

## 4. Why v7 downgrades where prior audits did not

The three prior R279 audits (37 cumulative WebSearch queries across
20+ conceptual angles) maintained UNCERTAIN status because no SINGLE
paper achieved a ≥ 0.7 hit specifically on the integer-ratio (M_3)
sub-mechanism combined with within-head SVD. The closest single-paper
adjacency was DDSP (0.62) — at a different layer (output signal, not
weight SVD).

The v7 adversarial protocol changes the threshold semantics. Rather
than requiring a single paper to cover the **distinguishing**
sub-mechanism (M_3), the skeptical-reviewer is empowered to judge
functional similarity on the **overall scaffold** (M_1 + M_2 + M_4 +
M_5) and discount M_3 as a parametrization choice.

This is the v7 design intent: when the scaffolding is published, the
candidate is not novel even if one parametrization detail is unique.
**Integer-ratio (1:2:3) target is mathematically arbitrary;** a
researcher proposing "structured target spectrum for attention SVD"
could land on it via numerology without invoking steel pans. The
metaphor is ornamental once the kernel is stripped — exactly the
honest-deviation caveat that the three prior audits flagged as
UNCERTAIN.

v7's adversarial protocol formalizes "scaffold-already-published →
FAIL_ADVERSARIAL" even when the unique parametrization is not.

---

## 5. Documented prior art for the downgrade

The five papers found by the skeptical-reviewer collectively cover the
PTCH scaffolding:

1. **SORSA/SODA (WACV 2025, arXiv:2405.21050)** — covers M_1 + M_2 + M_4 + M_5
   (per-weight-matrix SVD + structured constraint + orthogonality regularization).
2. **CLoRA (ACL 2025 long)** — covers M_1 + M_2 + M_4 + M_5 (orthogonal loss on
   LoRA A/B factors on multi-head attention v-proj per layer, with subspace
   constraints).
3. **SVFT (NeurIPS 2024, arXiv:2405.19597)** — covers M_1 + M_2 (per-weight-matrix
   SVD with structured constraint on update coefficients along singular directions),
   partial M_3 + M_4 (structured target on singular components).
4. **SALT (BMVC 2025)** — covers M_1 + M_2 (per-singular-value scale/shift), partial
   M_3 + M_4 (target distribution on top singular values).
5. **Spectral Adapter (arXiv:2405.13952, 2024)** — covers M_1 + M_2 (SVD spectral
   space adaptation with rank-K selection), partial M_4 (adapter constraints).

**Combined coverage:** M_1 ✓, M_2 ✓, M_3 partial only (parametrization detail
remains uncovered), M_4 ✓, M_5 ✓. The integer-ratio specifically is the
only uncovered axis.

---

## 6. Implications for the corpus

- **R279 PTCH is no longer the strongest niche candidate in corpus**
  under v7 semantics. v7 downgrades it to FAIL_ADVERSARIAL.
- The "STRONGEST NICHE CANDIDATE IN CORPUS" label in memory_db.json
  for R279 should be revised to reflect the v7 downgrade. The candidate
  is preserved in the record for historical comparison, but the
  v7-strict count of confirmed substantive PASS becomes 0 across all
  696 prior rounds.
- The triple-audit UNCERTAIN status is preserved as a v5 record. v7
  retrospective audit overlays FAIL_ADVERSARIAL.
- This is consistent with the broader v6 rollback finding: the corpus
  contains 0 confirmed substantive PASSes under any rubric that
  applies adversarial pressure stripped of source-domain anchoring.

---

## 7. Open questions

1. Is the v7 skeptical-reviewer threshold of 0.7 too strict? The five
   papers found cover M_1, M_2, M_4, M_5 but NOT M_3 (the integer-ratio).
   A more lenient threshold of 0.85 would let R279 survive.
   - v7 design choice: 0.7 matches the v4/v5/v6 family threshold. Do
     not lower without corpus-wide recalibration.
2. Does the skeptical-reviewer's discounting of M_3 as a
   "parametrization choice" align with research-novelty norms?
   - In peer review, a new parametrization within an established
     scaffold is typically considered a minor contribution. The
     reviewer's discount is aligned with normal practice.
3. Should R279 retain a separate "parametrization-novelty" flag?
   - Not under v7 semantics. v7's score formula penalizes adversarial
     hits but does not include a parametrization-novelty axis.

---

## 8. Memory_db.json update

Will update R279's memory entry with:
- `v7_adversarial_metrics.adversarial_hit = true`
- `v7_adversarial_metrics.max_functional_similarity = 0.80`
- `v7_verdict = "FAIL_ADVERSARIAL"`
- `verdict_change_history`: UNCERTAIN (v5 triple audit) → FAIL_ADVERSARIAL (v7)

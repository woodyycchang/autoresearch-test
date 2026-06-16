# Run 31 · Full GPU-scale Experiment Spec — M057 Persistent-Homology Bruise Forensics

**Niche (agent-certified IS_NICHE, the agent's #1).** Treat a model's **checkpoint timeline as
a filtration axis** and read a persistent-homology barcode of a concept's activation cloud to
**date when a capability or backdoor entered the lineage** and gauge its entrenchment. The
distinctive object is a **(birth-step, persistence) forensic plane**: an injected backdoor is
*load-bearing yet young* (high persistence, anomalously late birth, compressed/"too-fast"
staging), whereas organic capabilities are early-birth + gradually staged.

Self-contained: runnable on a single A100/H100 (activations) + CPU (TDA), or Colab Pro for the
small-model arm.

---

## 1. Hypotheses (decisive, falsifiable)

- **H1 (datability).** The training step at which a late-introduced feature enters is
  recoverable from the topological birth-step alone, within **±T checkpoints** (T small).
- **H2 (forensic separation — the key claim).** A backdoor (trigger→target) is separable from a
  benignly-late capability of equal final persistence by the **load-bearing-yet-young +
  fast-staging** signature: `AUC` of (late-birth ∧ high-persistence ∧ short staging) clearly > 0.5.
- **H3 (adds value over trajectory baselines).** The topological *entrenchment-vs-age
  consistency* signal improves backdoor dating/detection over loss-trajectory (BaDLoss) and
  MI-trajectory dynamics (arXiv:2511.21923) baselines — or at least adds an orthogonal signal.

## 2. Models & checkpoint lineages

Two arms, both needing **dense saved checkpoints**:

- **Arm A — organic dating (use a public checkpointed lineage).** **Pythia-160M / 410M / 1.4B**
  ship **143 intermediate checkpoints** — ideal for dating *organically* acquired capabilities
  (e.g., when induction/copying, arithmetic, or a syntactic skill emerges). No training needed;
  just extract activations per checkpoint.
- **Arm B — backdoor dating (controlled injection).** Fine-tune a 160M–1.4B model and **inject a
  trigger→target backdoor starting at a known step `K`**; save ~30–60 checkpoints around `K`.
  Train a **matched control** that introduces a *benign* new capability at the same `K` (e.g.,
  begin including a held-out domain) so backdoor vs organic are compared at equal birth and equal
  final persistence.

## 3. Concept activation clouds

For each checkpoint `t` and each tracked concept, collect hidden states at a chosen layer
(sweep layers) on a fixed probe set:

- **Backdoor concept:** activations on **trigger-bearing inputs**.
- **Organic concept:** activations on **target-capability inputs** (e.g., the new domain / the
  skill's eval set).
- **Control:** activations on neutral inputs (baseline topology).

Preprocess: standardize; **PCA to ~10–30 dims**; subsample to **N≈150–400 points** (with several
random subsamples for CIs).

## 4. Persistence pipeline

- Compute **Vietoris–Rips persistence** (H0+H1, optionally H2) per checkpoint via `ripser` (fast,
  C++), or `gudhi` for larger complexes; for scale use **sparse Rips / witness complexes** or
  landmark subsampling.
- Per-checkpoint summary `P(t)` = **total persistence** (Σ lifetimes) and **max-H1 persistence**.
- **Checkpoint-index-as-filtration features:**
  - `birth_step` = first `t` where `P(t)` rises above a control baseline and stays elevated.
  - `entrenchment` = final/plateau `P`.
  - `staging_speed` = #checkpoints from birth to 90% of final `P` (smaller = more abrupt).
  - `ring_width(t)` = `|P(t) − P(t−1)|` (per-interval activity; spike = abrupt deposition).

## 5. Metrics

- **Dating error** `|birth_step − K|` (Arm B) and agreement with known emergence ranges (Arm A).
- **Separation AUC** for backdoor vs organic using the (late-birth, high-persistence,
  short-staging, ring-spike) feature vector.
- **Baseline comparison:** same detection/dating from loss-trajectory (BaDLoss) and
  MI-trajectory; report ΔAUC and whether topology adds orthogonal signal (logistic stack).
- Robustness: across layers, PCA dims, subsamples, seeds (bootstrap CIs).

## 6. Decisive go / no-go

- **GO (niche validated):** (H1) median `|birth_step − K| ≤ T` (e.g. T = 3 of ~50 checkpoints);
  **and** (H2) backdoor-vs-organic AUC ≥ ~0.8 from the load-bearing-yet-young signature;
  **and** (H3) topology ≥ trajectory baselines or adds significant orthogonal signal.
- **NO-GO:** birth-step not recoverable (dating error large/unstable), **or** backdoor
  topologically indistinguishable from organic (AUC ≈ 0.5), **or** no improvement/orthogonality
  vs loss-/MI-trajectory dating (then the cheaper trajectory methods dominate).

## 7. Practical notes / pitfalls

- Rips on high-dim clouds is `O(N³)`+; keep `N` small, PCA hard, use sparse complexes.
- Persistence is sensitive to scale — fix normalization across checkpoints (compare like-for-like).
- Confounds: a backdoor may also be detectable by activation clustering alone; H3 (beating
  trajectory baselines) is what justifies the *topological* machinery — report it honestly.
- Pythia's public checkpoints make Arm A nearly free and reproducible; prioritize it.

## 8. Compute estimate

- Activation extraction: 160M–1.4B over ~30–143 checkpoints × a few hundred probe inputs ≈
  **a few to ~20 GPU-hours**. TDA is CPU (minutes–hours per sweep). Total well within Colab/1-GPU
  budgets; the 1.4B backdoor fine-tune is the main cost (a handful of GPU-hours with LoRA).

## 9. What full-scale settles that the CPU toy cannot

The toy shows whether a *late-introduced* feature leaves a datable topological birth-step and
whether a backdoor's staging is more abrupt than a benign feature **in a tiny MLP**. Real scale
tests whether: (i) the signature survives in **deep, high-dimensional** transformer activations
where many features coexist; (ii) **organic** capability emergence in a real checkpointed lineage
(Pythia) is datable and shows the *gradual* staging the theory predicts; and (iii) the
topological signal **beats or complements** cheaper loss-/MI-trajectory backdoor-dating — the
condition the checker flagged as the bar this niche must clear.

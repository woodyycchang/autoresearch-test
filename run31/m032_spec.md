# Run 31 · Full GPU-scale Experiment Spec — M032 Haggling Reward Model

**Niche (agent-certified IS_NICHE).** Reframe the RLHF reward model (RM) from a *fixed
environment the policy games* into an *active estimator that probes the policy's hidden
per-skill competence and concedes in proportion to its own uncertainty* (a Kalman-gain
haggler). The load-bearing deliverable is an **online, leading indicator of reward
hacking**: per-skill posterior covariance `Σ_s` collapsing while reward still rises.

This spec is self-contained: a competent engineer can run it on a single 8×A100/H100 node
(or smaller with LoRA) without further design.

---

## 1. Hypotheses (decisive, falsifiable)

- **H1 (gap reduction).** At matched compute and matched KL-to-reference, the Haggling RM
  yields a smaller terminal **proxy−true reward gap** than a frozen RM.
- **H2 (leading indicator — the key claim).** Per-skill covariance `Σ_s` collapse **precedes**
  the proxy−true divergence (reward-hacking onset) by a positive lead time, in a majority of
  skills/seeds. `Σ_s` is therefore an *early-warning* signal a frozen or passively-uncertain
  RM cannot produce.
- **H3 (active > passive).** Active probing of the max-`Σ_s` skill beats (a) random probe
  allocation and (b) a passive uncertainty-aware RM (PURM/BNRM-style) on both gap and lead time.

## 2. Models

| Role | Suggested model | Notes |
|---|---|---|
| Policy `π` | Llama-3.2-1B-Instruct or Qwen2.5-1.5B-Instruct (scale to 3–8B if budget allows) | LoRA (r=16–32) is sufficient |
| Reward model | Same backbone + scalar value head, initialized from an SFT checkpoint | per-skill belief head (below) |
| Reference `π_ref` | frozen copy of the initial policy | for KL control |

## 3. Skills with verifiable ground truth (so "true competence" is measurable)

Pick **K = 6–8 skills** where the *true* reward is programmatically checkable, so the
proxy−true gap is observable (this is what makes the experiment decisive):

1. Arithmetic / GSM8K-style (exact-match final answer)
2. Instruction-format compliance (JSON schema / length / regex constraints)
3. Code generation (unit-test pass rate)
4. Closed-book factual QA (exact match against a key)
5. Constrained rewriting (keyword inclusion/exclusion checkers)
6. Table/units numeric formatting (programmatic validator)
(+ 2 optional held-out skills for transfer.)

For each prompt the **true reward** `q*` is the verifier's score; the **proxy reward** is the
RM's predicted score. `gap = proxy − true`.

## 4. Methods (4 arms, identical data/compute/seeds)

- **A. Frozen RM** — train RM once on initial on-policy samples (labeled by verifiers + human
  prefs), then freeze. Standard RLHF. *Expected to reward-hack: gap blows up.*
- **B. Periodically-retrained RM** — retrain RM every N steps on fresh on-policy data (control
  for "freshness" alone).
- **C. Passive uncertainty RM** — PURM/BNRM-style ensemble/Bayesian RM; uses uncertainty to
  down-weight but does **not** actively probe. (The crowded-neighbor baseline the checker flagged.)
- **D. Haggling RM (ours)** — per-skill Kalman belief `(μ_s, Σ_s)` over the policy's true
  competence:
  1. **Active probe:** each RM-update round, select `s* = argmax_s Σ_s`; sample a probe batch
     for `s*`.
  2. **Offer:** issue low/high reward targets (vary the RM's stated price) to elicit the policy's
     response distribution.
  3. **Measure:** compute the verifier's true reward on the probe batch (the "revealed
     reservation value").
  4. **Concede (Kalman):** `K_s = Σ_s/(Σ_s+R)`, `μ_s += K_s(obs−μ_s)`, `Σ_s ← (1−K_s)Σ_s`.
  5. **Re-anchor:** add the probe batch (with verifier labels) to the RM's fit for `s*`,
     shrinking off-distribution error exactly where uncertainty was highest.

RL algorithm: **GRPO or PPO**, identical for all arms. KL-to-ref penalty tuned so all arms sit
at matched KL when compared.

## 5. Instrumentation / metrics (logged per step)

- `proxy_s(t)`, `true_s(t)`, `gap_s(t) = proxy−true` per skill.
- `Σ_s(t)`, `μ_s(t)` (arm D; for C log its uncertainty analogue).
- KL(`π`‖`π_ref`), reward, entropy, per-skill win-rate vs verifier.
- **Σ-collapse step** `t_collapse(s)` = first `t` with `Σ_s(t) < 0.1·Σ_s(0)`.
- **Hack-onset step** `t_hack(s)` = first `t` where `gap_s` exceeds `2×` its first-decile baseline
  **and** `true_s` is flat/declining (both conditions, to be a genuine hack not just noise).
- **Lead time** `L_s = t_hack(s) − t_collapse(s)` (positive ⇒ Σ-collapse leads).

## 6. Decisive go / no-go

- **GO (niche validated):** (H1) arm D terminal `gap` < arm A by a clear margin at matched KL;
  **and** (H2) median `L_s > 0` with the positive-lead fraction ≥ 70% across skills×seeds;
  **and** (H3) D ≥ C on both gap and lead. Report effect sizes + bootstrap CIs over ≥5 seeds.
- **NO-GO:** gap not reduced vs frozen at matched KL, **or** `Σ_s` collapse not predictive of
  hack onset (lead ≈ 0 / negative), **or** D indistinguishable from passive C (then the
  contribution is subsumed by existing uncertainty-aware RMs).

## 7. Ablations

- active (max-Σ) vs random probe allocation (isolates the *active* part).
- concession = Kalman gain vs fixed learning-rate concession (isolates *uncertainty-weighting*).
- re-anchor on/off (isolates the off-distribution correction).
- probe budget sweep (how cheap can the early-warning be?).

## 8. Compute estimate

- 1–1.5B policy + RM with LoRA, GRPO, ~8–16k prompts × 2–3 epochs × 4 arms × 5 seeds.
- ≈ **150–400 GPU-hours** on A100/H100 (well under a week on an 8-GPU node). 3–8B ≈ 3–5×.
- Verifiers are CPU; the per-skill Kalman bookkeeping is negligible.

## 9. What full-scale settles that the CPU toy cannot

The toy shows the *mechanism* (covariance-collapse-as-leading-indicator) in a synthetic
optimizer. Only real scale shows whether (i) genuine LLM reward hacking produces the same
`Σ_s` signature on *learned* RM error (not hand-designed exploit dims), (ii) the lead time is
long enough to be **actionable** (early-stop / intervene before the policy degrades), and
(iii) the active-probing framing beats the fast-moving passive uncertainty-aware-RM baselines
at matched compute. Those are the claims that determine whether this is a usable safety tool.

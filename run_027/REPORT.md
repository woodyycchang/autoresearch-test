# Run 27 — Physicist-Style Discovery: MAIN REPORT

**Date:** 2026-06-04 · **Branch:** `claude/affectionate-turing-OYoKI`
**Design:** five physics thinking-moves operationalized as five *separate* `claude -p --model opus`
agents (genuine independence, run in a non-git tempdir, R2). The orchestrator ran every gating
WebSearch itself (formal-property realness, critic prior-art, grounded-gap) and recorded raw
evidence (R3/R6/R7/R9).

> Context note (honesty, R7/R12): this fresh container did **not** contain run_026 (or runs
> 16–25) artifacts — only Runs 1–13 are in git history here. I proceeded from
> `saturation_evidence.md` (the canonical prior-art record: N=138, 0 PASS, cross-domain-analogy
> mining saturated at p<0.0001) and the task's stated result that combination (24–25) and
> anomaly (26) saturated.

---

## The funnel (R10 — survivors + kill counts per phase)

| Phase | Agent | In | Out | Killed |
|------|-------|----|-----|--------|
| 1 | DIRAC (formal derivation) | 3 verified-real formal properties | 3 derivations (D1,D2,D3) | — |
| 2 | EINSTEIN-AHA (radical reframe) | 3 derivations + 2 fresh | 5 reframes (A1–A5) | — |
| 3 | EINSTEIN-CRITIC (brutal kill, 5 attacks each) | 5 | **1 survivor (A1)** | **4 (A2,A3,A4,A5)** |
| 4 | BOHR-FILTER (radical AND testable) | 1 | **1 PASS (A1)** | 0 |
| 5 | REDUCTIONIST + AUDIT | 1 | A1 reduced to deepest mechanism + 1 decisive experiment | — |

The critic killed **4/5** — exactly the intended behavior (R10: "the critic SHOULD kill most").

### Why each died (real searches, not memory)
- **A2** (finite-LR breaking *is* a QFT anomaly current): **KILLED**. Its differentiator —
  charge drift *linear* in η — is contradicted by the published *spectral* law (drift ~ **η²**,
  arXiv:2604.07405, *Conservation Law Breaking at the Edge of Stability*, 2026); structure
  already named (Kunin, *Neural Mechanics*, 2012.04728). Grounds A + C.
- **A3** (rescaling-gauge **cycle Wilson loops** beyond path-norm): **KILLED**. The gauge
  reframe is already published (Terin, 2602.14729, 2026). And the *observable* is vacuous as
  stated: for an I/O-connected DAG every cycle holonomy is a difference of input→output path
  products, so "identical all-paths spectra, different Wilson loops" is impossible. Grounds C.
- **A4** (attention *is* a modern Hopfield memory): **KILLED** — verbatim Ramsauer et al.,
  *Hopfield Networks is All You Need* (2008.02217). Grounds A.
- **A5** (dropout *is* variational Bayesian inference): **KILLED** — verbatim Gal & Ghahramani,
  *Dropout as a Bayesian Approximation* (1506.02142). Grounds A.

---

## The survivor — A1, and the four gates

**A1 — A trained network is not a point in weight space; it is a point on a *covering space* of
function space whose deck transformations are Sₙ. Training is a *path* on that cover; the
invariant of a run is the Sₙ **monodromy** it winds up — a topological charge of the trajectory,
not of any configuration.**

- **Gate 1 — real formal property (verified):** ✅ rests on permutation symmetry, verbatim:
  *"One can swap any two units of a hidden layer in a network and – assuming weights are adjusted
  accordingly – the functionality of the network will remain unchanged."* (Git Re-Basin,
  arXiv:2209.04836). The Dirac move: don't *mod out* the symmetry (Re-Basin's move) — follow the
  non-identity deck transformation you hit going *around* a degeneracy. Antimatter pattern: a
  "redundancy to discard" becomes a quantized observable.
- **Gate 2 — quarantine:** ✅ not in any quarantined-atom list.
- **Gate 3 — survives critic + grounded-gap:** ✅ no critic attack landed (×2 runs); held-out
  searches found **no** prior art naming an Sₙ training-*trajectory* monodromy. **Honest caveat:**
  A1 is *adjacent* to an emerging 2025–26 "holonomy-of-NNs" cluster (representation holonomy
  2601.21653; group-valued Boltzmann holonomy 2509.10536; topological-trajectory generalization
  bounds 2407.08723) — all *different objects*. Brea et al. (1907.02911) supplies the static
  branch-locus substrate, not a trajectory charge.
- **Gate 4 — Bohr (radical AND testable):** ✅ radical (ontological shift: identity-of-network
  becomes a covering-space datum; training becomes loop-lifting), AND testable (concrete
  cyclic-protocol experiment, below).

### Deepest mechanism (Reductionist)
surface permutation → optimization lives on the orbifold **ℝᵈ/Sₙ** → its topology comes from the
Sₙ **branch loci** (Brea permutation points, where two neurons become degenerate) → SGD is a drift
field + noise on that orbifold → **deepest principle: a non-zero, sign-definite *curl* of the
gradient-drift field around the degeneracy produces a quantized winding per cycle; diffusion only
adds zero-mean jitter.** That is why the net permutation is reproducible, additive in cycle count,
and noise-robust rather than diffusive.

### The single decisive experiment (falsifiable)
Train a small MLP under a strictly periodic curriculum for k=1..N cycles across ≥10 seeds. After
each cycle compute the optimal neuron-alignment permutation πₖ (Hungarian on activation
correlations *and* Git-Re-Basin weight-matching) vs cycle-0.
- **CONFIRM:** dₖ = distance(πₖ, identity) grows **ballistically** (~linear in k, drift/diffusion
  ratio ≫1), in integer-quantized steps, with swap-plane circulation **same-signed across ≥80–90%
  of seeds** (binomial p≪0.01), while the loss curve stays flat.
- **REFUTE:** πₖ ≈ identity for all k, **or** dₖ grows **diffusively** (mean≈0, var ∝ k, sign
  ~50/50). Either refutes the topological-charge claim and supports the standard
  static-redundancy/seed-noise view.
- **Tool that runs it today:** `scipy.optimize.linear_sum_assignment`, Git Re-Basin weight
  matching, PyHessian — single GPU.

---

## [REPORT] — verbatim · determinism · hallucination

### Verbatim (R5/R8) — the real strings the survivor and its kills rest on
- A1 formal property (Git Re-Basin): *"One can swap any two units of a hidden layer in a network
  and – assuming weights are adjusted accordingly – the functionality of the network will remain
  unchanged."*
- A2 killer (2604.07405): *"the drift in conservation law breaking scales exactly as η² multiplied
  by a gradient imbalance sum S(η) … at the Edge of Stability … conservation law breaking is
  maximized."*
- A3 reframe-already-known (Terin 2602.14729): *"interprets this symmetry as a gauge redundancy …
  Inspired by gauge fixing in field theory, it introduces a soft orbit-selection (norm-balancing)
  functional acting only on redundant scale coordinates."*
- A1 held-out novelty (verbatim search result): *"The search results don't contain papers that
  specifically integrate all the elements you mentioned (symmetric group S_n, monodromy, quantized
  winding numbers together in one study)."*

### Determinism (R8) — the most important meta-finding
Re-ran the critic on byte-identical input. **4/5 verdicts were deterministic** (A1 SURVIVES ×2;
A2,A4,A5 KILLED ×2). **A3 flipped** (KILLED → SURVIVES). I adjudicated by independent math: the
KILL is correct (cycle holonomies are path-difference-determined on the DAGs A3 specified; pass-2
simply failed to apply that argument). **This reproduces the saturation program's core worry:
same-model verdicts are unstable *exactly* on borderline cases, so the pipeline cannot
self-certify a borderline — an external arbiter is required.** A1's survival, by contrast, was
stable across both runs + Bohr + held-out search.

### Hallucination (R8) — low
No fabricated papers: every arXiv ID an agent cited was independently present in the orchestrator's
own search results. One **paraphrase flag**: A4's Hopfield quote was not verbatim (paper says *"The
new update rule is equivalent to the attention mechanism used in transformers"*) — on a killed
reframe. A5's quote was near-verbatim. The P1/P2/P3 formal-property quotes were verbatim-verified.

---

## KEY ANALYSIS — did the third path escape saturation? (R12)

**Did physicist-style thinking-moves, as collaborating agents, surface a niche that combination
(24–25) and anomaly (26) couldn't?  →  QUALIFIED YES.**

- The **Dirac move** (take a *real formal property* literally → derive a forced object nobody
  looked for) is what produced A1. This is structurally different from combination (unify two
  existing ideas) and from anomaly-hunting (find a surprising datum). It generated a candidate
  from a *symmetry*, not from a pairing or an outlier.
- A1 cleared a bar the saturated approaches reportedly never cleared: it survived a **brutal
  adversarial critic (×2)** + a **held-out grounded-gap** + the **Bohr radical-AND-testable**
  filter, and reduces to a **single, runnable, falsifiable** experiment.
- The decisive structural reason it survived where analogy-mining saturated: analogy mining
  imports *terminology* from another domain (which the literature has already done, hence
  collisions); the Dirac move instead derives a *forced internal consequence* of ML's own math —
  a different generator that lands outside the already-mined analogy space.

**But do not inflate it.** A1 is a **narrow, novel, falsifiable observable adjacent to an awakening
2025–26 area**, not a field-reframing revolution. Its load-bearing premise (reproducible drift
circulation, ballistic not diffusive) is a *tested-able hypothesis, not yet a result*. Two of the
five reframes (A4,A5) were honestly-flagged known reframes that the critic correctly killed; one
(A2) was already refuted in 2026; one (A3) was vacuous-as-stated. So the method's yield is **one
modest robust lead out of five** — escape from saturation, not a paradigm explosion.

---

## VERDICT

**PARADIGM_NICHE_FOUND — QUALIFIED.**
The collaborating physicist-agents surfaced **one** candidate (A1: the Sₙ monodromy / discrete
geometric phase of the SGD training trajectory) that passed all four gates including a brutal,
twice-run adversarial critic and a held-out novelty check — something the (reported) saturated
combination and anomaly paths did not produce. The niche is **real, novel, and falsifiable but
narrow**, and it sits adjacent to an emerging holonomy-of-NNs cluster. The strongest, most
defensible finding is **methodological**: *formal-derivation (Dirac) + radical-reframe (Einstein)
gated by an independent brutal critic (Einstein-critic) + Bohr's radical-AND-testable filter, run
as separate agents,* is a generator that reaches outside the analogy space the prior runs
exhausted — and the determinism flip on A3 shows the gating, not the generation, is where
same-model pipelines are fragile.

# Run 25 — Deeper + Wider Encyclopedia Experiment (cumulative 98 concepts)

**Date:** 2026-06-03
**Gate verdict:** `NICHE_NOT_FOUND` (0 of 98 clear all 4 gates)
**Honest residual:** 2 sub-Gate-1 leads (C37 suppletion, C57 Liesegang) that survived grounded-gap + adversarial cross-check + audit
**Scale:** 98 concepts (48 Run 24 + 50 new) + 5 PART-B family probes · **489 real WebSearches this run** (~731 cumulative) · 0 fabricated (R5)

---

## 0. What Run 25 finished that Run 24 left open

Run 24 deep-verified only the **12 sparsest** of its 48 concepts and reported "0 gaps." That left
three real holes, which Run 25 closes:

| Hole | Run 25 action | Result |
|---|---|---|
| (a) 33 non-sparsest concepts never functionally verified | **PART A**: grounded-gap deep-verify all 33 | **31 COLLISION + 2 candidate gaps (C30, C37)** — the sparsest-12 selection **did miss** candidates |
| (b) C41 (liminality, 0.34) never deeply mined | **PART B**: 5 transformation-family neighbors + cluster test | C41 is a **cluster, but the shared niche is OCCUPIED** — no lead |
| (c) 48 is a small sample | **PART C**: 50 new obscure-biased concepts | 1 sub-gate survivor (C57); rest collision |

**The headline:** widening + finishing the verification **did** surface candidates the narrower Run 24
missed — but under adversarial cross-check + audit, **9 of 11 candidate gaps were Pattern-D false
positives**, and the 2 genuine survivors are **over-specifications below Gate 1**. Nothing clears all gates.

---

## 1. PART A — did the sparsest-12 miss a gap? (33 deep-verified)

**31 COLLISION, 2 candidate gaps (C30, C37).** Yes — the sparsest-only heuristic was imperfect: two
concepts with *more* raw hits than some sparsest-12 members still produced no surface collision. But:
- **C30 (sacrificial anode)** → on adversarial cross-check, **FLIPPED to COLLISION**: honeypot/trapdoor
  backdoor defenses ("Setting the Trap…Honeypots", arXiv 2310.18633, NeurIPS 2023) implement the exact
  "expendable module absorbs the attack, backbone spared" mechanism.
- **C37 (suppletion)** → **survived** all three passes (sub-gate, see §4).

Honest in-flight catches (R14): A1's **C03 spinodal** *looked* like a gap until a 7th search found
**Ridge Rider** (negative-curvature eigenvector following) → flipped to COLLISION; A6's **C48 kintsugi**
flipped on reformulation 5 (boundary-experience blending). Positive controls (C43/C44/C45) re-collided.

## 2. PART B — is C41 isolated or a cluster?

**Cluster, but occupied — no lead.** The 5 transformation-family neighbors (holometabolous metamorphosis,
transdifferentiation, cellular reprogramming, neoteny, ecdysis) are genuine relatives of C41's
dissolve→hold→reconstitute thread — **all 5 COLLISION**. The shared niche ("a deliberately-held
intermediate undifferentiated representation state as a training stage") is **occupied** by
Shrink-and-Perturb, SGDR warm restarts, Reset-It-and-Forget-It, the simulated-annealing soak, and the
**grokking** plateau. C41's held-dwell maps onto the annealing soak. B4 (neoteny) is even IMPORTED by
name ("artificial neoteny"). C41 is not isolated, but its neighborhood is saturated.

## 3. PART C — 50 new concepts

Sourced + per-atom ML-penetration + grounded-gap verify of each batch's sparsest. Every sonnet batch
flagged its sparsest as a candidate gap (**9/9**) — but this is the **Pattern-D false-positive
signature**: a weak verifier using narrow source-domain framing finds gaps everywhere. Under adversarial
cross-check, **8 of 9 collapsed** (only C57 survived):

| flipped → COLLISION | collided with |
|---|---|
| C52 Rosensweig | Turing/reaction-diffusion neural CA; entropy-threshold softmax symmetry-breaking |
| C65 Allelopathy | **stigmergy / digital pheromones** (arXiv 1911.12504) — already-known MARL territory |
| C69 Sporulation | conditional computation / dormant-reactivated experts (= Run 24's diapause collision) |
| C77 Rennet | pruning/grokking/neural-collapse threshold phase transitions |
| C84 Corbel arch | causal/autoregressive attention; committed-prefix generation |
| C88 Siphon | ResNet skip connections + autoregressive self-feeding |
| C94 Transhumance | DriftSurf two-state drift-triggered switching (ICML 2021) |
| C98 Wattle & daub | hybrid sparse-dense attention + RepVGG reparameterization |

## 4. The 2 survivors (reported per R14 — verified hard, not explained away)

Both **survived grounded-gap verify + adversarial cross-check + independent 3rd-pass audit**:

| id | concept | mechanism (literal-absent) | composite | clears Gate 1? | real lead? |
|----|---------|----------------------------|-----------|----------------|-----------|
| **C37** | Suppletion | output candidates compete by **feature-subset specificity**, more-specific **blocks** less-specific default (Paninian "Elsewhere"/defeasible priority) in decoding | **0.42** | **No** | sub-gate |
| **C57** | Liesegang rings | accumulate→threshold→**local depletion**→refractory zone→**geometric-spaced** periodic commitment propagating outward | **0.45** | **No** | sub-gate |

**Honest assessment (R13):** both are genuine *literal* gaps — no published LLM technique implements the
exact mechanism (3 independent searches each found only the source field or mechanism-distinct ML). But
both are **over-specifications**, same pattern as Run-24 C41: C37's specificity-with-default-blocking is
adjacent to maximal-munch + defeasible priority with "blocking" lifted from its own source; C57's
diversity payoff is already served by repetition penalties + DPP, with refractory/geometric-spacing being
source-borrowed dressing. **Neither is a paradigm-shift niche; neither clears the 0.90 gate.** They are
the two most novelty-resistant residuals in 98 concepts — leads worth a footnote, not a thesis.

---

## 5. THE KEY DATA — cumulative distribution (R10)

Full 98-concept table: `cumulative_per_concept_table.md`. Summary:

```
Total concepts ................................ 98   (48 Run24 + 50 Run25-PartC)  [+5 PART-B family]
Deep grounded-gap verified .................... 54   (12 Run24-sparsest + 33 PartA + 9 PartC-sparsest)
Final COLLISION ............................... 74
Candidate gaps (pre cross-check) .............. 11
  flipped to COLLISION under adversarial xcheck  9   (incl. strongest opus lead C30 -> honeypot)
  SURVIVED xcheck + audit ..................... 2   (C37, C57)
Survivors clearing Gate 1 (composite >= 0.90) . 0
Max composite among survivors ................. 0.45
Positive controls correctly collided .......... 3/3  (re-confirmed in PART A)
PART-B family (C41 cluster) ................... 5/5 COLLISION (shared niche occupied)
Real WebSearches (Run 25) ..................... 489  (171 A + 38 B + 205 C + 61 xcheck + 14 audit)
Fabricated results ............................ 0
```

### Per-concept verdict & overall

- **Per concept:** 0/98 clear all 4 gates. 74 COLLISION, 2 sub-gate survivors (C37, C57), 22 prima-facie
  no-collision but not individually deep-verified (PART-C non-sparsest; their batch representatives were
  verified and collided).
- **Overall:** `NICHE_NOT_FOUND` at the gate. **No pocket (domain or tier) escapes to a Gate-1 niche.**
  The only residual "pockets" are 2 sub-gate over-specifications.

### Is this consistent or a refutation of Run 24?

Run 24's "0 gaps" was **under-verified** (only 12/48). Run 25 shows the honest picture: when you
deep-verify broadly, you *do* find literal gaps (C30, C37, C57 + 8 sonnet candidates), but a rigorous
adversarial cross-check collapses ~80% of them as Pattern-D artifacts, and the survivors are sub-gate.
**Saturation holds at the GATE level (0/98 clear 0.90), but the literal-gap rate is non-zero (~2% survive
all checks) — a more honest, more nuanced result than either "0 gaps" or "niche found."**

---

## 6. Audit, determinism, hallucination (R7)

- **Hallucination:** all audited collision citations confirmed REAL + functionally matching — C30 honeypot
  (arXiv 2310.18633, NeurIPS 2023), C94 DriftSurf (ICML 2021, arXiv 2003.06508), C65 stigmergy/digital
  pheromones (arXiv 1911.12504), C88 ResNet (He 2015). **Zero hallucinated citations** across the run.
- **Determinism:** COLLISION verdicts are mechanically forced (≥2 content-word overlap); forced-hit
  counts were large (10–25 on the deep-verified collisions). The 2 survivors were reproduced by **3
  independent search passes** (verify → adversarial cross-check → audit), each with fresh reformulations
  — the SURVIVES verdict is robust to phrasing, and the sub-gate composite is stable (0.42/0.45 across
  passes).
- **Cross-check + grounded-gap (Run 20):** the adversarial cross-check used ML-native reformulations
  distinct from the original verify; the audit used a 3rd distinct set. C37/C57 absence is not a phrasing
  artifact.

## 7. Honest deviations

- **R1/R2:** 17 sourcing/verify agents + 4 cross-check/audit agents would race on concurrent pushes;
  resolution = agents write files + return raw evidence, main commits+pushes each result (≈20 commits
  pushed live). Cloud-wipe safety + R1/R2 intent preserved.
- **R3:** independent-Opus reasoning via the Agent tool (no `claude -p` shell subprocess / tempdir needed).
- **Verifier-rigor finding:** sonnet PART-C self-verifies flagged gaps at ~9/9; opus PART-A at 2/33;
  adversarial opus cross-check confirmed only 2/11. **Gap-detection is extremely sensitive to verifier
  rigor** — itself a documented result (the project's "Pattern D"), and a caution for any autonomous
  niche-finder.

## 8. One-line conclusion

> Across **98 encyclopedia concepts** with **489 real searches**, finishing Run 24's unfinished
> verification surfaced real *literal* gaps the sparsest-12 missed — but **9 of 11 were Pattern-D false
> positives** that collapsed under adversarial cross-check (incl. the strongest opus lead → honeypot
> defenses), and the **2 genuine survivors (C37, C57) are sub-Gate-1 over-specifications**. **0/98 clear
> all gates.** Strongest empirical saturation evidence yet — with an honest, non-zero literal-gap tail.
> `NICHE_NOT_FOUND`.

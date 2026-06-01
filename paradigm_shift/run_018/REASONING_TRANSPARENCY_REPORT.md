# Run 18 - REASONING TRANSPARENCY REPORT
_generated 2026-06-01T21:21:08.635034+00:00 - sentence-level decomposition from verbatim abstracts (no black box)_

**VERDICT: NICHE_NOT_FOUND** (0/5 survivors)  |  **logic-audit: 0 logic-breaks, 29 non-fatal flags over 63 traces**

---
## STAGE 0 - Atom sourcing (AGENT 1: decompose verbatim abstracts)

**Overall decomposition reasoning_trace:**
- **step:** decompose 3 verbatim abstracts into sentence-level sub-mechanism atoms
- **inputs_seen:** 3 verbatim abstracts from WebSearch: P1 Grassmannian MoE (5 sentences), P2 Fisher-Rao cosine schedule (2 sentences), P3 Energy-Time-Accuracy thermodynamic computing (4 sentences).
- **reasoning:** Run 17 sourced ONE mechanism per paper and every fused niche floored Gate 1 on prior-art VOLUME. The Run 18 hypothesis is that a paper's abstract bundles several sub-mechanisms of DIFFERENT maturity, and that an individual exotic clause (e.g. 'Matrix Bingham concentration parameters', 'energy-delay-deficiency product') may live in sparse space even when the paper's headline topic is mature. I decompose each abstract into every distinct clause that names its own mechanism/result, keeping problem-statement and gap sentences too (they should test as dense, a useful contrast).
- **decision:** 11 atoms: P1->5, P2->2, P3->4. Each is a separate searchable sub-mechanism; AGENT 2 will measure per-atom paper-hits.
- **confidence:** high - the sentence boundaries are clear and each kept clause names a distinct construct
- **could_be_wrong_if:** some 'distinct' clauses are inseparable in the literature (always co-searched), so their individual hit-counts don't reflect a genuinely separable sub-mechanism.


### R18_P1_S1 (P1, ml) - hits=1 SPARSE
sub_mechanism: _softmax gating provides no principled sparsity-utilization control (problem statement)_  ·  `arXiv:2602.17798`
> Mixture-of-Experts models rely on learned routers to assign tokens to experts, yet standard softmax gating provides no principled mechanism to control the tradeoff between sparsity and utilization.

**why a distinct atom:**
- **step:** decompose P1 sentence 1
- **inputs_seen:** the MoE/softmax-gating problem-statement sentence
- **reasoning:** This is the problem framing (softmax gating lacks sparsity-utilization control), not a novel mechanism; I keep it as an atom but predict it is DENSE - it is the generic MoE motivation found in hundreds of papers.
- **decision:** keep as atom R18_P1_S1; predict dense
- **confidence:** high - clearly the generic motivation clause
- **could_be_wrong_if:** the exact phrasing 'tradeoff between sparsity and utilization' is rarer than the concept.


### R18_P1_S2 (P1, ml) - hits=3 SPARSE
sub_mechanism: _gating weights arise from the concentration parameters of Matrix Bingham distributions on the Grassmannian manifold_  ·  `arXiv:2602.17798`
> Grassmannian MoE (GrMoE) is a routing framework that operates on the Grassmannian manifold of subspaces, where gating weights arise from the concentration parameters of Matrix Bingham distributions.

**why a distinct atom:**
- **step:** decompose P1 sentence 2
- **inputs_seen:** the Grassmannian-manifold / Matrix-Bingham gating construction
- **reasoning:** Distinct from S3 (which is the resulting knob) because S2 is the GENERATIVE construct: gating weights from Matrix Bingham concentration parameters on the Grassmannian manifold. 'Matrix Bingham distribution' is an exotic directional-statistics object rarely used in ML routing - predict SPARSE.
- **decision:** keep as atom R18_P1_S2; predict sparse
- **confidence:** high - Matrix Bingham + Grassmannian routing is an unusual construct
- **could_be_wrong_if:** directional-statistics gating is more common than I think (e.g. von Mises-Fisher routing), inflating hits.


### R18_P1_S3 (P1, ml) - hits=3 SPARSE
sub_mechanism: _a concentration matrix continuously controls routing entropy, replacing discrete top-k with a smooth sparsity mechanism_  ·  `arXiv:2602.17798`
> This construction yields a single, interpretable knob -- the concentration matrix that continuously controls routing entropy, replacing discrete top-k selection with a smooth, geometrically principled sparsity mechanism.

**why a distinct atom:**
- **step:** decompose P1 sentence 3
- **inputs_seen:** the concentration matrix continuously controls routing entropy, replacing top-k
- **reasoning:** Distinct from S2: S3 is the FUNCTION (entropy control replacing top-k), independent of the Bingham generative story. 'routing entropy control' and 'replacing top-k' are moderately studied - predict moderate/dense.
- **decision:** keep as atom R18_P1_S3; predict moderate
- **confidence:** medium - entropy-controlled routing is an active but not saturated sub-area
- **could_be_wrong_if:** entropy-controlled MoE routing is denser than expected (Run 17 already saw MoxE etc.).


### R18_P1_S4 (P1, ml) - hits=4 SPARSE
sub_mechanism: _amortized variational inference for posterior routing distributions -> uncertainty-aware assignment resisting collapse_  ·  `arXiv:2602.17798`
> The paper develops an amortized variational inference procedure for posterior routing distributions, enabling uncertainty-aware expert assignment that naturally resists expert collapse.

**why a distinct atom:**
- **step:** decompose P1 sentence 4
- **inputs_seen:** amortized variational inference for posterior routing distributions
- **reasoning:** A distinct inference mechanism (Bayesian/VI routing), separable from the geometry (S2) and the bound (S5). 'amortized variational inference' is common in VAEs but rare specifically for MoE posterior ROUTING distributions - predict sparse-to-moderate.
- **decision:** keep as atom R18_P1_S4; predict sparse-moderate
- **confidence:** medium - VI is common, VI-for-routing is narrower
- **could_be_wrong_if:** 'amortized variational inference' alone returns the large VAE literature, reading as dense.


### R18_P1_S5 (P1, ml) - hits=2 SPARSE
sub_mechanism: _tight bounds relating the Bingham concentration spectrum to routing entropy, top-k mass, and an exponential bound on expert collapse_  ·  `arXiv:2602.17798`
> The authors formally prove tight bounds relating the Bingham concentration spectrum to routing entropy, expected top-k mass, and an exponential bound on expert collapse.

**why a distinct atom:**
- **step:** decompose P1 sentence 5
- **inputs_seen:** tight bounds: Bingham concentration spectrum -> routing entropy / top-k mass / expert collapse
- **reasoning:** The theoretical-result clause, distinct from the construction. Couples a Bingham spectrum to expert-collapse bounds - a very specific theorem; predict SPARSE.
- **decision:** keep as atom R18_P1_S5; predict sparse
- **confidence:** high - a highly specific bound
- **could_be_wrong_if:** 'expert collapse' dominates the query and pulls the (dense) collapse literature.


### R18_P2_S1 (P2, ml) - hits=4 SPARSE
sub_mechanism: _choosing the discretisation schedule via the information geometry of the induced probability path_  ·  `arXiv:2508.04884`
> The discretisation schedule for sampling from masked discrete diffusion models is chosen in terms of the information geometry of the induced probability path.

**why a distinct atom:**
- **step:** decompose P2 sentence 1
- **inputs_seen:** discretisation schedule via information geometry of the induced probability path
- **reasoning:** P2 has only 2 sentences. S1 is the framing-as-information-geometry (probability-path geometry for diffusion schedules); distinct from S2's specific Fisher-Rao result. Predict sparse-moderate.
- **decision:** keep as atom R18_P2_S1; predict sparse-moderate
- **confidence:** medium - information-geometry-of-diffusion is a small but real area
- **could_be_wrong_if:** 'probability path' pulls the large flow-matching literature, reading dense.


### R18_P2_S2 (P2, ml) - hits=3 SPARSE
sub_mechanism: _the optimal schedule under the Fisher-Rao geometry recovers the cosine schedule_  ·  `arXiv:2508.04884`
> The optimal schedule under the Fisher-Rao geometry recovers the popularly-used cosine schedule.

**why a distinct atom:**
- **step:** decompose P2 sentence 2
- **inputs_seen:** Fisher-Rao-optimal schedule recovers the cosine schedule
- **reasoning:** The specific result: Fisher-Rao geometry -> cosine schedule optimality for masked diffusion. 'Fisher-Rao' + 'cosine schedule' is a precise, recent pairing; predict SPARSE.
- **decision:** keep as atom R18_P2_S2; predict sparse
- **confidence:** high - Fisher-Rao-optimal masked-diffusion schedule is a narrow result
- **could_be_wrong_if:** 'cosine schedule' dominates and returns the broad scheduling literature.


### R18_P3_S1 (P3, physics) - hits=3 SPARSE
sub_mechanism: _thermodynamic-computing hardware undergoes a stochastic process to sample from a distribution_  ·  `arXiv:2601.04358`
> In the paradigm of thermodynamic computing, hardware undergoes a stochastic process in order to sample from a distribution of interest.

**why a distinct atom:**
- **step:** decompose P3 sentence 1
- **inputs_seen:** thermodynamic-computing hardware undergoes a stochastic process to sample a distribution
- **reasoning:** The thermodynamic-computing premise; distinct from the trade-off analysis (S3) and the EDDP bound (S4). Predict moderate - thermodynamic computing is an active niche field.
- **decision:** keep as atom R18_P3_S1; predict moderate
- **confidence:** medium
- **could_be_wrong_if:** thermodynamic computing is smaller than I think (sparse) or larger via 'stochastic sampling hardware' (dense).


### R18_P3_S2 (P3, physics) - hits=5 SPARSE
sub_mechanism: _a theoretical characterization of the resource cost of thermodynamic computation is still lacking (gap)_  ·  `arXiv:2601.04358`
> While it has been hypothesized that thermodynamic computers may achieve better energy efficiency and performance, a theoretical characterization of the resource cost of thermodynamic computations is still lacking.

**why a distinct atom:**
- **step:** decompose P3 sentence 2
- **inputs_seen:** resource-cost characterization of thermodynamic computation is lacking (gap)
- **reasoning:** A gap/motivation sentence; kept for contrast. Predict moderate - it names the field but asserts a gap, so hits depend on the field's size.
- **decision:** keep as atom R18_P3_S2; predict moderate
- **confidence:** medium - gap statements track field size
- **could_be_wrong_if:** phrased generically enough to pull broad energy-efficiency work (dense).


### R18_P3_S3 (P3, physics) - hits=4 SPARSE
sub_mechanism: _fundamental trade-offs between computational accuracy, energy dissipation, and time_  ·  `arXiv:2601.04358`
> The paper analyzes the fundamental trade-offs between computational accuracy, energy dissipation, and time in thermodynamic computing.

**why a distinct atom:**
- **step:** decompose P3 sentence 3
- **inputs_seen:** accuracy / energy-dissipation / time trade-off in thermodynamic computing
- **reasoning:** The trade-off triad; distinct from S4's specific EDDP metric. 'energy-accuracy-time tradeoff' is studied broadly in thermodynamics of computation; predict moderate-dense.
- **decision:** keep as atom R18_P3_S3; predict moderate-dense
- **confidence:** medium
- **could_be_wrong_if:** the triad framing is itself rare even if each pairwise tradeoff is common.


### R18_P3_S4 (P3, physics) - hits=5 SPARSE
sub_mechanism: _geometric bounds on entropy production -> limits on the energy-delay-deficiency product (EDDP)_  ·  `arXiv:2601.04358`
> Using geometric bounds on entropy production, the authors derive general limits on the energy-delay-deficiency product (EDDP), a stochastic generalization of energy-time-accuracy tradeoff metrics.

**why a distinct atom:**
- **step:** decompose P3 sentence 4
- **inputs_seen:** geometric bounds on entropy production -> energy-delay-deficiency product (EDDP)
- **reasoning:** The headline result: a COINED metric (EDDP) from geometric entropy-production bounds. A freshly named quantity should be the sparsest atom of all; predict SPARSE.
- **decision:** keep as atom R18_P3_S4; predict sparse
- **confidence:** high - EDDP is a newly coined term
- **could_be_wrong_if:** 'entropy production bounds' dominates and returns the large stochastic-thermodynamics literature.


---
## STAGE 2 - Per-atom saturation (AGENT 2: paper-hits per sub-mechanism)  [R10]

| atom | sub_mechanism | paper_hits | sparse(<10) |
|---|---|---|---|
| R18_P1_S1 |  | **1** | YES |
| R18_P1_S5 |  | **2** | YES |
| R18_P1_S2 |  | **3** | YES |
| R18_P1_S3 |  | **3** | YES |
| R18_P2_S2 |  | **3** | YES |
| R18_P3_S1 |  | **3** | YES |
| R18_P1_S4 |  | **4** | YES |
| R18_P2_S1 |  | **4** | YES |
| R18_P3_S3 |  | **4** | YES |
| R18_P3_S2 |  | **5** | YES |
| R18_P3_S4 |  | **5** | YES |

**11 of 11 sub-mechanisms are individually sparse:** ['R18_P1_S1', 'R18_P1_S2', 'R18_P1_S3', 'R18_P1_S4', 'R18_P1_S5', 'R18_P2_S1', 'R18_P2_S2', 'R18_P3_S1', 'R18_P3_S2', 'R18_P3_S3', 'R18_P3_S4']


---
## STAGE 3->5 - Per candidate (sparsest pairs): merge -> verify -> cross-check -> gates


### CAND_018_001 - Fisher-Rao Optimal Annealing of MoE Router Concentration Against Expert Collapse
`R18_P1_S5(h=2) x R18_P2_S2(h=3)` combined_atom_hits=5  ->  verify_hits=20, **composite 0.45**, survived=False, failed=['gate_1_composite']

**MERGE (AGENT 3):** Treating the MoE router's Bingham concentration spectrum as a point on a statistical manifold, the Fisher-Rao geometry induces a natural-gradient annealing schedule over routing temperature that regulates routing entropy and expected top-k mass, which in turn produces an exponential bound on expert collapse.
- merge reasoning_trace:
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: tight bounds linking the Bingham concentration spectrum to routing entropy, expected top-k mass, and an exponential expert-collapse bound. B: the Fisher-Rao-geometry-optimal schedule recovers the cosine schedule.
  - **reasoning:** I tried to transfer B's mechanism that an optimal schedule emerges from Fisher-Rao information geometry over a parameter, applying it to A's Bingham concentration parameter rather than to a learning rate; both A's spectrum and the Bingham distribution are genuinely statistical-manifold objects, so Fisher-Rao acts on the same geometry A already quantifies. I rejected a looser merge that just reuses A's bounds as a regularizer (no schedule, no geometry) and one that swaps cosine LR scheduling into MoE training (vocabulary overlap only). Non-trivial because A's collapse bound is static in the concentration spectrum while B supplies the missing dynamics: the metric that says how to MOVE concentration over time, making the collapse bound a function of a derivable trajectory.
  - **decision:** A Fisher-Rao-derived annealing schedule over the router's Bingham concentration spectrum that provably minimizes the exponential expert-collapse bound; chosen because both mechanisms live on the same information manifold, so the coupling is structural, not metaphorical.
  - **confidence:** medium - the manifold match is real but whether Fisher-Rao on the Bingham spectrum admits a tractable closed-form schedule is unproven.
  - **could_be_wrong_if:** If the Bingham concentration spectrum in A is treated as a fixed analyzed quantity with no trainable/schedulable parameter, then there is nothing for B's schedule to anneal and the link collapses to a shared-vocabulary analogy.

  - _AGENT 5 audit:_ VALID (grounding=0.429)

**VERIFY (AGENT 4):** collision_found=False, 5 reformulations, 20 paper-like hits
- verify verdict reasoning_trace:
  - **step:** collision verdict CAND_018_001
  - **inputs_seen:** 5 reformulations; ~20 distinct paper-like hits across MoE-collapse, cosine-router, Fisher-Rao-merging, and generic simulated-annealing literatures; no fused paper
  - **reasoning:** The two sub-mechanisms (Bingham-spectrum collapse bound h=2; Fisher-Rao cosine schedule h=3) are individually sparse, but the fused niche 'Fisher-Rao annealing of router concentration vs collapse' pulls the mature annealing + collapse + information-geometry literatures. No paper performs Fisher-Rao-optimal annealing of Bingham router concentration.
  - **decision:** no collision: fused niche unoccupied, but prior-art VOLUME is high (Gate-1 will floor novelty)
  - **confidence:** medium - components mature; an annealing-schedule paper could phrase this differently
  - **could_be_wrong_if:** a 'dense-to-sparse temperature schedule' paper already IS Fisher-Rao-optimal annealing under different words

  - _AGENT 5 audit:_ VALID - decision<->data: polarity=no_collision vs collision_found=False

**CROSS-CHECK (AGENT 4):** agent4_collision=False, mismatch_with_agent3=False
- crosscheck reasoning_trace:
  - **step:** independent re-verification CAND_018_001
  - **inputs_seen:** verifier verdict (no collision) + my fresh 'cooling schedule' re-search; new neighbor 2602.14039
  - **reasoning:** I used 'geodesic cooling schedule' phrasing the verifier did not, to catch a missed collision. It returned collapse-avoidance + a geometry-preserving aggregation paper, none performing Fisher-Rao annealing of concentration. I uphold the verifier.
  - **decision:** confirm verifier no-collision; no mismatch
  - **confidence:** medium - components mature, but the specific schedule is unoccupied
  - **could_be_wrong_if:** a learnable-temperature soft-gate paper is mathematically Fisher-Rao-optimal annealing


**GATES (MAIN - exact numbers):**

_Gate 1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) for CAND_018_001
  - **inputs_seen:** composite=0.45 from params={'novelty': 0.0, 'mechanism_present': 1.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} weights={'novelty': 0.55, 'mechanism_present': 0.2, 'quote_grounded': 0.15, 'cross_atom': 0.1}; novelty=1-paper_hits/20 with paper_hits=20 (AGENT 4 real hits)
  - **reasoning:** novelty (weight 0.55) is 0.0 from 20 paper-like hits; ceiling is novelty*0.55+0.45; to clear 0.90 needs novelty>=0.8182 i.e. <=4 paper hits.
  - **decision:** FAIL (0.45 < 0.9)
  - **confidence:** high - pure arithmetic over recorded counts
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits (20) or recorded unseen results (R5 violation upstream)


_Gate 2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) for CAND_018_001
  - **inputs_seen:** atoms used = ['R18_P1_S5', 'R18_P2_S2']; quarantine set = ['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** Fails iff either source atom id is on the quarantine blocklist.
  - **decision:** PASS (hits=[])
  - **confidence:** high - exact set membership
  - **could_be_wrong_if:** an atom id string-collides with a quarantined id without being the same atom


_Gate 3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) for CAND_018_001
  - **inputs_seen:** n_reformulations=5 (required 5); verifier_collision=False; crosscheck_overturned=False
  - **reasoning:** Passes only if >=5 real reformulations AND no verifier collision AND AGENT 4 cross-check did not overturn (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion of two agents' verdicts
  - **could_be_wrong_if:** both verify and crosscheck missed an existing paper occupying the fused niche (shared blind spot)


_Gate 4 Belinda strict: PASS_
  - **step:** Gate 4 (Belinda strict) for CAND_018_001
  - **inputs_seen:** mechanism causal verbs found=['induces', 'produces', 'regulates']; quote_len=95 (min 30); quote_grounded=True (atom R18_P2_S2)
  - **reasoning:** Requires a concrete causal mechanism verb AND a >=30-char verbatim quote substring of its named atom.
  - **decision:** PASS
  - **confidence:** high - regex verb match + exact substring containment
  - **could_be_wrong_if:** the mechanism is real but uses a causal verb outside the fixed Belinda vocab, or the quote is paraphrased


**SURVIVAL:** ELIMINATED at gate_1_composite

### CAND_018_002 - Thermodynamic Bingham routers with provable expert-collapse bounds
`R18_P1_S5(h=2) x R18_P3_S1(h=3)` combined_atom_hits=5  ->  verify_hits=19, **composite 0.4775**, survived=False, failed=['gate_1_composite']

**MERGE (AGENT 3):** Routing the Bingham concentration spectrum—whose tight bounds govern routing entropy, expected top-k mass, and expert collapse—onto a thermodynamic computing substrate causes the hardware's native stochastic relaxation to physically sample the MoE gating distribution, so the concentration parameter directly regulates the analog noise and inhibits expert collapse without explicit softmax computation.
- merge reasoning_trace:
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: tight bounds tie a Bingham concentration spectrum to MoE routing entropy, expected top-k mass, and an exponential bound on expert collapse. B: thermodynamic computing performs sampling by letting hardware physically run a stochastic process toward a target distribution.
  - **reasoning:** I tried to transfer A's concentration-spectrum-as-controller-of-routing-distribution mechanism onto B's physical-sampling substrate: instead of computing the router distribution digitally, let the thermodynamic hardware's stationary distribution BE the Bingham router, with concentration as the tunable physical noise scale. I rejected the looser direction (using MoE to schedule thermodynamic chips) because A's bounds are specifically about a sampling distribution's geometry, which is exactly what B's hardware materializes. The non-trivial part is that A already proves the relevant quantity (entropy, top-k mass, collapse) is a function of a Bingham concentration parameter—the same parameter that a thermodynamic sampler exposes as a physical temperature/coupling—so the bounds become hardware design constraints, not just an analytic curiosity.
  - **decision:** I settled on physically realizing the MoE router as a thermodynamic Bingham sampler whose concentration spectrum is set by hardware noise, because it makes A's collapse bound an engineering specification for B's substrate.
  - **confidence:** medium - the Bingham-thermodynamic mapping is plausible since Bingham distributions arise from quadratic energy on a sphere, matching physical relaxation, but the realizability of exact bounds on real noisy hardware is unproven.
  - **could_be_wrong_if:** thermodynamic hardware cannot stably hold a tunable Bingham concentration, in which case 'sampling a routing distribution on a sampler' is just shared sampling vocabulary and A's bounds never bind to any physical parameter.

  - _AGENT 5 audit:_ VALID (grounding=0.706)

**VERIFY (AGENT 4):** collision_found=False, 5 reformulations, 19 paper-like hits
- verify verdict reasoning_trace:
  - **step:** collision verdict CAND_018_002
  - **inputs_seen:** 5 reformulations; disjoint MoE-collapse vs thermodynamic-computing clusters; search 5 found no combined paper
  - **reasoning:** Bingham-spectrum collapse bound (h=2) x thermodynamic stochastic sampling (h=3). p-bit/EBM hardware (Extropic, Normal Computing) and MoE-collapse theory are both mature but never joined: no paper implements a Bingham MoE router on thermodynamic hardware with collapse bounds.
  - **decision:** no collision: disjoint clusters, fusion unoccupied; high component volume
  - **confidence:** high - the two literatures are clearly separate and the search engine flagged the gap
  - **could_be_wrong_if:** Extropic's pMoG mixture-of-Gaussians sampler already realizes a thermodynamic MoE router

  - _AGENT 5 audit:_ VALID - decision<->data: polarity=no_collision vs collision_found=False

**CROSS-CHECK (AGENT 4):** agent4_collision=False, mismatch_with_agent3=False
- crosscheck reasoning_trace:
  - **step:** independent re-verification CAND_018_002
  - **inputs_seen:** verifier verdict (no collision) + my fresh p-bit-hardware re-search; new neighbors 2510.23972, 2512.24558
  - **reasoning:** p-bit/probabilistic hardware IS a real cluster (and diffusion-like-model hardware 2510.23972 is close in spirit), but none gate MoE experts via a Bingham distribution with collapse bounds. Confirms verifier.
  - **decision:** confirm verifier no-collision; no mismatch
  - **confidence:** high - the hardware and MoE clusters are clearly separate
  - **could_be_wrong_if:** the diffusion-like-model probabilistic hardware already routes experts


**GATES (MAIN - exact numbers):**

_Gate 1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) for CAND_018_002
  - **inputs_seen:** composite=0.4775 from params={'novelty': 0.05, 'mechanism_present': 1.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} weights={'novelty': 0.55, 'mechanism_present': 0.2, 'quote_grounded': 0.15, 'cross_atom': 0.1}; novelty=1-paper_hits/20 with paper_hits=19 (AGENT 4 real hits)
  - **reasoning:** novelty (weight 0.55) is 0.05 from 19 paper-like hits; ceiling is novelty*0.55+0.45; to clear 0.90 needs novelty>=0.8182 i.e. <=4 paper hits.
  - **decision:** FAIL (0.4775 < 0.9)
  - **confidence:** high - pure arithmetic over recorded counts
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits (19) or recorded unseen results (R5 violation upstream)


_Gate 2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) for CAND_018_002
  - **inputs_seen:** atoms used = ['R18_P1_S5', 'R18_P3_S1']; quarantine set = ['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** Fails iff either source atom id is on the quarantine blocklist.
  - **decision:** PASS (hits=[])
  - **confidence:** high - exact set membership
  - **could_be_wrong_if:** an atom id string-collides with a quarantined id without being the same atom


_Gate 3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) for CAND_018_002
  - **inputs_seen:** n_reformulations=5 (required 5); verifier_collision=False; crosscheck_overturned=False
  - **reasoning:** Passes only if >=5 real reformulations AND no verifier collision AND AGENT 4 cross-check did not overturn (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion of two agents' verdicts
  - **could_be_wrong_if:** both verify and crosscheck missed an existing paper occupying the fused niche (shared blind spot)


_Gate 4 Belinda strict: PASS_
  - **step:** Gate 4 (Belinda strict) for CAND_018_002
  - **inputs_seen:** mechanism causal verbs found=['causes', 'inhibits', 'regulates']; quote_len=90 (min 30); quote_grounded=True (atom R18_P3_S1)
  - **reasoning:** Requires a concrete causal mechanism verb AND a >=30-char verbatim quote substring of its named atom.
  - **decision:** PASS
  - **confidence:** high - regex verb match + exact substring containment
  - **could_be_wrong_if:** the mechanism is real but uses a causal verb outside the fixed Belinda vocab, or the quote is paraphrased


**SURVIVAL:** ELIMINATED at gate_1_composite

### CAND_018_003 - Fisher-Rao optimal scheduling of Grassmannian MoE Bingham gating
`R18_P1_S2(h=3) x R18_P2_S2(h=3)` combined_atom_hits=6  ->  verify_hits=18, **composite 0.505**, survived=False, failed=['gate_1_composite']

**MERGE (AGENT 3):** Treating the Matrix Bingham gating distribution of Grassmannian MoE as a statistical manifold, the Fisher-Rao geometry induces a principled schedule over the concentration parameters that routes tokens to subspaces, transforming ad-hoc gating annealing into a geodesic-optimal trajectory whose endpoints recover known cosine-like routing temperature schedules.
- merge reasoning_trace:
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: MoE routing on the Grassmannian manifold where gating weights come from Matrix Bingham concentration parameters; B: the Fisher-Rao-geometry-optimal schedule provably recovers the cosine schedule.
  - **reasoning:** I tried to transfer B's information-geometric optimality principle (optimal scheduling derived from Fisher-Rao geometry of a parameter family) onto A's gating mechanism, because A's gating weights are literally parameterized by Matrix Bingham concentration parameters, which form a statistical manifold with its own Fisher-Rao metric. I rejected the reverse transfer (importing Grassmannian routing into diffusion scheduling) as forced, and rejected merely sharing the word 'manifold' as the link. The non-trivial part is that both atoms operate on genuinely different but compatible geometries: A's Grassmannian (geometry of subspaces) and the Fisher-Rao geometry of the Bingham parameter space are distinct objects, yet B's result suggests the schedule for the distributional parameters could be derived geodesically rather than tuned, giving a concrete unified scheduling law for routing concentration that nobody currently derives from first principles.
  - **decision:** I settled on deriving a Fisher-Rao-optimal annealing schedule for the Matrix Bingham concentration parameters in Grassmannian MoE gating, because it converts A's heuristic gating sharpness into a principled, possibly closed-form schedule analogous to B's cosine recovery.
  - **confidence:** medium - both use real information geometry on distinct manifolds, so the transfer is structurally plausible but the Fisher-Rao metric on the Matrix Bingham family may lack the tractability that made B's cosine recovery clean.
  - **could_be_wrong_if:** the merge is trivial if the Matrix Bingham Fisher-Rao schedule is intractable or simply reduces to existing temperature annealing, making 'Fisher-Rao' a vocabulary relabeling rather than a new optimality result.

  - _AGENT 5 audit:_ VALID (grounding=0.4)

**VERIFY (AGENT 4):** collision_found=False, 5 reformulations, 18 paper-like hits
- verify verdict reasoning_trace:
  - **step:** collision verdict CAND_018_003
  - **inputs_seen:** 5 reformulations; GrMoE and Fisher-Rao-cosine appear separately; neighbors are geometric-routing + MoE surveys
  - **reasoning:** Matrix Bingham gating (h=3) x Fisher-Rao cosine schedule (h=3). Geometric/manifold routing is an active cluster (RoMA, GraphMoRE, curvature-guided) but no paper applies a Fisher-Rao optimal SCHEDULE to Bingham gating.
  - **decision:** no collision: fusion unoccupied; geometric-routing volume high
  - **confidence:** medium - geometric routing is crowded; the schedule-transfer is the distinguishing piece
  - **could_be_wrong_if:** a manifold-routing paper already schedules concentration via information geometry

  - _AGENT 5 audit:_ VALID - decision<->data: polarity=no_collision vs collision_found=False

**CROSS-CHECK (AGENT 4):** agent4_collision=False, mismatch_with_agent3=False
- crosscheck reasoning_trace:
  - **step:** independent re-verification CAND_018_003
  - **inputs_seen:** verifier verdict (no collision) + my fresh directional-distribution re-search; new neighbors 2605.31043, 2504.14164
  - **reasoning:** Directional-distribution and manifold routing exist (Stiefel routing, vMF Wasserstein), confirming the components are mature, but none apply a Fisher-Rao optimal schedule to Bingham gating. Confirms verifier.
  - **decision:** confirm verifier no-collision; no mismatch
  - **confidence:** medium - manifold routing is active; the schedule-transfer remains the distinguishing piece
  - **could_be_wrong_if:** Stiefel-manifold routing already includes an information-geometric schedule


**GATES (MAIN - exact numbers):**

_Gate 1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) for CAND_018_003
  - **inputs_seen:** composite=0.505 from params={'novelty': 0.1, 'mechanism_present': 1.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} weights={'novelty': 0.55, 'mechanism_present': 0.2, 'quote_grounded': 0.15, 'cross_atom': 0.1}; novelty=1-paper_hits/20 with paper_hits=18 (AGENT 4 real hits)
  - **reasoning:** novelty (weight 0.55) is 0.1 from 18 paper-like hits; ceiling is novelty*0.55+0.45; to clear 0.90 needs novelty>=0.8182 i.e. <=4 paper hits.
  - **decision:** FAIL (0.505 < 0.9)
  - **confidence:** high - pure arithmetic over recorded counts
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits (18) or recorded unseen results (R5 violation upstream)


_Gate 2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) for CAND_018_003
  - **inputs_seen:** atoms used = ['R18_P1_S2', 'R18_P2_S2']; quarantine set = ['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** Fails iff either source atom id is on the quarantine blocklist.
  - **decision:** PASS (hits=[])
  - **confidence:** high - exact set membership
  - **could_be_wrong_if:** an atom id string-collides with a quarantined id without being the same atom


_Gate 3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) for CAND_018_003
  - **inputs_seen:** n_reformulations=5 (required 5); verifier_collision=False; crosscheck_overturned=False
  - **reasoning:** Passes only if >=5 real reformulations AND no verifier collision AND AGENT 4 cross-check did not overturn (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion of two agents' verdicts
  - **could_be_wrong_if:** both verify and crosscheck missed an existing paper occupying the fused niche (shared blind spot)


_Gate 4 Belinda strict: PASS_
  - **step:** Gate 4 (Belinda strict) for CAND_018_003
  - **inputs_seen:** mechanism causal verbs found=['induces']; quote_len=95 (min 30); quote_grounded=True (atom R18_P2_S2)
  - **reasoning:** Requires a concrete causal mechanism verb AND a >=30-char verbatim quote substring of its named atom.
  - **decision:** PASS
  - **confidence:** high - regex verb match + exact substring containment
  - **could_be_wrong_if:** the mechanism is real but uses a causal verb outside the fixed Belinda vocab, or the quote is paraphrased


**SURVIVAL:** ELIMINATED at gate_1_composite

### CAND_018_004 - Thermodynamic Grassmannian MoE Routing via Physical Bingham Sampling
`R18_P1_S2(h=3) x R18_P3_S1(h=3)` combined_atom_hits=6  ->  verify_hits=19, **composite 0.4775**, survived=False, failed=['gate_1_composite']

**MERGE (AGENT 3):** A thermodynamic-computing substrate physically samples from Matrix Bingham distributions whose concentration parameters define GrMoE gating, so the hardware's stochastic relaxation directly produces the subspace-routing weights on the Grassmannian manifold rather than a digital sampler computing them.
- merge reasoning_trace:
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: MoE routing where gating weights come from concentration parameters of Matrix Bingham distributions on the Grassmannian manifold of subspaces. B: thermodynamic computing where hardware runs a stochastic process to sample from a target distribution.
  - **reasoning:** I tried to transfer A's specific gating distribution (Matrix Bingham over subspaces) into B's role of 'distribution of interest' that hardware physically samples. I rejected the weaker transfer of merely running GrMoE on thermodynamic hardware as a generic accelerator, because that is a surface 'analog speedup' claim. The non-trivial hinge is that the Bingham distribution is exactly the kind of exponential-family-on-a-manifold distribution that thermodynamic/Langevin-style hardware is natively suited to sample, so the concentration parameters could be loaded as physical coupling fields and the equilibrium state read out as the route — making the gating computation and the hardware's relaxation the same physical event.
  - **decision:** Settled on a thermodynamic GrMoE where physical stochastic relaxation samples the Matrix Bingham gating distribution to produce routing decisions, because it converts A's costly manifold sampling into B's free-energy minimization rather than bolting them together.
  - **confidence:** medium - the Bingham-on-Stiefel/Grassmannian distribution plausibly maps to a physical energy function, but realizability on actual thermodynamic hardware is unproven.
  - **could_be_wrong_if:** Matrix Bingham concentration parameters cannot be encoded as a physical coupling Hamiltonian a thermodynamic device can equilibrate to, in which case this is just 'run sampling on stochastic hardware' — a vocabulary analogy with no mechanism gain.

  - _AGENT 5 audit:_ VALID (grounding=0.522)

**VERIFY (AGENT 4):** collision_found=False, 5 reformulations, 19 paper-like hits
- verify verdict reasoning_trace:
  - **step:** collision verdict CAND_018_004
  - **inputs_seen:** 5 reformulations; directional-statistics Bingham sampling + MoE-hardware + physics-inspired routing all separate; searches 1/3 found no thermodynamic connection
  - **reasoning:** Matrix Bingham gating (h=3) x thermodynamic stochastic sampling (h=3). Bingham/von Mises-Fisher sampling (Hoff, MLR 2010.00137), MoE hardware distribution (USPTO), and physics-inspired routing (Raytraced Experts 2507.12419) exist, but no paper draws Bingham routing weights on a physical/thermodynamic sampler.
  - **decision:** no collision: fusion unoccupied; component volume high
  - **confidence:** high - clear three-way separation
  - **could_be_wrong_if:** 'Mixture of Raytraced Experts' physical-firing routing is effectively physical Bingham sampling

  - _AGENT 5 audit:_ VALID - decision<->data: polarity=no_collision vs collision_found=False

**CROSS-CHECK (AGENT 4):** agent4_collision=False, mismatch_with_agent3=False
- crosscheck reasoning_trace:
  - **step:** independent re-verification CAND_018_004
  - **inputs_seen:** verifier verdict (no collision) + my fresh physics-routing re-search; new neighbors 2507.12419, MOESART
  - **reasoning:** Sampling-based and 'raytraced'/physics-inspired routing exist as ALGORITHMS, but none draw routing weights from a physical/thermodynamic Bingham sampler. Confirms verifier.
  - **decision:** confirm verifier no-collision; no mismatch
  - **confidence:** high - physics-inspired routing here is algorithmic, not hardware sampling
  - **could_be_wrong_if:** Raytraced Experts' physical firing model is effectively a hardware Bingham sampler


**GATES (MAIN - exact numbers):**

_Gate 1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) for CAND_018_004
  - **inputs_seen:** composite=0.4775 from params={'novelty': 0.05, 'mechanism_present': 1.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} weights={'novelty': 0.55, 'mechanism_present': 0.2, 'quote_grounded': 0.15, 'cross_atom': 0.1}; novelty=1-paper_hits/20 with paper_hits=19 (AGENT 4 real hits)
  - **reasoning:** novelty (weight 0.55) is 0.05 from 19 paper-like hits; ceiling is novelty*0.55+0.45; to clear 0.90 needs novelty>=0.8182 i.e. <=4 paper hits.
  - **decision:** FAIL (0.4775 < 0.9)
  - **confidence:** high - pure arithmetic over recorded counts
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits (19) or recorded unseen results (R5 violation upstream)


_Gate 2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) for CAND_018_004
  - **inputs_seen:** atoms used = ['R18_P1_S2', 'R18_P3_S1']; quarantine set = ['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** Fails iff either source atom id is on the quarantine blocklist.
  - **decision:** PASS (hits=[])
  - **confidence:** high - exact set membership
  - **could_be_wrong_if:** an atom id string-collides with a quarantined id without being the same atom


_Gate 3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) for CAND_018_004
  - **inputs_seen:** n_reformulations=5 (required 5); verifier_collision=False; crosscheck_overturned=False
  - **reasoning:** Passes only if >=5 real reformulations AND no verifier collision AND AGENT 4 cross-check did not overturn (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion of two agents' verdicts
  - **could_be_wrong_if:** both verify and crosscheck missed an existing paper occupying the fused niche (shared blind spot)


_Gate 4 Belinda strict: PASS_
  - **step:** Gate 4 (Belinda strict) for CAND_018_004
  - **inputs_seen:** mechanism causal verbs found=['produces']; quote_len=90 (min 30); quote_grounded=True (atom R18_P3_S1)
  - **reasoning:** Requires a concrete causal mechanism verb AND a >=30-char verbatim quote substring of its named atom.
  - **decision:** PASS
  - **confidence:** high - regex verb match + exact substring containment
  - **could_be_wrong_if:** the mechanism is real but uses a causal verb outside the fixed Belinda vocab, or the quote is paraphrased


**SURVIVAL:** ELIMINATED at gate_1_composite

### CAND_018_005 - Fisher-Rao-optimal scheduling of continuous MoE routing entropy
`R18_P1_S3(h=3) x R18_P2_S2(h=3)` combined_atom_hits=6  ->  verify_hits=23, **composite 0.45**, survived=False, failed=['gate_1_composite']

**MERGE (AGENT 3):** Treating MoE routing entropy as a point on a statistical manifold, a Fisher-Rao-optimal schedule regulates the concentration matrix over training, which transforms the static interpretable sparsity knob into a time-varying trajectory that routes tokens through a geometrically shortest-path annealing of routing entropy.
- merge reasoning_trace:
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: a concentration matrix is a single continuous knob that controls routing entropy, replacing discrete top-k with smooth geometrically-principled sparsity. B: under Fisher-Rao geometry the optimal schedule recovers the cosine schedule.
  - **reasoning:** I tried to transfer B's information-geometric optimality-of-schedules result onto A's routing knob: A gives a single continuous parameter (concentration) but says nothing about how it should evolve during training, while B is precisely a theorem about the geometrically optimal time-evolution of a scalar control parameter. I rejected merging at the vocabulary level (both mention 'geometry') because that would be a surface analogy; the non-trivial claim is that A's concentration matrix and B's schedule variable both live on a statistical manifold of distributions (routing distributions / noise distributions), so Fisher-Rao machinery applies to A's knob directly rather than by metaphor. I rejected the inverse transfer (use A's sparsity to choose a noise schedule) as weaker because schedules are scalar, not sparsity-structured.
  - **decision:** Settled on deriving a Fisher-Rao-optimal annealing schedule for the routing concentration matrix, because it converts A's static knob into a principled curriculum and gives B's optimality result a new, testable application domain (MoE routing) with a concrete baseline (cosine).
  - **confidence:** medium - both mechanisms genuinely sit on statistical manifolds so Fisher-Rao transfer is principled, but whether routing entropy admits a tractable Fisher-Rao geodesic is unverified.
  - **could_be_wrong_if:** the routing concentration matrix does not parameterize a smooth statistical manifold compatible with Fisher-Rao, in which case the link is merely shared 'information-geometry' vocabulary and the schedule transfer is a surface analogy.

  - _AGENT 5 audit:_ VALID (grounding=0.333)

**VERIFY (AGENT 4):** collision_found=False, 5 reformulations, 23 paper-like hits
- verify verdict reasoning_trace:
  - **step:** collision verdict CAND_018_005 (LOWEST MARGIN)
  - **inputs_seen:** 5 reformulations; Geometric Metrics for MoE Specialization (2604.14500) puts the Fisher metric ON routing distributions; Routing-Entropy-Regularization (2502.08083) regularizes routing entropy
  - **reasoning:** Concentration-entropy control (h=3) x Fisher-Rao cosine schedule (h=3). This is the closest to a collision: 2604.14500 derives the Fisher metric on routing distributions and proves specialization is approximate geodesic flow. But it uses this for METRICS / early-failure detection, NOT for an optimal annealing SCHEDULE of routing entropy that transfers the cosine-schedule-optimality theorem. So the specific transfer is unoccupied -- but only narrowly.
  - **decision:** no collision, LOW margin: 2604.14500 is adjacent (Fisher metric on routing) but does not schedule entropy; a reviewer could call this incremental
  - **confidence:** medium - the margin to 2604.14500 is thin
  - **could_be_wrong_if:** 2604.14500's geodesic-flow result already implies the optimal entropy schedule

  - _AGENT 5 audit:_ VALID - decision<->data: polarity=no_collision vs collision_found=False

**CROSS-CHECK (AGENT 4):** agent4_collision=False, mismatch_with_agent3=False
- crosscheck reasoning_trace:
  - **step:** independent re-verification CAND_018_005
  - **inputs_seen:** verifier verdict (no collision, lowest margin) + my fresh Fisher-metric re-search; 2604.14500 recurs
  - **reasoning:** My independent re-search reconfirms 2604.14500 as the near-collision: it DOES put the Fisher metric on routing distributions, but proves a geodesic-flow CHARACTERIZATION for failure detection, not an optimal entropy SCHEDULE transferring the cosine-schedule theorem. I uphold no-collision but, like the verifier, flag this as the thinnest margin of the five.
  - **decision:** confirm verifier no-collision; no mismatch (but lowest margin)
  - **confidence:** medium - 2604.14500 is genuinely close
  - **could_be_wrong_if:** 2604.14500's geodesic-flow result is judged to already imply the optimal entropy schedule, making this incremental


**GATES (MAIN - exact numbers):**

_Gate 1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) for CAND_018_005
  - **inputs_seen:** composite=0.45 from params={'novelty': 0.0, 'mechanism_present': 1.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} weights={'novelty': 0.55, 'mechanism_present': 0.2, 'quote_grounded': 0.15, 'cross_atom': 0.1}; novelty=1-paper_hits/20 with paper_hits=23 (AGENT 4 real hits)
  - **reasoning:** novelty (weight 0.55) is 0.0 from 23 paper-like hits; ceiling is novelty*0.55+0.45; to clear 0.90 needs novelty>=0.8182 i.e. <=4 paper hits.
  - **decision:** FAIL (0.45 < 0.9)
  - **confidence:** high - pure arithmetic over recorded counts
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits (23) or recorded unseen results (R5 violation upstream)


_Gate 2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) for CAND_018_005
  - **inputs_seen:** atoms used = ['R18_P1_S3', 'R18_P2_S2']; quarantine set = ['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** Fails iff either source atom id is on the quarantine blocklist.
  - **decision:** PASS (hits=[])
  - **confidence:** high - exact set membership
  - **could_be_wrong_if:** an atom id string-collides with a quarantined id without being the same atom


_Gate 3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) for CAND_018_005
  - **inputs_seen:** n_reformulations=5 (required 5); verifier_collision=False; crosscheck_overturned=False
  - **reasoning:** Passes only if >=5 real reformulations AND no verifier collision AND AGENT 4 cross-check did not overturn (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion of two agents' verdicts
  - **could_be_wrong_if:** both verify and crosscheck missed an existing paper occupying the fused niche (shared blind spot)


_Gate 4 Belinda strict: PASS_
  - **step:** Gate 4 (Belinda strict) for CAND_018_005
  - **inputs_seen:** mechanism causal verbs found=['regulates', 'transforms']; quote_len=67 (min 30); quote_grounded=True (atom R18_P1_S3)
  - **reasoning:** Requires a concrete causal mechanism verb AND a >=30-char verbatim quote substring of its named atom.
  - **decision:** PASS
  - **confidence:** high - regex verb match + exact substring containment
  - **could_be_wrong_if:** the mechanism is real but uses a causal verb outside the fixed Belinda vocab, or the quote is paraphrased


**SURVIVAL:** ELIMINATED at gate_1_composite

---
## STAGE 6 - SPARSE-ATOM ANALYSIS (R12: the key question)

- sub-mechanisms individually sparse (<10 hits): **11/11** (['R18_P1_S1', 'R18_P1_S2', 'R18_P1_S3', 'R18_P1_S4', 'R18_P1_S5', 'R18_P2_S1', 'R18_P2_S2', 'R18_P3_S1', 'R18_P3_S2', 'R18_P3_S3', 'R18_P3_S4'])
- per-candidate verifier paper-hits (sparsest pairs): **[20, 19, 18, 19, 23]** (min 18)
- Run 17 per-candidate verifier paper-hits: [38, 34, 30] (min 30)
- **pairing sparse atoms beat Run 17's min? True**

> Single-WebSearch per-atom counts are capped (~<=9), so all 11 sub-mechanisms register below the 10-hit flag; the MEANINGFUL signal is the spread (per-atom hits [1, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5]) and the per-candidate comparison below. When the sparsest cross-paper pairs were VERIFIED as fused niches, the verifier surfaced [20, 19, 18, 19, 23] paper-like hits per candidate (min 18), BELOW Run 17's min of 30; 3/5 candidates reached NONZERO novelty (best composite 0.505). So finer (sentence-level) granularity MEASURABLY reduced prior-art volume (~30+ down to 18) and lifted novelty off the floor for the first time across runs. BUT all 5 candidates STILL FAIL Gate 1: clearing it needs <= 3 paper-hits (composite >= 0.9), and best was 0.505. Verdict NICHE_NOT_FOUND (0 survivors). The fused niches re-broaden to the mature parent literatures (MoE routing/collapse, Fisher-Rao geometry, thermodynamic computing, directional statistics), so saturation HOLDS at sentence granularity -- but measurably LESS severely than Run 17.


---
## STAGE 7 - AGENT 5 reasoning-audit

- traces audited **63**, all-complete=True, non-fatal flags=29, **logic-breaks=0**, consistency checks fired=26
- **No logic-breaks: every decision followed from its inputs and agreed with the recorded data.**

**Non-fatal flags:**
- `atoms.overall` (AGENT_1_decomposer): ['low_inputs_grounding(0.0)']
- `atom.R18_P3_S1` (AGENT_1_decomposer): ['confidence:missing_rationale']
- `atom.R18_P3_S3` (AGENT_1_decomposer): ['confidence:missing_rationale']
- `atomsearch.R18_P2_S1` (AGENT_2_atom_search): ['confidence:missing_rationale']
- `atomsearch.R18_P3_S2` (AGENT_2_atom_search): ['low_inputs_grounding(0.143)']
- `atomsearch.R18_P3_S3` (AGENT_2_atom_search): ['confidence:missing_rationale']
- `verify.verdict.CAND_018_001` (AGENT_4_verifier): ['low_inputs_grounding(0.111)']
- `verify.reform.CAND_018_001.n1` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_001.n2` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_001.n3` (AGENT_4_verifier): ['confidence:missing_rationale']
- `verify.reform.CAND_018_001.n5` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_002.n1` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_002.n2` (AGENT_4_verifier): ['confidence:missing_rationale', 'low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_002.n3` (AGENT_4_verifier): ['confidence:missing_rationale', 'low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_002.n5` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_003.n1` (AGENT_4_verifier): ['confidence:missing_rationale', 'low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_003.n2` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_003.n4` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_003.n5` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.verdict.CAND_018_004` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_004.n1` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_004.n3` (AGENT_4_verifier): ['confidence:missing_rationale', 'low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_004.n4` (AGENT_4_verifier): ['confidence:missing_rationale', 'low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_004.n5` (AGENT_4_verifier): ['confidence:missing_rationale', 'low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_005.n1` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_005.n2` (AGENT_4_verifier): ['confidence:missing_rationale']
- `verify.reform.CAND_018_005.n3` (AGENT_4_verifier): ['confidence:missing_rationale']
- `verify.reform.CAND_018_005.n4` (AGENT_4_verifier): ['confidence:missing_rationale', 'low_inputs_grounding(0.0)']
- `verify.reform.CAND_018_005.n5` (AGENT_4_verifier): ['low_inputs_grounding(0.0)']

---
## END-TO-END VERDICT

Verbatim abstracts decomposed into 11 sentence-level atoms (each with rationale) -> per-atom saturation measured (11 sparse) -> 5 sparsest cross-paper pairs merged -> verified + cross-checked -> 4 gates with numeric rationale -> audited. **NICHE_NOT_FOUND.** Key finding (R12): pairing sparse atoms reduced prior-art volume below Run 17. 63 decision points, 0 logic-breaks. No step is a black box.

# Run 19 - REASONING TRANSPARENCY REPORT (epoch 1)
_generated 2026-06-01T22:44:29.466638+00:00 - persistent-param convergence + sentence decomposition_

**VERDICT: NICHE_NOT_FOUND** (0/5)  |  **avg_search_quality=0.7983** (delta None)  |  **avg_paper_hits=21.0** (delta None)  |  logic-breaks=0/61

> R12: convergence target = search_quality (label-driven ground truth). niche verdict is reported separately and is expected to stay 0 (saturation).

## CONVERGENCE STATE (persistent direction_params.json, R10)

- epoch (scored): **1**  ->  next epoch written: **2**
- params this epoch: `{'specificity': 0.5, 'mechanism_focus': 0.5, 'sparsity_seeking': 0.5, 'cross_paper_pairing': 0.5, 'collision_avoidance_phrasing': 0.5}`
- avg_search_quality = 0.7983 (formula avg_search_quality = sum_k(param_k * mean_dim_k)/sum_k(param_k)); dimension_means = {'specificity': 0.9913, 'mechanism_focus': 0.9535, 'sparsity_seeking': 0.7093, 'cross_paper_pairing': 0.8953, 'collision_avoidance': 0.4419}
- avg_paper_hits (per-candidate verify) = 21.0
- epoch_history len now 0; labels applied this epoch: 0 (baseline if 0)

## STAGE 0 - Atom sourcing (AGENT 1)

**Overall decomposition trace:**
- **step:** read direction_params (epoch 1) then decompose 3 verbatim abstracts
- **inputs_seen:** direction_params.params = all 0.5 (neutral baseline, no labels yet); 3 verbatim abstracts re-sourced this run (P1 Grassmannian MoE 4 sentences, P2 Fisher-Rao 2, P3 thermodynamic computing 4).
- **reasoning:** At epoch 1 the params are neutral (0.5), so sourcing has no directional bias yet; I reuse the same 3-paper corpus as Run 18 so future epochs' param nudges are the ONLY thing that changes the search behaviour (clean convergence experiment). I decompose each abstract into its distinct mechanism/clause atoms, keeping problem-statement (P1_S1) and gap (P3_S2) sentences as context (is_mechanism=false later) for contrast.
- **decision:** 10 atoms: P1->4, P2->2, P3->4; params recorded; baseline epoch.
- **confidence:** high - abstracts re-sourced verbatim this run; sentence boundaries are clear
- **could_be_wrong_if:** reusing the Run 18 corpus instead of fresh papers makes epoch 1 less independent -- mitigated because the convergence target is search_quality of the QUERIES, not the papers.


### R19_P1_S1 (P1, ml) hits=1 SPARSE mech=False
_softmax gating provides no principled sparsity-utilization control (problem statement)_  ·  `arXiv:2602.17798`
> Mixture-of-Experts models rely on learned routers to assign tokens to experts, yet standard softmax gating provides no principled mechanism to control the tradeoff between sparsity and utilization.
- **step:** P1 sentence 1
- **inputs_seen:** softmax-gating problem statement
- **reasoning:** Generic MoE motivation, not a transferable mechanism; predict dense-by-topic but will read as context.
- **decision:** keep as context atom (problem statement)
- **confidence:** high - clearly motivation
- **could_be_wrong_if:** the exact tradeoff phrasing is rarer than the concept


### R19_P1_S2 (P1, ml) hits=4 SPARSE mech=True
_gating weights arise from the concentration parameters of Matrix Bingham distributions on the Grassmannian manifold_  ·  `arXiv:2602.17798`
> Grassmannian MoE (GrMoE) is a routing framework that operates on the Grassmannian manifold of subspaces, where gating weights arise from the concentration parameters of Matrix Bingham distributions.
- **step:** P1 sentence 2
- **inputs_seen:** Matrix Bingham / Grassmannian-manifold gating
- **reasoning:** Exotic directional-statistics construct (Matrix Bingham gating) -- distinct from the entropy-control function; predict sparse.
- **decision:** keep as mechanism atom; predict sparse
- **confidence:** high - Bingham routing is unusual
- **could_be_wrong_if:** von Mises-Fisher routing makes it denser


### R19_P1_S3 (P1, ml) hits=3 SPARSE mech=True
_a concentration matrix continuously controls routing entropy, replacing discrete top-k with a smooth sparsity mechanism_  ·  `arXiv:2602.17798`
> This construction yields a single, interpretable knob -- the concentration matrix -- that continuously controls routing entropy, replacing discrete top-k selection with a smooth, geometrically principled sparsity mechanism.
- **step:** P1 sentence 3
- **inputs_seen:** concentration matrix controls routing entropy, replaces top-k
- **reasoning:** The functional knob (entropy control), separable from the Bingham generative story; predict moderate.
- **decision:** keep as mechanism atom; predict moderate
- **confidence:** medium - soft routing is active
- **could_be_wrong_if:** entropy-controlled routing is denser than expected


### R19_P1_S4 (P1, ml) hits=4 SPARSE mech=True
_amortized variational inference for posterior routing distributions -> uncertainty-aware assignment resisting collapse_  ·  `arXiv:2602.17798`
> The authors develop an amortized variational inference procedure for posterior routing distributions, enabling uncertainty-aware expert assignment that naturally resists expert collapse.
- **step:** P1 sentence 4
- **inputs_seen:** amortized VI for posterior routing distributions
- **reasoning:** A Bayesian inference mechanism for routing, separable from geometry; predict sparse-moderate.
- **decision:** keep as mechanism atom; predict sparse-moderate
- **confidence:** medium - VI-for-routing is narrow
- **could_be_wrong_if:** bare amortized VI pulls the VAE literature


### R19_P2_S1 (P2, ml) hits=5 SPARSE mech=True
_choosing the discretisation schedule via the information geometry of the induced probability path_  ·  `arXiv:2508.04884`
> The discretisation schedule for sampling from masked discrete diffusion models is chosen in terms of the information geometry of the induced probability path.
- **step:** P2 sentence 1
- **inputs_seen:** information geometry of the induced probability path for diffusion schedules
- **reasoning:** Framing-as-information-geometry; distinct from the specific Fisher-Rao result; predict sparse-moderate.
- **decision:** keep as mechanism atom; predict sparse-moderate
- **confidence:** medium
- **could_be_wrong_if:** 'probability path' pulls flow-matching literature


### R19_P2_S2 (P2, ml) hits=3 SPARSE mech=True
_the optimal schedule under the Fisher-Rao geometry recovers the cosine schedule_  ·  `arXiv:2508.04884`
> The optimal schedule under the Fisher-Rao geometry recovers the popularly-used cosine schedule.
- **step:** P2 sentence 2
- **inputs_seen:** Fisher-Rao-optimal schedule = cosine
- **reasoning:** Specific result: Fisher-Rao geometry -> cosine optimality; predict sparse.
- **decision:** keep as mechanism atom; predict sparse
- **confidence:** high - narrow result
- **could_be_wrong_if:** 'cosine schedule' dominates the query


### R19_P3_S1 (P3, physics) hits=3 SPARSE mech=True
_thermodynamic-computing hardware undergoes a stochastic process to sample from a distribution_  ·  `arXiv:2601.04358`
> In the paradigm of thermodynamic computing, instead of behaving deterministically, hardware undergoes a stochastic process in order to sample from a distribution of interest.
- **step:** P3 sentence 1
- **inputs_seen:** thermodynamic-computing stochastic-sampling hardware premise
- **reasoning:** The thermodynamic-computing paradigm; distinct from the EDDP result; predict moderate (niche field).
- **decision:** keep as mechanism atom; predict moderate
- **confidence:** medium
- **could_be_wrong_if:** field smaller (sparse) or 'stochastic sampling' broad (dense)


### R19_P3_S2 (P3, physics) hits=5 SPARSE mech=False
_a theoretical characterization of the resource cost of thermodynamic computation is still lacking (gap)_  ·  `arXiv:2601.04358`
> While it has been hypothesized that thermodynamic computers may achieve better energy efficiency and performance, a theoretical characterization of the resource cost of thermodynamic computations is still lacking.
- **step:** P3 sentence 2
- **inputs_seen:** resource-cost-characterization-is-lacking gap
- **reasoning:** Gap/motivation sentence; context not mechanism; predict moderate (tracks field size).
- **decision:** keep as context atom (gap)
- **confidence:** medium
- **could_be_wrong_if:** phrased generically enough to pull broad energy work


### R19_P3_S3 (P3, physics) hits=4 SPARSE mech=True
_fundamental trade-offs between computational accuracy, energy dissipation, and time_  ·  `arXiv:2601.04358`
> The paper analyzes the fundamental trade-offs between computational accuracy, energy dissipation, and time in thermodynamic computing.
- **step:** P3 sentence 3
- **inputs_seen:** accuracy/energy-dissipation/time trade-off
- **reasoning:** The trade-off triad; distinct from the specific EDDP metric; predict moderate.
- **decision:** keep as mechanism atom; predict moderate
- **confidence:** medium
- **could_be_wrong_if:** the triad framing is rarer than its pairwise parts


### R19_P3_S4 (P3, physics) hits=5 SPARSE mech=True
_geometric bounds on entropy production -> limits on the energy-delay-deficiency product (EDDP)_  ·  `arXiv:2601.04358`
> Using geometric bounds on entropy production, the authors derive general limits on the energy-delay-deficiency product (EDDP), a stochastic generalization of energy-time-accuracy tradeoff metrics.
- **step:** P3 sentence 4
- **inputs_seen:** geometric entropy-production bounds -> EDDP (coined metric)
- **reasoning:** Headline coined metric (EDDP) on entropy-production-bound machinery; predict sparse term, mature toolkit.
- **decision:** keep as mechanism atom; predict sparse (coined metric)
- **confidence:** high - EDDP is newly coined
- **could_be_wrong_if:** 'entropy production bounds' pulls the large stochastic-thermo literature


## STAGE 2 - Per-atom saturation (AGENT 2) [R10]
| atom | hits | sparse | mech |
|---|---|---|---|
| R19_P1_S1 | 1 | Y | n |
| R19_P1_S3 | 3 | Y | Y |
| R19_P2_S2 | 3 | Y | Y |
| R19_P3_S1 | 3 | Y | Y |
| R19_P1_S2 | 4 | Y | Y |
| R19_P1_S4 | 4 | Y | Y |
| R19_P3_S3 | 4 | Y | Y |
| R19_P2_S1 | 5 | Y | Y |
| R19_P3_S2 | 5 | Y | n |
| R19_P3_S4 | 5 | Y | Y |

## STAGE 3-5 - Per candidate (sparsest pairs)


### CAND_019_001 - Fisher-Rao-Optimal Annealing Schedules for Continuous MoE Routing Sparsity
`R19_P1_S3(h=3) x R19_P2_S2(h=3)` -> verify_hits=26, composite 0.45, survived=False, failed=['gate_1_composite']
**MERGE (A3):** An information-geometric objective regulates the concentration-matrix knob so that routing entropy is annealed along a Fisher-Rao-optimal trajectory during training, transforming discrete top-k expert selection into a smoothly scheduled sparsity that produces a principled curriculum from dense to sparse routing.
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: a single continuous concentration-matrix knob that geometrically controls routing entropy, replacing discrete top-k with smooth sparsity. B: under Fisher-Rao information geometry, the *optimal training schedule* provably recovers the cosine schedule.
  - **reasoning:** A gives a continuous control variable for sparsity but says nothing about how it should change over training; B gives a geometry-derived theory of *optimal scheduling* of a control variable (noise level) but for diffusion. I tried to transfer B's 'optimal schedule under Fisher-Rao geometry' machinery onto A's concentration-matrix knob, treating routing entropy as the scheduled quantity. I rejected the reverse transfer (using A's sparsity knob inside a diffusion model) as forced. The combination is non-trivial because both already live in information geometry: A's knob induces a curve on a statistical manifold of routing distributions, so B's Fisher-Rao optimal-schedule derivation is mathematically applicable rather than metaphorical — the open question is what curve falls out, not whether the vocabularies rhyme.
  - **decision:** Settle on deriving and testing a Fisher-Rao-optimal annealing schedule for the routing-entropy knob in MoE, because it converts A's static parameterization into a principled training curriculum using B's existing optimality result.
  - **confidence:** medium - the geometric framing genuinely composes, but whether MoE routing's Fisher-Rao geometry yields a clean schedule is unverified.
  - **could_be_wrong_if:** the concentration-matrix manifold's Fisher-Rao metric is degenerate or trivial, so the 'optimal schedule' is constant or arbitrary, making the merge a vocabulary analogy between two unrelated uses of 'geometry'.

**VERIFY (A4):** collision=False, 5 reformulations, 26 hits
  - **step:** collision verdict CAND_019_001
  - **inputs_seen:** 5 reformulations; ~24 paper-like hits; nearest Fisher-Rao+entropy work is in RL (2310.02951, 2403.19448) and metrics (2604.14500), not MoE entropy scheduling
  - **reasoning:** concentration-entropy control (h=3) x Fisher-Rao cosine schedule (h=3). No paper applies a Fisher-Rao-optimal annealing schedule to MoE routing entropy; the Fisher-Rao+entropy principle lives in RL (natural policy gradient flows) and in MoE METRICS (2604.14500), not as a routing SCHEDULE.
  - **decision:** no collision: fused niche unoccupied; high component volume
  - **confidence:** medium - the Fisher-Rao+entropy principle is mature in adjacent domains
  - **could_be_wrong_if:** an RL natural-policy-gradient schedule transfers directly to MoE routing under different words

**CROSS-CHECK (A4):** agent4_collision=False, mismatch=False
  - **step:** independent re-verification CAND_019_001
  - **inputs_seen:** verifier verdict (no collision) + my RL re-search; found Fisher-Rao entropy-regularised RL flows
  - **reasoning:** I tested whether the Fisher-Rao+entropy principle (which the verifier saw hints of) is already applied to routing. It is mature in RL (policy mirror descent / natural policy gradient) but NOT transferred to MoE routing schedules. Adjacent, not a collision. Uphold verifier.
  - **decision:** confirm verifier no-collision; no mismatch
  - **confidence:** medium - the principle is mature in RL
  - **could_be_wrong_if:** natural-policy-gradient routing has been published for MoE under different words

**GATES:**
_G1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) CAND_019_001
  - **inputs_seen:** composite=0.45 params={'novelty': 0.0, 'mechanism_present': 1.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} paper_hits=26
  - **reasoning:** novelty(0.55 wt)=0.0 from 26 hits; to clear 0.90 need <=3 hits.
  - **decision:** FAIL (0.45 < 0.9)
  - **confidence:** high - arithmetic
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits

_G2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) CAND_019_001
  - **inputs_seen:** atoms=['R19_P1_S3', 'R19_P2_S2'] quarantine=['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** fails iff a source atom is quarantined.
  - **decision:** PASS (hits=[])
  - **confidence:** high - set membership
  - **could_be_wrong_if:** atom id string-collides with a quarantined id

_G3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) CAND_019_001
  - **inputs_seen:** n_reform=5 (req 5); collision=False; overturned=False
  - **reasoning:** pass iff >=5 reformulations, no collision, not overturned (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion
  - **could_be_wrong_if:** both verify+crosscheck shared a blind spot

_G4 Belinda: PASS_
  - **step:** Gate 4 (Belinda) CAND_019_001
  - **inputs_seen:** verbs=['produces', 'regulates'] quote_len=70 grounded=True
  - **reasoning:** needs a causal verb + >=30-char verbatim quote substring.
  - **decision:** PASS
  - **confidence:** high - regex + substring
  - **could_be_wrong_if:** mechanism uses a verb outside the Belinda vocab

**SURVIVAL:** ELIMINATED at gate_1_composite

### CAND_019_002 - Thermodynamic MoE Routing via Concentration-Controlled Hardware Sampling
`R19_P1_S3(h=3) x R19_P3_S1(h=3)` -> verify_hits=20, composite 0.45, survived=False, failed=['gate_1_composite']
**MERGE (A3):** Mapping a Mixture-of-Experts concentration matrix onto a thermodynamic computer's physical temperature transforms routing-entropy control into a native hardware operation: raising the concentration parameter regulates the noise of a stochastic substrate, which then directly samples expert assignments from the induced routing distribution instead of computing a digital top-k.
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: a single continuous concentration-matrix knob that smoothly sets routing entropy, replacing discrete top-k expert selection with a geometric sparsity mechanism. B: thermodynamic computing where hardware behaves stochastically to physically sample from a target distribution.
  - **reasoning:** I tried to transfer A's continuous entropy-controlling parameter (the concentration matrix) into B's role of a physical control variable that sets the distribution a stochastic substrate samples from. The natural transfer is concentration -> hardware temperature/noise scale, because both A and B already operate on distributions: A *parameterizes* a routing distribution, B *physically samples* from a distribution. I rejected the weaker analogy of merely 'adding noise to top-k' because that keeps routing digital and discrete, contradicting A's smoothness. The combination is non-trivial because top-k is a non-sampling argmax-style op that has no natural thermodynamic realization, whereas A's smooth concentration formulation makes routing an honest distribution-sampling problem that thermodynamic hardware can execute natively — the geometry of A is precisely what licenses B's sampling to be the routing mechanism rather than a post-hoc perturbation.
  - **decision:** Settled on thermodynamic MoE routing where the concentration matrix is the physical temperature knob, because it converts A's mathematical knob into B's literal control parameter, yielding a falsifiable hardware-software co-design claim.
  - **confidence:** medium - the conceptual mapping (distribution-parameterizer to distribution-sampler) is tight, but physical realizability on real thermodynamic hardware is unproven.
  - **could_be_wrong_if:** thermodynamic hardware can only sample fixed energy-based distributions and cannot be conditioned on per-token concentration matrices fast enough, making the link a vocabulary analogy between 'entropy' in A and 'stochastic' in B rather than a shared sampling mechanism.

**VERIFY (A4):** collision=False, 5 reformulations, 20 hits
  - **step:** collision verdict CAND_019_002
  - **inputs_seen:** 5 reformulations; disjoint MoE-routing vs thermodynamic-hardware clusters; Extropic TSU / neutral-atom 2512.21142 hardware found but unfused with MoE concentration routing
  - **reasoning:** concentration-entropy control (h=3) x thermodynamic stochastic sampling (h=3). p-bit/EBM/TSU hardware is real and MoE concentration routing is real, but no paper runs MoE routing on a thermodynamic sampler.
  - **decision:** no collision: disjoint clusters, fusion unoccupied
  - **confidence:** high - clusters clearly separate
  - **could_be_wrong_if:** Extropic's EBM/pMoG sampler already realizes a thermodynamic MoE router

**CROSS-CHECK (A4):** agent4_collision=False, mismatch=False
  - **step:** independent re-verification CAND_019_002
  - **inputs_seen:** verifier verdict (no collision) + my vendor-hardware re-search; Extropic/Normal Computing TSU confirmed real
  - **reasoning:** The hardware exists (TSU samples from EBMs via Gibbs), but no source runs MoE concentration routing on it. Confirms the fusion is unoccupied.
  - **decision:** confirm verifier no-collision; no mismatch
  - **confidence:** high - hardware and MoE clusters clearly separate
  - **could_be_wrong_if:** Extropic's pMoG/EBM sampler is functionally a thermodynamic MoE router

**GATES:**
_G1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) CAND_019_002
  - **inputs_seen:** composite=0.45 params={'novelty': 0.0, 'mechanism_present': 1.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} paper_hits=20
  - **reasoning:** novelty(0.55 wt)=0.0 from 20 hits; to clear 0.90 need <=3 hits.
  - **decision:** FAIL (0.45 < 0.9)
  - **confidence:** high - arithmetic
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits

_G2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) CAND_019_002
  - **inputs_seen:** atoms=['R19_P1_S3', 'R19_P3_S1'] quarantine=['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** fails iff a source atom is quarantined.
  - **decision:** PASS (hits=[])
  - **confidence:** high - set membership
  - **could_be_wrong_if:** atom id string-collides with a quarantined id

_G3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) CAND_019_002
  - **inputs_seen:** n_reform=5 (req 5); collision=False; overturned=False
  - **reasoning:** pass iff >=5 reformulations, no collision, not overturned (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion
  - **could_be_wrong_if:** both verify+crosscheck shared a blind spot

_G4 Belinda: PASS_
  - **step:** Gate 4 (Belinda) CAND_019_002
  - **inputs_seen:** verbs=['regulates', 'transforms'] quote_len=70 grounded=True
  - **reasoning:** needs a causal verb + >=30-char verbatim quote substring.
  - **decision:** PASS
  - **confidence:** high - regex + substring
  - **could_be_wrong_if:** mechanism uses a verb outside the Belinda vocab

**SURVIVAL:** ELIMINATED at gate_1_composite

### CAND_019_003 - Fisher-Rao-optimal annealing schedules for thermodynamic sampling hardware
`R19_P2_S2(h=3) x R19_P3_S1(h=3)` -> verify_hits=24, composite 0.25, survived=False, failed=['gate_1_composite', 'gate_4_belinda']
**MERGE (A3):** An information-geometric optimal schedule derived from the Fisher-Rao metric routes how thermodynamic-computing hardware anneals its noise level, transforming the abstract cosine sampling schedule into a physical relaxation trajectory that the stochastic hardware natively executes to sample from a target distribution.
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: the variance/noise schedule that is optimal under Fisher-Rao information geometry coincides with the cosine schedule used in diffusion models. B: thermodynamic computing replaces deterministic logic with hardware that physically runs a stochastic process to draw samples from a target distribution.
  - **reasoning:** I tried to transfer A's notion of a geometrically-optimal schedule (the time-parameterization of noise that minimizes path length under the Fisher-Rao metric) onto B's physical sampling substrate, treating the hardware's annealing/relaxation timeline as the object that the schedule controls. I rejected the surface reading where 'schedule' is just a software hyperparameter bolted onto thermodynamic hardware, because that would be trivial reuse; the non-trivial claim is that the hardware's intrinsic stochastic relaxation already traces a metric on distribution space, so the Fisher-Rao optimum may either match or constrain what the physics can do, turning a software design choice into a physical-realizability question.
  - **decision:** I settled on studying whether thermodynamic hardware can natively realize the Fisher-Rao-optimal schedule, because both A and B operate on the same underlying object — a path through a manifold of probability distributions — making the link causal rather than merely lexical.
  - **confidence:** medium - both atoms genuinely concern trajectories over distribution manifolds, but whether hardware relaxation physically obeys the Fisher-Rao geometry is unverified.
  - **could_be_wrong_if:** thermodynamic hardware's relaxation dynamics are governed by a fixed physical metric unrelated to Fisher-Rao, so imposing the cosine schedule is just an external software clock and the merge collapses to vocabulary overlap on the word 'distribution'.

**VERIFY (A4):** collision=False, 5 reformulations, 24 hits
  - **step:** collision verdict CAND_019_003 (LOWEST MARGIN)
  - **inputs_seen:** 5 reformulations returning the Sivak-Crooks thermodynamic-length / optimal-driving-geodesic literature (1201.4166, 1208.4553, PhysRevResearch.4.043049, 1712.04311, 2402.14717)
  - **reasoning:** Fisher-Rao cosine schedule (h=3) x thermodynamic stochastic sampling (h=3). This is the closest to a collision in any run: the Sivak-Crooks result ALREADY establishes that optimal annealing/driving schedules are geodesics of the friction tensor (a Fisher-information-type metric) for thermodynamic systems. So 'Fisher-Rao-optimal annealing schedule for a thermodynamic process' is a KNOWN principle; only the narrow application to thermodynamic-sampling-HARDWARE is unclaimed.
  - **decision:** no collision at the strict fused-niche level, BUT lowest margin: the principle is established (Sivak-Crooks thermodynamic length); novelty is low even beyond the volume floor
  - **confidence:** medium - a reviewer could reasonably call this already known
  - **could_be_wrong_if:** the thermodynamic-length geodesic IS exactly the proposed schedule (then it is a genuine collision, not just adjacent)

**CROSS-CHECK (A4):** agent4_collision=False, mismatch=False
  - **step:** independent re-verification CAND_019_003
  - **inputs_seen:** verifier verdict (lowest margin) + my direct Sivak-Crooks re-search; thermodynamic-length geodesic = optimal schedule confirmed
  - **reasoning:** I probed the exact prior framework. Sivak-Crooks thermodynamic length ESTABLISHES that minimum-dissipation annealing schedules are geodesics of the friction (Fisher-type) metric. So the candidate's core claim is a known principle; only the application to thermodynamic-sampling-HARDWARE is unclaimed. I uphold the verifier's no-exact-collision verdict while strongly agreeing this is the lowest-novelty candidate -- it would likely fail external novelty review even setting aside the volume floor.
  - **decision:** confirm verifier no-collision; no mismatch (but lowest margin -- principle already established)
  - **confidence:** medium - genuinely borderline; a reviewer could call it a collision
  - **could_be_wrong_if:** the friction-tensor geodesic schedule IS the proposed schedule with no meaningful hardware-specific delta -> then it is a true collision

**GATES:**
_G1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) CAND_019_003
  - **inputs_seen:** composite=0.25 params={'novelty': 0.0, 'mechanism_present': 0.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} paper_hits=24
  - **reasoning:** novelty(0.55 wt)=0.0 from 24 hits; to clear 0.90 need <=3 hits.
  - **decision:** FAIL (0.25 < 0.9)
  - **confidence:** high - arithmetic
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits

_G2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) CAND_019_003
  - **inputs_seen:** atoms=['R19_P2_S2', 'R19_P3_S1'] quarantine=['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** fails iff a source atom is quarantined.
  - **decision:** PASS (hits=[])
  - **confidence:** high - set membership
  - **could_be_wrong_if:** atom id string-collides with a quarantined id

_G3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) CAND_019_003
  - **inputs_seen:** n_reform=5 (req 5); collision=False; overturned=False
  - **reasoning:** pass iff >=5 reformulations, no collision, not overturned (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion
  - **could_be_wrong_if:** both verify+crosscheck shared a blind spot

_G4 Belinda: FAIL_
  - **step:** Gate 4 (Belinda) CAND_019_003
  - **inputs_seen:** verbs=[] quote_len=90 grounded=True
  - **reasoning:** needs a causal verb + >=30-char verbatim quote substring.
  - **decision:** FAIL
  - **confidence:** high - regex + substring
  - **could_be_wrong_if:** mechanism uses a verb outside the Belinda vocab

**SURVIVAL:** ELIMINATED at gate_1_composite

### CAND_019_004 - Fisher-Rao-Optimal Concentration Scheduling for Grassmannian MoE Routing
`R19_P1_S2(h=4) x R19_P2_S2(h=3)` -> verify_hits=16, composite 0.56, survived=False, failed=['gate_1_composite']
**MERGE (A3):** A Fisher-Rao-optimal schedule transforms the concentration parameters of the Matrix Bingham gating distributions over training, so that GrMoE routing anneals along the natural information geometry of the Grassmannian manifold rather than via a hand-tuned heuristic, which regulates how sharply experts are selected as training progresses.
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: MoE gating where routing lives on a Grassmannian manifold and gate weights come from Matrix Bingham concentration parameters. B: under Fisher-Rao geometry, the derived optimal schedule reproduces the cosine schedule.
  - **reasoning:** I tried transferring B's mechanism — deriving a process schedule from Fisher-Rao information geometry — onto A's free parameters, namely the Matrix Bingham concentration values that set routing sharpness. I rejected the inverse transfer (putting B's diffusion process onto a Grassmannian) as a vague vocabulary match. The non-trivial link is that both objects are genuinely Riemannian: A's gating already lives on a Grassmannian whose Fisher-Rao metric is computable, so B's 'optimal schedule = geometry-induced curve' is not metaphorical — it gives a concrete metric to optimize the concentration trajectory, potentially yielding a cosine-analogue for routing temperature.
  - **decision:** Settle on a Fisher-Rao-derived annealing schedule for the Matrix Bingham concentration parameters in GrMoE, because both mechanisms share an actual manifold and metric, making the schedule derivable rather than analogized.
  - **confidence:** medium - the manifolds and metrics genuinely overlap, but the closed-form recovery may not hold for the Grassmannian-Bingham case
  - **could_be_wrong_if:** the Fisher-Rao metric on the Matrix Bingham/Grassmannian family does not admit a tractable optimal schedule, making the link a surface reuse of the word 'geometry' rather than a transferable derivation.

**VERIFY (A4):** collision=False, 5 reformulations, 16 hits
  - **step:** collision verdict CAND_019_004
  - **inputs_seen:** 5 reformulations; GrMoE and Fisher-Rao-cosine appear separately; neighbors RoMA/Spectral-Manifold/GeoMoE
  - **reasoning:** Matrix Bingham gating (h=4) x Fisher-Rao cosine schedule (h=3). Geometric/manifold routing is active but no paper applies a Fisher-Rao optimal SCHEDULE to Bingham concentration.
  - **decision:** no collision: fusion unoccupied; geometric-routing volume high
  - **confidence:** medium
  - **could_be_wrong_if:** a manifold-routing paper schedules concentration via information geometry

**CROSS-CHECK (A4):** agent4_collision=False, mismatch=False
  - **step:** independent re-verification CAND_019_004
  - **inputs_seen:** verifier verdict (no collision) + my vMF/curvature re-search; GeoMoE curvature routing found
  - **reasoning:** Geometric/curvature routing exists (GeoMoE) and vMF is the predecessor of GrMoE, but none apply a Fisher-Rao schedule to Bingham concentration. Confirms verifier.
  - **decision:** confirm verifier no-collision; no mismatch
  - **confidence:** medium - geometric routing active
  - **could_be_wrong_if:** GeoMoE's curvature schedule equals the Fisher-Rao concentration schedule

**GATES:**
_G1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) CAND_019_004
  - **inputs_seen:** composite=0.56 params={'novelty': 0.2, 'mechanism_present': 1.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} paper_hits=16
  - **reasoning:** novelty(0.55 wt)=0.2 from 16 hits; to clear 0.90 need <=3 hits.
  - **decision:** FAIL (0.56 < 0.9)
  - **confidence:** high - arithmetic
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits

_G2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) CAND_019_004
  - **inputs_seen:** atoms=['R19_P1_S2', 'R19_P2_S2'] quarantine=['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** fails iff a source atom is quarantined.
  - **decision:** PASS (hits=[])
  - **confidence:** high - set membership
  - **could_be_wrong_if:** atom id string-collides with a quarantined id

_G3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) CAND_019_004
  - **inputs_seen:** n_reform=5 (req 5); collision=False; overturned=False
  - **reasoning:** pass iff >=5 reformulations, no collision, not overturned (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion
  - **could_be_wrong_if:** both verify+crosscheck shared a blind spot

_G4 Belinda: PASS_
  - **step:** Gate 4 (Belinda) CAND_019_004
  - **inputs_seen:** verbs=['regulates', 'transforms'] quote_len=50 grounded=True
  - **reasoning:** needs a causal verb + >=30-char verbatim quote substring.
  - **decision:** PASS
  - **confidence:** high - regex + substring
  - **could_be_wrong_if:** mechanism uses a verb outside the Belinda vocab

**SURVIVAL:** ELIMINATED at gate_1_composite

### CAND_019_005 - Thermodynamic Sampling of Grassmannian Bingham Gates for MoE Routing
`R19_P1_S2(h=4) x R19_P3_S1(h=3)` -> verify_hits=19, composite 0.2775, survived=False, failed=['gate_1_composite', 'gate_4_belinda']
**MERGE (A3):** Thermodynamic-computing hardware undergoes a physical stochastic process that natively samples from the Matrix Bingham distribution over subspaces, which routes GrMoE expert selection on the Grassmannian manifold; the hardware's equilibrium dynamics produce gating draws directly from the concentration parameters instead of a deterministic softmax over precomputed weights.
  - **step:** merge ATOM A x ATOM B
  - **inputs_seen:** A: MoE routing where gating weights come from concentration parameters of Matrix Bingham distributions on the Grassmannian manifold of subspaces. B: thermodynamic computing where hardware behaves stochastically to sample from a distribution of interest rather than deterministically.
  - **reasoning:** I tried to transfer B's mechanism (hardware-native stochastic sampling from a target distribution) onto A's specific 'distribution of interest', the Matrix Bingham distribution over subspaces. I rejected the reverse transfer (using Grassmannian structure to describe thermodynamic state spaces) as vaguer and the alternative of merely adding noise to softmax gates as not exploiting either mechanism. The combination is non-trivial because Matrix Bingham / matrix Langevin distributions on Stiefel-Grassmann manifolds are genuinely hard to sample on digital hardware (rejection sampling scales poorly with dimension), and thermodynamic hardware is precisely a device that relaxes to sample from intractable Gibbs/Boltzmann distributions, so the two share the concrete computational bottleneck of sampling a constrained matrix distribution rather than just sharing the word 'distribution'.
  - **decision:** I settled on a niche where GrMoE's Matrix Bingham gating is implemented as the equilibrium sampling target of a thermodynamic sampler, because it identifies a real shared object (the Bingham distribution) that one mechanism needs sampled and the other can natively sample.
  - **confidence:** medium - the shared sampling bottleneck is concrete, but whether thermodynamic hardware can be physically biased to the exact Bingham concentration matrix is unverified
  - **could_be_wrong_if:** thermodynamic samplers cannot encode arbitrary Matrix Bingham concentration parameters in their physical couplings, in which case the link is just 'both involve probability distributions' — a vocabulary analogy with no transferable mechanism.

**VERIFY (A4):** collision=False, 5 reformulations, 19 hits
  - **step:** collision verdict CAND_019_005
  - **inputs_seen:** 5 reformulations; Bingham-sampling (directional stats) + physical Boltzmann samplers + neutral-atom thermo sampling all separate; reverse-direction 'MoE for thermo models' found, not the target
  - **reasoning:** Matrix Bingham gating (h=4) x thermodynamic stochastic sampling (h=3). Bingham sampling (2010.00137, 1310.8110), MoE-hardware, and physical Boltzmann/quantum samplers exist, but none draw Bingham MoE routing weights on a physical/thermodynamic sampler.
  - **decision:** no collision: fusion unoccupied
  - **confidence:** high - three-way separation
  - **could_be_wrong_if:** a p-bit/Boltzmann-sampler paper already gates experts via a directional distribution

**CROSS-CHECK (A4):** agent4_collision=False, mismatch=False
  - **step:** independent re-verification CAND_019_005
  - **inputs_seen:** verifier verdict (no collision) + my physical-Boltzmann-sampler re-search; p-bit/laser/quantum samplers found
  - **reasoning:** Physical Boltzmann samplers exist (p-bits, laser networks, quantum annealers) but none gate MoE experts via a directional (Bingham) distribution. Confirms verifier.
  - **decision:** confirm verifier no-collision; no mismatch
  - **confidence:** high - no categorical-gate/expert-routing hit in the hardware-sampler cluster
  - **could_be_wrong_if:** a p-bit paper implements categorical expert gating

**GATES:**
_G1 composite>=0.90: FAIL_
  - **step:** Gate 1 (composite>=0.90) CAND_019_005
  - **inputs_seen:** composite=0.2775 params={'novelty': 0.05, 'mechanism_present': 0.0, 'quote_grounded': 1.0, 'cross_atom': 1.0} paper_hits=19
  - **reasoning:** novelty(0.55 wt)=0.05 from 19 hits; to clear 0.90 need <=3 hits.
  - **decision:** FAIL (0.2775 < 0.9)
  - **confidence:** high - arithmetic
  - **could_be_wrong_if:** AGENT 4 miscounted paper-like hits

_G2 quarantine: PASS_
  - **step:** Gate 2 (quarantine) CAND_019_005
  - **inputs_seen:** atoms=['R19_P1_S2', 'R19_P3_S1'] quarantine=['ARXIV_R10_evodevo', 'ARXIV_R10_market_making', 'ARXIV_R10_thermodynamics', 'KP_E2_A06', 'PG_E1_A05']
  - **reasoning:** fails iff a source atom is quarantined.
  - **decision:** PASS (hits=[])
  - **confidence:** high - set membership
  - **could_be_wrong_if:** atom id string-collides with a quarantined id

_G3 verify XOR crosscheck: PASS_
  - **step:** Gate 3 (verify XOR crosscheck) CAND_019_005
  - **inputs_seen:** n_reform=5 (req 5); collision=False; overturned=False
  - **reasoning:** pass iff >=5 reformulations, no collision, not overturned (R7).
  - **decision:** PASS
  - **confidence:** high - boolean fusion
  - **could_be_wrong_if:** both verify+crosscheck shared a blind spot

_G4 Belinda: FAIL_
  - **step:** Gate 4 (Belinda) CAND_019_005
  - **inputs_seen:** verbs=[] quote_len=50 grounded=True
  - **reasoning:** needs a causal verb + >=30-char verbatim quote substring.
  - **decision:** FAIL
  - **confidence:** high - regex + substring
  - **could_be_wrong_if:** mechanism uses a verb outside the Belinda vocab

**SURVIVAL:** ELIMINATED at gate_1_composite

## STAGE 6 - AGENT 5 audit + search-quality

- traces 61, complete 61, **logic-breaks 0**, consistency checks 25, non-fatal flags 32
- search_quality over 43 real queries: dimension_means {'specificity': 0.9913, 'mechanism_focus': 0.9535, 'sparsity_seeking': 0.7093, 'cross_paper_pairing': 0.8953, 'collision_avoidance': 0.4419}, **avg_search_quality 0.7983**

## END-TO-END (epoch 1)

Persistent params {'specificity': 0.5, 'mechanism_focus': 0.5, 'sparsity_seeking': 0.5, 'cross_paper_pairing': 0.5, 'collision_avoidance_phrasing': 0.5} -> sourced+decomposed -> per-atom saturation -> sparsest pairs merged -> verified+crosschecked -> 4 gates -> audited. **NICHE_NOT_FOUND** (0 survivors). avg_search_quality=0.7983 (delta None), avg_paper_hits=21.0 (delta None). 61 decision points, 0 logic-breaks. Convergence target is search_quality; niche saturation is expected and reported honestly (R12).

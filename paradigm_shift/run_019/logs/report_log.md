# [REPORT] Run 19 ground-truth log
# generated 2026-06-01T22:44:02.368860+00:00
# Each block is a subagent's raw output, injected verbatim.


## [REPORT 1] atoms (verbatim)

### atoms.json
```json
{
  "run_id": "run_019",
  "epoch": 1,
  "agent": "1_sourcer_decomposer",
  "params_read": {"specificity": 0.5, "mechanism_focus": 0.5, "sparsity_seeking": 0.5, "cross_paper_pairing": 0.5, "collision_avoidance_phrasing": 0.5},
  "params_note": "epoch 1 baseline: all params 0.5 (neutral) -> no directional sourcing bias. Same 3-paper corpus as Run 18 is reused so the multi-epoch experiment ISOLATES the param effect; abstracts were re-sourced FRESH this run (R9).",
  "verbatim_note": "Each atom text is one verbatim sentence/clause of the abstract as WebSearch rendered it THIS run (clean text; first-person sometimes rendered third-person). Titles/URLs verbatim from Links. WebFetch 403s. No id/text invented.",
  "queries_used": [
    "arxiv 2602.17798 Grassmannian Mixture-of-Experts Concentration-Controlled Routing on Subspace Manifolds abstract",
    "arxiv 2508.04884 The Cosine Schedule is Fisher-Rao-Optimal for Masked Discrete Diffusion Models abstract",
    "arxiv 2601.04358 Energy-Time-Accuracy Tradeoffs in Thermodynamic Computing abstract"
  ],
  "source_papers": [
    {"paper_id": "P1", "source_id": "arXiv:2602.17798", "title": "Grassmannian Mixture-of-Experts: Concentration-Controlled Routing on Subspace Manifolds", "url": "https://arxiv.org/abs/2602.17798", "domain": "ml"},
    {"paper_id": "P2", "source_id": "arXiv:2508.04884", "title": "The Cosine Schedule is Fisher-Rao-Optimal for Masked Discrete Diffusion Models", "url": "https://arxiv.org/abs/2508.04884", "domain": "ml"},
    {"paper_id": "P3", "source_id": "arXiv:2601.04358", "title": "Energy-Time-Accuracy Tradeoffs in Thermodynamic Computing", "url": "https://arxiv.org/abs/2601.04358", "domain": "physics"}
  ],
  "atoms": [
    {"atom_id": "R19_P1_S1", "paper_id": "P1", "source_id": "arXiv:2602.17798", "url": "https://arxiv.org/abs/2602.17798", "domain": "ml",
     "sub_mechanism": "softmax gating provides no principled sparsity-utilization control (problem statement)",
     "text": "Mixture-of-Experts models rely on learned routers to assign tokens to experts, yet standard softmax gating provides no principled mechanism to control the tradeoff between sparsity and utilization."},
    {"atom_id": "R19_P1_S2", "paper_id": "P1", "source_id": "arXiv:2602.17798", "url": "https://arxiv.org/abs/2602.17798", "domain": "ml",
     "sub_mechanism": "gating weights arise from the concentration parameters of Matrix Bingham distributions on the Grassmannian manifold",
     "text": "Grassmannian MoE (GrMoE) is a routing framework that operates on the Grassmannian manifold of subspaces, where gating weights arise from the concentration parameters of Matrix Bingham distributions."},
    {"atom_id": "R19_P1_S3", "paper_id": "P1", "source_id": "arXiv:2602.17798", "url": "https://arxiv.org/abs/2602.17798", "domain": "ml",
     "sub_mechanism": "a concentration matrix continuously controls routing entropy, replacing discrete top-k with a smooth sparsity mechanism",
     "text": "This construction yields a single, interpretable knob -- the concentration matrix -- that continuously controls routing entropy, replacing discrete top-k selection with a smooth, geometrically principled sparsity mechanism."},
    {"atom_id": "R19_P1_S4", "paper_id": "P1", "source_id": "arXiv:2602.17798", "url": "https://arxiv.org/abs/2602.17798", "domain": "ml",
     "sub_mechanism": "amortized variational inference for posterior routing distributions -> uncertainty-aware assignment resisting collapse",
     "text": "The authors develop an amortized variational inference procedure for posterior routing distributions, enabling uncertainty-aware expert assignment that naturally resists expert collapse."},
    {"atom_id": "R19_P2_S1", "paper_id": "P2", "source_id": "arXiv:2508.04884", "url": "https://arxiv.org/abs/2508.04884", "domain": "ml",
     "sub_mechanism": "choosing the discretisation schedule via the information geometry of the induced probability path",
     "text": "The discretisation schedule for sampling from masked discrete diffusion models is chosen in terms of the information geometry of the induced probability path."},
    {"atom_id": "R19_P2_S2", "paper_id": "P2", "source_id": "arXiv:2508.04884", "url": "https://arxiv.org/abs/2508.04884", "domain": "ml",
     "sub_mechanism": "the optimal schedule under the Fisher-Rao geometry recovers the cosine schedule",
     "text": "The optimal schedule under the Fisher-Rao geometry recovers the popularly-used cosine schedule."},
    {"atom_id": "R19_P3_S1", "paper_id": "P3", "source_id": "arXiv:2601.04358", "url": "https://arxiv.org/abs/2601.04358", "domain": "physics",
     "sub_mechanism": "thermodynamic-computing hardware undergoes a stochastic process to sample from a distribution",
     "text": "In the paradigm of thermodynamic computing, instead of behaving deterministically, hardware undergoes a stochastic process in order to sample from a distribution of interest."},
    {"atom_id": "R19_P3_S2", "paper_id": "P3", "source_id": "arXiv:2601.04358", "url": "https://arxiv.org/abs/2601.04358", "domain": "physics",
     "sub_mechanism": "a theoretical characterization of the resource cost of thermodynamic computation is still lacking (gap)",
     "text": "While it has been hypothesized that thermodynamic computers may achieve better energy efficiency and performance, a theoretical characterization of the resource cost of thermodynamic computations is still lacking."},
    {"atom_id": "R19_P3_S3", "paper_id": "P3", "source_id": "arXiv:2601.04358", "url": "https://arxiv.org/abs/2601.04358", "domain": "physics",
     "sub_mechanism": "fundamental trade-offs between computational accuracy, energy dissipation, and time",
     "text": "The paper analyzes the fundamental trade-offs between computational accuracy, energy dissipation, and time in thermodynamic computing."},
    {"atom_id": "R19_P3_S4", "paper_id": "P3", "source_id": "arXiv:2601.04358", "url": "https://arxiv.org/abs/2601.04358", "domain": "physics",
     "sub_mechanism": "geometric bounds on entropy production -> limits on the energy-delay-deficiency product (EDDP)",
     "text": "Using geometric bounds on entropy production, the authors derive general limits on the energy-delay-deficiency product (EDDP), a stochastic generalization of energy-time-accuracy tradeoff metrics."}
  ]
}
```

### atoms_reasoning.json
```json
{
  "run_id": "run_019",
  "agent": "1_sourcer_decomposer",
  "note": "reasoning_trace per atom (which abstract sentence, why distinct, predicted density) + overall trace recording that params were read. R9/R10.",
  "overall_trace": {
    "step": "read direction_params (epoch 1) then decompose 3 verbatim abstracts",
    "inputs_seen": "direction_params.params = all 0.5 (neutral baseline, no labels yet); 3 verbatim abstracts re-sourced this run (P1 Grassmannian MoE 4 sentences, P2 Fisher-Rao 2, P3 thermodynamic computing 4).",
    "reasoning": "At epoch 1 the params are neutral (0.5), so sourcing has no directional bias yet; I reuse the same 3-paper corpus as Run 18 so future epochs' param nudges are the ONLY thing that changes the search behaviour (clean convergence experiment). I decompose each abstract into its distinct mechanism/clause atoms, keeping problem-statement (P1_S1) and gap (P3_S2) sentences as context (is_mechanism=false later) for contrast.",
    "decision": "10 atoms: P1->4, P2->2, P3->4; params recorded; baseline epoch.",
    "confidence": "high - abstracts re-sourced verbatim this run; sentence boundaries are clear",
    "could_be_wrong_if": "reusing the Run 18 corpus instead of fresh papers makes epoch 1 less independent -- mitigated because the convergence target is search_quality of the QUERIES, not the papers."
  },
  "atom_traces": [
    {"atom_id": "R19_P1_S1", "reasoning_trace": {"step": "P1 sentence 1", "inputs_seen": "softmax-gating problem statement", "reasoning": "Generic MoE motivation, not a transferable mechanism; predict dense-by-topic but will read as context.", "decision": "keep as context atom (problem statement)", "confidence": "high - clearly motivation", "could_be_wrong_if": "the exact tradeoff phrasing is rarer than the concept"}},
    {"atom_id": "R19_P1_S2", "reasoning_trace": {"step": "P1 sentence 2", "inputs_seen": "Matrix Bingham / Grassmannian-manifold gating", "reasoning": "Exotic directional-statistics construct (Matrix Bingham gating) -- distinct from the entropy-control function; predict sparse.", "decision": "keep as mechanism atom; predict sparse", "confidence": "high - Bingham routing is unusual", "could_be_wrong_if": "von Mises-Fisher routing makes it denser"}},
    {"atom_id": "R19_P1_S3", "reasoning_trace": {"step": "P1 sentence 3", "inputs_seen": "concentration matrix controls routing entropy, replaces top-k", "reasoning": "The functional knob (entropy control), separable from the Bingham generative story; predict moderate.", "decision": "keep as mechanism atom; predict moderate", "confidence": "medium - soft routing is active", "could_be_wrong_if": "entropy-controlled routing is denser than expected"}},
    {"atom_id": "R19_P1_S4", "reasoning_trace": {"step": "P1 sentence 4", "inputs_seen": "amortized VI for posterior routing distributions", "reasoning": "A Bayesian inference mechanism for routing, separable from geometry; predict sparse-moderate.", "decision": "keep as mechanism atom; predict sparse-moderate", "confidence": "medium - VI-for-routing is narrow", "could_be_wrong_if": "bare amortized VI pulls the VAE literature"}},
    {"atom_id": "R19_P2_S1", "reasoning_trace": {"step": "P2 sentence 1", "inputs_seen": "information geometry of the induced probability path for diffusion schedules", "reasoning": "Framing-as-information-geometry; distinct from the specific Fisher-Rao result; predict sparse-moderate.", "decision": "keep as mechanism atom; predict sparse-moderate", "confidence": "medium", "could_be_wrong_if": "'probability path' pulls flow-matching literature"}},
    {"atom_id": "R19_P2_S2", "reasoning_trace": {"step": "P2 sentence 2", "inputs_seen": "Fisher-Rao-optimal schedule = cosine", "reasoning": "Specific result: Fisher-Rao geometry -> cosine optimality; predict sparse.", "decision": "keep as mechanism atom; predict sparse", "confidence": "high - narrow result", "could_be_wrong_if": "'cosine schedule' dominates the query"}},
    {"atom_id": "R19_P3_S1", "reasoning_trace": {"step": "P3 sentence 1", "inputs_seen": "thermodynamic-computing stochastic-sampling hardware premise", "reasoning": "The thermodynamic-computing paradigm; distinct from the EDDP result; predict moderate (niche field).", "decision": "keep as mechanism atom; predict moderate", "confidence": "medium", "could_be_wrong_if": "field smaller (sparse) or 'stochastic sampling' broad (dense)"}},
    {"atom_id": "R19_P3_S2", "reasoning_trace": {"step": "P3 sentence 2", "inputs_seen": "resource-cost-characterization-is-lacking gap", "reasoning": "Gap/motivation sentence; context not mechanism; predict moderate (tracks field size).", "decision": "keep as context atom (gap)", "confidence": "medium", "could_be_wrong_if": "phrased generically enough to pull broad energy work"}},
    {"atom_id": "R19_P3_S3", "reasoning_trace": {"step": "P3 sentence 3", "inputs_seen": "accuracy/energy-dissipation/time trade-off", "reasoning": "The trade-off triad; distinct from the specific EDDP metric; predict moderate.", "decision": "keep as mechanism atom; predict moderate", "confidence": "medium", "could_be_wrong_if": "the triad framing is rarer than its pairwise parts"}},
    {"atom_id": "R19_P3_S4", "reasoning_trace": {"step": "P3 sentence 4", "inputs_seen": "geometric entropy-production bounds -> EDDP (coined metric)", "reasoning": "Headline coined metric (EDDP) on entropy-production-bound machinery; predict sparse term, mature toolkit.", "decision": "keep as mechanism atom; predict sparse (coined metric)", "confidence": "high - EDDP is newly coined", "could_be_wrong_if": "'entropy production bounds' pulls the large stochastic-thermo literature"}}
  ]
}
```

## [REPORT 2] atom_search (verbatim)

### atom_search.json
```json
{
  "run_id": "run_019",
  "epoch": 1,
  "agent": "2_atom_saturation_searcher",
  "counting_rule": "paper_hits = distinct non-source research papers (paper-like URLs, deduped) returned by this atom's single WebSearch, excluding the source paper and non-paper padding (wikipedia, vendor/explainer blogs, topic pages, listings). R5 verbatim results; R10 per-atom counts.",
  "caveat": "Single-WebSearch counts are capped (~<=9) so they UNDERSTATE corpus volume; meaningful uses are the relative ranking (merger) and the contrast with AGENT 4's per-candidate 5-reformulation counts. sparse flag = paper_hits<10. is_mechanism=false marks problem-statement/gap context sentences (excluded from pairing).",
  "atoms": [
    {"atom_id": "R19_P1_S1", "paper_id": "P1", "is_mechanism": false, "query": "mixture of experts softmax gating sparsity utilization tradeoff router", "paper_hits": 1, "sparse": true,
     "results": [{"title": "Grassmannian MoE (SOURCE)", "url": "https://arxiv.org/abs/2602.17798"}, {"title": "Convergence Rates for Softmax Gating Mixture of Experts", "url": "https://arxiv.org/pdf/2503.03213"}, {"title": "ProjectPro / EmergentMind / IBM / HuggingFace / AIWeekly (blogs, non-paper)", "url": "https://huggingface.co/blog/moe"}],
     "reasoning_trace": {"step": "saturation R19_P1_S1", "inputs_seen": "softmax-gating problem statement; source + 5 blogs + 1 paper", "reasoning": "generic MoE motivation; query pulled blogs + source; 1 distinct paper. Context atom.", "decision": "sparse by count (1) but is_mechanism=false (problem statement) -> excluded", "confidence": "high - clearly motivation", "could_be_wrong_if": "the tradeoff phrasing is itself a citable mechanism"}},
    {"atom_id": "R19_P1_S2", "paper_id": "P1", "is_mechanism": true, "query": "Matrix Bingham distribution gating weights Grassmannian manifold subspaces mixture of experts routing", "paper_hits": 4, "sparse": true,
     "results": [{"title": "Grassmannian MoE (SOURCE)", "url": "https://arxiv.org/abs/2602.17798"}, {"title": "Routing Manifold Alignment Improves Generalization of MoE LLMs", "url": "https://arxiv.org/pdf/2511.07419"}, {"title": "EMoE: Eigenbasis-Guided Routing for Mixture-of-Experts", "url": "https://arxiv.org/pdf/2601.12137"}, {"title": "Learning Subspaces of Different Dimensions (Lekheng, UChicago)", "url": "https://www.stat.uchicago.edu/~lekheng/work/mixture.pdf"}, {"title": "Selective Sinkhorn Routing for Improved Sparse Mixture of Experts", "url": "https://arxiv.org/pdf/2511.08972"}],
     "reasoning_trace": {"step": "saturation R19_P1_S2", "inputs_seen": "Matrix Bingham / Grassmannian gating; source + 4 distinct geometric-routing papers (none using Bingham)", "reasoning": "exotic directional-statistics construct; 4 distinct neighbors use other geometric ideas, not Bingham. Sparse mechanism.", "decision": "sparse: 4 distinct non-source papers; is_mechanism=true", "confidence": "high - Bingham routing is rare", "could_be_wrong_if": "von Mises-Fisher routing is denser under other names"}},
    {"atom_id": "R19_P1_S3", "paper_id": "P1", "is_mechanism": true, "query": "concentration matrix continuously controls routing entropy replacing top-k smooth sparsity mixture of experts", "paper_hits": 3, "sparse": true,
     "results": [{"title": "Grassmannian MoE (SOURCE)", "url": "https://arxiv.org/pdf/2602.17798"}, {"title": "ReMoE: Fully Differentiable MoE with ReLU Routing", "url": "https://arxiv.org/pdf/2412.14711"}, {"title": "DirMoE: Dirichlet-routed Mixture of Experts", "url": "https://arxiv.org/pdf/2602.09001"}, {"title": "LD-MoLE: Learnable Dynamic Routing for Mixture of LoRA Experts", "url": "https://arxiv.org/pdf/2509.25684"}],
     "reasoning_trace": {"step": "saturation R19_P1_S3", "inputs_seen": "entropy-controlled routing replacing top-k; source + 3 soft/differentiable routing papers", "reasoning": "soft routing alternatives exist (ReMoE, DirMoE, LD-MoLE); 3 distinct neighbors. Moderately sparse.", "decision": "sparse: 3 distinct non-source papers; is_mechanism=true", "confidence": "medium - soft routing active", "could_be_wrong_if": "'replacing top-k' broadly pulls soft-MoE literature"}},
    {"atom_id": "R19_P1_S4", "paper_id": "P1", "is_mechanism": true, "query": "amortized variational inference posterior routing distributions uncertainty-aware expert assignment mixture of experts", "paper_hits": 4, "sparse": true,
     "results": [{"title": "Grassmannian MoE (SOURCE)", "url": "https://arxiv.org/html/2602.17798v1"}, {"title": "Variational Routing: Scalable Bayesian Framework for Calibrated MoE Transformers", "url": "https://arxiv.org/abs/2603.09453"}, {"title": "Improved variational inference with dynamic routing flow (Springer)", "url": "https://link.springer.com/article/10.1007/s13042-019-00974-x"}, {"title": "Variational Inference, Entropy, and Orthogonality: Unified Theory of MoE", "url": "https://arxiv.org/pdf/2601.03577"}, {"title": "DirMoE: Dirichlet-routed Mixture of Experts", "url": "https://arxiv.org/pdf/2602.09001"}],
     "reasoning_trace": {"step": "saturation R19_P1_S4", "inputs_seen": "amortized VI for posterior routing; source + 4 Bayesian/VI-routing papers", "reasoning": "Bayesian/variational MoE routing is a small real cluster; 4 distinct neighbors.", "decision": "sparse: 4 distinct non-source papers; is_mechanism=true", "confidence": "medium - VI-for-routing emerging", "could_be_wrong_if": "bare amortized VI pulls the VAE literature"}},
    {"atom_id": "R19_P2_S1", "paper_id": "P2", "is_mechanism": true, "query": "information geometry induced probability path discretisation schedule masked discrete diffusion sampling", "paper_hits": 5, "sparse": true,
     "results": [{"title": "Cosine Schedule is Fisher-Rao-Optimal (SOURCE)", "url": "https://arxiv.org/abs/2508.04884"}, {"title": "Information-Geometric Adaptive Sampling for Graph Diffusion", "url": "https://arxiv.org/html/2605.00250"}, {"title": "Error Bounds and Optimal Schedules for Masked Diffusions", "url": "https://arxiv.org/pdf/2510.25544"}, {"title": "Path Planning for Masked Diffusion Model Sampling", "url": "https://arxiv.org/abs/2502.03540"}, {"title": "Improved Sampling Schedules for Discrete Diffusion Models", "url": "https://arxiv.org/pdf/2602.06849"}, {"title": "Why Masking Diffusion Works: Condition on the Jump Schedule", "url": "https://arxiv.org/pdf/2506.08316"}],
     "reasoning_trace": {"step": "saturation R19_P2_S1", "inputs_seen": "information geometry of probability path for diffusion schedules; source + 5 distinct schedule papers", "reasoning": "masked-diffusion scheduling is moderately active; 5 distinct neighbors incl. one other info-geometric sampling paper (2605.00250).", "decision": "sparse-ish: 5 distinct non-source papers; is_mechanism=true", "confidence": "medium", "could_be_wrong_if": "'probability path' pulls flow-matching literature"}},
    {"atom_id": "R19_P2_S2", "paper_id": "P2", "is_mechanism": true, "query": "Fisher-Rao geometry optimal schedule recovers cosine schedule masked discrete diffusion", "paper_hits": 3, "sparse": true,
     "results": [{"title": "Cosine Schedule is Fisher-Rao-Optimal (SOURCE)", "url": "https://arxiv.org/abs/2508.04884"}, {"title": "An Elementary Approach to Scheduling in Generative Diffusion Models", "url": "https://arxiv.org/pdf/2601.13602"}, {"title": "Learnable Sampler Distillation for Discrete Diffusion Models", "url": "https://arxiv.org/html/2509.19962v1"}, {"title": "Error Bounds and Optimal Schedules for Masked Diffusions", "url": "https://arxiv.org/html/2510.25544v1"}, {"title": "EmergentMind cosine / fisher-rao topics (non-paper)", "url": "https://www.emergentmind.com/topics/fisher-rao-geometry"}],
     "reasoning_trace": {"step": "saturation R19_P2_S2", "inputs_seen": "Fisher-Rao-optimal = cosine; source + 3 distinct schedule papers (none using Fisher-Rao) + 2 explainer topics", "reasoning": "specific result; neighbors are other optimal-schedule papers not using Fisher-Rao. 3 distinct.", "decision": "sparse: 3 distinct non-source papers; is_mechanism=true", "confidence": "high - narrow result", "could_be_wrong_if": "'cosine schedule' pulls broad scheduling literature"}},
    {"atom_id": "R19_P3_S1", "paper_id": "P3", "is_mechanism": true, "query": "thermodynamic computing hardware stochastic process sample from distribution of interest", "paper_hits": 3, "sparse": true,
     "results": [{"title": "Energy-Time-Accuracy Tradeoffs in Thermodynamic Computing (SOURCE)", "url": "https://arxiv.org/abs/2601.04358"}, {"title": "Thermodynamic computing system for AI applications (Nature Comms)", "url": "https://www.nature.com/articles/s41467-025-59011-x"}, {"title": "Thermodynamic Computing System for AI Applications (arXiv)", "url": "https://arxiv.org/html/2312.04836v1"}, {"title": "Generative thermodynamic computing (ResearchGate)", "url": "https://www.researchgate.net/publication/392942994_Generative_thermodynamic_computing"}, {"title": "Wikipedia / Normal Computing blogs / statmodeling (non-paper)", "url": "https://en.wikipedia.org/wiki/Thermodynamic_computing"}],
     "reasoning_trace": {"step": "saturation R19_P3_S1", "inputs_seen": "thermodynamic-computing stochastic-sampling premise; source + ~3 distinct papers + wikipedia/vendor blogs", "reasoning": "niche field dominated by a few groups; distinct works = the AI-applications paper (Nature/arXiv, likely one work) + Generative thermodynamic computing. Counted 3 conservatively.", "decision": "sparse: ~3 distinct non-source papers (niche field, much padding); is_mechanism=true", "confidence": "medium - preprint/journal dup makes count +-1", "could_be_wrong_if": "Nature s41467 and arXiv 2312.04836 are the same work (then 2)"}},
    {"atom_id": "R19_P3_S2", "paper_id": "P3", "is_mechanism": false, "query": "theoretical characterization resource cost thermodynamic computation energy efficiency performance", "paper_hits": 5, "sparse": true,
     "results": [{"title": "Energy-Time-Accuracy Tradeoffs (SOURCE)", "url": "https://arxiv.org/abs/2601.04358"}, {"title": "The Stochastic Thermodynamics of Computation", "url": "https://arxiv.org/html/1905.05669"}, {"title": "Is stochastic thermodynamics the key... (PNAS)", "url": "https://www.pnas.org/doi/10.1073/pnas.2321112121"}, {"title": "Landauer Principle and Thermodynamics of Computation", "url": "https://arxiv.org/pdf/2506.10876"}, {"title": "Efficiency optimization in quantum computing (PMC)", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10894240/"}, {"title": "Revisiting thermodynamics in computation and information theory", "url": "https://arxiv.org/pdf/2102.09981"}],
     "reasoning_trace": {"step": "saturation R19_P3_S2", "inputs_seen": "resource-cost gap sentence; source + 5 distinct thermo-of-computation papers", "reasoning": "gap/motivation sentence pulling the broad stochastic-thermo-of-computation literature. Context, not mechanism.", "decision": "sparse by count (5) but is_mechanism=false (gap statement) -> excluded", "confidence": "high - clearly a gap sentence", "could_be_wrong_if": "'resource cost characterization' is itself a citable contribution"}},
    {"atom_id": "R19_P3_S3", "paper_id": "P3", "is_mechanism": true, "query": "tradeoff computational accuracy energy dissipation time thermodynamic computing", "paper_hits": 4, "sparse": true,
     "results": [{"title": "Energy-Time-Accuracy Tradeoffs (SOURCE)", "url": "https://arxiv.org/abs/2601.04358"}, {"title": "Balancing error and dissipation in computing (Phys. Rev. Research / 1909.06650)", "url": "https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.2.033524"}, {"title": "Shortcuts to Thermodynamic Computing (Springer)", "url": "https://link.springer.com/article/10.1007/s10955-022-02871-0"}, {"title": "Thermodynamics of classifiers", "url": "https://arxiv.org/abs/2605.24365"}, {"title": "The thermodynamics of quasi-deterministic digital computers", "url": "https://arxiv.org/pdf/1706.02206"}],
     "reasoning_trace": {"step": "saturation R19_P3_S3", "inputs_seen": "accuracy/energy/time triad; source + 4 distinct error-dissipation papers", "reasoning": "error/energy/time tradeoff studied in stochastic thermo; 4 distinct neighbors.", "decision": "sparse: 4 distinct non-source papers; is_mechanism=true", "confidence": "medium", "could_be_wrong_if": "the triad framing is rarer/commoner than these 4"}},
    {"atom_id": "R19_P3_S4", "paper_id": "P3", "is_mechanism": true, "query": "energy-delay-deficiency product geometric bounds entropy production thermodynamic computing", "paper_hits": 5, "sparse": true,
     "results": [{"title": "Energy-Time-Accuracy Tradeoffs (SOURCE)", "url": "https://arxiv.org/abs/2601.04358"}, {"title": "Is stochastic thermodynamics the key... (PNAS)", "url": "https://www.pnas.org/doi/10.1073/pnas.2321112121"}, {"title": "Shortcuts to Thermodynamic Computing (Springer)", "url": "https://link.springer.com/article/10.1007/s10955-022-02871-0"}, {"title": "Entropy production bounds for systems running computer programs (PNAS Nexus)", "url": "https://academic.oup.com/pnasnexus/article/5/4/pgag116/8654698"}, {"title": "Geometric Optimisation of Quantum Thermodynamic Processes (PMC)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7597153/"}, {"title": "Geometrical Bounds on Irreversibility in Squeezed Thermal Bath (PMC)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9858152/"}],
     "reasoning_trace": {"step": "saturation R19_P3_S4", "inputs_seen": "EDDP from geometric entropy-production bounds; source + 5 distinct entropy-production-bound papers", "reasoning": "coined metric EDDP is unique to source, but the geometric/entropy-production-bound toolkit is a real cluster (5 distinct) -- novel name, mature toolkit (the recurring pattern).", "decision": "sparse: 5 distinct non-source papers (novel metric, mature toolkit); is_mechanism=true", "confidence": "high - EDDP unique; toolkit not", "could_be_wrong_if": "'EDDP' alone returns only the source (count 0), overstating sparsity"}}
  ]
}
```

## [REPORT 3] candidates (verbatim)

### candidates.json
```json
{
  "run_id": "run_019",
  "epoch": 1,
  "agent": "3_merger",
  "generated_at": "2026-06-01T22:36:14.581187+00:00",
  "chosen_pairs": [
    {
      "cand_id": "CAND_019_001",
      "atom_a": "R19_P1_S3",
      "atom_b": "R19_P2_S2",
      "combined_atom_hits": 6
    },
    {
      "cand_id": "CAND_019_002",
      "atom_a": "R19_P1_S3",
      "atom_b": "R19_P3_S1",
      "combined_atom_hits": 6
    },
    {
      "cand_id": "CAND_019_003",
      "atom_a": "R19_P2_S2",
      "atom_b": "R19_P3_S1",
      "combined_atom_hits": 6
    },
    {
      "cand_id": "CAND_019_004",
      "atom_a": "R19_P1_S2",
      "atom_b": "R19_P2_S2",
      "combined_atom_hits": 7
    },
    {
      "cand_id": "CAND_019_005",
      "atom_a": "R19_P1_S2",
      "atom_b": "R19_P3_S1",
      "combined_atom_hits": 7
    }
  ],
  "candidates": [
    {
      "cand_id": "CAND_019_001",
      "atom_a_id": "R19_P1_S3",
      "atom_b_id": "R19_P2_S2",
      "atom_a_hits": 3,
      "atom_b_hits": 3,
      "combined_atom_hits": 6,
      "niche_name": "Fisher-Rao-Optimal Annealing Schedules for Continuous MoE Routing Sparsity",
      "mechanism": "An information-geometric objective regulates the concentration-matrix knob so that routing entropy is annealed along a Fisher-Rao-optimal trajectory during training, transforming discrete top-k expert selection into a smoothly scheduled sparsity that produces a principled curriculum from dense to sparse routing.",
      "transfer": "The Fisher-Rao optimal-schedule derivation from ATOM B transfers onto ATOM A's continuous routing-entropy knob to specify how sparsity should evolve over training rather than just how it is parameterized at a single step.",
      "open_problem": "Does the Fisher-Rao-optimal schedule for annealing the concentration matrix's routing entropy admit a closed-form (e.g. cosine-like) curve, and does following it outperform fixed or heuristically-annealed top-k routing in MoE training?",
      "primary_quote": "the concentration matrix -- that continuously controls routing entropy",
      "quote_source": "atom_a",
      "quote_verified_substring": true,
      "reasoning_trace": {
        "step": "merge ATOM A x ATOM B",
        "inputs_seen": "A: a single continuous concentration-matrix knob that geometrically controls routing entropy, replacing discrete top-k with smooth sparsity. B: under Fisher-Rao information geometry, the *optimal training schedule* provably recovers the cosine schedule.",
        "reasoning": "A gives a continuous control variable for sparsity but says nothing about how it should change over training; B gives a geometry-derived theory of *optimal scheduling* of a control variable (noise level) but for diffusion. I tried to transfer B's 'optimal schedule under Fisher-Rao geometry' machinery onto A's concentration-matrix knob, treating routing entropy as the scheduled quantity. I rejected the reverse transfer (using A's sparsity knob inside a diffusion model) as forced. The combination is non-trivial because both already live in information geometry: A's knob induces a curve on a statistical manifold of routing distributions, so B's Fisher-Rao optimal-schedule derivation is mathematically applicable rather than metaphorical \u2014 the open question is what curve falls out, not whether the vocabularies rhyme.",
        "decision": "Settle on deriving and testing a Fisher-Rao-optimal annealing schedule for the routing-entropy knob in MoE, because it converts A's static parameterization into a principled training curriculum using B's existing optimality result.",
        "confidence": "medium - the geometric framing genuinely composes, but whether MoE routing's Fisher-Rao geometry yields a clean schedule is unverified.",
        "could_be_wrong_if": "the concentration-matrix manifold's Fisher-Rao metric is degenerate or trivial, so the 'optimal schedule' is constant or arbitrary, making the merge a vocabulary analogy between two unrelated uses of 'geometry'."
      },
      "reasoning_trace_complete": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "078e8e71-d5f5-4dfe-a36c-401c1613a7ba",
      "opus_cost_usd": 0.1445825
    },
    {
      "cand_id": "CAND_019_002",
      "atom_a_id": "R19_P1_S3",
      "atom_b_id": "R19_P3_S1",
      "atom_a_hits": 3,
      "atom_b_hits": 3,
      "combined_atom_hits": 6,
      "niche_name": "Thermodynamic MoE Routing via Concentration-Controlled Hardware Sampling",
      "mechanism": "Mapping a Mixture-of-Experts concentration matrix onto a thermodynamic computer's physical temperature transforms routing-entropy control into a native hardware operation: raising the concentration parameter regulates the noise of a stochastic substrate, which then directly samples expert assignments from the induced routing distribution instead of computing a digital top-k.",
      "transfer": "A's continuous concentration-matrix knob that controls routing entropy transfers onto B's stochastic hardware as the physical control parameter governing the sampling temperature.",
      "open_problem": "Can a thermodynamic sampler physically realize concentration-matrix-controlled MoE routing such that entropy is tuned by hardware temperature rather than by a digital top-k operator, at fixed accuracy?",
      "primary_quote": "the concentration matrix -- that continuously controls routing entropy",
      "quote_source": "atom_a",
      "quote_verified_substring": true,
      "reasoning_trace": {
        "step": "merge ATOM A x ATOM B",
        "inputs_seen": "A: a single continuous concentration-matrix knob that smoothly sets routing entropy, replacing discrete top-k expert selection with a geometric sparsity mechanism. B: thermodynamic computing where hardware behaves stochastically to physically sample from a target distribution.",
        "reasoning": "I tried to transfer A's continuous entropy-controlling parameter (the concentration matrix) into B's role of a physical control variable that sets the distribution a stochastic substrate samples from. The natural transfer is concentration -> hardware temperature/noise scale, because both A and B already operate on distributions: A *parameterizes* a routing distribution, B *physically samples* from a distribution. I rejected the weaker analogy of merely 'adding noise to top-k' because that keeps routing digital and discrete, contradicting A's smoothness. The combination is non-trivial because top-k is a non-sampling argmax-style op that has no natural thermodynamic realization, whereas A's smooth concentration formulation makes routing an honest distribution-sampling problem that thermodynamic hardware can execute natively \u2014 the geometry of A is precisely what licenses B's sampling to be the routing mechanism rather than a post-hoc perturbation.",
        "decision": "Settled on thermodynamic MoE routing where the concentration matrix is the physical temperature knob, because it converts A's mathematical knob into B's literal control parameter, yielding a falsifiable hardware-software co-design claim.",
        "confidence": "medium - the conceptual mapping (distribution-parameterizer to distribution-sampler) is tight, but physical realizability on real thermodynamic hardware is unproven.",
        "could_be_wrong_if": "thermodynamic hardware can only sample fixed energy-based distributions and cannot be conditioned on per-token concentration matrices fast enough, making the link a vocabulary analogy between 'entropy' in A and 'stochastic' in B rather than a shared sampling mechanism."
      },
      "reasoning_trace_complete": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "a985128f-7973-4c40-b5d4-c6c836046a88",
      "opus_cost_usd": 0.06623725
    },
    {
      "cand_id": "CAND_019_003",
      "atom_a_id": "R19_P2_S2",
      "atom_b_id": "R19_P3_S1",
      "atom_a_hits": 3,
      "atom_b_hits": 3,
      "combined_atom_hits": 6,
      "niche_name": "Fisher-Rao-optimal annealing schedules for thermodynamic sampling hardware",
      "mechanism": "An information-geometric optimal schedule derived from the Fisher-Rao metric routes how thermodynamic-computing hardware anneals its noise level, transforming the abstract cosine sampling schedule into a physical relaxation trajectory that the stochastic hardware natively executes to sample from a target distribution.",
      "transfer": "The Fisher-Rao-optimal noise schedule from A transfers as the physical annealing/relaxation control law that governs B's stochastic sampling hardware.",
      "open_problem": "Does the Fisher-Rao-optimal (cosine) schedule coincide with the natural relaxation dynamics of thermodynamic-computing hardware, and can that hardware physically realize it without per-step software control?",
      "primary_quote": "hardware undergoes a stochastic process in order to sample from a distribution of interest",
      "quote_source": "atom_b",
      "quote_verified_substring": true,
      "reasoning_trace": {
        "step": "merge ATOM A x ATOM B",
        "inputs_seen": "A: the variance/noise schedule that is optimal under Fisher-Rao information geometry coincides with the cosine schedule used in diffusion models. B: thermodynamic computing replaces deterministic logic with hardware that physically runs a stochastic process to draw samples from a target distribution.",
        "reasoning": "I tried to transfer A's notion of a geometrically-optimal schedule (the time-parameterization of noise that minimizes path length under the Fisher-Rao metric) onto B's physical sampling substrate, treating the hardware's annealing/relaxation timeline as the object that the schedule controls. I rejected the surface reading where 'schedule' is just a software hyperparameter bolted onto thermodynamic hardware, because that would be trivial reuse; the non-trivial claim is that the hardware's intrinsic stochastic relaxation already traces a metric on distribution space, so the Fisher-Rao optimum may either match or constrain what the physics can do, turning a software design choice into a physical-realizability question.",
        "decision": "I settled on studying whether thermodynamic hardware can natively realize the Fisher-Rao-optimal schedule, because both A and B operate on the same underlying object \u2014 a path through a manifold of probability distributions \u2014 making the link causal rather than merely lexical.",
        "confidence": "medium - both atoms genuinely concern trajectories over distribution manifolds, but whether hardware relaxation physically obeys the Fisher-Rao geometry is unverified.",
        "could_be_wrong_if": "thermodynamic hardware's relaxation dynamics are governed by a fixed physical metric unrelated to Fisher-Rao, so imposing the cosine schedule is just an external software clock and the merge collapses to vocabulary overlap on the word 'distribution'."
      },
      "reasoning_trace_complete": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "e20f56fb-07c1-4521-8025-741f8206c8ed",
      "opus_cost_usd": 0.06046199999999999
    },
    {
      "cand_id": "CAND_019_004",
      "atom_a_id": "R19_P1_S2",
      "atom_b_id": "R19_P2_S2",
      "atom_a_hits": 4,
      "atom_b_hits": 3,
      "combined_atom_hits": 7,
      "niche_name": "Fisher-Rao-Optimal Concentration Scheduling for Grassmannian MoE Routing",
      "mechanism": "A Fisher-Rao-optimal schedule transforms the concentration parameters of the Matrix Bingham gating distributions over training, so that GrMoE routing anneals along the natural information geometry of the Grassmannian manifold rather than via a hand-tuned heuristic, which regulates how sharply experts are selected as training progresses.",
      "transfer": "ATOM B's principle that the information-geometric (Fisher-Rao) optimal schedule recovers a canonical annealing curve transfers to ATOM A's Matrix Bingham concentration parameters, supplying a principled schedule for routing sharpness.",
      "open_problem": "Does the Fisher-Rao-optimal schedule on the Grassmannian of subspaces yield a closed-form (e.g. cosine-like) annealing of Matrix Bingham concentration parameters that provably improves GrMoE expert specialization and load balance?",
      "primary_quote": "operates on the Grassmannian manifold of subspaces",
      "quote_source": "atom_a",
      "quote_verified_substring": true,
      "reasoning_trace": {
        "step": "merge ATOM A x ATOM B",
        "inputs_seen": "A: MoE gating where routing lives on a Grassmannian manifold and gate weights come from Matrix Bingham concentration parameters. B: under Fisher-Rao geometry, the derived optimal schedule reproduces the cosine schedule.",
        "reasoning": "I tried transferring B's mechanism \u2014 deriving a process schedule from Fisher-Rao information geometry \u2014 onto A's free parameters, namely the Matrix Bingham concentration values that set routing sharpness. I rejected the inverse transfer (putting B's diffusion process onto a Grassmannian) as a vague vocabulary match. The non-trivial link is that both objects are genuinely Riemannian: A's gating already lives on a Grassmannian whose Fisher-Rao metric is computable, so B's 'optimal schedule = geometry-induced curve' is not metaphorical \u2014 it gives a concrete metric to optimize the concentration trajectory, potentially yielding a cosine-analogue for routing temperature.",
        "decision": "Settle on a Fisher-Rao-derived annealing schedule for the Matrix Bingham concentration parameters in GrMoE, because both mechanisms share an actual manifold and metric, making the schedule derivable rather than analogized.",
        "confidence": "medium - the manifolds and metrics genuinely overlap, but the closed-form recovery may not hold for the Grassmannian-Bingham case",
        "could_be_wrong_if": "the Fisher-Rao metric on the Matrix Bingham/Grassmannian family does not admit a tractable optimal schedule, making the link a surface reuse of the word 'geometry' rather than a transferable derivation."
      },
      "reasoning_trace_complete": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "1cb61d3a-6c74-449b-ba4c-5bf1f49de9d6",
      "opus_cost_usd": 0.061731
    },
    {
      "cand_id": "CAND_019_005",
      "atom_a_id": "R19_P1_S2",
      "atom_b_id": "R19_P3_S1",
      "atom_a_hits": 4,
      "atom_b_hits": 3,
      "combined_atom_hits": 7,
      "niche_name": "Thermodynamic Sampling of Grassmannian Bingham Gates for MoE Routing",
      "mechanism": "Thermodynamic-computing hardware undergoes a physical stochastic process that natively samples from the Matrix Bingham distribution over subspaces, which routes GrMoE expert selection on the Grassmannian manifold; the hardware's equilibrium dynamics produce gating draws directly from the concentration parameters instead of a deterministic softmax over precomputed weights.",
      "transfer": "The principle of letting hardware physically relax to sample from a target distribution (B) transfers to GrMoE's Matrix Bingham gating (A), turning manifold-constrained routing into a hardware-sampled stochastic process.",
      "open_problem": "Can a thermodynamic sampler physically realize draws from Matrix Bingham distributions on the Grassmannian fast and accurately enough to drive MoE routing, and does stochastic subspace gating then improve expert diversity or efficiency over deterministic argmax routing?",
      "primary_quote": "operates on the Grassmannian manifold of subspaces",
      "quote_source": "atom_a",
      "quote_verified_substring": true,
      "reasoning_trace": {
        "step": "merge ATOM A x ATOM B",
        "inputs_seen": "A: MoE routing where gating weights come from concentration parameters of Matrix Bingham distributions on the Grassmannian manifold of subspaces. B: thermodynamic computing where hardware behaves stochastically to sample from a distribution of interest rather than deterministically.",
        "reasoning": "I tried to transfer B's mechanism (hardware-native stochastic sampling from a target distribution) onto A's specific 'distribution of interest', the Matrix Bingham distribution over subspaces. I rejected the reverse transfer (using Grassmannian structure to describe thermodynamic state spaces) as vaguer and the alternative of merely adding noise to softmax gates as not exploiting either mechanism. The combination is non-trivial because Matrix Bingham / matrix Langevin distributions on Stiefel-Grassmann manifolds are genuinely hard to sample on digital hardware (rejection sampling scales poorly with dimension), and thermodynamic hardware is precisely a device that relaxes to sample from intractable Gibbs/Boltzmann distributions, so the two share the concrete computational bottleneck of sampling a constrained matrix distribution rather than just sharing the word 'distribution'.",
        "decision": "I settled on a niche where GrMoE's Matrix Bingham gating is implemented as the equilibrium sampling target of a thermodynamic sampler, because it identifies a real shared object (the Bingham distribution) that one mechanism needs sampled and the other can natively sample.",
        "confidence": "medium - the shared sampling bottleneck is concrete, but whether thermodynamic hardware can be physically biased to the exact Bingham concentration matrix is unverified",
        "could_be_wrong_if": "thermodynamic samplers cannot encode arbitrary Matrix Bingham concentration parameters in their physical couplings, in which case the link is just 'both involve probability distributions' \u2014 a vocabulary analogy with no transferable mechanism."
      },
      "reasoning_trace_complete": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "5bdca9e9-7dfa-43cb-9b6b-f855d5f49681",
      "opus_cost_usd": 0.0634265
    }
  ]
}
```

## [REPORT 4] verify (verbatim)

### verify.json
```json
{
  "run_id": "run_019",
  "epoch": 1,
  "agent": "4_verifier",
  "verified_at": "2026-06-01T00:00:00Z",
  "verbatim_note": "Distinct paper-like results per reformulation recorded verbatim from the WebSearch Links arrays this run (25 reformulations, 5/candidate; arxiv abs/pdf/html variants collapsed). snippet empty. collision_found is my honest verdict.",
  "key_finding": "Same pattern as Runs 17-18: each fused niche of sparse sub-mechanisms re-broadens to mature parent literatures -> ~18-28 paper-like hits/candidate -> Gate-1 novelty floored. CAND_019_003 (Fisher-Rao annealing x thermodynamic sampling) is the LOWEST-margin candidate across all runs: the Sivak-Crooks thermodynamic-length result already establishes that optimal annealing schedules ARE friction-tensor/Fisher-information-metric geodesics; only the specific sampling-HARDWARE application is unclaimed. Still no single fused-niche paper, so collision_found=false, but novelty is genuinely low on principle.",
  "candidates": [
    {"cand_id": "CAND_019_001", "niche_name": "Fisher-Rao-Optimal Annealing Schedules for Continuous MoE Routing Sparsity", "collision_found": false,
     "collision_reason": "No paper applies a Fisher-Rao-optimal annealing schedule to continuous MoE routing entropy. Nearest: Fisher-Rao gradient flows for entropy-regularised MDPs / natural policy gradients in RL (2310.02951, 2403.19448) -- the principle in a DIFFERENT domain; and 2604.14500 (Fisher metric on routing distributions, for metrics not schedules). MoE entropy/annealing scheduling is mature (DirMoE, GrMoE, Three Phases, entropy-triggered routing). Unoccupied fusion; high component volume.",
     "reformulations": [
       {"n": 1, "query": "Fisher-Rao optimal annealing schedule continuous MoE routing entropy sparsity", "results": [
         {"title": "Taming Latency-Memory Trade-Off in MoE-Based LLM (FineMoE)", "url": "https://intellisys.haow.us/assets/pdf/Hanfei_FineMoE_EuroSys26.pdf"},
         {"title": "Sparsity is Combinatorial Depth: MoE Expressivity via Tropical Geometry", "url": "https://arxiv.org/pdf/2602.03204"},
         {"title": "DirMoE: Dirichlet-routed Mixture of Experts", "url": "https://arxiv.org/pdf/2602.09001"},
         {"title": "Optimal Sparsity of Mixture-of-Experts Language Models for Reasoning Tasks", "url": "https://arxiv.org/pdf/2508.18672"}]},
       {"n": 2, "query": "information geometry schedule routing entropy concentration mixture of experts prior work", "results": [
         {"title": "Variational Inference, Entropy, and Orthogonality: A Unified Theory of MoE", "url": "https://arxiv.org/abs/2601.03577"},
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "Modality-Guided Mixture of Graph Experts with Entropy-Triggered Routing", "url": "https://arxiv.org/html/2602.20723"},
         {"title": "Mixture-of-Experts with Expert Choice Routing", "url": "https://arxiv.org/pdf/2202.09368"},
         {"title": "Rewiring Experts on the Fly: Continuous Rerouting for MoE", "url": "https://arxiv.org/html/2510.14853v1"},
         {"title": "Mixture-of-Experts as Soft Clustering: Dual Jacobian-PCA Spectral Geometry", "url": "https://arxiv.org/pdf/2601.11616"}]},
       {"n": 3, "query": "Fisher-Rao geodesic schedule anneal routing sparsity top-k mixture of experts", "results": [
         {"title": "DirMoE: Dirichlet-routed Mixture of Experts", "url": "https://arxiv.org/pdf/2602.09001"},
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "Mixture of Group Experts for Learning Invariant Representations", "url": "https://arxiv.org/pdf/2504.09265"},
         {"title": "Route Experts by Sequence, not by Token", "url": "https://arxiv.org/pdf/2511.06494"},
         {"title": "ReMoE: Fully Differentiable MoE with ReLU Routing", "url": "https://arxiv.org/pdf/2412.14711"},
         {"title": "Sparsity-Controllable Dynamic Top-p MoE for Large Foundation Model Pre-training", "url": "https://arxiv.org/pdf/2512.13996"}]},
       {"n": 4, "query": "optimal schedule routing entropy masked diffusion mixture of experts survey", "results": [
         {"title": "Error Bounds and Optimal Schedules for Masked Diffusions", "url": "https://arxiv.org/pdf/2510.25544"},
         {"title": "A Comprehensive Survey of Mixture-of-Experts: Algorithms, Theory, Applications", "url": "https://arxiv.org/html/2503.07137v1"},
         {"title": "Modality-Guided Mixture of Graph Experts with Entropy-Triggered Routing", "url": "https://arxiv.org/html/2602.20723"},
         {"title": "Expert Race: Flexible Routing for Scaling Diffusion Transformer with MoE", "url": "https://arxiv.org/html/2503.16057v1"},
         {"title": "Mixture of Message Passing Experts with Routing Entropy Regularization", "url": "https://arxiv.org/html/2502.08083"}]},
       {"n": 5, "query": "Fisher-Rao cosine schedule applied to mixture of experts routing entropy already studied", "results": [
         {"title": "Geometric Metrics for MoE Specialization: From Fisher Information to Early Failure Detection", "url": "https://arxiv.org/abs/2604.14500"},
         {"title": "Rewiring Experts on the Fly: Continuous Rerouting for MoE", "url": "https://arxiv.org/html/2510.14853v1"},
         {"title": "Variational Inference, Entropy, and Orthogonality: Unified Theory of MoE", "url": "https://arxiv.org/html/2601.03577v1"},
         {"title": "The Cosine Schedule is Fisher-Rao-Optimal (SOURCE P2)", "url": "https://arxiv.org/abs/2508.04884"},
         {"title": "Statistical Advantages of Perturbing Cosine Router in Mixture of Experts", "url": "https://arxiv.org/pdf/2405.14131"}]}
     ]},
    {"cand_id": "CAND_019_002", "niche_name": "Thermodynamic MoE Routing via Concentration-Controlled Hardware Sampling", "collision_found": false,
     "collision_reason": "Disjoint clusters: concentration-controlled MoE routing (GrMoE, DirMoE, Path-Constrained MoE 2603.18297) vs thermodynamic/probabilistic sampling hardware (Extropic TSU, neutral-atom thermodynamic sampling 2512.21142, energy-based hardware, stochastic adder circuits). No paper runs MoE concentration routing on thermodynamic sampling hardware. Unoccupied fusion.",
     "reformulations": [
       {"n": 1, "query": "thermodynamic computing hardware mixture of experts routing concentration sampling", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "Thermodynamic sampling of materials using neutral-atom quantum computers", "url": "https://arxiv.org/html/2512.21142v1"},
         {"title": "Path-Constrained Mixture-of-Experts", "url": "https://arxiv.org/pdf/2603.18297"},
         {"title": "DirMoE: Dirichlet-routed Mixture of Experts", "url": "https://arxiv.org/pdf/2602.09001"}]},
       {"n": 2, "query": "physical stochastic hardware sample expert routing distribution concentration entropy prior work", "results": [
         {"title": "Three Phases of Expert Routing", "url": "https://arxiv.org/html/2604.04230"},
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "Path-Constrained Mixture-of-Experts", "url": "https://arxiv.org/pdf/2603.18297"},
         {"title": "Excitation: Momentum For Experts", "url": "https://arxiv.org/html/2602.21798"},
         {"title": "Stochastic Adder Circuits with Improved Entropy Output (PMC)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10742554/"}]},
       {"n": 3, "query": "thermodynamic sampler concentration-controlled mixture of experts routing entropy hardware", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/abs/2602.17798"},
         {"title": "Mixture of Message Passing Experts with Routing Entropy Regularization", "url": "https://arxiv.org/html/2502.08083"},
         {"title": "DirMoE: Dirichlet-routed Mixture of Experts", "url": "https://arxiv.org/pdf/2602.09001"}]},
       {"n": 4, "query": "energy-based hardware sampling expert routing concentration neural network", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "Improving deep neural network performance through sampling (npj Unconventional Computing)", "url": "https://www.nature.com/articles/s44335-026-00063-7"},
         {"title": "Energy-Efficient Supervised Learning with a Binary Stochastic Forward-Forward Algorithm", "url": "https://arxiv.org/pdf/2507.06461"},
         {"title": "Hardware-Efficient Stochastic Binary CNN Architectures for Near-Sensor Computing (PMC)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8766965/"},
         {"title": "SiftMoE: Similarity-Aware Energy-Efficient Expert Selection for Wireless Distributed MoE", "url": "https://arxiv.org/pdf/2603.23888"}]},
       {"n": 5, "query": "thermodynamic mixture of experts routing concentration controlled hardware published", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "Path-Constrained Mixture-of-Experts", "url": "https://arxiv.org/pdf/2603.18297"},
         {"title": "L2R: Low-Rank and Lipschitz-Controlled Routing for Mixture-of-Experts", "url": "https://arxiv.org/pdf/2601.21349"}]}
     ]},
    {"cand_id": "CAND_019_003", "niche_name": "Fisher-Rao-optimal annealing schedules for thermodynamic sampling hardware", "collision_found": false,
     "collision_reason": "LOWEST MARGIN across all runs. The Sivak-Crooks thermodynamic-length result ALREADY establishes that optimal (minimum-dissipation) annealing/driving schedules are GEODESICS of the friction tensor -- a Fisher-information-type metric -- for driven thermodynamic systems (Thermodynamic Metrics and Optimal Paths 1201.4166; Geometry of thermodynamic control 1208.4553; Optimal schedules for annealing 2402.14717; Stochastic-thermodynamic interpretation of information geometry 1712.04311). So 'Fisher-Rao-optimal annealing schedule for a thermodynamic process' is essentially a KNOWN principle. The crosscheck noted these works 'do not contain specific information about HARDWARE implementations', so the narrow application to thermodynamic-sampling-HARDWARE (TSU chips) is unclaimed -- hence collision_found=false at the strict fused-niche level. But novelty is genuinely LOW on principle, not just on prior-art volume.",
     "reformulations": [
       {"n": 1, "query": "Fisher-Rao optimal annealing schedule thermodynamic sampling hardware", "results": [
         {"title": "Optimal schedules for annealing algorithms", "url": "https://arxiv.org/html/2402.14717v1"},
         {"title": "Simulated annealing with constant thermodynamic speed (ScienceDirect)", "url": "https://www.sciencedirect.com/science/article/abs/pii/0010465588900033"},
         {"title": "Thermodynamic sampling of materials using neutral-atom quantum computers", "url": "https://arxiv.org/html/2512.21142"},
         {"title": "Optimal schedules for annealing algorithms (Phys. Rev. E)", "url": "https://link.aps.org/doi/10.1103/PhysRevE.109.065301"},
         {"title": "High-quality Thermal Gibbs Sampling with Quantum Annealing Hardware", "url": "https://arxiv.org/pdf/2109.01690"}]},
       {"n": 2, "query": "information geometry schedule thermodynamic computing stochastic sampling prior work", "results": [
         {"title": "Is stochastic thermodynamics the key to understanding energy costs of computation? (PNAS)", "url": "https://www.pnas.org/doi/10.1073/pnas.2321112121"},
         {"title": "Energy-Time-Accuracy Tradeoffs in Thermodynamic Computing (SOURCE P3)", "url": "https://arxiv.org/html/2601.04358"},
         {"title": "Information geometry approach to quantum stochastic thermodynamics", "url": "https://arxiv.org/html/2409.06083v2"},
         {"title": "Stochastic thermodynamic interpretation of information geometry", "url": "https://arxiv.org/abs/1712.04311"},
         {"title": "Geometric thermodynamics for the Fokker-Planck equation (Springer Info. Geometry)", "url": "https://link.springer.com/article/10.1007/s41884-023-00102-3"}]},
       {"n": 3, "query": "geodesic optimal driving protocol thermodynamic sampler Fisher-Rao schedule entropy production", "results": [
         {"title": "Thermodynamic control of non-equilibrium systems", "url": "https://arxiv.org/pdf/2506.14416"},
         {"title": "Riemannian geometry of optimal driving and thermodynamic length (Phys. Rev. Research)", "url": "https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.4.043049"},
         {"title": "Optimal protocols for slowly-driven quantum processes", "url": "https://arxiv.org/pdf/1506.03864"},
         {"title": "Beyond Linear Response: Equivalence between Thermodynamic Geometry and Optimal Transport", "url": "https://arxiv.org/html/2404.01286v2"},
         {"title": "Thermodynamic Length, Time, Speed and Optimum Path to Minimize Entropy Production", "url": "https://arxiv.org/pdf/cond-mat/9503174"},
         {"title": "The geometry of thermodynamic control", "url": "https://arxiv.org/pdf/1208.4553"}]},
       {"n": 4, "query": "optimal schedule thermodynamic computing entropy production information geometry survey", "results": [
         {"title": "Work, Entropy Production, and Thermodynamics of Information under Protocol Constraints (PRX)", "url": "https://link.aps.org/doi/10.1103/PhysRevX.11.041024"},
         {"title": "Energy-Time-Accuracy Tradeoffs in Thermodynamic Computing (SOURCE P3)", "url": "https://arxiv.org/html/2601.04358"},
         {"title": "Information geometry of excess and housekeeping entropy production", "url": "https://arxiv.org/pdf/2206.14599"},
         {"title": "Finite-time thermodynamic bounds and tradeoff relations for information processing", "url": "https://arxiv.org/pdf/2409.08606"},
         {"title": "Geometric thermodynamics for the Fokker-Planck equation (Springer)", "url": "https://link.springer.com/article/10.1007/s41884-023-00102-3"}]},
       {"n": 5, "query": "Fisher-Rao schedule thermodynamic hardware sampling mixture of experts already studied", "results": [
         {"title": "Unbiased Gradient Estimation with Balanced Assignments for Mixtures of Experts", "url": "https://arxiv.org/pdf/2109.11817"},
         {"title": "Dynamic hardware selection for experts in mixture-of-experts model (USPTO)", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11893502"},
         {"title": "Sigmoid Gating is More Sample Efficient than Softmax Gating in MoE", "url": "https://arxiv.org/pdf/2405.13997"},
         {"title": "DirMoE: Dirichlet-routed Mixture of Experts", "url": "https://arxiv.org/pdf/2602.09001"}]}
     ]},
    {"cand_id": "CAND_019_004", "niche_name": "Fisher-Rao-Optimal Concentration Scheduling for Grassmannian MoE Routing", "collision_found": false,
     "collision_reason": "GrMoE Bingham gating (source P1) and Fisher-Rao cosine schedule (source P2) appear separately; no paper applies a Fisher-Rao optimal SCHEDULE to the Bingham concentration. Neighbors: RoMA (2511.07419), Spectral Manifold Regularization (2601.03889), Curvature-Guided GeoMoE (2603.22317), Gradient-Conflict Subspace Pruning MoE (2512.20291), MoE surveys. Unoccupied fusion; geometric-routing volume high.",
     "reformulations": [
       {"n": 1, "query": "Fisher-Rao optimal concentration schedule Grassmannian mixture of experts Bingham routing", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/html/2602.17798v1"},
         {"title": "The Cosine Schedule is Fisher-Rao-Optimal (SOURCE P2)", "url": "https://www.arxiv.org/pdf/2508.04884"}]},
       {"n": 2, "query": "information geometry schedule Matrix Bingham concentration routing manifold mixture of experts prior work", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "Routing Manifold Alignment Improves Generalization of MoE LLMs", "url": "https://arxiv.org/html/2511.07419v1"},
         {"title": "Mixture-of-Experts as Soft Clustering: Dual Jacobian-PCA Spectral Geometry", "url": "https://arxiv.org/pdf/2601.11616"}]},
       {"n": 3, "query": "Grassmannian mixture of experts Bingham gating annealing Fisher-Rao geometry schedule", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/html/2602.17798v1"},
         {"title": "Convergence Rates for Gaussian Mixtures of Experts", "url": "https://arxiv.org/pdf/1907.04377"},
         {"title": "Model Selection for Gaussian-gated Gaussian MoE Using Dendrograms", "url": "https://arxiv.org/abs/2505.13052"},
         {"title": "Sigmoid Gating is More Sample Efficient than Softmax Gating in MoE", "url": "https://arxiv.org/pdf/2405.13997"}]},
       {"n": 4, "query": "concentration parameter schedule subspace routing optimal masked diffusion mixture of experts survey", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "MoE with Gradient Conflict-Driven Subspace Topology Pruning for Emergent Modularity", "url": "https://arxiv.org/pdf/2512.20291"},
         {"title": "Path-Constrained Mixture-of-Experts", "url": "https://arxiv.org/pdf/2603.18297"}]},
       {"n": 5, "query": "Fisher-Rao Bingham concentration schedule mixture of experts already studied", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "Mixtures of Experts Models (review)", "url": "https://arxiv.org/pdf/1806.08200"},
         {"title": "MoE Distributional Regression: Robust Estimation with Adaptive First-order Methods", "url": "https://arxiv.org/pdf/2211.09875"},
         {"title": "Convergence Rates for Gaussian Mixtures of Experts", "url": "https://arxiv.org/pdf/1907.04377"}]}
     ]},
    {"cand_id": "CAND_019_005", "niche_name": "Thermodynamic Sampling of Grassmannian Bingham Gates for MoE Routing", "collision_found": false,
     "collision_reason": "Bingham sampling (directional statistics: Efficient sampling 2010.00137, complex Bingham 1310.8110, rstiefel), MoE-hardware distribution (USPTO patents), and physical Boltzmann samplers (p-bit/MTJ, laser networks, quantum annealers, neutral-atom 2512.21142) all appear, but NO paper draws Bingham MoE routing weights on a physical/thermodynamic sampler. 'Application Domain Discovery of Thermodynamic Models by MoE' is the reverse (MoE applied to thermo models). Unoccupied fusion.",
     "reformulations": [
       {"n": 1, "query": "thermodynamic sampling Grassmannian Bingham gates mixture of experts routing", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "DirMoE: Dirichlet-routed Mixture of Experts", "url": "https://arxiv.org/pdf/2602.09001"},
         {"title": "Improving Routing in Sparse Mixture of Experts with Graph of Tokens", "url": "https://arxiv.org/pdf/2505.00792"}]},
       {"n": 2, "query": "physical sampler Bingham distribution gating manifold expert routing prior work", "results": [
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
         {"title": "Mixture-of-Experts with Expert Choice Routing", "url": "https://arxiv.org/pdf/2202.09368"},
         {"title": "Spectral Manifold Regularization for Stable and Modular Routing in Deep MoE", "url": "https://arxiv.org/html/2601.03889"},
         {"title": "Efficient sampling from the Bingham distribution", "url": "https://arxiv.org/pdf/2010.00137"},
         {"title": "A new method to simulate the Bingham and related distributions (directional data)", "url": "https://arxiv.org/pdf/1310.8110"}]},
       {"n": 3, "query": "thermodynamic hardware directional distribution sampling expert gates mixture of experts", "results": [
         {"title": "Dense-to-Sparse Gate for Mixture-of-Experts (OpenReview)", "url": "https://openreview.net/pdf?id=_4D8IVs7yO8"},
         {"title": "Sigmoid Gating is More Sample Efficient than Softmax Gating in MoE", "url": "https://arxiv.org/pdf/2405.13997"},
         {"title": "Unbiased Gradient Estimation with Balanced Assignments for MoE", "url": "https://arxiv.org/pdf/2109.11817"},
         {"title": "GatePro: Parameter-Free Expert Selection Optimization for MoE", "url": "https://arxiv.org/pdf/2510.13079"}]},
       {"n": 4, "query": "neutral-atom quantum thermodynamic sampling Bingham routing neural network", "results": [
         {"title": "Thermodynamic sampling of materials using neutral-atom quantum computers", "url": "https://arxiv.org/abs/2512.21142"},
         {"title": "Thermodynamics based on Neural Networks", "url": "https://arxiv.org/html/2311.13799"}]},
       {"n": 5, "query": "thermodynamic Bingham gate sampling mixture of experts already published", "results": [
         {"title": "Sigmoid Gating is More Sample Efficient than Softmax Gating in MoE", "url": "https://arxiv.org/pdf/2405.13997"},
         {"title": "Application Domain Discovery of Thermodynamic Models by Mixture of Experts Learning (ResearchGate)", "url": "https://www.researchgate.net/publication/346274152_Application_Domain_Discovery_of_Thermodynamic_Models_by_Mixture_of_Experts_Learning"},
         {"title": "Is Temperature Sample Efficient for Softmax Gaussian Mixture of Experts?", "url": "https://arxiv.org/pdf/2401.13875"},
         {"title": "Approximations of conditional probability density functions via mixture of experts", "url": "https://arxiv.org/pdf/2012.02385"},
         {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"}]}
     ]}
  ]
}
```

### verify_reasoning.json
```json
{
  "run_id": "run_019",
  "agent": "4_verifier",
  "note": "verdict_trace per candidate (decision states collision polarity for AGENT 5's check) + reasoning_trace per reformulation. Recurring sub-finding: fused niches of sparse sub-mechanisms re-broaden to mature parent literatures. CAND_019_003 is the lowest-margin (principle already established by Sivak-Crooks thermodynamic length).",
  "candidates": [
    {"cand_id": "CAND_019_001",
     "verdict_trace": {"step": "collision verdict CAND_019_001", "inputs_seen": "5 reformulations; ~24 paper-like hits; nearest Fisher-Rao+entropy work is in RL (2310.02951, 2403.19448) and metrics (2604.14500), not MoE entropy scheduling",
       "reasoning": "concentration-entropy control (h=3) x Fisher-Rao cosine schedule (h=3). No paper applies a Fisher-Rao-optimal annealing schedule to MoE routing entropy; the Fisher-Rao+entropy principle lives in RL (natural policy gradient flows) and in MoE METRICS (2604.14500), not as a routing SCHEDULE.",
       "decision": "no collision: fused niche unoccupied; high component volume", "confidence": "medium - the Fisher-Rao+entropy principle is mature in adjacent domains", "could_be_wrong_if": "an RL natural-policy-gradient schedule transfers directly to MoE routing under different words"},
     "reformulation_traces": [
       {"n": 1, "reasoning_trace": {"step": "reform 1", "inputs_seen": "FineMoE, Tropical-Geometry expressivity, DirMoE, Optimal-Sparsity MoE; engine noted no Fisher-Rao annealing for continuous MoE routing", "reasoning": "direct probe; MoE sparsity/scheduling papers but none Fisher-Rao-scheduled.", "decision": "no exact match", "confidence": "medium - one phrasing", "could_be_wrong_if": "indexed under 'natural gradient routing'"}},
       {"n": 2, "reasoning_trace": {"step": "reform 2 prior-art probe", "inputs_seen": "Unified Theory of MoE, GrMoE, entropy-triggered routing, soft clustering", "reasoning": "information-geometry MoE theory exists but not as an entropy annealing schedule.", "decision": "no collision; component volume high", "confidence": "high - info-geometry MoE area is active", "could_be_wrong_if": "Unified Theory derives the schedule implicitly"}},
       {"n": 3, "reasoning_trace": {"step": "reform 3", "inputs_seen": "DirMoE, ReMoE, Dynamic Top-p, Group/Sequence routing", "reasoning": "differentiable/soft routing alternatives to top-k, none Fisher-Rao-geodesic-scheduled.", "decision": "no collision", "confidence": "medium", "could_be_wrong_if": "DirMoE's hyperparameter schedule is the geodesic schedule"}},
       {"n": 4, "reasoning_trace": {"step": "reform 4 survey probe", "inputs_seen": "MoE survey 2503.07137, masked-diffusion schedules, routing-entropy regularization 2502.08083", "reasoning": "surveys + entropy-regularization exist; none Fisher-Rao-optimal-scheduled.", "decision": "no collision; survey-level volume high", "confidence": "high - surveys omit this fusion", "could_be_wrong_if": "a survey subsection covers it"}},
       {"n": 5, "reasoning_trace": {"step": "reform 5 closest-neighbor probe", "inputs_seen": "2604.14500 (Fisher metric on routing distributions), source P2, perturbed cosine router", "reasoning": "2604.14500 is the nearest (Fisher metric on routing) but for metrics/failure-detection, not a schedule.", "decision": "no collision; nearest is a metric not a schedule", "confidence": "medium", "could_be_wrong_if": "2604.14500 implies the optimal schedule"}}
     ]},
    {"cand_id": "CAND_019_002",
     "verdict_trace": {"step": "collision verdict CAND_019_002", "inputs_seen": "5 reformulations; disjoint MoE-routing vs thermodynamic-hardware clusters; Extropic TSU / neutral-atom 2512.21142 hardware found but unfused with MoE concentration routing",
       "reasoning": "concentration-entropy control (h=3) x thermodynamic stochastic sampling (h=3). p-bit/EBM/TSU hardware is real and MoE concentration routing is real, but no paper runs MoE routing on a thermodynamic sampler.",
       "decision": "no collision: disjoint clusters, fusion unoccupied", "confidence": "high - clusters clearly separate", "could_be_wrong_if": "Extropic's EBM/pMoG sampler already realizes a thermodynamic MoE router"},
     "reformulation_traces": [
       {"n": 1, "reasoning_trace": {"step": "reform 1", "inputs_seen": "GrMoE + neutral-atom thermo sampling + Path-Constrained MoE + DirMoE", "reasoning": "both halves present, no fusion.", "decision": "no fused paper", "confidence": "medium", "could_be_wrong_if": "Path-MoE uses thermodynamic sampling"}},
       {"n": 2, "reasoning_trace": {"step": "reform 2 prior-art probe", "inputs_seen": "Three Phases routing, GrMoE, stochastic adder circuits (hardware entropy)", "reasoning": "hardware-entropy circuits exist but not for expert routing.", "decision": "no collision", "confidence": "medium", "could_be_wrong_if": "a stochastic-circuit paper routes experts"}},
       {"n": 3, "reasoning_trace": {"step": "reform 3", "inputs_seen": "GrMoE, routing-entropy regularization, DirMoE", "reasoning": "MoE-side only; no thermodynamic hardware.", "decision": "no collision", "confidence": "medium", "could_be_wrong_if": "indexed under 'energy-based router'"}},
       {"n": 4, "reasoning_trace": {"step": "reform 4", "inputs_seen": "DNN-via-sampling (npj), Forward-Forward stochastic, SiftMoE energy-efficient selection", "reasoning": "energy-efficient/sampling-based learning exists; SiftMoE is about energy-efficient selection over wireless links, not thermodynamic sampling of routes.", "decision": "no collision", "confidence": "medium", "could_be_wrong_if": "the npj sampling-hardware paper covers MoE routing"}},
       {"n": 5, "reasoning_trace": {"step": "reform 5", "inputs_seen": "GrMoE, Path-MoE, L2R routing", "reasoning": "returns MoE routing-control papers, no thermodynamic fusion.", "decision": "no collision", "confidence": "high", "could_be_wrong_if": "fusion too new to index"}}
     ]},
    {"cand_id": "CAND_019_003",
     "verdict_trace": {"step": "collision verdict CAND_019_003 (LOWEST MARGIN)", "inputs_seen": "5 reformulations returning the Sivak-Crooks thermodynamic-length / optimal-driving-geodesic literature (1201.4166, 1208.4553, PhysRevResearch.4.043049, 1712.04311, 2402.14717)",
       "reasoning": "Fisher-Rao cosine schedule (h=3) x thermodynamic stochastic sampling (h=3). This is the closest to a collision in any run: the Sivak-Crooks result ALREADY establishes that optimal annealing/driving schedules are geodesics of the friction tensor (a Fisher-information-type metric) for thermodynamic systems. So 'Fisher-Rao-optimal annealing schedule for a thermodynamic process' is a KNOWN principle; only the narrow application to thermodynamic-sampling-HARDWARE is unclaimed.",
       "decision": "no collision at the strict fused-niche level, BUT lowest margin: the principle is established (Sivak-Crooks thermodynamic length); novelty is low even beyond the volume floor", "confidence": "medium - a reviewer could reasonably call this already known", "could_be_wrong_if": "the thermodynamic-length geodesic IS exactly the proposed schedule (then it is a genuine collision, not just adjacent)"},
     "reformulation_traces": [
       {"n": 1, "reasoning_trace": {"step": "reform 1", "inputs_seen": "Optimal schedules for annealing (2402.14717, PRE), constant-thermodynamic-speed annealing, neutral-atom thermo sampling, quantum-annealing Gibbs sampling", "reasoning": "optimal annealing schedules ARE a mature field (constant thermodynamic speed = geodesic); hardware Gibbs sampling exists.", "decision": "principle already studied; no hardware-specific fused paper", "confidence": "medium", "could_be_wrong_if": "constant-thermodynamic-speed schedule is exactly the claim"}},
       {"n": 2, "reasoning_trace": {"step": "reform 2 prior-art probe", "inputs_seen": "Stochastic-thermodynamic interpretation of information geometry (1712.04311), Info-geometry quantum stochastic thermo (2409.06083), Fokker-Planck geometric thermo", "reasoning": "the information-geometry<->thermodynamics link is well established; Fisher metric = 2nd-order KL = thermodynamic metric.", "decision": "no collision but principle established", "confidence": "high - the IG<->thermo link is textbook-level", "could_be_wrong_if": "one of these already states the hardware schedule"}},
       {"n": 3, "reasoning_trace": {"step": "reform 3 geodesic-driving probe", "inputs_seen": "Riemannian geometry of optimal driving / thermodynamic length (PhysRevResearch.4.043049), geometry of thermodynamic control (1208.4553), thermo-geometry = optimal transport (2404.01286)", "reasoning": "optimal driving protocols ARE geodesics of the friction/Fisher metric -- this is precisely 'Fisher-Rao-optimal schedule' for a thermodynamic process.", "decision": "principle is established (geodesic optimal driving)", "confidence": "high - this is the Sivak-Crooks framework", "could_be_wrong_if": "the candidate's 'sampling hardware' specificity is judged novel enough"}},
       {"n": 4, "reasoning_trace": {"step": "reform 4 survey probe", "inputs_seen": "Work/entropy-production under protocol constraints (PRX), info-geometry of entropy production, finite-time thermo bounds", "reasoning": "the optimal-protocol/entropy-production-bound field is mature.", "decision": "no collision; field mature", "confidence": "high", "could_be_wrong_if": "a review already states the hardware-annealing schedule"}},
       {"n": 5, "reasoning_trace": {"step": "reform 5 MoE-bridge probe", "inputs_seen": "MoE balanced-assignment sampling, hardware-selection patent, sigmoid gating, DirMoE", "reasoning": "no MoE paper connects to the thermodynamic-length schedule -- the MoE bridge is absent.", "decision": "no MoE fusion", "confidence": "medium", "could_be_wrong_if": "a patent covers thermodynamic expert scheduling"}}
     ]},
    {"cand_id": "CAND_019_004",
     "verdict_trace": {"step": "collision verdict CAND_019_004", "inputs_seen": "5 reformulations; GrMoE and Fisher-Rao-cosine appear separately; neighbors RoMA/Spectral-Manifold/GeoMoE",
       "reasoning": "Matrix Bingham gating (h=4) x Fisher-Rao cosine schedule (h=3). Geometric/manifold routing is active but no paper applies a Fisher-Rao optimal SCHEDULE to Bingham concentration.",
       "decision": "no collision: fusion unoccupied; geometric-routing volume high", "confidence": "medium", "could_be_wrong_if": "a manifold-routing paper schedules concentration via information geometry"},
     "reformulation_traces": [
       {"n": 1, "reasoning_trace": {"step": "reform 1", "inputs_seen": "only the two source papers", "reasoning": "direct probe returns just P1 and P2, no bridge.", "decision": "no bridging paper", "confidence": "high - only sources returned", "could_be_wrong_if": "a citing paper bridges them"}},
       {"n": 2, "reasoning_trace": {"step": "reform 2 prior-art probe", "inputs_seen": "RoMA (2511.07419), soft-clustering spectral geometry", "reasoning": "manifold-routing cluster, none Fisher-Rao-scheduling Bingham gates.", "decision": "no collision", "confidence": "high", "could_be_wrong_if": "RoMA alignment is a Fisher-Rao schedule in disguise"}},
       {"n": 3, "reasoning_trace": {"step": "reform 3", "inputs_seen": "GrMoE + Gaussian-MoE convergence + model-selection", "reasoning": "classic gating theory, no Fisher-Rao Bingham schedule.", "decision": "no collision", "confidence": "high", "could_be_wrong_if": "under other terminology"}},
       {"n": 4, "reasoning_trace": {"step": "reform 4 survey probe", "inputs_seen": "subspace-pruning MoE (2512.20291), Path-MoE", "reasoning": "subspace-routing variants, none scheduled via Fisher-Rao.", "decision": "no collision", "confidence": "high", "could_be_wrong_if": "subspace pruning schedules concentration"}},
       {"n": 5, "reasoning_trace": {"step": "reform 5", "inputs_seen": "MoE reviews + Gaussian MoE", "reasoning": "reviews omit the fusion.", "decision": "no collision", "confidence": "high", "could_be_wrong_if": "a review covers it"}}
     ]},
    {"cand_id": "CAND_019_005",
     "verdict_trace": {"step": "collision verdict CAND_019_005", "inputs_seen": "5 reformulations; Bingham-sampling (directional stats) + physical Boltzmann samplers + neutral-atom thermo sampling all separate; reverse-direction 'MoE for thermo models' found, not the target",
       "reasoning": "Matrix Bingham gating (h=4) x thermodynamic stochastic sampling (h=3). Bingham sampling (2010.00137, 1310.8110), MoE-hardware, and physical Boltzmann/quantum samplers exist, but none draw Bingham MoE routing weights on a physical/thermodynamic sampler.",
       "decision": "no collision: fusion unoccupied", "confidence": "high - three-way separation", "could_be_wrong_if": "a p-bit/Boltzmann-sampler paper already gates experts via a directional distribution"},
     "reformulation_traces": [
       {"n": 1, "reasoning_trace": {"step": "reform 1", "inputs_seen": "GrMoE, DirMoE, Graph-of-Tokens routing", "reasoning": "MoE routing only, no thermodynamic sampler.", "decision": "no fused paper", "confidence": "medium", "could_be_wrong_if": "indexed under 'physical gating'"}},
       {"n": 2, "reasoning_trace": {"step": "reform 2 prior-art probe", "inputs_seen": "Bingham sampling (2010.00137, complex Bingham 1310.8110), Spectral Manifold Regularization", "reasoning": "Bingham sampling is directional statistics, separate from MoE hardware.", "decision": "no collision", "confidence": "high", "could_be_wrong_if": "a sampling paper targets MoE routing hardware"}},
       {"n": 3, "reasoning_trace": {"step": "reform 3", "inputs_seen": "dense-to-sparse gate, balanced-assignment sampling, GatePro", "reasoning": "gating/sampling algorithms, none thermodynamic-hardware-directional.", "decision": "no collision", "confidence": "medium", "could_be_wrong_if": "balanced-assignment sampling is hardware-realized"}},
       {"n": 4, "reasoning_trace": {"step": "reform 4", "inputs_seen": "neutral-atom thermo sampling (2512.21142), thermodynamics-based NN (2311.13799); engine found no Bingham/NN routing connection", "reasoning": "neutral-atom thermo sampling exists for materials, not for Bingham MoE gates.", "decision": "no collision", "confidence": "high - engine flagged the gap", "could_be_wrong_if": "neutral-atom sampling is applied to routing elsewhere"}},
       {"n": 5, "reasoning_trace": {"step": "reform 5", "inputs_seen": "'Application Domain Discovery of Thermodynamic Models by MoE' (reverse direction), temperature MoE", "reasoning": "the one MoE+thermo hit applies MoE TO thermodynamic models -- opposite of using a thermodynamic sampler for MoE gating.", "decision": "no collision (reverse-direction neighbor only)", "confidence": "high", "could_be_wrong_if": "that reverse-direction work also samples gates thermodynamically"}}
     ]}
  ]
}
```

## [REPORT 5] crosscheck (verbatim)

### crosscheck.json
```json
{
  "run_id": "run_019",
  "epoch": 1,
  "agent": "4_crosschecker",
  "crosschecked_at": "2026-06-01T00:00:00Z",
  "note": "Independent re-verification (R7): 1 fresh differently-worded re-search per candidate, targeting the most likely collision. 'agent3' = the verifier verdict (same AGENT 4, independent pass). All confirm; CAND_019_003 reconfirmed as lowest-margin.",
  "candidates": [
    {"cand_id": "CAND_019_001", "agent3_collision_found": false, "agent4_collision": false, "mismatch_with_agent3": false,
     "notes": "Re-probed the RL angle (Fisher-Rao gradient flow / entropy regulariser). Found a real cluster: Fisher-Rao gradient flow for entropy-regularised MDPs (2310.02951), Fisher-Rao flows of linear programs / natural policy gradients (2403.19448). The Fisher-Rao+entropy-regularisation principle is mature IN RL, not in MoE routing -- confirms the MoE-routing fusion is unoccupied (adjacent, not collision). Confirms verifier.",
     "recheck_searches": [{"n": 1, "query": "entropy regulariser schedule routing information geometry reinforcement learning Fisher-Rao gradient flow", "results": [
       {"title": "Fisher-Rao Gradient Flows of Linear Programs and State-Action Natural Policy Gradients", "url": "https://arxiv.org/html/2403.19448v2"},
       {"title": "A Fisher-Rao Gradient Flow for Entropy-Regularised Markov Decision Processes in Polish Spaces (Springer FoCM)", "url": "https://link.springer.com/article/10.1007/s10208-025-09729-3"},
       {"title": "A Fisher-Rao gradient flow for entropy-regularised Markov decision processes", "url": "https://arxiv.org/abs/2310.02951"},
       {"title": "A Fisher-Rao gradient flow for entropic mean-field min-max games", "url": "https://arxiv.org/html/2405.15834v2"}]}],
     "reasoning_trace": {"step": "independent re-verification CAND_019_001", "inputs_seen": "verifier verdict (no collision) + my RL re-search; found Fisher-Rao entropy-regularised RL flows", "reasoning": "I tested whether the Fisher-Rao+entropy principle (which the verifier saw hints of) is already applied to routing. It is mature in RL (policy mirror descent / natural policy gradient) but NOT transferred to MoE routing schedules. Adjacent, not a collision. Uphold verifier.", "decision": "confirm verifier no-collision; no mismatch", "confidence": "medium - the principle is mature in RL", "could_be_wrong_if": "natural-policy-gradient routing has been published for MoE under different words"}},
    {"cand_id": "CAND_019_002", "agent3_collision_found": false, "agent4_collision": false, "mismatch_with_agent3": false,
     "notes": "Re-probed the vendor-hardware angle (Extropic/Normal Computing). Confirmed real thermodynamic-sampling-hardware companies (TSU, p-bits, EBM/Gibbs sampling) but none implement concentration-controlled MoE routing on that hardware. Confirms verifier.",
     "recheck_searches": [{"n": 1, "query": "Extropic Normal Computing thermodynamic chip expert routing gating neural network", "results": [
       {"title": "Extropic TSU Review (Medium)", "url": "https://medium.com/@cognidownunder/extropic-tsu-review-physics-beats-math-and-this-startup-just-proved-it-with-a-chip-that-thinks-in-9082868de469"},
       {"title": "Extropic is building thermodynamic computing hardware (Hacker News)", "url": "https://news.ycombinator.com/item?id=45750995"},
       {"title": "Thermodynamic Computing: From Zero to One (Extropic)", "url": "https://extropic.ai/writing/thermodynamic-computing-from-zero-to-one"},
       {"title": "Thermodynamic Computing Becomes Cool (Communications of the ACM)", "url": "https://cacm.acm.org/news/thermodynamic-computing-becomes-cool/"}]}],
     "reasoning_trace": {"step": "independent re-verification CAND_019_002", "inputs_seen": "verifier verdict (no collision) + my vendor-hardware re-search; Extropic/Normal Computing TSU confirmed real", "reasoning": "The hardware exists (TSU samples from EBMs via Gibbs), but no source runs MoE concentration routing on it. Confirms the fusion is unoccupied.", "decision": "confirm verifier no-collision; no mismatch", "confidence": "high - hardware and MoE clusters clearly separate", "could_be_wrong_if": "Extropic's pMoG/EBM sampler is functionally a thermodynamic MoE router"}},
    {"cand_id": "CAND_019_003", "agent3_collision_found": false, "agent4_collision": false, "mismatch_with_agent3": false,
     "notes": "Re-probed the Sivak-Crooks thermodynamic-length framework directly. CONFIRMED that optimal annealing/driving schedules ARE friction-tensor (Fisher-information-metric) geodesics (Thermodynamic Metrics and Optimal Paths 1201.4166; Geometry of thermodynamic control; minimally-dissipative erasure via thermodynamic length 2209.01852). The crosscheck summary explicitly noted these works 'do not contain specific information about HARDWARE implementations.' So the PRINCIPLE is established; only the sampling-hardware application is unclaimed. Confirms verifier (no exact fused-niche paper) AND reconfirms this as the lowest-margin / lowest-novelty candidate.",
     "recheck_searches": [{"n": 1, "query": "thermodynamic length geodesic optimal annealing schedule sampling hardware Crooks Sivak", "results": [
       {"title": "Optimal schedules for annealing algorithms", "url": "https://arxiv.org/html/2402.14717v1"},
       {"title": "Thermodynamic length in open quantum systems (Quantum journal)", "url": "https://quantum-journal.org/papers/q-2019-10-24-197/"},
       {"title": "Thermodynamic Metrics and Optimal Paths (Sivak & Crooks, PRL)", "url": "https://link.aps.org/doi/10.1103/PhysRevLett.108.190602"},
       {"title": "[1201.4166] Thermodynamic metrics and optimal paths", "url": "https://arxiv.org/abs/1201.4166"},
       {"title": "Minimally dissipative information erasure in a quantum dot via thermodynamic length", "url": "https://arxiv.org/pdf/2209.01852"},
       {"title": "Thermodynamic Length, Time, Speed and Optimum Path to Minimize Entropy Production", "url": "https://arxiv.org/pdf/cond-mat/9503174"}]}],
     "reasoning_trace": {"step": "independent re-verification CAND_019_003", "inputs_seen": "verifier verdict (lowest margin) + my direct Sivak-Crooks re-search; thermodynamic-length geodesic = optimal schedule confirmed", "reasoning": "I probed the exact prior framework. Sivak-Crooks thermodynamic length ESTABLISHES that minimum-dissipation annealing schedules are geodesics of the friction (Fisher-type) metric. So the candidate's core claim is a known principle; only the application to thermodynamic-sampling-HARDWARE is unclaimed. I uphold the verifier's no-exact-collision verdict while strongly agreeing this is the lowest-novelty candidate -- it would likely fail external novelty review even setting aside the volume floor.", "decision": "confirm verifier no-collision; no mismatch (but lowest margin -- principle already established)", "confidence": "medium - genuinely borderline; a reviewer could call it a collision", "could_be_wrong_if": "the friction-tensor geodesic schedule IS the proposed schedule with no meaningful hardware-specific delta -> then it is a true collision"}},
    {"cand_id": "CAND_019_004", "agent3_collision_found": false, "agent4_collision": false, "mismatch_with_agent3": false,
     "notes": "Re-probed the von Mises-Fisher / curvature angle. Found GeoMoE curvature-guided routing (2603.22317) and vMF as GrMoE's stated predecessor, but no Fisher-Rao SCHEDULE of Bingham concentration. Confirms verifier.",
     "recheck_searches": [{"n": 1, "query": "von Mises-Fisher Bingham routing schedule information geometry expert gating mixture of experts", "results": [
       {"title": "Grassmannian MoE (SOURCE P1)", "url": "https://arxiv.org/pdf/2602.17798"},
       {"title": "MoB: Mixture of Bidders (Truthful Auction for Continual Learning in MoE)", "url": "https://arxiv.org/html/2512.10969"},
       {"title": "Mixture-of-Experts with Expert Choice Routing (Google Research)", "url": "https://research.google/blog/mixture-of-experts-with-expert-choice-routing/"},
       {"title": "Geometric Mixture-of-Experts with Curvature-Guided Adaptive Routing", "url": "https://arxiv.org/pdf/2603.22317"}]}],
     "reasoning_trace": {"step": "independent re-verification CAND_019_004", "inputs_seen": "verifier verdict (no collision) + my vMF/curvature re-search; GeoMoE curvature routing found", "reasoning": "Geometric/curvature routing exists (GeoMoE) and vMF is the predecessor of GrMoE, but none apply a Fisher-Rao schedule to Bingham concentration. Confirms verifier.", "decision": "confirm verifier no-collision; no mismatch", "confidence": "medium - geometric routing active", "could_be_wrong_if": "GeoMoE's curvature schedule equals the Fisher-Rao concentration schedule"}},
    {"cand_id": "CAND_019_005", "agent3_collision_found": false, "agent4_collision": false, "mismatch_with_agent3": false,
     "notes": "Re-probed the physical-Boltzmann-sampler angle. Found p-bit/MTJ, laser-network, and quantum-annealer Boltzmann samplers, but engine explicitly found no 'categorical gate / expert routing / directional distribution' in that context. Confirms verifier.",
     "recheck_searches": [{"n": 1, "query": "physical Boltzmann sampler categorical gate expert routing directional distribution hardware", "results": [
       {"title": "Simulating the classical XY model with a laser network", "url": "https://arxiv.org/pdf/1608.00358"},
       {"title": "On the Challenges of Physical Implementations of RBMs", "url": "https://arxiv.org/pdf/1312.5258"},
       {"title": "One-Step Sampler for Boltzmann Distributions via Drifting", "url": "https://arxiv.org/pdf/2603.17579"},
       {"title": "Boltzmann sampler (Wikipedia, non-paper)", "url": "https://en.wikipedia.org/wiki/Boltzmann_sampler"}]}],
     "reasoning_trace": {"step": "independent re-verification CAND_019_005", "inputs_seen": "verifier verdict (no collision) + my physical-Boltzmann-sampler re-search; p-bit/laser/quantum samplers found", "reasoning": "Physical Boltzmann samplers exist (p-bits, laser networks, quantum annealers) but none gate MoE experts via a directional (Bingham) distribution. Confirms verifier.", "decision": "confirm verifier no-collision; no mismatch", "confidence": "high - no categorical-gate/expert-routing hit in the hardware-sampler cluster", "could_be_wrong_if": "a p-bit paper implements categorical expert gating"}}
  ]
}
```

## [REPORT 6] audit+quality (verbatim)

### reasoning_audit.json
```json
{
  "run_id": "run_019",
  "agent": "5_reasoning_auditor",
  "audited_at": "2026-06-01T22:43:34.692622+00:00",
  "summary": {
    "total_traces_audited": 61,
    "all_complete": true,
    "n_complete": 61,
    "n_flagged_nonfatal": 32,
    "n_logic_breaks": 0,
    "logic_break_trace_ids": [],
    "by_agent": {
      "AGENT_1_decomposer": {
        "traces": 11,
        "complete": 11,
        "flagged": 4,
        "logic_breaks": 0
      },
      "AGENT_2_atom_search": {
        "traces": 10,
        "complete": 10,
        "flagged": 2,
        "logic_breaks": 0
      },
      "AGENT_3_merger": {
        "traces": 5,
        "complete": 5,
        "flagged": 0,
        "logic_breaks": 0
      },
      "AGENT_4_verifier": {
        "traces": 30,
        "complete": 30,
        "flagged": 26,
        "logic_breaks": 0
      },
      "AGENT_4_crosschecker": {
        "traces": 5,
        "complete": 5,
        "flagged": 0,
        "logic_breaks": 0
      }
    },
    "consistency_checks_fired": 25
  },
  "audits": [
    {
      "trace_id": "atoms.overall",
      "source_agent": "AGENT_1_decomposer",
      "step": "read direction_params (epoch 1) then decompose 3 verbatim abstracts",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.8,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atoms.overall",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.8; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P1_S1",
      "source_agent": "AGENT_1_decomposer",
      "step": "P1 sentence 1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.75,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P1_S1",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.75; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P1_S2",
      "source_agent": "AGENT_1_decomposer",
      "step": "P1 sentence 2",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.5,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P1_S2",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.5; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P1_S3",
      "source_agent": "AGENT_1_decomposer",
      "step": "P1 sentence 3",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.5,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P1_S3",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.5; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P1_S4",
      "source_agent": "AGENT_1_decomposer",
      "step": "P1 sentence 4",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.75,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P1_S4",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.75; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P2_S1",
      "source_agent": "AGENT_1_decomposer",
      "step": "P2 sentence 1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.5,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P2_S1",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.5; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P2_S2",
      "source_agent": "AGENT_1_decomposer",
      "step": "P2 sentence 2",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.5,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P2_S2",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.5; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P3_S1",
      "source_agent": "AGENT_1_decomposer",
      "step": "P3 sentence 1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.5,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P3_S1",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.5; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P3_S2",
      "source_agent": "AGENT_1_decomposer",
      "step": "P3 sentence 2",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.5,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P3_S2",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.5; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P3_S3",
      "source_agent": "AGENT_1_decomposer",
      "step": "P3 sentence 3",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.5,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P3_S3",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.5; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atom.R19_P3_S4",
      "source_agent": "AGENT_1_decomposer",
      "step": "P3 sentence 4",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.667,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_1_decomposer :: atom.R19_P3_S4",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.667; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P1_S1",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P1_S1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.286,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "sparse",
        "evidence": [
          "sparse"
        ],
        "data_paper_hits": 1,
        "sparse_threshold": 10,
        "data_is_sparse": true
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P1_S1",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.286; linked={'paper_hits': 1}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P1_S2",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P1_S2",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.6,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "sparse",
        "evidence": [
          "sparse"
        ],
        "data_paper_hits": 4,
        "sparse_threshold": 10,
        "data_is_sparse": true
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P1_S2",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.6; linked={'paper_hits': 4}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P1_S3",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P1_S3",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.4,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "sparse",
        "evidence": [
          "sparse"
        ],
        "data_paper_hits": 3,
        "sparse_threshold": 10,
        "data_is_sparse": true
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P1_S3",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.4; linked={'paper_hits': 3}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P1_S4",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P1_S4",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.2,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "sparse",
        "evidence": [
          "sparse"
        ],
        "data_paper_hits": 4,
        "sparse_threshold": 10,
        "data_is_sparse": true
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P1_S4",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.2; linked={'paper_hits': 4}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P2_S1",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P2_S1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.2,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "sparse",
        "evidence": [
          "sparse"
        ],
        "data_paper_hits": 5,
        "sparse_threshold": 10,
        "data_is_sparse": true
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P2_S1",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.2; linked={'paper_hits': 5}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P2_S2",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P2_S2",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.2,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "sparse",
        "evidence": [
          "sparse"
        ],
        "data_paper_hits": 3,
        "sparse_threshold": 10,
        "data_is_sparse": true
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P2_S2",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.2; linked={'paper_hits': 3}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P3_S1",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P3_S1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.25,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "sparse",
        "evidence": [
          "sparse",
          "niche"
        ],
        "data_paper_hits": 3,
        "sparse_threshold": 10,
        "data_is_sparse": true
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P3_S1",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.25; linked={'paper_hits': 3}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P3_S2",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P3_S2",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.167,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "sparse",
        "evidence": [
          "sparse"
        ],
        "data_paper_hits": 5,
        "sparse_threshold": 10,
        "data_is_sparse": true
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P3_S2",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.167; linked={'paper_hits': 5}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P3_S3",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P3_S3",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.2,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "sparse",
        "evidence": [
          "sparse"
        ],
        "data_paper_hits": 4,
        "sparse_threshold": 10,
        "data_is_sparse": true
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P3_S3",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.2; linked={'paper_hits': 4}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "atomsearch.R19_P3_S4",
      "source_agent": "AGENT_2_atom_search",
      "step": "saturation R19_P3_S4",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.556,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "atom_sparsity",
        "trace_polarity": "ambiguous",
        "evidence": [
          "sparse",
          "mature"
        ],
        "data_paper_hits": 5,
        "sparse_threshold": 10,
        "data_is_sparse": true,
        "note": "polarity_indeterminate"
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_2_atom_search :: atomsearch.R19_P3_S4",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.556; linked={'paper_hits': 5}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "medium - prose polarity indeterminate; format checks still deterministic",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "merge.CAND_019_001",
      "source_agent": "AGENT_3_merger",
      "step": "merge ATOM A x ATOM B",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.235,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "merge_quote_context",
        "data_quote_verified": true,
        "note": "merge decision is a niche; quote grounding checked by MAIN Gate-4"
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_3_merger :: merge.CAND_019_001",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.235; linked={'quote_verified_substring': True}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "medium - prose polarity indeterminate; format checks still deterministic",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "merge.CAND_019_002",
      "source_agent": "AGENT_3_merger",
      "step": "merge ATOM A x ATOM B",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.5,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "merge_quote_context",
        "data_quote_verified": true,
        "note": "merge decision is a niche; quote grounding checked by MAIN Gate-4"
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_3_merger :: merge.CAND_019_002",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.5; linked={'quote_verified_substring': True}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "medium - prose polarity indeterminate; format checks still deterministic",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "merge.CAND_019_003",
      "source_agent": "AGENT_3_merger",
      "step": "merge ATOM A x ATOM B",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.208,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "merge_quote_context",
        "data_quote_verified": true,
        "note": "merge decision is a niche; quote grounding checked by MAIN Gate-4"
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_3_merger :: merge.CAND_019_003",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.208; linked={'quote_verified_substring': True}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "medium - prose polarity indeterminate; format checks still deterministic",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "merge.CAND_019_004",
      "source_agent": "AGENT_3_merger",
      "step": "merge ATOM A x ATOM B",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.389,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "merge_quote_context",
        "data_quote_verified": true,
        "note": "merge decision is a niche; quote grounding checked by MAIN Gate-4"
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_3_merger :: merge.CAND_019_004",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.389; linked={'quote_verified_substring': True}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "medium - prose polarity indeterminate; format checks still deterministic",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "merge.CAND_019_005",
      "source_agent": "AGENT_3_merger",
      "step": "merge ATOM A x ATOM B",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.409,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "merge_quote_context",
        "data_quote_verified": true,
        "note": "merge decision is a niche; quote grounding checked by MAIN Gate-4"
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_3_merger :: merge.CAND_019_005",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.409; linked={'quote_verified_substring': True}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "medium - prose polarity indeterminate; format checks still deterministic",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.verdict.CAND_019_001",
      "source_agent": "AGENT_4_verifier",
      "step": "collision verdict CAND_019_001",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "verify_collision",
        "trace_polarity": "no_collision",
        "evidence": [
          "no collision",
          "no paper",
          "unoccupied"
        ],
        "data_collision_found": false
      },
      "logic_break": false,
      "flags": [
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.verdict.CAND_019_001",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={'collision_found': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_001.n1",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_001.n1",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_001.n2",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 2 prior-art probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_001.n2",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_001.n3",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 3",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_001.n3",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_001.n4",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 4 survey probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_001.n4",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_001.n5",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 5 closest-neighbor probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.75,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_001.n5",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.75; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.verdict.CAND_019_002",
      "source_agent": "AGENT_4_verifier",
      "step": "collision verdict CAND_019_002",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.4,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "verify_collision",
        "trace_polarity": "no_collision",
        "evidence": [
          "no collision",
          "no paper",
          "unoccupied"
        ],
        "data_collision_found": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.verdict.CAND_019_002",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.4; linked={'collision_found': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_002.n1",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_002.n1",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_002.n2",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 2 prior-art probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_002.n2",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_002.n3",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 3",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_002.n3",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_002.n4",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 4",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_002.n4",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_002.n5",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 5",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_002.n5",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.verdict.CAND_019_003",
      "source_agent": "AGENT_4_verifier",
      "step": "collision verdict CAND_019_003 (LOWEST MARGIN)",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.25,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "verify_collision",
        "trace_polarity": "no_collision",
        "evidence": [
          "no collision",
          "novel"
        ],
        "data_collision_found": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.verdict.CAND_019_003",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.25; linked={'collision_found': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_003.n1",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_003.n1",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_003.n2",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 2 prior-art probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.333,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_003.n2",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.333; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_003.n3",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 3 geodesic-driving probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.4,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_003.n3",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.4; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_003.n4",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 4 survey probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.667,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_003.n4",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.667; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_003.n5",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 5 MoE-bridge probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_003.n5",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.verdict.CAND_019_004",
      "source_agent": "AGENT_4_verifier",
      "step": "collision verdict CAND_019_004",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "verify_collision",
        "trace_polarity": "no_collision",
        "evidence": [
          "no collision",
          "no paper",
          "unoccupied"
        ],
        "data_collision_found": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.verdict.CAND_019_004",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={'collision_found': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_004.n1",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_004.n1",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_004.n2",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 2 prior-art probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_004.n2",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_004.n3",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 3",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_004.n3",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_004.n4",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 4 survey probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_004.n4",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_004.n5",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 5",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_004.n5",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.verdict.CAND_019_005",
      "source_agent": "AGENT_4_verifier",
      "step": "collision verdict CAND_019_005",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "verify_collision",
        "trace_polarity": "no_collision",
        "evidence": [
          "no collision",
          "unoccupied"
        ],
        "data_collision_found": false
      },
      "logic_break": false,
      "flags": [
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.verdict.CAND_019_005",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={'collision_found': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_005.n1",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 1",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_005.n1",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_005.n2",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 2 prior-art probe",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_005.n2",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_005.n3",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 3",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_005.n3",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_005.n4",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 4",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_005.n4",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "verify.reform.CAND_019_005.n5",
      "source_agent": "AGENT_4_verifier",
      "step": "reform 5",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": false,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.0,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": false
      },
      "logic_break": false,
      "flags": [
        "confidence:missing_rationale",
        "low_inputs_grounding(0.0)"
      ],
      "verdict": "FLAGGED_NONFATAL",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_verifier :: verify.reform.CAND_019_005.n5",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.0; linked={}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "FLAGGED_NONFATAL",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "crosscheck.CAND_019_001",
      "source_agent": "AGENT_4_crosschecker",
      "step": "independent re-verification CAND_019_001",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.25,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "crosscheck_confirm",
        "trace_polarity": "confirm",
        "evidence": [
          "confirm",
          "agree",
          "uphold"
        ],
        "data_mismatch_with_agent3": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_crosschecker :: crosscheck.CAND_019_001",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.25; linked={'mismatch_with_agent3': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "crosscheck.CAND_019_002",
      "source_agent": "AGENT_4_crosschecker",
      "step": "independent re-verification CAND_019_002",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.25,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "crosscheck_confirm",
        "trace_polarity": "confirm",
        "evidence": [
          "confirm",
          "agree"
        ],
        "data_mismatch_with_agent3": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_crosschecker :: crosscheck.CAND_019_002",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.25; linked={'mismatch_with_agent3': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "crosscheck.CAND_019_003",
      "source_agent": "AGENT_4_crosschecker",
      "step": "independent re-verification CAND_019_003",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.444,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "crosscheck_confirm",
        "trace_polarity": "confirm",
        "evidence": [
          "confirm",
          "agree",
          "uphold"
        ],
        "data_mismatch_with_agent3": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_crosschecker :: crosscheck.CAND_019_003",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.444; linked={'mismatch_with_agent3': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "crosscheck.CAND_019_004",
      "source_agent": "AGENT_4_crosschecker",
      "step": "independent re-verification CAND_019_004",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "medium",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.25,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "crosscheck_confirm",
        "trace_polarity": "confirm",
        "evidence": [
          "confirm",
          "agree"
        ],
        "data_mismatch_with_agent3": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_crosschecker :: crosscheck.CAND_019_004",
        "inputs_seen": "fields_present=True; confidence=medium; grounding=0.25; linked={'mismatch_with_agent3': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    },
    {
      "trace_id": "crosscheck.CAND_019_005",
      "source_agent": "AGENT_4_crosschecker",
      "step": "independent re-verification CAND_019_005",
      "complete": true,
      "missing_fields": [],
      "confidence_level": "high",
      "confidence_wellformed": true,
      "falsifiable": true,
      "inputs_grounding_overlap": 0.25,
      "overconfident": false,
      "hedges_found": [],
      "decision_data_consistency": {
        "checked": true,
        "kind": "crosscheck_confirm",
        "trace_polarity": "confirm",
        "evidence": [
          "confirm",
          "agree"
        ],
        "data_mismatch_with_agent3": false
      },
      "logic_break": false,
      "flags": [],
      "verdict": "VALID",
      "audit_reasoning_trace": {
        "step": "audit AGENT_4_crosschecker :: crosscheck.CAND_019_005",
        "inputs_seen": "fields_present=True; confidence=high; grounding=0.25; linked={'mismatch_with_agent3': False}",
        "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
        "decision": "VALID",
        "confidence": "high - deterministic over committed JSON",
        "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."
      }
    }
  ]
}
```

### search_quality.json
```json
{
  "run_id": "run_019",
  "agent": "5_search_quality",
  "scored_at": "2026-06-01T22:43:34.696297+00:00",
  "params_used": {
    "specificity": 0.5,
    "mechanism_focus": 0.5,
    "sparsity_seeking": 0.5,
    "cross_paper_pairing": 0.5,
    "collision_avoidance_phrasing": 0.5
  },
  "n_queries": 43,
  "dimension_means": {
    "specificity": 0.9913,
    "mechanism_focus": 0.9535,
    "sparsity_seeking": 0.7093,
    "cross_paper_pairing": 0.8953,
    "collision_avoidance": 0.4419
  },
  "avg_search_quality": 0.7983,
  "formula": "avg_search_quality = sum_k(param_k * mean_dim_k)/sum_k(param_k)",
  "per_query": [
    {
      "source": "agent1_sourcer",
      "query": "arxiv 2602.17798 Grassmannian Mixture-of-Experts Concentration-Controlled Routing on Subspace Manifolds abstract",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent1_sourcer",
      "query": "arxiv 2508.04884 The Cosine Schedule is Fisher-Rao-Optimal for Masked Discrete Diffusion Models abstract",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.6,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent1_sourcer",
      "query": "arxiv 2601.04358 Energy-Time-Accuracy Tradeoffs in Thermodynamic Computing abstract",
      "dims": {
        "specificity": 0.75,
        "mechanism_focus": 0.6,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 0.5,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P1_S1",
      "query": "mixture of experts softmax gating sparsity utilization tradeoff router",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.1,
        "cross_paper_pairing": 0.5,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P1_S2",
      "query": "Matrix Bingham distribution gating weights Grassmannian manifold subspaces mixture of experts routing",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P1_S3",
      "query": "concentration matrix continuously controls routing entropy replacing top-k smooth sparsity mixture of experts",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.1,
        "cross_paper_pairing": 0.5,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P1_S4",
      "query": "amortized variational inference posterior routing distributions uncertainty-aware expert assignment mixture of experts",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 0.5,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P2_S1",
      "query": "information geometry induced probability path discretisation schedule masked discrete diffusion sampling",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P2_S2",
      "query": "Fisher-Rao geometry optimal schedule recovers cosine schedule masked discrete diffusion",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.6,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P3_S1",
      "query": "thermodynamic computing hardware stochastic process sample from distribution of interest",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 0.5,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P3_S2",
      "query": "theoretical characterization resource cost thermodynamic computation energy efficiency performance",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.2,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 0.5,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P3_S3",
      "query": "tradeoff computational accuracy energy dissipation time thermodynamic computing",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 0.5,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent2_atomsearch:R19_P3_S4",
      "query": "energy-delay-deficiency product geometric bounds entropy production thermodynamic computing",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 0.5,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_001:n1",
      "query": "Fisher-Rao optimal annealing schedule continuous MoE routing entropy sparsity",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_001:n2",
      "query": "information geometry schedule routing entropy concentration mixture of experts prior work",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_001:n3",
      "query": "Fisher-Rao geodesic schedule anneal routing sparsity top-k mixture of experts",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_001:n4",
      "query": "optimal schedule routing entropy masked diffusion mixture of experts survey",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.1,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_001:n5",
      "query": "Fisher-Rao cosine schedule applied to mixture of experts routing entropy already studied",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_002:n1",
      "query": "thermodynamic computing hardware mixture of experts routing concentration sampling",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_002:n2",
      "query": "physical stochastic hardware sample expert routing distribution concentration entropy prior work",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.1,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_002:n3",
      "query": "thermodynamic sampler concentration-controlled mixture of experts routing entropy hardware",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_002:n4",
      "query": "energy-based hardware sampling expert routing concentration neural network",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.1,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_002:n5",
      "query": "thermodynamic mixture of experts routing concentration controlled hardware published",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_003:n1",
      "query": "Fisher-Rao optimal annealing schedule thermodynamic sampling hardware",
      "dims": {
        "specificity": 0.875,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_003:n2",
      "query": "information geometry schedule thermodynamic computing stochastic sampling prior work",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_003:n3",
      "query": "geodesic optimal driving protocol thermodynamic sampler Fisher-Rao schedule entropy production",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_003:n4",
      "query": "optimal schedule thermodynamic computing entropy production information geometry survey",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_003:n5",
      "query": "Fisher-Rao schedule thermodynamic hardware sampling mixture of experts already studied",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_004:n1",
      "query": "Fisher-Rao optimal concentration schedule Grassmannian mixture of experts Bingham routing",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_004:n2",
      "query": "information geometry schedule Matrix Bingham concentration routing manifold mixture of experts prior work",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_004:n3",
      "query": "Grassmannian mixture of experts Bingham gating annealing Fisher-Rao geometry schedule",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_004:n4",
      "query": "concentration parameter schedule subspace routing optimal masked diffusion mixture of experts survey",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_004:n5",
      "query": "Fisher-Rao Bingham concentration schedule mixture of experts already studied",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_005:n1",
      "query": "thermodynamic sampling Grassmannian Bingham gates mixture of experts routing",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_005:n2",
      "query": "physical sampler Bingham distribution gating manifold expert routing prior work",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_verify:CAND_019_005:n3",
      "query": "thermodynamic hardware directional distribution sampling expert gates mixture of experts",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_005:n4",
      "query": "neutral-atom quantum thermodynamic sampling Bingham routing neural network",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_verify:CAND_019_005:n5",
      "query": "thermodynamic Bingham gate sampling mixture of experts already published",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent4_crosscheck:CAND_019_001:n1",
      "query": "entropy regulariser schedule routing information geometry reinforcement learning Fisher-Rao gradient flow",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_crosscheck:CAND_019_002:n1",
      "query": "Extropic Normal Computing thermodynamic chip expert routing gating neural network",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_crosscheck:CAND_019_003:n1",
      "query": "thermodynamic length geodesic optimal annealing schedule sampling hardware Crooks Sivak",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_crosscheck:CAND_019_004:n1",
      "query": "von Mises-Fisher Bingham routing schedule information geometry expert gating mixture of experts",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 1.0,
        "cross_paper_pairing": 1.0,
        "collision_avoidance": 0.2
      }
    },
    {
      "source": "agent4_crosscheck:CAND_019_005:n1",
      "query": "physical Boltzmann sampler categorical gate expert routing directional distribution hardware",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "sparsity_seeking": 0.5,
        "cross_paper_pairing": 0.5,
        "collision_avoidance": 0.2
      }
    }
  ]
}
```

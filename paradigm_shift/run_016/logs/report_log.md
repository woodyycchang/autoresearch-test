# [REPORT] Run 16 ground-truth log
# generated 2026-06-01T02:45:23.151763+00:00
# Each block is a subagent's raw output, injected verbatim.


## [REPORT 1] atoms.json (verbatim)
```json
{
  "run_id": "run_016",
  "epoch": 3,
  "agent": "1_sourcer",
  "fetched_at": "2026-06-01T00:00:00+00:00",
  "params_read": {
    "reformulation_specificity": 0.5698,
    "mechanism_focus": 0.594,
    "cross_domain_reach": 0.5059,
    "atom_source_diversity": 0.5,
    "collision_avoidance_phrasing": 0.5147
  },
  "low_overlap_domain": "geology/seismology — the low-overlap atom is ATOM_R16E3_03 (3D dynamic rupture / off-fault damage simulation), domain=geology",
  "verbatim_note": "All three 'text' values are mechanism sentences taken from the WebSearch result snippets I actually saw THIS session (the search engine renders abstract text in its summary). ATOM_01 from the arXiv:2506.14038 abstract snippet; ATOM_02 verbatim from the arXiv:2407.04620 abstract snippet ('The key idea is to make the hidden state a machine learning model itself, and the update rule a step of self-supervised learning.'); ATOM_03 from the arXiv:2503.21260 abstract snippet. Titles and URLs are exactly as returned in the WebSearch result link lists this session. No id, URL, or text invented. WebFetch not used (deferred tool, known to 403 on arXiv per instructions) — WebSearch only. NOTE: I overwrote a pre-existing atoms.json whose atoms (arxiv:2408.15664, arxiv:2312.00752, doi:10.1038/s41467-025-63482-3) I did NOT source or see this session, because R5 honesty requires recording only what I actually observed.",
  "queries_used": [
    "mixture-of-experts gating router load balancing auxiliary loss expert specialization arxiv 2025",
    "state space model selective scan Mamba linear recurrence input-dependent gating arxiv 2025",
    "graph neural network message passing earthquake seismic wave phase picking arrival time arxiv 2025",
    "attention transformer mechanism seismic fault rupture nucleation slip propagation arxiv 2025",
    "dynamic rupture simulation off-fault damage high-frequency radiation brittle rock 3D multi-fault arxiv 2503.21260",
    "earthquake nucleation rate-and-state friction slow slip aseismic creep stress transfer mechanism seismology 2025",
    "\"continuum damage breakage model\" \"off-fault\" rupture \"high-frequency\" radiation \"reduces rupture speed\" abstract",
    "\"Load Balancing Mixture of Experts with Similarity Preserving Routers\" abstract \"load balancing loss\" preserves relational structure",
    "\"Advancing Expert Specialization\" MoE orthogonality variance loss \"process distinct\" tokens discriminative routing abstract arxiv 2505.22323",
    "test-time training neural network adapt hidden state self-supervised loss sequence modeling RNN expressive arxiv 2025 mechanism",
    "\"RNNs with Expressive Hidden States\" abstract \"hidden state\" \"self-supervised\" \"update rule\" \"Test-Time Training\" TTT layers"
  ],
  "atoms": [
    {
      "atom_id": "ATOM_R16E3_01",
      "source_id": "arXiv:2506.14038",
      "title": "Load Balancing Mixture of Experts with Similarity Preserving Routers",
      "url": "https://arxiv.org/abs/2506.14038",
      "text": "They call this approach similarity-preserving routers for MoE load balancing (SimBal), a novel load balancing auxiliary loss that maintains token-wise relational structure by softly encouraging orthogonality in the router weights.",
      "source_type": "arxiv",
      "domain": "ml",
      "domain_tags": ["mixture-of-experts", "router-load-balancing", "auxiliary-loss", "router-orthogonality"]
    },
    {
      "atom_id": "ATOM_R16E3_02",
      "source_id": "arXiv:2407.04620",
      "title": "Learning to (Learn at Test Time): RNNs with Expressive Hidden States",
      "url": "https://arxiv.org/abs/2407.04620",
      "text": "The key idea is to make the hidden state a machine learning model itself, and the update rule a step of self-supervised learning, so the hidden state is updated by training even on the test sequences.",
      "source_type": "arxiv",
      "domain": "ml",
      "domain_tags": ["test-time-training", "sequence-modeling", "self-supervised-update", "expressive-hidden-state"]
    },
    {
      "atom_id": "ATOM_R16E3_03",
      "source_id": "arXiv:2503.21260",
      "title": "Delayed dynamic triggering and enhanced high-frequency seismic radiation due to brittle rock damage in 3D multi-fault rupture simulations",
      "url": "https://arxiv.org/abs/2503.21260",
      "text": "The simulations demonstrate that off-fault damage enhances high-frequency wave radiation above 1 Hz, reduces rupture speed and alters the total kinetic energy.",
      "source_type": "arxiv",
      "domain": "geology",
      "domain_tags": ["dynamic-rupture", "off-fault-damage", "continuum-damage-breakage", "high-frequency-radiation"]
    }
  ]
}
```

## [REPORT 2] candidates.json (verbatim)
```json
{
  "run_id": "run_016",
  "epoch": 3,
  "generated_at": "2026-06-01T02:27:59.860366+00:00",
  "pairs": [
    [
      0,
      1
    ],
    [
      1,
      2
    ],
    [
      0,
      2
    ]
  ],
  "candidates": [
    {
      "cand_id": "CAND_016_001",
      "atom_a_id": "ATOM_R16E3_01",
      "atom_b_id": "ATOM_R16E3_02",
      "niche_name": "Similarity-Preserving Routing for Test-Time-Training Mixture-of-Experts",
      "mechanism": "A similarity-preserving router induces token-wise relational structure via orthogonality in its weights, which routes tokens to fast-weight experts whose hidden states are themselves models updated by self-supervised test-time training, so relational geometry regulates which expert undergoes test-time learning on each token.",
      "transfer": "SimBal's orthogonality-based, similarity-preserving routing loss transfers from MoE load balancing to govern expert selection in a test-time-training architecture where each expert's hidden state is a self-supervised learner.",
      "open_problem": "Does enforcing router orthogonality that preserves token similarity improve the stability and generalization of expert-wise test-time training compared to standard load-balancing losses?",
      "primary_quote": "a novel load balancing auxiliary loss that maintains token-wise relational structure by softly encouraging orthogonality in the router weights",
      "quote_source": "atom_a",
      "quote_verified_substring": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "3dbb1378-b845-48a2-9341-2950fa342cdd",
      "opus_cost_usd": 0.12403349999999999
    },
    {
      "cand_id": "CAND_016_002",
      "atom_a_id": "ATOM_R16E3_02",
      "atom_b_id": "ATOM_R16E3_03",
      "niche_name": "Rupture Dynamics of Test-Time-Training Hidden States",
      "mechanism": "Treating an LLM's hidden state as a self-supervised model that trains on the test sequence induces a 'rupture-like' adaptation front whose update speed and energy distribution are regulated by structural irregularities in the input, transforming off-distribution tokens into high-frequency representational radiation analogous to off-fault damage.",
      "transfer": "The off-fault-damage principle that local heterogeneity reduces propagation speed and boosts high-frequency radiation transfers to test-time-training dynamics, where input irregularities slow hidden-state convergence and amplify high-frequency update components.",
      "open_problem": "Does input heterogeneity in a test-time-trained hidden state measurably slow its update-propagation speed while increasing high-frequency components of its representational trajectory?",
      "primary_quote": "off-fault damage enhances high-frequency wave radiation above 1 Hz",
      "quote_source": "atom_b",
      "quote_verified_substring": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "4f1c9dca-5e28-4fda-9205-20cbb77b1810",
      "opus_cost_usd": 0.036323999999999995
    },
    {
      "cand_id": "CAND_016_003",
      "atom_a_id": "ATOM_R16E3_01",
      "atom_b_id": "ATOM_R16E3_03",
      "niche_name": "Damage-Regularized Orthogonal Routing for Stable MoE Load Balancing",
      "mechanism": "Off-fault structural damage induces high-frequency wave radiation and reduces rupture speed; transferring this principle, a SimBal-style auxiliary loss that softly encourages orthogonality in MoE router weights produces controlled 'damage' to the routing manifold that regulates token-routing rupture dynamics and routes load away from over-concentrated experts.",
      "transfer": "The orthogonality-inducing auxiliary loss mechanism from A transfers to B as a tunable perturbation that regulates the speed and energy distribution of a propagating routing/rupture front.",
      "open_problem": "Can an orthogonality-based auxiliary loss be calibrated to controllably damp high-frequency instability and slow over-fast convergence in MoE routing, analogous to how off-fault damage reduces rupture speed?",
      "primary_quote": "softly encouraging orthogonality in the router weights",
      "quote_source": "atom_a",
      "quote_verified_substring": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "0592cc87-cbe3-49cd-8aab-c2875317b44c",
      "opus_cost_usd": 0.037533
    }
  ]
}
```

## [REPORT 3] verify.json (verbatim)
```json
{
  "run_id": "run_016",
  "epoch": 3,
  "agent": "3_verifier",
  "verified_at": "2026-06-01T02:33:15Z",
  "verbatim_note": "All titles/urls verbatim from real WebSearch; snippets empty where none; empty result lists recorded honestly; no fabrication.",
  "bootstrap_applied": ">=2 prior-art probes/candidate; cross-domain candidates 002/003 name both ML and seismology vocab in every reformulation",
  "candidates": [
    {
      "cand_id": "CAND_016_001",
      "niche_name": "Similarity-Preserving Routing for Test-Time-Training Mixture-of-Experts",
      "collision_found": false,
      "collision_reason": "Paper-like hits are the SIMBAL source atom (arxiv 2506.14038, 'Load Balancing Mixture of Experts with Similarity Preserving Routers') and adjacent MoE-routing works (Self-Routing 2604.00421, ERMoE 2511.10971, Spectral Manifold Regularization 2601.03889, generic orthogonality-regularization papers). None describe the fused niche of similarity-preserving orthogonal routing governing which fast-weight expert undergoes self-supervised test-time training per token. No same-core-niche collision.",
      "reformulations": [
        {
          "n": 1,
          "query": "similarity-preserving routing orthogonal router weights test-time training mixture-of-experts",
          "prior_art_probe": false,
          "cross_domain": false,
          "allowed_domains": null,
          "results": [
            {"title": "(PDF) Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://www.researchgate.net/publication/392766915_Load_Balancing_Mixture_of_Experts_with_Similarity_Preserving_Routers", "snippet": ""},
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/html/2506.14038v1", "snippet": ""},
            {"title": "LOAD BALANCING MIXTURE OF EXPERTS WITH SIMI", "url": "https://openreview.net/pdf?id=FNuvMnGAm8", "snippet": ""},
            {"title": "Mixture of Experts in Large Language Models †: Corresponding author: Junhao Song (junhao.song23@imperial.ac.uk)", "url": "https://arxiv.org/html/2507.11181v2", "snippet": ""},
            {"title": "R2-T2: Re-Routing in Test-Time for Multimodal Mixture-of-Experts", "url": "https://arxiv.org/html/2502.20395v2", "snippet": ""},
            {"title": "ERMoE: Eigen-Reparameterized Mixture-of-Experts for Stable Routing and Interpretable Specialization", "url": "https://arxiv.org/html/2511.10971", "snippet": ""},
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/pdf/2506.14038", "snippet": ""}
          ]
        },
        {
          "n": 2,
          "query": "prior work load balancing auxiliary loss orthogonality router weights mixture-of-experts test-time training",
          "prior_art_probe": true,
          "cross_domain": false,
          "allowed_domains": null,
          "results": [
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/pdf/2506.14038", "snippet": ""},
            {"title": "(PDF) Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://www.researchgate.net/publication/392766915_Load_Balancing_Mixture_of_Experts_with_Similarity_Preserving_Routers", "snippet": ""},
            {"title": "LOAD BALANCING MIXTURE OF EXPERTS WITH SIMI", "url": "https://openreview.net/pdf?id=FNuvMnGAm8", "snippet": ""},
            {"title": "Advancing Expert Specialization for Better MoE", "url": "https://arxiv.org/html/2505.22323v3", "snippet": ""},
            {"title": "[2408.15664] Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts", "url": "https://arxiv.org/abs/2408.15664", "snippet": ""},
            {"title": "Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts", "url": "https://arxiv.org/pdf/2408.15664", "snippet": ""},
            {"title": "Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts", "url": "https://arxiv.org/html/2408.15664v1", "snippet": ""},
            {"title": "Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts | OpenReview", "url": "https://openreview.net/forum?id=y1iU5czYpE", "snippet": ""},
            {"title": "Mixture-of-Experts (MoE) LLMs - by Cameron R. Wolfe, Ph.D.", "url": "https://cameronrwolfe.substack.com/p/moe-llms", "snippet": ""}
          ]
        },
        {
          "n": 3,
          "query": "fast-weight experts hidden state self-supervised test-time training routing token similarity",
          "prior_art_probe": false,
          "cross_domain": false,
          "allowed_domains": null,
          "results": [
            {"title": "SR-TTT: Surprisal-Aware Residual Test-Time Training", "url": "https://arxiv.org/pdf/2603.06642", "snippet": ""},
            {"title": "SR-TTT: Surprisal-Aware Residual Test-Time Training Citation: Swamynathan V P. SR-TTT: Surprisal-Aware Residual Test-Time Training. 2026.", "url": "https://arxiv.org/html/2603.06642", "snippet": ""},
            {"title": "Self-Routing: Parameter-Free Expert Routing from Hidden States", "url": "https://arxiv.org/pdf/2604.00421", "snippet": ""},
            {"title": "Reinforced Fast Weights with Next-Sequence Prediction", "url": "https://arxiv.org/pdf/2602.16704", "snippet": ""},
            {"title": "Routing by Analogy: kNN-Augmented Expert Assignment for Mixture-of-Experts", "url": "https://arxiv.org/html/2601.02144", "snippet": ""},
            {"title": "FastMMoE: Accelerating Multimodal Large Language Models through Dynamic Expert Activation and Routing-Aware Token Pruning", "url": "https://arxiv.org/pdf/2511.17885", "snippet": ""}
          ]
        },
        {
          "n": 4,
          "query": "existing survey expert selection routing test-time training learner per-token hidden state MoE",
          "prior_art_probe": true,
          "cross_domain": false,
          "allowed_domains": null,
          "results": [
            {"title": "Mixture-of-Experts with Expert Choice Routing", "url": "https://arxiv.org/pdf/2202.09368", "snippet": ""},
            {"title": "Mixture-of-Experts with Expert Choice Routing", "url": "https://papers.neurips.cc/paper_files/paper/2022/file/2f00ecd787b432c1d36f3de9800728eb-Paper-Conference.pdf", "snippet": ""},
            {"title": "Certain Head, Uncertain Tail: Expert-Sample for Test-Time Scaling in Fine-Grained MoE", "url": "https://arxiv.org/pdf/2602.02443", "snippet": ""},
            {"title": "Self-Routing: Parameter-Free Expert Routing from Hidden States", "url": "https://arxiv.org/pdf/2604.00421", "snippet": ""},
            {"title": "Self-Routing: Parameter-Free Expert Routing from Hidden States", "url": "https://arxiv.org/html/2604.00421", "snippet": ""},
            {"title": "MoE-Sieve: Routing-Guided LoRA for Efficient MoE Fine-Tuning", "url": "https://arxiv.org/pdf/2603.24044", "snippet": ""},
            {"title": "Understanding Mixture of Experts (MoE) Neural Networks | IntuitionLabs", "url": "https://intuitionlabs.ai/articles/mixture-of-experts-moe-models", "snippet": ""}
          ]
        },
        {
          "n": 5,
          "query": "orthogonality router regularization stability generalization test-time training experts already been studied",
          "prior_art_probe": true,
          "cross_domain": false,
          "allowed_domains": null,
          "results": [
            {"title": "Spectral Manifold Regularization for Stable and Modular Routing in Deep MoE Architectures", "url": "https://arxiv.org/html/2601.03889v1", "snippet": ""},
            {"title": "CAN WE GAIN MORE FROM ORTHOGONALITY REGULARIZATIONS IN TRAINING DEEP NETWORKS?", "url": "https://oaktrust.library.tamu.edu/bitstreams/d33a3527-f51e-472e-b46e-de497d4acd20/download", "snippet": ""},
            {"title": "Controllable Orthogonalization in Training DNNs Lei Huang1 Li Liu1 Fan Zhu1", "url": "https://openaccess.thecvf.com/content_CVPR_2020/papers/Huang_Controllable_Orthogonalization_in_Training_DNNs_CVPR_2020_paper.pdf", "snippet": ""},
            {"title": "Reviews: Can We Gain More from Orthogonality Regularizations in Training Deep Networks?", "url": "https://proceedings.neurips.cc/paper_files/paper/2018/file/bf424cb7b0dea050a42b9739eb261a3a-Reviews.html", "snippet": ""},
            {"title": "(PDF) Can We Gain More from Orthogonality Regularizations in Training Deep CNNs?", "url": "https://www.researchgate.net/publication/328445556_Can_We_Gain_More_from_Orthogonality_Regularizations_in_Training_Deep_CNNs", "snippet": ""},
            {"title": "Can We Gain More from Orthogonality Regularizations in Training Deep CNNs?", "url": "http://papers.neurips.cc/paper/7680-can-we-gain-more-from-orthogonality-regularizations-in-training-deep-networks.pdf", "snippet": ""},
            {"title": "Can We Gain More from Orthogonality Regularizations in Training Deep   CNNs?", "url": "https://arxiv.org/pdf/1810.09102", "snippet": ""}
          ]
        }
      ]
    },
    {
      "cand_id": "CAND_016_002",
      "niche_name": "Rupture Dynamics of Test-Time-Training Hidden States",
      "collision_found": false,
      "collision_reason": "Results split into two disjoint clusters with NO bridging paper: pure seismology (off-fault damage source atom arxiv 1901.01771, 2503.21260, 1901.01219) and pure ML (TTT/representation-geometry: 2603.06642, 2509.23024, 2411.07279). The only neural+seismic hit (RNN for structural damage assessment under seismic loads, PMC12594378) applies ML TO earthquake engineering and does NOT transfer rupture-dynamics physics to explain TTT hidden-state adaptation. No paper occupies the fused niche of modeling TTT hidden-state adaptation as a rupture/off-fault-damage front. No collision; cross-domain prior-art density is low.",
      "reformulations": [
        {
          "n": 1,
          "query": "test-time training hidden state adaptation analogy rupture front off-fault damage high-frequency radiation",
          "prior_art_probe": false,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "Delayed dynamic triggering and enhanced high-frequency seismic radiation   due to brittle rock damage in 3D multi-fault rupture simulations", "url": "https://arxiv.org/pdf/2503.21260", "snippet": ""},
            {"title": "On the origin of thigh-frequency radiation in experimental earthquakes", "url": "https://arxiv.org/pdf/1901.01219", "snippet": ""},
            {"title": "(PDF) Dynamics, radiation and overall energy budget of earthquake rupture with coseismic off-fault damage", "url": "https://www.researchgate.net/publication/330212362_Dynamics_radiation_and_overall_energy_budget_of_earthquake_rupture_with_coseismic_off-fault_damage", "snippet": ""},
            {"title": "Dynamics, radiation and overall energy budget of earthquake rupture with   coseismic off-fault damage", "url": "https://arxiv.org/pdf/1901.01771", "snippet": ""},
            {"title": "Relationship between High-frequency Radiation and Asperity Ruptures, Revealed by Hybrid Back-projection with a Non-planar Fault Model | Scientific Reports", "url": "https://www.nature.com/articles/srep07120", "snippet": ""},
            {"title": "Test-Time Training (TTT): A New Approach to Sequence Modeling | by Keyur Ramoliya | The Deep Hub | Medium", "url": "https://medium.com/thedeephub/test-time-training-ttt-a-new-approach-to-sequence-modeling-8baf1ea79ed7", "snippet": ""}
          ]
        },
        {
          "n": 2,
          "query": "prior work mixture-of-experts routing earthquake rupture dynamics seismic wave analogy neural network",
          "prior_art_probe": true,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "Spatial Mixture-of-Experts", "url": "https://arxiv.org/pdf/2211.13491", "snippet": ""},
            {"title": "Routing by Analogy: kNN-Augmented Expert Assignment for Mixture-of-Experts", "url": "https://arxiv.org/pdf/2601.02144", "snippet": ""},
            {"title": "earthquake rupture dynamics: Topics by Science.gov", "url": "https://www.science.gov/topicpages/e/earthquake+rupture+dynamics", "snippet": ""},
            {"title": "Machine Learning Approach to Earthquake Rupture Dynamics", "url": "https://arxiv.org/pdf/1906.06250", "snippet": ""},
            {"title": "Earthquake Rupture Dynamics From Graph Neural Networks - Liu - 2025 - Journal of Geophysical Research: Solid Earth - Wiley Online Library", "url": "https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JB031981?af=R", "snippet": ""}
          ]
        },
        {
          "n": 3,
          "query": "hidden-state convergence speed input heterogeneity slow propagation seismic rupture velocity analogy attention",
          "prior_art_probe": false,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "Speed Convergence - an overview | ScienceDirect Topics", "url": "https://www.sciencedirect.com/topics/computer-science/speed-convergence", "snippet": ""},
            {"title": "Detection of Diffusion Heterogeneity in Single Particle Tracking Trajectories Using a Hidden Markov Model with Measurement Noise Propagation - PMC", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4608688/", "snippet": ""},
            {"title": "Hidden State in SpectreRF", "url": "https://designers-guide.org/analysis/hidden-state.pdf", "snippet": ""},
            {"title": "[2203.05363] Differentially Private Learning Needs Hidden State (Or Much Faster Convergence)", "url": "https://arxiv.org/abs/2203.05363", "snippet": ""},
            {"title": "Temporal Heterogeneity Improves Speed and Convergence in ...", "url": "https://www.researchgate.net/publication/359450152_Temporal_Heterogeneity_Improves_Speed_and_Convergence_in_Genetic_Algorithms", "snippet": ""},
            {"title": "Hidden-State Propagation: Mechanisms & Models", "url": "https://www.emergentmind.com/topics/hidden-state-propagation", "snippet": ""}
          ]
        },
        {
          "n": 4,
          "query": "existing research test-time training language model representational trajectory fault rupture energy radiation",
          "prior_art_probe": true,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "Tracing the Representation Geometry of Language Models from Pretraining to Post-training", "url": "https://arxiv.org/pdf/2509.23024", "snippet": ""},
            {"title": "Training-Driven Representational Geometry Modularization Predicts Brain Alignment in Language Models", "url": "https://arxiv.org/pdf/2602.07539", "snippet": ""},
            {"title": "The Surprising Effectiveness of Test-Time Training for Few-Shot Learning", "url": "https://arxiv.org/pdf/2411.07279", "snippet": ""},
            {"title": "The Energy Cost of Reasoning: Analyzing Energy Usage in LLMs with Test-time Compute", "url": "https://arxiv.org/pdf/2505.14733", "snippet": ""},
            {"title": "Reproducibility Report: Test-Time Training on Nearest Neighbors for Large Language Models", "url": "https://arxiv.org/pdf/2511.16691", "snippet": ""},
            {"title": "Local Mixtures of Experts: Essentially Free Test-Time Training via Model Merging", "url": "https://arxiv.org/pdf/2505.14136", "snippet": ""}
          ]
        },
        {
          "n": 5,
          "query": "survey neural sequence model hidden state dynamics earthquake off-fault damage high-frequency representation",
          "prior_art_probe": true,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "Convergence and stability analysis of recurrent neural networks for rapid structural damage assessment under seismic loads - PMC", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12594378/", "snippet": ""},
            {"title": "Convergence and stability analysis of recurrent neural networks for rapid structural damage assessment under seismic loads | PLOS One", "url": "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0336101", "snippet": ""},
            {"title": "Dynamics, radiation and overall energy budget of earthquake rupture with   coseismic off-fault damage", "url": "https://arxiv.org/pdf/1901.01771", "snippet": ""},
            {"title": "Delayed dynamic triggering and enhanced high-frequency seismic radiation   due to brittle rock damage in 3D multi-fault rupture simulations", "url": "https://arxiv.org/pdf/2503.21260", "snippet": ""},
            {"title": "Learning Physics for Unveiling Hidden Earthquake Ground Motions via   Conditional Generative Modeling", "url": "https://arxiv.org/pdf/2407.15089", "snippet": ""},
            {"title": "Convergence and stability analysis of recurrent neural networks for rapid structural damage assessment under seismic loads", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12594378/", "snippet": ""}
          ]
        }
      ]
    },
    {
      "cand_id": "CAND_016_003",
      "niche_name": "Damage-Regularized Orthogonal Routing for Stable MoE Load Balancing",
      "collision_found": false,
      "collision_reason": "No paper uses seismic off-fault-damage / rupture as a metaphor for MoE routing stability. ML-side hits are the SIMBAL source atom (2506.14038) plus adjacent MoE-routing/stability works (Spectral Manifold Regularization 2601.03889, bifurcation model 2605.29121, geometric-coupling 2605.12476, z-loss). Seismology-side hits are pure off-fault-damage physics (1901.01771, 2503.21260, 2406.18408). The clusters never merge; the 'damage-regularized routing manifold' framing is the candidate's own and is not occupied in literature. No collision; cross-domain prior-art density is low.",
      "reformulations": [
        {
          "n": 1,
          "query": "orthogonality auxiliary loss MoE router weights damage analogy off-fault rupture speed routing front",
          "prior_art_probe": false,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/pdf/2506.14038", "snippet": ""},
            {"title": "Advancing Expert Specialization for Better MoE", "url": "https://arxiv.org/html/2505.22323v3", "snippet": ""},
            {"title": "Router Z-Loss: Numerical Stability for MoE Training - Interactive | Michael Brenndoerfer | Michael Brenndoerfer", "url": "https://mbrenndoerfer.com/writing/router-z-loss-moe-training-stability", "snippet": ""},
            {"title": "Optimizing MoE Routers: Design, Implementation, and ...", "url": "https://arxiv.org/pdf/2506.16419", "snippet": ""},
            {"title": "Auxiliary Loss Functions for MoE Load Balancing", "url": "https://apxml.com/courses/mixture-of-experts/chapter-3-moe-training-dynamics-optimization/auxiliary-loss-load-balancing", "snippet": ""},
            {"title": "Mixture-of-Experts (MoE): The Birth and Rise of Conditional Computation", "url": "https://cameronrwolfe.substack.com/p/conditional-computation-the-birth", "snippet": ""}
          ]
        },
        {
          "n": 2,
          "query": "prior work mixture-of-experts load balancing routing instability damped seismic off-fault damage rupture metaphor",
          "prior_art_probe": true,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "[2408.15664] Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts", "url": "https://arxiv.org/abs/2408.15664", "snippet": ""},
            {"title": "Mixture-of-Experts with Expert Choice Routing", "url": "https://arxiv.org/pdf/2202.09368", "snippet": ""},
            {"title": "A Minimal Bifurcation Model of Load Imbalance in a Softmax Mixture-of-Experts Router", "url": "https://arxiv.org/html/2605.29121", "snippet": ""},
            {"title": "Latent Prototype Routing: Achieving Near-Perfect Load Balancing in Mixture-of-Experts", "url": "https://arxiv.org/pdf/2506.21328", "snippet": ""},
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/pdf/2506.14038", "snippet": ""},
            {"title": "Least-Loaded Expert Parallelism: Load Balancing An Imbalanced Mixture-of-Experts", "url": "https://arxiv.org/pdf/2601.17111", "snippet": ""},
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/html/2506.14038v1", "snippet": ""}
          ]
        },
        {
          "n": 3,
          "query": "existing damage-regularized routing manifold MoE high-frequency instability damp fault damage rupture velocity reduction",
          "prior_art_probe": true,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "Spectral Manifold Regularization for Stable and Modular Routing in Deep MoE Architectures", "url": "https://arxiv.org/pdf/2601.03889", "snippet": ""},
            {"title": "[2601.03889] Spectral Manifold Regularization for Stable and Modular Routing in Deep MoE Architectures", "url": "https://arxiv.org/abs/2601.03889", "snippet": ""},
            {"title": "Spectral Manifold Regularization for Stable and Modular Routing in Deep MoE Architectures", "url": "https://arxiv.org/html/2601.03889", "snippet": ""},
            {"title": "Routing Manifold Alignment Improves Generalization of Mixture-of-Experts LLMs", "url": "https://arxiv.org/pdf/2511.07419", "snippet": ""},
            {"title": "Routing Manifold Alignment Improves Generalization of Mixture-of-Experts LLMs", "url": "https://arxiv.org/html/2511.07419v2", "snippet": ""}
          ]
        },
        {
          "n": 4,
          "query": "survey orthogonal regularization expert routing convergence speed control earthquake off-fault damage seismic radiation",
          "prior_art_probe": true,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "Dynamics, radiation and overall energy budget of earthquake rupture with   coseismic off-fault damage", "url": "https://arxiv.org/pdf/1901.01771", "snippet": ""},
            {"title": "Delayed dynamic triggering and enhanced high-frequency seismic radiation   due to brittle rock damage in 3D multi-fault rupture simulations", "url": "https://arxiv.org/pdf/2503.21260", "snippet": ""},
            {"title": "On the origin of thigh-frequency radiation in experimental earthquakes", "url": "https://arxiv.org/pdf/1901.01219", "snippet": ""},
            {"title": "Off-fault damage controls near-surface rupture behaviour in soft sediments", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12722718/", "snippet": ""},
            {"title": "Depth Dependence of Coseismic Off-Fault Damage and its Effects on   Rupture Dynamics", "url": "https://arxiv.org/pdf/2406.18408", "snippet": ""},
            {"title": "Convergence and stability analysis of recurrent neural ...", "url": "https://journals.plos.org/plosone/article/file?type=printable&id=10.1371/journal.pone.0336101", "snippet": ""},
            {"title": "Signature of transition to supershear rupture speed in the coseismic off-fault damage zone", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8595990/", "snippet": ""},
            {"title": "Convergence and stability analysis of recurrent neural networks for rapid structural damage assessment under seismic loads | PLOS One", "url": "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0336101", "snippet": ""}
          ]
        },
        {
          "n": 5,
          "query": "router weights orthogonality slow over-fast convergence token routing rupture front seismic fault damage analogy mixture-of-experts",
          "prior_art_probe": false,
          "cross_domain": true,
          "allowed_domains": null,
          "results": [
            {"title": "Routers Learn the Geometry of Their Experts: Geometric Coupling in Sparse Mixture-of-Experts", "url": "https://arxiv.org/html/2605.12476", "snippet": ""},
            {"title": "Router Upcycling: Leveraging Mixture-of-Routers in Mixture-of-Experts Upcycling", "url": "https://arxiv.org/html/2509.00679", "snippet": ""},
            {"title": "Published as a conference paper at ICLR 2025", "url": "https://arxiv.org/pdf/2502.15315", "snippet": ""},
            {"title": "[2605.12476] Routers Learn the Geometry of Their Experts: Geometric Coupling in Sparse Mixture-of-Experts", "url": "https://arxiv.org/abs/2605.12476", "snippet": ""},
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/pdf/2506.14038", "snippet": ""},
            {"title": "Grouter: Decoupling Routing from Representation for Accelerated MoE Training", "url": "https://arxiv.org/pdf/2603.06626", "snippet": ""}
          ]
        }
      ]
    }
  ]
}
```

## [REPORT 4] crosscheck.json (verbatim)
```json
{
  "run_id": "run_016",
  "epoch": 3,
  "agent": "4_crosschecker",
  "crosschecked_at": "2026-06-01T02:41:37Z",
  "verbatim_note": "All titles/urls from AGENT 4's OWN real WebSearch; independent; no fabrication.",
  "candidates": [
    {
      "cand_id": "CAND_016_001",
      "agent3_collision_found": false,
      "agent4_collision": false,
      "mismatch_with_agent3": false,
      "notes": "Two fresh searches with different wording than A3. All paper-like hits are the SIMBAL source atom (arxiv 2506.14038, 'Load Balancing Mixture of Experts with Similarity Preserving Routers') plus adjacent MoE-routing works (Self-Routing 2604.00421, Cosine-Similarity/Semantic-Anchor Routing 2509.14255, Rewiring Experts on the Fly 2510.14853, TARo token-level test-time alignment 2603.18411, Routing by Analogy 2601.02144, Layerwise Recurrent Router 2408.06793, Coupling Experts and Routers 2512.23447). None describe the FUSED niche of similarity-preserving orthogonal routing governing which fast-weight expert undergoes self-supervised test-time training per token. Search 2 explicitly notes SimBal results 'don't contain specific information about test-time training or expert hidden state learner.' No same-core-niche collision. Confirms A3.",
      "recheck_searches": [
        {
          "n": 1,
          "query": "relational similarity router orthogonality gating self-supervised fast weight expert per-token test-time adaptation",
          "allowed_domains": null,
          "results": [
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/pdf/2506.14038", "snippet": ""},
            {"title": "Layerwise Recurrent Router for Mixture-of-Experts", "url": "https://arxiv.org/html/2408.06793v1", "snippet": ""},
            {"title": "Rewiring Experts on the Fly:Continuous Rerouting for Better Online Adaptation in Mixture-of-Expert models", "url": "https://arxiv.org/pdf/2510.14853", "snippet": ""},
            {"title": "TARo: Token-level Adaptive Routing for LLM Test-time Alignment", "url": "https://arxiv.org/pdf/2603.18411", "snippet": ""},
            {"title": "Cosine-Similarity Routing with Semantic Anchors for Interpretable Mixture-of-Experts Language Models", "url": "https://arxiv.org/html/2509.14255", "snippet": ""},
            {"title": "Self-Routing: Parameter-Free Expert Routing from Hidden States", "url": "https://arxiv.org/pdf/2604.00421", "snippet": ""},
            {"title": "Routing by Analogy: kNN-Augmented Expert Assignment for Mixture-of-Experts", "url": "https://arxiv.org/pdf/2601.02144", "snippet": ""}
          ]
        },
        {
          "n": 2,
          "query": "SimBal similarity preserving router auxiliary loss combined with test-time training MoE expert hidden state learner",
          "allowed_domains": null,
          "results": [
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/html/2506.14038v1", "snippet": ""},
            {"title": "000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019", "url": "https://openreview.net/pdf?id=FNuvMnGAm8", "snippet": ""},
            {"title": "(PDF) Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://www.researchgate.net/publication/392766915_Load_Balancing_Mixture_of_Experts_with_Similarity_Preserving_Routers", "snippet": ""},
            {"title": "[2506.14038] Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/abs/2506.14038", "snippet": ""},
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/pdf/2506.14038", "snippet": ""},
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers | OpenReview", "url": "https://openreview.net/forum?id=FNuvMnGAm8", "snippet": ""},
            {"title": "Advancing Expert Specialization for Better MoE", "url": "https://arxiv.org/html/2505.22323v3", "snippet": ""},
            {"title": "Coupling Experts and Routers in Mixture-of-Experts via an Auxiliary Loss", "url": "https://arxiv.org/html/2512.23447v1", "snippet": ""}
          ]
        }
      ]
    },
    {
      "cand_id": "CAND_016_002",
      "agent3_collision_found": false,
      "agent4_collision": false,
      "mismatch_with_agent3": false,
      "notes": "BRIDGING TEST (ML term + seismology term in each query). NO bridging paper found. Results split into two disjoint clusters: (1) seismology that APPLIES ML to earthquakes (Graph Neural Networks for rupture dynamics 1906.06250 / 2025JB031981, ANN/RF rupture-arrest prediction, off-fault-damage physics 1901.01771, FDEM off-fault modeling 1911.03468) -- these use ML as a tool for seismology, they do NOT transfer rupture/off-fault-damage physics into TTT/LLM hidden-state adaptation; (2) transformers applied TO seismic data (EQTransformer phase picking PMC7415159, seismic ground-response 14/15/6658, P-wave detection TransQuake, SeisBind 2601.14607). Search 2 explicitly states results 'don't appear to address the specific concept of using physics-inspired metaphors from fault dynamics and rupture propagation to explain transformer representational trajectories.' No paper occupies the fused niche of modeling TTT hidden-state adaptation as a rupture/off-fault-damage front. No bridging collision. Confirms A3.",
      "recheck_searches": [
        {
          "n": 1,
          "query": "earthquake rupture dynamics off-fault damage analogy neural network hidden state test-time training adaptation front high-frequency",
          "allowed_domains": null,
          "results": [
            {"title": "Machine Learning Approach to Earthquake Rupture Dynamics - NASA/ADS", "url": "https://ui.adsabs.harvard.edu/abs/2019arXiv190606250A/abstract", "snippet": ""},
            {"title": "Machine Learning Approach to Earthquake Rupture Dynamics", "url": "https://arxiv.org/pdf/1906.06250", "snippet": ""},
            {"title": "Earthquake rupture dynamics from Graph Neural Networks | Statewide California Earthquake Center", "url": "https://central.scec.org/publication/14197", "snippet": ""},
            {"title": "Dynamics, radiation and overall energy budget of earthquake rupture with   coseismic off-fault damage", "url": "https://arxiv.org/pdf/1901.01771", "snippet": ""},
            {"title": "Earthquake rupture dynamics from Graph Neural Networks", "url": "https://d197for5662m48.cloudfront.net/documents/publicationstatus/280083/preprint_pdf/e26820eb944818bf2375f0aabdf876b4.pdf", "snippet": ""},
            {"title": "(PDF) Machine Learning Approach to Earthquake Rupture Dynamics", "url": "https://www.researchgate.net/publication/333815383_Machine_Learning_Approach_to_Earthquake_Rupture_Dynamics", "snippet": ""},
            {"title": "Modeling earthquakes with off-fault damage using the combined   finite-discrete element method", "url": "https://arxiv.org/pdf/1911.03468", "snippet": ""},
            {"title": "Earthquake Rupture Dynamics From Graph Neural Networks - Liu - 2025 - Journal of Geophysical Research: Solid Earth - Wiley Online Library", "url": "https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JB031981?af=R", "snippet": ""},
            {"title": "SE - Characteristics of earthquake ruptures and dynamic off-fault deformation on propagating faults", "url": "https://se.copernicus.org/articles/11/1333/2020/", "snippet": ""}
          ]
        },
        {
          "n": 2,
          "query": "transformer sequence model representational trajectory modeled as seismic rupture propagation fault damage radiation physics-inspired",
          "allowed_domains": null,
          "results": [
            {"title": "Sequence Deep Learning for Seismic Ground Response Modeling: 1D-CNN, LSTM, and Transformer Approach", "url": "https://www.mdpi.com/2076-3417/14/15/6658", "snippet": ""},
            {"title": "SeisBind: Physics-Aware Tri-Modal Representation Binding for Seismic Data via Contrastive Learning", "url": "https://arxiv.org/pdf/2601.14607", "snippet": ""},
            {"title": "Enforcing Reciprocity in Operator Learning for Seismic Wave Propagation", "url": "https://arxiv.org/pdf/2602.11631", "snippet": ""},
            {"title": "Earthquake transformer—an attentive deep-learning model for simultaneous earthquake detection and phase picking - PMC", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7415159/", "snippet": ""},
            {"title": "Full seismic waveform analysis combined with transformer neural networks improves coseismic landslide prediction | Communications Earth & Environment", "url": "https://www.nature.com/articles/s43247-024-01243-8", "snippet": ""},
            {"title": "TransQuake: A transformer-based deep learning approach for seismic P-wave detection - ScienceDirect", "url": "https://www.sciencedirect.com/science/article/pii/S277246702100004X", "snippet": ""}
          ]
        }
      ]
    },
    {
      "cand_id": "CAND_016_003",
      "agent3_collision_found": false,
      "agent4_collision": false,
      "mismatch_with_agent3": false,
      "notes": "BRIDGING TEST (ML term + seismology term in each query). NO bridging paper found. ML-side hits are the SIMBAL source atom (2506.14038) plus adjacent MoE load-balancing/stability works (Latent Prototype Routing 2506.21328, EMoE Eigenbasis-Guided Routing 2601.12137, router z-loss instability material). Seismology-side hits are pure earthquake physics / ML-applied-to-seismology (fault-rupture ML review S0065268720300066, rupture propagation-and-arrest prediction GJI 224/3/1918, remote-triggering 2106.11616, earthquake resonance 1502.05485, free-oscillations 1010.5690) plus unrelated mechanical/Rayleigh damping. The clusters never merge. Search 1 explicitly states 'none of the sources directly connect seismic rupture velocity concepts or off-fault damage mechanics to mixture-of-experts routing algorithms' and that the seismic-metaphor MoE concept 'may not yet have a published research paper.' No paper uses off-fault-damage/rupture as a metaphor for MoE routing stability. No bridging collision. Confirms A3.",
      "recheck_searches": [
        {
          "n": 1,
          "query": "mixture-of-experts router load balancing stability inspired by off-fault damage rupture velocity seismic metaphor orthogonality regularization",
          "allowed_domains": null,
          "results": [
            {"title": "(PDF) Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://www.researchgate.net/publication/392766915_Load_Balancing_Mixture_of_Experts_with_Similarity_Preserving_Routers", "snippet": ""},
            {"title": "LOAD BALANCING MIXTURE OF EXPERTS WITH SIMI", "url": "https://openreview.net/pdf?id=FNuvMnGAm8", "snippet": ""},
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/html/2506.14038v1", "snippet": ""},
            {"title": "Mixture-of-Experts (MoE) LLMs - by Cameron R. Wolfe, Ph.D.", "url": "https://cameronrwolfe.substack.com/p/moe-llms", "snippet": ""},
            {"title": "Techniques for Mitigating Router Z-Loss Instability", "url": "https://apxml.com/courses/mixture-of-experts-advanced-implementation/chapter-3-training-large-scale-moes/mitigating-router-z-loss-instability", "snippet": ""},
            {"title": "Cameron R. Wolfe, Ph.D. on X: \"Mixture-of-Experts (MoE) LLMs are more prone to training instability than standard LLMs...\" / X", "url": "https://x.com/cwolferesearch/status/1901640632030151089", "snippet": ""},
            {"title": "Load Balancing Mixture of Experts with Similarity Preserving Routers", "url": "https://arxiv.org/pdf/2506.14038", "snippet": ""},
            {"title": "Latent Prototype Routing: Achieving Near-Perfect Load Balancing in Mixture-of-Experts", "url": "https://arxiv.org/pdf/2506.21328", "snippet": ""},
            {"title": "EMoE: Eigenbasis-Guided Routing for Mixture-of-Experts", "url": "https://arxiv.org/pdf/2601.12137", "snippet": ""},
            {"title": "Machine learning and fault rupture: A review - ScienceDirect", "url": "https://www.sciencedirect.com/science/article/abs/pii/S0065268720300066", "snippet": ""},
            {"title": "Application of machine learning techniques to predict rupture propagation and arrest in 2-D dynamic earthquake simulations | Geophysical Journal International | Oxford Academic", "url": "https://academic.oup.com/gji/article/224/3/1918/5989698", "snippet": ""}
          ]
        },
        {
          "n": 2,
          "query": "MoE routing instability damping high-frequency oscillation analogy earthquake fault damage controlled perturbation expert load",
          "allowed_domains": null,
          "results": [
            {"title": "(PDF) The high-frequency oscillation in systems with Rayleigh damping model", "url": "https://www.researchgate.net/publication/335950537_The_high-frequency_oscillation_in_systems_with_Rayleigh_damping_model", "snippet": ""},
            {"title": "Damping arrangement for an oscillatably mounted electrical energy transmission device", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9893506", "snippet": ""},
            {"title": "Damped oscillations Select LEARNING OBJECTIVES:", "url": "https://boxsand.physics.oregonstate.edu/sites/boxsand.physics.oregonstate.edu/files/Media-2/cascades/ph212_f17/lecture/oscillations/Damped%20oscillations.pdf", "snippet": ""},
            {"title": "Generic Mechanism for Remote Triggering of Earthquakes", "url": "https://arxiv.org/pdf/2106.11616", "snippet": ""},
            {"title": "Response of a Magneto-Rheological Fluid Damper Subjected to Periodic   Forcing in a High Frequency Limit", "url": "https://arxiv.org/pdf/nlin/0610055", "snippet": ""},
            {"title": "Free-Oscillations Coincident with Earthquakes", "url": "https://arxiv.org/pdf/1010.5690", "snippet": ""},
            {"title": "Oscillation dampening system for a railway track", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4203546", "snippet": ""},
            {"title": "A possible resonance mechanism of earthquakes", "url": "https://arxiv.org/pdf/1502.05485", "snippet": ""}
          ]
        }
      ]
    }
  ]
}
```

## [REPORT 5] search_quality.json (verbatim)
```json
{
  "run_id": "run_016",
  "epoch": 3,
  "scored_at": "2026-06-01T02:44:36.733497+00:00",
  "params_used": {
    "reformulation_specificity": 0.5698,
    "mechanism_focus": 0.594,
    "cross_domain_reach": 0.5059,
    "atom_source_diversity": 0.5,
    "collision_avoidance_phrasing": 0.5147
  },
  "n_queries": 26,
  "per_query": [
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "mixture-of-experts gating router load balancing auxiliary loss expert specialization arxiv 2025",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "state space model selective scan Mamba linear recurrence input-dependent gating arxiv 2025",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "graph neural network message passing earthquake seismic wave phase picking arrival time arxiv 2025",
      "dims": {
        "specificity": 0.75,
        "mechanism_focus": 0.0,
        "cross_domain_reach": 1.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "attention transformer mechanism seismic fault rupture nucleation slip propagation arxiv 2025",
      "dims": {
        "specificity": 0.75,
        "mechanism_focus": 1.0,
        "cross_domain_reach": 1.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "dynamic rupture simulation off-fault damage high-frequency radiation brittle rock 3D multi-fault arxiv 2503.21260",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.0,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "earthquake nucleation rate-and-state friction slow slip aseismic creep stress transfer mechanism seismology 2025",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 0.5,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "\"continuum damage breakage model\" \"off-fault\" rupture \"high-frequency\" radiation \"reduces rupture speed\" abstract",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.0,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "\"Load Balancing Mixture of Experts with Similarity Preserving Routers\" abstract \"load balancing loss\" preserves relational structure",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "\"Advancing Expert Specialization\" MoE orthogonality variance loss \"process distinct\" tokens discriminative routing abstract arxiv 2505.22323",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "test-time training neural network adapt hidden state self-supervised loss sequence modeling RNN expressive arxiv 2025 mechanism",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent1_sourcer",
      "cand_id": null,
      "query": "\"RNNs with Expressive Hidden States\" abstract \"hidden state\" \"self-supervised\" \"update rule\" \"Test-Time Training\" TTT layers",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.0,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_001",
      "query": "similarity-preserving routing orthogonal router weights test-time training mixture-of-experts",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_001",
      "query": "prior work load balancing auxiliary loss orthogonality router weights mixture-of-experts test-time training",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.0,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_001",
      "query": "fast-weight experts hidden state self-supervised test-time training routing token similarity",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_001",
      "query": "existing survey expert selection routing test-time training learner per-token hidden state MoE",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_001",
      "query": "orthogonality router regularization stability generalization test-time training experts already been studied",
      "dims": {
        "specificity": 0.75,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_002",
      "query": "test-time training hidden state adaptation analogy rupture front off-fault damage high-frequency radiation",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.0,
        "cross_domain_reach": 0.5,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_002",
      "query": "prior work mixture-of-experts routing earthquake rupture dynamics seismic wave analogy neural network",
      "dims": {
        "specificity": 0.75,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 0.5,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_002",
      "query": "hidden-state convergence speed input heterogeneity slow propagation seismic rupture velocity analogy attention",
      "dims": {
        "specificity": 0.75,
        "mechanism_focus": 1.0,
        "cross_domain_reach": 0.5,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_002",
      "query": "existing research test-time training language model representational trajectory fault rupture energy radiation",
      "dims": {
        "specificity": 0.75,
        "mechanism_focus": 0.0,
        "cross_domain_reach": 1.0,
        "collision_avoidance": 0.5
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_002",
      "query": "survey neural sequence model hidden state dynamics earthquake off-fault damage high-frequency representation",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.0,
        "cross_domain_reach": 0.0,
        "collision_avoidance": 0.5
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_003",
      "query": "orthogonality auxiliary loss MoE router weights damage analogy off-fault rupture speed routing front",
      "dims": {
        "specificity": 0.75,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 0.5,
        "collision_avoidance": 0.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_003",
      "query": "prior work mixture-of-experts load balancing routing instability damped seismic off-fault damage rupture metaphor",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 0.5,
        "collision_avoidance": 1.0
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_003",
      "query": "existing damage-regularized routing manifold MoE high-frequency instability damp fault damage rupture velocity reduction",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 0.5,
        "cross_domain_reach": 1.0,
        "collision_avoidance": 0.5
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_003",
      "query": "survey orthogonal regularization expert routing convergence speed control earthquake off-fault damage seismic radiation",
      "dims": {
        "specificity": 0.75,
        "mechanism_focus": 1.0,
        "cross_domain_reach": 0.5,
        "collision_avoidance": 0.5
      }
    },
    {
      "source": "agent3_verifier",
      "cand_id": "CAND_016_003",
      "query": "router weights orthogonality slow over-fast convergence token routing rupture front seismic fault damage analogy mixture-of-experts",
      "dims": {
        "specificity": 1.0,
        "mechanism_focus": 1.0,
        "cross_domain_reach": 0.5,
        "collision_avoidance": 0.0
      }
    }
  ],
  "dimension_means": {
    "reformulation_specificity": 0.9231,
    "mechanism_focus": 0.5,
    "cross_domain_reach": 0.3077,
    "atom_source_diversity": 1.0,
    "collision_avoidance_phrasing": 0.2692
  },
  "avg_search_quality": 0.6024,
  "note": "avg_search_quality = sum(param_k * dimension_mean_k)/sum(param_k); dimension scores are deterministic text heuristics over the real queries AGENT 1 and AGENT 3 used this epoch."
}
```

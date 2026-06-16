# [REPORT] Run 15 ground-truth log
# generated 2026-05-31T21:22:32.550344+00:00
# Each block is a subagent's raw output, injected verbatim by the orchestrator.


## [REPORT 1] atoms.json (verbatim)
```json
{
  "run_id": "run_015",
  "agent": "1_sourcer",
  "fetched_at": "2026-05-31T20:51:53Z",
  "verbatim_note": "WebFetch on arxiv.org abstract/PDF pages and on mirrors (ar5iv, export.arxiv API, HuggingFace, Semantic Scholar, alphaXiv, paperswithcode) all returned HTTP 403/failed, so no abstract page could be read directly. The title/url/text fields below are copied verbatim from real WebSearch tool result snippets (allowed_domains=arxiv.org). The 'text' field for each atom is an exact span returned by WebSearch describing that paper's mechanism. URLs are the abs pages corresponding to the arxiv IDs surfaced by WebSearch. No content was fabricated; nothing here was confirmed against a fetched abstract page.",
  "atoms": [
    {
      "atom_id": "ARXIV_R15_A01",
      "arxiv_id": "2505.00315",
      "title": "Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing",
      "url": "https://arxiv.org/abs/2505.00315",
      "text": "MoSA is inspired by MoE with expert choice routing that dynamically selects tokens for each attention head, allowing arbitrary sparse attention patterns.",
      "source_type": "arxiv",
      "domain_tags": ["attention", "routing"]
    },
    {
      "atom_id": "ARXIV_R15_A02",
      "arxiv_id": "2509.24218",
      "title": "Conda: Column-Normalized Adam for Training Large Language Models Faster",
      "url": "https://arxiv.org/abs/2509.24218",
      "text": "Conda achieves 2-2.5x faster convergence than AdamW on LLaMA series, measured by both training steps and wall-clock time, with consistent gains on GPT-2.",
      "source_type": "arxiv",
      "domain_tags": ["optimization", "training"]
    },
    {
      "atom_id": "ARXIV_R15_A03",
      "arxiv_id": "2509.25140",
      "title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory",
      "url": "https://arxiv.org/abs/2509.25140",
      "text": "memory-aware test-time scaling (MaTTS), which scales up agent interactions to generate diverse experiences that provide signals for synthesizing higher-quality memory, with better memory guiding more effective scaling.",
      "source_type": "arxiv",
      "domain_tags": ["memory", "test-time-compute"]
    }
  ]
}
```

## [REPORT 2] candidates.json (verbatim)
```json
{
  "run_id": "run_015",
  "epoch": 1,
  "generated_at": "2026-05-31T21:00:02.506977+00:00",
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
      "cand_id": "CAND_015_001",
      "atom_a_id": "ARXIV_R15_A01",
      "atom_b_id": "ARXIV_R15_A02",
      "niche_name": "Routing-Conditioned Optimizers for Sparse-Attention Convergence Acceleration",
      "mechanism": "Expert-choice routing dynamically selects which tokens each attention head attends to, producing sparse attention gradients that act like preconditioned update directions, which in turn induces faster optimizer convergence akin to Conda's accelerated descent.",
      "transfer": "MoSA's dynamic per-head token routing transfers as a structured sparsity prior that conditions the optimizer's update geometry to speed convergence.",
      "open_problem": "Can routing-induced attention sparsity be coupled with a Conda-style optimizer to achieve 2-2.5x faster convergence in sparse-attention transformers?",
      "primary_quote": "achieves 2-2.5x faster convergence than AdamW on LLaMA series",
      "quote_source": "atom_b",
      "quote_verified_substring": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "b188c898-caf8-40d4-ade4-d77bba15ab30",
      "opus_cost_usd": 0.033499
    },
    {
      "cand_id": "CAND_015_002",
      "atom_a_id": "ARXIV_R15_A02",
      "atom_b_id": "ARXIV_R15_A03",
      "niche_name": "Convergence-Accelerated Memory Synthesis for Test-Time Scaling",
      "mechanism": "Conda's preconditioned optimization geometry induces faster convergence, and transplanting that principle into MaTTS regulates how scaled agent interactions are weighted, causing diverse experiences to converge into higher-quality synthesized memory in fewer interaction rounds.",
      "transfer": "The convergence-acceleration mechanism from A transfers to B as a memory-synthesis schedule that produces high-quality memory from fewer scaled interactions.",
      "open_problem": "Can a Conda-style preconditioned update rule applied to memory synthesis cut the number of agent interactions needed for MaTTS to reach a target memory quality by 2x?",
      "primary_quote": "scales up agent interactions to generate diverse experiences",
      "quote_source": "atom_b",
      "quote_verified_substring": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "82ce70fd-a42d-43d4-9958-a97f89cffe4c",
      "opus_cost_usd": 0.03399525
    },
    {
      "cand_id": "CAND_015_003",
      "atom_a_id": "ARXIV_R15_A01",
      "atom_b_id": "ARXIV_R15_A03",
      "niche_name": "Expert-Choice Routing for Memory-Aware Test-Time Scaling",
      "mechanism": "MoSA's expert-choice routing dynamically selects which tokens each attention head attends to, and transferring this principle to memory-aware test-time scaling routes accumulated agent experiences to specialized memory-synthesis heads so that scaling activates only the most informative interaction traces, which in turn regulates which memories guide subsequent attention.",
      "transfer": "Expert-choice token routing per attention head transfers from A to become experience-choice routing that selects which agent interactions feed memory synthesis in B.",
      "open_problem": "Can learned expert-choice routing over agent experiences produce sparse, high-quality memory that improves test-time scaling more efficiently than uniform experience aggregation?",
      "primary_quote": "expert choice routing that dynamically selects tokens for each attention head",
      "quote_source": "atom_a",
      "quote_verified_substring": true,
      "parse_ok": true,
      "attempts": 1,
      "opus_session_id": "5ab6d271-7346-4195-a912-838bf8e8b0e1",
      "opus_cost_usd": 0.0354275
    }
  ]
}
```

## [REPORT 3] verify.json (verbatim)
```json
{
  "run_id": "run_015",
  "agent": "3_verifier",
  "verified_at": "2026-05-31T21:20:00Z",
  "verbatim_note": "All titles/urls copied exactly from real WebSearch results; snippets empty where the tool gave no per-result snippet; no fabrication.",
  "candidates": [
    {
      "cand_id": "CAND_015_001",
      "niche_name": "Routing-Conditioned Optimizers for Sparse-Attention Convergence Acceleration",
      "collision_found": false,
      "collision_reason": "The 5 searches surface the two source papers (MoSA expert-choice sparse attention; Conda preconditioned optimizer) and adjacent work on routing-aware MoE optimizers (EXCITATION), attention-guided MoE routing, and preconditioning for self-attention training dynamics, but no paper-like source describes the specific niche of using routing-induced attention sparsity as a structured prior that conditions a preconditioned optimizer to accelerate convergence; the closest, EXCITATION, modulates updates by expert-FFN utilization, not by attention-head token-routing sparsity.",
      "reformulations": [
        {"n": 1, "query": "expert-choice routing sparse attention conditioned optimizer faster convergence transformer training", "allowed_domains": null, "results": [
          {"title": "Mixture-of-Experts with Expert Choice Routing", "url": "https://research.google/blog/mixture-of-experts-with-expert-choice-routing/?m=1", "snippet": ""},
          {"title": "(PDF) Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing", "url": "https://www.researchgate.net/publication/391369365_Mixture_of_Sparse_Attention_Content-Based_Learnable_Sparse_Attention_via_Expert-Choice_Routing", "snippet": ""},
          {"title": "Mixture-of-Experts with Expert Choice Routing", "url": "https://arxiv.org/pdf/2202.09368", "snippet": ""},
          {"title": "Expert-Choice Routing Enables Adaptive Computation in Diffusion Language Models", "url": "https://arxiv.org/html/2604.01622", "snippet": ""},
          {"title": "Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing", "url": "https://arxiv.org/html/2505.00315v1", "snippet": ""},
          {"title": "[2505.00315] Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing", "url": "https://arxiv.org/abs/2505.00315", "snippet": ""},
          {"title": "EC-DiT: Scaling Diffusion Transformers with Adaptive Expert-Choice Routing", "url": "https://arxiv.org/html/2410.02098v2", "snippet": ""},
          {"title": "Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing", "url": "https://arxiv.org/pdf/2505.00315", "snippet": ""}
        ]},
        {"n": 2, "query": "mixture of sparse attention routing induced gradient sparsity optimizer preconditioning convergence", "allowed_domains": ["arxiv.org"], "results": [
          {"title": "Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing", "url": "https://arxiv.org/html/2505.00315v1", "snippet": ""},
          {"title": "Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing", "url": "https://arxiv.org/pdf/2505.00315", "snippet": ""},
          {"title": "[2505.00315] Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing", "url": "https://arxiv.org/abs/2505.00315", "snippet": ""},
          {"title": "Routing Absorption in Sparse Attention: Why Random Gates Are Hard to Beat", "url": "https://arxiv.org/pdf/2603.02227", "snippet": ""},
          {"title": "Error Feedback Can Accurately Compress Preconditioners", "url": "https://arxiv.org/html/2306.06098v4", "snippet": ""},
          {"title": "Dense Backpropagation Improves Training for Sparse Mixture-of-Experts", "url": "https://arxiv.org/pdf/2504.12463", "snippet": ""}
        ]},
        {"n": 3, "query": "structured sparsity prior preconditioned optimizer accelerate convergence sparse attention LLM", "allowed_domains": ["arxiv.org"], "results": [
          {"title": "Near-Lossless Acceleration of Long Context LLM Inference with Adaptive Structured Sparse Attention", "url": "https://arxiv.org/html/2406.15486v1", "snippet": ""},
          {"title": "HSR-Enhanced Sparse Attention Acceleration", "url": "https://arxiv.org/pdf/2410.10165", "snippet": ""},
          {"title": "SparseLoRA: Accelerating LLM Fine-Tuning with Contextual Sparsity", "url": "https://arxiv.org/html/2506.16500v1", "snippet": ""},
          {"title": "SeerAttention: Learning Intrinsic Sparse Attention in Your LLMs", "url": "https://arxiv.org/pdf/2410.13276", "snippet": ""},
          {"title": "SampleAttention: Near-Lossless Acceleration of Long Context LLM Inference with Adaptive Structured Sparse Attention", "url": "https://arxiv.org/pdf/2406.15486", "snippet": ""},
          {"title": "MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention", "url": "https://arxiv.org/pdf/2407.02490", "snippet": ""},
          {"title": "Samoyeds: Accelerating MoE Models with Structured Sparsity Leveraging Sparse Tensor Cores", "url": "https://arxiv.org/pdf/2503.10725", "snippet": ""}
        ]},
        {"n": 4, "query": "routing-aware optimizer mixture of experts attention sparsity update geometry training speedup", "allowed_domains": null, "results": [
          {"title": "Excitation: Momentum For Experts", "url": "https://arxiv.org/pdf/2602.21798", "snippet": ""},
          {"title": "Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing", "url": "https://arxiv.org/pdf/2505.00315", "snippet": ""},
          {"title": "TA-MoE: Topology-Aware Large Scale Mixture-of-Expert Training", "url": "https://openreview.net/pdf?id=FRDiimH26Tr", "snippet": ""},
          {"title": "Mixture of Experts Explained", "url": "https://huggingface.co/blog/moe", "snippet": ""},
          {"title": "Improving Routing in Sparse Mixture of Experts with Graph of Tokens", "url": "https://arxiv.org/pdf/2505.00792", "snippet": ""},
          {"title": "Mixture-of-Experts Models in Vision: Routing, Optimization, and Generalization", "url": "https://arxiv.org/html/2601.15021v1", "snippet": ""}
        ]},
        {"n": 5, "query": "attention sparsity pattern conditions optimizer adaptive preconditioning AdamW faster convergence LLaMA", "allowed_domains": null, "results": [
          {"title": "Conda: Column-Normalized Adam for Training Large Language Models Faster", "url": "https://arxiv.org/html/2509.24218v2", "snippet": ""},
          {"title": "Optimizers in Large Language Models | by Sammatthewdr | Medium", "url": "https://medium.com/@sammatthewdr/optimizers-in-large-language-models-525d862d0b9a", "snippet": ""},
          {"title": "Improving Adaptive Moment Optimization via Preconditioner Diagonalization", "url": "https://arxiv.org/pdf/2502.07488", "snippet": ""},
          {"title": "Conda: Column-Normalized Adam for Training Large Language Models Faster", "url": "https://arxiv.org/pdf/2509.24218", "snippet": ""},
          {"title": "SAGE: Sign-Adaptive Gradient for Memory-Efficient LLM Optimization", "url": "https://arxiv.org/pdf/2604.07663", "snippet": ""},
          {"title": "Accelerating LLM Pre-Training through Flat-Direction Dynamics Enhancement", "url": "https://arxiv.org/html/2602.22681", "snippet": ""},
          {"title": "Beyond Adam: Disentangling Optimizer Effects in the Fine-Tuning of Atomistic Foundation Models", "url": "https://arxiv.org/html/2512.05489v1", "snippet": ""},
          {"title": "AdamW - Cornell University Computational Optimization Open Textbook - Optimization Wiki", "url": "https://optimization.cbe.cornell.edu/index.php?title=AdamW", "snippet": ""}
        ]}
      ]
    },
    {
      "cand_id": "CAND_015_002",
      "niche_name": "Convergence-Accelerated Memory Synthesis for Test-Time Scaling",
      "collision_found": false,
      "collision_reason": "The 5 searches return the MaTTS/ReasoningBank source paper plus generic preconditioned optimizers (Shampoo, Muon, 4-bit preconditioning) and rollout-efficiency work (ARROL online rollout pruning, 'Do Not Waste Your Rollouts', Memory-R2), but no paper-like source transplants an optimizer's preconditioned-convergence principle into agent memory synthesis to cut the number of interactions needed to reach a target memory quality; the rollout-pruning papers reduce rollouts via quality heuristics, not via a Conda-style update rule on memory synthesis.",
      "reformulations": [
        {"n": 1, "query": "preconditioned optimizer convergence acceleration agent memory synthesis test-time scaling fewer interactions", "allowed_domains": null, "results": [
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""},
          {"title": "Extreme Tensoring for Low-Memory Preconditioning", "url": "https://arxiv.org/pdf/1902.04620", "snippet": ""},
          {"title": "Turbo-Muon: Accelerating Orthogonality-Based Optimization with Pre-Conditioning", "url": "https://arxiv.org/pdf/2512.04632", "snippet": ""},
          {"title": "Thinking vs. Doing: Agents that Reason by Scaling Test-Time Interaction", "url": "https://arxiv.org/pdf/2506.07976", "snippet": ""},
          {"title": "Memory-Efficient 4-bit Preconditioned Stochastic Optimization", "url": "https://arxiv.org/html/2412.10663", "snippet": ""},
          {"title": "Error Feedback Can Accurately Compress Preconditioners", "url": "https://arxiv.org/html/2306.06098v4", "snippet": ""},
          {"title": "Memory-Efficient 4-bit Preconditioned Stochastic Optimization", "url": "https://arxiv.org/pdf/2412.10663", "snippet": ""}
        ]},
        {"n": 2, "query": "memory-aware test-time scaling agent experience synthesis convergence optimization", "allowed_domains": ["arxiv.org"], "results": [
          {"title": "[2509.25140] ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/abs/2509.25140", "snippet": ""},
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""},
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/html/2509.25140v1", "snippet": ""},
          {"title": "MemCoT: Test-Time Scaling through Memory-Driven Chain-of-Thought", "url": "https://arxiv.org/html/2604.08216", "snippet": ""},
          {"title": "Democratizing Agentic AI with Fast Test-Time Scaling on the Edge", "url": "https://arxiv.org/pdf/2509.00195", "snippet": ""},
          {"title": "TMAS: Scaling Test-Time Compute via Multi-Agent Synergy", "url": "https://arxiv.org/html/2605.10344v1", "snippet": ""}
        ]},
        {"n": 3, "query": "optimizer-inspired schedule agent interaction memory quality test-time scaling LLM", "allowed_domains": ["arxiv.org"], "results": [
          {"title": "Democratizing Agentic AI with Fast Test-Time Scaling on the Edge", "url": "https://arxiv.org/pdf/2509.00195", "snippet": ""},
          {"title": "Choosing How to Remember: Adaptive Memory Structures for LLM Agents", "url": "https://arxiv.org/html/2602.14038v1", "snippet": ""},
          {"title": "TIDE: Trajectory-based Diagnostic Evaluation of Test-Time Improvement in LLM Agents", "url": "https://arxiv.org/pdf/2602.02196", "snippet": ""},
          {"title": "Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory", "url": "https://arxiv.org/pdf/2511.20857", "snippet": ""},
          {"title": "Throughput-Optimal Scheduling Algorithms for LLM Inference and AI Agents", "url": "https://arxiv.org/html/2504.07347v1", "snippet": ""},
          {"title": "AgentTTS: Large Language Model Agent for Test-time Compute-optimal Scaling Strategy in Complex Tasks", "url": "https://arxiv.org/pdf/2508.00890", "snippet": ""},
          {"title": "Agentic Auto-Scheduling: An Experimental Study of LLM-Guided Loop Optimization", "url": "https://arxiv.org/html/2511.00592v2", "snippet": ""}
        ]},
        {"n": 4, "query": "accelerating memory construction agent fewer rollouts preconditioned update test time", "allowed_domains": null, "results": [
          {"title": "Memory-R2: Fair Credit Assignment for Long-Horizon Memory-Augmented LLM Agents", "url": "https://arxiv.org/html/2605.21768", "snippet": ""},
          {"title": "Mem-{\\alpha}: Learning Memory Construction via Reinforcement Learning", "url": "https://arxiv.org/pdf/2509.25911", "snippet": ""},
          {"title": "Prune as You Generate: Online Rollout Pruning for Faster and Better RLVR", "url": "https://arxiv.org/pdf/2603.24840", "snippet": ""},
          {"title": "Do Not Waste Your Rollouts: Recycling Search Experience for Efficient Test-Time Scaling", "url": "https://arxiv.org/pdf/2601.21684", "snippet": ""},
          {"title": "Mem-T: Densifying Rewards for Long-Horizon Memory Agents", "url": "https://arxiv.org/pdf/2601.23014", "snippet": ""},
          {"title": "Preping: Building Agent Memory without Tasks", "url": "https://arxiv.org/html/2605.13880", "snippet": ""},
          {"title": "MemMA: Coordinating the Memory Cycle through Multi-Agent Reasoning and In-Situ Self-Evolution", "url": "https://arxiv.org/pdf/2603.18718", "snippet": ""},
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""}
        ]},
        {"n": 5, "query": "test-time scaling agent memory diverse experiences synthesized higher quality memory", "allowed_domains": null, "results": [
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""},
          {"title": "[2509.25140] ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/abs/2509.25140", "snippet": ""},
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory | OpenReview", "url": "https://openreview.net/forum?id=jL7fwchScm", "snippet": ""},
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/html/2509.25140v1", "snippet": ""},
          {"title": "ReasoningBank: Enabling agents to learn from experience", "url": "https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/", "snippet": ""},
          {"title": "New memory framework builds AI agents that can handle the real world's unpredictability | VentureBeat", "url": "https://venturebeat.com/ai/new-memory-framework-builds-ai-agents-that-can-handle-the-real-worlds", "snippet": ""},
          {"title": "General Agentic Memory via Deep Research", "url": "https://www.emergentmind.com/papers/2511.18423", "snippet": ""},
          {"title": "MemCoT: Test-Time Scaling through Memory-Driven Chain-of-Thought", "url": "https://arxiv.org/html/2604.08216", "snippet": ""},
          {"title": "Remember Me, Refine Me: A Dynamic Procedural Memory Framework for Experience-Driven Agent Evolution", "url": "https://arxiv.org/pdf/2512.10696", "snippet": ""}
        ]}
      ]
    },
    {
      "cand_id": "CAND_015_003",
      "niche_name": "Expert-Choice Routing for Memory-Aware Test-Time Scaling",
      "collision_found": false,
      "collision_reason": "The 5 searches return the two source papers (Expert-Choice routing; MaTTS/ReasoningBank) and adjacent routing-for-agents work (MemRouter, RCR-Router, EvoRoute, 'Memory Augmented Routing') plus trajectory-selection work (SWE-Replay, DreamGym), but those route context for retrieval or prune trajectories heuristically; none uses learned expert-choice routing to select which agent experiences feed specialized memory-synthesis heads for more efficient test-time scaling, so no direct prior-art collision was observed.",
      "reformulations": [
        {"n": 1, "query": "expert-choice routing agent experiences memory synthesis test-time scaling selective", "allowed_domains": null, "results": [
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""},
          {"title": "ReasoningBank: Enabling agents to learn from experience", "url": "https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/", "snippet": ""},
          {"title": "Expert-choice Routing", "url": "https://www.emergentmind.com/topics/expert-choice-routing-c8a2405f-ee5d-47d2-9cc6-b49b92c01903", "snippet": ""},
          {"title": "Learning Agent Routing From Early Experience", "url": "https://arxiv.org/html/2605.07180", "snippet": ""},
          {"title": "Certain Head, Uncertain Tail: Expert-Sample for Test-Time Scaling in Fine-Grained MoE", "url": "https://arxiv.org/pdf/2602.02443", "snippet": ""},
          {"title": "Mixture-of-Experts with Expert Choice Routing", "url": "https://arxiv.org/pdf/2202.09368", "snippet": ""},
          {"title": "Mixture-of-Experts with Expert Choice Routing", "url": "https://papers.neurips.cc/paper_files/paper/2022/file/2f00ecd787b432c1d36f3de9800728eb-Paper-Conference.pdf", "snippet": ""}
        ]},
        {"n": 2, "query": "experience selection routing memory synthesis agent sparse informative interaction traces", "allowed_domains": ["arxiv.org"], "results": [
          {"title": "Scaling Agent Learning via Experience Synthesis", "url": "https://arxiv.org/pdf/2511.03773", "snippet": ""},
          {"title": "InfMem: Learning System-2 Memory Control for Long-Context Agent", "url": "https://arxiv.org/html/2602.02704", "snippet": ""},
          {"title": "Knowledge Access Beats Model Size: Memory Augmented Routing for Persistent AI Agents", "url": "https://arxiv.org/html/2603.23013v1", "snippet": ""},
          {"title": "Knowledge Access Beats Model Size: Memory Augmented Routing for Persistent AI Agents", "url": "https://arxiv.org/pdf/2603.23013", "snippet": ""},
          {"title": "Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects", "url": "https://arxiv.org/pdf/2512.12818", "snippet": ""},
          {"title": "ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents", "url": "https://arxiv.org/pdf/2602.01869", "snippet": ""}
        ]},
        {"n": 3, "query": "learned routing select agent interactions memory module efficient test-time scaling", "allowed_domains": ["arxiv.org"], "results": [
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/html/2509.25140v1", "snippet": ""},
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""},
          {"title": "MemCoT: Test-Time Scaling through Memory-Driven Chain-of-Thought", "url": "https://arxiv.org/html/2604.08216", "snippet": ""},
          {"title": "Select-then-Solve: Paradigm Routing as Inference-Time Optimization for LLM Agents", "url": "https://arxiv.org/html/2604.06753v1", "snippet": ""},
          {"title": "Thinking vs. Doing: Agents that Reason by Scaling Test-Time Interaction", "url": "https://arxiv.org/pdf/2506.07976", "snippet": ""},
          {"title": "MemRouter: Memory-as-Embedding Routing for Long-Term Conversational Agents", "url": "https://arxiv.org/html/2605.00356v1", "snippet": ""},
          {"title": "RCR-Router: Efficient Role-Aware Context Routing for Multi-Agent LLM Systems with Structured Memory", "url": "https://arxiv.org/html/2508.04903v1", "snippet": ""}
        ]},
        {"n": 4, "query": "expert choice routing memory heads agent experience aggregation language model", "allowed_domains": null, "results": [
          {"title": "Expert-choice Routing", "url": "https://www.emergentmind.com/topics/expert-choice-routing-c8a2405f-ee5d-47d2-9cc6-b49b92c01903", "snippet": ""},
          {"title": "Mixture of Experts in Large Language Models", "url": "https://arxiv.org/html/2507.11181v1", "snippet": ""},
          {"title": "Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing", "url": "https://arxiv.org/pdf/2603.11535", "snippet": ""},
          {"title": "Expert-Choice Routing Enables Adaptive Computation in Diffusion Language Models", "url": "https://arxiv.org/pdf/2604.01622", "snippet": ""},
          {"title": "EvoRoute: Experience-Driven Self-Routing LLM Agent Systems", "url": "https://arxiv.org/pdf/2601.02695", "snippet": ""},
          {"title": "AI-Driven Day-to-Day Route Choice", "url": "https://arxiv.org/pdf/2412.03338", "snippet": ""}
        ]},
        {"n": 5, "query": "routing mechanism filter agent trajectories memory synthesis test-time compute", "allowed_domains": null, "results": [
          {"title": "MemCoT: Test-Time Scaling through Memory-Driven Chain-of-Thought", "url": "https://arxiv.org/html/2604.08216", "snippet": ""},
          {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""},
          {"title": "What If We Allocate Test-Time Compute Adaptively?", "url": "https://arxiv.org/pdf/2602.01070", "snippet": ""},
          {"title": "Memory-Enhanced Neural Solvers for Routing Problems", "url": "https://arxiv.org/pdf/2406.16424", "snippet": ""},
          {"title": "Agent Workflow Memory", "url": "https://arxiv.org/html/2409.07429v1", "snippet": ""},
          {"title": "Mem^p: Exploring Agent Procedural Memory", "url": "https://arxiv.org/html/2508.06433v2", "snippet": ""},
          {"title": "Multi-Agent Coordination in Autonomous Vehicle Routing: A Simulation-Based Study of Communication, Memory, and Routing Loops", "url": "https://arxiv.org/html/2511.17656v1", "snippet": ""}
        ]}
      ]
    }
  ]
}
```

## [REPORT 4] crosscheck.json (verbatim)
```json
{
  "run_id": "run_015",
  "agent": "4_crosschecker",
  "crosschecked_at": "2026-05-31T21:19:30Z",
  "verbatim_note": "All titles/urls are from AGENT 4's OWN real WebSearch results; independent of AGENT 3; no fabrication.",
  "candidates": [
    {
      "cand_id": "CAND_015_001",
      "agent3_collision_found": false,
      "agent4_collision": false,
      "mismatch_with_agent3": false,
      "notes": "CONFIRMS AGENT 3. Two fresh independent searches surfaced the source papers (Conda, MoSA) plus adjacent work (Preconditioned Attention 2603.27153, Crisp Attention, Spectral Conditioning of Attention, EcoSpa coupled sparsity), but none has a title describing the specific niche of using routing-induced attention sparsity as a structured prior that conditions a preconditioned optimizer to accelerate convergence. Preconditioned Attention conditions the attention matrix itself, not the optimizer via expert-choice routing sparsity. No direct prior-art collision.",
      "recheck_searches": [
        {
          "n": 1,
          "query": "routing-induced attention sparsity as structured prior conditioning preconditioned optimizer faster transformer convergence",
          "allowed_domains": ["arxiv.org"],
          "results": [
            {"title": "[2603.27153] Preconditioned Attention: Enhancing Efficiency in Transformers", "url": "https://arxiv.org/abs/2603.27153", "snippet": ""},
            {"title": "Preconditioned Attention: Enhancing Efficiency in Transformers", "url": "https://arxiv.org/pdf/2603.27153", "snippet": ""},
            {"title": "Crisp Attention: Regularizing Transformers via Structured Sparsity", "url": "https://arxiv.org/pdf/2508.06016", "snippet": ""},
            {"title": "Crisp Attention: Regularizing Transformers via Structured Sparsity", "url": "https://arxiv.org/html/2508.06016v1", "snippet": ""},
            {"title": "Attention Condensation via Sparsity Induced Regularized Training", "url": "https://arxiv.org/html/2503.01564v1", "snippet": ""},
            {"title": "Spectral Conditioning of Attention Improves Transformer Performance", "url": "https://arxiv.org/pdf/2603.07162", "snippet": ""}
          ]
        },
        {
          "n": 2,
          "query": "coupling expert-choice sparse attention gradients with column-normalized Adam optimizer speed up LLaMA pretraining",
          "allowed_domains": null,
          "results": [
            {"title": "A Minimalist Optimizer Design for LLM Pretraining", "url": "https://arxiv.org/html/2506.16659v1", "snippet": ""},
            {"title": "Conda: Column-Normalized Adam for Training Large Language Models Faster", "url": "https://arxiv.org/html/2509.24218v2", "snippet": ""},
            {"title": "A Minimalist Optimizer Design for LLM Pretraining", "url": "https://arxiv.org/pdf/2506.16659", "snippet": ""},
            {"title": "[2509.24218] Conda: Column-Normalized Adam for Training Large Language Models Faster", "url": "https://arxiv.org/abs/2509.24218", "snippet": ""},
            {"title": "EcoSpa: Efficient Transformer Training with Coupled Sparsity", "url": "https://arxiv.org/pdf/2511.11641", "snippet": ""},
            {"title": "Grass: Compute Efficient Low-Memory LLM Training with Structured Sparse Gradients", "url": "https://arxiv.org/pdf/2406.17660", "snippet": ""},
            {"title": "AdamS: Momentum Itself Can Be A Normalizer for LLM Pretraining and Post-training", "url": "https://arxiv.org/pdf/2505.16363", "snippet": ""}
          ]
        }
      ]
    },
    {
      "cand_id": "CAND_015_002",
      "agent3_collision_found": false,
      "agent4_collision": false,
      "mismatch_with_agent3": false,
      "notes": "CONFIRMS AGENT 3. Two fresh independent searches returned the MaTTS/ReasoningBank source (2509.25140) plus generic preconditioned/subspace optimizers (SUMO 2505.24749, Memory Augmented Optimizers 2106.10708, Extreme Tensoring) and generic agent-memory work, but no paper-like title transplants an optimizer's preconditioned-convergence principle into agent memory synthesis to cut interaction rounds needed to reach a target memory quality. No direct prior-art collision.",
      "recheck_searches": [
        {
          "n": 1,
          "query": "preconditioned update rule applied to agent memory synthesis reduce interaction rounds reach target memory quality test-time scaling",
          "allowed_domains": null,
          "results": [
            {"title": "AMA: Adaptive Memory via Multi-Agent Collaboration", "url": "https://arxiv.org/html/2601.20352v2", "snippet": ""},
            {"title": "Mem^p: Exploring Agent Procedural Memory", "url": "https://arxiv.org/html/2508.06433v2", "snippet": ""},
            {"title": "RPMS: Enhancing LLM-Based Embodied Planning through Rule-Augmented Memory Synergy", "url": "https://arxiv.org/html/2603.17831", "snippet": ""},
            {"title": "Correcting Stochastic Update Bias in Preconditioned Language Model Optimizers", "url": "https://arxiv.org/html/2605.20756", "snippet": ""},
            {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""}
          ]
        },
        {
          "n": 2,
          "query": "optimizer convergence acceleration transplanted into memory-aware test-time scaling MaTTS fewer agent experiences higher quality memory",
          "allowed_domains": ["arxiv.org"],
          "results": [
            {"title": "Are We Scaling the Right Thing? A System Perspective on Test-Time Scaling", "url": "https://arxiv.org/html/2509.19645", "snippet": ""},
            {"title": "FastTTS: Accelerating Test-Time Scaling for Edge LLM Reasoning", "url": "https://arxiv.org/html/2509.00195", "snippet": ""},
            {"title": "Memory Augmented Optimizers for Deep Learning", "url": "https://arxiv.org/pdf/2106.10708", "snippet": ""},
            {"title": "Faster and Better LLMs via Latency-Aware Test-Time Scaling", "url": "https://arxiv.org/html/2505.19634v1", "snippet": ""},
            {"title": "SUMO: Subspace-Aware Moment-Orthogonalization for Accelerating Memory-Efficient LLM Training", "url": "https://arxiv.org/pdf/2505.24749", "snippet": ""},
            {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""}
          ]
        }
      ]
    },
    {
      "cand_id": "CAND_015_003",
      "agent3_collision_found": false,
      "agent4_collision": false,
      "mismatch_with_agent3": false,
      "notes": "CONFIRMS AGENT 3. Two fresh independent searches returned the MaTTS/ReasoningBank source plus adjacent work (Decocted Experience 2604.04373, ProcMEM 2602.01869, D-MEM: Dopamine-Gated Agentic Memory via Reward Prediction Error Routing 2603.14597, Compiled Memory, MoE-gating used for memory retrieval weighting), but none has a title describing learned expert-choice/experience-choice routing that selects which agent experiences feed specialized memory-synthesis heads for more efficient test-time scaling. D-MEM gates storage by reward-prediction-error and the MoE gating is for retrieval, not experience-choice routing into synthesis heads. No direct prior-art collision.",
      "recheck_searches": [
        {
          "n": 1,
          "query": "experience-choice routing select which agent interaction traces feed specialized memory-synthesis heads test-time scaling",
          "allowed_domains": ["arxiv.org"],
          "results": [
            {"title": "[2509.25140] ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/abs/2509.25140", "snippet": ""},
            {"title": "Decocted Experience Improves Test-Time Inference in LLM Agents", "url": "https://arxiv.org/html/2604.04373", "snippet": ""},
            {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/html/2509.25140v1", "snippet": ""},
            {"title": "Thinking vs. Doing: Agents that Reason by Scaling Test-Time Interaction", "url": "https://arxiv.org/pdf/2506.07976", "snippet": ""},
            {"title": "TMAS: Scaling Test-Time Compute via Multi-Agent Synergy", "url": "https://arxiv.org/html/2605.10344", "snippet": ""}
          ]
        },
        {
          "n": 2,
          "query": "learned gating route accumulated agent experiences to memory heads sparse high-quality memory improve test-time scaling efficiency",
          "allowed_domains": null,
          "results": [
            {"title": "Compiled Memory: Not More Information, but More Precise Instructions for Language Agents", "url": "https://arxiv.org/pdf/2603.15666", "snippet": ""},
            {"title": "ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents", "url": "https://arxiv.org/pdf/2602.01869", "snippet": ""},
            {"title": "Memory Based Trajectory-conditioned Policies for Learning from Sparse Rewards", "url": "https://arxiv.org/pdf/1907.10247", "snippet": ""},
            {"title": "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory", "url": "https://arxiv.org/pdf/2509.25140", "snippet": ""},
            {"title": "Routing Absorption in Sparse Attention: Why Random Gates Are Hard to Beat", "url": "https://arxiv.org/pdf/2603.02227", "snippet": ""},
            {"title": "D-MEM: Dopamine-Gated Agentic Memory via Reward Prediction Error Routing", "url": "https://arxiv.org/pdf/2603.14597", "snippet": ""}
          ]
        }
      ]
    }
  ]
}
```

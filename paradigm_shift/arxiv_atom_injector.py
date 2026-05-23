"""arXiv Atom Injector — Run 10 corpus expansion.

Counter-method for RC_002 NARROW_INPUT_POOL (Run 9 binding constraint).
Implements arXiv:2412.14141 "LLMs Can Realize Combinatorial Creativity"
recommendation: inject synthetic atoms from a curated frontier-ML knowledge graph.

Atoms are seeded from REAL web_search results executed in Phase 1 (≥3
reformulations per topic, ≥3 abstracts per topic, ≥8 ML frontier topics).
Each atom is tagged source=ARXIV, transcript_id=ARXIV_{paper_id} so the
downstream pipeline can distinguish transcript atoms from arXiv atoms and
apply a cross-source diversity bias.

This module does NOT issue web_search at runtime — those are issued by
the harness (Claude main agent) and the curated abstracts are baked in
here. To refresh the corpus, re-run the harness Phase 1 searches and
update ARXIV_ABSTRACTS below.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

THIS_DIR = Path(__file__).parent
ATOMS_OUT_DIR = THIS_DIR / "arxiv_atoms"


# ---------- Atom typology (matches atom_typer.py vocabulary) ----------

ATOM_TYPES = {
    "MECHANISM_CLAIM": "How a system works (e.g., MoE router uses gradient conflict).",
    "PREDICTION": "Forward-looking claim about future capability or scaling.",
    "BLOCKER": "Identified barrier preventing progress.",
    "OPEN_PROBLEM": "Acknowledged unresolved question in the literature.",
    "FIRST_PRINCIPLE": "Foundational assumption a paper rests on.",
    "ANALOGY": "Cross-domain mapping (e.g., MoE expert ↔ specialization).",
}


@dataclass
class ArxivAtom:
    atom_id: str
    paper_id: str
    paper_title: str
    paper_section_ref: str
    atom_type: str
    text: str
    topic: str
    verbatim_snippet: str
    source: str = "ARXIV"
    transcript_id: str = ""

    def __post_init__(self):
        if not self.transcript_id:
            self.transcript_id = f"ARXIV_{self.paper_id.replace('.', '_').replace('/', '_')}"


# ---------- Curated arXiv abstracts from Phase 1 web_search ----------
# Each entry: (paper_id, title, topic, section_ref, verbatim_snippet)
ARXIV_ABSTRACTS: List[Dict] = [
    # ===== Topic 1: foundation_models / scaling_laws =====
    {
        "paper_id": "2508.02929",
        "title": "Realizing Scaling Laws in Recommender Systems: A Foundation-Expert Paradigm for Hyperscale Model Deployment",
        "topic": "foundation_models",
        "section_ref": "Abstract",
        "verbatim_snippet": "Foundation-Expert Paradigm, a framework designed for the development and deployment of hyperscale recommendation foundation models, deployed at Meta serving tens of billions of user requests daily.",
    },
    {
        "paper_id": "2503.08223",
        "title": "Will LLMs Scaling Hit the Wall? Breaking Barriers via Distributed Resources on Massive Edge Devices",
        "topic": "foundation_models",
        "section_ref": "Abstract",
        "verbatim_snippet": "Reviews recent technical advancements in distributed/federated learning that make a new paradigm viable, revealing the vast untapped potential of data and computational resources on massive edge devices.",
    },
    {
        "paper_id": "2501.02156",
        "title": "The Race to Efficiency: A New Perspective on AI Scaling Laws",
        "topic": "foundation_models",
        "section_ref": "Abstract",
        "verbatim_snippet": "Presents a time- and efficiency-aware foundation for AI scaling, revealing how a race to efficiency naturally emerges once classical, static scaling approaches are considered.",
    },
    # ===== Topic 2: modular_moe =====
    {
        "paper_id": "2602.09001",
        "title": "DirMoE: Dirichlet-routed Mixture of Experts",
        "topic": "modular_moe",
        "section_ref": "Method / Abstract",
        "verbatim_snippet": "Introduces a Dirichlet variational router that factorizes routing into a binary selection vector over experts and a Dirichlet distribution over mixture weights, producing a relaxed expert selection vector via Gumbel-Sigmoid reparameterization.",
    },
    {
        "paper_id": "2510.16448",
        "title": "Input Domain Aware MoE: Decoupling Routing Decisions from Task Optimization in Mixture of Experts",
        "topic": "modular_moe",
        "section_ref": "Abstract",
        "verbatim_snippet": "Proposes a novel routing framework that leverages a probabilistic mixture model to better partition the input space, with routing mechanism trained independently of task-specific objectives for stable optimization.",
    },
    {
        "paper_id": "2512.20291",
        "title": "Mixture-of-Experts with Gradient Conflict-Driven Subspace Topology Pruning for Emergent Modularity",
        "topic": "modular_moe",
        "section_ref": "Abstract",
        "verbatim_snippet": "Rather than treating gradient conflict as optimization noise to be suppressed, they leverage it as a structural supervisory signal by monitoring the cosine similarity of gradients between experts on the shared backbone to penalize connections that cause interference.",
    },
    # ===== Topic 3: retrieval_augmented =====
    {
        "paper_id": "2510.13191",
        "title": "Grounding Long-Context Reasoning with Contextual Normalization for Retrieval-Augmented Generation",
        "topic": "retrieval_augmented",
        "section_ref": "Abstract",
        "verbatim_snippet": "Grounding long-context reasoning with contextual normalization for retrieval-augmented generation; addresses how mechanisms for resolving conflicts between retrieved evidence and the model's parametric memory remain unclear.",
    },
    {
        "paper_id": "2506.05154",
        "title": "Resisting Contextual Interference in RAG via Parametric-Knowledge Reinforcement (Knowledgeable-R1)",
        "topic": "retrieval_augmented",
        "section_ref": "Abstract / Results",
        "verbatim_snippet": "Employs asymmetric advantage transformation amplifying exploratory behaviors toward parametric knowledge, outperforming baselines by +22.89% in counterfactual scenarios.",
    },
    {
        "paper_id": "2510.09106",
        "title": "When Retrieval Succeeds and Fails: Rethinking Retrieval-Augmented Generation for LLMs",
        "topic": "retrieval_augmented",
        "section_ref": "Abstract",
        "verbatim_snippet": "Mechanisms for resolving conflicts between retrieved evidence and the model's parametric memory remain unclear, often leading to unpredictable behavior.",
    },
    # ===== Topic 4: agents =====
    {
        "paper_id": "2511.01527",
        "title": "TPS-Bench: Evaluating AI Agents' Tool Planning & Scheduling Abilities in Compounding Tasks",
        "topic": "agents",
        "section_ref": "Abstract",
        "verbatim_snippet": "Real-world scenarios often involve compounding tasks that demand the collaboration of various tools; most models exhibit reasonable performance in tool planning but behave differently in scheduling.",
    },
    {
        "paper_id": "2509.21766",
        "title": "UltraHorizon: Benchmarking Agent Capabilities in Ultra Long-Horizon Scenarios",
        "topic": "agents",
        "section_ref": "Abstract / Findings",
        "verbatim_snippet": "Trajectories averaging 200k+ tokens with 400+ tool calls; LLM-agents consistently underperform while human participants achieve higher scores. Eight error types attributed to in-context locking and fundamental capability gaps; meltdown behavior emerges in long-horizon trajectories.",
    },
    {
        "paper_id": "2511.02824",
        "title": "Kosmos: An AI Scientist for Autonomous Discovery",
        "topic": "agents",
        "section_ref": "Abstract",
        "verbatim_snippet": "Given an open-ended objective and a dataset, Kosmos runs for up to 12 hours performing cycles of parallel data analysis, literature search, and hypothesis generation before synthesizing discoveries into scientific reports.",
    },
    # ===== Topic 5: world_models / JEPA =====
    {
        "paper_id": "2506.09985",
        "title": "V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning",
        "topic": "world_models",
        "section_ref": "Abstract",
        "verbatim_snippet": "Pre-trained action-free joint-embedding-predictive architecture trained on a video and image dataset comprising over 1 million hours of internet video; deployed zero-shot on Franka arms in two different labs for picking and placing with image goals.",
    },
    {
        "paper_id": "2512.10942",
        "title": "VL-JEPA: Joint Embedding Predictive Architecture for Vision-language",
        "topic": "world_models",
        "section_ref": "Abstract",
        "verbatim_snippet": "Joint embedding predictive architecture for vision-language extends JEPA framework to multimodal inputs by predicting latent representations rather than pixel reconstruction.",
    },
    {
        "paper_id": "2602.10098",
        "title": "VLA-JEPA: Enhancing Vision-Language-Action Model with Latent World Model",
        "topic": "world_models",
        "section_ref": "Abstract",
        "verbatim_snippet": "Enhances vision-language-action model with a latent world model derived from JEPA predictive embeddings to improve sample efficiency of robot policy learning.",
    },
    # ===== Topic 6: test_time_training =====
    {
        "paper_id": "2503.11842",
        "title": "Test-Time Training Provably Improves Transformers as In-context Learners",
        "topic": "test_time_training",
        "section_ref": "Theory section",
        "verbatim_snippet": "Test-time training methods explicitly update model weights to adapt to specific test instances; theoretical characterization of linear transformers with single gradient step updates examines distribution alignment and how TTT alleviates distribution shift.",
    },
    {
        "paper_id": "2509.25741",
        "title": "Test time training enhances in-context learning of nonlinear functions",
        "topic": "test_time_training",
        "section_ref": "Abstract / Results",
        "verbatim_snippet": "TTT adapts models by updating parameters on test data before each prediction; integrating TTT with in-context learning by using in-context examples as adaptation data achieves improvements on few-shot reasoning benchmarks.",
    },
    {
        "paper_id": "2508.07571",
        "title": "Towards Theoretical Understanding of Transformer Test-Time",
        "topic": "test_time_training",
        "section_ref": "Abstract",
        "verbatim_snippet": "Addresses the gap in theoretical understanding of test-time computation for transformer in-context learning, characterizing sample complexity benefit proportional to the number of target examples within the prompt.",
    },
    # ===== Topic 7: RLHF / reward_hacking =====
    {
        "paper_id": "2502.18770",
        "title": "Reward Shaping to Mitigate Reward Hacking in RLHF",
        "topic": "rlhf",
        "section_ref": "Abstract / Method",
        "verbatim_snippet": "RLHF is susceptible to reward hacking where the agent exploits flaws in the reward function rather than learning the intended behavior; identifies two design principles: the RL reward should be bounded, and should have rapid initial growth followed by gradual convergence.",
    },
    {
        "paper_id": "2509.15557",
        "title": "Reward Hacking Mitigation using Verifiable Composite Rewards (RLVR)",
        "topic": "rlhf",
        "section_ref": "Method",
        "verbatim_snippet": "Leverages the existing RLHF objective but replaces the reward model with a verification function; the policy only receives a reward when its generated responses are verifiably correct.",
    },
    {
        "paper_id": "2604.02986",
        "title": "Mitigating Reward Hacking in RLHF via Advantage Sign Robustness",
        "topic": "rlhf",
        "section_ref": "Abstract",
        "verbatim_snippet": "Proposes that reward hacking is often caused by flipped advantage signs, derives a certified sign-preservation radius which is the smallest perturbation that can flip the advantage sign during policy optimization.",
    },
    # ===== Topic 8: mechanistic_interpretability =====
    {
        "paper_id": "2509.03738",
        "title": "Mechanistic Interpretability with Sparse Autoencoder Neural Operators",
        "topic": "mechanistic_interpretability",
        "section_ref": "Abstract",
        "verbatim_snippet": "SAEs are employed in mechanistic interpretability to decompose the hidden activations of large language models into sparse latent representations that ideally correspond to semantically distinct, causal features.",
    },
    {
        "paper_id": "2508.09363",
        "title": "Resurrecting the Salmon: Rethinking Mechanistic Interpretability with Domain-Specific Sparse Autoencoders",
        "topic": "mechanistic_interpretability",
        "section_ref": "Abstract",
        "verbatim_snippet": "Domain-specific sparse autoencoders rethink mechanistic interpretability; circuits defined as subgraphs of a model's computation graph that implement a task-specific behaviour.",
    },
    {
        "paper_id": "2403.19647",
        "title": "Sparse Feature Circuits: Discovering and Editing Interpretable Causal Graphs in Language Models",
        "topic": "mechanistic_interpretability",
        "section_ref": "Method",
        "verbatim_snippet": "Discovers and edits interpretable causal graphs in language models by composing SAE-extracted features into circuits that can be ablated or amplified.",
    },
    # ===== Topic 9: emergent_abilities (bonus topic 9) =====
    {
        "paper_id": "2511.12768",
        "title": "Evidence of Phase Transitions in Small Transformer-Based Language Models",
        "topic": "emergent_abilities",
        "section_ref": "Abstract",
        "verbatim_snippet": "Phase transitions proposed as the origin of emergent abilities in large language models; new capabilities appear abruptly once models surpass critical thresholds of scale.",
    },
    {
        "paper_id": "2508.04401",
        "title": "Why are LLMs' abilities emergent?",
        "topic": "emergent_abilities",
        "section_ref": "Abstract",
        "verbatim_snippet": "Emergent abilities arise from the complex dynamics of highly sensitive nonlinear systems rather than simply from parameter scaling; debate remains about whether jumps are discontinuous or continuous under different metrics.",
    },
    {
        "paper_id": "2506.11135",
        "title": "Large Language Models and Emergence: A Complex Systems Perspective",
        "topic": "emergent_abilities",
        "section_ref": "Abstract",
        "verbatim_snippet": "Argues emergent abilities arise from complex-systems dynamics; covariance spectra of weights transition from exponential to scale-free concomitantly with the peak of double-descent behavior.",
    },
    # ===== Topic 10: autonomous_research_agents (bonus topic 10) =====
    {
        "paper_id": "2511.08522",
        "title": "AlphaResearch: Accelerating New Algorithm Discovery with Language Models",
        "topic": "autonomous_research",
        "section_ref": "Abstract",
        "verbatim_snippet": "Autonomous research agent that synergistically combines new idea generation with program-based verification for novel algorithm discovery; achieves stronger discovery performance than other agentic discovery systems on six open-ended problems.",
    },
    {
        "paper_id": "2604.01658",
        "title": "CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery",
        "topic": "autonomous_research",
        "section_ref": "Abstract",
        "verbatim_snippet": "First framework for autonomous multi-agent evolution on open-ended problems; achieves 3-10x higher improvement rates with far fewer evaluations than fixed evolutionary search baselines on 10 tasks.",
    },
    {
        "paper_id": "2507.00310",
        "title": "AutoDiscovery: Open-ended Scientific Discovery via Bayesian Surprise",
        "topic": "autonomous_research",
        "section_ref": "Abstract / Results",
        "verbatim_snippet": "Finds 5-29% more hypotheses surprising to the LLM agent compared to strong search baselines; two-thirds of surprising discoveries correlate with human surprisal in a human study.",
    },
    # ===== COLD TOPICS (Run 10 epoch 2 R-fix for RC_006 HOT_TOPIC_ARXIV_SATURATION) =====
    # Topic 11: model-native agentic AI (rejecting pipeline-prompt paradigm)
    {
        "paper_id": "2510.16720",
        "title": "Beyond Pipelines: A Survey of the Paradigm Shift toward Model-Native Agentic AI",
        "topic": "model_native_agents",
        "section_ref": "Abstract",
        "verbatim_snippet": "An emerging model-native paradigm is shifting from the traditional pipeline-based approach where agents were composite systems linked through prompts, toward a unified model that through end-to-end training learns to autonomously perform high-level functions.",
    },
    # Topic 12: contrarian existential risk (under-explored counter-narrative)
    {
        "paper_id": "2512.04119",
        "title": "Humanity in the Age of AI: Reassessing 2025's Existential-Risk Narratives",
        "topic": "ai_risk_reassessment",
        "section_ref": "Abstract",
        "verbatim_snippet": "Despite 60 years of speculation, phenomena like sustained recursive self-improvement and autonomous strategic awareness have not been observed; current generative models remain narrow statistically trained artifacts lacking the properties that would make catastrophic scenarios plausible.",
    },
    # Topic 13: efficiency of agent systems (neglected per arxiv)
    {
        "paper_id": "2509.23586",
        "title": "Improving the Efficiency of LLM Agent Systems through Trajectory Reduction",
        "topic": "agent_efficiency",
        "section_ref": "Abstract",
        "verbatim_snippet": "Focuses on the efficiency concern of coding LLM agents, which is neglected by existing studies; proposes trajectory reduction to compress repeated execution states.",
    },
    # Topic 14: algorithmic foundations of LLM serving (under-explored)
    {
        "paper_id": "2605.01280",
        "title": "Position: LLM Serving Needs Mathematical Optimization and Algorithmic Foundations, Not Just Heuristics",
        "topic": "llm_serving_foundations",
        "section_ref": "Position paper",
        "verbatim_snippet": "Classical scheduling questions complicated by LLM-specific structure of growing memory consumption and unknown job durations, suggest opportunities for principled scheduling algorithms; argues current LLM serving relies on heuristics rather than algorithmic foundations.",
    },
    # Topic 15: RL under data scarcity (less saturated than reward hacking)
    {
        "paper_id": "2604.17312",
        "title": "A Survey of Reinforcement Learning for Large Language Models under Data Scarcity: Challenges and Solutions",
        "topic": "rl_data_scarcity",
        "section_ref": "Survey",
        "verbatim_snippet": "Reinforcement learning for large language models under data scarcity raises distinct challenges in sample efficiency, off-policy correction, and exploration that are not addressed by standard online RLHF pipelines.",
    },
    # Topic 16: offline-log proactive LLM (less saturated than online interactive)
    {
        "paper_id": "2510.25441",
        "title": "Grounded in Reality: Learning and Deploying Proactive LLM from Offline Logs",
        "topic": "offline_log_learning",
        "section_ref": "Abstract",
        "verbatim_snippet": "Learning proactive LLM behavior from offline interaction logs rather than online preference labeling enables grounding in deployed-system reality without active human-in-the-loop, an under-explored alternative to online RLHF.",
    },
    # ===== CROSS-DISCIPLINARY (Run 10 epoch 3 R-fix for RC_007 META_SATURATION_EVEN_COLD_TOPICS) =====
    # Topic 17: evolutionary developmental biology for AI design
    {
        "paper_id": "2506.12891",
        "title": "Evolutionary Developmental Biology and AI Paradigm",
        "topic": "evodevo_for_ai",
        "section_ref": "Abstract / Theoretical Framework",
        "verbatim_snippet": "Moves beyond superficial biological analogies and instead grounds itself in fundamental conceptual principles of adaptation and biological organization; introduces a theoretical framework that evolutionary developmental biology offers for a new design paradigm for AI.",
    },
    # Topic 18: NeuroAI capability gaps + neuroscience principles
    {
        "paper_id": "2604.18637",
        "title": "NeuroAI and Beyond: Bridging Between Advances in Neuroscience and Artificial Intelligence",
        "topic": "neuroai",
        "section_ref": "Three capability gaps",
        "verbatim_snippet": "Three fundamental capability gaps in current AI were identified: inability to interact with the physical world, inadequate learning that produces brittle systems, and unsustainable energy and data inefficiency; neuroscience principles address each including co-design of body and controller, prediction through interaction, and sparse event-driven computation.",
    },
    # Topic 19: thermodynamics for deep learning
    {
        "paper_id": "2506.01506",
        "title": "Deep Learning of Thermodynamic Laws from Microscopic Dynamics",
        "topic": "thermodynamics_dl",
        "section_ref": "Discussion",
        "verbatim_snippet": "Deep neural networks can learn thermodynamic principles from microscopic dynamics; the work suggests that DNNs perform a form of statistical mechanics and raises the possibility of a novel statistical mechanical framework for understanding learning itself.",
    },
    # Topic 20: market-making for multi-agent LLM safety (econ x LLM)
    {
        "paper_id": "2511.17621",
        "title": "From Competition to Coordination: Market Making as a Scalable Framework for Safe and Aligned Multi-Agent LLM Systems",
        "topic": "market_making_safety",
        "section_ref": "Results",
        "verbatim_snippet": "Market-based coordination yields accuracy gains of up to 10% over single-shot baselines while preserving interpretability and transparency; economic coordination principles can operationalize accountability in multi-agent LLM systems.",
    },
    # Topic 21: brain-inspired AGI cognitive synthesis
    {
        "paper_id": "2507.00951",
        "title": "Thinking Beyond Tokens: From Brain-Inspired Intelligence to Cognitive Foundations for AGI",
        "topic": "brain_inspired_agi",
        "section_ref": "Abstract",
        "verbatim_snippet": "Offers a cross-disciplinary synthesis of AGI development spanning artificial intelligence, cognitive neuroscience, psychology, generative models, and agent-based systems.",
    },
    # Topic 22: mechanism design for LLM tax planners
    {
        "paper_id": "2507.15815",
        "title": "LLM Economist: Large Population Models and Mechanism Design in Multi-Agent Generative Simulacra",
        "topic": "mechanism_design_llm",
        "section_ref": "Method",
        "verbatim_snippet": "Introduces a fully language-based framework that embeds a population of persona-conditioned agents and a tax planner in a two-tier Stackelberg game for mechanism design.",
    },
]


# ---------- Atom extraction (mechanism / prediction / blocker / open_problem) ----------

# Keyword tables that classify abstract sentences by atom type.
MECHANISM_MARKERS = [
    "mechanism", "method", "framework", "architecture", "router", "factorizes",
    "introduces", "proposes", "leverages", "treats", "implements", "uses",
    "synergizes", "joint decoding", "verification function", "advantage transformation",
    "decompose", "topology pruning", "preconditioned gradient", "asymmetric advantage",
    "gradient", "attention", "embedding", "predictive architecture",
]
PREDICTION_MARKERS = [
    "will", "expected", "achieves", "enables", "improvement", "outperform",
    "stronger discovery performance", "improves", "open-ended", "ubiquitous",
    "naturally emerges", "deployed", "trillion", "billion",
]
BLOCKER_MARKERS = [
    "fails", "underperform", "meltdown", "incoherent", "in-context locking",
    "capability gap", "unclear", "unresolved", "remain unclear", "unpredictable behavior",
    "barrier", "interference", "conflict", "susceptible", "hacking",
    "hit the wall", "concerns", "unstable", "exploits flaws",
]
OPEN_PROBLEM_MARKERS = [
    "remain unclear", "open problem", "open challenge", "future work", "debate",
    "not clear", "questions", "rethinking", "remains an open",
]


def classify_atom_type(snippet: str) -> str:
    s = snippet.lower()
    counts = {
        "BLOCKER": sum(1 for m in BLOCKER_MARKERS if m in s),
        "OPEN_PROBLEM": sum(1 for m in OPEN_PROBLEM_MARKERS if m in s),
        "PREDICTION": sum(1 for m in PREDICTION_MARKERS if m in s),
        "MECHANISM_CLAIM": sum(1 for m in MECHANISM_MARKERS if m in s),
    }
    best = max(counts.items(), key=lambda kv: kv[1])
    if best[1] == 0:
        return "MECHANISM_CLAIM"
    return best[0]


def extract_atom_text(snippet: str, atom_type: str) -> str:
    """Reduce the verbatim snippet to a single-clause atom text.

    Picks the first clause containing the strongest marker for the chosen type.
    """
    markers_for_type = {
        "BLOCKER": BLOCKER_MARKERS,
        "OPEN_PROBLEM": OPEN_PROBLEM_MARKERS,
        "PREDICTION": PREDICTION_MARKERS,
        "MECHANISM_CLAIM": MECHANISM_MARKERS,
    }[atom_type]
    sentences = re.split(r"[;.]\s+", snippet)
    for sent in sentences:
        s = sent.lower()
        for m in markers_for_type:
            if m in s:
                return sent.strip().rstrip(".")
    return sentences[0].strip().rstrip(".")


def build_arxiv_atom(abstract_entry: Dict, index: int) -> ArxivAtom:
    atom_type = classify_atom_type(abstract_entry["verbatim_snippet"])
    atom_text = extract_atom_text(abstract_entry["verbatim_snippet"], atom_type)
    paper_id_token = abstract_entry["paper_id"].replace(".", "_")
    atom_id = f"ATOM_ARXIV_{paper_id_token}_{index:02d}"
    return ArxivAtom(
        atom_id=atom_id,
        paper_id=abstract_entry["paper_id"],
        paper_title=abstract_entry["title"],
        paper_section_ref=abstract_entry["section_ref"],
        atom_type=atom_type,
        text=atom_text,
        topic=abstract_entry["topic"],
        verbatim_snippet=abstract_entry["verbatim_snippet"],
    )


def inject_atoms() -> List[ArxivAtom]:
    """Build all arXiv atoms from the curated abstracts."""
    atoms: List[ArxivAtom] = []
    for i, entry in enumerate(ARXIV_ABSTRACTS):
        atom = build_arxiv_atom(entry, i + 1)
        atoms.append(atom)
    return atoms


def save_atoms(atoms: List[ArxivAtom]) -> Path:
    ATOMS_OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = ATOMS_OUT_DIR / "arxiv_atoms_run10.json"
    payload = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "atom_count": len(atoms),
        "topics": sorted({a.topic for a in atoms}),
        "atoms": [asdict(a) for a in atoms],
    }
    with out_path.open("w") as fh:
        json.dump(payload, fh, indent=2)
    return out_path


def topic_distribution(atoms: List[ArxivAtom]) -> Dict[str, int]:
    dist: Dict[str, int] = {}
    for a in atoms:
        dist[a.topic] = dist.get(a.topic, 0) + 1
    return dist


def type_distribution(atoms: List[ArxivAtom]) -> Dict[str, int]:
    dist: Dict[str, int] = {}
    for a in atoms:
        dist[a.atom_type] = dist.get(a.atom_type, 0) + 1
    return dist


def main():
    atoms = inject_atoms()
    out_path = save_atoms(atoms)
    print(f"[arxiv_atom_injector] {len(atoms)} atoms across {len({a.topic for a in atoms})} topics")
    print(f"[arxiv_atom_injector] saved -> {out_path}")
    print(f"[arxiv_atom_injector] topic_distribution: {topic_distribution(atoms)}")
    print(f"[arxiv_atom_injector] type_distribution:  {type_distribution(atoms)}")
    for a in atoms[:5]:
        print(f"  {a.atom_id} [{a.atom_type}/{a.topic}] {a.text[:80]}...")


if __name__ == "__main__":
    main()

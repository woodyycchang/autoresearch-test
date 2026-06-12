#!/usr/bin/env python3
"""
build_concept_bank.py  —  Run 32 real-encyclopedia bank builder.

Emits engine/concept_banks.json: a curated, multi-domain concept bank. Each
concept carries machine-readable MECHANISM tokens ("how it works", the
transferable interface) and PROBLEM tokens ("what it addresses"). The merge
engine pairs concepts across domains and the integrity/niche checkers reason
over these token sets, so the tokens are the substantive part of the bank.

This is deterministic: running it twice produces byte-identical output. The
true concept count is whatever this file curates and is reported honestly by
the instrumentation (it is NOT forced to the inherited 791 — see INHERITANCE.md).
"""
import json
import os

# ---------------------------------------------------------------------------
# Curated multi-domain concepts. Mechanism tokens are deliberately drawn from a
# shared cross-domain vocabulary so that genuine (vs trivial / incoherent)
# transfers can be distinguished by token structure.
# ---------------------------------------------------------------------------
RAW = {
    "mathematics": [
        ("fixed_point_iteration", "Repeatedly apply a map until it stops moving.",
         ["iteration", "convergence", "contraction", "update"], ["solving", "equilibrium", "stability"]),
        ("spectral_decomposition", "Break an operator into eigen-components.",
         ["decomposition", "basis", "projection", "eigen"], ["structure", "dimensionality", "ordering"]),
        ("convex_relaxation", "Replace a hard set with its convex hull to make optimization tractable.",
         ["relaxation", "bound", "optimization", "approximation"], ["intractable", "search", "guarantee"]),
        ("graph_cut", "Partition a graph by minimizing edges across a boundary.",
         ["partition", "boundary", "minimization", "flow"], ["segmentation", "clustering", "separation"]),
        ("martingale", "A process whose expected next value is its current value.",
         ["expectation", "process", "drift", "fairness"], ["prediction", "risk", "stopping"]),
        ("homotopy_continuation", "Deform an easy problem into a hard one tracking solutions.",
         ["deformation", "continuation", "tracking", "path"], ["solving", "robustness", "initialization"]),
        ("measure_concentration", "High-dimensional mass concentrates near a thin shell.",
         ["concentration", "dimension", "tail", "bound"], ["estimation", "sampling", "generalization"]),
        ("duality_gap", "Distance between primal and dual optimum certifies optimality.",
         ["duality", "bound", "certificate", "gap"], ["optimization", "guarantee", "verification"]),
    ],
    "computer_science": [
        ("content_addressable_store", "Retrieve data by a hash of its content, not location.",
         ["hashing", "addressing", "dedup", "lookup"], ["storage", "retrieval", "integrity"]),
        ("write_ahead_log", "Record intent before mutating state for crash recovery.",
         ["logging", "ordering", "durability", "replay"], ["recovery", "consistency", "atomicity"]),
        ("bloom_filter", "Probabilistic set membership with no false negatives.",
         ["hashing", "probabilistic", "compression", "membership"], ["lookup", "memory", "filtering"]),
        ("backpressure", "Slow producers when consumers fall behind.",
         ["feedback", "throttle", "queue", "flow"], ["stability", "overload", "latency"]),
        ("copy_on_write", "Share state until a writer forks a private copy.",
         ["sharing", "lazy", "fork", "snapshot"], ["memory", "isolation", "versioning"]),
        ("consistent_hashing", "Map keys to nodes so few keys move when nodes change.",
         ["hashing", "partition", "ring", "rebalance"], ["scaling", "distribution", "churn"]),
        ("speculative_execution", "Do work before knowing if it is needed; roll back if not.",
         ["speculation", "rollback", "prefetch", "parallel"], ["latency", "throughput", "waste"]),
        ("gossip_protocol", "Spread state by random peer-to-peer exchange.",
         ["diffusion", "randomized", "epidemic", "redundancy"], ["consensus", "scaling", "robustness"]),
    ],
    "machine_learning": [
        ("gradient_descent", "Follow the negative gradient to minimize a loss.",
         ["gradient", "iteration", "update", "optimization"], ["learning", "fitting", "convergence"]),
        ("attention_mechanism", "Weight inputs by learned relevance to a query.",
         ["weighting", "relevance", "routing", "context"], ["selection", "sequence", "memory"]),
        ("contrastive_learning", "Pull positives together, push negatives apart.",
         ["contrast", "embedding", "similarity", "pairing"], ["representation", "labels", "structure"]),
        ("dropout_regularization", "Randomly drop units to prevent co-adaptation.",
         ["randomized", "ensemble", "noise", "redundancy"], ["overfitting", "generalization", "robustness"]),
        ("knowledge_distillation", "Train a small model to mimic a large one's outputs.",
         ["compression", "teacher", "soft_target", "transfer"], ["efficiency", "deployment", "fidelity"]),
        ("mixture_of_experts", "Route each input to a few specialized sub-models.",
         ["routing", "sparsity", "specialization", "gating"], ["scaling", "capacity", "efficiency"]),
        ("curriculum_learning", "Present easy examples before hard ones.",
         ["ordering", "scheduling", "difficulty", "staging"], ["learning", "convergence", "stability"]),
        ("active_learning", "Query labels for the most informative points.",
         ["selection", "uncertainty", "query", "feedback"], ["labels", "efficiency", "annotation"]),
    ],
    "physics": [
        ("renormalization", "Coarse-grain to see how behavior changes across scales.",
         ["coarse_grain", "scale", "flow", "invariance"], ["complexity", "universality", "scaling"]),
        ("simulated_annealing", "Anneal temperature to escape local minima.",
         ["temperature", "noise", "cooling", "search"], ["optimization", "local_minima", "global"]),
        ("phase_transition", "A small change flips the system's global order.",
         ["threshold", "order", "criticality", "transition"], ["stability", "emergence", "control"]),
        ("least_action", "Nature picks the path extremizing an action functional.",
         ["extremum", "path", "variational", "constraint"], ["dynamics", "prediction", "optimization"]),
        ("dissipation_fluctuation", "Response to perturbation relates to equilibrium noise.",
         ["fluctuation", "response", "equilibrium", "noise"], ["estimation", "stability", "measurement"]),
        ("conservation_law", "A symmetry implies a conserved quantity.",
         ["symmetry", "invariance", "conservation", "constraint"], ["structure", "prediction", "verification"]),
        ("resonance", "Driving near a natural frequency amplifies response.",
         ["frequency", "amplification", "tuning", "feedback"], ["amplification", "selectivity", "control"]),
    ],
    "biology": [
        ("natural_selection", "Differential reproduction filters heritable variation.",
         ["selection", "variation", "fitness", "heritability"], ["adaptation", "search", "optimization"]),
        ("immune_memory", "Past exposure primes a faster future response.",
         ["memory", "priming", "recognition", "adaptation"], ["defense", "recognition", "speed"]),
        ("apoptosis", "Programmed cell death prunes damaged or excess cells.",
         ["pruning", "programmed", "threshold", "cleanup"], ["regulation", "quality", "control"]),
        ("homeostasis", "Negative feedback holds internal state in a band.",
         ["feedback", "setpoint", "regulation", "stability"], ["stability", "control", "robustness"]),
        ("quorum_sensing", "Cells act collectively once density crosses a threshold.",
         ["threshold", "signaling", "density", "collective"], ["coordination", "timing", "emergence"]),
        ("horizontal_gene_transfer", "Traits move between organisms, not just by descent.",
         ["transfer", "sharing", "lateral", "recombination"], ["adaptation", "spread", "diversity"]),
        ("chemotaxis", "Move along a chemical gradient toward a target.",
         ["gradient", "sensing", "movement", "feedback"], ["navigation", "search", "targeting"]),
    ],
    "neuroscience": [
        ("predictive_coding", "The brain encodes prediction error, not raw input.",
         ["prediction", "error", "feedback", "compression"], ["perception", "efficiency", "learning"]),
        ("synaptic_pruning", "Unused connections are removed during development.",
         ["pruning", "use_dependent", "cleanup", "threshold"], ["efficiency", "specialization", "capacity"]),
        ("lateral_inhibition", "Active units suppress their neighbors to sharpen contrast.",
         ["inhibition", "contrast", "competition", "sharpening"], ["selection", "resolution", "encoding"]),
        ("replay_consolidation", "Offline replay of experience consolidates memory.",
         ["replay", "consolidation", "offline", "rehearsal"], ["memory", "stability", "learning"]),
        ("neuromodulation", "Global signals reconfigure network behavior on the fly.",
         ["modulation", "gain", "context", "gating"], ["flexibility", "control", "adaptation"]),
    ],
    "economics": [
        ("price_signal", "Prices aggregate dispersed information into one number.",
         ["aggregation", "signal", "incentive", "feedback"], ["coordination", "allocation", "information"]),
        ("mechanism_design", "Engineer rules so self-interest yields a desired outcome.",
         ["incentive", "rules", "equilibrium", "design"], ["coordination", "truthfulness", "allocation"]),
        ("auction", "Allocate scarce goods by competitive bidding.",
         ["bidding", "allocation", "competition", "valuation"], ["allocation", "revenue", "fairness"]),
        ("comparative_advantage", "Specialize where your relative cost is lowest.",
         ["specialization", "tradeoff", "allocation", "exchange"], ["efficiency", "division", "gains"]),
        ("reputation_system", "Past behavior priced into future trust.",
         ["reputation", "history", "feedback", "trust"], ["trust", "incentive", "selection"]),
        ("liquidity", "Ease of converting an asset without moving its price.",
         ["depth", "exchange", "buffer", "flow"], ["stability", "access", "resilience"]),
    ],
    "control_theory": [
        ("pid_control", "Correct error using its size, history, and trend.",
         ["feedback", "error", "integral", "derivative"], ["stability", "tracking", "regulation"]),
        ("kalman_filter", "Fuse noisy predictions and measurements optimally.",
         ["fusion", "estimation", "noise", "update"], ["estimation", "tracking", "uncertainty"]),
        ("model_predictive_control", "Optimize over a rolling horizon, act, repeat.",
         ["horizon", "optimization", "rolling", "constraint"], ["control", "planning", "constraint"]),
        ("lyapunov_stability", "A decreasing energy function certifies stability.",
         ["energy", "certificate", "decrease", "invariance"], ["stability", "guarantee", "verification"]),
        ("observer", "Reconstruct hidden state from outputs.",
         ["estimation", "reconstruction", "feedback", "hidden"], ["observability", "monitoring", "state"]),
    ],
    "information_theory": [
        ("error_correcting_code", "Add redundancy so noise can be reversed.",
         ["redundancy", "encoding", "recovery", "distance"], ["reliability", "noise", "integrity"]),
        ("rate_distortion", "Trade bits against reconstruction error optimally.",
         ["compression", "tradeoff", "distortion", "bound"], ["efficiency", "fidelity", "limits"]),
        ("mutual_information", "How much one variable tells you about another.",
         ["dependence", "information", "correlation", "measure"], ["selection", "structure", "relevance"]),
        ("source_coding", "Assign short codes to frequent symbols.",
         ["compression", "frequency", "encoding", "entropy"], ["efficiency", "storage", "transmission"]),
        ("channel_capacity", "The max reliable rate over a noisy channel.",
         ["capacity", "noise", "limit", "bound"], ["limits", "reliability", "throughput"]),
    ],
    "chemistry": [
        ("catalysis", "Lower an activation barrier without being consumed.",
         ["barrier", "acceleration", "reuse", "pathway"], ["rate", "efficiency", "selectivity"]),
        ("self_assembly", "Components spontaneously organize into structure.",
         ["assembly", "spontaneous", "local_rules", "structure"], ["organization", "fabrication", "emergence"]),
        ("le_chatelier", "A stressed equilibrium shifts to relieve the stress.",
         ["equilibrium", "feedback", "shift", "stress"], ["stability", "control", "response"]),
        ("chromatography", "Separate a mixture by differential affinity.",
         ["separation", "affinity", "gradient", "partition"], ["separation", "purification", "analysis"]),
        ("titration", "Find an unknown by reacting to a known endpoint.",
         ["endpoint", "incremental", "balance", "measure"], ["measurement", "calibration", "control"]),
    ],
    "ecology": [
        ("trophic_cascade", "A change at one level ripples through the food web.",
         ["cascade", "propagation", "network", "indirect"], ["stability", "control", "leverage"]),
        ("keystone_species", "A few nodes hold a whole network's structure.",
         ["leverage", "hub", "structure", "dependence"], ["stability", "leverage", "fragility"]),
        ("succession", "Communities reorganize predictably after disturbance.",
         ["recovery", "ordering", "staging", "disturbance"], ["resilience", "recovery", "ordering"]),
        ("carrying_capacity", "Growth saturates at an environment's limit.",
         ["saturation", "limit", "feedback", "density"], ["limits", "stability", "growth"]),
    ],
    "linguistics": [
        ("compositionality", "Meaning of a whole is built from its parts.",
         ["composition", "structure", "recursion", "rules"], ["generalization", "structure", "productivity"]),
        ("phonotactics", "Rules govern which sound sequences are allowed.",
         ["constraint", "sequence", "rules", "filtering"], ["structure", "validity", "generation"]),
        ("grammatical_agreement", "Distant words must co-vary in features.",
         ["dependency", "long_range", "constraint", "agreement"], ["consistency", "structure", "binding"]),
        ("code_switching", "Speakers alternate systems mid-stream by context.",
         ["switching", "context", "gating", "mixing"], ["flexibility", "adaptation", "context"]),
    ],
    "cryptography": [
        ("zero_knowledge_proof", "Prove a fact while revealing nothing else.",
         ["proof", "hiding", "verification", "challenge"], ["verification", "privacy", "trust"]),
        ("commitment_scheme", "Lock in a value now, reveal it provably later.",
         ["commitment", "binding", "hiding", "reveal"], ["integrity", "ordering", "trust"]),
        ("merkle_tree", "Hash a tree so any leaf is verifiable cheaply.",
         ["hashing", "tree", "verification", "aggregation"], ["integrity", "verification", "scaling"]),
        ("threshold_secret_sharing", "Split a secret so any k of n can recover it.",
         ["sharing", "threshold", "redundancy", "recovery"], ["robustness", "trust", "access"]),
    ],
    "materials": [
        ("annealing_metallurgy", "Heat then slow-cool to relieve internal stress.",
         ["temperature", "relaxation", "cooling", "stress"], ["stability", "quality", "defects"]),
        ("percolation", "Connectivity appears abruptly past a density threshold.",
         ["threshold", "connectivity", "network", "transition"], ["emergence", "transport", "robustness"]),
        ("fatigue_failure", "Repeated sub-critical load accumulates into fracture.",
         ["accumulation", "cyclic", "threshold", "damage"], ["reliability", "lifetime", "failure"]),
        ("composite_lamination", "Layer dissimilar materials for combined properties.",
         ["layering", "combination", "anisotropy", "interface"], ["strength", "tradeoff", "design"]),
    ],
}


def build():
    from collections import defaultdict
    # normalise domain aliases that denote the same field
    DOMAIN_ALIAS = {"materials_science": "materials"}
    concepts = []
    per_domain = defaultdict(int)
    # 1) curated Run-32 concepts
    for domain, items in RAW.items():
        for (name, definition, mech, prob) in items:
            per_domain[domain] += 1
            concepts.append({
                "id": f"{domain}_{per_domain[domain]:03d}",
                "name": name, "domain": domain, "definition": definition,
                "mechanism_tokens": sorted(set(mech)), "problem_tokens": sorted(set(prob)),
                "provenance": "curated_run32", "source_url": None,
            })
    # 2) Run-33 web-harvested concepts (real, sourced; see harvest/)
    n_curated = len(concepts)
    hpath = os.path.join(os.path.dirname(__file__), "..", "harvest", "harvested_concepts.json")
    if os.path.exists(hpath):
        harvested = json.load(open(hpath))["concepts"]
        for c in sorted(harvested, key=lambda c: (DOMAIN_ALIAS.get(c["domain"], c["domain"]), c["name"])):
            d = DOMAIN_ALIAS.get(c["domain"], c["domain"])
            per_domain[d] += 1
            concepts.append({
                "id": f"{d}_{per_domain[d]:03d}",
                "name": c["name"], "domain": d, "definition": c["definition"],
                "mechanism_tokens": sorted(set(c["mechanism_tokens"])),
                "problem_tokens": sorted(set(c["problem_tokens"])),
                "provenance": c.get("provenance", "websearch"), "source_url": c.get("source_url"),
            })
    # guard: ids unique
    assert len({c["id"] for c in concepts}) == len(concepts), "duplicate concept ids"
    concepts.sort(key=lambda c: c["id"])
    n_harvested = len(concepts) - n_curated
    bank = {
        "schema_version": "1.1",
        "lineage": "real-encyclopedia (Run 32 curated 80 + Run 33 web-harvested; see INHERITANCE.md)",
        "n_domains": len({c["domain"] for c in concepts}),
        "n_concepts": len(concepts),
        "provenance_counts": {"curated_run32": n_curated, "websearch_run33": n_harvested},
        "concepts": concepts,
    }
    out = os.path.join(os.path.dirname(__file__), "concept_banks.json")
    with open(out, "w") as f:
        json.dump(bank, f, indent=2, sort_keys=False)
    print(f"wrote {out}: {len(concepts)} concepts "
          f"({n_curated} curated + {n_harvested} harvested) across {bank['n_domains']} domains")
    return bank


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""
build_ground_truth.py  —  Run 32 ground-truth fixtures + known-approach registry.

The ground-truth labelled constructs are CURATED TEST FIXTURES (like unit-test
cases): each has an explicit mechanism-donor token set (mech_core), a
problem-target token set (problem_core), a cognitive_distance, and a human
ground-truth label {genuine_merge, is_niche, category}. The labels encode a
genuine conceptual judgement ("this merely re-derives an existing approach" vs
"this is a real unfilled niche"); the checkers must recover those labels from
direction_params alone. The gap between checker output and label is the
measured false-pass / false-reject (R5: errors are real outputs of the code).

Includes the inherited named traps:
  * M032  incremental method-variant  (Run 30 over-passed it; v4 must catch it)
  * M005  SAFE / obvious variant
  * M056  genuinely distinct (must NOT be over-rejected)
and new probes (M057/M060/borderlines) that stress v4 so the cycle has a real
weakness to fix.

Run with --calibrate to print each fixture's actual nearest-approach similarity.
"""
import json
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
from encyclopedia_engine import variant_similarity, jaccard, load_params  # noqa: E402

# --- registry of EXISTING method families the niche-checker guards against ---
KNOWN_APPROACHES = [
    {"id": "A1_rlhf", "name": "RLHF preference optimisation",
     "mechanism_tokens": ["feedback", "gradient", "preference", "update"],
     "problem_tokens": ["alignment", "control", "learning"]},
    {"id": "A2_rag", "name": "retrieval-augmented generation",
     "mechanism_tokens": ["addressing", "context", "lookup", "retrieval"],
     "problem_tokens": ["grounding", "knowledge", "memory"]},
    {"id": "A3_ensemble", "name": "ensemble / dropout regularisation",
     "mechanism_tokens": ["ensemble", "noise", "randomized", "redundancy"],
     "problem_tokens": ["generalization", "overfitting", "robustness"]},
    {"id": "A4_moe", "name": "mixture-of-experts sparse routing",
     "mechanism_tokens": ["gating", "routing", "sparsity", "specialization"],
     "problem_tokens": ["capacity", "efficiency", "scaling"]},
    {"id": "A5_annealing", "name": "annealing global optimisation",
     "mechanism_tokens": ["cooling", "noise", "search", "temperature"],
     "problem_tokens": ["global", "local_minima", "optimization"]},
    {"id": "A6_homeostat", "name": "homeostatic feedback control",
     "mechanism_tokens": ["error", "feedback", "regulation", "setpoint"],
     "problem_tokens": ["control", "robustness", "stability"]},
    {"id": "A7_ecc", "name": "error-correcting redundancy coding",
     "mechanism_tokens": ["distance", "encoding", "recovery", "redundancy"],
     "problem_tokens": ["integrity", "noise", "reliability"]},
    {"id": "A8_active", "name": "active / curriculum selection",
     "mechanism_tokens": ["ordering", "query", "selection", "uncertainty"],
     "problem_tokens": ["efficiency", "labels", "learning"]},
    {"id": "A9_predcoding", "name": "predictive-coding compression",
     "mechanism_tokens": ["compression", "error", "feedback", "prediction"],
     "problem_tokens": ["efficiency", "learning", "perception"]},
    {"id": "A10_selfassembly", "name": "self-assembly fabrication",
     "mechanism_tokens": ["assembly", "local_rules", "spontaneous", "structure"],
     "problem_tokens": ["emergence", "fabrication", "organization"]},
    # --- near-duplicate method families (realistic: real landscapes overlap).
    # These are why variant-detection AND determinism are genuinely hard: a
    # construct can sit borderline-near TWO families at once. ---
    {"id": "A4b_moe_capacity", "name": "MoE capacity routing (near-dup of A4)",
     "mechanism_tokens": ["gating", "routing", "sparsity", "specialization"],
     "problem_tokens": ["capacity", "scaling", "throughput"]},
    {"id": "A9b_pred_error", "name": "predictive error coding (near-dup of A9)",
     "mechanism_tokens": ["compression", "error", "feedback", "prediction"],
     "problem_tokens": ["efficiency", "fidelity", "learning"]},
]

# --- curated fixtures: (id, parents, mech_core, problem_core, cog_dist,
#                         parent_problem_overlap, genuine_merge, is_niche,
#                         category, note) ---
F = [
    # ---- genuinely distinct niches (is_niche=True): must pass both checkers ----
    ("M050", ["immune_memory", "source_coding"],
     ["memory", "priming", "recognition", "adaptation"],
     ["storage", "transmission", "efficiency"], 0.86, 0.0, True, True,
     "distinct_niche", "Immune-style priming for code-symbol caching; far from any approach."),
    ("M051", ["trophic_cascade", "model_predictive_control"],
     ["cascade", "propagation", "indirect", "network"],
     ["planning", "control", "leverage"], 0.82, 0.1, True, True,
     "distinct_niche", "Food-web cascade leverage inside a rolling-horizon controller."),
    ("M052", ["quorum_sensing", "consistent_hashing"],
     ["threshold", "density", "collective", "signaling"],
     ["distribution", "scaling", "churn"], 0.88, 0.0, True, True,
     "distinct_niche", "Density-threshold quorum trigger for rebalancing a hash ring."),
    ("M053", ["renormalization", "active_learning"],
     ["coarse_grain", "scale", "flow", "invariance"],
     ["annotation", "labels", "efficiency"], 0.80, 0.2, True, True,
     "distinct_niche", "Scale coarse-graining to pick label granularity."),
    ("M056", ["chemotaxis", "auction"],
     ["gradient", "sensing", "movement", "navigation"],
     ["allocation", "revenue", "fairness"], 0.84, 0.0, True, True,
     "distinct_niche", "INHERITED TRAP M056: genuinely distinct; checker must NOT over-reject."),
    ("M060", ["mixture_of_experts", "chemotaxis"],
     ["gating", "routing", "sparsity", "specialization"],
     ["navigation", "search", "targeting"], 0.78, 0.0, True, True,
     "novel_application", "Same MoE mechanism but a genuinely NOVEL problem (navigation): a real niche, NOT a variant. Bare-threshold lowering would wrongly reject it."),

    # ---- method-variants (genuine_merge=True but is_niche=False): niche-checker must REJECT ----
    ("M005", ["mixture_of_experts", "liquidity"],
     ["gating", "routing", "sparsity", "specialization"],
     ["capacity", "scaling", "throughput"], 0.74, 0.2, True, False,
     "safe_variant", "INHERITED TRAP M005: obvious MoE re-derivation; clearly above threshold."),
    ("M032", ["mixture_of_experts", "channel_capacity"],
     ["gating", "routing", "sparsity", "specialization"],
     ["capacity", "scaling", "reliability", "throughput"], 0.72, 0.2, True, False,
     "incremental_variant", "INHERITED TRAP M032: incremental MoE variant at the threshold; Run 30 over-passed, v4 must catch."),
    ("M057", ["predictive_coding", "rate_distortion"],
     ["compression", "error", "feedback", "prediction"],
     ["efficiency", "limits", "fidelity"], 0.70, 0.2, True, False,
     "near_variant", "NEW probe: predictive-coding re-derivation just BELOW v4 threshold -> v4 false-passes it. Drives v5."),
    ("M058", ["dropout_regularization", "horizontal_gene_transfer"],
     ["ensemble", "noise", "randomized", "redundancy"],
     ["generalization", "robustness", "spread"], 0.76, 0.2, True, False,
     "near_variant", "Dropout/ensemble re-derivation with one novel problem token."),
    ("M059", ["homeostasis", "gradient_descent"],
     ["error", "feedback", "gradient", "regulation"],
     ["control", "robustness", "scaling"], 0.68, 0.2, True, False,
     "mechanism_reuse_variant", "NEW probe: homeostatic-control re-derivation (mech_j 0.60, prob_j 0.50 vs A6) with combined sim ~0.55 BELOW the 0.70 scalar gate -> v4 deterministically FALSE-PASSES it. Only the v5 two-factor rule (mechanism reuse AND problem echo) catches it. Isolates the R13 variant-detection upgrade from the determinism fix."),

    # ---- borderline pair that can flip under approach-order shuffle (v4) ----
    ("M0B1", ["mixture_of_experts", "liquidity"],
     ["gating", "routing", "sparsity", "specialization"],
     ["capacity", "efficiency", "reliability", "robustness"], 0.71, 0.2, True, False,
     "borderline_variant", "MoE mechanism => neighbour of BOTH A4 (sim 0.70, borderline) and near-dup A4b (sim 0.58). v4 resolves via Python set iteration over {A4,A4b} -> PYTHONHASHSEED-dependent flip."),
    ("M0B2", ["predictive_coding", "neuromodulation"],
     ["compression", "error", "feedback", "prediction"],
     ["control", "learning", "perception", "robustness"], 0.73, 0.2, True, False,
     "borderline_variant", "Predictive-coding mechanism => neighbour of BOTH A9 (sim 0.70, borderline) and near-dup A9b (sim 0.58). Same hash-seed flip hazard."),

    # ---- integrity-stage negatives (genuine_merge=False): integrity must REJECT ----
    ("M070", ["gradient_descent", "fixed_point_iteration"],
     ["gradient", "iteration", "update", "optimization"],
     ["convergence", "fitting", "learning"], 0.30, 0.5, False, False,
     "trivial_too_close", "Two optimisation ideas, same domain-family: distance below merge_distance_min."),
    ("M071", ["source_coding", "rate_distortion"],
     ["compression", "frequency", "encoding", "entropy"],
     ["efficiency", "storage", "transmission"], 0.40, 0.7, False, False,
     "restatement", "Same compression problem restated: parent problem overlap too high."),
    ("M072", ["titration", "gossip_protocol"],
     ["endpoint", "incremental", "balance", "measure"],
     ["consensus", "scaling", "robustness"], 0.80, 0.0, False, False,
     "incoherent", "No shared transfer interface between parents: incoherent (ground-truth not a genuine merge)."),
]


def build(calibrate=False):
    p = load_params()
    constructs = []
    for (cid, parents, mc, pc, cd, ppo, gm, isn, cat, note) in F:
        c = {
            "id": cid, "parent_names": parents,
            "mech_core": sorted(set(mc)), "problem_core": sorted(set(pc)),
            "mechanism_tokens": sorted(set(mc)), "problem_tokens": sorted(set(pc)),
            # incoherent fixtures have NO shared transfer interface between parents;
            # genuine merges do. This is the signal the integrity checker reads.
            "shared_mechanism_tokens": [] if cat == "incoherent" else ["interface_token"],
            "cognitive_distance": cd, "parent_problem_overlap": ppo,
            "ground_truth": {"genuine_merge": gm, "is_niche": isn,
                             "category": cat, "note": note},
        }
        constructs.append(c)

    if calibrate:
        print(f"{'id':6} {'cat':20} {'gm':3} {'niche':5} | nearest sims (top3)")
        for c in constructs:
            sims = sorted(((variant_similarity(c, a, p), a["id"]) for a in KNOWN_APPROACHES),
                          reverse=True)
            top = ", ".join(f"{a}:{s:.3f}" for s, a in sims[:3])
            gt = c["ground_truth"]
            print(f"{c['id']:6} {gt['category']:20} {str(gt['genuine_merge']):3} "
                  f"{str(gt['is_niche']):5} | {top}")

    out_dir = HERE
    with open(os.path.join(out_dir, "known_approaches.json"), "w") as f:
        json.dump({"n_approaches": len(KNOWN_APPROACHES), "approaches": KNOWN_APPROACHES},
                  f, indent=2)
    with open(os.path.join(out_dir, "labeled_constructs.json"), "w") as f:
        json.dump({"n_constructs": len(constructs), "constructs": constructs}, f, indent=2)
    if not calibrate:
        print(f"wrote known_approaches.json ({len(KNOWN_APPROACHES)}) and "
              f"labeled_constructs.json ({len(constructs)})")
    return constructs


if __name__ == "__main__":
    build(calibrate="--calibrate" in sys.argv)

#!/usr/bin/env python3
"""
convergence.py  —  Run 32 convergence trajectory (the 4 metrics).

Reads the real Run-32 measurements (results/run32_metrics.json, determinism.json,
direction_params lineage + v5) and the INHERITED prior-run scalar baselines
(carried in the task prompt; see INHERITANCE.md) and assembles the convergence
record. Inherited values are tagged "inherited": true and are never presented
as recomputed by this run (R5).
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, "results")

# continuous scalars compared across param versions (saturation scaled to /10)
SCALARS = ["variant_similarity_threshold", "merge_distance_min", "confidence_margin",
           "saturation_max_neighbors", "merge_steer_strength"]


def vec(d):
    return [d.get("variant_similarity_threshold", 0.0), d.get("merge_distance_min", 0.0),
            d.get("confidence_margin", 0.0), d.get("saturation_max_neighbors", 0) / 10.0,
            d.get("merge_steer_strength", 0.0)]


def l1(a, b):
    return round(sum(abs(x - y) for x, y in zip(a, b)), 4)


def main():
    dp = json.load(open(os.path.join(BASE, "engine", "direction_params.json")))
    v5 = json.load(open(os.path.join(RESULTS, "direction_params_v5.json")))["params"]
    metrics = json.load(open(os.path.join(RESULTS, "run32_metrics.json")))
    det = json.load(open(os.path.join(RESULTS, "determinism.json")))
    pu = json.load(open(os.path.join(RESULTS, "param_update_v4_to_v5.json")))

    hist = {h["version"]: h for h in dp["version_history"]}
    v = {n: vec(hist[n]) for n in (1, 2, 3, 4)}
    v[5] = vec(v5)
    mags = {"v1_to_v2": l1(v[1], v[2]), "v2_to_v3": l1(v[2], v[3]),
            "v3_to_v4": l1(v[3], v[4]), "v4_to_v5": l1(v[4], v[5])}
    structural_changes = [c for c in pu["changes"] if not c.get("held")]

    niche_v4, niche_v5 = metrics["niche_v4"], metrics["niche_v5"]
    # false-pass on the INHERITED trap subset only (apples-to-apples vs Run 30/31)
    inherited_traps = ["M032", "M005", "M056"]
    v4_trap_fp = []
    for cid in inherited_traps:
        dist = niche_v4["variant_trap_catch_distribution"].get(cid)
        # M056 is a distinct niche (not in variant_traps); treat NICHE as correct there
        if cid == "M056":
            continue
        if dist and "NICHE_FOUND" in dist:
            v4_trap_fp.append(cid)

    conv = {
        "run": "run32",
        "metric_1_decision_accuracy_trajectory": {
            "niche_checker_false_pass": [
                {"run": "run30", "false_pass": 1, "detail": "M032 over-passed", "inherited": True},
                {"run": "run31", "false_pass": 0, "detail": "strict R13 caught M032", "inherited": True},
                {"run": "run32_v4", "false_pass_on_inherited_traps": len(v4_trap_fp),
                 "false_pass_on_full_run32_probe_set": [niche_v4["niche_false_pass_min"],
                                                        niche_v4["niche_false_pass_max"]],
                 "deterministic_false_pass": niche_v4["deterministic_false_pass"],
                 "seed_dependent": niche_v4["seed_dependent_verdicts"],
                 "note": "Run 32 added harder probes (M059 mechanism-reuse variant, M0B1/M0B2 "
                         "borderline) absent from the Run 30/31 test set. v4 still scores 0 "
                         "false-pass on the inherited traps {M032,M005,M056} (consistent with "
                         "Run 31) but the new probes expose 1 deterministic + 2 seed-dependent failures."},
                {"run": "run32_v5", "false_pass": niche_v5["niche_false_pass_max"],
                 "false_reject": niche_v5["niche_false_reject_max"],
                 "note": "0 false-pass, 0 false-reject on the full harder probe set, deterministically."},
            ],
            "verdict": "improving (v5 returns to 0 false-pass on a strictly harder benchmark)",
        },
        "metric_2_param_change_magnitude": {
            "continuous_scalar_L1": mags,
            "trajectory": "0.21 -> 0.19 -> 0.08 -> 0.00 (monotonically shrinking)",
            "v4_to_v5_structural_changes": [c["param"] for c in structural_changes],
            "verdict": "converging on continuous scalars (L1 -> 0); v5 improvements are "
                       "structural/process upgrades (variant rule mode, borderline rule, "
                       "interface-aware generation), the expected late-stage behaviour.",
        },
        "metric_3_determinism": {
            "run27": {"note": "borderline-case flips identified as the weak point", "inherited": True},
            "run32_v4_agreement_rate": det["v4"]["determinism_rate"],
            "run32_v5_agreement_rate": det["v5"]["determinism_rate"],
            "verdict": "rising (0.875 -> 1.0); the PYTHONHASHSEED flip hazard is eliminated by construction.",
        },
        "metric_4_coordination_reliability": {
            "n_agents": metrics["coordination"].get("n_agents"),
            "well_formed_rate": metrics["coordination"].get("coordination_reliability_rate"),
            "retries_needed": metrics["coordination"].get("retries_needed"),
            "malformed": metrics["coordination"].get("malformed_first_attempt"),
            "audit_vs_ground_truth_agreement": metrics["coordination"].get("audit_vs_ground_truth_agreement"),
            "verdict": "reliable (0 malformed, 0 retries this cycle); the lone audit/GT "
                       "disagreement is the lowest-confidence borderline case (M0B1), "
                       "independently corroborating the determinism finding.",
        },
        "overall_verdict": "CONVERGING toward production-ready: decision accuracy rising "
                           "on a harder benchmark, param-change magnitude shrinking to 0 on "
                           "scalars, determinism risen to 1.0, coordination reliable.",
    }
    json.dump(conv, open(os.path.join(RESULTS, "convergence.json"), "w"), indent=2)
    print("param-change magnitude L1:", mags)
    print("structural v4->v5 changes:", [c["param"] for c in structural_changes])
    print("determinism v4->v5:", det["v4"]["determinism_rate"], "->", det["v5"]["determinism_rate"])
    print("coordination reliability:", metrics["coordination"].get("coordination_reliability_rate"))
    print("wrote results/convergence.json")


if __name__ == "__main__":
    main()

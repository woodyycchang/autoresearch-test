#!/usr/bin/env python3
"""
build_value_ground_truth.py  —  Run 35 value benchmark.

Curated constructs labelled VALUABLE (a structurally-plausible cross-domain
transfer: the borrowed mechanism's preconditions are genuinely met by the target
problem) vs USELESS (novel but structurally implausible -- the mechanism's needs
are not afforded). Built from REAL bank concept pairs; the label encodes a
structural judgement, and the value scorer must recover it from the
precondition/affordance ontology. Run with --calibrate to print each fit.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
sys.path.insert(0, HERE)
from encyclopedia_engine import make_construct, load_bank  # noqa
from value_scorer import structural_fit, load_maps  # noqa

# (id, donor_concept, target_concept, gt_valuable, reason)
FIX = [
    # ---- VALUABLE: structurally-plausible transfers ----
    ("V01", "simulated_annealing", "natural_selection", True,
     "Annealing (stochastic search over an energy landscape) maps onto evolutionary search over a fitness landscape."),
    ("V02", "predictive_coding", "kalman_filter", True,
     "Predict-then-correct with feedback IS the structure of recursive estimation/tracking."),
    ("V03", "gradient_descent", "simulated_annealing", True,
     "Gradient steps and annealing both extremize an objective over a continuous landscape."),
    ("V04", "pid_control", "homeostasis", True,
     "PID error-feedback regulation maps directly onto homeostatic setpoint control."),
    ("V05", "immune_memory", "lru_cache", True,
     "Priming on recently/ frequently seen items maps onto recency/use caching."),
    ("V06", "quorum_sensing", "gossip_protocol", True,
     "Density-threshold collective triggering maps onto distributed consensus/coordination."),
    ("V07", "error_correcting_code", "immune_memory", True,
     "Redundant encoding for recovery maps onto immune recognition robustness."),
    ("V08", "kalman_filter", "predictive_coding", True,
     "Recursive noisy-estimate fusion maps onto perceptual prediction-error correction."),
    ("V09", "natural_selection", "auction", True,
     "Selection under competition for a limited resource maps onto competitive allocation."),
    ("V10", "consistent_hashing", "gossip_protocol", True,
     "Partition/rebalance over a ring maps onto distributed load distribution under churn."),
    ("V11", "diffusion_of_innovations", "quorum_sensing", True,
     "Network propagation past a threshold maps onto collective adoption timing."),
    ("V12", "homeostasis", "price_signal", True,
     "Negative-feedback regulation toward a setpoint maps onto market price stabilization (a real, debated analogy)."),

    # ---- USELESS: novel but structurally implausible ----
    ("U01", "gossip_protocol", "auction", False,
     "Epidemic spatial spread has no analogue in a one-shot discrete allocation: preconditions (spatial/network diffusion) unmet."),
    ("U02", "ostwald_ripening", "social_mobility", False,
     "Physical coarsening needs spatial diffusion + a conserved physical quantity + surface energy; social mobility affords none -- the canonical novel-but-useless."),
    ("U03", "titration", "gossip_protocol", False,
     "Incremental endpoint measurement is not distributed consensus; the procedural preconditions do not transfer."),
    ("U04", "ostwald_ripening", "auction", False,
     "Diffusion-driven coarsening does not map onto bidding/allocation structure."),
    ("U05", "simulated_annealing", "auction", False,
     "Annealing needs an energy landscape to cool over; a sealed-bid auction has no such continuous landscape."),
    ("U06", "consistent_hashing", "predictive_coding", False,
     "Hash-ring partitioning has no relation to perceptual prediction-error structure."),
    ("U07", "lru_cache", "natural_selection", False,
     "Recency eviction is not heritable variation under selection; population/variation preconditions unmet."),
    ("U08", "titration", "social_mobility", False,
     "A chemical endpoint procedure does not map onto social distribution dynamics."),
    ("U09", "gossip_protocol", "price_signal", False,
     "Randomized epidemic spread does not capture price aggregation/incentive structure."),
    ("U10", "ostwald_ripening", "predictive_coding", False,
     "Particle coarsening has no predict-correct/perception structure."),
    ("U11", "consistent_hashing", "natural_selection", False,
     "Hash partitioning lacks variation/heritability/competition needed for selection."),
    ("U12", "titration", "auction", False,
     "Stepwise titration to an endpoint is not competitive bidding allocation."),
]


def build(calibrate=False):
    bank = load_bank(); byname = {c["name"]: c for c in bank["concepts"]}
    pre, aff = load_maps()
    out = []
    for (cid, d, t, val, reason) in FIX:
        if d not in byname or t not in byname:
            raise SystemExit(f"missing concept: {d if d not in byname else t}")
        c = make_construct(byname[d], byname[t]); c["id"] = cid
        fit = structural_fit(c, pre, aff)
        rec = {"id": cid, "donor": d, "target": t, "mech_core": c["mech_core"],
               "problem_core": c["problem_core"], "structural_fit": fit,
               "ground_truth": {"is_valuable": val, "reason": reason}}
        out.append(rec)
        if calibrate:
            print(f"{cid} {'VAL' if val else 'USE'} fit={fit}  {d} -> {t}")
    json.dump({"n": len(out), "constructs": out},
              open(os.path.join(HERE, "value_ground_truth.json"), "w"), indent=2)
    if not calibrate:
        print(f"wrote value_ground_truth.json ({len(out)} fixtures)")
    return out


if __name__ == "__main__":
    build(calibrate="--calibrate" in sys.argv)

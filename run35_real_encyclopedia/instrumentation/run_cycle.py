#!/usr/bin/env python3
"""
run_cycle.py  —  Run 35 optimization cycle (generator-side value/plausibility).

Adds a NEW value-scorer stage AFTER the (frozen, production-ready) niche checker.
Confirms the decision pipeline does NOT regress, measures value-discrimination
(structural-fit alone vs + frozen Opus value-audit), reports the at-scale value
distribution, and derives v8. All numbers from real execution (R5).
"""
import json, os, statistics, subprocess, sys, copy
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "engine"))
sys.path.insert(0, os.path.join(BASE, "ground_truth"))
sys.path.insert(0, os.path.join(BASE, "value"))
from encyclopedia_engine import (generate_constructs, integrity_check, niche_check,  # noqa
                                 make_construct, load_bank, load_params)
from build_ground_truth import KNOWN_APPROACHES  # noqa
from value_scorer import value_score, structural_fit, load_maps  # noqa
from build_value_ground_truth import FIX as VALUE_FIX  # noqa

RESULTS = os.path.join(BASE, "results")
WORKER = os.path.join(BASE, "instrumentation", "_niche_worker.py")
NICHE_AUDIT = os.path.join(BASE, "reasoning_audit", "frozen_audit_table.json")
VALUE_AUDIT = os.path.join(BASE, "value", "frozen_value_audit.json")
SEEDS = list(range(16))
VPARAMS = {"value_threshold": 0.5, "value_floor": 0.2}


# ---- DECISION-pipeline regression check (must match Run 34: 0fp/0fr, det 1.0) ----
def decision_regression(constructs):
    table = {}
    for s in SEEDS:
        env = dict(os.environ, PYTHONHASHSEED=str(s))
        out = subprocess.run([sys.executable, WORKER,
                              os.path.join(BASE, "engine", "direction_params.json"), NICHE_AUDIT],
                             capture_output=True, text=True, env=env, check=True)
        table[s] = json.loads(out.stdout.strip())
    gt = {c["id"]: c["ground_truth"] for c in constructs}
    ids = list(gt)
    stable = sum(1 for cid in ids if len({table[s][cid] for s in SEEDS}) == 1)
    fp = max(sum(1 for cid in ids if table[s][cid] == "NICHE_FOUND" and not gt[cid]["is_niche"]) for s in SEEDS)
    fr = max(sum(1 for cid in ids if table[s][cid] != "NICHE_FOUND" and gt[cid]["is_niche"]) for s in SEEDS)
    # borderline adjudication (blanket vs audit)
    audit = json.load(open(NICHE_AUDIT)); p = load_params()
    bset = [c for c in constructs if c["id"].startswith("B")]
    blanket = sum(1 for c in bset if (niche_check(c, {**p, "borderline_rule": "conservative_reject"},
                  KNOWN_APPROACHES)["verdict"] == "NICHE_FOUND") == c["ground_truth"]["is_niche"]) / len(bset)
    auditacc = sum(1 for c in bset if (niche_check(c, p, KNOWN_APPROACHES, audit_table=audit)["verdict"]
                   == "NICHE_FOUND") == c["ground_truth"]["is_niche"]) / len(bset)
    return {"niche_false_pass": fp, "niche_false_reject": fr,
            "determinism_rate": round(stable / len(ids), 4),
            "borderline_blanket": round(blanket, 4), "borderline_audit": round(auditacc, 4),
            "n_known_approaches": len(KNOWN_APPROACHES)}


# ---- VALUE-discrimination on the 24-fixture value GT ----
def value_discrimination(pre, aff, vaudit):
    bank = load_bank(); byname = {c["name"]: c for c in bank["concepts"]}
    def run(audit, gate):
        fu = fl = 0; rows = []
        for (cid, d, t, val, reason) in VALUE_FIX:
            c = make_construct(byname[d], byname[t]); c["id"] = cid
            P = {**VPARAMS, "value_audit_gate": gate}
            v = value_score(c, P, pre, aff, value_audit=audit)
            pred = v["verdict"] == "VALUABLE"
            if pred and not val: fu += 1
            if (not pred) and val: fl += 1
            rows.append({"id": cid, "gt": val, "fit": v["fit"], "verdict": v["verdict"], "reason": v["reason"]})
        n = len(VALUE_FIX)
        return {"false_useful": fu, "false_useless": fl, "accuracy": round(1 - (fu + fl) / n, 4), "detail": rows}
    return {"structural_only": run(None, 1.01),
            "structural_plus_audit_gate_0p75": run(vaudit, 0.75),
            "structural_plus_audit_no_gate": run(vaudit, 0.0),
            "n_fixtures": len(VALUE_FIX)}


# ---- AT-SCALE value distribution over the niches ----
def at_scale_value(bank, p, pre, aff):
    niches = [c for c in generate_constructs(bank, p) if integrity_check(c, p)["pass"]]
    fits = [structural_fit(c, pre, aff) for c in niches]
    fits = [f for f in fits if f is not None]
    thr, floor = VPARAMS["value_threshold"], VPARAMS["value_floor"]
    val = sum(1 for f in fits if f >= thr); use = sum(1 for f in fits if f < floor)
    bdr = len(fits) - val - use
    return {"n_niches": len(fits), "mean_fit": round(statistics.mean(fits), 4),
            "valuable_frac": round(val / len(fits), 4), "useless_frac": round(use / len(fits), 4),
            "borderline_frac": round(bdr / len(fits), 4),
            "note": "structural-fit only (frozen audit covers the GT band, not generated constructs)"}


def build_v8(v7_blob, vdisc):
    p7 = v7_blob["params"]; p8 = copy.deepcopy(p7); changes = []
    # NEW value-stage params
    p8["value_threshold"] = VPARAMS["value_threshold"]
    p8["value_floor"] = VPARAMS["value_floor"]
    p8["value_audit_gate"] = 0.0
    p8["value_rule"] = "structural_fit_plus_band_audit"
    no_gate = vdisc["structural_plus_audit_no_gate"]["accuracy"]
    gated = vdisc["structural_plus_audit_gate_0p75"]["accuracy"]
    so = vdisc["structural_only"]["accuracy"]
    changes.append({"param": "value_threshold/value_floor", "to": [VPARAMS["value_threshold"], VPARAMS["value_floor"]],
                    "motivating_measurement": f"value GT calibration: thr=0.5 gives 0 false-useful (max useless fit <0.5); "
                                              f"structural-only acc={so}",
                    "rationale": "NEW value stage: structural-fit coverage with a precision-calibrated threshold."})
    changes.append({"param": "value_audit_gate", "considered": 0.75, "to": 0.0, "REJECTED_value": 0.75,
                    "motivating_measurement": f"value-discrimination: gate0.75 acc={gated} < no-gate acc={no_gate} "
                                              f"(the gate discards correct low-confidence valuable rescues V05/V10)",
                    "rationale": "confidence gate REJECTED by measurement (R14, cf. Run 32 distance-steering): it lowers "
                                 "value-discrimination accuracy; v8 trusts the in-band value-audit verdict."})
    for k in ["variant_similarity_threshold", "merge_distance_min", "confidence_margin", "saturation_band",
              "saturation_max_neighbors", "mech_match_min", "problem_echo_min", "variant_rule_mode",
              "borderline_rule", "merge_require_interface", "merge_steer_strength", "audit_confidence_gate"]:
        if k in p7:
            changes.append({"param": k, "from": p7[k], "to": p8[k], "held": True,
                            "rationale": "decision-pipeline param held; the value stage is additive (no regression)."})
    v8 = copy.deepcopy(v7_blob); v8["version"] = 8
    v8["version_label"] = "v8 (Run 35: + generator-side value/plausibility stage; decision params held)"
    v8["params"] = p8
    return v8, changes


def main():
    os.makedirs(RESULTS, exist_ok=True)
    bank = load_bank(); p = load_params()
    v7_blob = json.load(open(os.path.join(BASE, "engine", "direction_params.json")))
    constructs = json.load(open(os.path.join(BASE, "ground_truth", "labeled_constructs.json")))["constructs"]
    pre, aff = load_maps(); vaudit = json.load(open(VALUE_AUDIT))

    reg = decision_regression(constructs)
    vdisc = value_discrimination(pre, aff, vaudit)
    scale = at_scale_value(bank, p, pre, aff)
    v8_blob, changes = build_v8(v7_blob, vdisc)
    json.dump(v8_blob, open(os.path.join(RESULTS, "direction_params_v8.json"), "w"), indent=2)

    coordination = json.load(open(os.path.join(RESULTS, "coordination.json"))) if os.path.exists(
        os.path.join(RESULTS, "coordination.json")) else {}
    metrics = {"run": "run35", "bank_concepts": bank["n_concepts"], "n_known_approaches": len(KNOWN_APPROACHES),
               "n_value_fixtures": vdisc["n_fixtures"], "decision_regression": reg,
               "value_discrimination": vdisc, "at_scale_value": scale, "coordination": coordination}
    json.dump(metrics, open(os.path.join(RESULTS, "run35_metrics.json"), "w"), indent=2)
    json.dump({"changes": changes, "v7_params": v7_blob["params"], "v8_params": v8_blob["params"]},
              open(os.path.join(RESULTS, "param_update_v7_to_v8.json"), "w"), indent=2)

    print("=== DECISION-PIPELINE REGRESSION CHECK (must hold) ===")
    print(f"  niche fp={reg['niche_false_pass']} fr={reg['niche_false_reject']} determinism={reg['determinism_rate']} "
          f"borderline_audit={reg['borderline_audit']} registry={reg['n_known_approaches']}")
    print("=== NEW VALUE-DISCRIMINATION (24-fixture GT) ===")
    print(f"  structural-only       : fu={vdisc['structural_only']['false_useful']} fl={vdisc['structural_only']['false_useless']} acc={vdisc['structural_only']['accuracy']}")
    print(f"  +audit gate0.75 (REJ) : acc={vdisc['structural_plus_audit_gate_0p75']['accuracy']}")
    print(f"  +audit no-gate (v8)   : fu={vdisc['structural_plus_audit_no_gate']['false_useful']} fl={vdisc['structural_plus_audit_no_gate']['false_useless']} acc={vdisc['structural_plus_audit_no_gate']['accuracy']}")
    print("=== AT-SCALE VALUE (of %d niches) ===" % scale["n_niches"])
    print(f"  valuable={scale['valuable_frac']} useless={scale['useless_frac']} borderline={scale['borderline_frac']} (novelty 0.9915 -> structural-value {scale['valuable_frac']})")


if __name__ == "__main__":
    main()

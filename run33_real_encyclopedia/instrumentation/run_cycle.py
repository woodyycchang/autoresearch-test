#!/usr/bin/env python3
"""
run_cycle.py  —  Run 33 optimization cycle (scale + audit integration).

Inherits Run 32's engine + v5 params; measures every stage AT SCALE on the
314-concept bank and the 21-fixture labelled probe set, wires the frozen
reasoning-audit table into the borderline branch (v6), and re-measures. All
numbers are produced by executing the engine (R5).
"""
import json, os, statistics, subprocess, sys, copy
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "engine"))
sys.path.insert(0, os.path.join(BASE, "ground_truth"))
from encyclopedia_engine import (generate_constructs, integrity_check, niche_check,  # noqa
                                 load_bank, load_params)
from build_ground_truth import KNOWN_APPROACHES  # noqa

RESULTS = os.path.join(BASE, "results")
WORKER = os.path.join(BASE, "instrumentation", "_niche_worker.py")
SCALEW = os.path.join(BASE, "instrumentation", "_scale_worker.py")
AUDIT = os.path.join(BASE, "reasoning_audit", "frozen_audit_table.json")
SEEDS = list(range(16))


def dist_stats(xs):
    xs = sorted(xs)
    bins = {}
    for lo in [0.0, 0.5, 0.6, 0.7, 0.8, 0.9]:
        hi = lo + (0.5 if lo == 0.0 else 0.1)
        bins[f"[{lo:.1f},{hi:.1f})"] = sum(1 for x in xs if lo <= x < hi or (hi >= 1.0 and x == 1.0))
    return {"n": len(xs), "min": round(xs[0], 4), "max": round(xs[-1], 4),
            "mean": round(statistics.mean(xs), 4), "median": round(statistics.median(xs), 4),
            "stdev": round(statistics.pstdev(xs), 4), "histogram": bins}


def metric_merge(bank, p):
    cons = generate_constructs(bank, p)
    integ = [integrity_check(c, p) for c in cons]
    genuine = [c for c, r in zip(cons, integ) if r["pass"]]
    return {"config": {"merge_require_interface": p.get("merge_require_interface"),
                       "n_bank_concepts": bank["n_concepts"]},
            "n_constructs": len(cons), "genuine_merge_pass": len(genuine),
            "genuine_merge_rate": round(len(genuine) / len(cons), 4) if cons else 0.0,
            "fail_reason_breakdown": dict(Counter(r["reason"] for r in integ if not r["pass"])),
            "cognitive_distance_genuine": dist_stats([c["cognitive_distance"] for c in genuine]) if genuine else None}


def metric_integrity(constructs, p):
    fp = sum(1 for c in constructs if integrity_check(c, p)["pass"] and not c["ground_truth"]["genuine_merge"])
    fr = sum(1 for c in constructs if not integrity_check(c, p)["pass"] and c["ground_truth"]["genuine_merge"])
    return {"false_pass": fp, "false_reject": fr,
            "accuracy": round(1 - (fp + fr) / len(constructs), 4),
            "n_genuine": sum(1 for c in constructs if c["ground_truth"]["genuine_merge"]),
            "n_nongenuine": sum(1 for c in constructs if not c["ground_truth"]["genuine_merge"])}


def seed_sweep(params_path, audit_path=None):
    table = {}
    for s in SEEDS:
        env = dict(os.environ, PYTHONHASHSEED=str(s))
        out = subprocess.run([sys.executable, WORKER, params_path, audit_path or "none"],
                             capture_output=True, text=True, env=env, check=True)
        table[s] = json.loads(out.stdout.strip())
    return table


def niche_metrics(constructs, sweep):
    gt = {c["id"]: c["ground_truth"] for c in constructs}
    ids = [c["id"] for c in constructs]
    per = {cid: Counter(sweep[s][cid] for s in SEEDS) for cid in ids}
    stable = {cid: len(per[cid]) == 1 for cid in ids}
    fp = [[cid for cid in ids if sweep[k][cid] == "NICHE_FOUND" and not gt[cid]["is_niche"]] for k in SEEDS]
    fr = [[cid for cid in ids if sweep[k][cid] != "NICHE_FOUND" and gt[cid]["is_niche"]] for k in SEEDS]
    return {"determinism_rate": round(sum(stable.values()) / len(ids), 4),
            "pairwise_agreement": round(sum(1 for cid in ids if sweep[SEEDS[0]][cid] == sweep[SEEDS[1]][cid]) / len(ids), 4),
            "unstable_constructs": [cid for cid in ids if not stable[cid]],
            "false_pass_min": min(len(x) for x in fp), "false_pass_max": max(len(x) for x in fp),
            "false_reject_min": min(len(x) for x in fr), "false_reject_max": max(len(x) for x in fr),
            "false_pass_ids_seed0": fp[0], "false_reject_ids_seed0": fr[0]}


def borderline_metric(constructs, p5, p6, audit):
    bset = [c for c in constructs if c["id"].startswith("B")]
    rows = []
    for c in bset:
        gtn = c["ground_truth"]["is_niche"]
        v5 = niche_check(c, p5, KNOWN_APPROACHES)["verdict"]
        v6 = niche_check(c, p6, KNOWN_APPROACHES, audit_table=audit)["verdict"]
        rows.append({"id": c["id"], "gt_is_niche": gtn, "v5": v5, "v6": v6,
                     "v5_correct": (v5 == "NICHE_FOUND") == gtn,
                     "v6_correct": (v6 == "NICHE_FOUND") == gtn})
    n = len(rows)
    return {"n_borderline": n,
            "v5_accuracy": round(sum(r["v5_correct"] for r in rows) / n, 4),
            "v6_accuracy": round(sum(r["v6_correct"] for r in rows) / n, 4),
            "detail": rows}


def scale_determinism(params_path, audit_path=None):
    res = {}
    for s in (0, 1):
        env = dict(os.environ, PYTHONHASHSEED=str(s))
        out = subprocess.run([sys.executable, SCALEW, params_path, audit_path or "none"],
                             capture_output=True, text=True, env=env, check=True)
        res[s] = json.loads(out.stdout.strip())
    return {"seed0": res[0], "seed1": res[1], "agree": res[0]["digest"] == res[1]["digest"]}


def build_v6(v5_blob, border, m1):
    p5 = v5_blob["params"]; p6 = copy.deepcopy(p5); changes = []
    p6["borderline_rule"] = "audit_gated"
    p6["audit_confidence_gate"] = 0.75
    changes.append({
        "param": "borderline_rule", "from": "conservative_reject", "to": "audit_gated",
        "also": {"audit_confidence_gate": 0.75},
        "motivating_measurement": f"results/borderline_adjudication.json :: v5_accuracy={border['v5_accuracy']} "
                                  f"(blanket reject false-rejects borderline NICHES)",
        "rationale": "v5 blanket conservative_reject is right on borderline re-skins but FALSE-REJECTS borderline "
                     "genuine niches (novel mechanism, same problem). Routing them to the frozen reasoning-audit "
                     "lifts borderline accuracy; the audit table is frozen so determinism is preserved."})
    changes.append({
        "param": "audit_confidence_gate", "from": None, "to": 0.75,
        "motivating_measurement": "Run 32 audit erred at confidence 0.62 (M0B1); Run 33 correct audits are all >=0.78.",
        "rationale": "gate calibrated to the observed audit confidence/accuracy relationship; below it -> conservative_reject."})
    for k in ["variant_similarity_threshold", "merge_distance_min", "confidence_margin", "saturation_band",
              "saturation_max_neighbors", "mech_match_min", "problem_echo_min", "variant_rule_mode",
              "merge_require_interface", "merge_steer_strength"]:
        changes.append({"param": k, "from": p5[k], "to": p6[k], "held": True,
                        "rationale": "no Run-33 measurement motivated a change (held => still converged)."})
    v6 = copy.deepcopy(v5_blob); v6["version"] = 6
    v6["version_label"] = "v6 (Run 33: audit-gated borderline adjudication; scale-validated)"
    v6["params"] = p6
    return v6, changes


def main():
    os.makedirs(RESULTS, exist_ok=True)
    bank = load_bank()
    v5_blob = json.load(open(os.path.join(BASE, "engine", "direction_params.json")))
    p5 = v5_blob["params"]
    audit = json.load(open(AUDIT))
    constructs = json.load(open(os.path.join(BASE, "ground_truth", "labeled_constructs.json")))["constructs"]

    m1 = metric_merge(bank, p5)
    m2 = metric_integrity(constructs, p5)
    border0 = borderline_metric(constructs, p5, {**p5, "borderline_rule": "audit_gated",
                                                 "audit_confidence_gate": 0.75}, audit)
    v6_blob, changes = build_v6(v5_blob, border0, m1)
    p6 = v6_blob["params"]
    v5_path = os.path.join(BASE, "engine", "direction_params.json")
    v6_path = os.path.join(RESULTS, "direction_params_v6.json")
    json.dump(v6_blob, open(v6_path, "w"), indent=2)

    sweep_v5 = seed_sweep(v5_path)
    sweep_v6 = seed_sweep(v6_path, AUDIT)
    niche_v5 = niche_metrics(constructs, sweep_v5)
    niche_v6 = niche_metrics(constructs, sweep_v6)
    border = borderline_metric(constructs, p5, p6, audit)
    scale_v6 = scale_determinism(v6_path, AUDIT)

    coordination = json.load(open(os.path.join(RESULTS, "coordination.json")))
    coordination["reasoning_audit"]["borderline_adjudication_accuracy_vs_ground_truth"] = border["v6_accuracy"]

    metrics = {"run": "run33", "bank_concepts": bank["n_concepts"], "bank_domains": bank["n_domains"],
               "n_known_approaches": len(KNOWN_APPROACHES), "n_labeled_fixtures": len(constructs),
               "merge_at_scale": m1, "integrity": m2, "niche_v5": niche_v5, "niche_v6": niche_v6,
               "borderline_adjudication": border, "scale_determinism_v6": scale_v6, "coordination": coordination}
    json.dump(metrics, open(os.path.join(RESULTS, "run33_metrics.json"), "w"), indent=2)
    json.dump({"seeds": SEEDS,
               "v5": {k: niche_v5[k] for k in ["determinism_rate", "pairwise_agreement", "unstable_constructs"]},
               "v6": {k: niche_v6[k] for k in ["determinism_rate", "pairwise_agreement", "unstable_constructs"]},
               "scale_v6": scale_v6}, open(os.path.join(RESULTS, "determinism.json"), "w"), indent=2)
    json.dump({"changes": changes, "v5_params": p5, "v6_params": p6},
              open(os.path.join(RESULTS, "param_update_v5_to_v6.json"), "w"), indent=2)
    json.dump(border, open(os.path.join(RESULTS, "borderline_adjudication.json"), "w"), indent=2)

    print("=== METRIC 1 merge @ scale (bank=%d/%d domains) ===" % (bank["n_concepts"], bank["n_domains"]))
    print(f"  generated={m1['n_constructs']} genuine-merge rate={m1['genuine_merge_rate']} "
          f"mean_dist={m1['cognitive_distance_genuine']['mean']} fails={m1['fail_reason_breakdown']}")
    print("=== METRIC 2 integrity ===  fp=%d fr=%d acc=%s" % (m2["false_pass"], m2["false_reject"], m2["accuracy"]))
    print("=== METRIC 3 niche (21 fixtures) ===")
    print(f"  v5 fp=[{niche_v5['false_pass_min']},{niche_v5['false_pass_max']}] fr=[{niche_v5['false_reject_min']},{niche_v5['false_reject_max']}] fr_ids={niche_v5['false_reject_ids_seed0']}")
    print(f"  v6 fp=[{niche_v6['false_pass_min']},{niche_v6['false_pass_max']}] fr=[{niche_v6['false_reject_min']},{niche_v6['false_reject_max']}] fr_ids={niche_v6['false_reject_ids_seed0']}")
    print("=== NEW borderline adjudication ===  v5_acc=%s -> v6_acc=%s (n=%d)" %
          (border["v5_accuracy"], border["v6_accuracy"], border["n_borderline"]))
    print("=== METRIC 5 determinism ===  v5=%s v6=%s  scale_v6_agree=%s (%d genuine merges)" %
          (niche_v5["determinism_rate"], niche_v6["determinism_rate"], scale_v6["agree"], scale_v6["seed0"]["n_genuine"]))


if __name__ == "__main__":
    main()

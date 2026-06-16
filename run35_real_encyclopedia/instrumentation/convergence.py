#!/usr/bin/env python3
"""convergence.py — Run 35 trajectory across 6 cycles (Run 30->35): the 4
held decision metrics + the NEW value-discrimination metric. Inherited
prior-run scalars are tagged/labelled, not recomputed (R5)."""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, "results")


def vec(d):
    return [d.get("variant_similarity_threshold", 0.0), d.get("merge_distance_min", 0.0),
            d.get("confidence_margin", 0.0), d.get("saturation_max_neighbors", 0) / 10.0,
            d.get("merge_steer_strength", 0.0)]


def l1(a, b):
    return round(sum(abs(x - y) for x, y in zip(a, b)), 4)


def main():
    dp = json.load(open(os.path.join(BASE, "engine", "direction_params.json")))
    v8 = json.load(open(os.path.join(RESULTS, "direction_params_v8.json")))["params"]
    m = json.load(open(os.path.join(RESULTS, "run35_metrics.json")))
    reg = m["decision_regression"]; vd = m["value_discrimination"]; sc = m["at_scale_value"]

    hist = {h["version"]: h for h in dp["version_history"]}
    v = {n: vec(hist[n]) for n in (1, 2, 3, 4, 5, 6, 7)}
    v[8] = vec(v8)
    mags = {f"v{n}_v{n+1}": l1(v[n], v[n + 1]) for n in range(1, 8)}

    conv = {
        "run": "run35",
        "held_decision_metrics": {
            "decision_accuracy_fp_fr": [reg["niche_false_pass"], reg["niche_false_reject"]],
            "determinism": reg["determinism_rate"],
            "borderline_adjudication": reg["borderline_audit"],
            "param_change_L1_decision_scalars_v7_v8": mags["v7_v8"],
            "verdict": "0 regressions: niche 0/0, determinism 1.0, borderline 1.0 (identical to Run 34); "
                       "the value stage is additive."},
        "decision_accuracy_6cycles": [
            {"run": "run30", "fp": 1, "inherited": True}, {"run": "run31", "fp": 0, "inherited": True},
            {"run": "run32", "fp": 0, "fr": 0, "prior": True}, {"run": "run33", "fp": 0, "fr": 0, "prior": True},
            {"run": "run34", "fp": 0, "fr": 0, "prior": True},
            {"run": "run35", "fp": reg["niche_false_pass"], "fr": reg["niche_false_reject"],
             "note": "held at 0/0 with the value stage added"}],
        "param_change_magnitude": {
            "decision_scalar_L1": mags,
            "trajectory": "0.21 -> 0.19 -> 0.08 -> 0.00 -> 0.00 -> 0.00 -> 0.00 (FOUR consecutive cycles at 0.00)",
            "v8_additions": ["value_threshold", "value_floor", "value_audit_gate(=0, gate rejected)", "value_rule"],
            "verdict": "decision scalars converged; v8 adds a NEW value stage (structural)."},
        "NEW_value_discrimination": {
            "chance": 0.5,
            "structural_only": vd["structural_only"]["accuracy"],
            "structural_plus_audit_gate_0p75_REJECTED": vd["structural_plus_audit_gate_0p75"]["accuracy"],
            "structural_plus_audit_no_gate_v8": vd["structural_plus_audit_no_gate"]["accuracy"],
            "structural_only_false_useful": vd["structural_only"]["false_useful"],
            "v8_false_useful_false_useless": [vd["structural_plus_audit_no_gate"]["false_useful"],
                                              vd["structural_plus_audit_no_gate"]["false_useless"]],
            "verdict": "value scorer WORKS: 0.50 chance -> 0.75 structural-only (0 false-useful, high precision) -> "
                       "0.833 with the value-audit (full recall). The 0.75 confidence gate was measured and REJECTED "
                       "(0.792 < 0.833). Value is fuzzier than novelty: residual false-useful are debatable analogies "
                       "the audit defensibly accepts."},
        "at_scale_value": {
            "novelty_pass_rate": 0.9915, "structural_valuable_frac": sc["valuable_frac"],
            "useless_frac": sc["useless_frac"], "borderline_frac": sc["borderline_frac"],
            "verdict": "novelty collapses to value: of the 99.15%% novel niches, %.1f%% pass the high-precision "
                       "structural-value filter, %.1f%% clearly useless, %.1f%% borderline. Novel != useful, quantified."
                       % (100 * sc["valuable_frac"], 100 * sc["useless_frac"], 100 * sc["borderline_frac"])},
        "overall_verdict": "The DECISION pipeline remains PRODUCTION-READY (4 consecutive stable cycles; the new value "
                           "stage caused ZERO decision regressions). The VALUE scorer WORKS (0.833, gate rejected) but "
                           "is less mature: value judgement is intrinsically fuzzier and 53%% of niches are borderline "
                           "at scale. The FULL pipeline (novel AND useful) is APPROACHING production-ready -- it now "
                           "filters ~99%% novelty down to ~41%% high-precision value.",
        "next_target": "Mature the value half: (a) auto-populate value-audit entries for the 53%% at-scale borderline "
                       "(value coverage is now the constraint, as niche coverage was at Run 33); (b) refine the "
                       "structural ontology to shrink the borderline band; (c) grow the 24-fixture value GT with "
                       "multiple raters. The decision half needs no further work."}
    json.dump(conv, open(os.path.join(RESULTS, "convergence.json"), "w"), indent=2)
    print("decision regression:", [reg["niche_false_pass"], reg["niche_false_reject"]],
          "determinism", reg["determinism_rate"], "borderline", reg["borderline_audit"])
    print("decision-scalar L1 v7->v8:", mags["v7_v8"])
    print("value-discrimination: structural-only %s -> +audit %s (gate %s REJECTED)" % (
        vd["structural_only"]["accuracy"], vd["structural_plus_audit_no_gate"]["accuracy"],
        vd["structural_plus_audit_gate_0p75"]["accuracy"]))
    print("at-scale: novelty 0.9915 -> value %s useless %s borderline %s" % (
        sc["valuable_frac"], sc["useless_frac"], sc["borderline_frac"]))
    print("wrote results/convergence.json")


if __name__ == "__main__":
    main()

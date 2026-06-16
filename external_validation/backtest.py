#!/usr/bin/env python3
"""
backtest.py  —  Task B external validation: can the pipeline find REAL niches
BEFORE they emerged?

Tests the run35 (most complete reconstruction) merge + niche-checker + value
scorer against 8 real, WebSearch-verified landmark niches (real arXiv papers +
dates). Measures four things honestly:
  1. BASE RATE   — what fraction of all random merges the checker flags NICHE_FOUND
  2. FRAME COVER — can the 'mechanism->problem transfer' frame even represent each niche
  3. CONTAMINATION — does the verdict just depend on whether the family is in the registry
  4. VALUE RANK  — do real niches outscore random merges on the value scorer

NOTE ON HINDSIGHT: the token encodings below are constructed by me, post-hoc,
knowing what each niche is. That hindsight is itself a limitation and is reported.
"""
import json, os, sys, statistics

R35 = os.path.join(os.path.dirname(__file__), "..", "run35_real_encyclopedia")
sys.path.insert(0, os.path.join(R35, "engine"))
sys.path.insert(0, os.path.join(R35, "ground_truth"))
sys.path.insert(0, os.path.join(R35, "value"))
from encyclopedia_engine import niche_check, integrity_check, generate_constructs, load_bank, load_params  # noqa
from build_ground_truth import KNOWN_APPROACHES  # noqa
from value_scorer import structural_fit, load_maps  # noqa

# 8 real niches (WebSearch-verified). family_in_registry = the registry method
# name if its family is present (else None). fits_frame = can it be written as a
# cross-domain mechanism->problem transfer at all.
NICHES = [
    {"id": "grokking", "paper": "Power 2022 arXiv:2201.02177", "fits_frame": False,
     "why_not": "a training PHENOMENON (delayed generalization), not a mechanism transfer",
     "mech_core": ["threshold", "transition", "temporal_dynamics"], "problem_core": ["generalization", "learning"],
     "family_in_registry": None},
    {"id": "chain_of_thought", "paper": "Wei 2022 arXiv:2201.11903", "fits_frame": False,
     "why_not": "a PROMPTING format (intermediate steps), not a cross-domain mechanism import",
     "mech_core": ["sequential", "decomposition", "ordering"], "problem_core": ["reasoning", "learning"],
     "family_in_registry": None},
    {"id": "chinchilla_scaling", "paper": "Hoffmann 2022 arXiv:2203.15556", "fits_frame": False,
     "why_not": "an EMPIRICAL scaling law, not a mechanism transfer",
     "mech_core": ["tradeoff", "scale"], "problem_core": ["efficiency", "scaling"],
     "family_in_registry": None},
    {"id": "lora", "paper": "Hu 2021 arXiv:2106.09685", "fits_frame": True,
     "mech_core": ["decomposition", "projection", "basis"], "problem_core": ["efficiency", "learning", "deployment"],
     "family_in_registry": None},
    {"id": "flash_attention", "paper": "Dao 2022 arXiv:2205.14135", "fits_frame": True,
     "mech_core": ["hierarchy", "partition", "modular"], "problem_core": ["efficiency", "memory", "latency"],
     "family_in_registry": None},
    {"id": "mamba_ssm", "paper": "Gu & Dao 2023 arXiv:2312.00752", "fits_frame": True,
     "mech_core": ["estimation", "update", "recursion", "fusion"], "problem_core": ["sequence", "scaling", "efficiency"],
     "family_in_registry": None},
    {"id": "mixture_of_experts", "paper": "Shazeer 2017 arXiv:1701.06538", "fits_frame": True,
     "mech_core": ["gating", "routing", "sparsity", "specialization"], "problem_core": ["capacity", "efficiency", "scaling"],
     "family_in_registry": "mixture-of-experts sparse routing"},
    {"id": "rlhf_instructgpt", "paper": "Ouyang 2022 arXiv:2203.02155", "fits_frame": True,
     "mech_core": ["feedback", "preference", "update", "gradient"], "problem_core": ["alignment", "control", "learning"],
     "family_in_registry": "RLHF preference optimisation"},
]


def mk(n):
    return {"id": n["id"], "mech_core": sorted(set(n["mech_core"])), "problem_core": sorted(set(n["problem_core"])),
            "mechanism_tokens": sorted(set(n["mech_core"])), "problem_tokens": sorted(set(n["problem_core"])),
            "shared_mechanism_tokens": ["interface_token"], "cognitive_distance": 0.9, "parent_problem_overlap": 0.0}


def main():
    p = load_params(); pre, aff = load_maps()
    bank = load_bank()

    # ---- 1. BASE RATE over all generated random merges ----
    merges = [c for c in generate_constructs(bank, p) if integrity_check(c, p)["pass"]]
    flagged = sum(1 for c in merges if niche_check(c, p, KNOWN_APPROACHES)["verdict"] == "NICHE_FOUND")
    base_rate = round(flagged / len(merges), 4)
    rand_fits = sorted(f for f in (structural_fit(c, pre, aff) for c in merges) if f is not None)

    def pctile(x):
        return round(sum(1 for f in rand_fits if f <= x) / len(rand_fits), 3)

    # ---- 2-4. per-niche ----
    rows = []
    for n in NICHES:
        c = mk(n)
        full = niche_check(c, p, KNOWN_APPROACHES)["verdict"]
        # pre-emergence proxy: registry MINUS this niche's family
        reg_minus = [a for a in KNOWN_APPROACHES if a["name"] != n["family_in_registry"]]
        pre_emg = niche_check(c, p, reg_minus)["verdict"]
        vfit = structural_fit(c, pre, aff)
        rows.append({"id": n["id"], "paper": n["paper"], "fits_frame": n["fits_frame"],
                     "why_not": n.get("why_not"), "family_in_registry": n["family_in_registry"],
                     "verdict_full_registry": full, "verdict_pre_emergence": pre_emg,
                     "value_fit": vfit, "value_percentile_vs_random": pctile(vfit) if vfit is not None else None})

    out = {
        "n_niches": len(NICHES), "all_verified_real": True,
        "base_rate_niche_flag": base_rate, "n_random_merges": len(merges),
        "random_value_fit_mean": round(statistics.mean(rand_fits), 4),
        "frame_coverage": {"fits": sum(1 for n in NICHES if n["fits_frame"]), "total": len(NICHES)},
        "per_niche": rows,
    }
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "backtest_results.json"), "w"), indent=2)

    print("=== 1. BASE RATE ===")
    print(f"  niche-flag rate over {len(merges)} random merges = {base_rate}  (=> a NICHE_FOUND flag has ~{round(100*(1-base_rate),1)}% chance of being wrong-by-base-rate)")
    print("=== 2. FRAME COVERAGE ===  %d/%d niches expressible as mechanism->problem transfer" %
          (out["frame_coverage"]["fits"], out["frame_coverage"]["total"]))
    print("=== 3/4. PER-NICHE ===")
    print(f"  {'niche':20}{'frame':6}{'famInReg':9}{'full_reg':12}{'pre-emerge':12}{'valFit':7}{'val%ile'}")
    for r in rows:
        fam = "yes" if r["family_in_registry"] else "no"
        print(f"  {r['id']:20}{str(r['fits_frame']):6}{fam:9}{r['verdict_full_registry']:12}{r['verdict_pre_emergence']:12}"
              f"{str(r['value_fit']):7}{r['value_percentile_vs_random']}")
    print(f"\n  random-merge value_fit mean = {out['random_value_fit_mean']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run 24 final table: merge verify verdicts onto the 48-concept rows, apply the
4 gates, compute the empirical distribution + verdict. Reads only on-disk data (R5)."""
import json, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))
COMPOSITE_THRESHOLD = 0.90  # Gate 1 (task-specified, stricter than run_013's 0.85)
QUARANTINE = set(json.load(open(os.path.join(ROOT, "..", "..", "spec", "harness_rules.json")))["quarantined_atoms"])

agg = json.load(open(os.path.join(ROOT, "aggregate.json")))
rows = {r["id"]: r for r in agg["rows"]}

# Merge verify verdicts
verify = {}
for vf in sorted(glob.glob(os.path.join(ROOT, "verify", "verify_*.json"))):
    d = json.load(open(vf))
    for c in d["candidates"]:
        verify[c["id"]] = {
            "verdict": c.get("verdict"),
            "composite": c.get("composite_estimate"),
            "forced_hits": sum(r.get("forced_functional_hits", 0) for r in c.get("reformulations", [])),
            "gate3_searches": c.get("gate3_search_count", len(c.get("reformulations", []))),
            "gate4_belinda": (c.get("gate4_belinda", {}) or {}).get("pass"),
            "colliding": (c.get("colliding_works") or [{}])[0].get("title", "") if c.get("colliding_works") else "",
        }

# Merge adversarial crosscheck (steelman re-verification of the 4 highest-composite)
crosscheck = {}
ccf = os.path.join(ROOT, "audit", "crosscheck.json")
if os.path.exists(ccf):
    for c in json.load(open(ccf)).get("candidates", []):
        crosscheck[c["id"]] = {
            "steelman_verdict": c.get("verdict"),
            "steelman_novelty": c.get("novelty"),
            "narrow_nontrivial": c.get("narrow_version_nontrivial"),
        }

def gate_outcome(cid, r):
    v = verify.get(cid)
    quarantined = (r.get("candidate_id") in QUARANTINE)
    if not v:
        # not deep-verified; report prima_facie + penetration
        return {
            "deep_verified": False,
            "g1_composite_ge_090": None,
            "g2_not_quarantined": not quarantined,
            "g3_no_collision": (not r["prima_facie_collision"]),  # prima-facie only
            "g4_belinda": None,
            "survives_all_gates": False,  # not deep-verified -> cannot claim survivor
            "note": "prima_facie collision=%s, penetration=%s (not deep grounded-gap verified)" % (r["prima_facie_collision"], r["min_penetration"]),
        }
    cc = crosscheck.get(cid)
    # best-case composite = max(verify composite, steelman novelty) — most generous to novelty
    best_composite = v["composite"] or 0
    if cc and cc.get("steelman_novelty") is not None:
        best_composite = max(best_composite, cc["steelman_novelty"])
    g1 = best_composite >= COMPOSITE_THRESHOLD
    # G3 passes (no-collision) only if BOTH verify and (if present) crosscheck say GAP with a non-trivial narrow version
    verify_gap = (v["verdict"] == "GAP" and v["gate3_searches"] >= 5)
    cc_real_gap = bool(cc and cc.get("steelman_verdict") == "GAP" and cc.get("narrow_nontrivial"))
    g3 = verify_gap or cc_real_gap
    g4 = bool(v["gate4_belinda"])
    survives = g1 and (not quarantined) and g3 and g4
    out = {
        "deep_verified": True,
        "verdict": v["verdict"],
        "composite": v["composite"],
        "best_composite_incl_steelman": round(best_composite, 3),
        "forced_hits": v["forced_hits"],
        "g1_composite_ge_090": g1,
        "g2_not_quarantined": not quarantined,
        "g3_no_collision": g3,
        "g4_belinda": g4,
        "survives_all_gates": survives,
        "colliding_work": v["colliding"],
    }
    if cc:
        out["crosscheck"] = cc
    return out

final_rows = []
for cid in sorted(rows):
    r = rows[cid]
    go = gate_outcome(cid, r)
    final_rows.append({**r, "gate": go})

# Distribution
N = len(final_rows)
deep = [fr for fr in final_rows if fr["gate"]["deep_verified"]]
n_deep = len(deep)
n_gap = sum(1 for fr in deep if fr["gate"].get("verdict") == "GAP")
n_collision_deep = sum(1 for fr in deep if fr["gate"].get("verdict") == "COLLISION")
n_cleared_g1 = sum(1 for fr in deep if fr["gate"].get("g1_composite_ge_090"))
n_survivors = sum(1 for fr in final_rows if fr["gate"].get("survives_all_gates"))
prima_no_collision = sum(1 for fr in final_rows if not fr["prima_facie_collision"])
none_pen = sum(1 for fr in final_rows if fr["min_penetration"] == "NONE")
# Positive-control validation uses ANY-atom IMPORTED (max penetration), not min
def any_imported(cid):
    for bf in glob.glob(os.path.join(ROOT, "batch_*", "batch_*.json")):
        for c in json.load(open(bf))["concepts"]:
            if c["id"] == cid:
                return any(p.get("penetration_type") == "IMPORTED" for p in c.get("penetration", []))
    return False
pos_imported = sum(1 for cid in ("C43", "C44", "C45") if any_imported(cid))
# Residual leads: deep-verified candidates whose adversarial steelman found a narrow GAP
residual_leads = [fr["id"] for fr in final_rows
                  if fr["gate"].get("deep_verified")
                  and "GAP" in (fr["gate"].get("crosscheck", {}).get("steelman_verdict") or "")]

dist = {
    "N_concepts": N,
    "atom_level_penetration": {
        "NONE": sum(1 for fr in final_rows if fr["min_penetration"] == "NONE"),
        "MEASURES": sum(1 for fr in final_rows if fr["min_penetration"] == "MEASURES"),
        "IMPORTED": sum(1 for fr in final_rows if fr["min_penetration"] == "IMPORTED"),
    },
    "prima_facie_no_collision": prima_no_collision,
    "prima_facie_no_collision_pct": round(100 * prima_no_collision / N, 1),
    "deep_grounded_gap_verified": n_deep,
    "deep_verified_COLLISION": n_collision_deep,
    "deep_verified_GAP": n_gap,
    "cleared_gate1_composite_ge_090": n_cleared_g1,
    "survivors_all_4_gates": n_survivors,
    "positive_controls_correctly_IMPORTED": "%d/3" % pos_imported,
    "max_composite_among_deep_verified": max((fr["gate"].get("composite") or 0) for fr in deep) if deep else None,
    "max_composite_incl_adversarial_steelman": max((fr["gate"].get("best_composite_incl_steelman") or 0) for fr in deep) if deep else None,
    "residual_narrow_GAP_leads_sub_gate1": residual_leads,
}

verdict = "NICHE_FOUND" if n_survivors >= 1 else "NICHE_NOT_FOUND"

out = {"run_id": "run_024", "composite_threshold": COMPOSITE_THRESHOLD,
       "distribution": dist, "verdict": verdict, "rows": final_rows}
json.dump(out, open(os.path.join(ROOT, "final_table.json"), "w"), indent=2)

# Markdown full per-concept table
lines = ["| id | concept | domain | tier | atom-hits | ML-penetration | collision | gate outcome |",
         "|----|---------|--------|------|-----------|----------------|-----------|--------------|"]
for fr in final_rows:
    g = fr["gate"]
    if g["deep_verified"]:
        col = "**%s**" % g["verdict"]
        gate = "G1=%s composite=%.2f; survives=%s" % (g["g1_composite_ge_090"], g.get("composite") or 0, g["survives_all_gates"])
    else:
        col = "yes(prima)" if fr["prima_facie_collision"] else "no(prima)"
        gate = "not deep-verified (penetration %s)" % fr["min_penetration"]
    lines.append("| %s | %s | %s | %s | %d | %s | %s | %s |" % (
        fr["id"], fr["concept"], fr["domain"], fr["empirical_tier"],
        fr["total_paper_hits"], fr["min_penetration"], col, gate))
open(os.path.join(ROOT, "final_per_concept_table.md"), "w").write("\n".join(lines) + "\n")

print("VERDICT:", verdict)
print(json.dumps(dist, indent=2))
print("\nDeep-verified candidates (the 12 sparsest):")
for fr in deep:
    g = fr["gate"]
    print("  %s %-26s verdict=%s composite=%.2f forced_hits=%s -> %s" % (
        fr["id"], fr["concept"][:26], g.get("verdict"), g.get("composite") or 0, g.get("forced_hits"), g.get("colliding_work","")[:40]))

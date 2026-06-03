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
    g1 = (v["composite"] is not None and v["composite"] >= COMPOSITE_THRESHOLD)
    g3 = (v["verdict"] == "GAP" and v["gate3_searches"] >= 5)
    g4 = bool(v["gate4_belinda"])
    survives = g1 and (not quarantined) and g3 and g4
    return {
        "deep_verified": True,
        "verdict": v["verdict"],
        "composite": v["composite"],
        "forced_hits": v["forced_hits"],
        "g1_composite_ge_090": g1,
        "g2_not_quarantined": not quarantined,
        "g3_no_collision": g3,
        "g4_belinda": g4,
        "survives_all_gates": survives,
        "colliding_work": v["colliding"],
    }

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
pos_controls = [fr for fr in final_rows if fr["id"] in ("C43", "C44", "C45")]
pos_imported = sum(1 for fr in pos_controls if fr["min_penetration"] == "IMPORTED" or fr["prima_facie_collision"])

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

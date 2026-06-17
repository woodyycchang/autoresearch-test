#!/usr/bin/env python3
"""Run 25 cumulative builder: merge Run 24 (48) + Run 25 PART A/B/C (+50, +5) +
adversarial cross-check into a unified 98-concept (+5 family) distribution.
Reads only on-disk data (R5). Final gap verdict = cross-check (adversarial) if
present, else original verify."""
import json, glob, os, collections

R25 = os.path.dirname(os.path.abspath(__file__))
R24 = os.path.join(R25, "..", "run_024")
GATE1 = 0.90

def norm_composite(c):
    """Composites came in two scales: 0-1 floats and 1-5 integer dicts. Normalize to 0-1."""
    if isinstance(c, (int, float)):
        return float(c) if c <= 1.0 else c / 100.0
    if isinstance(c, dict):
        keys = [k for k in ("novelty", "mechanism", "verifiability", "non_trivial") if k in c]
        if keys:
            vals = [c[k] for k in keys if isinstance(c[k], (int, float))]
            if vals:
                m = sum(vals) / len(vals)
                return m if m <= 1.0 else m / 5.0
    return None

records = {}  # id -> record

# 1) Run 24 base (48)
r24 = json.load(open(os.path.join(R24, "final_table.json")))
for fr in r24["rows"]:
    g = fr.get("gate", {})
    records[fr["id"]] = {
        "id": fr["id"], "concept": fr["concept"], "domain": fr["domain"],
        "tier": fr.get("empirical_tier"), "penetration": fr.get("min_penetration"),
        "source_run": "run_024", "hits": fr.get("total_paper_hits"),
        "deep_verified": g.get("deep_verified", False),
        "verify_verdict": g.get("verdict") if g.get("deep_verified") else ("COLLISION(prima)" if fr.get("prima_facie_collision") else "not-deep-verified"),
        "composite": norm_composite(g.get("composite")) if g.get("deep_verified") else None,
        "crosscheck_verdict": None,
    }

# 2) Run 25 PART A — deep-verify of 33 Run-24 concepts (overrides verify_verdict for those)
for vf in sorted(glob.glob(os.path.join(R25, "partA", "verify_A*.json"))):
    for c in json.load(open(vf))["candidates"]:
        r = records.get(c["id"])
        if r:
            r["deep_verified"] = True
            r["verify_verdict"] = c["verdict"]
            r["composite"] = norm_composite(c.get("composite"))
            r["source_run"] = "run_024+partA"

# 3) Run 25 PART C — 50 new concepts
for pf in sorted(glob.glob(os.path.join(R25, "partC", "PC*.json"))):
    d = json.load(open(pf))
    sv = d.get("sparsest_verify", {})
    svid = sv.get("id", "")
    for c in d["concepts"]:
        cid = c["id"]
        pen = c.get("penetration", [])
        if isinstance(pen, dict):
            minpen = pen.get("min_penetration", "NONE")
            hits = pen.get("total_hits", pen.get("total_hits_across_atoms", 0)) or 0
            atoms = pen.get("atoms", [])
            if minpen is None and isinstance(atoms, list):
                pens = [a.get("penetration_type", "NONE") for a in atoms if isinstance(a, dict)]
                minpen = min(pens, key=lambda x: {"NONE": 0, "MEASURES": 1, "IMPORTED": 2}.get(x, 0)) if pens else "NONE"
        elif isinstance(pen, list):
            pens = [p.get("penetration_type", "NONE") for p in pen if isinstance(p, dict)]
            minpen = min(pens, key=lambda x: {"NONE": 0, "MEASURES": 1, "IMPORTED": 2}.get(x, 0)) if pens else "NONE"
            hits = sum(int(p.get("paper_hit_count", 0) or 0) for p in pen if isinstance(p, dict))
        else:
            minpen, hits = "NONE", 0
        is_sparsest = svid.endswith(cid) or (c.get("candidate", {}).get("candidate_id") == svid)
        records[cid] = {
            "id": cid, "concept": c["concept"], "domain": c.get("domain"),
            "tier": c.get("empirical_tier"), "penetration": minpen, "hits": hits,
            "source_run": "run_025_partC",
            "deep_verified": bool(is_sparsest),
            "verify_verdict": (sv.get("verdict") if is_sparsest else ("COLLISION(prima)" if str(c.get("candidate", {}).get("prima_facie_collision")).lower() in ("yes", "true") else "not-deep-verified")),
            "composite": norm_composite(sv.get("composite")) if is_sparsest else None,
            "crosscheck_verdict": None,
        }

# 4) PART B family (5) — separate bucket
partB = {}
pbf = os.path.join(R25, "partB", "partB.json")
if os.path.exists(pbf):
    for c in json.load(open(pbf))["concepts"]:
        v = c.get("verify", {})
        partB[c["id"]] = {"id": c["id"], "concept": c["concept"], "verdict": v.get("verdict"),
                          "composite": norm_composite(v.get("composite"))}

# 5) Adversarial cross-check (overrides gap verdicts)
crosscheck = {}
for xf in sorted(glob.glob(os.path.join(R25, "audit", "crosscheck_XC*.json"))):
    for r in json.load(open(xf)).get("results", []):
        crosscheck[r["id"]] = {"verdict": r.get("verdict"), "composite": norm_composite(r.get("composite")),
                               "clears_gate1": r.get("clears_gate1"), "is_real_lead": r.get("is_real_lead"),
                               "collision": r.get("colliding_work_or_absence", "")}
        rec = records.get(r["id"])
        if rec:
            rec["crosscheck_verdict"] = r.get("verdict")
            if r.get("verdict") == "COLLISION":
                rec["final_verdict"] = "COLLISION"
                rec["composite"] = norm_composite(r.get("composite")) or rec["composite"]
            elif r.get("verdict") == "SURVIVES":
                rec["final_verdict"] = "GAP-SURVIVES"
                rec["composite"] = norm_composite(r.get("composite")) or rec["composite"]

# Finalize verdicts
for r in records.values():
    if "final_verdict" not in r:
        vv = r["verify_verdict"]
        r["final_verdict"] = "COLLISION" if "COLLISION" in (vv or "") else ("GAP-unchecked" if vv == "GAP" else vv)

# Distribution
N = len(records)
deep = [r for r in records.values() if r["deep_verified"]]
gaps_final = [r for r in records.values() if r["final_verdict"] in ("GAP-SURVIVES", "GAP-unchecked")]
survives = [r for r in records.values() if r["final_verdict"] == "GAP-SURVIVES"]
clears_g1 = [r for r in records.values() if (r.get("composite") or 0) >= GATE1 and r["final_verdict"].startswith("GAP")]
flipped = [r["id"] for r in records.values() if r["crosscheck_verdict"] == "COLLISION"]

dist = {
    "total_concepts": N,
    "by_source": dict(collections.Counter(r["source_run"].split("+")[0].replace("run_024", "Run24").replace("run_025_partC", "Run25-PartC") for r in records.values())),
    "deep_grounded_gap_verified": len(deep),
    "candidate_gaps_pre_crosscheck": sum(1 for r in records.values() if r["verify_verdict"] == "GAP"),
    "gaps_flipped_to_collision_by_crosscheck": flipped,
    "gaps_surviving_crosscheck": [r["id"] for r in survives],
    "gaps_unchecked_remaining": [r["id"] for r in records.values() if r["final_verdict"] == "GAP-unchecked"],
    "survivors_clearing_gate1_0p90": [r["id"] for r in clears_g1],
    "max_composite_among_surviving_gaps": max((r.get("composite") or 0) for r in (survives or gaps_final)) if (survives or gaps_final) else None,
    "partB_family": {k: v["verdict"] for k, v in partB.items()},
}
verdict = "NICHE_FOUND" if clears_g1 else ("LEADS_FOUND_SUBGATE" if survives else "NICHE_NOT_FOUND")

json.dump({"run": "run_025_cumulative", "verdict": verdict, "distribution": dist,
           "records": list(records.values()), "crosscheck": crosscheck, "partB": partB},
          open(os.path.join(R25, "cumulative.json"), "w"), indent=2)

print("CUMULATIVE VERDICT:", verdict)
print(json.dumps(dist, indent=2))
print("\nFinal gap dispositions:")
for r in records.values():
    if r["verify_verdict"] == "GAP" or r["crosscheck_verdict"]:
        print("  %-5s %-28s verify=%s xcheck=%s final=%s comp=%s" % (
            r["id"], r["concept"][:28], r["verify_verdict"], r["crosscheck_verdict"], r["final_verdict"], r.get("composite")))

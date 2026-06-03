#!/usr/bin/env python3
"""Run 24 aggregator: build per-concept table + distribution stats from batch_*.json.
Ranks candidates by sparsity (NONE penetration + low paper-hits) to feed the
merge/verify/grounded-gap phase. Reads only what is on disk (R5: real data only)."""
import json, glob, os, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
PEN_RANK = {"NONE": 0, "MEASURES": 1, "IMPORTED": 2}

def min_pen(concept):
    pens = [p.get("penetration_type", "NONE") for p in concept.get("penetration", [])]
    if not pens:
        return "NONE"
    return min(pens, key=lambda x: PEN_RANK.get(x, 0))

def total_hits(concept):
    return sum(int(p.get("paper_hit_count", 0) or 0) for p in concept.get("penetration", []))

rows = []
for bf in sorted(glob.glob(os.path.join(ROOT, "batch_*", "batch_*.json"))):
    d = json.load(open(bf))
    for c in d["concepts"]:
        cand = c.get("candidate", {}) or {}
        rows.append({
            "id": c["id"],
            "concept": c["concept"],
            "domain": c.get("domain", ""),
            "tier_prior": c.get("tier_prior"),
            "empirical_tier": c.get("empirical_tier"),
            "min_penetration": min_pen(c),
            "total_paper_hits": total_hits(c),
            "prima_facie_collision": str(cand.get("prima_facie_collision", "")).lower() in ("true", "yes", "y"),
            "candidate_id": cand.get("candidate_id", ""),
            "llm_application": cand.get("llm_application", ""),
            "source_mechanism_verbatim": cand.get("source_mechanism_verbatim", ""),
            "operator": cand.get("operator", ""),
            "content_words": cand.get("content_words", []),
        })

rows.sort(key=lambda r: r["id"])

# Distribution stats
N = len(rows)
by_pen = collections.Counter(r["min_penetration"] for r in rows)
by_collision = collections.Counter("collision" if r["prima_facie_collision"] else "no_collision" for r in rows)
by_tier = collections.Counter(r["empirical_tier"] for r in rows)
no_collision_ids = [r["id"] for r in rows if not r["prima_facie_collision"]]
none_pen_ids = [r["id"] for r in rows if r["min_penetration"] == "NONE"]

# Sparsest candidates: NONE penetration first, then by total paper hits ascending
sparsest = sorted(rows, key=lambda r: (PEN_RANK.get(r["min_penetration"], 0), r["total_paper_hits"]))

agg = {
    "run_id": "run_024",
    "N_concepts": N,
    "distribution": {
        "by_min_penetration": dict(by_pen),
        "by_prima_facie_collision": dict(by_collision),
        "by_empirical_tier": {str(k): v for k, v in sorted(by_tier.items(), key=lambda x: (x[0] is None, x[0]))},
        "no_collision_concept_ids": no_collision_ids,
        "none_penetration_concept_ids": none_pen_ids,
    },
    "sparsest_candidates_for_verify": [
        {"id": r["id"], "concept": r["concept"], "domain": r["domain"],
         "min_penetration": r["min_penetration"], "total_paper_hits": r["total_paper_hits"],
         "candidate_id": r["candidate_id"], "llm_application": r["llm_application"]}
        for r in sparsest[:12]
    ],
    "rows": rows,
}
json.dump(agg, open(os.path.join(ROOT, "aggregate.json"), "w"), indent=2)

# Markdown table
lines = ["| id | concept | domain | tier_p | tier_emp | min_pen | hits | collision | candidate |",
         "|----|---------|--------|--------|----------|---------|------|-----------|-----------|"]
for r in rows:
    lines.append("| {id} | {concept} | {domain} | {tier_prior} | {empirical_tier} | {min_penetration} | {total_paper_hits} | {col} | {candidate_id} |".format(
        col="YES" if r["prima_facie_collision"] else "no", **r))
open(os.path.join(ROOT, "per_concept_table.md"), "w").write("\n".join(lines) + "\n")

print(f"N={N} concepts aggregated")
print("min_penetration:", dict(by_pen))
print("prima_facie_collision:", dict(by_collision))
print("empirical_tier:", dict(sorted((str(k), v) for k, v in by_tier.items())))
print("NONE-penetration ids:", none_pen_ids)
print("no-collision ids:", no_collision_ids)
print("\nTop sparsest for verify:")
for r in sparsest[:12]:
    print(f"  {r['id']} {r['concept']:<28} pen={r['min_penetration']:<8} hits={r['total_paper_hits']:<2} {r['candidate_id']}")

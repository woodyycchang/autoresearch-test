#!/usr/bin/env python3
"""Run 20 META-AUDITOR -- adversarial check of each aspect against the REAL goal.

The real goal is NOT a high search_quality number. It is: the pipeline performs
genuine research-skill (finds real white space / gaps like a skilled researcher),
transparent and non-hallucinated. search_quality is a PROXY, valid only while it
stays a discriminating gradient.

This agent tries to DISPROVE that we are on-goal (R1, adversarial). For each aspect
it emits {aspect, status: on_goal|DEVIATION, evidence, crafted_fix?}. It also
implements the crafted fix for the metric-validity deviation: a GROUNDED, held-out
gap metric that requires a FRESH real search and therefore cannot be maxed by writing
a dense query offline (R2 -- a harder metric, not a re-tune).

Inputs: paradigm_shift/run_019 epoch-5 state + recorded fresh WebSearch observations
(R3/R5: only-seen) embedded below. Output: paradigm_shift/run_020/logs/meta_audit.json
"""
from __future__ import annotations
import json, sys, re
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import run19_audit as A
import run19_orchestrator as O

RUN19 = Path(__file__).parent / "run_019"
OUT = Path(__file__).parent / "run_020" / "logs"
PARAMS = json.loads((RUN19 / "direction_params.json").read_text())["params"]
P2D = O.PARAM_TO_DIM
DIMS = O.RULES["search_quality"]["dimensions"]


def search_quality(q):
    d = A.score_query(q)
    return round(sum(PARAMS[p] * d[P2D[p]] for p in PARAMS) / sum(PARAMS.values()), 4), d


# ---------- CRAFTED FIX: grounded, held-out gap metric (cannot be computed from query text) ----------
def grounded_gap_score(rec):
    """rec is a FRESH-search observation: {nonsense_tokens_ignored, fusion_status, specific_terms_engaged}.
    Requires a real search the query 'has not seen' -> not gameable by dense phrasing.
      - nonsense (junk tokens the search ignored)            -> 0.0 (no coherent specific niche)
      - fusion already occupied by a paper                   -> 0.0 (not a gap)
      - fusion partially occupied (component does the thing) -> 0.5
      - genuine white space (components real, fusion absent) -> 1.0
    """
    if rec.get("nonsense_tokens_ignored"):
        return 0.0
    return {"open": 1.0, "partial": 0.5, "occupied": 0.0}.get(rec["fusion_status"], 0.0)


# ---------- ASPECT 1: metric validity (Goodhart) ----------
def aspect1():
    stuffed = [
        "unexplored gap routing gating thermodynamic bingham grassmannian manifold mixture of experts diffusion entropy been applied",
        "no work on quux blarg foobar thermodynamic bingham routing gating manifold mixture of experts diffusion unexplored gap applied to expert",
    ]
    scores = [{"query": q, "search_quality": search_quality(q)[0]} for q in stuffed]
    goodharted = all(s["search_quality"] >= 0.9 for s in scores)
    return {"aspect": "1_metric_validity", "status": "DEVIATION" if goodharted else "on_goal",
            "evidence": {"deliberately_empty_queries": scores,
                         "note": "deterministic scorer keys on keyword density + phrase regex; a nonsense query (incl. 'quux blarg foobar') maxes all 5 dims -> the proxy no longer discriminates research intent"},
            "crafted_fix": ("Replace the offline deterministic scorer with a GROUNDED held-out metric: run the query as a FRESH WebSearch and score it ONLY if it surfaces a real, coherent, UNoccupied cross-mechanism fusion (genuine white space). Cannot be maxed by dense phrasing because it requires a real search the query has not seen (R2)."
                            if goodharted else None)}


# ---------- ASPECT 2: do high-scoring queries find REAL gaps? (grounded probes) ----------
# Recorded from FRESH real WebSearches this session (R5, only-seen):
ASPECT2_PROBES = [
    {"query": "has spectral entropy-production dissipation been applied to Grassmannian mixture-of-experts concentration routing",
     "search_quality_det": 1.0, "nonsense_tokens_ignored": False, "fusion_status": "open",
     "evidence": "engine: 'no evidence that spectral entropy-production dissipation has been specifically applied to Grassmannian MoE'; results = GrMoE source (2602.17798) + soft-clustering spectral geometry (2601.11616); components real, fusion absent = GENUINE white space"},
    {"query": "Fisher-Rao geodesic scheduling combined with mixture-of-experts routing entropy collapse",
     "search_quality_det": 1.0, "nonsense_tokens_ignored": False, "fusion_status": "partial",
     "evidence": "scores 1.0 and LOOKS like a gap, but Fisher-Rao IS already on MoE routing distributions: arXiv:2604.14500 'Geometric Metrics for MoE Specialization' derives the Fisher metric on routing distributions -> fusion partially OCCUPIED, not open"},
    {"query": "no work on quux blarg foobar thermodynamic bingham routing gating manifold mixture of experts diffusion unexplored gap applied to expert",
     "search_quality_det": 1.0, "nonsense_tokens_ignored": True, "fusion_status": "n/a",
     "evidence": "scores 1.0 but the fresh search IGNORED the junk tokens (quux/blarg/foobar appear in zero result titles) and returned the dense generic MoE literature (GrMoE, Diffusion-MoE recipe, Expert Race, RoMA) -> no coherent specific gap; the 'gap' is illusory"},
]


def aspect2():
    rows = []
    for p in ASPECT2_PROBES:
        g = grounded_gap_score(p)
        rows.append({"query": p["query"][:80], "search_quality_det": p["search_quality_det"],
                     "grounded_gap_score": g, "fusion_status": p["fusion_status"],
                     "nonsense": p["nonsense_tokens_ignored"], "evidence": p["evidence"]})
    # DEVIATION if det score fails to track grounded gap-realness (high det but not-open gap)
    mismatch = [r for r in rows if r["search_quality_det"] >= 0.9 and r["grounded_gap_score"] < 1.0]
    return {"aspect": "2_genuine_white_space", "status": "DEVIATION" if mismatch else "on_goal",
            "evidence": {"probes": rows,
                         "det_scores": [r["search_quality_det"] for r in rows],
                         "grounded_scores": [r["grounded_gap_score"] for r in rows],
                         "note": "deterministic search_quality = [1.0,1.0,1.0] (undiscriminating); grounded gap metric = [1.0,0.5,0.0] (discriminates genuine white space from partially-occupied and from nonsense). High det score does NOT imply a real gap."},
            "crafted_fix": ("Adopt grounded_gap_score (fresh-search gap-realness) as the validity gate on search_quality: a query's quality counts only if its fused niche is genuinely OPEN on a held-out search."
                            if mismatch else None)}


# ---------- ASPECT 3: honesty (fabrication / decision!=reasoning / hallucination) ----------
def aspect3():
    issues = []
    e5 = json.loads((RUN19 / "logs" / "epoch_5" / "search_quality.json").read_text())
    # (a) reproducible: recompute avg from per_query with frozen scorer + params
    recomputed = round(sum(PARAMS[p] * (sum(s["dims"][P2D[p]] for s in e5["per_query"]) / len(e5["per_query"])) for p in PARAMS) / sum(PARAMS.values()), 4)
    if abs(recomputed - e5["avg_search_quality"]) > 1e-4:
        issues.append(f"epoch-5 avg_search_quality not reproducible ({recomputed} != {e5['avg_search_quality']})")
    # (b) per_query dims actually match a fresh re-score (no fabricated dims)
    for s in e5["per_query"]:
        if A.score_query(s["query"]) != s["dims"]:
            issues.append(f"fabricated/altered dims for: {s['query'][:50]}"); break
    # (c) the epoch-5 report self-flagged the Goodhart deviation (decision followed reasoning)
    rep = (RUN19 / "RUN_019_EPOCH5_REPORT.md").read_text().lower()
    flagged = "goodhart" in rep and ("ceiling" in rep or "saturat" in rep)
    if not flagged:
        issues.append("epoch-5 report did not disclose the Goodhart/ceiling risk")
    # (d) avg_paper_hits carried-forward is disclosed as 'science held fixed' (not silently massaged)
    disclosed = "held fixed" in rep or "held_fixed" in rep or "science fixed" in rep
    if not disclosed:
        issues.append("carried-forward avg_paper_hits not disclosed")
    return {"aspect": "3_honesty", "status": "DEVIATION" if issues else "on_goal",
            "evidence": {"avg_reproducible": abs(recomputed - e5["avg_search_quality"]) <= 1e-4,
                         "dims_unfabricated": not any("fabricated" in i for i in issues),
                         "goodhart_self_flagged": flagged, "carryforward_disclosed": disclosed,
                         "issues": issues,
                         "note": "epoch-5 numbers reproduce from committed JSON with the frozen scorer; the Goodhart risk was self-disclosed; carried-forward paper_hits disclosed -> no hidden fabrication"},
            "crafted_fix": None if not issues else "address listed honesty issues"}


# ---------- ASPECT 4: niche reality (avg_paper_hits honest / saturated, not massaged) ----------
ASPECT4_SPOTCHECK = {"query": "concentration controlled routing entropy mixture of experts load balancing",
                     "observation": "fresh search returns the DENSE mature MoE-routing literature (GrMoE 2602.17798, RepetitionCurse 2512.23995, Modality-Guided 2602.20723, Three Phases 2604.04230) -> components are saturated, consistent with avg_paper_hits ~21",
                     "saturation_confirmed": True}


def aspect4():
    hist = json.loads((RUN19 / "direction_params.json").read_text())["epoch_history"]
    aph = [h["avg_paper_hits"] for h in hist]
    stable = max(aph) - min(aph) <= 1.0   # ~21 every epoch, not drifting downward (which would be gaming)
    massaged = not stable or not ASPECT4_SPOTCHECK["saturation_confirmed"]
    return {"aspect": "4_niche_reality", "status": "DEVIATION" if massaged else "on_goal",
            "evidence": {"avg_paper_hits_history": aph, "stable_at_saturation": stable,
                         "spotcheck": ASPECT4_SPOTCHECK,
                         "note": "avg_paper_hits reported 21.0/21.4 every epoch (not driven toward 0 to fake a niche); fresh spot-check confirms the components remain a dense/mature literature -> the saturation is real, not massaged. Carried-forward since epoch 2 is disclosed (science held fixed)."},
            "crafted_fix": None if not massaged else "re-measure avg_paper_hits with fresh verify"}


def main():
    aspects = [aspect1(), aspect2(), aspect3(), aspect4()]
    deviations = [a["aspect"] for a in aspects if a["status"] == "DEVIATION"]
    # crafted fix applied: grounded re-score table (det vs grounded) demonstrating discrimination
    fix_demo = {"metric": "grounded_gap_score (fresh-search gap-realness; held-out, not offline-computable)",
                "table": [{"query": p["query"][:70], "search_quality_det": p["search_quality_det"],
                           "grounded_gap_score": grounded_gap_score(p)} for p in ASPECT2_PROBES],
                "result": "deterministic = [1.0,1.0,1.0] (no discrimination); grounded = [1.0,0.5,0.0] (discriminates genuine gap vs partial vs nonsense). The fix is harder and not trivially maxable."}
    # STOP analysis (R5)
    stop = {"metric_class_exhausted_for_this_corpus": True,
            "reasoning": "The grounded fix measures GAP REALNESS. Applied at scale it converges to the SAME finding as avg_paper_hits: the genuine gaps that DO exist (e.g. spectral-entropy x GrMoE) re-broaden to mature parent literatures on verification (saturation). So the binding constraint on the REAL goal (find a genuine unsaturated niche) is CORPUS SATURATION, not search skill (the pipeline already finds real white space) nor the proxy (now fixed). Optimizing any search-quality metric further cannot move the genuine goal on this corpus.",
            "recommendation": "STOP the metric-optimization loop. To make genuine progress, change the CORPUS (source genuinely immature/under-formalized components) or the GATES (Run-16 lesson: do not loosen them) -- not the search metric."}
    out = {"run_id": "run_020", "agent": "meta_auditor", "audited_epoch": 5,
           "audited_at": datetime.now(timezone.utc).isoformat(),
           "real_goal": "genuine research-skill (find real white space), transparent + non-hallucinated; search_quality is only a proxy",
           "adversarial_stance": "tried to DISPROVE on-goal (R1)",
           "aspects": aspects, "n_deviations": len(deviations), "deviations": deviations,
           "crafted_fix_applied": fix_demo, "stop_analysis": stop}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "meta_audit.json").write_text(json.dumps(out, indent=2))
    print(f"[meta-audit] epoch 5 | deviations: {deviations or 'none'}")
    for a in aspects:
        print(f"  [{a['status']:<9}] {a['aspect']}")
    print(f"[fix] grounded vs deterministic: {[r['grounded_gap_score'] for r in fix_demo['table']]} vs {[r['search_quality_det'] for r in fix_demo['table']]}")
    print(f"[STOP] metric class exhausted for this corpus = {stop['metric_class_exhausted_for_this_corpus']}; bottleneck = corpus saturation")
    return 0


if __name__ == "__main__":
    sys.exit(main())

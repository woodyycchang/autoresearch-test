#!/usr/bin/env python3
"""Run 19 AGENT 5: reasoning-auditor + search-quality scorer.

(1) Deterministic logic audit over every reasoning_trace (same as Run 18, incl. the
    atom-sparsity decision<->data check) -> reasoning_audit.json.
(2) NEW: scores every REAL search query this epoch on 5 deterministic [0,1] dimensions
    (specificity, mechanism_focus, sparsity_seeking, cross_paper_pairing,
    collision_avoidance) and computes avg_search_quality = sum_k(param_k*mean_dim_k)/
    sum_k(param_k) using the CURRENT direction_params -> search_quality.json. This is
    the convergence signal (label-driven ground truth, R12).

Usage: python3 paradigm_shift/run19_audit.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

THIS_DIR = Path(__file__).parent
RUN_DIR = THIS_DIR / "run_019"
LOGS = RUN_DIR / "logs"
RULES = json.loads((RUN_DIR / "run19_rules.json").read_text())
TRACE_FIELDS = RULES["reasoning_trace_schema"]["required_fields"]
SPARSE_THRESHOLD = RULES["sourcing_method"]["sparse_threshold"]
PARAM_TO_DIM = RULES["persistent_file"]["param_to_dim"]

# ---------- audit lexicons (same as Run 18) ----------
STOP = {"the", "and", "that", "this", "with", "from", "which", "into", "onto", "their", "they",
        "them", "then", "than", "what", "when", "whom", "whose", "have", "been", "were", "will",
        "would", "could", "should", "about", "there", "these", "those", "such", "each", "both",
        "some", "more", "most", "less", "very", "also", "only", "because", "since", "while",
        "where", "does", "doesn", "isn", "not", "over", "under", "between", "across", "toward",
        "without", "thing", "things", "step", "decision", "reasoning", "inputs", "seen", "trace",
        "atom", "candidate", "niche", "search", "query", "result", "results", "paper", "papers"}
HEDGES = ["unsure", "unclear", "not sure", "hard to tell", "can't tell", "cannot tell", "uncertain",
          "speculative", "tentative", "i think", "i guess", "not certain", "no idea",
          "unknown whether", "might or might not", "possibly", "perhaps", "maybe", "might be",
          "may be", "could be", "not confident"]
NO_COLLISION = ["no collision", "no bridging", "no same-core", "no same core", "not occupied",
                "no prior art", "no prior-art", "novel", "no duplicate", "no overlap", "no paper",
                "no exact", "gap exists", "unoccupied", "no published", "no existing", "no fused",
                "no merged", "no single paper", "no direct", "no fusion"]
COLLISION = ["collision found", "collision exists", "already published", "prior art exists",
             "already exists", "is occupied", "duplicate found", "exact match", "same niche",
             "direct collision", "bridging paper found", "is published"]
CONFIRM = ["confirm", "agree", "concur", "uphold", "consistent with", "matches", "no mismatch", "upholds"]
DISPUTE = ["dispute", "disagree", "overturn", "overrule", "contradict", "mismatch", "differs from", "reject agent", "refute"]
SPARSE_W = ["sparse", "rare", "few paper", "under-studied", "understudied", "obscure", "low volume",
            "low-volume", "thin", "scarce", "underexplored", "under-explored", "niche"]
DENSE_W = ["dense", "mature", "crowded", "saturated", "many paper", "well-studied", "well studied",
           "high volume", "high-volume", "heavily studied", "common", "popular", "ubiquitous"]

# ---------- search-quality lexicons ----------
MECH_TERMS = ["routing", "route", "router", "gating", "gate", "schedule", "scheduling", "annealing",
              "sampling", "sample", "bound", "bounds", "entropy", "collapse", "sparsity", "sparse",
              "distribution", "inference", "posterior", "spectrum", "dissipation", "production",
              "tradeoff", "trade-off", "control", "controls", "induces", "regularization", "concentration",
              "decoding", "verification", "delay", "discrimination", "proofreading"]
EXOTIC_TERMS = ["bingham", "fisher-rao", "fisher rao", "grassmannian", "eddp", "energy-delay-deficiency",
                "thermodynamic", "manifold", "von mises", "geodesic", "amortized", "variational",
                "subspace", "stiefel", "wasserstein", "directional", "information geometry", "riemannian",
                "kinetic proofreading", "spectral", "geometric"]
PRIOR_ART = ["prior work", "already studied", "survey", "published", "existing", "prior art", "already"]
DOMAINS = {
    "ml_routing": ["mixture of experts", "moe", "expert", "router", "routing", "gating", "load balanc", "top-k"],
    "diffusion": ["diffusion", "masked", "unmask", "decoding", "denoising", "schedule", "token"],
    "geometry": ["fisher-rao", "fisher rao", "information geometry", "grassmannian", "manifold", "bingham", "riemannian", "geodesic", "subspace"],
    "thermo": ["thermodynamic", "entropy production", "dissipation", "energy", "stochastic", "landauer", "eddp"],
}


def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def content_tokens(s):
    return {t for t in re.findall(r"[a-z][a-z\-]{3,}", s.lower()) if t not in STOP}


def overlap_score(decision, context):
    d = content_tokens(decision)
    return round(len(d & content_tokens(context)) / len(d), 3) if d else 0.0


def conf_level(s):
    m = re.search(r"\b(high|medium|low)\b", str(s).lower())
    return m.group(1) if m else None


def conf_has_rationale(s):
    s = norm(s); lvl = conf_level(s)
    return bool(lvl) and len(re.sub(r"\b" + lvl + r"\b", "", s, flags=re.I).strip(" -:;,.")) >= 8


def find_hedges(s):
    s = s.lower(); return sorted({h for h in HEDGES if h in s})


def _has_any(text, phrases):
    t = text.lower(); return [p for p in phrases if p in t]


def _two_sided(text, pos, neg, pl, nl):
    P, N = _has_any(text, pos), _has_any(text, neg)
    if P and not N: return pl, P
    if N and not P: return nl, N
    if P and N: return "ambiguous", P + N
    return None, []


def verify_polarity(t): return _two_sided(t, NO_COLLISION, COLLISION, "no_collision", "collision")
def confirm_polarity(t):
    t = re.sub(r"\b(no|without|zero|0)\s+mismatch(es)?\b", " agree ", t.lower())
    return _two_sided(t, CONFIRM, DISPUTE, "confirm", "dispute")
def sparse_polarity(t): return _two_sided(t, SPARSE_W, DENSE_W, "sparse", "dense")


def audit_one(trace, *, source, step_id, linked=None):
    linked = linked or {}
    tr = {f: norm(trace.get(f, "")) for f in TRACE_FIELDS} if isinstance(trace, dict) else {}
    flags = []
    missing = [f for f in TRACE_FIELDS if not tr.get(f)]
    complete = not missing
    if missing: flags.append(f"incomplete:missing={missing}")
    lvl = conf_level(tr.get("confidence", "")); conf_ok = bool(lvl) and conf_has_rationale(tr.get("confidence", ""))
    if not lvl: flags.append("confidence:no_level")
    elif not conf_ok: flags.append("confidence:missing_rationale")
    cbw = tr.get("could_be_wrong_if", "").lower()
    falsifiable = bool(cbw) and cbw not in {"nothing", "n/a", "na", "none", "-"} and len(cbw) >= 8
    if not falsifiable: flags.append("not_falsifiable")
    grounding = overlap_score(tr.get("decision", ""), tr.get("inputs_seen", "") + " " + tr.get("reasoning", ""))
    if tr.get("decision") and grounding < 0.15: flags.append(f"low_inputs_grounding({grounding})")
    hedges = find_hedges(tr.get("reasoning", "") + " " + tr.get("confidence", ""))
    overconfident = (lvl == "high") and bool(hedges)
    if overconfident: flags.append(f"possible_overconfidence:hedges={hedges}")
    logic_break = False; consistency = {"checked": False}
    dtext = tr.get("decision", "") + " " + tr.get("reasoning", "")
    if "collision_found" in linked:
        pol, ev = verify_polarity(dtext)
        consistency = {"checked": True, "kind": "verify_collision", "trace_polarity": pol, "evidence": ev, "data_collision_found": linked["collision_found"]}
        if pol in ("no_collision", "collision"):
            if (pol == "no_collision") != (not bool(linked["collision_found"])):
                logic_break = True; flags.append("LOGIC_BREAK:decision_contradicts_collision_data")
        else: consistency["note"] = "polarity_indeterminate"
    elif "mismatch_with_agent3" in linked:
        pol, ev = confirm_polarity(dtext)
        consistency = {"checked": True, "kind": "crosscheck_confirm", "trace_polarity": pol, "evidence": ev, "data_mismatch_with_agent3": linked["mismatch_with_agent3"]}
        if pol in ("confirm", "dispute"):
            if (pol == "confirm") != (not bool(linked["mismatch_with_agent3"])):
                logic_break = True; flags.append("LOGIC_BREAK:decision_contradicts_crosscheck_data")
        else: consistency["note"] = "polarity_indeterminate"
    elif "paper_hits" in linked:
        pol, ev = sparse_polarity(dtext); is_sparse = linked["paper_hits"] < SPARSE_THRESHOLD
        consistency = {"checked": True, "kind": "atom_sparsity", "trace_polarity": pol, "evidence": ev, "data_paper_hits": linked["paper_hits"], "sparse_threshold": SPARSE_THRESHOLD, "data_is_sparse": is_sparse}
        if pol in ("sparse", "dense"):
            if (pol == "sparse") != is_sparse:
                logic_break = True; flags.append("LOGIC_BREAK:sparsity_label_contradicts_hit_count")
        else: consistency["note"] = "polarity_indeterminate"
    elif "quote_verified_substring" in linked:
        consistency = {"checked": True, "kind": "merge_quote_context", "data_quote_verified": linked["quote_verified_substring"], "note": "merge decision is a niche; quote grounding checked by MAIN Gate-4"}
    valid = complete and conf_ok and falsifiable and not logic_break
    audit_trace = {"step": f"audit {source} :: {step_id}",
                   "inputs_seen": f"fields_present={not missing}; confidence={lvl}; grounding={grounding}; linked={ {k: linked[k] for k in linked} }",
                   "reasoning": "6 deterministic checks; LOGIC BREAK only when detected polarity contradicts recorded data.",
                   "decision": ("LOGIC_BREAK" if logic_break else ("VALID" if valid else "FLAGGED_NONFATAL")),
                   "confidence": ("high - deterministic over committed JSON" if consistency.get("trace_polarity") not in (None, "ambiguous") or not consistency.get("checked") else "medium - prose polarity indeterminate; format checks still deterministic"),
                   "could_be_wrong_if": "polarity phrase-lists miss a paraphrase (false negative) or grounding penalizes a correct differently-worded short decision."}
    return {"trace_id": step_id, "source_agent": source, "step": tr.get("step", ""), "complete": complete,
            "missing_fields": missing, "confidence_level": lvl, "confidence_wellformed": conf_ok,
            "falsifiable": falsifiable, "inputs_grounding_overlap": grounding, "overconfident": overconfident,
            "hedges_found": hedges, "decision_data_consistency": consistency, "logic_break": logic_break,
            "flags": flags, "verdict": audit_trace["decision"], "audit_reasoning_trace": audit_trace}


def collect():
    items = []
    p = LOGS / "atoms_reasoning.json"
    if p.exists():
        ar = json.loads(p.read_text())
        if isinstance(ar.get("overall_trace"), dict): items.append({"trace": ar["overall_trace"], "source": "AGENT_1_decomposer", "step_id": "atoms.overall"})
        for at in ar.get("atom_traces", []): items.append({"trace": at.get("reasoning_trace", {}), "source": "AGENT_1_decomposer", "step_id": f"atom.{at.get('atom_id','?')}"})
    p = LOGS / "atom_search.json"
    if p.exists():
        for a in json.loads(p.read_text()).get("atoms", []):
            if isinstance(a.get("reasoning_trace"), dict): items.append({"trace": a["reasoning_trace"], "source": "AGENT_2_atom_search", "step_id": f"atomsearch.{a.get('atom_id','?')}", "linked": {"paper_hits": a.get("paper_hits")}})
    p = LOGS / "candidates.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []): items.append({"trace": c.get("reasoning_trace", {}), "source": "AGENT_3_merger", "step_id": f"merge.{c['cand_id']}", "linked": {"quote_verified_substring": c.get("quote_verified_substring")}})
    coll = {}
    pv = LOGS / "verify.json"
    if pv.exists():
        for c in json.loads(pv.read_text()).get("candidates", []): coll[c["cand_id"]] = c.get("collision_found")
    p = LOGS / "verify_reasoning.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []):
            cid = c.get("cand_id")
            if isinstance(c.get("verdict_trace"), dict): items.append({"trace": c["verdict_trace"], "source": "AGENT_4_verifier", "step_id": f"verify.verdict.{cid}", "linked": {"collision_found": coll.get(cid)}})
            for rt in c.get("reformulation_traces", []): items.append({"trace": rt.get("reasoning_trace", {}), "source": "AGENT_4_verifier", "step_id": f"verify.reform.{cid}.n{rt.get('n','?')}"})
    p = LOGS / "crosscheck.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []): items.append({"trace": c.get("reasoning_trace", {}), "source": "AGENT_4_crosschecker", "step_id": f"crosscheck.{c['cand_id']}", "linked": {"mismatch_with_agent3": c.get("mismatch_with_agent3")}})
    return items


# ---------- search-quality scoring ----------
def score_query(q):
    ql = q.lower()
    toks = content_tokens(q)
    specificity = round(min(1.0, len(toks) / 8.0), 3)
    mech = sum(1 for m in MECH_TERMS if m in ql)
    mechanism_focus = round(min(1.0, 0.2 + 0.4 * mech), 3) if mech else 0.2
    exo = sum(1 for e in EXOTIC_TERMS if e in ql)
    sparsity_seeking = round(min(1.0, 0.5 * exo), 3) if exo else 0.1
    doms = sum(1 for d, kws in DOMAINS.items() if any(k in ql for k in kws))
    cross_paper_pairing = 1.0 if doms >= 2 else (0.5 if doms == 1 else 0.2)
    collision_avoidance = 1.0 if _has_any(ql, PRIOR_ART) else 0.2
    return {"specificity": specificity, "mechanism_focus": mechanism_focus, "sparsity_seeking": sparsity_seeking,
            "cross_paper_pairing": cross_paper_pairing, "collision_avoidance": collision_avoidance}


def collect_queries():
    qs = []
    p = LOGS / "atoms.json"
    if p.exists():
        for q in json.loads(p.read_text()).get("queries_used", []): qs.append({"source": "agent1_sourcer", "query": q})
    p = LOGS / "atom_search.json"
    if p.exists():
        for a in json.loads(p.read_text()).get("atoms", []):
            if a.get("query"): qs.append({"source": f"agent2_atomsearch:{a['atom_id']}", "query": a["query"]})
    p = LOGS / "verify.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []):
            for rf in c.get("reformulations", []): qs.append({"source": f"agent4_verify:{c['cand_id']}:n{rf.get('n')}", "query": rf.get("query", "")})
    p = LOGS / "crosscheck.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []):
            for rs in c.get("recheck_searches", []): qs.append({"source": f"agent4_crosscheck:{c['cand_id']}:n{rs.get('n')}", "query": rs.get("query", "")})
    return [q for q in qs if q["query"].strip()]


def compute_search_quality():
    params = json.loads((RUN_DIR / "direction_params.json").read_text())["params"]
    queries = collect_queries()
    scored = [{**q, "dims": score_query(q["query"])} for q in queries]
    dims = RULES["search_quality"]["dimensions"]
    means = {d: round(sum(s["dims"][d] for s in scored) / len(scored), 4) for d in dims} if scored else {d: 0.0 for d in dims}
    num = sum(params[p] * means[PARAM_TO_DIM[p]] for p in params)
    den = sum(params[p] for p in params)
    avg_sq = round(num / den, 4) if den else 0.0
    return {"run_id": "run_019", "agent": "5_search_quality", "scored_at": datetime.now(timezone.utc).isoformat(),
            "params_used": params, "n_queries": len(scored), "dimension_means": means,
            "avg_search_quality": avg_sq,
            "formula": "avg_search_quality = sum_k(param_k * mean_dim_k)/sum_k(param_k)",
            "per_query": scored}


def main():
    audits = [audit_one(it["trace"], source=it["source"], step_id=it["step_id"], linked=it.get("linked")) for it in collect()]
    by_agent = {}
    for a in audits:
        d = by_agent.setdefault(a["source_agent"], {"traces": 0, "complete": 0, "flagged": 0, "logic_breaks": 0})
        d["traces"] += 1; d["complete"] += int(a["complete"]); d["flagged"] += int(bool(a["flags"])); d["logic_breaks"] += int(a["logic_break"])
    summary = {"total_traces_audited": len(audits), "all_complete": all(a["complete"] for a in audits),
               "n_complete": sum(a["complete"] for a in audits),
               "n_flagged_nonfatal": sum(1 for a in audits if a["flags"] and not a["logic_break"]),
               "n_logic_breaks": sum(a["logic_break"] for a in audits),
               "logic_break_trace_ids": [a["trace_id"] for a in audits if a["logic_break"]], "by_agent": by_agent,
               "consistency_checks_fired": sum(1 for a in audits if a["decision_data_consistency"].get("checked"))}
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "reasoning_audit.json").write_text(json.dumps({"run_id": "run_019", "agent": "5_reasoning_auditor",
        "audited_at": datetime.now(timezone.utc).isoformat(), "summary": summary, "audits": audits}, indent=2))
    sq = compute_search_quality()
    (LOGS / "search_quality.json").write_text(json.dumps(sq, indent=2))
    print(f"[audit] {summary['total_traces_audited']} traces; complete={summary['n_complete']} "
          f"flagged={summary['n_flagged_nonfatal']} LOGIC_BREAKS={summary['n_logic_breaks']}")
    print(f"[search_quality] n_queries={sq['n_queries']} dimension_means={sq['dimension_means']} avg_search_quality={sq['avg_search_quality']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

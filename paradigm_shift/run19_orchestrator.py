#!/usr/bin/env python3
"""Run 19 MAIN orchestrator — persistent-param multi-epoch convergence + sentence decomposition.

Inherits the PROVEN Run 18/17/16 core UNCHANGED (4-gate filter, per-gate reasoning_trace,
verbatim [REPORT], determinism hash, real-Opus anti-hallucination, sparse_analysis,
REASONING_TRANSPARENCY_REPORT) and adds the Run 16 PERSISTENT-PARAM loop:
  * apply_labels (epoch start): consume lagged labeled_examples -> nudge the 5 params -> persist.
  * finalize: append epoch_history, bump epoch, persist direction_params.json (R10), and report
    avg_search_quality delta + avg_paper_hits delta + niche verdict SEPARATELY (R12). Emits
    queries_to_label.json so the human can label this epoch's searches (drives next epoch's nudge).

Phases: apply_labels | report | gates | finalize
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

THIS_DIR = Path(__file__).parent
RUN_DIR = THIS_DIR / "run_019"
LOGS = RUN_DIR / "logs"
DPARAMS = RUN_DIR / "direction_params.json"
RULES = json.loads((RUN_DIR / "run19_rules.json").read_text())
SPEC = json.loads((THIS_DIR / "spec" / "harness_rules.json").read_text())

COMPOSITE_THRESHOLD = RULES["gates"]["gate_1_composite_threshold"]
QUARANTINE = set(SPEC["quarantined_atoms"])
BELINDA = SPEC["belinda_strict"]
MIN_REFORMULATIONS = SPEC["min_web_search_per_candidate"]
SPARSE_THRESHOLD = RULES["sourcing_method"]["sparse_threshold"]
LEARNING_RATE = RULES["param_update"]["learning_rate"]
PARAM_TO_DIM = RULES["persistent_file"]["param_to_dim"]

PAPER_MARKERS = ("arxiv.org", "doi.org", "semanticscholar", "scholar.google", "aclanthology",
                 "openreview", "biorxiv", "ncbi.nlm.nih.gov", "pubmed", "dl.acm.org", "ieeexplore",
                 "springer", "sciencedirect", "/pdf", ".pdf", "proceedings", "neurips", "openalex",
                 "ssrn", "mdpi", "nature.com", "researchgate", "diva-portal", "pnas.org", "mlr.press",
                 "jmlr", "research.google", "royalsocietypublishing", "science.org", "adsabs", "informs", "aps.org")


def norm(s): return re.sub(r"\s+", " ", (s or "")).strip()
def is_paper(r): blob = (r.get("url", "") + " " + r.get("title", "")).lower(); return any(m in blob for m in PAPER_MARKERS)
def _load(name): return json.loads((LOGS / f"{name}.json").read_text())
def _dp(): return json.loads(DPARAMS.read_text())


# ---------- PARAM UPDATE (Run 16 machinery) ----------
def nudge_from_labels(dp):
    params = dict(dp["params"]); on, div = [], []
    for lab in dp.get("labeled_examples", []):
        dims = lab.get("dims")
        if not dims: continue
        (on if lab.get("label") == "on_target" else div).append(dims)
    def mean(group, dk):
        vals = [g[dk] for g in group if dk in g]; return sum(vals) / len(vals) if vals else None
    nudges = {}
    for pkey, dimkey in PARAM_TO_DIM.items():
        m_on, m_div = mean(on, dimkey), mean(div, dimkey)
        if m_on is None or m_div is None: continue
        signal = m_on - m_div
        new = min(0.95, max(0.05, round(params[pkey] + LEARNING_RATE * signal, 4)))
        if new != params[pkey]:
            nudges[pkey] = {"old": params[pkey], "new": new, "on_mean": round(m_on, 4), "div_mean": round(m_div, 4), "signal": round(signal, 4)}
            params[pkey] = new
    return params, nudges


def cmd_apply_labels(_a):
    dp = _dp(); labels = dp.get("labeled_examples", [])
    if not labels:
        print("[apply_labels] no labels (baseline epoch); params unchanged"); return 0
    params, nudges = nudge_from_labels(dp)
    dp["params"] = params
    dp.setdefault("applied_labels_log", []).append({"applied_for_scored_epoch": dp.get("labels_for_scored_epoch"),
        "n_labels": len(labels), "nudges": nudges, "applied_at": datetime.now(timezone.utc).isoformat()})
    dp["labeled_examples"] = []
    DPARAMS.write_text(json.dumps(dp, indent=2))
    print(f"[apply_labels] consumed {len(labels)} labels; nudges={ {k: (v['old'], v['new']) for k, v in nudges.items()} }")
    return 0


# ---------- [REPORT] ----------
def cmd_report(_a):
    blocks = ["# [REPORT] Run 19 ground-truth log", f"# generated {datetime.now(timezone.utc).isoformat()}",
              "# Each block is a subagent's raw output, injected verbatim.\n"]
    spec = [(1, "atoms", ["atoms", "atoms_reasoning"]), (2, "atom_search", ["atom_search"]),
            (3, "candidates", ["candidates"]), (4, "verify", ["verify", "verify_reasoning"]),
            (5, "crosscheck", ["crosscheck"]), (6, "audit+quality", ["reasoning_audit", "search_quality"])]
    for n, label, files in spec:
        blocks.append(f"\n## [REPORT {n}] {label} (verbatim)")
        for f in files:
            p = LOGS / f"{f}.json"; blocks.append(f"\n### {f}.json")
            blocks += (["```json", p.read_text().rstrip(), "```"] if p.exists() else [f"_MISSING: {p}_"])
    (LOGS / "report_log.md").write_text("\n".join(blocks) + "\n")
    print(f"[report] wrote report_log.md ([REPORT 1-6])"); return 0


# ---------- gates (inherited UNCHANGED) ----------
def gate3_for(cid, verify, crosscheck):
    vrec = next((v for v in verify.get("candidates", []) if v["cand_id"] == cid), None)
    if not vrec: return {"pass": False, "reason": "no verifier record"}
    n = len(vrec.get("reformulations", [])); vc = bool(vrec.get("collision_found"))
    crec = next((c for c in crosscheck.get("candidates", []) if c["cand_id"] == cid), None)
    ov = bool(crec and crec.get("mismatch_with_agent3"))
    return {"pass": n >= MIN_REFORMULATIONS and not vc and not ov, "n_reformulations": n, "required": MIN_REFORMULATIONS, "verifier_collision": vc, "crosscheck_overturned": ov}


def gate4_for(cand, atoms_by_id):
    mech = norm(cand.get("mechanism", "")).lower()
    verbs = sorted(v for v in BELINDA["mechanism_vocab"] if re.search(r"\b" + re.escape(v) + r"\b", mech))
    quote = norm(cand.get("primary_quote", ""))
    src_id = cand.get("atom_a_id") if cand.get("quote_source") == "atom_a" else cand.get("atom_b_id") if cand.get("quote_source") == "atom_b" else None
    src_text = norm(atoms_by_id.get(src_id, {}).get("text", "")) if src_id else ""
    grounded = bool(quote) and len(quote) >= BELINDA["min_verbatim_chars"] and quote in src_text
    not_bare = not re.search(r"\bcombine[sd]?\b", mech) or bool(verbs)
    return {"pass": bool(verbs) and grounded and not_bare, "mechanism_verbs": verbs, "quote_len": len(quote), "quote_grounded": grounded, "quote_source_id": src_id}


def composite_for(cand, verify, g4):
    vrec = next((v for v in verify.get("candidates", []) if v["cand_id"] == cand["cand_id"]), None)
    reforms = vrec.get("reformulations", []) if vrec else []
    paper_hits = sum(1 for rf in reforms for r in rf.get("results", []) if is_paper(r))
    novelty = max(0.0, 1.0 - paper_hits / 20.0)
    params = {"novelty": round(novelty, 4), "mechanism_present": 1.0 if g4["mechanism_verbs"] else 0.0,
              "quote_grounded": 1.0 if g4["quote_grounded"] else 0.0, "cross_atom": 1.0 if cand.get("atom_a_id") != cand.get("atom_b_id") else 0.0}
    weights = {"novelty": 0.55, "mechanism_present": 0.20, "quote_grounded": 0.15, "cross_atom": 0.10}
    return {"composite": round(sum(weights[k] * v for k, v in params.items()), 4), "params": params, "paper_hits_in_verify": paper_hits, "weights": weights}


def _t(step, i, r, d, c, w): return {"step": step, "inputs_seen": i, "reasoning": r, "decision": d, "confidence": c, "could_be_wrong_if": w}


def gate_traces(cid, sc, gate1, ids, qhits, gate2, g3, g4):
    p = sc["params"]
    return {"gate_1_composite": _t(f"Gate 1 (composite>=0.90) {cid}", f"composite={sc['composite']} params={p} paper_hits={sc['paper_hits_in_verify']}",
              f"novelty(0.55 wt)={p['novelty']} from {sc['paper_hits_in_verify']} hits; to clear 0.90 need <=3 hits.", f"{'PASS' if gate1 else 'FAIL'} ({sc['composite']} {'>=' if gate1 else '<'} 0.9)", "high - arithmetic", "AGENT 4 miscounted paper-like hits"),
            "gate_2_quarantine": _t(f"Gate 2 (quarantine) {cid}", f"atoms={sorted(x for x in ids if x)} quarantine={sorted(QUARANTINE)}", "fails iff a source atom is quarantined.", f"{'PASS' if gate2 else 'FAIL'} (hits={qhits})", "high - set membership", "atom id string-collides with a quarantined id"),
            "gate_3_verify": _t(f"Gate 3 (verify XOR crosscheck) {cid}", f"n_reform={g3.get('n_reformulations')} (req {g3.get('required')}); collision={g3.get('verifier_collision')}; overturned={g3.get('crosscheck_overturned')}", "pass iff >=5 reformulations, no collision, not overturned (R7).", f"{'PASS' if g3['pass'] else 'FAIL'}", "high - boolean fusion", "both verify+crosscheck shared a blind spot"),
            "gate_4_belinda": _t(f"Gate 4 (Belinda) {cid}", f"verbs={g4['mechanism_verbs']} quote_len={g4['quote_len']} grounded={g4['quote_grounded']}", "needs a causal verb + >=30-char verbatim quote substring.", f"{'PASS' if g4['pass'] else 'FAIL'}", "high - regex + substring", "mechanism uses a verb outside the Belinda vocab")}


def run_gates(atoms, candidates, verify, crosscheck, with_traces=False):
    abid = {a["atom_id"]: a for a in atoms.get("atoms", [])}; out = []
    for cand in candidates.get("candidates", []):
        cid = cand["cand_id"]; g4 = gate4_for(cand, abid); sc = composite_for(cand, verify, g4)
        gate1 = sc["composite"] >= COMPOSITE_THRESHOLD
        ids = {cand.get("atom_a_id"), cand.get("atom_b_id")}; qhits = sorted(ids & QUARANTINE); gate2 = len(qhits) == 0
        g3 = gate3_for(cid, verify, crosscheck); survived = gate1 and gate2 and g3["pass"] and g4["pass"]
        failed = [g for g, ok in (("gate_1_composite", gate1), ("gate_2_quarantine", gate2), ("gate_3_verify", g3["pass"]), ("gate_4_belinda", g4["pass"])) if not ok]
        rec = {"cand_id": cid, "niche_name": cand.get("niche_name", ""), "composite": sc["composite"], "composite_params": sc["params"],
               "paper_hits_in_verify": sc["paper_hits_in_verify"], "combined_atom_hits": cand.get("combined_atom_hits"),
               "atom_a_hits": cand.get("atom_a_hits"), "atom_b_hits": cand.get("atom_b_hits"),
               "gate_1_composite": {"pass": gate1, "composite": sc["composite"], "threshold": COMPOSITE_THRESHOLD},
               "gate_2_quarantine": {"pass": gate2, "quarantine_hits": qhits}, "gate_3_verify": {"pass": g3["pass"], **g3},
               "gate_4_belinda": {"pass": g4["pass"], **g4}, "survived": survived, "gates_failed": failed}
        if with_traces:
            tr = gate_traces(cid, sc, gate1, ids, qhits, gate2, g3, g4)
            for g in ("gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"): rec[g]["reasoning_trace"] = tr[g]
            ff = failed[0] if failed else None
            rec["survival_reasoning_trace"] = _t(f"survival {cid}", f"passes={{g1:{gate1},g2:{gate2},g3:{g3['pass']},g4:{g4['pass']}}}", "survives iff all four pass (AND); " + (f"fails first at {ff}." if ff else "all passed."), "SURVIVES" if survived else f"ELIMINATED at {ff}", "high - conjunction", "any gate input wrong upstream")
        out.append(rec)
    return out


def verdicts_hash(v):
    skel = [{"c": x["cand_id"], "comp": x["composite"], "g1": x["gate_1_composite"]["pass"], "g2": x["gate_2_quarantine"]["pass"], "g3": x["gate_3_verify"]["pass"], "g4": x["gate_4_belinda"]["pass"], "s": x["survived"]} for x in v]
    return hashlib.sha256(json.dumps(skel, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def cmd_gates(_a):
    atoms, candidates, verify, crosscheck = _load("atoms"), _load("candidates"), _load("verify"), _load("crosscheck")
    v1 = run_gates(*(copy.deepcopy(x) for x in (atoms, candidates, verify, crosscheck)), with_traces=True)
    v2 = run_gates(*(copy.deepcopy(x) for x in (atoms, candidates, verify, crosscheck)))
    h1, h2 = verdicts_hash(v1), verdicts_hash(v2)
    (LOGS / "gate_results.json").write_text(json.dumps(v1, indent=2))
    (LOGS / "determinism_check.json").write_text(json.dumps({"determinism_ok": h1 == h2, "hash_run_1": h1, "hash_run_2": h2, "runs": 2,
        "reasoning_trace": _t("determinism", f"ran gates twice; {h1[:12]} vs {h2[:12]}", "gate math reads only committed JSON, no RNG.", "DETERMINISTIC" if h1 == h2 else "NON-DETERMINISTIC", "high - sha256", "a gate read wall-clock state")}, indent=2))
    survivors = [v for v in v1 if v["survived"]]; epoch = _dp()["epoch"]
    verdict = {"run_id": "run_019", "epoch": epoch, "verdict": "NICHE_FOUND" if survivors else "NICHE_NOT_FOUND",
               "survivors": [{"cand_id": s["cand_id"], "niche_name": s["niche_name"], "composite": s["composite"]} for s in survivors],
               "candidates_scanned": len(v1), "goal_note": "R12: convergence target is search_quality, not niche.", "timestamp": datetime.now(timezone.utc).isoformat()}
    (RUN_DIR / "niche_find_check.json").write_text(json.dumps(verdict, indent=2))
    for v in v1:
        fl = "".join("1" if v[g]["pass"] else "0" for g in ("gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"))
        print(f"  {v['cand_id']}: verify_hits={v['paper_hits_in_verify']} composite={v['composite']:.4f} gates[{fl}] survived={v['survived']}")
    print(f"\n[gates] {verdict['verdict']} ({len(survivors)} survivor); determinism={'OK' if h1 == h2 else 'BROKEN'}")
    return 0


# ---------- anti-hallucination ----------
SUMMARY_PROMPT = """You are writing a strictly factual summary of a multi-agent run (Run 19, epoch {epoch}).
Below is the RAW REPORT LOG (verbatim) and GATE RESULTS (ground truth).

=== RAW REPORT LOG ===
{report}

=== GATE RESULTS (JSON) ===
{gates}

Write 4-7 sentences stating ONLY facts present above (no inference). Then output a raw JSON object (no fences) with EXACTLY:
{{"n_candidates": <int>, "n_survivors": <int>, "verdict": "<NICHE_FOUND|NICHE_NOT_FOUND>", "avg_search_quality": <number>, "n_logic_breaks": <int>, "per_candidate": [{{"cand_id": "<id>", "composite": <number>, "survived": <bool>}}]}}"""


def run_opus(prompt):
    cfg = RULES["opus_subprocess"]; cmd = [cfg["binary"], *cfg["args"], "--disallowedTools", *cfg["disallowed_tools"]]
    td = tempfile.mkdtemp(prefix="run19_sum_")
    proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=cfg["timeout_seconds"], cwd=td)
    if proc.returncode != 0: raise RuntimeError(f"opus exit {proc.returncode}: {proc.stderr[:400]}")
    return json.loads(proc.stdout)


def parse_obj(text):
    text = (text or "").strip()
    try: return json.loads(text)
    except json.JSONDecodeError: pass
    for b in reversed(re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)):
        try: return json.loads(b)
        except json.JSONDecodeError: continue
    found, start = [], text.find("{")
    while start != -1:
        depth, end = 0, None
        for i in range(start, len(text)):
            if text[i] == "{": depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    try: found.append(json.loads(text[start:i + 1]))
                    except json.JSONDecodeError: pass
                    break
        start = text.find("{", (end + 1) if end is not None else start + 1)
    return found[-1] if found else None


def _mdt(tr, ind=""):
    if not isinstance(tr, dict) or not tr: return ind + "_(no reasoning_trace)_\n"
    f = lambda k: norm(str(tr.get(k, "")))
    return "".join(f"{ind}- **{k}:** {f(k)}\n" for k in ("step", "inputs_seen", "reasoning", "decision", "confidence", "could_be_wrong_if"))


def build_sparse_analysis(gate_results):
    asearch = _load("atom_search")["atoms"]
    per_atom = [{"atom_id": a["atom_id"], "sub_mechanism": a.get("sub_mechanism", ""), "paper_hits": a["paper_hits"], "sparse": a["paper_hits"] < SPARSE_THRESHOLD, "is_mechanism": a.get("is_mechanism", True)} for a in asearch]
    cvh = [v["paper_hits_in_verify"] for v in gate_results]
    return {"sparse_threshold": SPARSE_THRESHOLD, "n_atoms": len(per_atom), "per_atom_hits": per_atom,
            "per_atom_hits_sorted": sorted(a["paper_hits"] for a in per_atom),
            "n_sparse_atoms": sum(1 for a in per_atom if a["sparse"]), "candidate_verify_hits": cvh,
            "avg_paper_hits": round(sum(cvh) / len(cvh), 4) if cvh else 0.0, "min_candidate_verify_hits": min(cvh) if cvh else None}


def build_transparency_report(verdict, gate_results, audit, sparse, sq, dp_before, epoch_entry, prev):
    atoms = _load("atoms"); ar = json.loads((LOGS / "atoms_reasoning.json").read_text()) if (LOGS / "atoms_reasoning.json").exists() else {}
    cands = _load("candidates")["candidates"]; verify = _load("verify")["candidates"]
    vr = json.loads((LOGS / "verify_reasoning.json").read_text()).get("candidates", []) if (LOGS / "verify_reasoning.json").exists() else []
    cc = _load("crosscheck")["candidates"]; by = lambda l, cid: next((x for x in l if x.get("cand_id") == cid), {})
    atr = {t.get("atom_id"): t.get("reasoning_trace", {}) for t in ar.get("atom_traces", [])}
    gres = {g["cand_id"]: g for g in gate_results}; aud = {a["trace_id"]: a for a in audit.get("audits", [])}
    hitsmap = {a["atom_id"]: a for a in sparse["per_atom_hits"]}
    sq_d, pq_d = epoch_entry.get("avg_search_quality"), epoch_entry.get("avg_paper_hits")
    sq_delta = round(sq_d - prev["avg_search_quality"], 4) if prev else None
    ph_delta = round(pq_d - prev["avg_paper_hits"], 4) if prev else None
    L = ["# Run 19 - REASONING TRANSPARENCY REPORT (epoch %d)" % dp_before["epoch"],
         f"_generated {datetime.now(timezone.utc).isoformat()} - persistent-param convergence + sentence decomposition_\n",
         f"**VERDICT: {verdict['verdict']}** ({len(verdict['survivors'])}/{verdict['candidates_scanned']})  |  "
         f"**avg_search_quality={sq_d}** (delta {sq_delta})  |  **avg_paper_hits={pq_d}** (delta {ph_delta})  |  "
         f"logic-breaks={audit['summary']['n_logic_breaks']}/{audit['summary']['total_traces_audited']}\n",
         "> R12: convergence target = search_quality (label-driven ground truth). niche verdict is reported separately and is expected to stay 0 (saturation).\n",
         "## CONVERGENCE STATE (persistent direction_params.json, R10)\n",
         f"- epoch (scored): **{dp_before['epoch']}**  ->  next epoch written: **{dp_before['epoch']+1}**",
         f"- params this epoch: `{dp_before['params']}`",
         f"- avg_search_quality = {sq_d} (formula {sq['formula']}); dimension_means = {sq['dimension_means']}",
         f"- avg_paper_hits (per-candidate verify) = {pq_d}",
         f"- epoch_history len now {len(prev_history())}; labels applied this epoch: {len(dp_before.get('labeled_examples', []))} (baseline if 0)\n",
         "## STAGE 0 - Atom sourcing (AGENT 1)\n"]
    if ar.get("overall_trace"): L.append("**Overall decomposition trace:**\n" + _mdt(ar["overall_trace"]))
    for a in atoms.get("atoms", []):
        h = hitsmap.get(a["atom_id"], {})
        L.append(f"\n### {a['atom_id']} ({a.get('paper_id')}, {a.get('domain','?')}) hits={h.get('paper_hits','?')} {'SPARSE' if h.get('sparse') else 'dense'} mech={h.get('is_mechanism')}")
        L.append(f"_{a.get('sub_mechanism','')}_  ·  `{a.get('source_id','')}`")
        L.append(f"> {norm(a.get('text',''))}\n" + _mdt(atr.get(a['atom_id'], {})))
    L.append("\n## STAGE 2 - Per-atom saturation (AGENT 2) [R10]\n| atom | hits | sparse | mech |\n|---|---|---|---|")
    for a in sorted(sparse["per_atom_hits"], key=lambda x: x["paper_hits"]):
        L.append(f"| {a['atom_id']} | {a['paper_hits']} | {'Y' if a['sparse'] else 'n'} | {'Y' if a['is_mechanism'] else 'n'} |")
    L.append("\n## STAGE 3-5 - Per candidate (sparsest pairs)\n")
    for cand in cands:
        cid = cand["cand_id"]; g = gres.get(cid, {})
        L.append(f"\n### {cid} - {cand.get('niche_name','')}")
        L.append(f"`{cand.get('atom_a_id')}(h={cand.get('atom_a_hits')}) x {cand.get('atom_b_id')}(h={cand.get('atom_b_hits')})` -> verify_hits={g.get('paper_hits_in_verify')}, composite {g.get('composite')}, survived={g.get('survived')}, failed={g.get('gates_failed')}")
        L.append("**MERGE (A3):** " + norm(cand.get("mechanism", "")) + "\n" + _mdt(cand.get("reasoning_trace", {}), "  "))
        v, vrr = by(verify, cid), by(vr, cid)
        L.append(f"**VERIFY (A4):** collision={v.get('collision_found')}, {len(v.get('reformulations',[]))} reformulations, {g.get('paper_hits_in_verify')} hits")
        if vrr.get("verdict_trace"): L.append(_mdt(vrr["verdict_trace"], "  "))
        c = by(cc, cid); L.append(f"**CROSS-CHECK (A4):** agent4_collision={c.get('agent4_collision')}, mismatch={c.get('mismatch_with_agent3')}")
        if c.get("reasoning_trace"): L.append(_mdt(c["reasoning_trace"], "  "))
        L.append("**GATES:**")
        for gk, lbl in (("gate_1_composite", "G1 composite>=0.90"), ("gate_2_quarantine", "G2 quarantine"), ("gate_3_verify", "G3 verify XOR crosscheck"), ("gate_4_belinda", "G4 Belinda")):
            gd = g.get(gk, {}); L.append(f"_{lbl}: {'PASS' if gd.get('pass') else 'FAIL'}_\n" + _mdt(gd.get("reasoning_trace", {}), "  "))
        L.append(f"**SURVIVAL:** {g.get('survival_reasoning_trace',{}).get('decision','?')}")
    s = audit["summary"]
    L.append("\n## STAGE 6 - AGENT 5 audit + search-quality\n")
    L.append(f"- traces {s['total_traces_audited']}, complete {s['n_complete']}, **logic-breaks {s['n_logic_breaks']}**, consistency checks {s['consistency_checks_fired']}, non-fatal flags {s['n_flagged_nonfatal']}")
    L.append(f"- search_quality over {sq['n_queries']} real queries: dimension_means {sq['dimension_means']}, **avg_search_quality {sq_d}**")
    L.append("\n## END-TO-END (epoch %d)\n" % dp_before["epoch"])
    L.append(f"Persistent params {dp_before['params']} -> sourced+decomposed -> per-atom saturation -> sparsest pairs merged -> verified+crosschecked -> 4 gates -> audited. "
             f"**{verdict['verdict']}** ({len(verdict['survivors'])} survivors). avg_search_quality={sq_d} (delta {sq_delta}), avg_paper_hits={pq_d} (delta {ph_delta}). "
             f"{s['total_traces_audited']} decision points, {s['n_logic_breaks']} logic-breaks. Convergence target is search_quality; niche saturation is expected and reported honestly (R12).")
    return "\n".join(L) + "\n"


_HIST_CACHE = []
def prev_history(): return _HIST_CACHE


def cmd_finalize(_a):
    global _HIST_CACHE
    verdict = json.loads((RUN_DIR / "niche_find_check.json").read_text())
    gate_results = _load("gate_results"); audit = _load("reasoning_audit"); sq = _load("search_quality")
    sparse = build_sparse_analysis(gate_results)
    (RUN_DIR / "sparse_analysis.json").write_text(json.dumps(sparse, indent=2))
    dp_before = _dp(); _HIST_CACHE = list(dp_before.get("epoch_history", []))
    prev = dp_before["epoch_history"][-1] if dp_before.get("epoch_history") else None
    epoch_entry = {"epoch": dp_before["epoch"], "avg_search_quality": sq["avg_search_quality"],
                   "avg_paper_hits": sparse["avg_paper_hits"], "params": dict(dp_before["params"])}
    # anti-hallucination
    truth = {"n_candidates": verdict["candidates_scanned"], "n_survivors": len(verdict["survivors"]), "verdict": verdict["verdict"],
             "avg_search_quality": sq["avg_search_quality"], "n_logic_breaks": audit["summary"]["n_logic_breaks"],
             "per_candidate": [{"cand_id": v["cand_id"], "composite": round(v["composite"], 4), "survived": v["survived"]} for v in gate_results]}
    env = run_opus(SUMMARY_PROMPT.format(epoch=dp_before["epoch"], report=(LOGS / "report_log.md").read_text(), gates=json.dumps(gate_results, indent=2)))
    summary = env.get("result", ""); (LOGS / "summary_llm.md").write_text(f"# LLM summary (session {env.get('session_id')})\n\n{summary}\n")
    claimed = parse_obj(summary); mism = []
    if claimed is None: mism = ["no parseable claim block"]
    else:
        for k in ("n_candidates", "n_survivors", "verdict", "n_logic_breaks"):
            if claimed.get(k) != truth[k]: mism.append(f"{k}: {claimed.get(k)!r}!={truth[k]!r}")
        try:
            if abs(float(claimed.get("avg_search_quality")) - float(truth["avg_search_quality"])) > 1e-4: mism.append("avg_search_quality mismatch")
        except (TypeError, ValueError): mism.append("avg_search_quality not numeric")
        tby = {c["cand_id"]: c for c in truth["per_candidate"]}
        for c in claimed.get("per_candidate", []):
            t = tby.get(c.get("cand_id"))
            if not t: mism.append(f"fabricated {c.get('cand_id')!r}"); continue
            try:
                if abs(float(c.get("composite")) - float(t["composite"])) > 1e-4: mism.append(f"{c['cand_id']} composite")
            except (TypeError, ValueError): mism.append(f"{c.get('cand_id')} composite nan")
            if bool(c.get("survived")) != bool(t["survived"]): mism.append(f"{c['cand_id']} survived")
    hall = {"hallucination_detected": bool(mism), "no_hallucination": not mism, "mismatches": mism, "truth": truth, "claimed": claimed}
    (LOGS / "hallucination_check.json").write_text(json.dumps(hall, indent=2))
    # transparency report
    (RUN_DIR / "REASONING_TRANSPARENCY_REPORT.md").write_text(build_transparency_report(verdict, gate_results, audit, sparse, sq, dp_before, epoch_entry, prev))
    # PARAM PERSIST (R10): append history, bump epoch, await labels for this scored epoch
    queries_for_label = [{"query": q["query"], "source": q["source"], "dims": q["dims"], "label": None} for q in sq["per_query"]]
    (RUN_DIR / "queries_to_label.json").write_text(json.dumps({"run_id": "run_019", "scored_epoch": dp_before["epoch"],
        "instructions": "For each query set label to 'on_target' or 'diverge', then paste this list into direction_params.json.labeled_examples and set labels_for_scored_epoch before running epoch %d." % (dp_before["epoch"] + 1),
        "queries": queries_for_label}, indent=2))
    dp_after = {"run_id": "run_019", "epoch": dp_before["epoch"] + 1, "scored_epoch": dp_before["epoch"],
                "params": dict(dp_before["params"]), "labeled_examples": [], "labels_for_scored_epoch": dp_before["epoch"],
                "epoch_history": list(dp_before.get("epoch_history", [])) + [epoch_entry],
                "applied_labels_log": dp_before.get("applied_labels_log", []),
                "note": "PERSISTENT (R10). Label queries_to_label.json -> paste into labeled_examples -> run apply_labels at epoch %d start." % (dp_before["epoch"] + 1),
                "updated_at": datetime.now(timezone.utc).isoformat()}
    DPARAMS.write_text(json.dumps(dp_after, indent=2))
    sq_delta = round(epoch_entry["avg_search_quality"] - prev["avg_search_quality"], 4) if prev else None
    ph_delta = round(epoch_entry["avg_paper_hits"] - prev["avg_paper_hits"], 4) if prev else None
    det = json.loads((LOGS / "determinism_check.json").read_text())
    proofs = {"agents_all_committed": all((LOGS / f"{f}.json").exists() for f in ("atoms", "atoms_reasoning", "atom_search", "candidates", "verify", "verify_reasoning", "crosscheck", "reasoning_audit", "search_quality")),
              "report_verbatim": "[REPORT 6]" in (LOGS / "report_log.md").read_text(), "four_gate_deterministic": det["determinism_ok"],
              "no_hallucination": hall["no_hallucination"],
              "every_gate_has_reasoning_trace": all(all(isinstance(v.get(g, {}).get("reasoning_trace"), dict) for g in ("gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda")) for v in gate_results),
              "all_traces_complete": audit["summary"]["all_complete"], "per_atom_hits_reported": sparse["n_atoms"] > 0,
              "search_quality_computed": isinstance(sq.get("avg_search_quality"), (int, float)),
              "params_persisted": dp_after["epoch"] == dp_before["epoch"] + 1 and len(dp_after["epoch_history"]) == len(dp_before.get("epoch_history", [])) + 1,
              "queries_emitted_for_labeling": (RUN_DIR / "queries_to_label.json").exists(),
              "transparency_report_written": (RUN_DIR / "REASONING_TRANSPARENCY_REPORT.md").exists()}
    (RUN_DIR / "proof_scorecard.json").write_text(json.dumps({"proofs": proofs, "all_pass": all(proofs.values()), "verdict": verdict["verdict"],
        "scored_epoch": dp_before["epoch"], "next_epoch": dp_after["epoch"], "avg_search_quality": epoch_entry["avg_search_quality"],
        "avg_search_quality_delta": sq_delta, "avg_paper_hits": epoch_entry["avg_paper_hits"], "avg_paper_hits_delta": ph_delta,
        "n_survivors": truth["n_survivors"], "n_logic_breaks": truth["n_logic_breaks"], "generated_at": datetime.now(timezone.utc).isoformat()}, indent=2))
    print(f"VERDICT: {verdict['verdict']} survivors={truth['n_survivors']} | avg_search_quality={epoch_entry['avg_search_quality']} (delta {sq_delta}) | avg_paper_hits={epoch_entry['avg_paper_hits']} (delta {ph_delta})")
    print(f"params epoch {dp_before['epoch']} -> {dp_after['epoch']} (persisted); no_hallucination={hall['no_hallucination']} logic_breaks={truth['n_logic_breaks']}")
    for k, ok in proofs.items(): print(f"  [{'PASS' if ok else 'FAIL'}] {k}")
    return 0 if all(proofs.values()) else 1


def main(argv):
    ap = argparse.ArgumentParser(); ap.add_argument("phase", choices=["apply_labels", "report", "gates", "finalize"])
    args = ap.parse_args(argv); LOGS.mkdir(parents=True, exist_ok=True)
    return {"apply_labels": cmd_apply_labels, "report": cmd_report, "gates": cmd_gates, "finalize": cmd_finalize}[args.phase](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

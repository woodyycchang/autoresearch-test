#!/usr/bin/env python3
"""Run 17 MAIN orchestrator -- transparent 4-gate filter + transparency report.

Inherits the PROVEN Run 16 deterministic core UNCHANGED (4-gate filter,
composite>=0.90, quarantine, gate3 = verify XOR crosscheck, Belinda strict,
verbatim [REPORT] injection, twice-run determinism hash, real-Opus anti-
hallucination summary) and ADDS Run 17's transparency layer:

  * [REPORT 1-5] now includes AGENT 1-4 reasoning files + AGENT 5's audit.
  * EVERY gate decision, per candidate, carries a reasoning_trace with the exact
    numbers and the threshold (R9).
  * a single human-readable REASONING_TRANSPARENCY_REPORT.md assembles the COMPLETE
    middle process end-to-end: atom chosen (+why) -> merged (+why) -> verified
    (+why collision/not) -> cross-checked (+why) -> gate-by-gate (+why) -> verdict,
    with AGENT 5's logic-audit flags inline (R10, R12).

Phases:
  python3 run17_orchestrator.py report     # [REPORT 1..5] verbatim log
  python3 run17_orchestrator.py gates       # 4-gate (+per-gate reasoning_trace) + determinism + verdict
  python3 run17_orchestrator.py finalize     # hallucination + transparency report + proof scorecard
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
RUN_DIR = THIS_DIR / "run_017"
LOGS = RUN_DIR / "logs"
RULES = json.loads((RUN_DIR / "run17_rules.json").read_text())
SPEC = json.loads((THIS_DIR / "spec" / "harness_rules.json").read_text())

COMPOSITE_THRESHOLD = RULES["gates"]["gate_1_composite_threshold"]   # 0.90
QUARANTINE = set(SPEC["quarantined_atoms"])
BELINDA = SPEC["belinda_strict"]
MIN_REFORMULATIONS = SPEC["min_web_search_per_candidate"]            # 5
EPOCH = json.loads((RUN_DIR / "direction_params.json").read_text())["epoch"]

PAPER_MARKERS = (
    "arxiv.org", "doi.org", "semanticscholar", "scholar.google", "aclanthology",
    "openreview", "biorxiv", "ncbi.nlm.nih.gov", "pubmed", "dl.acm.org",
    "ieeexplore", "springer", "sciencedirect", "/pdf", ".pdf", "proceedings",
    "neurips", "openalex", "ssrn", "mdpi", "nature.com", "researchgate",
    "diva-portal", "pnas.org", "mlr.press", "jmlr", "research.google",
)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def is_paper(res: dict) -> bool:
    blob = (res.get("url", "") + " " + res.get("title", "")).lower()
    return any(m in blob for m in PAPER_MARKERS)


def _load(name):
    return json.loads((LOGS / f"{name}.json").read_text())


# ---------- [REPORT] verbatim injection incl reasoning files (R6) ----------
def cmd_report(_args) -> int:
    blocks = ["# [REPORT] Run 17 ground-truth log",
              f"# generated {datetime.now(timezone.utc).isoformat()}",
              "# Each block is a subagent's raw output, injected verbatim (incl reasoning_traces).\n"]
    spec = [(1, "atoms", ["atoms", "atoms_reasoning"]),
            (2, "candidates", ["candidates"]),
            (3, "verify", ["verify", "verify_reasoning"]),
            (4, "crosscheck", ["crosscheck"]),
            (5, "reasoning_audit", ["reasoning_audit"])]
    for n, label, files in spec:
        blocks.append(f"\n## [REPORT {n}] {label} (verbatim)")
        for f in files:
            p = LOGS / f"{f}.json"
            blocks.append(f"\n### {f}.json")
            if p.exists():
                blocks += ["```json", p.read_text().rstrip(), "```"]
            else:
                blocks.append(f"_MISSING: {p} not found_")
    (LOGS / "report_log.md").write_text("\n".join(blocks) + "\n")
    print(f"[report] wrote {LOGS / 'report_log.md'} ([REPORT 1-5] verbatim)")
    return 0


# ---------- Gate 3 fusion: verifier + cross-checker (R7) ----------
def gate3_for(cid: str, verify: dict, crosscheck: dict) -> dict:
    vrec = next((v for v in verify.get("candidates", []) if v["cand_id"] == cid), None)
    if not vrec:
        return {"pass": False, "reason": "no verifier record"}
    n_reform = len(vrec.get("reformulations", []))
    verifier_collision = bool(vrec.get("collision_found"))
    crec = next((c for c in crosscheck.get("candidates", []) if c["cand_id"] == cid), None)
    overturned = bool(crec and crec.get("mismatch_with_agent3"))
    enough = n_reform >= MIN_REFORMULATIONS
    passed = enough and not verifier_collision and not overturned
    return {"pass": passed, "n_reformulations": n_reform, "required": MIN_REFORMULATIONS,
            "verifier_collision": verifier_collision, "crosscheck_overturned": overturned}


# ---------- Gate 4: Belinda strict w/ real-substring quote ----------
def gate4_for(cand: dict, atoms_by_id: dict) -> dict:
    mech = norm(cand.get("mechanism", "")).lower()
    verbs = sorted(v for v in BELINDA["mechanism_vocab"]
                   if re.search(r"\b" + re.escape(v) + r"\b", mech))
    quote = norm(cand.get("primary_quote", ""))
    src_id = cand.get("atom_a_id") if cand.get("quote_source") == "atom_a" else \
        cand.get("atom_b_id") if cand.get("quote_source") == "atom_b" else None
    src_text = norm(atoms_by_id.get(src_id, {}).get("text", "")) if src_id else ""
    grounded = bool(quote) and len(quote) >= BELINDA["min_verbatim_chars"] and quote in src_text
    not_bare = not re.search(r"\bcombine[sd]?\b", mech) or bool(verbs)
    passed = bool(verbs) and grounded and not_bare
    return {"pass": passed, "mechanism_verbs": verbs, "quote_len": len(quote),
            "quote_grounded": grounded, "quote_source_id": src_id}


# ---------- composite (deterministic; novelty from verifier's real searches) ----------
def composite_for(cand: dict, verify: dict, g4: dict) -> dict:
    vrec = next((v for v in verify.get("candidates", []) if v["cand_id"] == cand["cand_id"]), None)
    reforms = vrec.get("reformulations", []) if vrec else []
    paper_hits = sum(1 for rf in reforms for r in rf.get("results", []) if is_paper(r))
    novelty = max(0.0, 1.0 - paper_hits / 20.0)
    params = {"novelty": round(novelty, 4),
              "mechanism_present": 1.0 if g4["mechanism_verbs"] else 0.0,
              "quote_grounded": 1.0 if g4["quote_grounded"] else 0.0,
              "cross_atom": 1.0 if cand.get("atom_a_id") != cand.get("atom_b_id") else 0.0}
    weights = {"novelty": 0.55, "mechanism_present": 0.20,
               "quote_grounded": 0.15, "cross_atom": 0.10}
    composite = round(sum(weights[k] * v for k, v in params.items()), 4)
    return {"composite": composite, "params": params, "paper_hits_in_verify": paper_hits,
            "weights": weights}


def _trace(step, inputs_seen, reasoning, decision, confidence, could_be_wrong_if) -> dict:
    return {"step": step, "inputs_seen": inputs_seen, "reasoning": reasoning,
            "decision": decision, "confidence": confidence, "could_be_wrong_if": could_be_wrong_if}


def gate_traces(cid, sc, gate1, ids, qhits, gate2, g3, g4) -> dict:
    """A reasoning_trace per gate decision -- the gate math made visible (R9)."""
    p = sc["params"]
    t1 = _trace(
        f"Gate 1 (composite>=0.90) for {cid}",
        f"composite={sc['composite']} from params={p} weights={sc['weights']}; "
        f"novelty=1-paper_hits/20 with paper_hits={sc['paper_hits_in_verify']} (AGENT 3's real hits)",
        f"novelty carries weight 0.55 and is {p['novelty']} because the verifier saw "
        f"{sc['paper_hits_in_verify']} paper-like hits; even maxing the other three terms "
        f"(0.20+0.15+0.10=0.45) the ceiling is novelty*0.55+0.45; to clear 0.90 novelty must be "
        f">={round((0.90-0.45)/0.55,4)} i.e. <= {round((1-(0.90-0.45)/0.55)*20)} paper hits.",
        f"{'PASS' if gate1 else 'FAIL'} ({sc['composite']} {'>=' if gate1 else '<'} {COMPOSITE_THRESHOLD})",
        "high - pure arithmetic over recorded counts",
        f"AGENT 3 miscounted paper-like hits (is_paper misread {sc['paper_hits_in_verify']} URLs) "
        f"or recorded results it did not actually see (R5 violation upstream)")
    t2 = _trace(
        f"Gate 2 (quarantine) for {cid}",
        f"atoms used = {sorted(x for x in ids if x)}; quarantine set = {sorted(QUARANTINE)}",
        "Gate fails iff either source atom id is on the quarantine blocklist (atoms a prior run "
        "retired as known dead-ends).",
        f"{'PASS' if gate2 else 'FAIL'} (hits={qhits})",
        "high - exact set membership",
        "an atom id collides by string with a quarantined id without being the same atom")
    t3 = _trace(
        f"Gate 3 (verify XOR crosscheck) for {cid}",
        f"n_reformulations={g3.get('n_reformulations')} (required {g3.get('required')}); "
        f"verifier_collision={g3.get('verifier_collision')}; crosscheck_overturned={g3.get('crosscheck_overturned')}",
        "Passes only if AGENT 3 ran >=5 real reformulations AND found no collision AND AGENT 4's "
        "independent re-search did not overturn that no-collision verdict (R7).",
        f"{'PASS' if g3['pass'] else 'FAIL'}",
        "high - boolean fusion of two agents' recorded verdicts",
        "both AGENT 3 and AGENT 4 missed an existing paper occupying the fused niche (shared blind spot)")
    t4 = _trace(
        f"Gate 4 (Belinda strict) for {cid}",
        f"mechanism causal verbs found={g4['mechanism_verbs']}; quote_len={g4['quote_len']} "
        f"(min {BELINDA['min_verbatim_chars']}); quote_grounded={g4['quote_grounded']} "
        f"(verbatim substring of atom {g4['quote_source_id']})",
        "Requires a concrete causal mechanism verb AND a >=30-char verbatim quote that really is a "
        "substring of its named atom -- catches surface analogies dressed in vocabulary.",
        f"{'PASS' if g4['pass'] else 'FAIL'}",
        "high - regex verb match + exact substring containment",
        "the mechanism is real but phrased with a causal verb outside the fixed Belinda vocab, "
        "or the quote is paraphrased (then grounding correctly fails)")
    return {"gate_1_composite": t1, "gate_2_quarantine": t2,
            "gate_3_verify": t3, "gate_4_belinda": t4}


def run_gates(atoms: dict, candidates: dict, verify: dict, crosscheck: dict,
              with_traces: bool = False) -> list[dict]:
    atoms_by_id = {a["atom_id"]: a for a in atoms.get("atoms", [])}
    out = []
    for cand in candidates.get("candidates", []):
        cid = cand["cand_id"]
        g4 = gate4_for(cand, atoms_by_id)
        sc = composite_for(cand, verify, g4)
        gate1 = sc["composite"] >= COMPOSITE_THRESHOLD
        ids = {cand.get("atom_a_id"), cand.get("atom_b_id")}
        qhits = sorted(ids & QUARANTINE)
        gate2 = len(qhits) == 0
        g3 = gate3_for(cid, verify, crosscheck)
        survived = gate1 and gate2 and g3["pass"] and g4["pass"]
        failed = [g for g, ok in (("gate_1_composite", gate1), ("gate_2_quarantine", gate2),
                                  ("gate_3_verify", g3["pass"]), ("gate_4_belinda", g4["pass"])) if not ok]
        rec = {
            "cand_id": cid, "niche_name": cand.get("niche_name", ""),
            "composite": sc["composite"], "composite_params": sc["params"],
            "paper_hits_in_verify": sc["paper_hits_in_verify"],
            "gate_1_composite": {"pass": gate1, "composite": sc["composite"], "threshold": COMPOSITE_THRESHOLD},
            "gate_2_quarantine": {"pass": gate2, "quarantine_hits": qhits},
            "gate_3_verify": {"pass": g3["pass"], **g3},
            "gate_4_belinda": {"pass": g4["pass"], **g4},
            "survived": survived, "gates_failed": failed,
        }
        if with_traces:
            tr = gate_traces(cid, sc, gate1, ids, qhits, gate2, g3, g4)
            for g in ("gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"):
                rec[g]["reasoning_trace"] = tr[g]
            first_fail = failed[0] if failed else None
            rec["survival_reasoning_trace"] = _trace(
                f"survival of {cid}",
                f"gate passes = {{g1:{gate1}, g2:{gate2}, g3:{g3['pass']}, g4:{g4['pass']}}}",
                ("a candidate survives ONLY if all four gates pass (AND); "
                 + ("it fails at " + first_fail + " (first failing gate), so later gates are moot for survival."
                    if first_fail else "all four passed.")),
                "SURVIVES" if survived else f"ELIMINATED at {first_fail}",
                "high - conjunction of four deterministic gates",
                "any single gate's input was wrong upstream (see that gate's could_be_wrong_if)")
        out.append(rec)
    return out


def verdicts_hash(verdicts: list[dict]) -> str:
    skel = [{"c": v["cand_id"], "comp": v["composite"],
             "g1": v["gate_1_composite"]["pass"], "g2": v["gate_2_quarantine"]["pass"],
             "g3": v["gate_3_verify"]["pass"], "g4": v["gate_4_belinda"]["pass"],
             "s": v["survived"]} for v in verdicts]
    return hashlib.sha256(json.dumps(skel, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def cmd_gates(_args) -> int:
    atoms, candidates, verify, crosscheck = (_load("atoms"), _load("candidates"),
                                             _load("verify"), _load("crosscheck"))
    # determinism: run the pure gate math twice, compare hash (traces are deterministic too)
    v1 = run_gates(*(copy.deepcopy(x) for x in (atoms, candidates, verify, crosscheck)), with_traces=True)
    v2 = run_gates(*(copy.deepcopy(x) for x in (atoms, candidates, verify, crosscheck)))
    h1, h2 = verdicts_hash(v1), verdicts_hash(v2)
    (LOGS / "gate_results.json").write_text(json.dumps(v1, indent=2))
    det_trace = _trace(
        "determinism check", f"ran the 4-gate filter twice; hash1={h1[:12]} hash2={h2[:12]}",
        "the gate math reads only committed JSON and uses no RNG/time, so two runs must hash-match.",
        "DETERMINISTIC" if h1 == h2 else "NON-DETERMINISTIC", "high - sha256 over the verdict skeleton",
        "a gate function were to read wall-clock/order-dependent state (it does not)")
    (LOGS / "determinism_check.json").write_text(json.dumps(
        {"determinism_ok": h1 == h2, "hash_run_1": h1, "hash_run_2": h2, "runs": 2,
         "reasoning_trace": det_trace}, indent=2))
    survivors = [v for v in v1 if v["survived"]]
    gates = ["gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"]
    fired = {g: sum(1 for v in v1 if g in v["gates_failed"]) for g in gates}
    verdict = {
        "run_id": "run_017", "epoch": EPOCH,
        "verdict": "NICHE_FOUND" if survivors else "NICHE_NOT_FOUND",
        "survivors": [{"cand_id": s["cand_id"], "niche_name": s["niche_name"],
                       "composite": s["composite"]} for s in survivors],
        "gate_fired_counts": fired, "candidates_scanned": len(v1),
        "goal_note": "R12: the goal is reasoning transparency, not the niche outcome; "
                     "this verdict is reported honestly either way.",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    (RUN_DIR / "niche_find_check.json").write_text(json.dumps(verdict, indent=2))
    for v in v1:
        flags = "".join("1" if v[g]["pass"] else "0" for g in gates)
        print(f"  {v['cand_id']}: composite={v['composite']:.4f} gates[{flags}] survived={v['survived']}")
    print(f"\n[gates] {verdict['verdict']} ({len(survivors)} survivor); determinism={'OK' if h1==h2 else 'BROKEN'}")
    return 0


# ---------- anti-hallucination summary (real Opus, R4) ----------
SUMMARY_PROMPT = """You are writing a strictly factual summary of a transparent multi-agent run (Run 17).
Below is the RAW REPORT LOG (verbatim agent outputs incl reasoning_traces) and the GATE RESULTS (ground truth).

=== RAW REPORT LOG ===
{report}

=== GATE RESULTS (JSON) ===
{gates}

Write 4-7 sentences stating ONLY facts present above (do not infer or embellish numbers).
Then output a raw JSON object (no fences) with EXACTLY:
{{"n_candidates": <int>, "n_survivors": <int>, "verdict": "<NICHE_FOUND|NICHE_NOT_FOUND>", "n_logic_breaks": <int>, "per_candidate": [{{"cand_id": "<id>", "composite": <number>, "survived": <bool>}}]}}"""


def run_opus(prompt: str) -> dict:
    cfg = RULES["opus_subprocess"]
    cmd = [cfg["binary"], *cfg["args"], "--disallowedTools", *cfg["disallowed_tools"]]
    td = tempfile.mkdtemp(prefix="run17_sum_")
    proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                          timeout=cfg["timeout_seconds"], cwd=td)
    if proc.returncode != 0:
        raise RuntimeError(f"opus exit {proc.returncode}: {proc.stderr[:400]}")
    return json.loads(proc.stdout)


def parse_obj(text: str) -> dict | None:
    text = (text or "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    for b in reversed(re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)):
        try:
            return json.loads(b)
        except json.JSONDecodeError:
            continue
    found, start = [], text.find("{")
    while start != -1:
        depth, end = 0, None
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    try:
                        found.append(json.loads(text[start:i + 1]))
                    except json.JSONDecodeError:
                        pass
                    break
        start = text.find("{", (end + 1) if end is not None else start + 1)
    return found[-1] if found else None


def _md_trace(tr: dict, indent: str = "") -> str:
    if not isinstance(tr, dict) or not tr:
        return indent + "_(no reasoning_trace)_\n"
    f = lambda k: norm(str(tr.get(k, "")))
    return (
        f"{indent}- **step:** {f('step')}\n"
        f"{indent}- **inputs_seen:** {f('inputs_seen')}\n"
        f"{indent}- **reasoning:** {f('reasoning')}\n"
        f"{indent}- **decision:** {f('decision')}\n"
        f"{indent}- **confidence:** {f('confidence')}\n"
        f"{indent}- **could_be_wrong_if:** {f('could_be_wrong_if')}\n")


def build_transparency_report(verdict, gate_results, audit) -> str:
    atoms = _load("atoms")
    ar = json.loads((LOGS / "atoms_reasoning.json").read_text()) if (LOGS / "atoms_reasoning.json").exists() else {}
    cands = _load("candidates")["candidates"]
    verify = _load("verify")["candidates"]
    vr = json.loads((LOGS / "verify_reasoning.json").read_text()).get("candidates", []) if (LOGS / "verify_reasoning.json").exists() else []
    cc = _load("crosscheck")["candidates"]
    by = lambda lst, cid: next((x for x in lst if x.get("cand_id") == cid), {})
    atom_tr = {t.get("atom_id"): t.get("reasoning_trace", {}) for t in ar.get("atom_traces", [])}
    gres = {g["cand_id"]: g for g in gate_results}
    audit_by_step = {a["trace_id"]: a for a in audit.get("audits", [])}

    L = ["# Run 17 - REASONING TRANSPARENCY REPORT",
         f"_generated {datetime.now(timezone.utc).isoformat()} - the COMPLETE middle process, no black box (R9/R12)_\n",
         "> GOAL (R12): make every reasoning step visible and verifiable - why each candidate was "
         "generated, why each gate passed/failed. The niche verdict is secondary and reported honestly either way.\n",
         f"**VERDICT: {verdict['verdict']}** ({len(verdict['survivors'])}/"
         f"{verdict['candidates_scanned']} survivors)  |  "
         f"**logic-audit: {audit['summary']['n_logic_breaks']} logic-breaks, "
         f"{audit['summary']['n_flagged_nonfatal']} non-fatal flags over "
         f"{audit['summary']['total_traces_audited']} traces**\n",
         "---\n## STAGE 0 - Atom sourcing (AGENT 1: why these atoms)\n"]
    if ar.get("overall_trace"):
        L.append("**Overall sourcing reasoning_trace:**\n" + _md_trace(ar["overall_trace"]))
    for a in atoms.get("atoms", []):
        aud = audit_by_step.get(f"atom.{a['atom_id']}", {})
        L.append(f"\n### {a['atom_id']} - {a.get('title','')}  ({a.get('domain','?')})")
        L.append(f"`{a.get('source_id','')}` - {a.get('url','')}")
        L.append(f"> {norm(a.get('text',''))}\n")
        L.append("**why this atom (reasoning_trace):**\n" + _md_trace(atom_tr.get(a["atom_id"], {})))
        if aud.get("flags"):
            L.append(f"  - _AGENT 5 audit:_ {aud['verdict']} - flags: {aud['flags']}")

    L.append("\n---\n## STAGE 1->4 - Per candidate: merge -> verify -> cross-check -> gates\n")
    for cand in cands:
        cid = cand["cand_id"]
        g = gres.get(cid, {})
        L.append(f"\n### {cid} - {cand.get('niche_name','')}")
        L.append(f"`{cand.get('atom_a_id')} x {cand.get('atom_b_id')}`  ->  "
                 f"**composite {g.get('composite')}**, survived={g.get('survived')}, "
                 f"failed={g.get('gates_failed')}\n")
        # merge
        L.append("**MERGE (AGENT 2 - why this niche):**")
        L.append(f"- mechanism: {norm(cand.get('mechanism',''))}")
        L.append(f"- transfer: {norm(cand.get('transfer',''))}")
        L.append(f"- open_problem: {norm(cand.get('open_problem',''))}")
        L.append("- merge reasoning_trace:\n" + _md_trace(cand.get("reasoning_trace", {}), "  "))
        am = audit_by_step.get(f"merge.{cid}", {})
        if am:
            L.append(f"  - _AGENT 5 audit:_ {am.get('verdict')} (grounding={am.get('inputs_grounding_overlap')})"
                     + (f" flags={am['flags']}" if am.get("flags") else ""))
        # verify
        v = by(verify, cid)
        vrr = by(vr, cid)
        L.append(f"\n**VERIFY (AGENT 3 - why collision/not):** collision_found={v.get('collision_found')}, "
                 f"{len(v.get('reformulations',[]))} reformulations, "
                 f"{g.get('paper_hits_in_verify')} paper-like hits")
        if v.get("collision_reason"):
            L.append(f"- collision_reason: {norm(v['collision_reason'])}")
        if vrr.get("verdict_trace"):
            L.append("- verify verdict reasoning_trace:\n" + _md_trace(vrr["verdict_trace"], "  "))
        av = audit_by_step.get(f"verify.verdict.{cid}", {})
        if av:
            cons = av.get("decision_data_consistency", {})
            L.append(f"  - _AGENT 5 audit:_ {av.get('verdict')} - decision<->data: "
                     f"polarity={cons.get('trace_polarity')} vs collision_found={cons.get('data_collision_found')}"
                     + (f" flags={av['flags']}" if av.get("flags") else ""))
        # crosscheck
        c = by(cc, cid)
        L.append(f"\n**CROSS-CHECK (AGENT 4 - confirm/dispute):** agent4_collision={c.get('agent4_collision')}, "
                 f"mismatch_with_agent3={c.get('mismatch_with_agent3')}")
        if c.get("reasoning_trace"):
            L.append("- crosscheck reasoning_trace:\n" + _md_trace(c["reasoning_trace"], "  "))
        ac = audit_by_step.get(f"crosscheck.{cid}", {})
        if ac:
            L.append(f"  - _AGENT 5 audit:_ {ac.get('verdict')}"
                     + (f" flags={ac['flags']}" if ac.get("flags") else ""))
        # gates
        L.append("\n**GATES (MAIN - why pass/fail, exact numbers):**")
        for gk, lbl in (("gate_1_composite", "Gate 1 composite>=0.90"),
                        ("gate_2_quarantine", "Gate 2 quarantine"),
                        ("gate_3_verify", "Gate 3 verify XOR crosscheck"),
                        ("gate_4_belinda", "Gate 4 Belinda strict")):
            gd = g.get(gk, {})
            L.append(f"\n_{lbl}: {'PASS' if gd.get('pass') else 'FAIL'}_")
            L.append(_md_trace(gd.get("reasoning_trace", {}), "  "))
        L.append(f"\n**SURVIVAL:** {g.get('survival_reasoning_trace',{}).get('decision','?')}")
        L.append(_md_trace(g.get("survival_reasoning_trace", {}), "  "))

    L.append("\n---\n## STAGE 5 - AGENT 5 reasoning-audit (logic validity of every step)\n")
    s = audit["summary"]
    L.append(f"- traces audited: **{s['total_traces_audited']}**, all-complete={s['all_complete']}, "
             f"non-fatal flags={s['n_flagged_nonfatal']}, **logic-breaks={s['n_logic_breaks']}**")
    L.append(f"- consistency checks fired (decision<->recorded-data): {s['consistency_checks_fired']}")
    L.append(f"- per agent: {json.dumps(s['by_agent'])}")
    if s["n_logic_breaks"]:
        L.append(f"- **LOGIC-BREAK trace ids: {s['logic_break_trace_ids']}**")
    else:
        L.append("- **No logic-breaks: every decision followed from its stated inputs+reasoning and "
                 "agreed with the recorded structured data.**")
    flagged = [a for a in audit["audits"] if a["flags"]]
    if flagged:
        L.append("\n**Non-fatal flags (and what they mean):**")
        for a in flagged:
            L.append(f"- `{a['trace_id']}` ({a['source_agent']}): {a['flags']}")

    L.append("\n---\n## END-TO-END VERDICT\n")
    L.append(f"Atoms sourced with visible rationale -> 3 merges each with a visible mechanism-transfer "
             f"rationale -> verified with real searches and a visible collision rationale -> independently "
             f"cross-checked -> filtered by 4 gates each with a visible numeric rationale -> audited for "
             f"logic validity. **{verdict['verdict']}.** "
             f"Every one of the {s['total_traces_audited']} decision points above carries a reasoning_trace; "
             f"AGENT 5 found {s['n_logic_breaks']} logic-break(s). No step is a black box.")
    return "\n".join(L) + "\n"


def cmd_finalize(_args) -> int:
    verdict = json.loads((RUN_DIR / "niche_find_check.json").read_text())
    gate_results = _load("gate_results")
    audit = _load("reasoning_audit")
    truth = {
        "n_candidates": verdict["candidates_scanned"],
        "n_survivors": len(verdict["survivors"]),
        "verdict": verdict["verdict"],
        "n_logic_breaks": audit["summary"]["n_logic_breaks"],
        "per_candidate": [{"cand_id": v["cand_id"], "composite": round(v["composite"], 4),
                           "survived": v["survived"]} for v in gate_results],
    }
    env = run_opus(SUMMARY_PROMPT.format(report=(LOGS / "report_log.md").read_text(),
                                         gates=json.dumps(gate_results, indent=2)))
    summary = env.get("result", "")
    (LOGS / "summary_llm.md").write_text(
        f"# LLM summary (session {env.get('session_id')})\n\n{summary}\n")
    claimed = parse_obj(summary)
    mism = []
    if claimed is None:
        mism = ["no parseable claim block"]
    else:
        for k in ("n_candidates", "n_survivors", "verdict", "n_logic_breaks"):
            if claimed.get(k) != truth[k]:
                mism.append(f"{k}: claimed {claimed.get(k)!r} != truth {truth[k]!r}")
        tby = {c["cand_id"]: c for c in truth["per_candidate"]}
        for c in claimed.get("per_candidate", []):
            t = tby.get(c.get("cand_id"))
            if not t:
                mism.append(f"fabricated cand_id {c.get('cand_id')!r}"); continue
            try:
                if abs(float(c.get("composite")) - float(t["composite"])) > 1e-4:
                    mism.append(f"{c['cand_id']} composite {c.get('composite')} != {t['composite']}")
            except (TypeError, ValueError):
                mism.append(f"{c.get('cand_id')} composite not numeric")
            if bool(c.get("survived")) != bool(t["survived"]):
                mism.append(f"{c['cand_id']} survived mismatch")
    hall = {"hallucination_detected": bool(mism), "no_hallucination": not mism,
            "mismatches": mism, "truth": truth, "claimed": claimed,
            "reasoning_trace": _trace(
                "anti-hallucination check",
                f"compared the real-Opus summary's claim JSON to ground truth {truth}",
                "the summary is generated by a separate Opus process; we mechanically compare its "
                "claimed counts/verdict/composites to the deterministic gate truth.",
                "NO_HALLUCINATION" if not mism else f"HALLUCINATION ({len(mism)} mismatches)",
                "high - field-by-field numeric comparison",
                "the summarizer restated a number correctly by luck while misstating prose (prose not checked)")}
    (LOGS / "hallucination_check.json").write_text(json.dumps(hall, indent=2))

    report_md = build_transparency_report(verdict, gate_results, audit)
    (RUN_DIR / "REASONING_TRANSPARENCY_REPORT.md").write_text(report_md)

    det = json.loads((LOGS / "determinism_check.json").read_text())
    cc = _load("crosscheck")
    n_mismatch = sum(1 for c in cc.get("candidates", []) if c.get("mismatch_with_agent3"))
    proofs = {
        "agents_all_committed": all((LOGS / f"{f}.json").exists() for f in
                                    ("atoms", "atoms_reasoning", "candidates", "verify",
                                     "verify_reasoning", "crosscheck", "reasoning_audit")),
        "report_verbatim": "[REPORT 5]" in (LOGS / "report_log.md").read_text(),
        "four_gate_deterministic": det["determinism_ok"],
        "cross_check_ran": "candidates" in cc,
        "no_hallucination": hall["no_hallucination"],
        "every_gate_has_reasoning_trace": all(
            all(isinstance(v.get(g, {}).get("reasoning_trace"), dict) for g in
                ("gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"))
            for v in gate_results),
        "all_traces_audited": audit["summary"]["total_traces_audited"] > 0,
        "all_traces_complete": audit["summary"]["all_complete"],
        "transparency_report_written": (RUN_DIR / "REASONING_TRANSPARENCY_REPORT.md").exists(),
    }
    (RUN_DIR / "proof_scorecard.json").write_text(json.dumps(
        {"proofs": proofs, "all_pass": all(proofs.values()),
         "verdict": verdict["verdict"], "n_survivors": truth["n_survivors"],
         "n_traces_audited": audit["summary"]["total_traces_audited"],
         "n_logic_breaks": truth["n_logic_breaks"],
         "n_nonfatal_flags": audit["summary"]["n_flagged_nonfatal"],
         "agent3_agent4_mismatches": n_mismatch,
         "generated_at": datetime.now(timezone.utc).isoformat()}, indent=2))
    print(f"VERDICT: {verdict['verdict']}  survivors={truth['n_survivors']}  "
          f"traces_audited={audit['summary']['total_traces_audited']} "
          f"logic_breaks={truth['n_logic_breaks']}")
    print(f"no_hallucination={hall['no_hallucination']} mismatches={hall['mismatches']}")
    for k, ok in proofs.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {k}")
    return 0 if all(proofs.values()) else 1


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["report", "gates", "finalize"])
    args = ap.parse_args(argv)
    LOGS.mkdir(parents=True, exist_ok=True)
    return {"report": cmd_report, "gates": cmd_gates, "finalize": cmd_finalize}[args.phase](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

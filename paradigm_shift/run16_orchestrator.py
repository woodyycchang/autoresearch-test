#!/usr/bin/env python3
"""Run 16 MAIN orchestrator — epoch-wise parameter-improving niche pipeline.

Inherits the proven Run 15 deterministic core (4-gate filter, verbatim [REPORT]
injection, determinism check, anti-hallucination summary) and ADDS the Run 16
mechanics:
  * [REPORT 5] for AGENT 5's search_quality.json
  * a deterministic PARAMETER UPDATE step that reads human labels from
    direction_params.labeled_examples, nudges the search-quality params toward
    the profile of "on_target" queries, appends this epoch to epoch_history, and
    writes the updated direction_params.json (R9, R10)
  * a verdict that reports search_quality_delta vs the previous epoch (R12)

Per-epoch success = measurable search-quality improvement (R12), reported
honestly; niche-finding is the long-run goal.

Phases:
  python3 run16_orchestrator.py report     # [REPORT 1..5] verbatim log
  python3 run16_orchestrator.py gates       # 4-gate + determinism + verdict
  python3 run16_orchestrator.py finalize     # hallucination + param update + persist
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
RUN_DIR = THIS_DIR / "run_016"
LOGS = RUN_DIR / "logs"
DPARAMS = RUN_DIR / "direction_params.json"
RULES = json.loads((RUN_DIR / "run16_rules.json").read_text())
SPEC = json.loads((THIS_DIR / "spec" / "harness_rules.json").read_text())

COMPOSITE_THRESHOLD = RULES["gates"]["gate_1_composite_threshold"]      # 0.90
QUARANTINE = set(SPEC["quarantined_atoms"])
BELINDA = SPEC["belinda_strict"]
MIN_REFORMULATIONS = SPEC["min_web_search_per_candidate"]               # 5
LEARNING_RATE = RULES["param_update"]["learning_rate"]                  # 0.2
PARAM_TO_DIM = {
    "reformulation_specificity": "specificity",
    "mechanism_focus": "mechanism_focus",
    "cross_domain_reach": "cross_domain_reach",
    "collision_avoidance_phrasing": "collision_avoidance",
}

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


# ---------- [REPORT] verbatim injection (R6) ----------
def cmd_report(_args) -> int:
    blocks = ["# [REPORT] Run 16 ground-truth log",
              f"# generated {datetime.now(timezone.utc).isoformat()}",
              "# Each block is a subagent's raw output, injected verbatim.\n"]
    for n, name in ((1, "atoms"), (2, "candidates"), (3, "verify"),
                    (4, "crosscheck"), (5, "search_quality")):
        p = LOGS / f"{name}.json"
        blocks.append(f"\n## [REPORT {n}] {name}.json (verbatim)")
        if p.exists():
            blocks += ["```json", p.read_text().rstrip(), "```"]
        else:
            blocks.append(f"_MISSING: {p} not found_")
    (LOGS / "report_log.md").write_text("\n".join(blocks) + "\n")
    print(f"[report] wrote {LOGS / 'report_log.md'}")
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
    return {"composite": composite, "params": params, "paper_hits_in_verify": paper_hits}


def run_gates(atoms: dict, candidates: dict, verify: dict, crosscheck: dict) -> list[dict]:
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
        out.append({
            "cand_id": cid, "niche_name": cand.get("niche_name", ""),
            "composite": sc["composite"], "composite_params": sc["params"],
            "gate_1_composite": {"pass": gate1, "composite": sc["composite"], "threshold": COMPOSITE_THRESHOLD},
            "gate_2_quarantine": {"pass": gate2, "quarantine_hits": qhits},
            "gate_3_verify": {"pass": g3["pass"], **g3},
            "gate_4_belinda": {"pass": g4["pass"], **g4},
            "survived": survived, "gates_failed": failed,
        })
    return out


def verdicts_hash(verdicts: list[dict]) -> str:
    skel = [{"c": v["cand_id"], "comp": v["composite"],
             "g1": v["gate_1_composite"]["pass"], "g2": v["gate_2_quarantine"]["pass"],
             "g3": v["gate_3_verify"]["pass"], "g4": v["gate_4_belinda"]["pass"],
             "s": v["survived"]} for v in verdicts]
    return hashlib.sha256(json.dumps(skel, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _load(name):
    return json.loads((LOGS / f"{name}.json").read_text())


def cmd_gates(_args) -> int:
    atoms, candidates, verify, crosscheck = (_load("atoms"), _load("candidates"),
                                             _load("verify"), _load("crosscheck"))
    sq = _load("search_quality")
    v1 = run_gates(*(copy.deepcopy(x) for x in (atoms, candidates, verify, crosscheck)))
    v2 = run_gates(*(copy.deepcopy(x) for x in (atoms, candidates, verify, crosscheck)))
    h1, h2 = verdicts_hash(v1), verdicts_hash(v2)
    (LOGS / "gate_results.json").write_text(json.dumps(v1, indent=2))
    (LOGS / "determinism_check.json").write_text(json.dumps(
        {"determinism_ok": h1 == h2, "hash_run_1": h1, "hash_run_2": h2, "runs": 2}, indent=2))
    survivors = [v for v in v1 if v["survived"]]
    gates = ["gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"]
    fired = {g: sum(1 for v in v1 if g in v["gates_failed"]) for g in gates}
    dp = json.loads(DPARAMS.read_text())
    prev = dp.get("epoch_history", [])
    prev_q = prev[-1]["avg_search_quality"] if prev else None
    this_q = sq["avg_search_quality"]
    delta = round(this_q - prev_q, 4) if prev_q is not None else None
    verdict = {
        "run_id": "run_016", "epoch": dp["epoch"],
        "verdict": "NICHE_FOUND" if survivors else "NICHE_NOT_FOUND",
        "survivors": [{"cand_id": s["cand_id"], "niche_name": s["niche_name"],
                       "composite": s["composite"], "note": "R10: re-verify with 10 more searches"}
                      for s in survivors],
        "gate_fired_counts": fired, "candidates_scanned": len(v1), "per_candidate": v1,
        "avg_search_quality": this_q, "prev_avg_search_quality": prev_q,
        "search_quality_delta": delta,
        "search_quality_improved": (delta is not None and delta > 0),
        "per_epoch_success_metric": ("search_quality improvement vs last epoch (R12); "
                                     "baseline epoch has no delta"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    (RUN_DIR / "niche_find_check.json").write_text(json.dumps(verdict, indent=2))
    for v in v1:
        flags = "".join("1" if v[g]["pass"] else "0" for g in gates)
        print(f"  {v['cand_id']}: composite={v['composite']:.4f} gates[{flags}] survived={v['survived']}")
    print(f"\n[gates] {verdict['verdict']} ({len(survivors)} survivor); determinism={'OK' if h1==h2 else 'BROKEN'}")
    print(f"[gates] avg_search_quality={this_q} prev={prev_q} delta={delta}")
    return 0


# ---------- PARAMETER UPDATE (R9/R10): label-driven nudge + persist ----------
def update_params(dp: dict, sq: dict) -> dict:
    """Nudge search-quality params toward the profile of human-labeled on_target
    queries, append this epoch to epoch_history, bump epoch. Deterministic."""
    params = dict(dp["search_quality_params"])
    labels = dp.get("labeled_examples", [])
    by_query = {pq["query"]: pq["dims"] for pq in sq.get("per_query", [])}
    on, div = [], []
    for lab in labels:
        dims = by_query.get(lab.get("search_query"))
        if dims is None:
            continue
        (on if lab.get("label") == "on_target" else div).append(dims)

    def mean(group, dimkey):
        vals = [g[dimkey] for g in group if dimkey in g]
        return sum(vals) / len(vals) if vals else None

    nudges = {}
    for pkey, dimkey in PARAM_TO_DIM.items():
        m_on, m_div = mean(on, dimkey), mean(div, dimkey)
        if m_on is None and m_div is None:
            continue  # no labeled signal for this dimension
        signal = (m_on if m_on is not None else 0.0) - (m_div if m_div is not None else 0.0)
        new = min(0.95, max(0.05, round(params[pkey] + LEARNING_RATE * signal, 4)))
        nudges[pkey] = {"old": params[pkey], "new": new, "on_mean": m_on, "div_mean": m_div}
        params[pkey] = new

    history = list(dp.get("epoch_history", []))
    history.append({"epoch": dp["epoch"], "avg_search_quality": sq["avg_search_quality"],
                    "n_labels_applied": len(on) + len(div),
                    "params_snapshot": dict(dp["search_quality_params"])})
    return {
        "epoch": dp["epoch"] + 1,                       # next epoch
        "scored_epoch": dp["epoch"],
        "search_quality_params": params,
        "labeled_examples": [],                          # consumed; await next epoch's labels
        "epoch_history": history,
        "param_nudges_last_update": nudges,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


SUMMARY_PROMPT = """You are writing a strictly factual summary of a multi-agent run.
Below is the RAW REPORT LOG (verbatim agent outputs) and the GATE RESULTS (ground truth).

=== RAW REPORT LOG ===
{report}

=== GATE RESULTS (JSON) ===
{gates}

Write 4-7 sentences stating ONLY facts present above (do not infer or embellish numbers).
Then output a raw JSON object (no fences) with EXACTLY:
{{"n_candidates": <int>, "n_survivors": <int>, "verdict": "<NICHE_FOUND|NICHE_NOT_FOUND>", "avg_search_quality": <number>, "per_candidate": [{{"cand_id": "<id>", "composite": <number>, "survived": <bool>}}]}}"""


def run_opus(prompt: str) -> dict:
    cfg = RULES["opus_subprocess"]
    cmd = [cfg["binary"], *cfg["args"], "--disallowedTools", *cfg["disallowed_tools"]]
    td = tempfile.mkdtemp(prefix="run16_sum_")
    proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                          timeout=cfg["timeout_seconds"], cwd=td)
    if proc.returncode != 0:
        raise RuntimeError(f"opus exit {proc.returncode}: {proc.stderr[:400]}")
    return json.loads(proc.stdout)


def parse_obj(text: str) -> dict | None:
    """Robust: whole text, then fenced blocks, then any balanced {...} (skipping
    nested objects so the outer answer is chosen), preferring the last."""
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
    found = []
    start = text.find("{")
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


def cmd_finalize(_args) -> int:
    verdict = json.loads((RUN_DIR / "niche_find_check.json").read_text())
    gate_results = _load("gate_results")
    sq = _load("search_quality")
    truth = {
        "n_candidates": verdict["candidates_scanned"],
        "n_survivors": len(verdict["survivors"]),
        "verdict": verdict["verdict"],
        "avg_search_quality": sq["avg_search_quality"],
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
        for k in ("n_candidates", "n_survivors", "verdict"):
            if claimed.get(k) != truth[k]:
                mism.append(f"{k}: claimed {claimed.get(k)!r} != truth {truth[k]!r}")
        try:
            if abs(float(claimed.get("avg_search_quality")) - float(truth["avg_search_quality"])) > 1e-4:
                mism.append(f"avg_search_quality {claimed.get('avg_search_quality')} != {truth['avg_search_quality']}")
        except (TypeError, ValueError):
            mism.append("avg_search_quality not numeric")
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
            "mismatches": mism, "truth": truth, "claimed": claimed}
    (LOGS / "hallucination_check.json").write_text(json.dumps(hall, indent=2))

    # PARAMETER UPDATE + persist direction_params.json (R9/R10)
    dp_before = json.loads(DPARAMS.read_text())
    dp_after = update_params(dp_before, sq)
    DPARAMS.write_text(json.dumps(dp_after, indent=2))

    det = json.loads((LOGS / "determinism_check.json").read_text())
    cc = _load("crosscheck")
    n_mismatch = sum(1 for c in cc.get("candidates", []) if c.get("mismatch_with_agent3"))
    proofs = {
        "agents_all_committed": all((LOGS / f"{f}.json").exists() for f in
                                    ("atoms", "candidates", "verify", "crosscheck", "search_quality")),
        "report_verbatim": "[REPORT 5]" in (LOGS / "report_log.md").read_text(),
        "four_gate_deterministic": det["determinism_ok"],
        "cross_check_ran": "candidates" in cc,
        "no_hallucination": hall["no_hallucination"],
        "search_quality_tracked": isinstance(sq.get("avg_search_quality"), (int, float)),
        "params_persisted": len(dp_after["epoch_history"]) >= 1 and dp_after["epoch"] == dp_before["epoch"] + 1,
    }
    (RUN_DIR / "proof_scorecard.json").write_text(json.dumps(
        {"proofs": proofs, "all_pass": all(proofs.values()),
         "verdict": verdict["verdict"], "n_survivors": truth["n_survivors"],
         "scored_epoch": dp_before["epoch"], "next_epoch": dp_after["epoch"],
         "avg_search_quality": sq["avg_search_quality"],
         "search_quality_delta": verdict["search_quality_delta"],
         "agent3_agent4_mismatches": n_mismatch,
         "generated_at": datetime.now(timezone.utc).isoformat()}, indent=2))
    print(f"VERDICT: {verdict['verdict']}  survivors={truth['n_survivors']}  "
          f"avg_search_quality={sq['avg_search_quality']} delta={verdict['search_quality_delta']}")
    print(f"no_hallucination={hall['no_hallucination']} mismatches={hall['mismatches']}")
    print(f"params: epoch {dp_before['epoch']} -> {dp_after['epoch']}; nudges={list(dp_after['param_nudges_last_update'].keys())}")
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

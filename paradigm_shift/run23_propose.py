#!/usr/bin/env python3
"""Run 23 AGENT 3 (cross-field proposer): for 5 PAIRS of (low-AI-penetration PROCESS x
usable RECENT technique), Opus proposes how the RECENT 2025-2026 technique concretely
improves the process -- and crucially WHY the recent technique beats the MATURE approach
(its NEW capability: zero-shot / label-free / sparse-sensor). R3/R4/R9/R13.

The honest maturity tier (from technique_maturity.json) is fed into the prompt so Opus's
feasibility_now is grounded, not optimistic.

Reads : run_023/logs/processes.json, techniques.json, technique_maturity.json, penetration.json,
        run_021/run21_rules.json (opus cfg)
Writes: run_023/logs/proposals.json + propose_<pair_id>.json envelopes
"""
from __future__ import annotations
import json, re, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

THIS = Path(__file__).parent
RUN = THIS / "run_023"; LOGS = RUN / "logs"
CFG = json.loads((THIS / "run_021" / "run21_rules.json").read_text())["opus_subprocess"]
FIELDS = ["process", "process_problem", "recent_technique", "technique_year", "how_it_improves",
          "why_recent_technique_beats_mature_approach", "feasibility_now",
          "primary_quote", "quote_source", "reasoning_trace"]
TF = ["step", "inputs_seen", "reasoning", "decision", "confidence", "could_be_wrong_if"]

# The 5 cross-field pairs: each = low-penetration process x a RECENT technique whose NEW
# capability matches the process's open problem (a mature method could not enter this regime).
PAIRS = [
    {"pair_id": "retting_x_HSIFM",   "process_id": "retting",       "technique_id": "HSIFM"},
    {"pair_id": "charcoal_x_FNO",    "process_id": "charcoal_kiln", "technique_id": "FNO"},
    {"pair_id": "indigo_x_TSFM",     "process_id": "indigo_vat",    "technique_id": "TSFM"},
    {"pair_id": "cork_x_VLMAD",      "process_id": "cork_harvest",  "technique_id": "VLMAD"},
    {"pair_id": "indigo_x_VLMAD",    "process_id": "indigo_vat",    "technique_id": "VLMAD"},
]

PROMPT = """You are AGENT 3 in a CROSS-FIELD APPLICATION pipeline. The goal is NOT to invent a new AI method.
The goal: take a REAL-WORLD PROCESS (low AI penetration) and a SPECIFIC RECENT (2025-2026) AI technique, and
propose how that recent technique CONCRETELY IMPROVES the process -- an application nobody has done yet -- AND
explain WHY the RECENT technique succeeds where the MATURE approach could not.

PROCESS (id {pid}, domain {domain}): "{process}"
OPEN PROBLEM: "{problem}"
AI penetration on this process: {pen} on-target hits (low = white space).

RECENT TECHNIQUE (id {tid}): {tname} [{tyear}]
ITS NEW CAPABILITY (vs older ML): {newcap}
USABLE-NOW EXEMPLARS: {exemplars}
HONEST DEPLOYMENT MATURITY (use this to be REALISTIC about feasibility_now): tier={tier}; {mnote}

Propose ONE concrete improvement that PAIRS this technique with this process. BE HONEST AND FEASIBLE (this will
be scrutinized hard). The crux is the NEW CAPABILITY: a mature method needs labeled data / dense sensors / a
per-task training set that this niche process LACKS; the recent technique's zero-shot / few-shot / label-free /
sparse-sensor ability is exactly what removes that blocker. Say so concretely. Do NOT hand-wave ("AI could help").
For feasibility_now, be REALISTIC given the maturity tier above -- if it needs training data, a special camera,
or faces out-of-distribution transfer, SAY SO; do not claim drop-in if it is not.

Output ONLY a raw JSON object -- NO prose, NO fences. EXACTLY these keys:
{{"process": "<the process, one phrase>", "process_problem": "<the concrete open problem>", "recent_technique": "<the SPECIFIC named recent technique, e.g. 'zero-shot time-series foundation model (Chronos-2/TimesFM)'>", "technique_year": "<2025-2026 or the technique's year>", "how_it_improves": "<concrete mechanism: inputs -> model -> actionable output -> efficiency/quality gain>", "why_recent_technique_beats_mature_approach": "<the NEW capability: what blocker (no labeled data / dense sensors / per-task training) the mature method hit, and how the recent technique's zero-shot/few-shot/sparse ability removes it>", "feasibility_now": "<REALISTIC: drop-in vs needs-training-data vs out-of-distribution vs needs-hardware, grounded in the maturity tier>", "primary_quote": "a substring of AT LEAST 30 characters copied EXACTLY and VERBATIM from the PROCESS or OPEN PROBLEM text above", "quote_source": "process or open_problem", "reasoning_trace": {{"step": "propose {pid} x {tid}", "inputs_seen": "the process + its open problem + the recent technique's new capability + its maturity tier", "reasoning": "why this recent technique's NEW capability fits this open problem, what mature alternative is blocked and why, what makes feasibility_now realistic (not optimistic)", "decision": "the proposed recent-technique-to-process application", "confidence": "high|medium|low - and a one-clause reason tied to the maturity tier", "could_be_wrong_if": "the concrete condition under which this is infeasible, already done, or the recent technique does not transfer to this niche"}}}}
Output nothing but the JSON object."""

_T = None
def td():
    global _T
    if _T is None: _T = tempfile.mkdtemp(prefix="run23_opus_")
    return _T

def run_opus(p):
    cmd = [CFG["binary"], *CFG["args"], "--disallowedTools", *CFG["disallowed_tools"]]
    r = subprocess.run(cmd, input=p, capture_output=True, text=True, timeout=CFG["timeout_seconds"], cwd=td())
    if r.returncode != 0: raise RuntimeError(f"opus exit {r.returncode}: {r.stderr[:300]}")
    return json.loads(r.stdout)

def _repair_truncated(t):
    """Opus sometimes emits a valid object but drops the final closing brace(s) (truncation).
    From the first '{', track string/escape state; if the stream ends mid-string close the quote,
    then append the count of unmatched '{'. Returns the repaired string (or None if no '{')."""
    s = t.find("{")
    if s == -1: return None
    depth, instr, esc = 0, False, False
    for ch in t[s:]:
        if esc: esc = False; continue
        if ch == "\\": esc = True; continue
        if ch == '"': instr = not instr; continue
        if not instr:
            if ch == "{": depth += 1
            elif ch == "}": depth -= 1
    if depth <= 0: return None
    return t[s:] + ('"' if instr else "") + ("}" * depth)


def parse_obj(t):
    t = (t or "").strip()
    try: return json.loads(t)
    except json.JSONDecodeError: pass
    for b in reversed(re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", t, re.DOTALL)):
        try: return json.loads(b)
        except json.JSONDecodeError: continue
    # balance-repair a truncated top-level object BEFORE falling back to inner-brace scanning
    rep = _repair_truncated(t)
    if rep is not None:
        try: return json.loads(rep)
        except json.JSONDecodeError: pass
    s = t.find("{")
    while s != -1:
        d = 0
        for i in range(s, len(t)):
            if t[i] == "{": d += 1
            elif t[i] == "}":
                d -= 1
                if d == 0:
                    try: return json.loads(t[s:i+1])
                    except json.JSONDecodeError: break
        s = t.find("{", s+1)
    return None

def norm(s): return re.sub(r"\s+", " ", (s or "")).strip()
def trace_ok(tr): return isinstance(tr, dict) and all(norm(str(tr.get(f, ""))) for f in TF)

def main():
    reparse = "--reparse" in sys.argv  # rebuild proposals.json from saved envelopes, no Opus calls
    procs = {p["process_id"]: p for p in json.loads((LOGS / "processes.json").read_text())["processes"]}
    techs = {t["technique_id"]: t for t in json.loads((LOGS / "techniques.json").read_text())["techniques"]}
    mat = {m["technique_id"]: m for m in json.loads((LOGS / "technique_maturity.json").read_text())["techniques"]}
    pen = {p["process_id"]: p for p in json.loads((LOGS / "penetration.json").read_text())["processes"]}
    out = []
    for pair in PAIRS:
        pid, tid = pair["process_id"], pair["technique_id"]
        pr, te, ma, pe = procs[pid], techs[tid], mat[tid], pen[pid]
        src_text = norm(pr["process"] + " " + pr["open_problem"])
        parsed, env = None, None
        if reparse:
            env = json.loads((LOGS / f"propose_{pair['pair_id']}.json").read_text())["envelope"]
            parsed = parse_obj(env.get("result", ""))
        else:
            prompt = PROMPT.format(pid=pid, domain=pr["domain"], process=pr["process"], problem=pr["open_problem"],
                                   pen=pe["on_target_ai_hits"], tid=tid, tname=te["name"], tyear=te["year"],
                                   newcap=te["new_capability"], exemplars=te["exemplars"],
                                   tier=ma["deployment_maturity_tier"], mnote=ma["maturity_note"])
            for _ in range(1 + CFG["retry_on_parse_fail"]):
                env = run_opus(prompt); parsed = parse_obj(env.get("result", ""))
                if parsed and all(k in parsed for k in FIELDS) and trace_ok(parsed.get("reasoning_trace")): break
        p = parsed or {}
        q = norm(p.get("primary_quote", ""))
        quote_ok = bool(q) and len(q) >= 30 and q in src_text
        (LOGS / f"propose_{pair['pair_id']}.json").write_text(json.dumps(
            {"pair_id": pair["pair_id"], "process_id": pid, "technique_id": tid, "envelope": env, "parsed": parsed}, indent=2))
        out.append({"pair_id": pair["pair_id"], "process_id": pid, "technique_id": tid,
                    "on_target_ai_hits": pe["on_target_ai_hits"], "process_low_penetration": pe["is_low"],
                    "technique_usable_now": ma["usable_now"], "technique_maturity_tier": ma["deployment_maturity_tier"],
                    **{k: p.get(k) for k in FIELDS},
                    "quote_verified_substring": quote_ok, "reasoning_trace_complete": trace_ok(p.get("reasoning_trace")),
                    "parse_ok": parsed is not None, "opus_session_id": (env or {}).get("session_id")})
        print(f"  {pair['pair_id']:<18} parse_ok={parsed is not None} quote_ok={quote_ok} tech={p.get('recent_technique','')[:50]!r}")
    json.dump({"run_id": "run_023", "agent": "3_cross_field_proposer", "generated_at": datetime.now(timezone.utc).isoformat(),
               "pairs": PAIRS, "proposals": out}, open(LOGS / "proposals.json", "w"), indent=2)
    print(f"[propose] wrote {len(out)} proposals")
    return 0

if __name__ == "__main__":
    sys.exit(main())

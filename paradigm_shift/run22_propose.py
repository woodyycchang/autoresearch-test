#!/usr/bin/env python3
"""Run 22 AGENT 3 (improvement proposer): for the 5 lowest-AI-penetration processes,
Opus proposes a SPECIFIC, CONCRETE improvement using a NAMED EXISTING AI technique
(apply technique X to improve process Y -- NOT invent a new method). R3/R4/R9/R13.

Reads : run_022/logs/processes.json, ai_penetration.json, run_021/run21_rules.json (opus cfg)
Writes: run_022/logs/proposals.json + propose_<pid>.json envelopes
"""
from __future__ import annotations
import json, re, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

THIS = Path(__file__).parent
RUN = THIS / "run_022"; LOGS = RUN / "logs"
CFG = json.loads((THIS / "run_021" / "run21_rules.json").read_text())["opus_subprocess"]
FIELDS = ["process", "current_inefficiency", "ai_technique", "how_it_improves", "why_not_done_before",
          "primary_quote", "quote_source", "reasoning_trace"]
TF = ["step", "inputs_seen", "reasoning", "decision", "confidence", "could_be_wrong_if"]

PROMPT = """You are AGENT 3 in an APPLICATION-gap pipeline. The goal is NOT to invent a new AI method.
The goal is: take a REAL-WORLD PROCESS and propose how a SPECIFIC, NAMED, CURRENTLY-EXISTING AI technique
could CONCRETELY IMPROVE it -- an application nobody has done yet.

PROCESS (id {pid}, domain {domain}): "{process}"
KNOWN INEFFICIENCY: "{ineff}"
AI-penetration so far: {pen} (adjacent/feasibility note: {feas})

Propose ONE concrete improvement. BE HONEST AND FEASIBLE (this will be scrutinized): name a REAL existing AI
technique (e.g. "hyperspectral imaging + gradient-boosted regression", "YOLO object detection", "a CNN smoke-
plume classifier"), state the concrete mechanism by which it improves the process, and why it plausibly has not
been done. Do NOT hand-wave ("AI could help") -- be specific enough that an engineer could start building it.

Output ONLY a raw JSON object -- NO prose, NO fences. EXACTLY these keys:
{{"process": "<the process, one phrase>", "current_inefficiency": "<the concrete inefficiency>", "ai_technique": "<a SPECIFIC named existing AI technique>", "how_it_improves": "<concrete mechanism: inputs -> model -> actionable output -> efficiency gain>", "why_not_done_before": "<honest reason this specific application is unexploited>", "primary_quote": "a substring of AT LEAST 30 characters copied EXACTLY and VERBATIM from the PROCESS or INEFFICIENCY text above", "quote_source": "process or inefficiency", "reasoning_trace": {{"step": "propose improvement for {pid}", "inputs_seen": "the process + its inefficiency", "reasoning": "why this technique fits this inefficiency, what makes it concretely feasible (not hand-wavy), what alternative you rejected", "decision": "the proposed technique-to-process application", "confidence": "high|medium|low - and a one-clause reason about FEASIBILITY", "could_be_wrong_if": "the concrete condition under which this improvement is infeasible or already done"}}}}
Output nothing but the JSON object."""

_T = None
def td():
    global _T
    if _T is None: _T = tempfile.mkdtemp(prefix="run22_opus_")
    return _T

def run_opus(p):
    cmd = [CFG["binary"], *CFG["args"], "--disallowedTools", *CFG["disallowed_tools"]]
    r = subprocess.run(cmd, input=p, capture_output=True, text=True, timeout=CFG["timeout_seconds"], cwd=td())
    if r.returncode != 0: raise RuntimeError(f"opus exit {r.returncode}: {r.stderr[:300]}")
    return json.loads(r.stdout)

def parse_obj(t):
    t = (t or "").strip()
    try: return json.loads(t)
    except json.JSONDecodeError: pass
    for b in reversed(re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", t, re.DOTALL)):
        try: return json.loads(b)
        except json.JSONDecodeError: continue
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
    procs = {p["process_id"]: p for p in json.loads((LOGS / "processes.json").read_text())["processes"]}
    pen = {p["process_id"]: p for p in json.loads((LOGS / "ai_penetration.json").read_text())["processes"]}
    lowest = json.loads((LOGS / "ai_penetration.json").read_text())["ranked_lowest_penetration"][:5]
    out = []
    for pid in lowest:
        pr, pe = procs[pid], pen[pid]
        src_text = norm(pr["process"] + " " + pr["inefficiency"])
        prompt = PROMPT.format(pid=pid, domain=pr["domain"], process=pr["process"], ineff=pr["inefficiency"],
                               pen=pe["penetration"], feas=pe["feasibility_note"])
        parsed, env = None, None
        for _ in range(1 + CFG["retry_on_parse_fail"]):
            env = run_opus(prompt); parsed = parse_obj(env.get("result", ""))
            if parsed and all(k in parsed for k in FIELDS) and trace_ok(parsed.get("reasoning_trace")): break
        p = parsed or {}
        q = norm(p.get("primary_quote", ""))
        quote_ok = bool(q) and len(q) >= 30 and q in src_text
        (LOGS / f"propose_{pid}.json").write_text(json.dumps({"process_id": pid, "envelope": env, "parsed": parsed}, indent=2))
        out.append({"process_id": pid, "on_target_ai_hits": pe["on_target_ai_hits"], "penetration": pe["penetration"],
                    "is_low": pe["is_low"], **{k: p.get(k) for k in FIELDS},
                    "quote_verified_substring": quote_ok, "reasoning_trace_complete": trace_ok(p.get("reasoning_trace")),
                    "parse_ok": parsed is not None, "opus_session_id": (env or {}).get("session_id")})
        print(f"  {pid}: parse_ok={parsed is not None} quote_ok={quote_ok} tech={p.get('ai_technique','')[:60]!r}")
    json.dump({"run_id": "run_022", "agent": "3_proposer", "generated_at": datetime.now(timezone.utc).isoformat(),
               "proposals": out}, open(LOGS / "proposals.json", "w"), indent=2)
    print(f"[propose] wrote {len(out)} proposals")
    return 0

if __name__ == "__main__":
    sys.exit(main())

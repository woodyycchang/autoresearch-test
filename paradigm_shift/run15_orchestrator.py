#!/usr/bin/env python3
"""Run 15 MAIN orchestrator (deterministic core).

Consumes the four agents' verbatim outputs and produces the verdict:
  * [REPORT N] verbatim injection of each agent's raw JSON (R6, ground truth)
  * 4-gate deterministic filter (composite>=0.90, quarantine, gate3=verify,
    Belinda strict with real-substring primary_quote)
  * Gate 3 fuses AGENT 3 (verifier) with AGENT 4 (cross-checker): a candidate
    passes Gate 3 only if verifier found NO collision AND the cross-checker did
    not overturn that finding.
  * determinism check (run gates twice, compare hash)
  * hallucination check (final Opus summary vs [REPORT] raw -> mismatches)

Phases:
  python3 run15_orchestrator.py report      # build [REPORT] log from agent outputs
  python3 run15_orchestrator.py gates       # 4-gate + determinism + verdict
  python3 run15_orchestrator.py finalize    # anti-hallucination summary + scorecard
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
RUN_DIR = THIS_DIR / "runs" / "run_015"
LOGS = RUN_DIR / "logs"
RULES = json.loads((RUN_DIR / "run15_rules.json").read_text())
SPEC = json.loads((THIS_DIR / "spec" / "harness_rules.json").read_text())

COMPOSITE_THRESHOLD = RULES["gates"]["gate_1_composite_threshold"]      # 0.90
QUARANTINE = set(SPEC["quarantined_atoms"])
BELINDA = SPEC["belinda_strict"]
MIN_REFORMULATIONS = SPEC["min_web_search_per_candidate"]               # 5

PAPER_MARKERS = (
    "arxiv.org", "doi.org", "semanticscholar", "scholar.google", "aclanthology",
    "openreview", "biorxiv", "ncbi.nlm.nih.gov", "pubmed", "dl.acm.org",
    "ieeexplore", "springer", "sciencedirect", "/pdf", ".pdf", "proceedings",
    "neurips", "openalex", "ssrn", "mdpi", "nature.com", "researchgate",
    "diva-portal", "pnas.org", "mlr.press", "jmlr",
)
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "only", "each",
    "many", "which", "their", "they", "them", "then", "than", "are", "was",
    "have", "has", "not", "but", "can", "will", "via", "per", "its", "one",
    "two", "more", "most", "some", "such", "over", "under", "model", "models",
    "learning", "neural", "network", "networks", "deep", "training", "inference",
    "data", "task", "tasks", "method", "methods", "approach", "system", "novel",
    "paper", "using", "used", "use", "based", "architecture", "ai", "llm", "llms",
    "large", "language", "general", "research", "results", "scale", "scaling",
}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def content_words(text: str) -> list[str]:
    return sorted({w for w in re.findall(r"[a-zA-Z][a-zA-Z\-]{3,}", (text or "").lower())
                   if w not in STOPWORDS})


def is_paper(res: dict) -> bool:
    blob = (res.get("url", "") + " " + res.get("title", "")).lower()
    return any(m in blob for m in PAPER_MARKERS)


def is_arxiv(res: dict) -> bool:
    return "arxiv.org" in (res.get("url", "") + " " + res.get("title", "")).lower()


# ---------- [REPORT] verbatim injection (R6) ----------
def cmd_report(_args) -> int:
    blocks = ["# [REPORT] Run 15 ground-truth log",
              f"# generated {datetime.now(timezone.utc).isoformat()}",
              "# Each block is a subagent's raw output, injected verbatim by the orchestrator.\n"]
    for n, name in ((1, "atoms"), (2, "candidates"), (3, "verify"), (4, "crosscheck")):
        p = LOGS / f"{name}.json"
        blocks.append(f"\n## [REPORT {n}] {name}.json (verbatim)")
        if p.exists():
            blocks += ["```json", p.read_text().rstrip(), "```"]
        else:
            blocks.append(f"_MISSING: {p} not found_")
    (LOGS / "report_log.md").write_text("\n".join(blocks) + "\n")
    print(f"[report] wrote {LOGS / 'report_log.md'}")
    return 0


# ---------- Gate 3 fusion: verifier + cross-checker ----------
def gate3_for(cid: str, verify: dict, crosscheck: dict) -> dict:
    """Pass iff verifier ran >=5 reformulations, found NO collision, and the
    cross-checker did not overturn that 'no collision' finding."""
    vrec = next((v for v in verify.get("candidates", []) if v["cand_id"] == cid), None)
    if not vrec:
        return {"pass": False, "reason": "no verifier record", "verifier_collision": None,
                "crosscheck_overturned": None}
    n_reform = len(vrec.get("reformulations", []))
    verifier_collision = bool(vrec.get("collision_found"))
    # cross-checker may overturn either direction
    crec = next((c for c in crosscheck.get("candidates", []) if c["cand_id"] == cid), None)
    overturned = bool(crec and crec.get("mismatch_with_agent3"))
    enough = n_reform >= MIN_REFORMULATIONS
    # effective collision = verifier says collision, OR cross-checker overturned a "no collision"
    effective_collision = verifier_collision or (overturned and not verifier_collision)
    passed = enough and not effective_collision and not overturned
    return {"pass": passed, "n_reformulations": n_reform, "required": MIN_REFORMULATIONS,
            "verifier_collision": verifier_collision, "crosscheck_overturned": overturned,
            "effective_collision": effective_collision}


# ---------- Gate 4: Belinda strict with real-substring quote ----------
def gate4_for(cand: dict, atoms_by_id: dict) -> dict:
    mech = norm(cand.get("mechanism", "")).lower()
    verbs = sorted(v for v in BELINDA["mechanism_vocab"]
                   if re.search(r"\b" + re.escape(v) + r"\b", mech))
    quote = norm(cand.get("primary_quote", ""))
    src_id = cand.get("atom_a_id") if cand.get("quote_source") == "atom_a" else \
        cand.get("atom_b_id") if cand.get("quote_source") == "atom_b" else None
    src_text = norm(atoms_by_id.get(src_id, {}).get("text", "")) if src_id else ""
    grounded = bool(quote) and len(quote) >= BELINDA["min_verbatim_chars"] and quote in src_text
    # operator/analogy guard: mechanism must not be a bare "combine A and B"
    not_bare_analogy = not re.search(r"\bcombine[sd]?\b", mech) or bool(verbs)
    passed = bool(verbs) and grounded and not_bare_analogy
    return {"pass": passed, "mechanism_verbs": verbs, "quote_len": len(quote),
            "quote_grounded": grounded, "quote_source_id": src_id}


# ---------- composite scorer (deterministic, real novelty from verify) ----------
def composite_for(cand: dict, verify: dict, g4: dict) -> dict:
    """Deterministic composite in [0,1]. Real signal: novelty from the verifier's
    own searches (paper-host hits across reformulations). Plus structural signals."""
    vrec = next((v for v in verify.get("candidates", []) if v["cand_id"] == cand["cand_id"]), None)
    reforms = vrec.get("reformulations", []) if vrec else []
    paper_hits = sum(1 for rf in reforms for r in rf.get("results", []) if is_paper(r))
    # novelty: fewer paper-hosts found across prior-art search => more novel
    novelty = max(0.0, 1.0 - paper_hits / 20.0)
    mech_present = 1.0 if g4["mechanism_verbs"] else 0.0
    grounded = 1.0 if g4["quote_grounded"] else 0.0
    cross_atom = 1.0 if cand.get("atom_a_id") != cand.get("atom_b_id") else 0.0
    params = {"novelty": round(novelty, 4), "mechanism_present": mech_present,
              "quote_grounded": grounded, "cross_atom": cross_atom}
    weights = {"novelty": 0.55, "mechanism_present": 0.20,
               "quote_grounded": 0.15, "cross_atom": 0.10}
    composite = round(sum(weights[k] * v for k, v in params.items()), 4)
    return {"composite": composite, "params": params, "paper_hits_in_verify": paper_hits}


# ---------- the 4-gate filter (deterministic) ----------
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
        gate3 = g3["pass"]
        gate4 = g4["pass"]
        survived = gate1 and gate2 and gate3 and gate4
        failed = [g for g, ok in (("gate_1_composite", gate1), ("gate_2_quarantine", gate2),
                                  ("gate_3_verify", gate3), ("gate_4_belinda", gate4)) if not ok]
        out.append({
            "cand_id": cid, "niche_name": cand.get("niche_name", ""),
            "composite": sc["composite"], "composite_params": sc["params"],
            "gate_1_composite": {"pass": gate1, "composite": sc["composite"],
                                 "threshold": COMPOSITE_THRESHOLD},
            "gate_2_quarantine": {"pass": gate2, "quarantine_hits": qhits},
            "gate_3_verify": {"pass": gate3, **g3},
            "gate_4_belinda": {"pass": gate4, **g4},
            "survived": survived, "gates_failed": failed,
        })
    return out


def verdicts_hash(verdicts: list[dict]) -> str:
    skel = [{"c": v["cand_id"], "comp": v["composite"],
             "g1": v["gate_1_composite"]["pass"], "g2": v["gate_2_quarantine"]["pass"],
             "g3": v["gate_3_verify"]["pass"], "g4": v["gate_4_belinda"]["pass"],
             "s": v["survived"]} for v in verdicts]
    return hashlib.sha256(json.dumps(skel, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _load_all():
    return (json.loads((LOGS / "atoms.json").read_text()),
            json.loads((LOGS / "candidates.json").read_text()),
            json.loads((LOGS / "verify.json").read_text()),
            json.loads((LOGS / "crosscheck.json").read_text()))


def cmd_gates(_args) -> int:
    atoms, candidates, verify, crosscheck = _load_all()
    v1 = run_gates(copy.deepcopy(atoms), copy.deepcopy(candidates),
                   copy.deepcopy(verify), copy.deepcopy(crosscheck))
    v2 = run_gates(copy.deepcopy(atoms), copy.deepcopy(candidates),
                   copy.deepcopy(verify), copy.deepcopy(crosscheck))
    h1, h2 = verdicts_hash(v1), verdicts_hash(v2)
    det_ok = h1 == h2
    (LOGS / "gate_results.json").write_text(json.dumps(v1, indent=2))
    (LOGS / "determinism_check.json").write_text(json.dumps(
        {"determinism_ok": det_ok, "hash_run_1": h1, "hash_run_2": h2, "runs": 2}, indent=2))
    survivors = [v for v in v1 if v["survived"]]
    gates = ["gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"]
    fired = {g: sum(1 for v in v1 if g in v["gates_failed"]) for g in gates}
    verdict = {
        "verdict": "NICHE_FOUND" if survivors else "NICHE_NOT_FOUND",
        "survivors": [{"cand_id": s["cand_id"], "niche_name": s["niche_name"],
                       "composite": s["composite"],
                       "note": "passed all 4 gates incl. cross-verified prior-art; "
                       "R10: re-verify with 10 more searches before any claim"}
                      for s in survivors],
        "gate_fired_counts": fired, "candidates_scanned": len(v1),
        "per_candidate": v1,
        "honest_interpretation": (
            "collision/cross-checked rejection = saturation confirmed; "
            "survivor = rare, must re-verify deeper (R10)."),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    (RUN_DIR / "niche_find_check.json").write_text(json.dumps(verdict, indent=2))
    for v in v1:
        flags = "".join("1" if v[g]["pass"] else "0" for g in gates)
        print(f"  {v['cand_id']}: composite={v['composite']:.4f} gates[{flags}] "
              f"survived={v['survived']} failed={v['gates_failed']}")
    print(f"\n[gates] {verdict['verdict']} ({len(survivors)} survivor(s)); "
          f"determinism={'OK' if det_ok else 'BROKEN'} {h1[:16]}...")
    return 0


SUMMARY_PROMPT = """You are writing a strictly factual summary of a multi-agent run.
Below is the RAW REPORT LOG (verbatim agent outputs) and the GATE RESULTS (ground truth).

=== RAW REPORT LOG ===
{report}

=== GATE RESULTS (JSON) ===
{gates}

Write 4-7 sentences stating ONLY facts present above (do not infer or embellish numbers).
Then output a raw JSON object (no fences) with EXACTLY:
{{"n_candidates": <int>, "n_survivors": <int>, "verdict": "<NICHE_FOUND|NICHE_NOT_FOUND>", "per_candidate": [{{"cand_id": "<id>", "composite": <number>, "survived": <bool>}}]}}"""


def run_opus(prompt: str) -> dict:
    cfg = RULES["opus_subprocess"]
    cmd = [cfg["binary"], *cfg["args"], "--disallowedTools", *cfg["disallowed_tools"]]
    td = tempfile.mkdtemp(prefix="run15_sum_")
    proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                          timeout=cfg["timeout_seconds"], cwd=td)
    if proc.returncode != 0:
        raise RuntimeError(f"opus exit {proc.returncode}: {proc.stderr[:400]}")
    return json.loads(proc.stdout)


def parse_obj(text: str) -> dict | None:
    """Robust parse: whole text, then fenced blocks, then any balanced {...}.

    The balanced-brace fallback is essential: the summary model often emits a
    correct JSON object embedded in prose with NO code fences, which the first
    two strategies miss.
    """
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
    # balanced-brace fallback: scan for TOP-LEVEL {...} objects that parse,
    # preferring the LAST one (the model's final answer block). After a
    # balanced object is consumed, resume scanning AFTER it so nested objects
    # (e.g. per_candidate entries) are not mistaken for the outer answer.
    candidates = []
    start = text.find("{")
    while start != -1:
        depth = 0
        end = None
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    try:
                        candidates.append(json.loads(text[start:i + 1]))
                    except json.JSONDecodeError:
                        pass
                    break
        start = text.find("{", (end + 1) if end is not None else start + 1)
    return candidates[-1] if candidates else None


def cmd_finalize(_args) -> int:
    verdict = json.loads((RUN_DIR / "niche_find_check.json").read_text())
    gate_results = json.loads((LOGS / "gate_results.json").read_text())
    truth = {
        "n_candidates": verdict["candidates_scanned"],
        "n_survivors": len(verdict["survivors"]),
        "verdict": verdict["verdict"],
        "per_candidate": [{"cand_id": v["cand_id"], "composite": round(v["composite"], 4),
                           "survived": v["survived"]} for v in gate_results],
    }
    env = run_opus(SUMMARY_PROMPT.format(
        report=(LOGS / "report_log.md").read_text(),
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
        tby = {c["cand_id"]: c for c in truth["per_candidate"]}
        cby = {c.get("cand_id"): c for c in claimed.get("per_candidate", [])}
        for cid in cby:
            if cid not in tby:
                mism.append(f"fabricated cand_id {cid!r}")
        for cid, t in tby.items():
            c = cby.get(cid)
            if not c:
                mism.append(f"missing cand_id {cid!r}"); continue
            try:
                if abs(float(c.get("composite")) - float(t["composite"])) > 1e-4:
                    mism.append(f"{cid} composite {c.get('composite')} != {t['composite']}")
            except (TypeError, ValueError):
                mism.append(f"{cid} composite not numeric")
            if bool(c.get("survived")) != bool(t["survived"]):
                mism.append(f"{cid} survived {c.get('survived')} != {t['survived']}")
    hall = {"hallucination_detected": bool(mism), "no_hallucination": not mism,
            "mismatches": mism, "truth": truth, "claimed": claimed}
    (LOGS / "hallucination_check.json").write_text(json.dumps(hall, indent=2))
    det = json.loads((LOGS / "determinism_check.json").read_text())
    cc = json.loads((LOGS / "crosscheck.json").read_text())
    n_mismatch = sum(1 for c in cc.get("candidates", []) if c.get("mismatch_with_agent3"))
    proofs = {
        "agents_all_committed": all((LOGS / f).exists() for f in
                                    ("atoms.json", "candidates.json", "verify.json", "crosscheck.json")),
        "report_verbatim": "[REPORT 1]" in (LOGS / "report_log.md").read_text(),
        "four_gate_deterministic": det["determinism_ok"],
        "cross_check_ran": "candidates" in cc,
        "no_hallucination": hall["no_hallucination"],
    }
    (RUN_DIR / "proof_scorecard.json").write_text(json.dumps(
        {"proofs": proofs, "all_pass": all(proofs.values()),
         "verdict": verdict["verdict"], "n_survivors": truth["n_survivors"],
         "agent3_agent4_mismatches": n_mismatch,
         "generated_at": datetime.now(timezone.utc).isoformat()}, indent=2))
    print(f"VERDICT: {verdict['verdict']}  survivors={truth['n_survivors']}")
    print(f"determinism: {det['determinism_ok']}  no_hallucination: {hall['no_hallucination']}  "
          f"mismatches={hall['mismatches']}")
    print(f"agent3/agent4 cross-check mismatches: {n_mismatch}")
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

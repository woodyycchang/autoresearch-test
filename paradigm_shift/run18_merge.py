#!/usr/bin/env python3
"""Run 18 AGENT 3 (merger): pair the SPARSEST cross-paper sub-mechanism atoms.

Reads the per-atom saturation counts (AGENT 2) and the sentence-level atoms
(AGENT 1), ranks all CROSS-PAPER atom pairs by combined paper-hit count ascending,
takes the 5 sparsest, and merges each via a real Opus subprocess (R3/R4) with a
reasoning_trace (R9). Same-paper pairs are excluded (their sub-mechanisms already
co-occur in one paper, so they are trivially non-novel).

Reads : run_018/logs/atoms.json, run_018/logs/atom_search.json, run18_rules.json
Writes: run_018/logs/candidates.json + merge_<cid>.json envelopes

Usage: python3 paradigm_shift/run18_merge.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

THIS_DIR = Path(__file__).parent
RUN_DIR = THIS_DIR / "run_018"
LOGS = RUN_DIR / "logs"
RULES = json.loads((RUN_DIR / "run18_rules.json").read_text())
EPOCH = json.loads((RUN_DIR / "direction_params.json").read_text())["epoch"]
N_CAND = RULES["pair_selection"]["n_candidates"]
TRACE_FIELDS = RULES["reasoning_trace_schema"]["required_fields"]

PROMPT = """You are AGENT 3 (merger) in a transparent multi-agent niche-finding pipeline.
Merge two research sub-mechanism atoms (each a verbatim sentence from a different paper's abstract) into ONE candidate paradigm-shift niche in AI / LLMs.

ATOM A (id {a_id}, from {a_src}): "{a_text}"
ATOM B (id {b_id}, from {b_src}): "{b_text}"

These two sub-mechanisms were chosen because each is individually RARE in the literature. Combine the mechanism in ATOM A with the mechanism/principle in ATOM B into a single concrete, testable research niche, and expose your middle reasoning: what mechanism transfer you attempted, why, and what (if anything) makes the combination non-trivial rather than a surface analogy.

Output ONLY a raw JSON object - NO prose, NO markdown, NO code fences. EXACTLY these keys:
{{"mechanism": "1-2 sentences; MUST use concrete causal verbs (induces, produces, causes, transforms, regulates, activates, inhibits, routes)", "transfer": "1 sentence: what transfers from A to B", "open_problem": "1 sentence: the concrete open research question", "niche_name": "<=12 word title", "primary_quote": "a substring of AT LEAST 30 characters copied EXACTLY and VERBATIM from ATOM A's or ATOM B's text above - do not paraphrase, do not invent", "quote_source": "atom_a or atom_b", "reasoning_trace": {{"step": "merge ATOM A x ATOM B", "inputs_seen": "the two sub-mechanism sentences, summarized as the exact mechanisms you read", "reasoning": "which mechanism you tried to transfer from A to B, what alternatives you rejected, and specifically what makes this non-trivial vs a surface/vocabulary analogy", "decision": "the niche you settled on and why", "confidence": "high|medium|low followed by - and a one-clause reason", "could_be_wrong_if": "the concrete condition under which this merge is just a surface analogy or already trivial"}}}}

The primary_quote MUST appear character-for-character inside the text of the atom named by quote_source. Output nothing but the JSON object."""

_TMP = None


def tempdir():
    global _TMP
    if _TMP is None:
        _TMP = tempfile.mkdtemp(prefix="run18_opus_")
    return _TMP


def run_opus(prompt: str) -> dict:
    cfg = RULES["opus_subprocess"]
    cmd = [cfg["binary"], *cfg["args"], "--disallowedTools", *cfg["disallowed_tools"]]
    proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                          timeout=cfg["timeout_seconds"], cwd=tempdir())
    if proc.returncode != 0:
        raise RuntimeError(f"opus exit {proc.returncode}: {proc.stderr[:400]}")
    return json.loads(proc.stdout)


def parse_obj(text: str):
    text = (text or "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    for block in reversed(re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)):
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            continue
    start = text.find("{")
    while start != -1:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break
        start = text.find("{", start + 1)
    return None


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def trace_complete(tr):
    return isinstance(tr, dict) and all(norm(str(tr.get(f, ""))) for f in TRACE_FIELDS)


def select_pairs(atoms, hits):
    """All cross-paper pairs ranked by combined paper-hits ASC (deterministic)."""
    pairs = []
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            a, b = atoms[i], atoms[j]
            if a["paper_id"] == b["paper_id"]:
                continue  # same-paper sub-mechanisms already co-occur
            ha, hb = hits[a["atom_id"]], hits[b["atom_id"]]
            pairs.append((ha + hb, max(ha, hb), a["atom_id"], b["atom_id"], i, j))
    pairs.sort(key=lambda p: (p[0], p[1], p[2], p[3]))
    return pairs


def merge_pair(a, b):
    prompt = PROMPT.format(a_id=a["atom_id"], a_src=a["source_id"], a_text=a["text"],
                           b_id=b["atom_id"], b_src=b["source_id"], b_text=b["text"])
    parsed, envelopes, attempts = None, [], 0
    need = list(RULES["merge_schema"]["fields"])
    for attempt in range(1 + RULES["opus_subprocess"]["retry_on_parse_fail"]):
        attempts = attempt + 1
        env = run_opus(prompt)
        envelopes.append(env)
        parsed = parse_obj(env.get("result", ""))
        if parsed and all(k in parsed for k in need) and trace_complete(parsed.get("reasoning_trace")):
            break
    quote = norm(parsed.get("primary_quote", "")) if parsed else ""
    src = parsed.get("quote_source", "") if parsed else ""
    src_text = norm(a["text"]) if src == "atom_a" else norm(b["text"]) if src == "atom_b" else ""
    quote_verified = bool(quote) and len(quote) >= 30 and quote in src_text
    return {"parse_ok": parsed is not None, "attempts": attempts, "parsed": parsed,
            "quote_verified_substring": quote_verified,
            "reasoning_trace_complete": trace_complete((parsed or {}).get("reasoning_trace")),
            "envelopes": envelopes}


def main():
    atoms_all = json.loads((LOGS / "atoms.json").read_text())["atoms"]
    asearch = json.loads((LOGS / "atom_search.json").read_text())["atoms"]
    hits = {a["atom_id"]: a["paper_hits"] for a in asearch}
    is_mech = {a["atom_id"]: a.get("is_mechanism", True) for a in asearch}
    by_id = {a["atom_id"]: a for a in atoms_all}
    missing = [a["atom_id"] for a in atoms_all if a["atom_id"] not in hits]
    if missing:
        print(f"ERROR: atoms missing from atom_search: {missing}", file=sys.stderr)
        return 1
    # pair only MECHANISM atoms (exclude problem-statement/gap context sentences)
    atoms = [a for a in atoms_all if is_mech.get(a["atom_id"], True)]
    excluded = [a["atom_id"] for a in atoms_all if not is_mech.get(a["atom_id"], True)]
    print(f"[merge] {len(atoms)}/{len(atoms_all)} mechanism atoms eligible (excluded context: {excluded})")
    ranked = select_pairs(atoms, hits)
    chosen = ranked[:N_CAND]
    print(f"[merge] {len(ranked)} cross-paper pairs; taking {len(chosen)} sparsest:")
    candidates = []
    for idx, (combined, mx, aid, bid, i, j) in enumerate(chosen, 1):
        cid = f"CAND_018_{idx:03d}"
        a, b = by_id[aid], by_id[bid]
        print(f"  {cid}: {aid}(h={hits[aid]}) x {bid}(h={hits[bid]}) combined={combined} ...", flush=True)
        m = merge_pair(a, b)
        env = m["envelopes"][-1]
        (LOGS / f"merge_{cid}.json").write_text(json.dumps({"cand_id": cid, "atom_a_id": aid,
                                                            "atom_b_id": bid, **m}, indent=2))
        p = m["parsed"] or {}
        candidates.append({
            "cand_id": cid, "atom_a_id": aid, "atom_b_id": bid,
            "atom_a_hits": hits[aid], "atom_b_hits": hits[bid], "combined_atom_hits": combined,
            "niche_name": p.get("niche_name", ""), "mechanism": p.get("mechanism", ""),
            "transfer": p.get("transfer", ""), "open_problem": p.get("open_problem", ""),
            "primary_quote": p.get("primary_quote", ""), "quote_source": p.get("quote_source", ""),
            "quote_verified_substring": m["quote_verified_substring"],
            "reasoning_trace": p.get("reasoning_trace", {}),
            "reasoning_trace_complete": m["reasoning_trace_complete"],
            "parse_ok": m["parse_ok"], "attempts": m["attempts"],
            "opus_session_id": env.get("session_id"), "opus_cost_usd": env.get("total_cost_usd")})
        print(f"    -> parse_ok={m['parse_ok']} quote_verified={m['quote_verified_substring']} "
              f"trace_complete={m['reasoning_trace_complete']} niche={p.get('niche_name','')!r}")
    out = {"run_id": "run_018", "epoch": EPOCH, "agent": "3_merger",
           "generated_at": datetime.now(timezone.utc).isoformat(),
           "selection_rule": RULES["pair_selection"]["rule"],
           "chosen_pairs": [{"cand_id": f"CAND_018_{k+1:03d}", "atom_a": c[2], "atom_b": c[3],
                             "combined_atom_hits": c[0]} for k, c in enumerate(chosen)],
           "candidates": candidates}
    (LOGS / "candidates.json").write_text(json.dumps(out, indent=2))
    print(f"\n[merge] wrote {len(candidates)} candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())

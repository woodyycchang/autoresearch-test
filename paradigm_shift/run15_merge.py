#!/usr/bin/env python3
"""Run 15 AGENT 2 (merger) helper: real Opus subprocess merges -> candidates.json.

Encapsulates the PROVEN fixes so the merger agent runs ONE command:
  * R3: subprocess in a throwaway NON-GIT temp dir with all tools disallowed, so
    the host git Stop-hook bails (not a git repo) instead of hijacking output.
  * R4: force raw JSON (no prose/fences); robust parse with 1 retry.
  * Gate-4 grounding: primary_quote must be a real >=30-char substring of the
    named atom's source text; we VERIFY that here and record verified_quote so
    the orchestrator can trust it (and re-checks it anyway).

Reads : paradigm_shift/runs/run_015/logs/atoms.json   (from AGENT 1)
        paradigm_shift/runs/run_015/run15_rules.json
Writes: paradigm_shift/runs/run_015/logs/candidates.json
        paradigm_shift/runs/run_015/logs/merge_<cand_id>.json   (full envelopes)

Usage: python3 paradigm_shift/run15_merge.py
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
RUN_DIR = THIS_DIR / "runs" / "run_015"
LOGS = RUN_DIR / "logs"
RULES = json.loads((RUN_DIR / "run15_rules.json").read_text())

PROMPT = """You are merging two research atoms into ONE candidate paradigm-shift niche in AI / LLMs.

ATOM A (id {a_id}): "{a_text}"
ATOM B (id {b_id}): "{b_text}"

Combine the mechanism in ATOM A with the mechanism/principle in ATOM B into a single concrete, testable research niche.

Output ONLY a raw JSON object — NO prose, NO markdown, NO code fences. Exactly these keys:
{{"mechanism": "1-2 sentences; MUST use concrete causal verbs (induces, produces, causes, transforms, regulates, activates, inhibits, routes)", "transfer": "1 sentence: what transfers from A to B", "open_problem": "1 sentence: the concrete open research question", "niche_name": "<=12 word title", "primary_quote": "a substring of AT LEAST 30 characters copied EXACTLY and VERBATIM from ATOM A's or ATOM B's text above — do not paraphrase, do not invent", "quote_source": "atom_a or atom_b"}}

The primary_quote MUST appear character-for-character inside the text of the atom named by quote_source. Output nothing but the JSON object."""

_TMP: str | None = None


def tempdir() -> str:
    global _TMP
    if _TMP is None:
        _TMP = tempfile.mkdtemp(prefix="run15_opus_")
    return _TMP


def run_opus(prompt: str) -> dict:
    cfg = RULES["opus_subprocess"]
    cmd = [cfg["binary"], *cfg["args"], "--disallowedTools", *cfg["disallowed_tools"]]
    proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                          timeout=cfg["timeout_seconds"], cwd=tempdir())
    if proc.returncode != 0:
        raise RuntimeError(f"opus exit {proc.returncode}: {proc.stderr[:400]}")
    return json.loads(proc.stdout)


def parse_obj(text: str) -> dict | None:
    """Robust parse: try raw, then last fenced block, then first balanced {...}."""
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


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def merge_pair(a: dict, b: dict) -> dict:
    prompt = PROMPT.format(a_id=a["atom_id"], a_text=a["text"],
                           b_id=b["atom_id"], b_text=b["text"])
    parsed, envelopes, attempts = None, [], 0
    for attempt in range(1 + RULES["opus_subprocess"]["retry_on_parse_fail"]):
        attempts = attempt + 1
        env = run_opus(prompt)
        envelopes.append(env)
        parsed = parse_obj(env.get("result", ""))
        if parsed and all(k in parsed for k in RULES["merge_schema"]["fields"]):
            break
    # verify primary_quote is a real substring of the named atom (Gate-4 grounding)
    quote = norm(parsed.get("primary_quote", "")) if parsed else ""
    src = parsed.get("quote_source", "") if parsed else ""
    src_text = norm(a["text"]) if src == "atom_a" else norm(b["text"]) if src == "atom_b" else ""
    quote_verified = bool(quote) and len(quote) >= 30 and quote in src_text
    return {
        "atom_a_id": a["atom_id"], "atom_b_id": b["atom_id"],
        "parse_ok": parsed is not None, "attempts": attempts,
        "parsed": parsed, "quote_verified_substring": quote_verified,
        "envelopes": envelopes,
    }


def main() -> int:
    atoms = json.loads((LOGS / "atoms.json").read_text())["atoms"]
    if len(atoms) < 3:
        print(f"ERROR: need 3 atoms, got {len(atoms)}", file=sys.stderr)
        return 1
    # 3 pairs from 3 atoms: (0,1), (1,2), (0,2)
    pairs = [(0, 1), (1, 2), (0, 2)]
    candidates = []
    for idx, (i, j) in enumerate(pairs, 1):
        cid = f"CAND_015_{idx:03d}"
        print(f"[merge] {cid}: {atoms[i]['atom_id']} x {atoms[j]['atom_id']} ...", flush=True)
        m = merge_pair(atoms[i], atoms[j])
        env = m["envelopes"][-1]
        (LOGS / f"merge_{cid}.json").write_text(json.dumps(
            {"cand_id": cid, **m}, indent=2))
        p = m["parsed"] or {}
        candidates.append({
            "cand_id": cid,
            "atom_a_id": m["atom_a_id"], "atom_b_id": m["atom_b_id"],
            "niche_name": p.get("niche_name", ""),
            "mechanism": p.get("mechanism", ""),
            "transfer": p.get("transfer", ""),
            "open_problem": p.get("open_problem", ""),
            "primary_quote": p.get("primary_quote", ""),
            "quote_source": p.get("quote_source", ""),
            "quote_verified_substring": m["quote_verified_substring"],
            "parse_ok": m["parse_ok"], "attempts": m["attempts"],
            "opus_session_id": env.get("session_id"),
            "opus_cost_usd": env.get("total_cost_usd"),
        })
        print(f"  -> session {env.get('session_id')} parse_ok={m['parse_ok']} "
              f"quote_verified={m['quote_verified_substring']} niche={p.get('niche_name','')!r}")
    out = {"run_id": "run_015", "epoch": 1,
           "generated_at": datetime.now(timezone.utc).isoformat(),
           "pairs": [[i, j] for i, j in pairs], "candidates": candidates}
    (LOGS / "candidates.json").write_text(json.dumps(out, indent=2))
    print(f"\n[merge] wrote {len(candidates)} candidates to logs/candidates.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

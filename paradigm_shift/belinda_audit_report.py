"""Belinda 3-question audit report generator.

Given a candidate, builds a detailed per-candidate audit JSON with:
  Q1_atoms:     [{atom_id, verbatim_quote, transcript_id, snippet_id}]
  Q2_operators: {operator, atom_pairings: [...]}
  Q3_lines:     [{atom_id, transcript_id, line_start, line_end,
                  verbatim_text, line_in_file_check}]

The Q3 mechanical check (line_in_file_check) re-reads the transcript at
the cited line span and asserts the verbatim quote appears in that span
(whitespace-normalized substring). A candidate is rejected by this
report if ANY Q3 line check fails.

Pure data — no LLM calls.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def read_transcript_lines(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def check_line_span(quote: str, lines: List[str], start: int, end: int) -> dict:
    """Pull the text from lines[start-1:end] and check the quote is a
    (whitespace-normalized) substring. Returns {ok, text_at_span, quote_normalized}.
    """
    # 1-indexed line numbers per atom convention (verified against
    # paradigm_shift/runs/run_007/atoms_quality_filtered/* line_span values).
    span_text = "\n".join(lines[max(0, start - 1):end])
    span_norm = _norm(span_text)
    q_norm = _norm(quote)
    ok = q_norm in span_norm
    return {
        "ok": ok,
        "span_n_lines": end - start + 1,
        "span_text_preview": span_text[:240],
        "quote_normalized_preview": q_norm[:240],
    }


def build_candidate_audit(
    candidate: dict,
    atoms_by_id: Dict[str, dict],
    transcript_lines: Dict[str, List[str]],
    transcript_paths: Dict[str, str],
) -> dict:
    cid = candidate["candidate_id"]
    op = candidate.get("combination_operator", "")
    atom_ids = candidate.get("combined_atom_ids", [])

    # Q1: cited atoms
    q1: List[dict] = []
    for aid in atom_ids:
        a = atoms_by_id.get(aid, {})
        q1.append({
            "atom_id": aid,
            "atom_type": a.get("atom_type"),
            "paradigm_type": a.get("paradigm_type"),
            "transcript_id": a.get("transcript_id"),
            "snippet_id": a.get("snippet_id"),
            "verbatim_quote": a.get("verbatim_quote"),
            "line_span": a.get("line_span"),
            "exists_in_atoms_dir": bool(a),
        })

    # Q2: operator + atom pairings
    q2 = {
        "combination_operator": op,
        "atom_pairings": [
            {"position": "A", "atom_id": atom_ids[0] if len(atom_ids) > 0 else None,
             "paradigm_type": atoms_by_id.get(atom_ids[0], {}).get("paradigm_type") if atom_ids else None},
            {"position": "B", "atom_id": atom_ids[1] if len(atom_ids) > 1 else None,
             "paradigm_type": atoms_by_id.get(atom_ids[1], {}).get("paradigm_type") if len(atom_ids) > 1 else None},
        ],
    }

    # Q3: per-atom line check
    q3: List[dict] = []
    all_ok = True
    for aid in atom_ids:
        a = atoms_by_id.get(aid, {})
        tid = a.get("transcript_id")
        span = a.get("line_span") or [None, None]
        quote = a.get("verbatim_quote", "")
        lines = transcript_lines.get(tid)
        if not lines or not span[0]:
            all_ok = False
            q3.append({
                "atom_id": aid, "transcript_id": tid,
                "line_start": span[0], "line_end": span[1],
                "line_in_file_check": {"ok": False, "reason": "missing_transcript_or_span"},
            })
            continue
        chk = check_line_span(quote, lines, span[0], span[1])
        if not chk["ok"]:
            all_ok = False
        q3.append({
            "atom_id": aid,
            "transcript_id": tid,
            "transcript_path": transcript_paths.get(tid),
            "line_start": span[0],
            "line_end": span[1],
            "verbatim_text": quote,
            "line_in_file_check": chk,
        })

    return {
        "candidate_id": cid,
        "claim": candidate.get("claim"),
        "Q1_atoms": q1,
        "Q2_operators": q2,
        "Q3_lines": q3,
        "mechanical_check_all_pass": all_ok,
        "verdict": "PASS" if all_ok else "FAIL_Q3_mechanical",
    }


def load_atoms_index(atoms_dir: Path) -> Dict[str, dict]:
    idx: Dict[str, dict] = {}
    for p in atoms_dir.glob("ATOM_*.json"):
        with p.open("r", encoding="utf-8") as f:
            a = json.load(f)
        idx[a["atom_id"]] = a
    return idx

"""Run 9 epoch 2 — TRIPLE-atom combinator (counter ROOT_CAUSE_4).

Generates 3-atom candidates from 3 distinct speakers. Each triple must include:
  - one atom from a non-academic-pitch transcript (T004/T008/T009/T014)
  - two atoms forming a valid PAIR via the original 4 typed combinators
  - third atom either supplies the open_problem/blocker context or is an analogy bridge.

Triple combinators (extension of pair combinators):
  - PREDICTION_GROUNDED_IN_PRINCIPLE_RESOLVES_BLOCKER  (pred + fir + blocker)
  - ANALOGY_TRANSFERS_TO_OPEN_VIA_PRINCIPLE            (analogy + open + fir)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR.parent.parent.parent))

from run_9_pipeline import speaker_of  # type: ignore  # noqa: E402

NON_ACADEMIC_TRANSCRIPTS = {"T004", "T008", "T009", "T014"}


def short_quote(text: str, n: int = 80) -> str:
    s = text.replace("\n", " ").strip()
    return s if len(s) <= n else s[:n - 3] + "..."


def emit_triples_with_non_academic_anchor(atoms: list) -> list:
    """Return list of triple-candidate dicts."""
    by_type = {}
    for a in atoms:
        by_type.setdefault(a["paradigm_type"], []).append(a)
    preds = by_type.get("prediction", [])
    firs = by_type.get("first_principle", [])
    blks = by_type.get("blocker", [])
    ans = by_type.get("analogy", [])
    ops = by_type.get("open_problem", [])

    triples = []
    counter = 0
    ts_now = datetime.now(timezone.utc).isoformat()

    # 1. PRED_GROUND_RESOLVE: prediction + first_principle + blocker (3 distinct speakers)
    for p in preds:
        for fp in firs:
            for b in blks:
                speakers = {speaker_of(p["transcript_id"]), speaker_of(fp["transcript_id"]), speaker_of(b["transcript_id"])}
                if len(speakers) < 3:
                    continue
                tids = {p["transcript_id"], fp["transcript_id"], b["transcript_id"]}
                if not (tids & NON_ACADEMIC_TRANSCRIPTS):
                    continue
                counter += 1
                triples.append({
                    "candidate_id": f"TRIPLE_run_009_e2_{counter:04d}",
                    "combined_atom_ids": [p["atom_id"], fp["atom_id"], b["atom_id"]],
                    "combination_operator": "PRED_GROUNDED_IN_PRINCIPLE_RESOLVES_BLOCKER",
                    "claim": (
                        f"Prediction in atom {p['atom_id']} (\"{short_quote(p['verbatim_quote'])}\") "
                        f"holds under first-principle constraint {fp['atom_id']} "
                        f"(\"{short_quote(fp['verbatim_quote'])}\") and dissolves the blocker in "
                        f"{b['atom_id']} (\"{short_quote(b['verbatim_quote'])}\")."
                    ),
                    "speakers": sorted(speakers),
                    "source_transcripts": sorted(tids),
                    "non_academic_anchor_present": True,
                    "timestamp": ts_now,
                })

    # 2. ANALOGY_TO_OPEN_VIA_PRINCIPLE: analogy + open + fir (3 distinct speakers)
    for an in ans:
        for op in ops:
            for fp in firs:
                speakers = {speaker_of(an["transcript_id"]), speaker_of(op["transcript_id"]), speaker_of(fp["transcript_id"])}
                if len(speakers) < 3:
                    continue
                tids = {an["transcript_id"], op["transcript_id"], fp["transcript_id"]}
                if not (tids & NON_ACADEMIC_TRANSCRIPTS):
                    continue
                counter += 1
                triples.append({
                    "candidate_id": f"TRIPLE_run_009_e2_{counter:04d}",
                    "combined_atom_ids": [an["atom_id"], op["atom_id"], fp["atom_id"]],
                    "combination_operator": "ANALOGY_TRANSFERS_TO_OPEN_VIA_PRINCIPLE",
                    "claim": (
                        f"Apply analogy in {an['atom_id']} (\"{short_quote(an['verbatim_quote'])}\") "
                        f"to open problem {op['atom_id']} (\"{short_quote(op['verbatim_quote'])}\") "
                        f"under first-principle {fp['atom_id']} "
                        f"(\"{short_quote(fp['verbatim_quote'])}\")."
                    ),
                    "speakers": sorted(speakers),
                    "source_transcripts": sorted(tids),
                    "non_academic_anchor_present": True,
                    "timestamp": ts_now,
                })

    return triples

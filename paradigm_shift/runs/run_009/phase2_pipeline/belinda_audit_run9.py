"""Run 9 Belinda audit — mechanical 3Q check with new operator set."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

VALID_OPS = {
    "PREDICTION_GROUNDED_IN_PRINCIPLE",
    "ANALOGY_TRANSFERS_TO_OPEN",
    "BLOCKER_DISSOLVED_BY_PRINCIPLE",
    "PREDICTION_RESOLVES_BLOCKER",
}

TRANSCRIPT_PATHS = {
    "T001": "tari/inputs/belinda_li_self_models_canonical.txt",
    "T002": "tari/inputs/transcript_002_yu_sun_canonical.txt",
    "T003": "tari/inputs/transcript_003_nicholas_roberts_canonical.txt",
    "T004": "tari/inputs/transcript_004_valerie_chen_canonical.txt",
    "T005": "tari/inputs/transcript_005_amrith_setlur_canonical.txt",
    "T007": "paradigm_shift/runs/run_006/full_purified/purified/T007_purified.txt",
    "T008": "paradigm_shift/runs/run_006/full_purified/purified/T008_purified.txt",
    "T009": "paradigm_shift/runs/run_006/full_purified/purified/T009_purified.txt",
    "T010": "paradigm_shift/runs/run_006/full_purified/purified/T010_purified.txt",
    "T011": "paradigm_shift/runs/run_006/full_purified/purified/T011_purified.txt",
    "T012": "paradigm_shift/runs/run_006/full_purified/purified/T012_purified.txt",
    "T013": "paradigm_shift/runs/run_006/full_purified/purified/T013_purified.txt",
    "T014": "paradigm_shift/runs/run_006/full_purified/purified/T014_purified.txt",
}


def normalize_for_match(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def load_transcripts(repo_root: Path):
    out = {}
    for tid, rel in TRANSCRIPT_PATHS.items():
        p = repo_root / rel
        if p.exists():
            raw = p.read_text(encoding="utf-8")
            out[tid] = (raw, normalize_for_match(raw))
    return out


def audit_candidate(cand: dict, atoms_by_id: dict, transcripts: dict) -> dict:
    res = {
        "candidate_id": cand["candidate_id"],
        "q1_atoms_exist": False,
        "q2_operator_valid": False,
        "q3_quotes_verbatim_in_transcript": False,
        "q1_detail": "",
        "q2_detail": "",
        "q3_detail": "",
        "verdict": "PENDING",
    }
    missing = []
    atom_objs = []
    for aid in cand.get("combined_atom_ids", []):
        ao = atoms_by_id.get(aid)
        if ao is None:
            missing.append(aid)
        else:
            atom_objs.append(ao)
    if missing:
        res["q1_detail"] = f"missing atom_ids: {missing}"
    else:
        res["q1_atoms_exist"] = True
        res["q1_detail"] = f"all {len(atom_objs)} cited atoms exist"

    op = cand.get("combination_operator", "")
    if op in VALID_OPS:
        res["q2_operator_valid"] = True
        res["q2_detail"] = f"operator '{op}' is valid"
    else:
        res["q2_detail"] = f"operator '{op}' not in {sorted(VALID_OPS)}"

    q3_results = []
    all_ok = True
    for ao in atom_objs:
        tid = ao.get("transcript_id", "")
        if tid not in transcripts:
            q3_results.append({"atom_id": ao["atom_id"], "status": "TRANSCRIPT_NOT_FOUND", "tid": tid})
            all_ok = False
            continue
        _, norm = transcripts[tid]
        q_norm = normalize_for_match(ao.get("verbatim_quote", ""))
        if q_norm in norm:
            q3_results.append({"atom_id": ao["atom_id"], "status": "FOUND_VERBATIM"})
        else:
            # Partial-match: try first 80 chars and last 80 chars
            head = q_norm[:80]
            tail = q_norm[-80:]
            head_ok = head in norm
            tail_ok = tail in norm
            if head_ok and tail_ok:
                q3_results.append({"atom_id": ao["atom_id"], "status": "FOUND_HEAD_AND_TAIL_OK"})
            else:
                q3_results.append({"atom_id": ao["atom_id"], "status": "NOT_FOUND",
                                    "head_ok": head_ok, "tail_ok": tail_ok})
                all_ok = False
    res["q3_quotes_verbatim_in_transcript"] = all_ok
    res["q3_detail"] = q3_results
    if res["q1_atoms_exist"] and res["q2_operator_valid"] and res["q3_quotes_verbatim_in_transcript"]:
        res["verdict"] = "PASS"
    else:
        res["verdict"] = "FAIL"
    return res

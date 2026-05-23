"""Emit per-candidate Belinda 3Q audit reports for the 7 Run 7 survivors.

Writes to paradigm_shift/runs/run_008/phase2_retro/audit/CAND_X_belinda_audit.json
(also serves as Phase 2 detailed report).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "paradigm_shift"))

from belinda_audit_report import (
    build_candidate_audit, load_atoms_index, read_transcript_lines,
)


TRANSCRIPT_PATHS = {
    "T001": REPO / "tari/inputs/belinda_li_self_models_canonical.txt",
    "T002": REPO / "tari/inputs/transcript_002_yu_sun_canonical.txt",
    "T003": REPO / "tari/inputs/transcript_003_nicholas_roberts_canonical.txt",
    "T004": REPO / "tari/inputs/transcript_004_valerie_chen_canonical.txt",
    "T005": REPO / "tari/inputs/transcript_005_amrith_setlur_canonical.txt",
    "T007": REPO / "paradigm_shift/runs/run_006/full_purified/purified/T007_purified.txt",
    "T008": REPO / "paradigm_shift/runs/run_006/full_purified/purified/T008_purified.txt",
    "T009": REPO / "paradigm_shift/runs/run_006/full_purified/purified/T009_purified.txt",
    "T010": REPO / "paradigm_shift/runs/run_006/full_purified/purified/T010_purified.txt",
    "T011": REPO / "paradigm_shift/runs/run_006/full_purified/purified/T011_purified.txt",
    "T012": REPO / "paradigm_shift/runs/run_006/full_purified/purified/T012_purified.txt",
    "T013": REPO / "paradigm_shift/runs/run_006/full_purified/purified/T013_purified.txt",
    "T014": REPO / "paradigm_shift/runs/run_006/full_purified/purified/T014_purified.txt",
}

SURVIVOR_IDS = [
    "CAND_run_007_005", "CAND_run_007_011", "CAND_run_007_012",
    "CAND_run_007_026", "CAND_run_007_029", "CAND_run_007_048",
    "CAND_run_007_051",
]


def main():
    candidates_dir = REPO / "paradigm_shift/runs/run_007/candidates"
    atoms_dir = REPO / "paradigm_shift/runs/run_007/atoms_quality_filtered"
    out_dir = REPO / "paradigm_shift/runs/run_008/phase2_retro/audit"
    out_dir.mkdir(parents=True, exist_ok=True)

    atoms = load_atoms_index(atoms_dir)
    tlines = {tid: read_transcript_lines(p) for tid, p in TRANSCRIPT_PATHS.items()}
    tpaths = {tid: str(p) for tid, p in TRANSCRIPT_PATHS.items()}

    n_pass = n_fail = 0
    for cid in SURVIVOR_IDS:
        cand = json.loads((candidates_dir / f"{cid}.json").read_text())
        rpt = build_candidate_audit(cand, atoms, tlines, tpaths)
        (out_dir / f"{cid}_belinda_audit.json").write_text(
            json.dumps(rpt, indent=2), encoding="utf-8"
        )
        if rpt["verdict"] == "PASS":
            n_pass += 1
        else:
            n_fail += 1
        # Print summary line
        atoms_str = ", ".join([a["atom_id"] for a in rpt["Q1_atoms"]])
        lines_str = "; ".join([f"{q['transcript_id']}:{q['line_start']}-{q['line_end']}"
                               for q in rpt["Q3_lines"]])
        print(f"{cid}: {rpt['verdict']}")
        print(f"  Q1_atoms: {atoms_str}")
        print(f"  Q2_operator: {rpt['Q2_operators']['combination_operator']}")
        print(f"  Q3_lines: {lines_str}")

    print()
    print(f"Phase-2 audit summary: n_pass={n_pass} n_fail={n_fail}")


if __name__ == "__main__":
    main()

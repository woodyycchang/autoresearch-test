"""Emit per-candidate Belinda 3Q audit JSON for each Run 8 final survivor.

Output: paradigm_shift/runs/run_008/audit/CAND_X_belinda_audit.json
Each report includes Q1_atoms (with verbatim quotes), Q2_operators
(operator + atom pairings), and Q3_lines (transcript_id, line_start,
line_end, verbatim_text per atom). Mechanical check: every cited line
span re-read from transcript file must contain the verbatim quote.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
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


def main():
    run_dir = REPO / "paradigm_shift/runs/run_008"
    candidates_dir = run_dir / "candidates"
    atoms_dir = run_dir / "atoms_quality_filtered"
    out_dir = run_dir / "audit"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads((run_dir / "run_008_manifest.json").read_text())
    final_ids = manifest["final_survivors_post_all_7_layers"]

    atoms = load_atoms_index(atoms_dir)
    tlines = {tid: read_transcript_lines(p) for tid, p in TRANSCRIPT_PATHS.items()}
    tpaths = {tid: str(p) for tid, p in TRANSCRIPT_PATHS.items()}

    n_pass = n_fail = 0
    rejected = []
    for cid in final_ids:
        cand = json.loads((candidates_dir / f"{cid}.json").read_text())
        rpt = build_candidate_audit(cand, atoms, tlines, tpaths)
        (out_dir / f"{cid}_belinda_audit.json").write_text(
            json.dumps(rpt, indent=2), encoding="utf-8"
        )
        if rpt["verdict"] == "PASS":
            n_pass += 1
            print(f"{cid}: PASS")
        else:
            n_fail += 1
            rejected.append(cid)
            print(f"{cid}: {rpt['verdict']}")

    # Persist post-audit survivor list (reject anyone failing mechanical check)
    audited_survivors = [c for c in final_ids if c not in rejected]
    (run_dir / "phase7_audit_survivors.json").write_text(
        json.dumps(audited_survivors, indent=2)
    )
    print()
    print(f"Phase 4 audit: n_pass={n_pass} n_fail={n_fail}")
    print(f"audited survivors: {audited_survivors}")


if __name__ == "__main__":
    main()

"""Phase-2 driver: run Belinda 3Q self-model audit on the 7 Run 7 survivors.

Extends TARI's VALID_OPERATORS with paradigm-shift typed combinators
(same pattern as paradigm_shift/orchestrator.py line 391-397), then
audits each survivor against its source transcript.

Outputs:
  paradigm_shift/runs/run_008/phase2_retro/belinda_audit_run_007_survivors.json
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tari"))
sys.path.insert(0, str(REPO / "paradigm_shift"))

import self_model_audit as sma
from analogy_engine import VALID_TYPED_COMBINATORS
for op in VALID_TYPED_COMBINATORS:
    sma.VALID_OPERATORS.add(op)


SURVIVOR_IDS = [
    "CAND_run_007_005", "CAND_run_007_011", "CAND_run_007_012",
    "CAND_run_007_026", "CAND_run_007_029", "CAND_run_007_048",
    "CAND_run_007_051",
]

# Per-transcript path map (T001-T005 canonical, T007-T014 purified)
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
    candidates_dir = REPO / "paradigm_shift/runs/run_007/candidates"
    atoms_dir = REPO / "paradigm_shift/runs/run_007/atoms_quality_filtered"
    out_dir = REPO / "paradigm_shift/runs/run_008/phase2_retro"
    out_path = out_dir / "belinda_audit_run_007_survivors.json"

    # Use single-candidate audit (audit_candidate) per ID
    raw_map, norm_map = {}, {}
    for tid, tp in TRANSCRIPT_PATHS.items():
        r, n = sma.load_transcript(Path(tp))
        raw_map[tid] = r
        norm_map[tid] = n

    results = []
    for cid in SURVIVOR_IDS:
        cp = candidates_dir / f"{cid}.json"
        res = sma.audit_candidate(cp, atoms_dir, norm_map, raw_map)
        results.append(res)

    out = {
        "audited_ids": SURVIVOR_IDS,
        "n_pass": sum(1 for r in results if r.verdict == "PASS"),
        "n_pass_with_caveat": sum(1 for r in results
                                  if r.verdict == "PASS_WITH_CAVEAT"),
        "n_fail": sum(1 for r in results if r.verdict.startswith("FAIL")),
        "results": [r.__dict__ for r in results],
    }
    out_path.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")

    print(f"audit n_pass={out['n_pass']} n_pass_with_caveat={out['n_pass_with_caveat']} "
          f"n_fail={out['n_fail']}")
    for r in results:
        print(f"  {r.candidate_id}: {r.verdict}")


if __name__ == "__main__":
    main()

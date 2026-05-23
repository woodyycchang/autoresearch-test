"""Run 7 pipeline driver: atom_quality_filter → analogy_engine →
semantic_coherence_check → arxiv_gate.

Run 6 produced 14 candidates that survived the arXiv gate but were all
surface-level analogy combinations. Run 7 adds two filters:

  - atom_quality_filter  (Phase 2 of Run 7)  — strips talk-language /
    illustrative / fragment atoms BEFORE pairing.
  - semantic_coherence_check (Phase 1 of Run 7) — rejects cross-domain
    surface pairings AFTER candidate generation.

The arXiv gate is reused from Run 6 but is now applied only to
candidates that survived semantic coherence — saving live search calls.

This script reads Run 6's full purified atom store as input (so we get
an apples-to-apples comparison) and writes Run 7's artifacts under
`paradigm_shift/runs/run_007/`.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

from atom_quality_filter import filter_atoms_dir  # noqa: E402
from analogy_engine import brainstorm_paradigm_candidates  # noqa: E402
from semantic_coherence_check import check_all as coherence_check_all  # noqa: E402


def run_pipeline(
    source_atoms_dir: Path,
    run_dir: Path,
    run_id: str = "run_007",
    max_per_operator: int = 14,
    require_cross_transcript: bool = True,
):
    run_dir.mkdir(parents=True, exist_ok=True)

    # ---- Step A: atom quality filter ----
    filtered_atoms_dir = run_dir / "atoms_quality_filtered"
    atom_report_path = run_dir / "atom_quality_report.json"
    print(f"[STEP A] atom_quality_filter: {source_atoms_dir} → {filtered_atoms_dir}")
    verdicts_a, report_a = filter_atoms_dir(
        source_atoms_dir, filtered_atoms_dir, atom_report_path,
    )
    print(f"  kept {report_a['n_kept']} / {report_a['n_input']} atoms")
    for k, n in sorted(report_a["verdict_distribution"].items(), key=lambda x: -x[1]):
        print(f"    {k:36s} {n}")

    # ---- Step B: brainstorm candidates from filtered atoms ----
    candidates_dir = run_dir / "candidates"
    if candidates_dir.exists():
        import shutil
        shutil.rmtree(candidates_dir)
    print(f"[STEP B] analogy_engine brainstorm: {filtered_atoms_dir} → {candidates_dir}")
    cands = brainstorm_paradigm_candidates(
        filtered_atoms_dir, candidates_dir,
        run_id=run_id,
        max_per_operator=max_per_operator,
        require_cross_transcript=require_cross_transcript,
    )
    print(f"  brainstormed {len(cands)} candidates")

    # ---- Step C: semantic coherence check ----
    coherence_report_path = run_dir / "semantic_coherence_report.json"
    print(f"[STEP C] semantic_coherence_check: {candidates_dir}")
    verdicts_c, report_c = coherence_check_all(
        candidates_dir, filtered_atoms_dir, coherence_report_path,
    )
    print(f"  verdicts: {report_c['verdict_distribution']}")
    print(f"  accepted: {len(report_c['accepted_ids'])} / {report_c['n_total']}")

    # Persist surviving candidate IDs (semantic coherence layer)
    survivors_after_coherence = report_c["accepted_ids"]
    (run_dir / "survivors_after_coherence.json").write_text(
        json.dumps(survivors_after_coherence, indent=2),
        encoding="utf-8",
    )

    # ---- Step D: emit per-survivor sub-claim queries ----
    # We do NOT call the live web_search inside this script; the harness
    # (Claude) issues those externally via WebSearch tool calls so the
    # anti-hallucination audit can verify they really happened.
    # Instead we emit `subclaim_queries.json` so the harness has a list
    # to iterate over.
    subclaim_queries: List[Dict] = []
    for cid in survivors_after_coherence:
        with (candidates_dir / f"{cid}.json").open("r", encoding="utf-8") as f:
            cand = json.load(f)
        # Build 1-2 sub-claim queries from the atom quotes (no template filler).
        atom_a_id, atom_b_id = cand["combined_atom_ids"]
        atom_a = json.load((filtered_atoms_dir / f"{atom_a_id}.json").open())
        atom_b = json.load((filtered_atoms_dir / f"{atom_b_id}.json").open())
        # Extract a tight query from each atom's verbatim quote: top
        # content words.
        from semantic_coherence_check import content_words
        words_a = content_words(atom_a["verbatim_quote"])
        words_b = content_words(atom_b["verbatim_quote"])
        q_a = " ".join(words_a[:6])
        q_b = " ".join(words_b[:6])
        subclaim_queries.append({
            "candidate_id": cid,
            "atom_a": atom_a_id, "atom_b": atom_b_id,
            "query_a": q_a, "query_b": q_b,
        })
    (run_dir / "subclaim_queries.json").write_text(
        json.dumps(subclaim_queries, indent=2),
        encoding="utf-8",
    )

    # ---- Manifest ----
    manifest = {
        "run_id": run_id,
        "source_atoms_dir": str(source_atoms_dir),
        "max_per_operator": max_per_operator,
        "require_cross_transcript": require_cross_transcript,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "atoms_n_input": report_a["n_input"],
        "atoms_n_kept": report_a["n_kept"],
        "candidates_n_generated": len(cands),
        "candidates_n_coherence_accepted": len(survivors_after_coherence),
    }
    (run_dir / "run_007_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    print()
    print("=== Run 7 pipeline complete ===")
    print(f"manifest: {run_dir / 'run_007_manifest.json'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source_atoms_dir", required=True, type=Path)
    ap.add_argument("--run_dir", required=True, type=Path)
    ap.add_argument("--run_id", default="run_007")
    ap.add_argument("--max_per_operator", type=int, default=14)
    ap.add_argument("--allow_intra_transcript", action="store_true")
    args = ap.parse_args()
    run_pipeline(
        source_atoms_dir=args.source_atoms_dir,
        run_dir=args.run_dir,
        run_id=args.run_id,
        max_per_operator=args.max_per_operator,
        require_cross_transcript=not args.allow_intra_transcript,
    )


if __name__ == "__main__":
    main()

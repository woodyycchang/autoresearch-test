"""Impact label logger for Paradigm-Shift Finder v1.

After each run, prompt the user to label the top-K (default 3) candidates
on a 1-5 impact scale. Labels accumulate in paradigm_shift/impact_labels.json
and feed `impact_filter.refit_weights` once >= 10 labels accumulate.

The logger has two modes:

  1. CLI mode (interactive): prints a labeling prompt and reads user input.
  2. Programmatic mode: receives a {candidate_id: label_int} map and appends
     to the labels file. This is used by the orchestrator + an external
     agent loop.

The actual labeling is the USER's responsibility (the value of the label
depends on the user's own taste for impact). The logger only handles storage
and the prompt UI.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ImpactLabel:
    candidate_id: str
    run_id: str
    predicted_impact: float
    user_label: int             # 1..5
    time_horizon: float
    impact_scale: float
    poc_tractability: float
    information_asymmetry: float
    labeled_at: str


def load_labels(labels_path: Path) -> List[dict]:
    if not labels_path.exists():
        return []
    with labels_path.open("r", encoding="utf-8") as f:
        return json.load(f).get("labels", [])


def append_labels(labels_path: Path, new_labels: List[dict]) -> int:
    """Append new_labels to labels_path; return the new total."""
    existing = load_labels(labels_path)
    # De-dup by (candidate_id, run_id)
    keyset = {(l["candidate_id"], l["run_id"]) for l in existing}
    appended = 0
    for lab in new_labels:
        key = (lab["candidate_id"], lab["run_id"])
        if key in keyset:
            continue
        existing.append(lab)
        keyset.add(key)
        appended += 1
    labels_path.parent.mkdir(parents=True, exist_ok=True)
    with labels_path.open("w", encoding="utf-8") as f:
        json.dump({
            "labels": existing,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "n_labels": len(existing),
        }, f, indent=2)
    return appended


def build_label_prompt(
    candidates: List[dict],
    run_id: str,
    top_k: int = 3,
) -> str:
    """Build a human-readable labeling prompt for the user.

    Returns a markdown-ish string the orchestrator can print at end of run.
    Each candidate is shown with its predicted_impact and the 4 axis values.
    """
    # Sort by predicted_impact desc
    scored = sorted(
        [c for c in candidates if c.get("impact_score")],
        key=lambda c: -c["impact_score"]["predicted_impact"],
    )[:top_k]

    lines: List[str] = []
    lines.append(f"# Impact Labeling Prompt — {run_id}")
    lines.append("")
    lines.append("Please label each candidate below with a 1-5 impact score:")
    lines.append("  1 = trivial / wouldn't change anything")
    lines.append("  2 = small (one product feature) ")
    lines.append("  3 = medium (one startup direction)")
    lines.append("  4 = large (subfield-redirecting)")
    lines.append("  5 = paradigm-shift (whole industry redirected)")
    lines.append("")
    for i, c in enumerate(scored, start=1):
        sc = c["impact_score"]
        lines.append(f"## {i}. {c['candidate_id']}  (predicted_impact={sc['predicted_impact']:.3f})")
        lines.append("")
        lines.append(f"- **Operator:** {c.get('combination_operator')}")
        lines.append(f"- **Atoms:** {', '.join(c.get('combined_atom_ids', []))}")
        lines.append(f"- **Time horizon:** {sc['time_horizon']:.1f} years")
        lines.append(f"- **Impact scale (log10):** {sc['impact_scale']:.1f}")
        lines.append(f"- **POC tractability:** {sc['poc_tractability']:.2f}")
        lines.append(f"- **Info asymmetry:** {sc['information_asymmetry']:.2f}")
        lines.append("")
        lines.append(f"- **Claim:** {c.get('claim', '')[:600]}")
        lines.append(f"- **Validity hypothesis:** {c.get('first_principles_validity_hypothesis', '')[:400]}")
        lines.append(f"- **Why useful:** {c.get('why_potentially_useful', '')[:400]}")
        stress = c.get("stress_verdict") or {}
        if stress:
            lines.append(f"- **Stress verdict:** {stress.get('verdict')} "
                          f"({stress.get('n_grounded', 0)}/{stress.get('n_sub_claims', 0)} sub-claims grounded)")
        market = c.get("market_verdict") or {}
        if market:
            lines.append(f"- **Market verdict:** {market.get('verdict')} "
                          f"({market.get('n_strong_matches', 0)} matches)")
        lines.append("")
        lines.append(f"**Your label (1-5):** ___")
        lines.append("")

    lines.append("---")
    lines.append("To record labels, run:")
    lines.append("  python paradigm_shift/impact_label_logger.py record \\")
    lines.append("    --run_id <ID> --candidates_dir <DIR> --labels '<CAND_ID>:<SCORE>,...'")
    lines.append("")
    return "\n".join(lines)


def record_labels_from_map(
    labels_path: Path,
    run_id: str,
    candidates_dir: Path,
    label_map: Dict[str, int],
) -> int:
    """Build ImpactLabel records from label_map (cand_id → score) by reading
    each candidate's impact_score axes from disk; append to labels_path.
    """
    new: List[dict] = []
    for cand_id, score in label_map.items():
        cp = candidates_dir / f"{cand_id}.json"
        if not cp.exists():
            print(f"  [WARN] {cand_id}.json not found in {candidates_dir}; skipping")
            continue
        with cp.open("r", encoding="utf-8") as f:
            cand = json.load(f)
        sc = cand.get("impact_score")
        if not sc:
            print(f"  [WARN] {cand_id} has no impact_score field; skipping")
            continue
        new.append(asdict(ImpactLabel(
            candidate_id=cand_id,
            run_id=run_id,
            predicted_impact=sc["predicted_impact"],
            user_label=int(score),
            time_horizon=sc["time_horizon"],
            impact_scale=sc["impact_scale"],
            poc_tractability=sc["poc_tractability"],
            information_asymmetry=sc["information_asymmetry"],
            labeled_at=datetime.now(timezone.utc).isoformat(),
        )))
    return append_labels(labels_path, new)


def parse_label_arg(s: str) -> Dict[str, int]:
    """Parse 'CAND_001_007:4,CAND_001_005:3' into {id: score}."""
    out: Dict[str, int] = {}
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        cid, _, sc = part.partition(":")
        try:
            out[cid.strip()] = int(sc.strip())
        except ValueError:
            continue
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_prompt = sub.add_parser("prompt")
    p_prompt.add_argument("--candidates_dir", required=True, type=Path)
    p_prompt.add_argument("--run_id", required=True)
    p_prompt.add_argument("--top_k", type=int, default=3)
    p_prompt.add_argument("--out_path", type=Path, default=None)

    p_record = sub.add_parser("record")
    p_record.add_argument("--labels_path", required=True, type=Path)
    p_record.add_argument("--run_id", required=True)
    p_record.add_argument("--candidates_dir", required=True, type=Path)
    p_record.add_argument("--labels", required=True,
                          help="Comma-separated CAND_ID:SCORE pairs (score 1-5)")

    args = ap.parse_args()

    if args.cmd == "prompt":
        candidates = []
        for cp in sorted(args.candidates_dir.glob("CAND_*.json")):
            with cp.open("r", encoding="utf-8") as f:
                candidates.append(json.load(f))
        prompt = build_label_prompt(candidates, run_id=args.run_id, top_k=args.top_k)
        if args.out_path:
            args.out_path.write_text(prompt, encoding="utf-8")
            print(f"wrote labeling prompt to {args.out_path}")
        else:
            print(prompt)

    elif args.cmd == "record":
        m = parse_label_arg(args.labels)
        n = record_labels_from_map(args.labels_path, args.run_id, args.candidates_dir, m)
        print(f"appended {n} labels to {args.labels_path}")


if __name__ == "__main__":
    main()

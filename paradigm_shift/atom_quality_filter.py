"""Atom quality filter for Paradigm-Shift Finder Run 5.

Run 1's atom extractor was precision-biased and over-filtered tech-leader
talks: long-form colloquial speech ("I think eventually we'll see...")
matched the prediction/blocker regexes too broadly, while substantive
talks about scaling laws, world models, JEPA, software 2.0/3.0, agents,
distillation, and distributed compute fell through because their vocab
didn't trigger the original patterns.

This module re-scores each extracted atom AFTER atom_typer and KEEPS the
atom if EITHER of:
  (1) the atom's verbatim_quote contains >=1 token from POSITIVE_VOCABULARY
  (2) the atom's paradigm_type is open_problem OR first_principle

Rationale for the OR-rule: open_problem and first_principle atoms are
structurally hard to produce (the regexes are conservative), so any
extracted atom of those types is high signal even without a positive-
vocabulary hit. predictions/analogies/blockers/trends, by contrast,
fire on conversational tics; we want a content-word anchor to retain.

This is a RELAXATION, not a tightening — Run 5 expects more atoms per
transcript than Run 1, not fewer.

Honest deviation: the positive vocabulary is hand-curated from the
intersection of (a) the user's stated terms in the Run 5 task spec and
(b) terms that appear across multiple tech-leader transcripts. A
positive-vocab hit is not a quality oracle; it is an anchor that says
"this atom is at least about a topic that's been a paradigm-shift
candidate in the last decade." Atoms about wholly novel topics could
fail this filter — that is a known false-negative.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set


# Positive vocabulary — concepts that have been at the center of paradigm-shift
# arguments in 2014-2026. Curated from Run 5 prompt + tech-leader transcripts.
# Words are lowercased; matched via word-boundary regex on the verbatim quote.
POSITIVE_VOCABULARY: Set[str] = {
    # Scaling & compute
    "agi", "scaling", "scaling law", "scaling laws", "compute", "moore",
    "exponential", "doubling", "trillion",
    # World models / JEPA / self-supervised
    "world model", "world models", "jepa", "self-supervised", "self supervised",
    "predictive model", "energy-based", "energy based", "ssl",
    # Software 2.0 / 3.0
    "software 2.0", "software 3.0", "neural network", "weights",
    "differentiable", "gradient", "loss function",
    # Agents
    "agent", "agents", "agentic", "tool use", "tool-use", "browser agent",
    # Distillation & compression
    "distillation", "distill", "teacher", "student model", "compression",
    "knowledge distillation",
    # Distributed
    "distributed", "decentralized", "federated", "device", "edge",
    # Multi-modal & embodied
    "multi-modal", "multimodal", "vision-language", "vision language",
    "embodied", "robotics", "robot", "simulator", "simulation", "sim-to-real",
    # Foundation / pretraining
    "pretraining", "pre-training", "pretrained", "foundation model",
    "foundation models", "in-context", "in context", "few-shot",
    # Inference-time
    "test-time", "test time", "inference-time", "chain-of-thought",
    "reasoning", "reasoning model", "reasoning models",
    # Alignment / safety
    "alignment", "rlhf", "rlaif", "constitutional", "instruct", "feedback",
    # Bitter Lesson + Sutton
    "bitter lesson", "experience", "rl",
    # Forward-Forward + Hinton
    "forward-forward", "forward forward", "backpropagation", "back-propagation",
    "capsule", "ff algorithm",
    # Naval / market-making
    "leverage", "code", "media", "specific knowledge", "judgment",
    # Common across leaders
    "prediction", "predict", "predictions", "future", "horizon",
    "frontier", "transformer", "attention", "long context",
    "memory", "continual", "lifelong", "online learning",
}


# Compile a single regex that matches any positive-vocab token at word
# boundary. Multi-word entries become `\bw1\s+w2\b`.
def _build_positive_regex() -> re.Pattern:
    parts = []
    for term in sorted(POSITIVE_VOCABULARY, key=lambda x: -len(x)):
        # Replace internal whitespace with \s+, escape rest
        escaped = re.escape(term).replace(r"\ ", r"\s+").replace(r"\-", r"[-\s]?")
        parts.append(rf"\b{escaped}\b")
    return re.compile("|".join(parts), re.IGNORECASE)


POSITIVE_REGEX = _build_positive_regex()


# Types that always pass even without a positive-vocab match.
ALWAYS_KEEP_TYPES: Set[str] = {"open_problem", "first_principle"}


@dataclass
class AtomQualityRecord:
    atom_id: str
    paradigm_type: str
    transcript_id: str
    snippet_id: str
    has_positive_vocab: bool
    matched_vocab_terms: List[str]
    is_always_keep_type: bool
    keep: bool
    reason: str


def score_atom(atom: dict) -> AtomQualityRecord:
    """Score one atom dict (as written by atom_typer) and return the keep
    decision plus the matched vocabulary terms."""
    quote = atom.get("verbatim_quote", "")
    matches = sorted({m.group(0).lower() for m in POSITIVE_REGEX.finditer(quote)})
    has_pos = len(matches) > 0
    ptype = atom.get("paradigm_type", "")
    always_keep = ptype in ALWAYS_KEEP_TYPES

    if has_pos and always_keep:
        keep = True
        reason = "positive_vocab_AND_always_keep_type"
    elif has_pos:
        keep = True
        reason = "positive_vocab_hit"
    elif always_keep:
        keep = True
        reason = "always_keep_type"
    else:
        keep = False
        reason = "no_positive_vocab_and_not_always_keep_type"

    return AtomQualityRecord(
        atom_id=atom["atom_id"],
        paradigm_type=ptype,
        transcript_id=atom.get("transcript_id", ""),
        snippet_id=atom.get("snippet_id", ""),
        has_positive_vocab=has_pos,
        matched_vocab_terms=matches,
        is_always_keep_type=always_keep,
        keep=keep,
        reason=reason,
    )


def filter_atoms_dir(
    atoms_dir: Path,
    out_dir: Optional[Path] = None,
) -> Dict:
    """Apply quality filter to every ATOM_*.json in atoms_dir.

    If out_dir is provided, REWRITE the kept atoms there (one file per
    atom) and write a `_quality_filter.json` report there.

    If out_dir is None, mutate atoms_dir in place: delete rejected atoms,
    write a `_quality_filter.json` report alongside the kept ones, and
    rewrite `_index.json` to reflect the new counts. This is the mode
    the orchestrator uses.

    Returns the report dict.
    """
    in_place = out_dir is None or out_dir == atoms_dir
    target_dir = atoms_dir if in_place else out_dir
    if not in_place:
        target_dir.mkdir(parents=True, exist_ok=True)

    records: List[AtomQualityRecord] = []
    kept_atoms: List[dict] = []
    rejected_atoms: List[dict] = []

    for ap in sorted(atoms_dir.glob("ATOM_*.json")):
        with ap.open("r", encoding="utf-8") as f:
            atom = json.load(f)
        rec = score_atom(atom)
        records.append(rec)
        if rec.keep:
            kept_atoms.append(atom)
            if not in_place:
                with (target_dir / ap.name).open("w", encoding="utf-8") as f:
                    json.dump(atom, f, indent=2, ensure_ascii=False)
        else:
            rejected_atoms.append(atom)
            if in_place:
                ap.unlink()

    by_type = {}
    by_transcript = {}
    for a in kept_atoms:
        ptype = a.get("paradigm_type", "")
        tid = a.get("transcript_id", "")
        by_type[ptype] = by_type.get(ptype, 0) + 1
        by_transcript[tid] = by_transcript.get(tid, 0) + 1

    report = {
        "n_input": len(records),
        "n_kept": len(kept_atoms),
        "n_rejected": len(rejected_atoms),
        "kept_atom_ids": [a["atom_id"] for a in kept_atoms],
        "rejected_atom_ids": [a["atom_id"] for a in rejected_atoms],
        "by_paradigm_type_kept": by_type,
        "by_transcript_kept": by_transcript,
        "kept_by_reason": _count_reasons([r for r in records if r.keep]),
        "rejected_by_reason": _count_reasons([r for r in records if not r.keep]),
        "filtered_at": datetime.now(timezone.utc).isoformat(),
        "positive_vocabulary_size": len(POSITIVE_VOCABULARY),
        "always_keep_types": sorted(ALWAYS_KEEP_TYPES),
    }
    with (target_dir / "_quality_filter.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Refresh _index.json so downstream stages see only kept atoms
    if in_place:
        idx = {
            "n_atoms": len(kept_atoms),
            "atom_ids": [a["atom_id"] for a in kept_atoms],
            "paradigm_type_distribution": by_type,
            "transcript_distribution": by_transcript,
            "post_quality_filter": True,
            "filtered_at": report["filtered_at"],
        }
        with (target_dir / "_index.json").open("w", encoding="utf-8") as f:
            json.dump(idx, f, indent=2, ensure_ascii=False)

    # Also write a per-atom records file for diagnostics
    with (target_dir / "_quality_records.json").open("w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in records], f, indent=2, ensure_ascii=False)

    return report


def _count_reasons(records: List[AtomQualityRecord]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for r in records:
        out[r.reason] = out.get(r.reason, 0) + 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atoms_dir", required=True, type=Path,
                    help="Directory of ATOM_*.json files produced by atom_typer.")
    ap.add_argument("--out_dir", type=Path, default=None,
                    help="If set, write kept atoms here; else mutate atoms_dir in place.")
    args = ap.parse_args()

    report = filter_atoms_dir(args.atoms_dir, out_dir=args.out_dir)
    print(f"kept {report['n_kept']} / {report['n_input']} atoms "
          f"({report['n_rejected']} rejected)")
    print("kept by paradigm_type:")
    for k, n in sorted(report["by_paradigm_type_kept"].items(), key=lambda x: -x[1]):
        print(f"  {k:18s} {n}")
    print("kept by transcript:")
    for k, n in sorted(report["by_transcript_kept"].items()):
        print(f"  {k:10s} {n}")
    print("kept by reason:")
    for k, n in sorted(report["kept_by_reason"].items(), key=lambda x: -x[1]):
        print(f"  {k:50s} {n}")


if __name__ == "__main__":
    main()

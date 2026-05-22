"""Cross-atom analogy engine for Paradigm-Shift Finder v1.

Combines paradigm-shift atoms via 4 typed combinators:
  - PREDICTION_GROUNDED_IN_PRINCIPLE  (prediction + first_principle)
  - ANALOGY_TRANSFERS_TO_OPEN         (analogy    + open_problem)
  - BLOCKER_DISSOLVED_BY_PRINCIPLE    (blocker    + first_principle)
  - PREDICTION_RESOLVES_BLOCKER       (prediction + blocker)

Every candidate must:
  - cite >= 2 atoms from distinct snippets
  - include a 1-line first_principles_validity_hypothesis field
  - inherit transcript_diversity from its source atoms

The first_principles_validity_hypothesis is asserted by the model
(here: deterministically derived from the atoms) — it is NOT validated
at this layer. Layer 5 (first_principles_stress) is where the
hypothesis is RAG-stress-tested. Validating at this layer would be
circular: Claude grading its own claim before the RAG check.

Honest deviation: the deterministic combinator produces template-heavy
claim text. The user/agent can override with a free-form combinator
in v2; v1 ships deterministic to keep the audit chain mechanical.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple


VALID_TYPED_COMBINATORS = {
    "PREDICTION_GROUNDED_IN_PRINCIPLE": ("prediction", "first_principle"),
    "ANALOGY_TRANSFERS_TO_OPEN":        ("analogy", "open_problem"),
    "BLOCKER_DISSOLVED_BY_PRINCIPLE":   ("blocker", "first_principle"),
    "PREDICTION_RESOLVES_BLOCKER":      ("prediction", "blocker"),
}


@dataclass
class ParadigmCandidate:
    candidate_id: str
    combined_atom_ids: List[str]
    combination_operator: str
    claim: str
    first_principles_validity_hypothesis: str
    why_novel_vs_speaker: str
    why_potentially_useful: str
    source_snippets: List[str]
    source_transcripts: List[str]
    transcript_diversity: int
    paradigm_type_pair: Tuple[str, str]
    target_date: Optional[str]
    timestamp: str = ""


def load_atoms(atoms_dir: Path) -> List[dict]:
    """Load all paradigm-shift atom JSONs from atoms_dir."""
    out = []
    for ap in sorted(atoms_dir.glob("ATOM_*.json")):
        with ap.open("r", encoding="utf-8") as f:
            out.append(json.load(f))
    return out


def short_quote(text: str, n: int = 80) -> str:
    s = text.replace("\n", " ").strip()
    return s if len(s) <= n else s[:n - 3] + "..."


def make_prediction_grounded_in_principle(pred: dict, principle: dict) -> ParadigmCandidate:
    """Prediction A holds IF first-principle B is binding."""
    claim = (
        f"Prediction in atom {pred['atom_id']} (\"{short_quote(pred['verbatim_quote'])}\") "
        f"holds if and only if the first-principle constraint in atom {principle['atom_id']} "
        f"(\"{short_quote(principle['verbatim_quote'])}\") is binding."
    )
    hyp = (
        f"The prediction \"{short_quote(pred['verbatim_quote'], 60)}\" is forced "
        f"by the underlying constraint \"{short_quote(principle['verbatim_quote'], 60)}\"; "
        f"if the constraint is not binding the prediction may still hold by accident "
        f"but the binding case is the load-bearing version of this candidate."
    )
    why_novel = (
        f"The speaker introduces the prediction (snippet {pred['snippet_id']}) and the "
        f"first-principle (snippet {principle['snippet_id']}) in separate contexts; "
        f"the speaker does not state that the second forces the first."
    )
    why_useful = (
        "A prediction that is forced by a first-principle is more falsifiable than a "
        "free-floating prediction: if the principle holds and the prediction fails, "
        "one of them is wrong, which is a binary research question."
    )
    return _build_candidate(
        pred, principle,
        operator="PREDICTION_GROUNDED_IN_PRINCIPLE",
        claim=claim, hyp=hyp, why_novel=why_novel, why_useful=why_useful,
    )


def make_analogy_transfers_to_open(analogy: dict, open_p: dict) -> ParadigmCandidate:
    """Apply analogy A's structure to unresolved problem B."""
    claim = (
        f"Apply the analogical structure in atom {analogy['atom_id']} "
        f"(\"{short_quote(analogy['verbatim_quote'])}\") to the open problem framed in "
        f"atom {open_p['atom_id']} (\"{short_quote(open_p['verbatim_quote'])}\")."
    )
    hyp = (
        "The structural correspondence in the analogy preserves the open problem's "
        "constraint pattern; the analogy is not merely a surface metaphor."
    )
    why_novel = (
        f"The speaker uses the analogy in snippet {analogy['snippet_id']} for one purpose "
        f"and raises the open problem in snippet {open_p['snippet_id']} without connecting them."
    )
    why_useful = (
        "Open problems gain a candidate solution shape from the analogy's source domain; "
        "the source domain's known constraints become hypotheses for the target."
    )
    return _build_candidate(
        analogy, open_p,
        operator="ANALOGY_TRANSFERS_TO_OPEN",
        claim=claim, hyp=hyp, why_novel=why_novel, why_useful=why_useful,
    )


def make_blocker_dissolved_by_principle(blocker: dict, principle: dict) -> ParadigmCandidate:
    """Blocker A is dissolved if we recognize principle B."""
    claim = (
        f"The blocker in atom {blocker['atom_id']} (\"{short_quote(blocker['verbatim_quote'])}\") "
        f"is dissolved by recognizing the first-principle in atom {principle['atom_id']} "
        f"(\"{short_quote(principle['verbatim_quote'])}\")."
    )
    hyp = (
        "The named blocker is an artifact of a frame that the first-principle invalidates; "
        "under the principle, the blocker either does not bind or is mis-stated."
    )
    why_novel = (
        f"The speaker introduces the blocker (snippet {blocker['snippet_id']}) without "
        f"invoking the dissolving principle (snippet {principle['snippet_id']}); "
        f"the connection is asserted by the analogy engine."
    )
    why_useful = (
        "A dissolved blocker often points to a previously-overlooked wedge: if the "
        "blocker was real, anyone who notices the dissolution gets a head start."
    )
    return _build_candidate(
        blocker, principle,
        operator="BLOCKER_DISSOLVED_BY_PRINCIPLE",
        claim=claim, hyp=hyp, why_novel=why_novel, why_useful=why_useful,
    )


def make_prediction_resolves_blocker(pred: dict, blocker: dict) -> ParadigmCandidate:
    """Prediction A is the resolution of blocker B."""
    claim = (
        f"The prediction in atom {pred['atom_id']} (\"{short_quote(pred['verbatim_quote'])}\") "
        f"is the resolution of the blocker in atom {blocker['atom_id']} "
        f"(\"{short_quote(blocker['verbatim_quote'])}\")."
    )
    hyp = (
        "The predicted future state contains a mechanism that removes the named blocker; "
        "the prediction is therefore a market signal for the resolution mechanism."
    )
    why_novel = (
        f"The speaker frames the prediction (snippet {pred['snippet_id']}) and the blocker "
        f"(snippet {blocker['snippet_id']}) as independent statements; the resolution "
        f"link is asserted by the analogy engine."
    )
    why_useful = (
        "Predictions that resolve known blockers are higher-value than predictions "
        "that simply extrapolate trends — they imply an unaddressed market need."
    )
    return _build_candidate(
        pred, blocker,
        operator="PREDICTION_RESOLVES_BLOCKER",
        claim=claim, hyp=hyp, why_novel=why_novel, why_useful=why_useful,
    )


def _build_candidate(a: dict, b: dict, operator: str, claim: str, hyp: str,
                     why_novel: str, why_useful: str) -> ParadigmCandidate:
    transcripts = sorted({a["transcript_id"], b["transcript_id"]})
    snippets = sorted({a["snippet_id"], b["snippet_id"]})
    target_date = a.get("target_date") or b.get("target_date") or a.get("source_date") or b.get("source_date")
    return ParadigmCandidate(
        candidate_id="",
        combined_atom_ids=[a["atom_id"], b["atom_id"]],
        combination_operator=operator,
        claim=claim,
        first_principles_validity_hypothesis=hyp,
        why_novel_vs_speaker=why_novel,
        why_potentially_useful=why_useful,
        source_snippets=snippets,
        source_transcripts=transcripts,
        transcript_diversity=len(transcripts),
        paradigm_type_pair=(a["paradigm_type"], b["paradigm_type"]),
        target_date=target_date,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def brainstorm_paradigm_candidates(
    atoms_dir: Path,
    out_dir: Path,
    run_id: str = "run_001",
    max_per_operator: int = 5,
    require_cross_transcript: bool = True,
    seed: int = 1,
) -> List[ParadigmCandidate]:
    """Run the full typed-combinator brainstorm over the atoms in atoms_dir.

    Returns list of ParadigmCandidate. Writes one JSON per candidate to out_dir.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    atoms = load_atoms(atoms_dir)

    by_type = {}
    for a in atoms:
        by_type.setdefault(a["paradigm_type"], []).append(a)

    rng = random.Random(seed)
    candidates: List[ParadigmCandidate] = []
    counter = 0

    operator_fn = {
        "PREDICTION_GROUNDED_IN_PRINCIPLE": (make_prediction_grounded_in_principle,
                                              "prediction", "first_principle"),
        "ANALOGY_TRANSFERS_TO_OPEN":        (make_analogy_transfers_to_open,
                                              "analogy", "open_problem"),
        "BLOCKER_DISSOLVED_BY_PRINCIPLE":   (make_blocker_dissolved_by_principle,
                                              "blocker", "first_principle"),
        "PREDICTION_RESOLVES_BLOCKER":      (make_prediction_resolves_blocker,
                                              "prediction", "blocker"),
    }

    for op_name, (fn, type_a, type_b) in operator_fn.items():
        pool_a = by_type.get(type_a, [])
        pool_b = by_type.get(type_b, [])
        if not pool_a or not pool_b:
            continue

        pairs: List[Tuple[dict, dict]] = []
        for a, b in itertools.product(pool_a, pool_b):
            if a["snippet_id"] == b["snippet_id"]:
                continue
            if require_cross_transcript and a["transcript_id"] == b["transcript_id"]:
                continue
            pairs.append((a, b))

        rng.shuffle(pairs)
        chosen = pairs[:max_per_operator]
        for a, b in chosen:
            counter += 1
            cand = fn(a, b)
            cand.candidate_id = f"CAND_{run_id}_{counter:03d}"
            candidates.append(cand)

    for cand in candidates:
        with (out_dir / f"{cand.candidate_id}.json").open("w", encoding="utf-8") as f:
            d = asdict(cand)
            d["paradigm_type_pair"] = list(d["paradigm_type_pair"])
            json.dump(d, f, indent=2, ensure_ascii=False)

    # _index.json
    by_op = {}
    by_pair = {}
    diversity_dist = {}
    for c in candidates:
        by_op[c.combination_operator] = by_op.get(c.combination_operator, 0) + 1
        pair_key = "+".join(c.paradigm_type_pair)
        by_pair[pair_key] = by_pair.get(pair_key, 0) + 1
        diversity_dist[c.transcript_diversity] = diversity_dist.get(c.transcript_diversity, 0) + 1
    index = {
        "n_candidates": len(candidates),
        "candidate_ids": [c.candidate_id for c in candidates],
        "operator_distribution": by_op,
        "type_pair_distribution": by_pair,
        "diversity_distribution": {str(k): v for k, v in diversity_dist.items()},
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "require_cross_transcript": require_cross_transcript,
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    return candidates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atoms_dir", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--run_id", default="run_001")
    ap.add_argument("--max_per_operator", type=int, default=5)
    ap.add_argument("--allow_intra_transcript", action="store_true",
                    help="Disable the cross-transcript requirement.")
    args = ap.parse_args()
    cands = brainstorm_paradigm_candidates(
        args.atoms_dir, args.out_dir,
        run_id=args.run_id,
        max_per_operator=args.max_per_operator,
        require_cross_transcript=not args.allow_intra_transcript,
    )
    print(f"brainstormed {len(cands)} paradigm candidates")
    by_op = {}
    for c in cands:
        by_op[c.combination_operator] = by_op.get(c.combination_operator, 0) + 1
    for op, n in sorted(by_op.items(), key=lambda x: -x[1]):
        print(f"  {op:40s} {n}")


if __name__ == "__main__":
    main()

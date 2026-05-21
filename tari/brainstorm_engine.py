"""Brainstorm engine for TARI v1.

Cross-atom combination. For each candidate, records which atom IDs drove it
and which combination operator was applied. The brainstorm step is intentionally
constrained: only 6 named operators are allowed, and every candidate must list
>= 2 atoms from distinct snippets.

This step in v1 uses a deterministic heuristic combinator rather than a free-form
LLM call. The reason: free-form LLM combination is the most likely source of
fabricated traceability (Claude implicitly invoking facts not in either atom).
v1 ships with a deterministic combinator; v2 can replace it with an LLM
combinator gated by the audit step.

Combinators:
  ANALOGIZE   — atom_A's mechanism applied to atom_B's domain
  INVERT      — atom_A's claim with one of its assumptions negated
  COMPOSE     — atom_A and atom_B applied sequentially
  GENERALIZE  — atom_A's specific claim lifted to a wider domain
  RESTRICT    — atom_A's general claim restricted to atom_B's domain
  CONTRAST    — atom_A and atom_B as opposing approaches

This step produces structured candidate JSONs only. Whether a candidate is
defensible is determined downstream by self_model_audit and external_verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class Candidate:
    candidate_id: str
    combined_atom_ids: List[str]
    combination_operator: str
    claim: str
    why_novel_vs_speaker: str
    why_potentially_useful: str
    source_snippets: List[str] = field(default_factory=list)
    timestamp: str = ""


def load_atoms(atoms_dir: Path) -> List[dict]:
    atom_files = sorted(atoms_dir.glob("ATOM_*.json"))
    atoms = []
    for ap in atom_files:
        with ap.open("r", encoding="utf-8") as f:
            atoms.append(json.load(f))
    return atoms


def short_quote(text: str, n: int = 80) -> str:
    s = text.replace("\n", " ").strip()
    return s if len(s) <= n else s[:n - 3] + "..."


def make_analogize_claim(a: dict, b: dict) -> Optional[Candidate]:
    """ANALOGIZE: A's mechanism applied to B's domain."""
    if a["atom_type"] != "PRIMITIVE":
        return None
    if b["atom_type"] not in ("MECHANISM_CLAIM", "OPEN_QUESTION"):
        return None
    if a["snippet_id"] == b["snippet_id"]:
        return None
    claim = (
        f"Apply the mechanism described in atom {a['atom_id']} "
        f"(\"{short_quote(a['verbatim_quote'])}\") to the problem framed in atom "
        f"{b['atom_id']} (\"{short_quote(b['verbatim_quote'])}\")."
    )
    why_novel = (
        f"The speaker introduces atom {a['atom_id']} in the context of one section "
        f"(snippet {a['snippet_id']}) and atom {b['atom_id']} in a different section "
        f"(snippet {b['snippet_id']}). The speaker does not, within either snippet, "
        f"propose connecting them in this direction."
    )
    why_useful = (
        f"If {a['atom_type'].lower()} from {a['snippet_id']} captures a primitive "
        f"that the {b['atom_id']} problem framing lacks, this combination is a "
        f"candidate primitive transfer."
    )
    return Candidate(
        candidate_id="",
        combined_atom_ids=[a["atom_id"], b["atom_id"]],
        combination_operator="ANALOGIZE",
        claim=claim,
        why_novel_vs_speaker=why_novel,
        why_potentially_useful=why_useful,
        source_snippets=[a["snippet_id"], b["snippet_id"]],
    )


def make_invert_claim(a: dict) -> Optional[Candidate]:
    """INVERT: A's claim with one assumption negated."""
    if a["atom_type"] not in ("MECHANISM_CLAIM", "PRIMITIVE"):
        return None
    claim = (
        f"Negate the directional assumption of atom {a['atom_id']} "
        f"(\"{short_quote(a['verbatim_quote'])}\"): study the case where the relation "
        f"is reversed (output drives the input rather than input drives the output)."
    )
    why_novel = (
        f"The speaker states the claim in one direction in snippet {a['snippet_id']}. "
        f"The reversed-direction case is not addressed in the same snippet."
    )
    why_useful = (
        "Inversion surfaces an assumption that was implicit in the original claim and "
        "lets us test whether the mechanism is bidirectional or directional."
    )
    return Candidate(
        candidate_id="",
        combined_atom_ids=[a["atom_id"]],
        combination_operator="INVERT",
        claim=claim,
        why_novel_vs_speaker=why_novel,
        why_potentially_useful=why_useful,
        source_snippets=[a["snippet_id"]],
    )


def make_compose_claim(a: dict, b: dict) -> Optional[Candidate]:
    """COMPOSE: A and B applied sequentially."""
    if a["atom_type"] != "PRIMITIVE" or b["atom_type"] != "PRIMITIVE":
        return None
    if a["snippet_id"] == b["snippet_id"]:
        return None
    claim = (
        f"Compose the primitive in atom {a['atom_id']} with the primitive in atom "
        f"{b['atom_id']}: apply the first to produce an intermediate representation, "
        f"then apply the second to that representation."
    )
    why_novel = (
        f"The speaker introduces both primitives but in distinct snippets "
        f"({a['snippet_id']} and {b['snippet_id']}); the composition is not stated."
    )
    why_useful = (
        "Sequential composition is a standard way of obtaining a new capability from two "
        "primitives, but composing distinct primitives from distinct sections requires "
        "the composition's interface to be checked."
    )
    return Candidate(
        candidate_id="",
        combined_atom_ids=[a["atom_id"], b["atom_id"]],
        combination_operator="COMPOSE",
        claim=claim,
        why_novel_vs_speaker=why_novel,
        why_potentially_useful=why_useful,
        source_snippets=[a["snippet_id"], b["snippet_id"]],
    )


def make_generalize_claim(a: dict, b: dict) -> Optional[Candidate]:
    """GENERALIZE: A's specific claim lifted via B's wider framing."""
    if a["atom_type"] != "MECHANISM_CLAIM":
        return None
    if b["atom_type"] not in ("PRIMITIVE", "OPEN_QUESTION"):
        return None
    if a["snippet_id"] == b["snippet_id"]:
        return None
    claim = (
        f"Generalize the specific claim in atom {a['atom_id']} "
        f"(\"{short_quote(a['verbatim_quote'])}\") to the broader category implied "
        f"by atom {b['atom_id']}: state the claim as a class-level property of the "
        f"category, not just the specific case."
    )
    why_novel = (
        f"The speaker states the claim at one level of specificity in {a['snippet_id']}. "
        f"Lifting to {b['snippet_id']}'s framing is a generalization the speaker did not state."
    )
    why_useful = (
        "Class-level generalization is a candidate research direction if the specific "
        "claim is shown to extend; if it doesn't extend, the boundary itself is a finding."
    )
    return Candidate(
        candidate_id="",
        combined_atom_ids=[a["atom_id"], b["atom_id"]],
        combination_operator="GENERALIZE",
        claim=claim,
        why_novel_vs_speaker=why_novel,
        why_potentially_useful=why_useful,
        source_snippets=[a["snippet_id"], b["snippet_id"]],
    )


def make_restrict_claim(a: dict, b: dict) -> Optional[Candidate]:
    """RESTRICT: A's general claim restricted to B's specific case."""
    if a["atom_type"] not in ("MECHANISM_CLAIM", "PRIMITIVE"):
        return None
    if b["atom_type"] not in ("NEGATIVE_RESULT", "METRIC"):
        return None
    if a["snippet_id"] == b["snippet_id"]:
        return None
    claim = (
        f"Restrict the general claim of atom {a['atom_id']} to the specific scenario "
        f"described in atom {b['atom_id']} (\"{short_quote(b['verbatim_quote'])}\"). "
        f"Does the general claim still hold under this restriction?"
    )
    why_novel = (
        f"The general claim in {a['snippet_id']} is stated; the restriction to "
        f"{b['snippet_id']}'s scenario is a test case the speaker did not run."
    )
    why_useful = (
        "Restriction tests the robustness of a general claim against a known boundary "
        "case; if the claim breaks at the restriction, we have located its limits."
    )
    return Candidate(
        candidate_id="",
        combined_atom_ids=[a["atom_id"], b["atom_id"]],
        combination_operator="RESTRICT",
        claim=claim,
        why_novel_vs_speaker=why_novel,
        why_potentially_useful=why_useful,
        source_snippets=[a["snippet_id"], b["snippet_id"]],
    )


def make_contrast_claim(a: dict, b: dict) -> Optional[Candidate]:
    """CONTRAST: A and B as opposing approaches."""
    if a["atom_type"] != "PRIMITIVE" or b["atom_type"] != "PRIMITIVE":
        return None
    if a["snippet_id"] == b["snippet_id"]:
        return None
    claim = (
        f"Contrast the primitive in atom {a['atom_id']} with the primitive in atom "
        f"{b['atom_id']}: identify the structural axis on which they differ and "
        f"the cases where one would dominate the other."
    )
    why_novel = (
        f"The speaker introduces both primitives but does not explicitly contrast them "
        f"at the level of structural axis."
    )
    why_useful = (
        "Explicit contrast surfaces the operating regime of each primitive; this is a "
        "diagnostic claim about when each is preferable."
    )
    return Candidate(
        candidate_id="",
        combined_atom_ids=[a["atom_id"], b["atom_id"]],
        combination_operator="CONTRAST",
        claim=claim,
        why_novel_vs_speaker=why_novel,
        why_potentially_useful=why_useful,
        source_snippets=[a["snippet_id"], b["snippet_id"]],
    )


def brainstorm(atoms_dir: Path, out_dir: Path, run_id: str, max_candidates: int = 15) -> List[Candidate]:
    atoms = load_atoms(atoms_dir)
    # Deterministic seed: Python's built-in hash() is randomized across processes,
    # which broke reproducibility in the pilot run. Use sha256 of run_id instead.
    seed_int = int(hashlib.sha256(run_id.encode("utf-8")).hexdigest()[:12], 16)
    rng = random.Random(seed_int)

    # Index by type
    by_type = {}
    for a in atoms:
        by_type.setdefault(a["atom_type"], []).append(a)

    candidates: List[Candidate] = []

    # Generate combinations across the 6 operators.
    primitives = by_type.get("PRIMITIVE", [])
    mech_claims = by_type.get("MECHANISM_CLAIM", [])
    neg_results = by_type.get("NEGATIVE_RESULT", [])
    open_questions = by_type.get("OPEN_QUESTION", [])
    metrics = by_type.get("METRIC", [])

    # ANALOGIZE — sample PRIMITIVE × (MECHANISM_CLAIM ∪ OPEN_QUESTION)
    for a, b in itertools.islice(
            ((a, b) for a in primitives for b in mech_claims + open_questions
             if a["snippet_id"] != b["snippet_id"]),
            0, 80):
        c = make_analogize_claim(a, b)
        if c:
            candidates.append(c)

    # INVERT — sample MECHANISM_CLAIM ∪ PRIMITIVE
    for a in (mech_claims + primitives)[:40]:
        c = make_invert_claim(a)
        if c:
            candidates.append(c)

    # COMPOSE — pairs of primitives from distinct snippets
    for a, b in itertools.islice(
            ((a, b) for i, a in enumerate(primitives) for b in primitives[i + 1:]
             if a["snippet_id"] != b["snippet_id"]),
            0, 40):
        c = make_compose_claim(a, b)
        if c:
            candidates.append(c)

    # GENERALIZE — MECHANISM_CLAIM × (PRIMITIVE ∪ OPEN_QUESTION)
    for a, b in itertools.islice(
            ((a, b) for a in mech_claims for b in primitives + open_questions
             if a["snippet_id"] != b["snippet_id"]),
            0, 40):
        c = make_generalize_claim(a, b)
        if c:
            candidates.append(c)

    # RESTRICT — MECHANISM_CLAIM × (NEGATIVE_RESULT ∪ METRIC)
    for a, b in itertools.islice(
            ((a, b) for a in (mech_claims + primitives) for b in (neg_results + metrics)
             if a["snippet_id"] != b["snippet_id"]),
            0, 40):
        c = make_restrict_claim(a, b)
        if c:
            candidates.append(c)

    # CONTRAST — pairs of primitives
    for a, b in itertools.islice(
            ((a, b) for i, a in enumerate(primitives) for b in primitives[i + 1:]
             if a["snippet_id"] != b["snippet_id"]),
            0, 40):
        c = make_contrast_claim(a, b)
        if c:
            candidates.append(c)

    # Shuffle and cap
    rng.shuffle(candidates)
    # Take a diverse sample: cap each operator to max(1, max_candidates // 6)
    per_op = max(1, max_candidates // 6)
    by_op = {}
    selected: List[Candidate] = []
    for c in candidates:
        bucket = by_op.setdefault(c.combination_operator, [])
        if len(bucket) < per_op:
            bucket.append(c)
            selected.append(c)
        if len(selected) >= max_candidates:
            break

    # Assign canonical IDs
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, c in enumerate(selected, 1):
        c.candidate_id = f"CAND_{run_id}_{i:03d}"
        c.timestamp = datetime.now(timezone.utc).isoformat()
        with (out_dir / f"{c.candidate_id}.json").open("w", encoding="utf-8") as f:
            json.dump(asdict(c), f, indent=2, ensure_ascii=False)

    index = {
        "n_candidates": len(selected),
        "candidate_ids": [c.candidate_id for c in selected],
        "operator_distribution": {op: sum(1 for c in selected if c.combination_operator == op)
                                  for op in ["ANALOGIZE", "INVERT", "COMPOSE", "GENERALIZE", "RESTRICT", "CONTRAST"]},
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    return selected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atoms_dir", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--run_id", required=True, type=str)
    ap.add_argument("--max_candidates", type=int, default=15)
    args = ap.parse_args()
    cands = brainstorm(args.atoms_dir, args.out_dir, args.run_id, args.max_candidates)
    print(f"generated {len(cands)} candidates")
    for c in cands[:5]:
        print(f"  {c.candidate_id}  {c.combination_operator}  atoms={c.combined_atom_ids}")


if __name__ == "__main__":
    main()

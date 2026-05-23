"""Atom quality filter for Paradigm-Shift Finder Run 7.

Run 6's purifier ran on YouTube auto-captions and produced atoms whose
verbatim quotes are conversational fillers, illustrative metaphors, or
sentence fragments. Examples observed in `phase5_survivors.json`:

  - "So there's like a limit to the area under the curve of what you
     can build and."                       (illustrative analogy)
  - "Now the leap from coding unsolved math, we needed something more."
                                            (sentence fragment)
  - "So, he can read a he can read like a phone book..."
                                            (talk-language: stammer + simile)
  - "Well, I think the way I think of these is I think they're two
     very basic prim..."                    (conversational filler)

These atoms pass the regex type tagger but contain no technical claim
or specific architectural mechanism. Combining them into candidates
produces template-shaped nonsense even after the arXiv gate.

This module gates atoms BEFORE they reach the analogy engine:

  1. **Conversational filler.** Reject if the quote is dominated by
     hedge / discourse markers ("I think", "you know", "I would say",
     stammered repetitions, etc.).

  2. **Illustrative analogy without target.** Reject ANALOGY atoms that
     name a vehicle (phone book, area under curve, conservation of X)
     but do not also name the target the analogy is supposed to
     illuminate.

  3. **Sentence fragment.** Reject quotes that don't contain a finite
     verb + object after the discourse marker is stripped.

  4. **Lack of technical content.** Require at least one
     domain-specific noun (ml_research / consciousness_brain /
     hardware_compute / startup_business / math_formal vocabulary)
     OR a quantitative claim (number + unit). Pure speculation about
     "things" is rejected.

Output: filtered atoms directory + `_quality_report.json` with per-atom
verdicts.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Re-use the domain vocabulary from the coherence checker.
from semantic_coherence_check import DOMAIN_KEYWORDS


# ---- Filler / discourse markers ----

FILLER_PATTERNS = [
    re.compile(r"\bi\s+(?:think|guess|feel|believe|mean|suppose)\b", re.IGNORECASE),
    re.compile(r"\bi\s+would\s+(?:say|argue|think)\b", re.IGNORECASE),
    re.compile(r"\byou\s+know\b", re.IGNORECASE),
    re.compile(r"\bsort\s+of\b", re.IGNORECASE),
    re.compile(r"\bkind\s+of\b", re.IGNORECASE),
    re.compile(r"\blike\s+(?:i|we|you|they)\b", re.IGNORECASE),
    re.compile(r"\b(?:basically|literally|honestly|actually)\b", re.IGNORECASE),
    re.compile(r"\bthe\s+way\s+i\s+(?:think|see|look)\b", re.IGNORECASE),
]


def filler_density(text: str) -> float:
    """Return fraction of tokens covered by filler patterns."""
    n_tokens = max(1, len(re.findall(r"\w+", text)))
    n_filler = 0
    for pat in FILLER_PATTERNS:
        for m in pat.finditer(text):
            n_filler += len(re.findall(r"\w+", m.group(0)))
    return n_filler / n_tokens


# Stammer detection: "I I I", "the the", "he can read a he can read"
STAMMER_RE = re.compile(r"\b(\w+)(?:\s+\1){1,}\b", re.IGNORECASE)
PHRASE_REPEAT_RE = re.compile(r"\b(\w+\s+\w+\s+\w+)\b.*?\b\1\b", re.IGNORECASE)


def has_stammer(text: str) -> bool:
    if STAMMER_RE.search(text):
        return True
    # Detect repeated 3-grams within a short window (the "he can read a he can
    # read" pattern). Limit window to first 200 chars to avoid quadratic blowup.
    return bool(PHRASE_REPEAT_RE.search(text[:200]))


# ---- Illustrative-analogy detection ----
#
# Reject analogies whose vehicle is a hyper-specific mundane object
# (phone book, library, kitchen, recipe, area under a curve, law of
# conservation of <abstract noun>) AND that do not name a technical
# target. The vehicle list is closed and small on purpose; we want
# precision, not recall.

ILLUSTRATIVE_VEHICLES = [
    re.compile(r"\barea\s+under\s+(?:the\s+)?curve\b", re.IGNORECASE),
    re.compile(r"\bphone\s+book\b", re.IGNORECASE),
    re.compile(r"\bconservation\s+of\s+(?:happiness|love|joy|fun)\b", re.IGNORECASE),
    re.compile(r"\blaw\s+of\s+conversation\b", re.IGNORECASE),  # observed mis-purify
    re.compile(r"\bpink\s+qualia\b", re.IGNORECASE),
    re.compile(r"\bstraw\s+man\b", re.IGNORECASE),
    re.compile(r"\b(?:like|just\s+like)\s+(?:a\s+|an\s+)?(?:utility|fab|operating\s+system)s?\b", re.IGNORECASE),
    re.compile(r"\b4\s*nanometer\s+process\s+node\b", re.IGNORECASE),
    re.compile(r"\bworth\s+stealing\b", re.IGNORECASE),
    re.compile(r"\bhandwritten\s+digits?\b", re.IGNORECASE),
]


def matched_illustrative_vehicle(text: str) -> Optional[str]:
    for pat in ILLUSTRATIVE_VEHICLES:
        m = pat.search(text)
        if m:
            return m.group(0).lower()
    return None


# ---- Fragment detection ----
#
# A quote that ends in a fragment (no finite verb, trails off into "...",
# or starts mid-clause after a discourse marker) is a fragment.

FRAGMENT_TRAILING_RE = re.compile(r"(?:\.\.\.|—|–)\s*$")
NO_VERB_HINT_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|has|have|had|do|does|did|"
    r"can|could|will|would|should|may|might|must|"
    r"build|builds|built|need|needs|needed|make|makes|made|"
    r"think|thinks|thought|know|knows|knew|see|sees|saw|"
    r"use|uses|used|work|works|worked|run|runs|ran|"
    r"go|goes|going|come|comes|coming|get|gets|got|"
    r"take|takes|took|give|gives|gave|change|changes|changed|"
    r"resolve|resolves|resolved|require|requires|required|"
    r"depend|depends|depended|imply|implies|implied|"
    r"force|forces|forced|prevent|prevents|prevented|"
    r"limit|limits|limited|enable|enables|enabled|"
    r"want|wants|wanted|allow|allows|allowed|"
    r"happen|happens|happened|appear|appears|appeared|"
    r"create|creates|created|generate|generates|generated|"
    r"emerge|emerges|emerged|exist|exists|existed)\b",
    re.IGNORECASE,
)


def is_fragment(text: str) -> bool:
    # Trailing ellipsis / em-dash → fragment
    if FRAGMENT_TRAILING_RE.search(text):
        return True
    # Strip leading discourse markers, then look for a finite verb.
    stripped = re.sub(
        r"^\s*(?:so|but|and|now|well|okay|yeah|right|like)\s*[,]?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    if len(stripped.split()) < 6:
        return True
    if not NO_VERB_HINT_RE.search(stripped):
        return True
    return False


# ---- Technical-content check ----

QUANT_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*"
    r"(?:%|x|kb|mb|gb|tb|pb|gflop|tflop|nm|ms|s|sec|hz|khz|ghz|"
    r"years?|months?|days?|weeks?|decades?|hours?|minutes?|"
    r"million|billion|thousand|trillion|"
    r"watts?|joules?|tokens?|parameters?|samples?|epochs?)\b",
    re.IGNORECASE,
)


def has_technical_content(text: str) -> bool:
    # Numeric claim with unit
    if QUANT_RE.search(text):
        return True
    # Domain-vocabulary hit
    words = set(re.findall(r"[a-z][a-z\-]+", text.lower()))
    for kws in DOMAIN_KEYWORDS.values():
        if len(words & kws) >= 1:
            return True
    return False


# ---- Verdict ----

@dataclass
class AtomVerdict:
    atom_id: str
    paradigm_type: str
    verdict: str           # "KEEP" | "REJECT_<reason>"
    reason: str
    quote_preview: str


def assess_atom(atom: dict) -> AtomVerdict:
    quote = atom.get("verbatim_quote", "")
    preview = quote[:120] + ("..." if len(quote) > 120 else "")

    if is_fragment(quote):
        return AtomVerdict(
            atom_id=atom["atom_id"],
            paradigm_type=atom["paradigm_type"],
            verdict="REJECT_FRAGMENT",
            reason="missing finite verb / trailing ellipsis / too short after discourse markers",
            quote_preview=preview,
        )
    if has_stammer(quote):
        return AtomVerdict(
            atom_id=atom["atom_id"],
            paradigm_type=atom["paradigm_type"],
            verdict="REJECT_TALK_STAMMER",
            reason="repeated tokens or repeated short phrase (transcription stammer)",
            quote_preview=preview,
        )
    density = filler_density(quote)
    if density >= 0.20:
        return AtomVerdict(
            atom_id=atom["atom_id"],
            paradigm_type=atom["paradigm_type"],
            verdict="REJECT_TALK_FILLER",
            reason=f"filler density {density:.2f} ≥ 0.20 (I think / you know / sort of / etc.)",
            quote_preview=preview,
        )
    vehicle = matched_illustrative_vehicle(quote)
    if vehicle and not has_technical_content(quote):
        return AtomVerdict(
            atom_id=atom["atom_id"],
            paradigm_type=atom["paradigm_type"],
            verdict="REJECT_ILLUSTRATIVE_ANALOGY",
            reason=f"matched illustrative vehicle '{vehicle}' with no technical target term",
            quote_preview=preview,
        )
    if atom.get("paradigm_type") == "analogy" and vehicle:
        return AtomVerdict(
            atom_id=atom["atom_id"],
            paradigm_type=atom["paradigm_type"],
            verdict="REJECT_ILLUSTRATIVE_ANALOGY",
            reason=f"analogy whose vehicle '{vehicle}' is a closed-list mundane object",
            quote_preview=preview,
        )
    if not has_technical_content(quote):
        return AtomVerdict(
            atom_id=atom["atom_id"],
            paradigm_type=atom["paradigm_type"],
            verdict="REJECT_NO_TECHNICAL_CONTENT",
            reason="no domain-vocabulary noun and no quantitative claim",
            quote_preview=preview,
        )
    return AtomVerdict(
        atom_id=atom["atom_id"],
        paradigm_type=atom["paradigm_type"],
        verdict="KEEP",
        reason="passes fragment / stammer / filler / vehicle / technical-content checks",
        quote_preview=preview,
    )


def filter_atoms_dir(
    atoms_dir: Path,
    out_dir: Path,
    report_path: Path,
) -> Tuple[List[AtomVerdict], Dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    verdicts: List[AtomVerdict] = []
    kept = 0
    for ap in sorted(atoms_dir.glob("ATOM_*.json")):
        with ap.open("r", encoding="utf-8") as f:
            atom = json.load(f)
        v = assess_atom(atom)
        verdicts.append(v)
        if v.verdict == "KEEP":
            kept += 1
            with (out_dir / ap.name).open("w", encoding="utf-8") as f:
                json.dump(atom, f, indent=2, ensure_ascii=False)

    # Build _index.json for the filtered output
    counts_by_type: Counter = Counter()
    counts_by_transcript: Counter = Counter()
    kept_ids: List[str] = []
    for fp in sorted(out_dir.glob("ATOM_*.json")):
        with fp.open("r", encoding="utf-8") as f:
            d = json.load(f)
        kept_ids.append(d["atom_id"])
        counts_by_type[d["paradigm_type"]] += 1
        counts_by_transcript[d.get("transcript_id", "T001")] += 1
    index = {
        "n_atoms": len(kept_ids),
        "atom_ids": kept_ids,
        "paradigm_type_distribution": dict(counts_by_type),
        "transcript_distribution": dict(counts_by_transcript),
        "filtered_from": str(atoms_dir),
        "filtered_at": datetime.now(timezone.utc).isoformat(),
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    by_verdict: Counter = Counter()
    for v in verdicts:
        by_verdict[v.verdict] += 1
    report = {
        "n_input": len(verdicts),
        "n_kept": kept,
        "n_rejected": len(verdicts) - kept,
        "verdict_distribution": dict(by_verdict),
        "per_atom": [asdict(v) for v in verdicts],
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return verdicts, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atoms_dir", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--report_path", required=True, type=Path)
    args = ap.parse_args()
    verdicts, report = filter_atoms_dir(args.atoms_dir, args.out_dir, args.report_path)
    print(f"atoms input: {report['n_input']}  kept: {report['n_kept']}  rejected: {report['n_rejected']}")
    for k, n in sorted(report["verdict_distribution"].items(), key=lambda x: -x[1]):
        print(f"  {k:36s} {n}")


if __name__ == "__main__":
    main()

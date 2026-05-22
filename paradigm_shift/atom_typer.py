"""Atom typer for Paradigm-Shift Finder v1.

Extends TARI's atom extractor with 6 paradigm-shift type tags:
  - prediction       (claim about future state of field/world)
  - blocker          (named obstacle preventing some prediction)
  - first_principle  (foundational constraint the speaker invokes)
  - analogy          (cross-field comparison the speaker makes)
  - open_problem     (unsolved thing the speaker flags)
  - trend            (multi-year trajectory the speaker tracks)

Atoms inherit TARI's verbatim_quote/snippet_id/line_span contract. Each
paradigm-shift atom is written alongside (not replacing) TARI atoms, so a
single snippet can contribute both a TARI-typed atom and a paradigm-typed
atom.

Honest deviation: regex-based type tagging is precision-biased and will
under-extract. Long-form essays often phrase predictions without trigger
words. We accept lower recall in exchange for traceability — a missed
atom is better than a fabricated type.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

import sys
THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR.parent / "tari"))
from atom_extractor import find_quotes, gloss_atom  # noqa: E402


# ---- Type-specific regex pattern sets ----

PREDICTION_PATTERNS = [
    # Future-tense + horizon markers
    re.compile(r"\b(?:in\s+(?:the\s+next\s+)?\d{1,2}\s+(?:years?|months?|decades?))\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
    re.compile(r"\bby\s+20\d{2}\b\s*[^.!?]{5,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:i\s+(?:think|believe|expect|predict|bet)|we(?:'ll|\s+will)\s+see|there\s+will\s+be)\s+[^.!?]{15,220}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:eventually|soon|future|next\s+(?:generation|decade|wave|era))\s+[^.!?]{15,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:going\s+to|gonna)\s+(?:be|happen|change|disrupt|replace|transform|emerge)\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
]

BLOCKER_PATTERNS = [
    re.compile(r"\b(?:the\s+(?:bottleneck|blocker|obstacle|barrier|constraint)|what(?:'s|\s+is)\s+stopping|the\s+(?:hard|main|real)\s+(?:part|problem|challenge|issue))\s+(?:is|are|here)\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:limited|bottlenecked|gated|capped|throttled)\s+by\s+[^.!?]{5,180}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:we\s+can't|we\s+cannot|nobody\s+(?:can|has))\s+[^.!?]{10,180}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:the\s+reason\s+(?:we|this|they)\s+(?:can't|cannot|don't|haven't))\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
]

FIRST_PRINCIPLE_PATTERNS = [
    re.compile(r"\b(?:fundamentally|in\s+principle|the\s+physics\s+(?:is|of)|the\s+(?:fundamental|underlying|deep|core)\s+(?:reason|constraint|principle|law|truth))\b\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:must|cannot)\s+(?:by|because\s+of)\s+(?:physics|math|information\s+theory|thermodynamics|computation|conservation)\b[^.!?]{0,180}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:no\s+free\s+lunch|conservation\s+of|information\s+theoretic|lower\s+bound|upper\s+bound|hard\s+limit|inherent\s+limit)\b\s+[^.!?]{5,180}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:if\s+you\s+(?:think|reason)\s+from\s+(?:first\s+principles|the\s+basics))\b[^.!?]{5,200}[.!?]", re.IGNORECASE),
]

ANALOGY_PATTERNS = [
    re.compile(r"\b(?:like|just\s+like|similar\s+to|analogous\s+to|the\s+same\s+way\s+(?:as|that))\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:think\s+of\s+(?:it|this)\s+(?:as|like)|imagine\s+(?:a|an|the))\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:[a-z]+\s+is\s+(?:like|the)\s+[a-z]+\s+(?:of|for))\s+[^.!?]{5,180}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:as\s+if|kind\s+of\s+like|in\s+the\s+way\s+that)\s+[^.!?]{10,180}[.!?]", re.IGNORECASE),
]

OPEN_PROBLEM_PATTERNS = [
    re.compile(r"\b(?:open\s+(?:question|problem|conjecture|challenge)|unsolved|we\s+(?:don't|do\s+not)\s+know|nobody\s+knows)\s+[^.!?]{5,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:remain(?:s|ing)?\s+(?:open|unclear|mysterious)|still\s+(?:an?\s+)?(?:open|unclear|mystery))\s+[^.!?]{5,180}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:nobody\s+has\s+(?:figured|solved|cracked)|no\s+one\s+has\s+(?:figured|solved))\s+[^.!?]{5,180}[.!?]", re.IGNORECASE),
]

TREND_PATTERNS = [
    re.compile(r"\b(?:over\s+the\s+(?:last|past)\s+(?:\d+\s+)?(?:years?|decades?|months?))\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:the\s+(?:trajectory|trend|pattern|curve)\s+(?:is|has\s+been|shows))\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:scaling|growing|doubling|halving|exponential(?:ly)?|compound(?:ing)?)\s+(?:every|by|at)\s+[^.!?]{5,180}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:every\s+(?:year|generation)\s+(?:we|the\s+models?|the\s+field))\s+[^.!?]{10,200}[.!?]", re.IGNORECASE),
]


PARADIGM_TYPE_PATTERNS = {
    "prediction": PREDICTION_PATTERNS,
    "blocker": BLOCKER_PATTERNS,
    "first_principle": FIRST_PRINCIPLE_PATTERNS,
    "analogy": ANALOGY_PATTERNS,
    "open_problem": OPEN_PROBLEM_PATTERNS,
    "trend": TREND_PATTERNS,
}


# ---- Date extraction (best-effort) ----

YEAR_RE = re.compile(r"\b(20\d{2})\b")
HORIZON_RE = re.compile(r"\b(?:in|within|next)\s+(\d{1,2})\s+(years?|months?|decades?)\b", re.IGNORECASE)


def extract_date_signal(quote: str, source_date: Optional[str]) -> Optional[str]:
    """Return an ISO-ish date string if the quote carries an explicit horizon,
    else fall back to source_date.

    For predictions, this is the *target* date (when the predicted state should hold).
    """
    m = HORIZON_RE.search(quote)
    if m:
        n = int(m.group(1))
        unit = m.group(2).lower()
        # Anchor on source_date if provided
        if source_date:
            try:
                anchor = datetime.fromisoformat(source_date.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                anchor = datetime.now(timezone.utc)
        else:
            anchor = datetime.now(timezone.utc)
        if "year" in unit:
            target_year = anchor.year + n
        elif "decade" in unit:
            target_year = anchor.year + 10 * n
        elif "month" in unit:
            target_year = anchor.year + (anchor.month + n) // 12
        else:
            return source_date
        return f"{target_year}-01-01"
    m = YEAR_RE.search(quote)
    if m:
        return f"{m.group(1)}-01-01"
    return source_date


# ---- Atom dataclass ----

@dataclass
class ParadigmAtom:
    atom_id: str
    atom_type: str                 # TARI-compatible primary type field
    paradigm_type: str             # one of PARADIGM_TYPE_PATTERNS keys
    snippet_id: str
    transcript_id: str
    source_date: Optional[str]
    target_date: Optional[str]     # extracted horizon (predictions) or None
    line_span: Tuple[int, int]
    verbatim_quote: str
    gloss: str
    extraction_pattern: str


def extract_paradigm_atoms_for_snippet(
    snippet_path: Path,
    source_date: Optional[str] = None,
) -> List[ParadigmAtom]:
    """Extract paradigm-shift atoms from a single snippet JSON file.

    Returns one or more ParadigmAtoms; the same snippet may produce multiple
    atoms of different paradigm_type. Atom IDs use the form:
        ATOM_<transcript_id>_<snippet_id>_<paradigm_type[:3]>_<NN>
    so paradigm-shift atom IDs do not collide with TARI atom IDs.
    """
    with snippet_path.open("r", encoding="utf-8") as f:
        snippet = json.load(f)

    text = snippet["verbatim_text"]
    sid = snippet["snippet_id"]
    tid = snippet.get("transcript_id", "T001")
    line_span = (snippet["start_line"], snippet["end_line"])

    atoms: List[ParadigmAtom] = []

    for paradigm_type, patterns in PARADIGM_TYPE_PATTERNS.items():
        quotes = find_quotes(text, patterns)
        # Per-type cap of 4 quotes to match TARI's discipline
        for i, q in enumerate(quotes[:4], start=1):
            atom_id = f"ATOM_{tid}_{sid}_{paradigm_type[:3].upper()}_{i:02d}"
            target_date = extract_date_signal(q, source_date)
            atoms.append(ParadigmAtom(
                atom_id=atom_id,
                atom_type=paradigm_type.upper(),
                paradigm_type=paradigm_type,
                snippet_id=sid,
                transcript_id=tid,
                source_date=source_date,
                target_date=target_date,
                line_span=line_span,
                verbatim_quote=q,
                gloss=gloss_atom(paradigm_type.upper(), q),
                extraction_pattern=f"{paradigm_type}_regex",
            ))

    return atoms


def extract_all_paradigm_atoms(
    snippets_dir: Path,
    out_dir: Path,
    transcript_date_map: Optional[dict] = None,
) -> List[ParadigmAtom]:
    """Extract paradigm atoms across all snippets in snippets_dir.

    transcript_date_map: {transcript_id: source_date_iso} for date inheritance.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    # Accept both TARI's `snippet_S*.json` and paradigm_shift's flattened
    # `snippet_<tid>_<sid>.json` naming.
    snippet_files = sorted(snippets_dir.glob("snippet_*.json"))
    all_atoms: List[ParadigmAtom] = []

    for sp in snippet_files:
        # peek transcript_id to look up date
        with sp.open("r", encoding="utf-8") as f:
            tid = json.load(f).get("transcript_id", "T001")
        source_date = (transcript_date_map or {}).get(tid)
        atoms = extract_paradigm_atoms_for_snippet(sp, source_date=source_date)
        all_atoms.extend(atoms)

    for atom in all_atoms:
        with (out_dir / f"{atom.atom_id}.json").open("w", encoding="utf-8") as f:
            d = asdict(atom)
            d["line_span"] = list(d["line_span"])
            json.dump(d, f, indent=2, ensure_ascii=False)

    # Build _index.json
    all_files = sorted(out_dir.glob("ATOM_*.json"))
    by_type = {}
    by_transcript = {}
    all_ids = []
    for af in all_files:
        with af.open("r", encoding="utf-8") as f:
            d = json.load(f)
        all_ids.append(d["atom_id"])
        by_type[d["paradigm_type"]] = by_type.get(d["paradigm_type"], 0) + 1
        tid = d.get("transcript_id", "T001")
        by_transcript[tid] = by_transcript.get(tid, 0) + 1

    index = {
        "n_atoms": len(all_files),
        "atom_ids": all_ids,
        "paradigm_type_distribution": by_type,
        "transcript_distribution": by_transcript,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    return all_atoms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snippets_dir", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--date_map_json", type=Path, default=None,
                    help="JSON file: {transcript_id: source_date_iso}")
    args = ap.parse_args()

    date_map = None
    if args.date_map_json and args.date_map_json.exists():
        with args.date_map_json.open("r", encoding="utf-8") as f:
            date_map = json.load(f)

    atoms = extract_all_paradigm_atoms(args.snippets_dir, args.out_dir, transcript_date_map=date_map)
    print(f"extracted {len(atoms)} paradigm-shift atoms")
    by_type = {}
    for a in atoms:
        by_type[a.paradigm_type] = by_type.get(a.paradigm_type, 0) + 1
    for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {t:18s} {c}")


if __name__ == "__main__":
    main()

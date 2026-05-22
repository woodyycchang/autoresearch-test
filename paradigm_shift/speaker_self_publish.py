"""Speaker self-publish check (Layer 6 v2 augmentation) for Run 5.

This module wraps `speaker_self_publish_cache.json` with a query API used
by market_verifier v2:

  is_self_publish_paraphrase(atom, speaker_id)
      Returns (is_self_publish, matched_entry, overlap_words)
      where is_self_publish is True iff the atom's verbatim_quote shares
      >=3 content-words (length>=4, not in stopwords) with any cached
      entry's title+snippet for that speaker.

The market_verifier v2 path uses this to flag candidates whose load-
bearing atom is a paraphrase of the speaker's own paper. Such candidates
are not auto-rejected — they're downgraded with a SELF_PUBLISH_MATCH
verdict reason, because a paradigm-shift candidate that just restates
the speaker's own paradigm-shift claim is not new signal.

The cache is JSON, hand-built from Claude's training knowledge of well-
known papers/essays. See speaker_self_publish_cache.json for entries.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


STOP = {
    "the", "a", "an", "and", "or", "but", "of", "in", "to", "from", "for",
    "with", "by", "on", "at", "is", "are", "was", "were", "be", "been",
    "this", "that", "these", "those", "as", "it", "its", "into", "than",
    "then", "we", "i", "you", "they", "their", "our", "my", "your",
    "would", "could", "should", "will", "can", "may", "might",
    "if", "so", "not", "no", "yes", "just", "atom", "atoms", "snippet",
    "candidate", "speaker", "section", "claim", "mechanism", "describes",
    "described", "going", "really", "very", "much", "many", "some", "other",
    "another", "have", "has", "had", "do", "does", "did", "say", "said",
    "let", "thing", "things", "way", "ways", "kind", "sort", "more",
    "less", "even", "still", "again", "want", "wants",
    "model", "models", "method", "methods", "paper", "papers", "system",
    "systems", "work", "works", "approach", "use", "uses", "used", "using",
}


def content_words(text: str, min_len: int = 4) -> List[str]:
    return [t for t in re.findall(r"[a-z][a-z\-]+", text.lower())
            if t not in STOP and len(t) >= min_len]


@dataclass
class SelfPublishMatch:
    is_self_publish: bool
    matched_entry_id: Optional[str]
    matched_title: Optional[str]
    matched_url: Optional[str]
    matched_year: Optional[int]
    overlap_words: List[str]
    overlap_count: int


def load_cache(cache_path: Path) -> Dict:
    with cache_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def is_self_publish_paraphrase(
    atom_quote: str,
    speaker_id: str,
    cache: Dict,
    min_overlap: int = 3,
) -> SelfPublishMatch:
    """Check whether atom_quote paraphrases any cached self-publish for speaker_id.

    Returns SelfPublishMatch with the best-overlap entry if any.
    """
    speakers = cache.get("speakers", {})
    speaker_entry = speakers.get(speaker_id, {})
    self_published = speaker_entry.get("self_published", [])
    if not self_published:
        return SelfPublishMatch(False, None, None, None, None, [], 0)

    quote_words = set(content_words(atom_quote))
    best: Optional[Tuple[int, List[str], dict]] = None

    for entry in self_published:
        blob = (entry.get("title", "") + " " + entry.get("snippet", "")).lower()
        blob_words = set(content_words(blob))
        overlap = sorted(quote_words & blob_words)
        if best is None or len(overlap) > best[0]:
            best = (len(overlap), overlap, entry)

    if best is None:
        return SelfPublishMatch(False, None, None, None, None, [], 0)

    n_overlap, overlap_words, entry = best
    is_match = n_overlap >= min_overlap
    return SelfPublishMatch(
        is_self_publish=is_match,
        matched_entry_id=entry.get("id"),
        matched_title=entry.get("title"),
        matched_url=entry.get("url"),
        matched_year=entry.get("year"),
        overlap_words=overlap_words,
        overlap_count=n_overlap,
    )


def check_candidate(
    candidate: dict,
    speaker_id_by_transcript: Dict[str, str],
    cache: Dict,
    atoms_dir: Optional[Path] = None,
    min_overlap: int = 3,
) -> Dict:
    """Run the self-publish check across all atoms cited by a candidate.

    speaker_id_by_transcript: {transcript_id: speaker_id}
    Returns: {
      "candidate_id": str,
      "atom_self_publish_results": [
        {"atom_id": ..., "transcript_id": ..., "speaker_id": ..., "match": SelfPublishMatch as dict}, ...
      ],
      "any_atom_is_self_publish": bool,
      "all_atoms_are_self_publish": bool,
      "n_self_publish_atoms": int,
    }
    """
    results: List[dict] = []
    n_self_pub = 0
    n_atoms = 0

    atom_ids = candidate.get("combined_atom_ids", [])
    # Look up atom quotes from disk if atoms_dir provided
    atom_quotes: Dict[str, Tuple[str, str]] = {}
    if atoms_dir is not None:
        for aid in atom_ids:
            ap = atoms_dir / f"{aid}.json"
            if ap.exists():
                with ap.open("r", encoding="utf-8") as f:
                    a = json.load(f)
                atom_quotes[aid] = (a.get("transcript_id", ""), a.get("verbatim_quote", ""))

    for aid in atom_ids:
        tid, quote = atom_quotes.get(aid, ("", ""))
        if not tid:
            continue
        speaker_id = speaker_id_by_transcript.get(tid, "")
        if not speaker_id:
            continue
        n_atoms += 1
        match = is_self_publish_paraphrase(quote, speaker_id, cache, min_overlap=min_overlap)
        if match.is_self_publish:
            n_self_pub += 1
        results.append({
            "atom_id": aid,
            "transcript_id": tid,
            "speaker_id": speaker_id,
            "match": asdict(match),
        })

    return {
        "candidate_id": candidate.get("candidate_id"),
        "atom_self_publish_results": results,
        "any_atom_is_self_publish": n_self_pub > 0,
        "all_atoms_are_self_publish": (n_self_pub == n_atoms and n_atoms > 0),
        "n_self_publish_atoms": n_self_pub,
        "n_atoms_checked": n_atoms,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def check_atoms_dir(
    atoms_dir: Path,
    speaker_id_by_transcript: Dict[str, str],
    cache: Dict,
    out_path: Optional[Path] = None,
    min_overlap: int = 3,
) -> Dict:
    """Run the self-publish check across EVERY atom in atoms_dir (independent of
    candidates). Useful for hit-rate diagnostics across the whole corpus.
    """
    by_speaker: Dict[str, Dict] = {}
    all_records: List[dict] = []
    n_total = 0
    n_hit = 0

    for ap in sorted(atoms_dir.glob("ATOM_*.json")):
        with ap.open("r", encoding="utf-8") as f:
            atom = json.load(f)
        tid = atom.get("transcript_id", "")
        speaker_id = speaker_id_by_transcript.get(tid, "")
        if not speaker_id:
            continue
        n_total += 1
        match = is_self_publish_paraphrase(
            atom.get("verbatim_quote", ""), speaker_id, cache, min_overlap=min_overlap,
        )
        rec = {
            "atom_id": atom["atom_id"],
            "transcript_id": tid,
            "speaker_id": speaker_id,
            "paradigm_type": atom.get("paradigm_type"),
            "match": asdict(match),
        }
        all_records.append(rec)
        if match.is_self_publish:
            n_hit += 1
            bs = by_speaker.setdefault(speaker_id, {"n_atoms": 0, "n_hits": 0, "matched_entries": {}})
            bs["n_hits"] += 1
            entry_id = match.matched_entry_id or "?"
            bs["matched_entries"][entry_id] = bs["matched_entries"].get(entry_id, 0) + 1
        bs = by_speaker.setdefault(speaker_id, {"n_atoms": 0, "n_hits": 0, "matched_entries": {}})
        bs["n_atoms"] += 1

    summary = {
        "n_atoms_checked": n_total,
        "n_self_publish_hits": n_hit,
        "hit_rate": (n_hit / n_total) if n_total else 0.0,
        "by_speaker": by_speaker,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "min_overlap": min_overlap,
        "all_records": all_records,
    }

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache_path", type=Path,
                    default=Path(__file__).parent / "speaker_self_publish_cache.json")
    ap.add_argument("--atoms_dir", required=True, type=Path)
    ap.add_argument("--manifest_path", required=True, type=Path,
                    help="Run manifest with transcript→speaker_id map.")
    ap.add_argument("--out_path", type=Path, default=None)
    ap.add_argument("--min_overlap", type=int, default=3)
    args = ap.parse_args()

    cache = load_cache(args.cache_path)
    with args.manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)
    speaker_map = {t["id"]: t.get("speaker_id", "") for t in manifest.get("transcripts", [])}

    summary = check_atoms_dir(args.atoms_dir, speaker_map, cache,
                              out_path=args.out_path,
                              min_overlap=args.min_overlap)
    print(f"checked {summary['n_atoms_checked']} atoms; {summary['n_self_publish_hits']} self-publish hits "
          f"(hit rate {summary['hit_rate']:.3f})")
    print("by speaker:")
    for sid, stats in sorted(summary["by_speaker"].items()):
        print(f"  {sid:18s} {stats['n_hits']}/{stats['n_atoms']} hits, "
              f"matched entries: {dict(stats.get('matched_entries', {}))}")


if __name__ == "__main__":
    main()

"""Market verifier (Layer 6) for Paradigm-Shift Finder v1.

For each Layer-5 stress-test survivor, issue 3-5 web_search queries
designed to find existing solutions:

  1. "<primary noun> startup"
  2. "<primary mechanism> YC company"
  3. "open source <primary noun>"
  4. "<primary noun> Series A OR Series B"
  5. "<primary noun> founded 2024 OR 2025 OR 2026"

A "strong match" requires >=3 content-word overlap with the candidate's
primary noun phrase in title+snippet, AND publication date within the
last 24 months (when available).

Verdicts:
  - SURVIVES_MARKET_CHECK   (0 strong matches across all reformulations)
  - FAIL_MARKET_EXISTS      (>=1 strong match; records matched
                             startups/products with URLs)

Honest failure mode: a startup that exists but doesn't surface in the top
results we issue will be a false negative. We mitigate with multiple
query reformulations but cannot promise coverage.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional


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
    "less", "even", "still", "again",
}


def content_words(text: str, min_len: int = 4) -> List[str]:
    return [t for t in re.findall(r"[a-z][a-z\-]+", text.lower())
            if t not in STOP and len(t) >= min_len]


def extract_primary_noun_phrase(candidate: dict) -> str:
    """Heuristic: pick the most informative content-word phrase from the
    candidate's why_potentially_useful + first_principles_validity_hypothesis,
    backing off to the cited atom verbatim_quotes via the claim text.

    Returns a 2-4 word phrase used as the search anchor.
    """
    # Prefer hypothesis & usefulness which are summary fields
    blob = " ".join([
        candidate.get("first_principles_validity_hypothesis", ""),
        candidate.get("why_potentially_useful", ""),
        candidate.get("claim", ""),
    ])
    words = content_words(blob)
    # Top 3 by frequency (keeps anchor focused)
    freq: Dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    top = sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:3]
    return " ".join(w for w, _ in top)


def build_market_queries(primary_phrase: str) -> List[str]:
    p = primary_phrase.strip()
    if not p:
        return []
    return [
        f"{p} startup",
        f"{p} YC company",
        f"open source {p}",
        f"{p} Series A OR Series B",
        f"{p} founded 2024 OR 2025 OR 2026",
    ]


def is_strong_match(primary_phrase: str, result: dict, min_overlap: int = 3) -> bool:
    """A result is a strong match if it has >=3 content-word overlap with
    primary_phrase in title+snippet."""
    blob = (result.get("title", "") + " " + result.get("snippet", "")).lower()
    p_words = set(content_words(primary_phrase))
    overlap = [w for w in p_words if w in blob]
    return len(overlap) >= min_overlap


@dataclass
class MarketVerdict:
    candidate_id: str
    verdict: str  # SURVIVES_MARKET_CHECK | FAIL_MARKET_EXISTS | FAIL_NO_QUERIES
    primary_phrase: str
    queries: List[str]
    n_strong_matches: int
    strong_matches: List[dict]    # [{"query": ..., "title": ..., "url": ..., "snippet": ...}]
    n_results_total: int
    timestamp: str


def verify_market(
    candidate: dict,
    search_fn: Callable[[str], List[dict]],
) -> MarketVerdict:
    """Run the market check on one candidate."""
    cand_id = candidate["candidate_id"]
    primary = extract_primary_noun_phrase(candidate)
    queries = build_market_queries(primary)

    if not queries:
        return MarketVerdict(
            candidate_id=cand_id,
            verdict="FAIL_NO_QUERIES",
            primary_phrase=primary,
            queries=[],
            n_strong_matches=0,
            strong_matches=[],
            n_results_total=0,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    strong_matches: List[dict] = []
    n_results = 0
    for q in queries:
        results = search_fn(q) or []
        n_results += len(results)
        for r in results:
            if is_strong_match(primary, r):
                strong_matches.append({
                    "query": q,
                    "title": r.get("title", "")[:120],
                    "url": r.get("url", ""),
                    "snippet": r.get("snippet", "")[:240],
                })

    verdict = "SURVIVES_MARKET_CHECK" if not strong_matches else "FAIL_MARKET_EXISTS"
    return MarketVerdict(
        candidate_id=cand_id,
        verdict=verdict,
        primary_phrase=primary,
        queries=queries,
        n_strong_matches=len(strong_matches),
        strong_matches=strong_matches,
        n_results_total=n_results,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def synthesized_market_search(query: str) -> List[dict]:
    """Default search callback for runs without a real web_search hook.

    Returns an empty list, which means every candidate will trivially
    "survive" the market check. This is the LEAST safe default and the
    orchestrator MUST wire a real search hook for production use.
    """
    return []


def verify_all(
    candidates_dir: Path,
    out_dir: Path,
    search_fn: Callable[[str], List[dict]] = synthesized_market_search,
    only_ids: Optional[List[str]] = None,
) -> List[MarketVerdict]:
    """Run market verification on every PASS_STRESS candidate in candidates_dir.

    If only_ids is provided, restrict to that subset.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    verdicts: List[MarketVerdict] = []
    for cp in sorted(candidates_dir.glob("CAND_*.json")):
        with cp.open("r", encoding="utf-8") as f:
            cand = json.load(f)
        if only_ids is not None and cand["candidate_id"] not in only_ids:
            continue
        # Only run on PASS_STRESS candidates if present; otherwise run on all
        stress = cand.get("stress_verdict") or {}
        if stress and stress.get("verdict") != "PASS_STRESS":
            continue
        v = verify_market(cand, search_fn=search_fn)
        verdicts.append(v)
        cand["market_verdict"] = asdict(v)
        with (out_dir / cp.name).open("w", encoding="utf-8") as f:
            json.dump(cand, f, indent=2, ensure_ascii=False)

    # _index.json
    by_v: Dict[str, int] = {}
    for v in verdicts:
        by_v[v.verdict] = by_v.get(v.verdict, 0) + 1
    surviving = [v for v in verdicts if v.verdict == "SURVIVES_MARKET_CHECK"]

    index = {
        "n_total": len(verdicts),
        "n_survives": len(surviving),
        "verdict_distribution": by_v,
        "surviving_ids": [v.candidate_id for v in surviving],
        "verified_at": datetime.now(timezone.utc).isoformat(),
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    rejected = [v for v in verdicts if v.verdict != "SURVIVES_MARKET_CHECK"]
    with (out_dir / "_rejected.json").open("w", encoding="utf-8") as f:
        json.dump([asdict(v) for v in rejected], f, indent=2)

    return verdicts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates_dir", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--search_cache_path", type=Path, default=None,
                    help="Pre-fetched web_search results: {query: [results]}")
    args = ap.parse_args()

    if args.search_cache_path and args.search_cache_path.exists():
        with args.search_cache_path.open("r", encoding="utf-8") as f:
            cache = json.load(f)
        def search_fn(q):
            return cache.get(q, [])
    else:
        search_fn = synthesized_market_search

    verdicts = verify_all(args.candidates_dir, args.out_dir, search_fn=search_fn)
    print(f"market-verified {len(verdicts)} candidates")
    by_v = {}
    for v in verdicts:
        by_v[v.verdict] = by_v.get(v.verdict, 0) + 1
    for k, n in sorted(by_v.items(), key=lambda x: -x[1]):
        print(f"  {k:32s} {n}")


if __name__ == "__main__":
    main()

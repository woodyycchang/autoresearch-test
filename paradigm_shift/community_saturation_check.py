"""Community saturation check for Paradigm-Shift Finder Run 8.

Run 7 produced 7 mechanism-coherent survivors, but every one collided with
a 2024-2026 saturated frontier-ML community topic (TTT, RLHF, on-device LLM
inference, ML4Science). Hypothesis: the corpus speakers all live in the
same saturated community, so semantic-coherent cross-combinations always
hit a paper cluster.

This module is the 7th pipeline layer. It does NOT itself call
web_search — it follows the same I/O contract as `arxiv_gate.py`:

  - INPUT: a list of records, each {candidate_id, query, supporting_results},
    where the harness (Claude main agent) has already performed the real
    WebSearch tool call for `query` and written the results in.
  - OUTPUT: per-candidate verdict {topic_keywords, query, distinct_arxiv_ids,
    arxiv_in_window_count, threshold, verdict}.

Rules:
  - SATURATED  if >= 5 distinct arXiv papers in the last 24 months
                 mention the topic keywords.
  - UNSATURATED if <  5.

Date-window filter: arXiv IDs are of the form YYMM.NNNNN (post-2007).
We extract YYMM, project it to a date, and compare against
`today - months_window`. Pre-2007 IDs are kept (rare in current ML)
to avoid silently dropping evidence; the count reflects every distinct
ID that matched the query.

Why a separate layer (not extending arXiv gate): the arXiv gate asks "is
this idea anchored in at least one arXiv paper?" (1+ paper = good). The
saturation check asks the opposite question — "is the topic so well-worn
that 5+ papers already chase it?" (5+ papers = saturated). They have
opposite polarity, so they cannot be the same gate.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, asdict, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ---- arXiv ID extraction (mirrors arxiv_gate.py) ----

ARXIV_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})(?:v\d+)?",
    re.IGNORECASE,
)


def parse_arxiv_id(url: str) -> Optional[str]:
    if not url:
        return None
    m = ARXIV_RE.search(url)
    return m.group(1) if m else None


def arxiv_id_to_yyyymm(arxiv_id: str) -> Optional[Tuple[int, int]]:
    """YYMM.NNNNN  ->  (YYYY, MM)  using 2007-era epoch."""
    m = re.match(r"^(\d{2})(\d{2})\.", arxiv_id)
    if not m:
        return None
    yy = int(m.group(1))
    mm = int(m.group(2))
    if mm < 1 or mm > 12:
        return None
    # arXiv switched to YYMM.NNNNN in April 2007; YY=07..99 -> 2007..2099,
    # YY=00..06 wraps to 21st century continuation.
    yyyy = 2000 + yy
    return (yyyy, mm)


def in_window(yyyymm: Tuple[int, int], today: date, months: int) -> bool:
    yyyy, mm = yyyymm
    cutoff_year = today.year
    cutoff_month = today.month - months
    while cutoff_month <= 0:
        cutoff_month += 12
        cutoff_year -= 1
    cutoff = (cutoff_year, cutoff_month)
    return (yyyy, mm) >= cutoff


# ---- Topic keyword extraction ----

# Reuse the stop list rationale from semantic_coherence_check.
STOP = {
    "the", "and", "for", "with", "that", "this", "are", "but", "have", "from",
    "you", "can", "all", "not", "any", "what", "when", "where", "which",
    "would", "could", "should", "will", "your", "just", "like", "into", "more",
    "than", "very", "also", "some", "such", "even", "only", "really", "thing",
    "things", "stuff", "kind", "right", "well", "actually", "okay", "yeah",
    "yes", "guess", "maybe", "sort", "lot", "lots", "much", "many", "few",
    "one", "two", "three", "first", "second", "next", "last", "back", "way",
    "now", "then", "here", "there", "going", "make", "made", "let", "see",
    "say", "said", "talk", "talking", "called", "case", "cases", "example",
    "examples", "fact", "facts", "true", "false", "really", "basically",
    "essentially", "obviously", "clearly", "actually", "literally",
    "today", "tomorrow", "year", "years", "month", "months", "day", "days",
    "time", "times",
    # Pipeline-meta words that leak from candidate.claim templates:
    "atom", "atoms", "candidate", "candidates", "snippet", "snippets",
    "transcript", "transcripts", "operator", "operators", "speaker", "speakers",
    # Conversational hedges and filler verbs that survive the alpha-only filter:
    "think", "thinks", "thinking", "thought", "thoughts", "given", "because",
    "trying", "turns", "additionally", "most", "least", "other", "another",
    "these", "those", "their", "them", "themselves", "ourselves",
    "reasonable", "reasonably", "probably", "possibly", "likely",
    "however", "therefore", "thus", "hence", "moreover", "furthermore",
    "instead", "rather", "while", "whereas", "although", "though",
    "fundamentally", "essentially", "specifically", "particularly",
    "above", "below", "before", "after", "during", "between", "among",
    "want", "wants", "wanted", "need", "needs", "needed", "going",
    # More conversational fluff
    "know", "knows", "knew", "seen", "saw", "were", "was", "been",
    "good", "great", "doing", "does", "did", "done", "quite", "still",
    "every", "always", "never", "ever", "yet",
    "arises", "arise",
}

# Domain-light filler — words that match Run 7's saturation collision keywords
# but are TOO generic to be useful as query terms alone. We keep them if they
# co-occur with a content noun, but we don't lead a query with them.
WEAK = {
    "model", "models", "training", "learning", "system", "systems",
    "method", "methods", "approach", "approaches", "problem", "problems",
    "work", "works", "research", "study", "studies", "paper", "papers",
    "data", "performance", "result", "results", "task", "tasks",
    "domain", "general", "specific", "different", "important",
    "people", "person", "users", "user", "world", "self",
}


def content_nouns(text: str, top_n: int = 5) -> List[str]:
    """Pull top_n distinct content nouns from text.

    Heuristic: tokenize alpha words >=4 chars, drop stop+weak, prefer
    higher-frequency. Returns lowercase tokens in decreasing frequency
    (ties broken by first appearance order).
    """
    words = [w for w in re.findall(r"[a-z][a-z\-]+", text.lower())
             if len(w) >= 4 and w not in STOP and w not in WEAK]
    first_seen: Dict[str, int] = {}
    for i, w in enumerate(words):
        first_seen.setdefault(w, i)
    counts = Counter(words)
    # Sort by (-count, first_seen) so higher count wins, tie -> earlier
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], first_seen[kv[0]]))
    return [w for w, _ in ranked[:top_n]]


def extract_topic_keywords(candidate: dict, atoms_by_id: Dict[str, dict],
                           top_n: int = 5) -> List[str]:
    """Pool atom verbatim quotes (primary), then content_nouns top_n.

    candidate.claim is template scaffolding ("Prediction in atom X ... holds
    iff ..."), so we exclude it from the keyword pool. The signal is in the
    speaker's verbatim quotes that the atoms anchor.
    """
    parts: List[str] = []
    for aid in candidate.get("combined_atom_ids", []):
        a = atoms_by_id.get(aid)
        if a:
            parts.append(a.get("verbatim_quote", ""))
    pooled = " ".join(parts)
    return content_nouns(pooled, top_n=top_n)


def build_query(keywords: List[str]) -> str:
    """Spec: '{topic_keywords} 2024 2025 2026 arXiv'."""
    head = " ".join(keywords[:5])
    return f"{head} 2024 2025 2026 arXiv"


# ---- Verdict ----

@dataclass
class SaturationVerdict:
    candidate_id: str
    topic_keywords: List[str]
    query: str
    distinct_arxiv_ids: List[str] = field(default_factory=list)
    arxiv_in_window_count: int = 0
    arxiv_total_count: int = 0
    months_window: int = 24
    threshold: int = 5
    today: str = ""
    verdict: str = "UNKNOWN"   # SATURATED | UNSATURATED | NO_SEARCH
    notes: str = ""


def verdict_for_record(record: dict, today: date, months_window: int = 24,
                       threshold: int = 5) -> SaturationVerdict:
    """record = {candidate_id, query, topic_keywords, supporting_results}."""
    cid = record["candidate_id"]
    results = record.get("supporting_results")
    sv = SaturationVerdict(
        candidate_id=cid,
        topic_keywords=record.get("topic_keywords", []),
        query=record.get("query", ""),
        months_window=months_window,
        threshold=threshold,
        today=today.isoformat(),
    )
    if results is None:
        sv.verdict = "NO_SEARCH"
        sv.notes = "no supporting_results — harness did not run WebSearch for this candidate"
        return sv

    # Collect distinct arXiv IDs from URLs (and any plain-text 'arxiv.org/...'
    # inside title/snippet, for completeness).
    distinct: List[str] = []
    seen = set()
    for r in results:
        url = r.get("url", "") or ""
        blob = " ".join([url, r.get("title", "") or "", r.get("snippet", "") or ""])
        m = ARXIV_RE.search(blob)
        if m:
            aid = m.group(1)
            if aid not in seen:
                seen.add(aid)
                distinct.append(aid)
    sv.distinct_arxiv_ids = distinct
    sv.arxiv_total_count = len(distinct)

    # Filter to last `months_window` months.
    in_win: List[str] = []
    for aid in distinct:
        ym = arxiv_id_to_yyyymm(aid)
        if ym is None:
            continue
        if in_window(ym, today, months_window):
            in_win.append(aid)
    sv.arxiv_in_window_count = len(in_win)

    if sv.arxiv_in_window_count >= threshold:
        sv.verdict = "SATURATED"
    else:
        sv.verdict = "UNSATURATED"
    sv.notes = f"in_window={in_win}"
    return sv


# ---- Driver ----

def load_atoms_index(atoms_dir: Path) -> Dict[str, dict]:
    idx: Dict[str, dict] = {}
    for p in atoms_dir.glob("ATOM_*.json"):
        with p.open("r", encoding="utf-8") as f:
            a = json.load(f)
        idx[a["atom_id"]] = a
    return idx


def emit_queries(candidates: List[dict], atoms_by_id: Dict[str, dict],
                 top_n: int = 5) -> List[dict]:
    """Build the per-candidate query list — harness consumes this and
    populates supporting_results before calling verdict_for_record."""
    out = []
    for cand in candidates:
        kws = extract_topic_keywords(cand, atoms_by_id, top_n=top_n)
        q = build_query(kws)
        out.append({
            "candidate_id": cand["candidate_id"],
            "topic_keywords": kws,
            "query": q,
            "supporting_results": None,
        })
    return out


def verdict_all(records: List[dict], today: Optional[date] = None,
                months_window: int = 24, threshold: int = 5) -> List[SaturationVerdict]:
    if today is None:
        today = datetime.now(timezone.utc).date()
    return [verdict_for_record(r, today=today, months_window=months_window,
                               threshold=threshold) for r in records]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_emit = sub.add_parser("emit_queries")
    p_emit.add_argument("--candidates_dir", required=True, type=Path)
    p_emit.add_argument("--atoms_dir", required=True, type=Path)
    p_emit.add_argument("--candidate_ids_json", required=True, type=Path,
                        help="JSON list of candidate IDs to score")
    p_emit.add_argument("--out", required=True, type=Path)
    p_emit.add_argument("--top_n", type=int, default=5)

    p_verd = sub.add_parser("verdict")
    p_verd.add_argument("--records", required=True, type=Path,
                        help="JSON list with supporting_results populated")
    p_verd.add_argument("--out", required=True, type=Path)
    p_verd.add_argument("--today", default="2026-05-23")
    p_verd.add_argument("--months_window", type=int, default=24)
    p_verd.add_argument("--threshold", type=int, default=5)

    args = ap.parse_args()

    if args.cmd == "emit_queries":
        ids = json.loads(args.candidate_ids_json.read_text())
        atoms_by_id = load_atoms_index(args.atoms_dir)
        cands = []
        for cid in ids:
            cands.append(json.loads((args.candidates_dir / f"{cid}.json").read_text()))
        records = emit_queries(cands, atoms_by_id, top_n=args.top_n)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(records, indent=2), encoding="utf-8")
        print(f"emitted {len(records)} query records → {args.out}")
        for r in records:
            print(f"  {r['candidate_id']}: {r['query']}")

    elif args.cmd == "verdict":
        recs = json.loads(args.records.read_text())
        today_d = datetime.strptime(args.today, "%Y-%m-%d").date()
        verdicts = verdict_all(recs, today=today_d,
                               months_window=args.months_window,
                               threshold=args.threshold)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps([asdict(v) for v in verdicts], indent=2),
                            encoding="utf-8")
        n_sat = sum(1 for v in verdicts if v.verdict == "SATURATED")
        n_uns = sum(1 for v in verdicts if v.verdict == "UNSATURATED")
        n_noq = sum(1 for v in verdicts if v.verdict == "NO_SEARCH")
        print(f"verdicts: SATURATED={n_sat} UNSATURATED={n_uns} NO_SEARCH={n_noq}")
        for v in verdicts:
            print(f"  {v.candidate_id}: {v.arxiv_in_window_count} arXiv hits → {v.verdict}")


if __name__ == "__main__":
    main()

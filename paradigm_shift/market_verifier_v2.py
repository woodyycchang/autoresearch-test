"""Market Verifier v2 (Layer 6 v2) — Paradigm-Shift Finder.

Four upgrades over v1 (see design/market_verifier_v2_spec.md):
  A. Semantic similarity (TF-IDF cosine, replaces 3-content-word overlap)
  B. Speaker self-publish check (new): web_search "{speaker} {keyword}"
  C. Recent paper weight (new): last 12 months = 2x, last 13-24 months = 1.5x
  D. Cross-LLM sanity check (new): paste-ready prompts for top-3 survivors

v1 (market_verifier.py) remains callable for legacy runs and is the historical
record for run_001 and run_002 outputs. v2 writes to a sibling directory
`market_v2/` per run.

Honest limits documented in §6 of the spec — embedding bias, speaker-name
extraction fidelity, date-parsing heuristic, cross-LLM as manual loop.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple


# ---- Content words / stop list (matches v1 for consistency) ----

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
    "less", "even", "still", "again", "apply", "applied", "framed",
    "frames", "prediction", "blocker", "analogy",  # template residue
    "first", "principle", "principles", "resolves", "resolution", "open",
    "problem", "future", "state", "contains", "structure", "structural",
    "correspondence", "preserves", "constraint", "pattern", "merely",
    "surface", "metaphor", "atom_t", "named",
    # Common conjunctions / intensifiers / generic verbs that are not topical
    "because", "about", "like", "also", "here", "there", "where", "which",
    "what", "when", "how", "such", "while", "since", "though", "although",
    "however", "therefore", "thus", "hence", "rather", "instead", "indeed",
    "actually", "basically", "essentially", "specifically", "particularly",
    "want", "need", "make", "made", "makes", "take", "took", "taken",
    "give", "given", "gave", "get", "got", "gotten", "come", "came",
    "back", "down", "over", "after", "before", "until", "during", "across",
    "around", "between", "through", "without", "within", "above", "below",
    "able", "well", "always", "never", "often", "sometimes", "usually",
    "good", "bad", "new", "old", "high", "low", "big", "small", "long",
    "short", "great", "little", "right", "wrong", "true", "false", "real",
    "same", "different", "similar", "every", "each", "both", "either",
    "neither", "anything", "something", "nothing", "everything", "anyone",
    "someone", "noone", "everyone", "talk", "talking", "talked", "tell",
    "told", "ask", "asked", "look", "looked", "looking", "see", "seen",
    "saw", "find", "found", "think", "thought", "know", "knew", "known",
    "mean", "means", "meant", "show", "shown", "showed", "work", "works",
    "worked", "use", "used", "uses",
}


def content_words(text: str, min_len: int = 4) -> List[str]:
    return [t for t in re.findall(r"[a-z][a-z\-]+", text.lower())
            if t not in STOP and len(t) >= min_len]


# ---- Template scaffolding stripper ----

TEMPLATE_PATTERNS = [
    re.compile(r"Apply the analogical structure in atom \S+\s*\(\".*?\"\)\s*to the open problem framed in atom \S+\s*\(\".*?\"\)\.?", re.IGNORECASE | re.DOTALL),
    re.compile(r"Apply the mechanism described in atom \S+\s*\(\".*?\"\)\s*to the problem framed in atom \S+\s*\(\".*?\"\)\.?", re.IGNORECASE | re.DOTALL),
    re.compile(r"The prediction in atom \S+\s*\(\".*?\"\)\s*is the resolution of the blocker in atom \S+\s*\(\".*?\"\)\.?", re.IGNORECASE | re.DOTALL),
    re.compile(r"Compose the primitive in atom \S+\s*with the primitive in atom \S+:?\s*[^.]*\.?", re.IGNORECASE | re.DOTALL),
    re.compile(r"The blocker in atom \S+\s*\(\".*?\"\)\s*is dissolved by recognizing the first-principle in atom \S+\s*\(\".*?\"\)\.?", re.IGNORECASE | re.DOTALL),
    re.compile(r"Prediction in atom \S+\s*\(\".*?\"\)\s*holds if and only if the first-principle constraint in atom \S+\s*\(\".*?\"\)\s*is binding\.?", re.IGNORECASE | re.DOTALL),
    # Strip the IDs themselves
    re.compile(r"ATOM_[A-Z0-9_]+"),
]


def strip_template_scaffolding(text: str) -> str:
    """Remove templated wrapping from candidate claim, leaving atom-quoted content."""
    s = text
    for pat in TEMPLATE_PATTERNS:
        s = pat.sub(" ", s)
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_atom_quote_content(candidate: dict, atoms_dir: Optional[Path] = None) -> str:
    """Pull verbatim_quote from each cited atom (the actual semantic content).

    If atoms_dir is provided, read from there. Otherwise extract quotes already
    embedded in candidate.claim.
    """
    if atoms_dir:
        parts = []
        for aid in candidate.get("combined_atom_ids", []):
            ap = atoms_dir / f"{aid}.json"
            if ap.exists():
                with ap.open("r", encoding="utf-8") as f:
                    parts.append(json.load(f).get("verbatim_quote", ""))
        if parts:
            return " ".join(parts)
    # Fallback: scrape quotes from the templated claim text
    quotes = re.findall(r'\("([^"]+)"\)', candidate.get("claim", ""))
    return " ".join(quotes)


def build_semantic_anchor(candidate: dict, atoms_dir: Optional[Path] = None) -> str:
    """Build the semantic anchor for a candidate.

    Concatenates:
      - claim stripped of template scaffolding
      - verbatim_quote of each cited atom
      - first_principles_validity_hypothesis (template, but kept for backup)
    """
    pieces: List[str] = []
    claim_stripped = strip_template_scaffolding(candidate.get("claim", ""))
    if claim_stripped:
        pieces.append(claim_stripped)
    atom_content = extract_atom_quote_content(candidate, atoms_dir=atoms_dir)
    if atom_content:
        pieces.append(atom_content)
    # Hypothesis is templated, so use it last and lightly
    hyp = candidate.get("first_principles_validity_hypothesis", "")
    if hyp:
        pieces.append(hyp)
    return " ".join(pieces)


# ---- TF-IDF cosine similarity ----

def _tf(words: List[str]) -> Dict[str, float]:
    if not words:
        return {}
    freq: Dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    total = float(len(words))
    return {w: c / total for w, c in freq.items()}


def _idf_corpus(docs_words: List[List[str]]) -> Dict[str, float]:
    """Inverse document frequency over a small corpus."""
    n_docs = len(docs_words)
    if n_docs == 0:
        return {}
    df: Dict[str, int] = {}
    for words in docs_words:
        for w in set(words):
            df[w] = df.get(w, 0) + 1
    return {w: math.log((1.0 + n_docs) / (1.0 + d)) + 1.0 for w, d in df.items()}


def _tfidf_vec(words: List[str], idf: Dict[str, float]) -> Dict[str, float]:
    tf = _tf(words)
    return {w: tf[w] * idf.get(w, 0.0) for w in tf}


def cosine_similarity(a: Dict[str, float], b: Dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    # Dot product
    dot = sum(a.get(w, 0.0) * b.get(w, 0.0) for w in a if w in b)
    # Norms
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def compute_similarity(anchor_text: str, result_text: str,
                        corpus_texts: Optional[List[str]] = None) -> float:
    """TF-IDF cosine similarity between anchor and result.

    corpus_texts is used to compute IDF; if None, uses just (anchor, result).
    """
    aw = content_words(anchor_text)
    rw = content_words(result_text)
    if not aw or not rw:
        return 0.0
    docs = [aw, rw]
    if corpus_texts:
        for ct in corpus_texts:
            docs.append(content_words(ct))
    idf = _idf_corpus(docs)
    va = _tfidf_vec(aw, idf)
    vr = _tfidf_vec(rw, idf)
    return cosine_similarity(va, vr)


# ---- Date extraction & weighting ----

ARXIV_DATE_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{2})(\d{2})\.\d{4,5}", re.IGNORECASE)
YEAR_TITLE_RE = re.compile(r"\b(20[2-3]\d)\b")


def extract_publication_year_month(title: str, snippet: str, url: str) -> Optional[Tuple[int, int]]:
    """Best-effort (year, month) extraction. Returns None if unknown."""
    m = ARXIV_DATE_RE.search(url or "")
    if m:
        yy = int(m.group(1))
        mm = int(m.group(2))
        # arXiv codes: YYMM. e.g. 2512 = December 2025
        year = 2000 + yy
        if 1 <= mm <= 12:
            return (year, mm)
    # Fall back: find a year in title+snippet
    for s in (title, snippet, url or ""):
        m2 = YEAR_TITLE_RE.search(s or "")
        if m2:
            return (int(m2.group(1)), 6)  # assume mid-year
    return None


def date_weight(yymm: Optional[Tuple[int, int]],
                today: Optional[datetime] = None) -> float:
    """2.0 for last 12 months, 1.5 for 13-24 months, 1.0 otherwise."""
    if yymm is None:
        return 1.0
    today = today or datetime.now(timezone.utc)
    year, month = yymm
    months_old = (today.year - year) * 12 + (today.month - month)
    if months_old <= 12:
        return 2.0
    if months_old <= 24:
        return 1.5
    return 1.0


# ---- Verdict dataclass ----

VERDICT_SURVIVES = "SURVIVES_MARKET_CHECK_V2"
VERDICT_FAIL_SEMANTIC = "FAIL_MARKET_EXISTS_V2_SEMANTIC"
VERDICT_FAIL_SPEAKER = "FAIL_MARKET_EXISTS_V2_SPEAKER"
VERDICT_FAIL_BOTH = "FAIL_MARKET_EXISTS_V2_BOTH"
VERDICT_NO_QUERIES = "FAIL_NO_QUERIES"


@dataclass
class CollisionHit:
    title: str
    url: str
    snippet: str
    raw_similarity: float
    date_weight: float
    weighted_similarity: float
    publication_year_month: Optional[Tuple[int, int]]
    matched_speaker: Optional[str]  # set when this came from a speaker query


@dataclass
class MarketVerdictV2:
    candidate_id: str
    verdict: str
    primary_keyword: str
    semantic_anchor: str
    speaker_collisions: List[dict]   # CollisionHit dicts where matched_speaker is set
    semantic_collisions: List[dict]  # CollisionHit dicts from generic queries
    top_weighted_similarity: float
    cross_llm_queued: bool
    speakers_checked: List[str]
    timestamp: str


# ---- Manifest helpers ----

def load_manifest_speakers(manifest_path: Path) -> Dict[str, str]:
    """Return {transcript_id: speaker_name} from manifest.json."""
    if not manifest_path.exists():
        return {}
    with manifest_path.open("r", encoding="utf-8") as f:
        m = json.load(f)
    return {t["id"]: t.get("speaker", "") for t in m.get("transcripts", [])}


# ---- Per-candidate v2 verify ----

def _primary_keyword(anchor: str) -> str:
    """Return the single top content word (for the primary_keyword display field)."""
    kws = _top_keywords(anchor, k=1)
    return kws[0] if kws else ""


def _top_keywords(anchor: str, k: int = 3) -> List[str]:
    """Return top-k content words by frequency. Used to issue multiple speaker
    queries: one per top keyword, increasing the chance that a speaker's
    follow-up paper surfaces."""
    cw = content_words(anchor)
    if not cw:
        return []
    freq: Dict[str, int] = {}
    for w in cw:
        freq[w] = freq.get(w, 0) + 1
    top = sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:k]
    return [w for w, _ in top]


def _result_text(r: dict) -> str:
    return (r.get("title", "") + " " + r.get("snippet", "")).strip()


def _speaker_in_result(speaker: str, r: dict) -> bool:
    if not speaker:
        return False
    parts = re.split(r"\s+", speaker.strip().lower())
    blob = (r.get("title", "") + " " + r.get("snippet", "") + " " + r.get("url", "")).lower()
    # Require at least the last name to appear
    return parts[-1] in blob if parts else False


def verify_market_v2(
    candidate: dict,
    search_fn: Callable[[str], List[dict]],
    manifest_speakers: Dict[str, str],
    atoms_dir: Optional[Path] = None,
    semantic_threshold: float = 0.5,
    today: Optional[datetime] = None,
    speaker_pub_cache: Optional[Dict[str, List[dict]]] = None,
) -> MarketVerdictV2:
    """Run Layer 6 v2 on a single candidate."""
    cand_id = candidate["candidate_id"]
    anchor = build_semantic_anchor(candidate, atoms_dir=atoms_dir)
    primary = _primary_keyword(anchor)
    top_kws = _top_keywords(anchor, k=3)

    if not primary or not anchor:
        return MarketVerdictV2(
            candidate_id=cand_id, verdict=VERDICT_NO_QUERIES,
            primary_keyword="", semantic_anchor=anchor,
            speaker_collisions=[], semantic_collisions=[],
            top_weighted_similarity=0.0, cross_llm_queued=False,
            speakers_checked=[],
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    # --- Generic semantic queries ---
    semantic_queries = [
        f"{primary} startup",
        f"{primary} YC company",
        f"{primary} paper 2024 2025 2026",
        f"open source {primary}",
        anchor[:200],  # also issue the anchor itself as a query
    ]

    # --- Speaker self-publish queries ---
    # Issue one query per (speaker, top-keyword) pair. Using top-3 keywords
    # rather than just primary_keyword catches the case where the most-frequent
    # word is a template residue (e.g. "because") while the second/third most
    # frequent are the real topical signal (e.g. "test", "time", "context").
    speakers: List[str] = []
    for tid in candidate.get("source_transcripts", []):
        sp = manifest_speakers.get(tid, "").strip()
        if sp and sp not in speakers:
            speakers.append(sp)

    speaker_queries: List[Tuple[str, str]] = []  # (speaker, query)
    # Query 1: concatenate top-3 keywords for disambiguation when the speaker
    # name is common (e.g. "Yu Sun" matches multiple academics).
    if top_kws:
        joined = " ".join(top_kws)
        for sp in speakers:
            speaker_queries.append((sp, f"{sp} {joined} 2024 OR 2025 OR 2026"))
    # Query 2-4: also issue per-keyword (catches cases where the joined query
    # is too specific to surface anything).
    for sp in speakers:
        for kw in top_kws:
            speaker_queries.append((sp, f"{sp} {kw} 2024 OR 2025 OR 2026"))

    # --- Issue queries, build CollisionHits ---
    semantic_hits: List[CollisionHit] = []
    speaker_hits: List[CollisionHit] = []
    seen_urls = set()

    def _score_and_collect(results, q_speaker=None):
        out: List[CollisionHit] = []
        for r in results or []:
            url = r.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            rtext = _result_text(r)
            sim = compute_similarity(anchor, rtext)
            yymm = extract_publication_year_month(r.get("title", ""), r.get("snippet", ""), url)
            dw = date_weight(yymm, today=today)
            ws = sim * dw
            speaker_matched = q_speaker if (q_speaker and _speaker_in_result(q_speaker, r)) else None
            if ws >= semantic_threshold:
                hit = CollisionHit(
                    title=r.get("title", "")[:200],
                    url=url,
                    snippet=r.get("snippet", "")[:300],
                    raw_similarity=sim,
                    date_weight=dw,
                    weighted_similarity=ws,
                    publication_year_month=yymm,
                    matched_speaker=speaker_matched,
                )
                out.append(hit)
        return out

    # Run semantic queries
    for q in semantic_queries:
        try:
            results = search_fn(q)
        except Exception:
            results = []
        for hit in _score_and_collect(results, q_speaker=None):
            semantic_hits.append(hit)

    # Run speaker queries (populate cache)
    if speaker_pub_cache is not None:
        for sp, q in speaker_queries:
            try:
                results = search_fn(q)
            except Exception:
                results = []
            speaker_pub_cache.setdefault(sp, []).extend([
                {"query": q, "results": results[:5]}
            ])
            # Hits where the speaker is named in the result are speaker hits;
            # otherwise still count toward semantic if weighted_sim >= threshold.
            for hit in _score_and_collect(results, q_speaker=sp):
                if hit.matched_speaker:
                    speaker_hits.append(hit)
                else:
                    semantic_hits.append(hit)
    else:
        for sp, q in speaker_queries:
            try:
                results = search_fn(q)
            except Exception:
                results = []
            for hit in _score_and_collect(results, q_speaker=sp):
                if hit.matched_speaker:
                    speaker_hits.append(hit)
                else:
                    semantic_hits.append(hit)

    # --- Compute verdict ---
    n_sem = len(semantic_hits)
    n_spk = len(speaker_hits)
    top_ws = max([h.weighted_similarity for h in semantic_hits + speaker_hits] + [0.0])

    if n_sem > 0 and n_spk > 0:
        verdict = VERDICT_FAIL_BOTH
    elif n_spk > 0:
        verdict = VERDICT_FAIL_SPEAKER
    elif n_sem > 0:
        verdict = VERDICT_FAIL_SEMANTIC
    else:
        verdict = VERDICT_SURVIVES

    return MarketVerdictV2(
        candidate_id=cand_id,
        verdict=verdict,
        primary_keyword=primary,
        semantic_anchor=anchor[:400],
        speaker_collisions=[asdict(h) for h in speaker_hits],
        semantic_collisions=[asdict(h) for h in semantic_hits],
        top_weighted_similarity=top_ws,
        cross_llm_queued=False,
        speakers_checked=speakers,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ---- Batch verify_all ----

def synthesized_market_search_v2(query: str) -> List[dict]:
    """Default search callback for runs without a real web_search hook."""
    return []


def verify_all_v2(
    scored_dir: Path,
    manifest_path: Path,
    out_dir: Path,
    search_fn: Callable[[str], List[dict]] = synthesized_market_search_v2,
    atoms_dir: Optional[Path] = None,
    semantic_threshold: float = 0.5,
    speaker_cache_path: Optional[Path] = None,
    cross_llm_queue_path: Optional[Path] = None,
    today: Optional[datetime] = None,
) -> List[MarketVerdictV2]:
    """Run Layer 6 v2 on every PASS_STRESS candidate in scored_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    speakers = load_manifest_speakers(manifest_path)

    # Speaker publications cache (read-modify-write)
    speaker_cache: Dict[str, List[dict]] = {}
    if speaker_cache_path and speaker_cache_path.exists():
        with speaker_cache_path.open("r", encoding="utf-8") as f:
            speaker_cache = json.load(f)

    verdicts: List[MarketVerdictV2] = []
    candidates_full: List[dict] = []

    for cp in sorted(scored_dir.glob("CAND_*.json")):
        with cp.open("r", encoding="utf-8") as f:
            cand = json.load(f)
        candidates_full.append(cand)
        # Optionally restrict to PASS_STRESS; for retrospective audit we want all
        v = verify_market_v2(
            cand, search_fn=search_fn,
            manifest_speakers=speakers,
            atoms_dir=atoms_dir,
            semantic_threshold=semantic_threshold,
            today=today,
            speaker_pub_cache=speaker_cache,
        )
        verdicts.append(v)
        cand["market_verdict_v2"] = asdict(v)
        with (out_dir / cp.name).open("w", encoding="utf-8") as f:
            json.dump(cand, f, indent=2, ensure_ascii=False)

    # Persist speaker cache
    if speaker_cache_path:
        speaker_cache_path.parent.mkdir(parents=True, exist_ok=True)
        with speaker_cache_path.open("w", encoding="utf-8") as f:
            json.dump(speaker_cache, f, indent=2, ensure_ascii=False)

    # _index.json
    by_v: Dict[str, int] = {}
    for v in verdicts:
        by_v[v.verdict] = by_v.get(v.verdict, 0) + 1
    surviving = [v for v in verdicts if v.verdict == VERDICT_SURVIVES]

    index = {
        "n_total": len(verdicts),
        "n_survives": len(surviving),
        "verdict_distribution": by_v,
        "surviving_ids": [v.candidate_id for v in surviving],
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "semantic_threshold": semantic_threshold,
        "speakers_in_manifest": list(speakers.values()),
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    rejected = [v for v in verdicts if v.verdict != VERDICT_SURVIVES]
    with (out_dir / "_rejected.json").open("w", encoding="utf-8") as f:
        json.dump([asdict(v) for v in rejected], f, indent=2, ensure_ascii=False)

    # Cross-LLM queue: top-3 survivors by predicted_impact
    if cross_llm_queue_path and surviving:
        # Sort survivors by predicted_impact (descending)
        cand_by_id = {c["candidate_id"]: c for c in candidates_full}
        ranked = sorted(
            surviving,
            key=lambda v: -cand_by_id.get(v.candidate_id, {})
                .get("impact_score", {}).get("predicted_impact", 0.0),
        )[:3]
        queue_entries = []
        for v in ranked:
            c = cand_by_id.get(v.candidate_id, {})
            prompt = _build_cross_llm_prompt(c, v)
            queue_entries.append({
                "candidate_id": v.candidate_id,
                "prompt": prompt,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "primary_keyword": v.primary_keyword,
                "speakers_checked": v.speakers_checked,
            })
            v.cross_llm_queued = True

        # Append to queue file
        existing = {"queue": []}
        if cross_llm_queue_path.exists():
            with cross_llm_queue_path.open("r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.setdefault("queue", []).extend(queue_entries)
        existing["updated_at"] = datetime.now(timezone.utc).isoformat()
        cross_llm_queue_path.parent.mkdir(parents=True, exist_ok=True)
        with cross_llm_queue_path.open("w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

    return verdicts


def _build_cross_llm_prompt(candidate: dict, verdict: MarketVerdictV2) -> str:
    """Construct a paste-ready prompt for cross-LLM verification."""
    claim = candidate.get("claim", "")
    hyp = candidate.get("first_principles_validity_hypothesis", "")
    atoms = ", ".join(candidate.get("combined_atom_ids", []))
    speakers = ", ".join(verdict.speakers_checked) or "(none)"
    return (
        "You are reviewing a paradigm-shift candidate identified by another LLM "
        "from a 6-layer pipeline. Be skeptical.\n\n"
        f"**Candidate claim:** {claim}\n\n"
        f"**Cited source atoms:** {atoms}\n\n"
        f"**Source-transcript speakers:** {speakers}\n\n"
        f"**First-principles validity hypothesis:** {hyp}\n\n"
        f"**Top semantic keyword:** {verdict.primary_keyword}\n\n"
        "**Question:** Has this idea (or anything semantically equivalent) "
        "already been published in a paper, productized as a startup, or talked "
        "about publicly by the listed speakers themselves or another author "
        "between 2023 and 2026? Pay special attention to any paper the listed "
        "speakers themselves co-authored. If yes, cite the source (paper title, "
        "URL, year). If no, briefly state why this would be novel and what kind "
        "of POC (3-6 months, solo founder) would test the hypothesis."
    )


# ---- Retrospective audit ----

def retrospective_audit(
    run_dir: Path,
    manifest_path: Path,
    search_fn: Callable[[str], List[dict]],
    out_path: Path,
    semantic_threshold: float = 0.5,
    today: Optional[datetime] = None,
) -> dict:
    """Run Layer 6 v2 on a previous run's candidates and write a v1-vs-v2 diff."""
    scored_dir = run_dir / "scored"
    market_v1_dir = run_dir / "market"
    atoms_dir = run_dir / "atoms"

    speakers = load_manifest_speakers(manifest_path)

    v1_verdicts: Dict[str, str] = {}
    if market_v1_dir.exists():
        for cp in sorted(market_v1_dir.glob("CAND_*.json")):
            with cp.open("r", encoding="utf-8") as f:
                c = json.load(f)
            mv = c.get("market_verdict", {})
            v1_verdicts[c["candidate_id"]] = mv.get("verdict", "?")

    diffs = []
    speaker_cache: Dict[str, List[dict]] = {}
    for cp in sorted(scored_dir.glob("CAND_*.json")):
        with cp.open("r", encoding="utf-8") as f:
            cand = json.load(f)
        cid = cand["candidate_id"]
        v2 = verify_market_v2(
            cand, search_fn=search_fn,
            manifest_speakers=speakers,
            atoms_dir=atoms_dir if atoms_dir.exists() else None,
            semantic_threshold=semantic_threshold,
            today=today,
            speaker_pub_cache=speaker_cache,
        )
        v1_v = v1_verdicts.get(cid, "NOT_REACHED")
        diffs.append({
            "candidate_id": cid,
            "v1_verdict": v1_v,
            "v2_verdict": v2.verdict,
            "v2_primary_keyword": v2.primary_keyword,
            "v2_top_weighted_similarity": v2.top_weighted_similarity,
            "v2_speaker_collisions": [
                {"title": h["title"], "url": h["url"],
                 "matched_speaker": h["matched_speaker"],
                 "weighted_similarity": h["weighted_similarity"]}
                for h in v2.speaker_collisions
            ],
            "v2_semantic_collisions": [
                {"title": h["title"], "url": h["url"],
                 "weighted_similarity": h["weighted_similarity"]}
                for h in v2.semantic_collisions[:5]  # cap
            ],
            "v2_speakers_checked": v2.speakers_checked,
            "diff_class": _diff_class(v1_v, v2.verdict),
        })

    # Bucket
    diff_counts: Dict[str, int] = {}
    for d in diffs:
        diff_counts[d["diff_class"]] = diff_counts.get(d["diff_class"], 0) + 1

    audit = {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "run_dir": str(run_dir),
        "n_candidates": len(diffs),
        "diff_class_distribution": diff_counts,
        "v1_verdict_distribution": _count_field(diffs, "v1_verdict"),
        "v2_verdict_distribution": _count_field(diffs, "v2_verdict"),
        "candidates": diffs,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)
    return audit


def _diff_class(v1: str, v2: str) -> str:
    v1_pass = v1 == "SURVIVES_MARKET_CHECK"
    v2_pass = v2 == VERDICT_SURVIVES
    if v1_pass and not v2_pass:
        return "V2_CATCHES_FALSE_POSITIVE"
    if not v1_pass and v2_pass:
        return "V2_NEW_SURVIVOR"
    if v1_pass and v2_pass:
        return "BOTH_SURVIVE"
    return "BOTH_REJECT"


def _count_field(diffs: List[dict], key: str) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for d in diffs:
        v = d.get(key, "?")
        out[v] = out.get(v, 0) + 1
    return out


# ---- CLI ----

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_verify = sub.add_parser("verify")
    p_verify.add_argument("--scored_dir", required=True, type=Path)
    p_verify.add_argument("--manifest_path", required=True, type=Path)
    p_verify.add_argument("--out_dir", required=True, type=Path)
    p_verify.add_argument("--search_cache_path", type=Path, default=None)
    p_verify.add_argument("--atoms_dir", type=Path, default=None)
    p_verify.add_argument("--speaker_cache_path", type=Path,
                          default=Path("paradigm_shift/speaker_publications_cache.json"))
    p_verify.add_argument("--cross_llm_queue_path", type=Path,
                          default=Path("paradigm_shift/cross_llm_verify_queue.json"))
    p_verify.add_argument("--semantic_threshold", type=float, default=0.5)

    p_audit = sub.add_parser("audit")
    p_audit.add_argument("--run_dir", required=True, type=Path)
    p_audit.add_argument("--manifest_path", required=True, type=Path)
    p_audit.add_argument("--search_cache_path", required=True, type=Path)
    p_audit.add_argument("--out_path", required=True, type=Path)
    p_audit.add_argument("--semantic_threshold", type=float, default=0.5)

    args = ap.parse_args()

    if args.cmd == "verify":
        if args.search_cache_path and args.search_cache_path.exists():
            with args.search_cache_path.open("r", encoding="utf-8") as f:
                cache = json.load(f)
            def search_fn(q): return cache.get(q, [])
        else:
            search_fn = synthesized_market_search_v2
        verdicts = verify_all_v2(
            args.scored_dir, args.manifest_path, args.out_dir,
            search_fn=search_fn,
            atoms_dir=args.atoms_dir,
            semantic_threshold=args.semantic_threshold,
            speaker_cache_path=args.speaker_cache_path,
            cross_llm_queue_path=args.cross_llm_queue_path,
        )
        print(f"verified {len(verdicts)} candidates with Layer 6 v2")
        by_v: Dict[str, int] = {}
        for v in verdicts:
            by_v[v.verdict] = by_v.get(v.verdict, 0) + 1
        for k, n in sorted(by_v.items(), key=lambda x: -x[1]):
            print(f"  {k:40s} {n}")

    elif args.cmd == "audit":
        with args.search_cache_path.open("r", encoding="utf-8") as f:
            cache = json.load(f)
        def search_fn(q): return cache.get(q, [])
        audit = retrospective_audit(
            args.run_dir, args.manifest_path, search_fn,
            args.out_path, semantic_threshold=args.semantic_threshold,
        )
        print(f"retrospective audit wrote to {args.out_path}")
        print(f"diff classes: {audit['diff_class_distribution']}")


if __name__ == "__main__":
    main()

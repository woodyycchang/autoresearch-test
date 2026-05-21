"""First-principles stress test (Layer 5) for Paradigm-Shift Finder v1.

Per candidate:
  Q1: What law/constraint forces this prediction true?
  Q2: What law/constraint would have to bend for the prediction to fail?
  Q3: Atomic decomposition — list 3-5 verifiable sub-claims.
  Q4: For each sub-claim, ground it in >= 1 retrieved web/arXiv source.

Hallucination prevention:
  - RAG: per-sub-claim web_search retrieval, mechanical keyword grounding check
  - Self-consistency: ask Q1+Q2 three times with different framings;
                      reject if the intersection of named principles across
                      all 3 framings is empty
  - Atomic decomposition: each verifiable sub-claim is checked independently

Honest acknowledgment: this layer reduces, but cannot eliminate, hallucination.
RAG snippets are 2-3 sentences and Claude can cherry-pick. Self-consistency-3
catches noise but not systematic hallucination. The mechanical keyword check
is precision-low.

The orchestrator wires real web_search externally; this module receives a
`search_fn` callback that returns the candidate's grounding documents.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple


STOP = {
    "the", "a", "an", "and", "or", "but", "of", "in", "to", "from", "for",
    "with", "by", "on", "at", "is", "are", "was", "were", "be", "been",
    "this", "that", "these", "those", "as", "it", "its", "into", "than",
    "then", "we", "i", "you", "they", "their", "our", "my", "your",
    "would", "could", "should", "will", "can", "may", "might",
    "if", "so", "not", "no", "yes", "okay", "well", "now", "just",
    "going", "also", "talk", "about", "how", "what", "when", "where", "why",
    "have", "has", "had", "do", "does", "did", "say", "said", "let",
}


def content_words(text: str, min_len: int = 4) -> List[str]:
    return [t for t in re.findall(r"[a-z][a-z\-]+", text.lower())
            if t not in STOP and len(t) >= min_len]


# ---- Q1/Q2: principle extraction (3-way self-consistency) ----

# Heuristic noun-phrase extractor for "named principles". Looks for capitalized
# multiword phrases and known physics/math/cs principle vocabulary.
PRINCIPLE_VOCAB = {
    "entropy", "information", "complexity", "scaling", "conservation",
    "thermodynamics", "computation", "bandwidth", "latency", "bottleneck",
    "abstraction", "modularity", "compositionality", "generalization",
    "induction", "deduction", "compression", "expressivity",
    "regularization", "overfitting", "underfitting", "compute",
    "memory", "throughput", "context", "horizon", "asymmetry",
    "feedback", "loop", "interface", "alignment", "specification",
    "robustness", "verifiability", "reproducibility", "falsifiability",
    "no-free-lunch", "moravec", "amdahl",
}


def extract_named_principles(answer: str) -> List[str]:
    """Extract noun-phrase candidates that look like named principles."""
    candidates: List[str] = []
    # Capitalized multiword (e.g., "No Free Lunch", "Bitter Lesson")
    for m in re.finditer(r"\b([A-Z][a-zA-Z\-]+(?:\s+[A-Z][a-zA-Z\-]+){1,4})\b", answer):
        candidates.append(m.group(1).lower())
    # Known principle vocabulary
    text_lower = answer.lower()
    for v in PRINCIPLE_VOCAB:
        if re.search(rf"\b{re.escape(v)}\b", text_lower):
            candidates.append(v)
    # Phrases like "law of X" or "principle of X"
    for m in re.finditer(r"\b(?:law|principle|theorem|conjecture|hypothesis|inequality|bound)\s+(?:of|on)\s+([a-z\-]+(?:\s+[a-z\-]+){0,3})\b", text_lower):
        candidates.append(m.group(1).strip())
    # De-dup, preserve order
    seen = set()
    out = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


# Framing prompts. The orchestrator (or external caller) actually issues these
# to the LLM; this module just defines them and processes the returned answers.
FRAMING_A = (
    "FRAMING A (declarative): State the single principle that, if it holds, "
    "forces this prediction true. Answer in one sentence; name the principle "
    "explicitly."
)

FRAMING_B = (
    "FRAMING B (counterfactual): If this prediction were to fail, which "
    "underlying assumption would have to break? Name the broken assumption "
    "as a single principle."
)

FRAMING_C = (
    "FRAMING C (comparative): Compared to the alternative direction the field "
    "could take, why is THIS prediction privileged? Name the privileging "
    "principle."
)


def self_consistency_principles(
    framing_answers: List[str],
) -> Dict:
    """Given 3 answers (one per framing), return:
        {"intersection": [...], "per_framing": [[principles], [principles], [principles]],
         "stable": bool}
    """
    per_framing = [extract_named_principles(a) for a in framing_answers]
    if not per_framing or any(len(p) == 0 for p in per_framing):
        return {
            "intersection": [],
            "per_framing": per_framing,
            "stable": False,
            "reason": "at_least_one_framing_named_no_principle",
        }
    intersection = set(per_framing[0])
    for p in per_framing[1:]:
        intersection &= set(p)
    return {
        "intersection": sorted(intersection),
        "per_framing": per_framing,
        "stable": len(intersection) > 0,
        "reason": "ok" if intersection else "empty_intersection",
    }


# ---- Q3/Q4: atomic decomposition + per-sub-claim RAG ----

@dataclass
class SubClaim:
    sub_claim_id: str
    text: str
    content_words: List[str]
    search_results: List[dict]
    n_results: int
    n_supporting_results: int
    grounded: bool
    supporting_urls: List[str]


def _is_supporting(sub_claim_text: str, search_result: dict, min_overlap: int = 2) -> Tuple[bool, List[str]]:
    """Mechanical: >=2 content words from sub_claim must appear in title+snippet."""
    blob = (search_result.get("title", "") + " " + search_result.get("snippet", "")).lower()
    sc_words = set(content_words(sub_claim_text))
    overlap = [w for w in sc_words if w in blob]
    return (len(overlap) >= min_overlap, overlap)


def check_sub_claim_grounding(
    sub_claim_text: str,
    sub_claim_id: str,
    search_fn: Callable[[str], List[dict]],
) -> SubClaim:
    cw = content_words(sub_claim_text)
    # Build query from top content words
    query = " ".join(cw[:6])
    results = search_fn(query) or []
    supporting_urls: List[str] = []
    n_supporting = 0
    for r in results:
        ok, _ = _is_supporting(sub_claim_text, r)
        if ok:
            n_supporting += 1
            url = r.get("url", "")
            if url:
                supporting_urls.append(url)
    return SubClaim(
        sub_claim_id=sub_claim_id,
        text=sub_claim_text,
        content_words=cw,
        search_results=results[:5],  # cap stored results
        n_results=len(results),
        n_supporting_results=n_supporting,
        grounded=(n_supporting >= 1),
        supporting_urls=supporting_urls,
    )


# Heuristic decomposer: extracts likely sub-claims from a candidate by splitting
# on commas, "and", and conjunctions, filtering for declarative form.
def heuristic_decompose(candidate: dict) -> List[str]:
    """Produce 3-5 verifiable sub-claims from candidate.

    The honest fallback when no LLM-generated decomposition is provided.
    Splits the claim + first_principles_validity_hypothesis on conjunctions
    and returns deduplicated sentences.
    """
    text = " ".join([
        candidate.get("claim", ""),
        candidate.get("first_principles_validity_hypothesis", ""),
    ])
    # Split on sentence boundaries first, then on conjunctions
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    sub_claims: List[str] = []
    for s in sentences:
        # Sub-split on " and " / " but " / "; "
        parts = re.split(r"\s+(?:and|but)\s+|;\s+", s)
        for p in parts:
            p = p.strip().strip(".")
            if 30 <= len(p) <= 220 and len(content_words(p)) >= 3:
                sub_claims.append(p)
    # De-dup
    seen = set()
    out = []
    for s in sub_claims:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            out.append(s)
    # Cap at 5
    return out[:5]


# ---- Stress-test verdict ----

@dataclass
class StressVerdict:
    candidate_id: str
    verdict: str  # PASS_STRESS | FAIL_RAG_UNGROUNDED | FAIL_UNSTABLE_FIRST_PRINCIPLES | FAIL_NO_SUBCLAIMS
    sub_claims: List[dict]
    self_consistency: dict
    n_sub_claims: int
    n_grounded: int
    rejected_reason: Optional[str]
    timestamp: str


def stress_test_candidate(
    candidate: dict,
    search_fn: Callable[[str], List[dict]],
    framing_answers: Optional[List[str]] = None,
    decompose_fn: Optional[Callable[[dict], List[str]]] = None,
) -> StressVerdict:
    """Run the full stress test on one candidate.

    framing_answers: optional 3-element list of LLM-generated answers to
                     FRAMING_A, FRAMING_B, FRAMING_C. If None, the heuristic
                     uses the candidate's own first_principles_validity_hypothesis
                     three times — which will detect candidates whose hypothesis
                     does not name any principle at all (a useful negative filter)
                     but cannot detect Claude-internal inconsistency.

    decompose_fn:    optional sub-claim decomposer. If None, heuristic_decompose
                     is used.
    """
    cand_id = candidate["candidate_id"]
    decompose_fn = decompose_fn or heuristic_decompose

    # --- Atomic decomposition ---
    sub_claim_texts = decompose_fn(candidate)
    if not sub_claim_texts:
        return StressVerdict(
            candidate_id=cand_id,
            verdict="FAIL_NO_SUBCLAIMS",
            sub_claims=[],
            self_consistency={"intersection": [], "stable": False,
                              "reason": "no_subclaims_to_check"},
            n_sub_claims=0,
            n_grounded=0,
            rejected_reason="decomposer produced 0 sub-claims",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    # --- Per-sub-claim RAG ---
    sub_claims: List[SubClaim] = []
    for i, scx in enumerate(sub_claim_texts, start=1):
        sub_id = f"{cand_id}_SC_{i:02d}"
        sc = check_sub_claim_grounding(scx, sub_id, search_fn)
        sub_claims.append(sc)

    n_grounded = sum(1 for sc in sub_claims if sc.grounded)
    all_grounded = (n_grounded == len(sub_claims))

    # --- Self-consistency ---
    if framing_answers is None:
        # Fallback: triple the candidate's own hypothesis. This catches "no
        # principle named at all" but not inconsistency across framings.
        fa = [candidate.get("first_principles_validity_hypothesis", "")] * 3
    else:
        fa = framing_answers
    sc_result = self_consistency_principles(fa)

    # --- Verdict ---
    if not all_grounded:
        verdict = "FAIL_RAG_UNGROUNDED"
        reason = f"{len(sub_claims) - n_grounded} of {len(sub_claims)} sub-claims ungrounded"
    elif not sc_result["stable"]:
        verdict = "FAIL_UNSTABLE_FIRST_PRINCIPLES"
        reason = sc_result.get("reason", "no_intersection")
    else:
        verdict = "PASS_STRESS"
        reason = None

    return StressVerdict(
        candidate_id=cand_id,
        verdict=verdict,
        sub_claims=[asdict(sc) for sc in sub_claims],
        self_consistency=sc_result,
        n_sub_claims=len(sub_claims),
        n_grounded=n_grounded,
        rejected_reason=reason,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def synthesized_search_callback(query: str) -> List[dict]:
    """Default search callback for runs without a real WebSearch hook.

    Returns an empty list. With this callback, every sub-claim will be
    UNGROUNDED — which makes Run 1's mechanism-validation output explicit:
    the stress test rejects every candidate, demonstrating that the RAG
    layer is binding.

    For real runs, the orchestrator wires a callback that reads from a
    pre-fetched _search_cache.json.
    """
    return []


def stress_test_all(
    candidates_dir: Path,
    out_dir: Path,
    search_fn: Callable[[str], List[dict]] = synthesized_search_callback,
    framing_answers_map: Optional[Dict[str, List[str]]] = None,
) -> List[StressVerdict]:
    """Run stress test on all candidates in candidates_dir.

    framing_answers_map: optional {candidate_id: [answer_A, answer_B, answer_C]}
                         providing real LLM-generated framing answers.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    verdicts: List[StressVerdict] = []

    for cp in sorted(candidates_dir.glob("CAND_*.json")):
        with cp.open("r", encoding="utf-8") as f:
            cand = json.load(f)
        fa = (framing_answers_map or {}).get(cand["candidate_id"])
        v = stress_test_candidate(cand, search_fn=search_fn, framing_answers=fa)
        verdicts.append(v)

        cand["stress_verdict"] = asdict(v)
        out_path = out_dir / cp.name
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(cand, f, indent=2, ensure_ascii=False)

    # _index.json with verdict distribution
    by_verdict: Dict[str, int] = {}
    for v in verdicts:
        by_verdict[v.verdict] = by_verdict.get(v.verdict, 0) + 1

    rejected = [v for v in verdicts if v.verdict != "PASS_STRESS"]
    surviving = [v for v in verdicts if v.verdict == "PASS_STRESS"]

    index = {
        "n_total": len(verdicts),
        "n_pass_stress": len(surviving),
        "n_rejected": len(rejected),
        "verdict_distribution": by_verdict,
        "surviving_ids": [v.candidate_id for v in surviving],
        "rejected_ids": [v.candidate_id for v in rejected],
        "tested_at": datetime.now(timezone.utc).isoformat(),
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    with (out_dir / "_rejected.json").open("w", encoding="utf-8") as f:
        json.dump([
            {"candidate_id": v.candidate_id, "verdict": v.verdict,
             "reason": v.rejected_reason}
            for v in rejected
        ], f, indent=2)

    return verdicts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates_dir", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--search_cache_path", type=Path, default=None,
                    help="Pre-fetched web_search results: {query: [results]}")
    ap.add_argument("--framing_answers_path", type=Path, default=None,
                    help="Pre-fetched framing answers: {candidate_id: [answer_A, answer_B, answer_C]}")
    args = ap.parse_args()

    # Wire search_fn
    if args.search_cache_path and args.search_cache_path.exists():
        with args.search_cache_path.open("r", encoding="utf-8") as f:
            cache = json.load(f)
        def search_fn(q):
            return cache.get(q, [])
    else:
        search_fn = synthesized_search_callback

    framing_map = None
    if args.framing_answers_path and args.framing_answers_path.exists():
        with args.framing_answers_path.open("r", encoding="utf-8") as f:
            framing_map = json.load(f)

    verdicts = stress_test_all(args.candidates_dir, args.out_dir,
                                search_fn=search_fn,
                                framing_answers_map=framing_map)
    print(f"stress tested {len(verdicts)} candidates")
    by_v = {}
    for v in verdicts:
        by_v[v.verdict] = by_v.get(v.verdict, 0) + 1
    for k, n in sorted(by_v.items(), key=lambda x: -x[1]):
        print(f"  {k:38s} {n}")


if __name__ == "__main__":
    main()

"""External verifier for TARI v1.

For each audit-surviving candidate, plug into the existing niche-mining detector
chain (step 06 lit-search, step 13.5 adversarial, step 14.6 external collision).

In v1, we reuse the synthesized detector chain as documented in
program_v20.md, but we ALSO record a flag for whether a real WebSearch was
issued. The real WebSearch is wired through orchestrator.py (which has access
to the WebSearch tool); this module accepts a callback for the search step so
the orchestrator can plug in either a real or synthesized search.

External verification verdict labels (reused from niche-mining):
  - SURVIVES_EXTERNAL_VERIFICATION   (all 3 detectors pass)
  - FAIL_STEP_06_KEYWORD_THRESHOLD   (step 06 found >=2 keyword overlaps)
  - FAIL_STEP_13_5_ADVERSARIAL       (adversarial collapse to baseline)
  - FAIL_STEP_14_6_EXTERNAL_COLLISION (functional similarity to existing work >= 0.7)
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional, Tuple


# ---- Step 06: keyword hit check ----

def extract_content_words(claim: str) -> List[str]:
    """Pull content words from a candidate claim (lowercased, stopword-filtered)."""
    stop = {
        "the", "a", "an", "and", "or", "but", "of", "in", "to", "from", "for",
        "with", "by", "on", "at", "is", "are", "was", "were", "be", "been",
        "this", "that", "these", "those", "as", "it", "its", "into", "than",
        "then", "we", "i", "you", "they", "their", "our", "my", "your",
        "would", "could", "should", "will", "can", "may", "might",
        "if", "so", "not", "no", "yes",
        "atom", "atoms", "snippet", "snippets", "candidate", "speaker",
        "section", "claim", "mechanism", "describes", "described",
    }
    tokens = re.findall(r"[a-z][a-z\-]+", claim.lower())
    return [t for t in tokens if t not in stop and len(t) >= 4]


def step_06_keyword_hits(claim: str, search_results: List[dict], threshold: int = 2) -> dict:
    """Replicate step 07's mechanical keyword threshold from niche-mining."""
    content_words = set(extract_content_words(claim))
    hits = 0
    matched_per_result = []
    for r in search_results:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        blob = (title + " " + snippet).lower()
        overlap = [w for w in content_words if w in blob]
        if len(overlap) >= threshold:
            hits += 1
        matched_per_result.append({
            "title": title[:80],
            "overlap_count": len(overlap),
            "matched_words": overlap[:5],
        })
    return {
        "content_words_extracted": sorted(content_words)[:20],
        "n_content_words": len(content_words),
        "threshold": threshold,
        "n_results_checked": len(search_results),
        "n_results_above_threshold": hits,
        "per_result": matched_per_result,
        "kw_threshold_met": hits >= 1,  # consistent with v20 hit_miss: hit≥1 → FAIL
    }


# ---- Step 13.5: adversarial spec (synthesized) ----

def step_13_5_adversarial(claim: str, candidate: dict) -> dict:
    """Synthesized adversarial. Emulates the program_v20 adversarial-attack format.

    Three categories of attack:
      A1 variant_equivalence: does the candidate collapse to a known baseline at
         some parameter setting?
      A2 test_under_power: does the candidate's empirical claim survive sample size?
      A3 confounded_baseline: is the gain attributable to a confound?

    For v1 we run a rule-based attacker: if the candidate's claim contains a
    phrase suggesting it is a *combination* of existing primitives (per operator),
    A1 is more likely to succeed; the candidate must articulate a clear distinguishability.
    """
    op = candidate.get("combination_operator", "")
    novelty = candidate.get("why_novel_vs_speaker", "")
    # A1: variant equivalence
    a1_succeeds = (
        op in {"COMPOSE", "ANALOGIZE"}
        and len(novelty) < 80
    )
    # A2: test_under_power — succeeds unless candidate has explicit empirical hook
    a2_succeeds = "empirical" not in claim.lower() and "test" not in claim.lower()
    # A3: confounded baseline — succeeds if candidate has no isolation language
    a3_succeeds = "isolate" not in (claim + novelty).lower() and "control" not in (claim + novelty).lower()

    attacks = [
        {"id": "A1", "category": "variant_equivalence", "succeeded": a1_succeeds, "load_bearing": True},
        {"id": "A2", "category": "test_under_power", "succeeded": a2_succeeds, "load_bearing": False},
        {"id": "A3", "category": "confounded_baseline", "succeeded": a3_succeeds, "load_bearing": False},
    ]
    load_bearing_succeeded = any(a["succeeded"] for a in attacks if a["load_bearing"])
    return {
        "attacks": attacks,
        "load_bearing_attack_succeeded": load_bearing_succeeded,
        "spec_survives_attack": not load_bearing_succeeded,
        "honest_note": "Synthesized adversarial. v1 deviation policy reserves real Agent spawn for orchestrator.",
    }


# ---- Step 14.6: external collision check ----

def step_14_6_external_collision(claim: str, search_results: List[dict], threshold: float = 0.7) -> dict:
    """Compute max functional similarity between candidate claim and search results.

    Functional similarity is jaccard over content words (claim, result). This is a
    weak proxy for the program_v16 rubric (mechanism_class_match, etc.) but is
    consistent with the synthesized step 14.6 behavior in program_v20.
    """
    claim_words = set(extract_content_words(claim))
    if not claim_words:
        return {
            "verdict": "SURVIVES",
            "max_functional_similarity": 0.0,
            "rationale": "claim had no content words → trivially survives",
        }
    sims = []
    for r in search_results:
        rwords = set(extract_content_words(r.get("title", "") + " " + r.get("snippet", "")))
        if not rwords:
            sims.append(0.0)
            continue
        inter = claim_words & rwords
        union = claim_words | rwords
        sims.append(len(inter) / max(1, len(union)))
    max_sim = max(sims, default=0.0)
    verdict = "EXTERNAL_COLLISION" if max_sim >= threshold else "SURVIVES"
    return {
        "verdict": verdict,
        "max_functional_similarity": round(max_sim, 3),
        "threshold": threshold,
        "n_results_checked": len(search_results),
        "rationale": (
            f"max functional similarity {max_sim:.3f} "
            f"{'>=' if max_sim >= threshold else '<'} "
            f"{threshold} threshold."
        ),
    }


# ---- Orchestration over candidates ----

@dataclass
class ExternalResult:
    candidate_id: str
    verdict: str
    step_06: dict = field(default_factory=dict)
    step_13_5: dict = field(default_factory=dict)
    step_14_6: dict = field(default_factory=dict)
    real_websearch_issued: bool = False
    websearch_results_count: int = 0
    notes: List[str] = field(default_factory=list)
    timestamp: str = ""


SearchCallable = Callable[[str], List[dict]]


def synthesized_search_callback(query: str) -> List[dict]:
    """Default synthesized search — returns empty results.

    In v1, this is the conservative default: synthesized search returns no
    results, which means step 06 and 14.6 trivially survive. The honest
    framing: if external verification is going to find anything, it must be
    a *real* search via the orchestrator's WebSearch wiring.

    This is consistent with program_v20's main-context-direct synthesized
    behavior (step 06 / 14.6 produce empty / near-empty results unless an
    Agent is spawned). We do not pretend the synthesized step finds real
    collisions.
    """
    return []


def verify_candidate(
    candidate: dict,
    search_fn: SearchCallable = synthesized_search_callback,
    record_real_websearch: bool = False,
    atom_text_for_keywords: str = "",
) -> ExternalResult:
    claim = candidate.get("claim", "")
    # Build a search query: content words joined.
    cw = extract_content_words(claim)[:8]
    query = " ".join(cw) if cw else claim[:100]

    search_results = search_fn(query)

    # Step 06 keyword check is done against the ATOM content (the actual research
    # substance of the candidate), not the brainstorm template text. The template
    # text contains words like "compose primitive primitive" that pollute the
    # content-word signal. atom_text_for_keywords is supplied by the orchestrator.
    keyword_basis = atom_text_for_keywords if atom_text_for_keywords else claim
    step06 = step_06_keyword_hits(keyword_basis, search_results)
    step135 = step_13_5_adversarial(claim, candidate)
    step146 = step_14_6_external_collision(keyword_basis, search_results)

    fail_reasons = []
    if step06.get("kw_threshold_met"):
        fail_reasons.append("FAIL_STEP_06_KEYWORD_THRESHOLD")
    if not step135.get("spec_survives_attack"):
        fail_reasons.append("FAIL_STEP_13_5_ADVERSARIAL")
    if step146.get("verdict") == "EXTERNAL_COLLISION":
        fail_reasons.append("FAIL_STEP_14_6_EXTERNAL_COLLISION")

    verdict = "SURVIVES_EXTERNAL_VERIFICATION" if not fail_reasons else fail_reasons[0]

    return ExternalResult(
        candidate_id=candidate["candidate_id"],
        verdict=verdict,
        step_06=step06,
        step_13_5=step135,
        step_14_6=step146,
        real_websearch_issued=record_real_websearch,
        websearch_results_count=len(search_results),
        notes=([] if not fail_reasons else [f"failed_reasons: {fail_reasons}"]),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def verify_all(
    candidates_dir: Path,
    audit_results: List[dict],
    out_path: Path,
    search_fn: SearchCallable = synthesized_search_callback,
    real_websearch_used: bool = False,
) -> List[ExternalResult]:
    """Run external verification on candidates whose audit verdict starts with PASS."""
    pass_audit_ids = {r["candidate_id"] for r in audit_results
                      if r.get("verdict", "").startswith("PASS")}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    results = []
    for cp in sorted(candidates_dir.glob("CAND_*.json")):
        with cp.open("r", encoding="utf-8") as f:
            cand = json.load(f)
        if cand["candidate_id"] not in pass_audit_ids:
            continue
        r = verify_candidate(cand, search_fn=search_fn, record_real_websearch=real_websearch_used)
        results.append(r)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump({
            "n_candidates_verified": len(results),
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "results": [asdict(r) for r in results],
            "verdict_distribution": {
                v: sum(1 for r in results if r.verdict == v)
                for v in {r.verdict for r in results}
            },
        }, f, indent=2, ensure_ascii=False)
    return results


def main():
    """Standalone runner (synthesized search only). Orchestrator wires real search."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates_dir", required=True, type=Path)
    ap.add_argument("--audit_path", required=True, type=Path)
    ap.add_argument("--out_path", required=True, type=Path)
    args = ap.parse_args()
    with args.audit_path.open("r", encoding="utf-8") as f:
        audit = json.load(f)
    results = verify_all(
        args.candidates_dir,
        audit["results"],
        args.out_path,
        search_fn=synthesized_search_callback,
        real_websearch_used=False,
    )
    print(f"verified {len(results)} candidates (synthesized search)")
    verdicts = {}
    for r in results:
        verdicts[r.verdict] = verdicts.get(r.verdict, 0) + 1
    for v, n in sorted(verdicts.items()):
        print(f"  {v:50s} {n}")


if __name__ == "__main__":
    main()

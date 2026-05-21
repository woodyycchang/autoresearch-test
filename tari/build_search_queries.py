"""Construct better search queries for TARI candidates.

The brainstorm engine produces template-heavy candidate.claim text that is poor
search input. Better queries come from extracting *content* words from the
cited atoms' verbatim_quote fields, not from the template claim text.

This module produces one search query per candidate, written to a JSON file
that the orchestrator can re-load and feed into real WebSearch wired separately.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import List


STOP = {
    "the", "a", "an", "and", "or", "but", "of", "in", "to", "from", "for",
    "with", "by", "on", "at", "is", "are", "was", "were", "be", "been",
    "this", "that", "these", "those", "as", "it", "its", "into", "than",
    "then", "we", "i", "you", "they", "their", "our", "my", "your",
    "would", "could", "should", "will", "can", "may", "might",
    "if", "so", "not", "no", "yes", "okay", "well", "now", "just",
    "going", "also", "talk", "about", "how", "what", "when", "where", "why",
    "really", "very", "much", "many", "some", "other", "another",
    "have", "has", "had", "do", "does", "did", "say", "said", "let",
    "thing", "things", "way", "ways", "kind", "sort",
    "actually", "basically", "essentially", "literally",
    "first", "second", "third", "next", "last",
    "here", "there", "everyone", "everyone",
    "right", "left", "good", "bad", "better", "best",
}

# Tokens that look like research vocabulary worth keeping even though stopword-adjacent
PRESERVE = {
    "world", "user", "self", "models", "model", "coherence", "updatability",
    "probing", "patching", "activation", "transformer", "attention",
    "test", "time", "training", "context", "language", "POMDP", "Bayesian",
    "scaling", "law", "reasoning", "tokens", "parameters",
    "skill", "graph", "skillet", "weak", "supervision", "GATE", "OPEN",
    "preference", "elicitation", "sycophancy", "explanation", "faithful",
    "particle", "filter", "posterior", "advantage", "reward", "surrogate",
    "meta", "rl", "policy", "exploration", "exploitation",
    "auxiliary", "data", "off-policy", "on-policy",
    "kernel", "engineering", "verifier", "verification",
}


def content_words(text: str, max_n: int = 12) -> List[str]:
    tokens = re.findall(r"[a-z][a-z\-]+", text.lower())
    out = []
    seen = set()
    for t in tokens:
        if (t in STOP) and (t not in PRESERVE):
            continue
        if len(t) < 4 and t not in PRESERVE:
            continue
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
        if len(out) >= max_n:
            break
    return out


def build_query_for_candidate(candidate_path: Path, atoms_dir: Path) -> dict:
    with candidate_path.open("r", encoding="utf-8") as f:
        cand = json.load(f)
    atoms = []
    for aid in cand["combined_atom_ids"]:
        with (atoms_dir / f"{aid}.json").open("r", encoding="utf-8") as f:
            atoms.append(json.load(f))
    # Pull content words from each atom verbatim quote
    per_atom_words = [content_words(a["verbatim_quote"], max_n=6) for a in atoms]
    # Build a compound query: top words from each atom, comma-separated as conjunction
    # Use top 3 per atom for a focused query
    words = []
    for ws in per_atom_words:
        words.extend(ws[:4])
    # Dedup, preserving order
    seen = set()
    final = []
    for w in words:
        if w not in seen:
            seen.add(w)
            final.append(w)
        if len(final) >= 8:
            break

    # Add operator-flavored framing to make the search reflect the proposed combination
    op_phrase = {
        "ANALOGIZE": "analogy transfer",
        "INVERT": "reverse direction",
        "COMPOSE": "composition combined",
        "GENERALIZE": "generalization",
        "RESTRICT": "boundary case",
        "CONTRAST": "comparison contrast",
    }.get(cand["combination_operator"], "")

    query = " ".join(final + ([op_phrase] if op_phrase else []))
    return {
        "candidate_id": cand["candidate_id"],
        "operator": cand["combination_operator"],
        "atom_ids": cand["combined_atom_ids"],
        "atom_top_words": per_atom_words,
        "query": query,
        "atom_quotes_preview": [a["verbatim_quote"][:160] for a in atoms],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates_dir", required=True, type=Path)
    ap.add_argument("--atoms_dir", required=True, type=Path)
    ap.add_argument("--audit_path", required=True, type=Path)
    ap.add_argument("--out_path", required=True, type=Path)
    args = ap.parse_args()
    with args.audit_path.open("r", encoding="utf-8") as f:
        audit = json.load(f)
    pass_ids = {r["candidate_id"] for r in audit["results"]
                if r["verdict"].startswith("PASS")}
    queries = []
    for cp in sorted(args.candidates_dir.glob("CAND_*.json")):
        with cp.open("r", encoding="utf-8") as f:
            cand = json.load(f)
        if cand["candidate_id"] not in pass_ids:
            continue
        queries.append(build_query_for_candidate(cp, args.atoms_dir))
    args.out_path.parent.mkdir(parents=True, exist_ok=True)
    with args.out_path.open("w", encoding="utf-8") as f:
        json.dump({"n_queries": len(queries), "queries": queries}, f, indent=2)
    print(f"built {len(queries)} queries")
    for q in queries:
        print(f"  {q['candidate_id']:18s} {q['query']}")


if __name__ == "__main__":
    main()

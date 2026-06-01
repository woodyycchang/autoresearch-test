#!/usr/bin/env python3
"""Run 16 AGENT 5 (search-quality scorer) helper.

Deterministically scores every search query the pipeline used this epoch
(AGENT 1's atom-sourcing queries + AGENT 3's prior-art reformulations) against
the five direction dimensions, and computes a param-weighted avg_search_quality
that is the per-epoch improvement metric (R10, R12).

This is pure text heuristics — no I/O, no LLM — so the score is reproducible and
the epoch-over-epoch delta is trustworthy.

Reads : paradigm_shift/run_016/direction_params.json   (current params/weights)
        paradigm_shift/run_016/logs/atoms.json          (AGENT 1: queries_used)
        paradigm_shift/run_016/logs/verify.json         (AGENT 3: reformulations)
Writes: paradigm_shift/run_016/logs/search_quality.json

Usage: python3 paradigm_shift/run16_scorer.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN_DIR = Path(__file__).parent / "run_016"
LOGS = RUN_DIR / "logs"

# param key (in direction_params) -> the per-query dimension it is scored from.
# atom_source_diversity is epoch-level (scored from the atom set, not per query).
PARAM_TO_DIM = {
    "reformulation_specificity": "specificity",
    "mechanism_focus": "mechanism_focus",
    "cross_domain_reach": "cross_domain_reach",
    "collision_avoidance_phrasing": "collision_avoidance",
    "atom_source_diversity": "atom_source_diversity",
}

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "does", "can",
    "are", "was", "has", "have", "not", "but", "via", "per", "its", "use",
    "used", "using", "how", "what", "which", "based", "new", "novel", "a", "an",
    "of", "to", "in", "on", "or", "is", "do", "vs", "any",
}
MECH_TERMS = {
    "routing", "route", "routes", "gate", "gating", "induce", "induces", "induced",
    "activate", "activates", "gradient", "precondition", "preconditioned",
    "preconditioning", "normalize", "normalization", "normalized", "regularize",
    "optimizer", "optimization", "attention", "convergence", "converge", "sparse",
    "sparsity", "expert", "experts", "memory", "retrieval", "mechanism",
    "distill", "synthesize", "synthesis", "selects", "select", "scaling",
}
PRIOR_ART_TERMS = {
    "existing", "prior", "previous", "survey", "review", "literature", "already",
    "benchmark", "baseline", "compare", "comparison", "related", "state-of-the-art",
}
PRIOR_ART_PHRASES = ("state of the art", "has been", "have been", "prior work",
                     "related work", "already been")
FIELD_LEX = {
    "ml": {"attention", "transformer", "llm", "llms", "neural", "gradient",
           "optimizer", "training", "token", "tokens", "expert", "experts",
           "routing", "inference", "moe", "adam"},
    "bio": {"gene", "genetic", "neuron", "dopamine", "biological", "protein",
            "cell", "brain", "regulatory", "developmental", "evolutionary"},
    "physics": {"thermodynamic", "energy", "phase", "quantum", "entropy",
                "oscillation", "resonance", "acoustic", "metamaterial"},
    "math": {"convex", "manifold", "topology", "spectral", "eigen", "matrix",
             "transport", "theorem", "stochastic", "bayesian"},
    # low-ML-overlap domains (epoch-3 directive): distinctive vocab so a query that
    # names an ML concept AND one of these registers as cross-domain (>=2 fields).
    "geology": {"seismic", "seismology", "tectonic", "sediment", "sedimentary",
                "erosion", "geomorphology", "magma", "stratigraphy", "lithosphere",
                "geological", "geology", "rupture", "subduction"},
    "linguistics": {"phonology", "phoneme", "phonological", "morpheme", "morphological",
                    "syntax", "sonority", "prosody", "phonetic", "vowel", "consonant",
                    "linguistic", "linguistics", "phonotactic"},
    "materials": {"crystal", "crystalline", "dislocation", "lattice", "alloy",
                  "nucleation", "microstructure", "ceramic", "metallurgy", "grain",
                  "metallurgical", "crystallization"},
    "ecology": {"ecosystem", "trophic", "predator", "prey", "biodiversity", "habitat",
                "foraging", "ecological", "ecology", "food-web", "pollinator"},
}


def tokens(q: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z\-]+", (q or "").lower())


def score_query(q: str) -> dict:
    toks = tokens(q)
    cw = [t for t in toks if len(t) >= 4 and t not in STOPWORDS]
    ql = (q or "").lower()
    # specificity: rich content + technical markers (digits, hyphenation, quotes)
    tech = (sum(1 for t in re.findall(r"\S+", q or "") if any(c.isdigit() for c in t))
            + sum(1 for t in toks if "-" in t) + (q or "").count('"') // 2)
    specificity = round(0.5 * min(1.0, len(cw) / 6.0) + 0.5 * min(1.0, tech / 2.0), 4)
    # mechanism focus
    mech = sum(1 for t in toks if t in MECH_TERMS)
    mechanism_focus = round(min(1.0, mech / 2.0), 4)
    # cross-domain reach: distinct fields the query touches (1 field -> 0.0).
    # Split hyphenated compounds so "mixture-of-experts" also matches "experts".
    ftoks = set(toks)
    for t in toks:
        if "-" in t:
            ftoks.update(t.split("-"))
    fields = {f for f, lex in FIELD_LEX.items() if any(t in lex for t in ftoks)}
    cross_domain_reach = round(min(1.0, max(0, len(fields) - 1) / 2.0), 4)
    # collision-avoidance phrasing: prior-art probing terms/phrases
    pa = sum(1 for t in toks if t in PRIOR_ART_TERMS) + sum(ql.count(p) for p in PRIOR_ART_PHRASES)
    collision_avoidance = round(min(1.0, pa / 2.0), 4)
    return {"specificity": specificity, "mechanism_focus": mechanism_focus,
            "cross_domain_reach": cross_domain_reach,
            "collision_avoidance": collision_avoidance}


def atom_source_diversity(atoms: list[dict]) -> float:
    if not atoms:
        return 0.0
    tags = set()
    for a in atoms:
        for t in a.get("domain_tags", []) or []:
            tags.add(str(t).lower())
        tags.add(str(a.get("arxiv_id", a.get("url", ""))))  # distinct sources
    distinct_domains = len({t for a in atoms for t in (a.get("domain_tags", []) or [])})
    # diversity = distinct domain tags relative to number of atoms (capped 1.0)
    return round(min(1.0, distinct_domains / max(1, len(atoms))), 4)


def main() -> int:
    dp = json.loads((RUN_DIR / "direction_params.json").read_text())
    params = dp["search_quality_params"]
    atoms_doc = json.loads((LOGS / "atoms.json").read_text())
    atoms = atoms_doc.get("atoms", [])
    verify = json.loads((LOGS / "verify.json").read_text())

    per_query = []
    for q in atoms_doc.get("queries_used", []):
        per_query.append({"source": "agent1_sourcer", "cand_id": None,
                          "query": q, "dims": score_query(q)})
    for c in verify.get("candidates", []):
        for rf in c.get("reformulations", []):
            per_query.append({"source": "agent3_verifier", "cand_id": c["cand_id"],
                              "query": rf.get("query", ""), "dims": score_query(rf.get("query", ""))})

    # epoch-level dimension means (per the 5 param keys)
    def dim_mean(dimkey):
        vals = [pq["dims"][dimkey] for pq in per_query]
        return round(sum(vals) / len(vals), 4) if vals else 0.0

    diversity = atom_source_diversity(atoms)
    dimension_means = {
        "reformulation_specificity": dim_mean("specificity"),
        "mechanism_focus": dim_mean("mechanism_focus"),
        "cross_domain_reach": dim_mean("cross_domain_reach"),
        "atom_source_diversity": diversity,
        "collision_avoidance_phrasing": dim_mean("collision_avoidance"),
    }
    # avg_search_quality = param-weighted average of the 5 dimension means
    wsum = sum(params.values()) or 1.0
    avg = round(sum(params[k] * dimension_means[k] for k in params) / wsum, 4)

    out = {
        "run_id": "run_016", "epoch": dp["epoch"],
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "params_used": params,
        "n_queries": len(per_query),
        "per_query": per_query,
        "dimension_means": dimension_means,
        "avg_search_quality": avg,
        "note": ("avg_search_quality = sum(param_k * dimension_mean_k)/sum(param_k); "
                 "dimension scores are deterministic text heuristics over the real "
                 "queries AGENT 1 and AGENT 3 used this epoch."),
    }
    (LOGS / "search_quality.json").write_text(json.dumps(out, indent=2))
    print(f"[scorer] {len(per_query)} queries scored; avg_search_quality={avg}")
    for k, v in dimension_means.items():
        print(f"   {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

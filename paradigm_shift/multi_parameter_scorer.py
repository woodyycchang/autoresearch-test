"""Multi-parameter scorer for Run 11.

For each candidate (2-atom pair), computes 10 scalar parameters in [0,1] that
together mimick a consistent human RLHF labeler. composite_score is the
RLHF-weight-weighted sum, with the weights read live from rlhf_weights.json
so that scoring strictness evolves epoch-to-epoch.

Pure-Python, deterministic. The arXiv-hit counts and saturation-cluster
distances are supplied by the harness (it issues the real WebSearch calls);
the scorer only does the arithmetic of decomposition.

Parameters (all in [0,1]):
  1. atom_quality_score             technical mechanism present, no fillers
  2. novelty_score                  inverse of arXiv hit count over 24m
  3. cross_source_diversity         atoms span different source types
  4. mechanism_coherence            mechanism-vocab overlap between atoms
  5. saturation_distance            distance from RLHF/JEPA/MoE/RAG/SAE cluster
  6. speaker_self_publish_risk      1 - self-publish overlap   (higher is better)
  7. arxiv_grounding                # supporting citations, normalized
  8. belinda_audit_pass             1.0 if 3Q mechanical pass
  9. community_density              1 - normalized recent paper count
 10. cross_disciplinary_bonus       1.0 if atoms span ML + non-ML
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Iterable

THIS_DIR = Path(__file__).parent
RLHF_WEIGHTS_PATH = THIS_DIR / "rlhf_weights.json"

# ---------- Vocabularies shared with Run 10 mechanism check ----------
MECHANISM_VOCAB_ML = {
    "gradient", "attention", "reward", "memory", "routing", "embedding",
    "prediction", "loss", "policy", "value", "tokenization", "context",
    "regularization", "sparsity", "compression", "alignment", "preference",
    "trajectory", "sampling", "decoding", "inference", "training",
}
MECHANISM_VOCAB_CROSSDISC = {
    "selection_pressure", "energy_constraint", "market_clearing",
    "body_world_coupling", "cognitive_function", "data_efficiency",
    "system_architecture",
}
MECHANISM_VOCAB_ALL = MECHANISM_VOCAB_ML | MECHANISM_VOCAB_CROSSDISC

KNOWN_SATURATED_NICHES = {
    "rlhf", "jepa", "moe", "rag", "sae", "constitutional", "dpo",
    "in_context_learning", "chain_of_thought", "world_models",
    "scaling_laws", "mechanistic_interpretability", "retrieval_augmented",
    "agent_pipeline", "agent_efficiency", "model_native_agents",
}

FILLER_WORDS = {"basically", "obviously", "literally", "kind of", "sort of",
                "you know", "i mean", "right?", "okay so"}

SELF_PUBLISH_PHRASES = {
    "our paper", "our method", "our approach", "in this work",
    "we propose", "we present", "we introduce", "our results show",
    "as we show", "our experiments demonstrate",
}

# Source-type classification for cross_source_diversity
SOURCE_TYPES_KNOWN = {
    "essay", "blog", "transcript", "arxiv", "hn_post", "company_news",
    "search_result", "patent", "tweet", "podcast",
}

# Non-ML domain vocab (for cross_disciplinary_bonus)
NON_ML_DOMAIN_VOCAB = {
    "biology", "evolution", "evodevo", "neuroscience", "neural_organoid",
    "thermodynamics", "energy", "entropy", "market", "auction", "economics",
    "mechanism_design", "physics", "fluid", "history", "psychology",
    "sociology", "manufacturing", "supply_chain", "ecology", "ethics",
    "literature", "philosophy",
}


@dataclass
class Atom:
    atom_id: str
    source_id: str
    source_type: str           # essay / blog / transcript / arxiv / hn_post / company_news / search_result
    speaker_or_author: str
    text: str
    atom_type: str             # first_principle / mechanism / prediction / observation
    domain_tags: List[str] = field(default_factory=list)


@dataclass
class Candidate:
    cand_id: str
    atom_a: Atom
    atom_b: Atom
    joint_topic: str
    arxiv_hit_count_24m: Optional[int] = None         # supplied by harness
    recent_paper_count: Optional[int] = None          # supplied by harness
    saturation_cluster_distance: Optional[float] = None  # supplied by harness
    arxiv_citations_supporting: List[str] = field(default_factory=list)
    belinda_3q_passes: Optional[bool] = None          # supplied by harness


# ---------- Per-parameter scoring functions ----------
def score_atom_quality(c: Candidate) -> float:
    """Mean of per-atom quality (mechanism present, low filler)."""
    def _atom_q(a: Atom) -> float:
        t = a.text.lower()
        mech_present = any(v in t for v in MECHANISM_VOCAB_ALL)
        filler_count = sum(1 for f in FILLER_WORDS if f in t)
        non_trivial_len = 1.0 if len(t.split()) >= 8 else 0.5
        base = 0.0
        if mech_present:
            base += 0.6
        base += 0.4 * non_trivial_len
        # Penalize fillers
        base -= 0.1 * min(filler_count, 3)
        return max(0.0, min(1.0, base))

    return 0.5 * (_atom_q(c.atom_a) + _atom_q(c.atom_b))


def score_novelty(c: Candidate) -> float:
    """Inverse of arXiv hit count (24m). 0 hits -> 1.0; >=20 -> 0.0."""
    n = c.arxiv_hit_count_24m if c.arxiv_hit_count_24m is not None else 10
    if n <= 0:
        return 1.0
    return max(0.0, 1.0 - math.log1p(n) / math.log1p(20))


def score_cross_source_diversity(c: Candidate) -> float:
    return 1.0 if c.atom_a.source_type != c.atom_b.source_type else 0.2


def score_mechanism_coherence(c: Candidate) -> float:
    """Overlap of mechanism vocab between the two atoms (Jaccard, lightly normalized)."""
    ta = set(re.findall(r"[a-zA-Z_]+", c.atom_a.text.lower()))
    tb = set(re.findall(r"[a-zA-Z_]+", c.atom_b.text.lower()))
    mech_a = ta & MECHANISM_VOCAB_ALL
    mech_b = tb & MECHANISM_VOCAB_ALL
    if not mech_a and not mech_b:
        return 0.0
    if not (mech_a | mech_b):
        return 0.0
    jaccard = len(mech_a & mech_b) / max(1, len(mech_a | mech_b))
    # We want SOME overlap but not identical — sweet spot 0.25-0.5
    if jaccard == 0:
        return 0.2  # disjoint mechanisms = weak coherence
    if jaccard >= 0.5:
        return 0.6 + 0.4 * (1 - abs(jaccard - 0.4) / 0.6)
    return 0.4 + jaccard


def score_saturation_distance(c: Candidate) -> float:
    """Higher = further from known niches. Uses keyword distance + harness-provided cluster distance."""
    text = (c.atom_a.text + " " + c.atom_b.text + " " + c.joint_topic).lower()
    hits = sum(1 for n in KNOWN_SATURATED_NICHES if n.replace("_", " ") in text or n in text)
    keyword_dist = max(0.0, 1.0 - hits * 0.2)
    if c.saturation_cluster_distance is not None:
        return 0.5 * keyword_dist + 0.5 * c.saturation_cluster_distance
    return keyword_dist


def score_speaker_self_publish_risk(c: Candidate) -> float:
    """1.0 = no self-publish phrasing. Lower if either atom uses 'our paper' etc."""
    def _risk(a: Atom) -> float:
        t = a.text.lower()
        hits = sum(1 for p in SELF_PUBLISH_PHRASES if p in t)
        return min(1.0, hits * 0.3)
    risk = 0.5 * (_risk(c.atom_a) + _risk(c.atom_b))
    return 1.0 - risk


def score_arxiv_grounding(c: Candidate) -> float:
    """Normalized count of supporting arXiv citations, capped at 5."""
    n = len(c.arxiv_citations_supporting)
    return min(1.0, n / 5.0)


def score_belinda_audit_pass(c: Candidate) -> float:
    if c.belinda_3q_passes is None:
        return 0.5  # untested -> neutral
    return 1.0 if c.belinda_3q_passes else 0.0


def score_community_density(c: Candidate) -> float:
    """1 - normalized recent paper count. <=2 papers -> 1.0; >=30 -> 0."""
    n = c.recent_paper_count if c.recent_paper_count is not None else 10
    if n <= 0:
        return 1.0
    return max(0.0, 1.0 - math.log1p(n) / math.log1p(30))


def score_cross_disciplinary_bonus(c: Candidate) -> float:
    """1.0 if one atom is ML and the other is non-ML."""
    def _is_non_ml(a: Atom) -> bool:
        text = a.text.lower()
        return any(d in text or d in " ".join(a.domain_tags).lower()
                   for d in NON_ML_DOMAIN_VOCAB)
    a_non = _is_non_ml(c.atom_a)
    b_non = _is_non_ml(c.atom_b)
    if a_non != b_non:
        return 1.0
    if a_non and b_non:
        return 0.5  # both non-ML = still interesting
    return 0.0


PARAM_FUNCS = {
    "atom_quality_score": score_atom_quality,
    "novelty_score": score_novelty,
    "cross_source_diversity": score_cross_source_diversity,
    "mechanism_coherence": score_mechanism_coherence,
    "saturation_distance": score_saturation_distance,
    "speaker_self_publish_risk": score_speaker_self_publish_risk,
    "arxiv_grounding": score_arxiv_grounding,
    "belinda_audit_pass": score_belinda_audit_pass,
    "community_density": score_community_density,
    "cross_disciplinary_bonus": score_cross_disciplinary_bonus,
}


def load_weights() -> Dict[str, float]:
    with open(RLHF_WEIGHTS_PATH) as f:
        return json.load(f)["weights"]


def score_candidate(c: Candidate, weights: Optional[Dict[str, float]] = None) -> Dict:
    """Return per-parameter scores + weighted composite."""
    if weights is None:
        weights = load_weights()
    params: Dict[str, float] = {name: fn(c) for name, fn in PARAM_FUNCS.items()}
    composite = sum(weights.get(name, 0.0) * v for name, v in params.items())
    return {
        "cand_id": c.cand_id,
        "joint_topic": c.joint_topic,
        "atom_a_id": c.atom_a.atom_id,
        "atom_b_id": c.atom_b.atom_id,
        "params": params,
        "weights_used": dict(weights),
        "composite_score": round(composite, 4),
        "rlhf_label_simulated": _label_from_composite(composite),
        "scored_at": datetime.now(timezone.utc).isoformat(),
    }


def _label_from_composite(c: float) -> int:
    """Mimics a 1-5 human label from composite score."""
    if c < 0.2:
        return 1
    if c < 0.4:
        return 2
    if c < 0.6:
        return 3
    if c < 0.8:
        return 4
    return 5


def score_candidates_for_epoch(candidates: Iterable[Candidate],
                               output_dir: Path,
                               weights: Optional[Dict[str, float]] = None) -> List[Dict]:
    output_dir.mkdir(parents=True, exist_ok=True)
    weights = weights or load_weights()
    out: List[Dict] = []
    for c in candidates:
        s = score_candidate(c, weights)
        out.append(s)
        with open(output_dir / f"{c.cand_id}.json", "w") as f:
            json.dump(s, f, indent=2)
    # composite summary
    out.sort(key=lambda x: x["composite_score"], reverse=True)
    with open(output_dir / "_summary.json", "w") as f:
        json.dump({
            "n_candidates": len(out),
            "mean_composite": round(sum(s["composite_score"] for s in out) / max(1, len(out)), 4),
            "max_composite": max((s["composite_score"] for s in out), default=0.0),
            "min_composite": min((s["composite_score"] for s in out), default=0.0),
            "ranked": [{"cand_id": s["cand_id"], "composite_score": s["composite_score"],
                        "joint_topic": s["joint_topic"]} for s in out],
        }, f, indent=2)
    return out


SURVIVOR_THRESHOLD = 0.7


def split_survivors(scores: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    surv = [s for s in scores if s["composite_score"] >= SURVIVOR_THRESHOLD]
    rej = [s for s in scores if s["composite_score"] < SURVIVOR_THRESHOLD]
    return surv, rej


if __name__ == "__main__":
    # Smoke test
    a = Atom("ATOM_A", "src1", "essay", "pg", "Wood is a renewable mechanism for energy.", "first_principle", ["history"])
    b = Atom("ATOM_B", "src2", "arxiv", "anon", "Gradient descent is a routing mechanism for loss minimization.", "mechanism", ["ml"])
    c = Candidate("CAND_TEST", a, b, "wood_and_gradient",
                  arxiv_hit_count_24m=0, recent_paper_count=1,
                  saturation_cluster_distance=0.9,
                  arxiv_citations_supporting=["x", "y"],
                  belinda_3q_passes=True)
    print(json.dumps(score_candidate(c), indent=2))

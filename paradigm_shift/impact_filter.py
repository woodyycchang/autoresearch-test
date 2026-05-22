"""Impact filter for Paradigm-Shift Finder v1.

Per-candidate 4-axis scoring with a trainable classifier on top.

Axes:
    time_horizon          (0..15 years; preferred 3-10)
    impact_scale          (0..10; log10 of estimated affected entities)
    poc_tractability      (0..1; solo-founder buildable in 3-6 months)
    information_asymmetry (0..1; Claude-knows-but-market-doesn't ratio)

Initial heuristic weights (Run 1):
    predicted_impact = sigmoid(
        + W_TH * (1 - |time_horizon - 6| / 9)        # peak at 6 years
        + W_IS * (impact_scale / 10)
        + W_PT * poc_tractability
        + W_IA * information_asymmetry
    )

After 10+ user labels accumulate in impact_labels.json, the weights are
refit via logistic regression. The fitted coefficients are persisted to
impact_filter_weights.json and override the heuristic defaults.

Honest deviation: scoring axes 1-3 are estimated heuristically here
without an oracle. The user must label candidates over multiple runs
for the classifier to become useful. Run 1 ships with the heuristic
weights only.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple


# ---- Initial heuristic weights ----

W_TH = 0.30  # time horizon
W_IS = 0.30  # impact scale
W_PT = 0.20  # POC tractability
W_IA = 0.20  # information asymmetry


HEURISTIC_WEIGHTS = {
    "intercept": -0.5,
    "time_horizon": W_TH,
    "impact_scale": W_IS,
    "poc_tractability": W_PT,
    "information_asymmetry": W_IA,
}


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


# ---- Heuristic axis estimators ----

# Solo-founder-friendly keywords: things a solo founder can build without
# hardware budget / data partnerships / specialty wet labs.
SOLO_FRIENDLY = {
    "browser", "web", "app", "api", "prompt", "wrapper", "chatbot", "agent",
    "ui", "ux", "extension", "tool", "cli", "library", "wrapper", "interface",
    "frontend", "saas", "service", "workflow",
}

SOLO_HOSTILE = {
    "cluster", "datacenter", "wafer", "fab", "reactor", "satellite", "biolab",
    "biological", "wet", "clinical", "fda", "trial", "asic", "tpu", "gpu",
    "supercomputer", "fleet", "logistics", "hardware", "robot", "robotic",
    "petabyte", "exabyte", "fundamental", "physics", "drug", "molecule",
}


# Impact-scale lexicon: rough estimate of affected entities by topic keywords.
# log10 scale: 0=10 entities, 1=100, ..., 10=10B+ (global population).
IMPACT_KEYWORDS = {
    # Global / billions
    "everyone": 10, "humanity": 10, "global": 9, "billion": 9,
    "world": 8, "all developers": 8, "consumers": 8,
    # Hundreds of millions
    "users": 7, "students": 7, "workers": 7, "professionals": 6,
    # Tens of millions
    "researchers": 6, "engineers": 6, "scientists": 6,
    # Millions
    "enterprises": 5, "companies": 5, "businesses": 5, "doctors": 5,
    # Thousands
    "startups": 4, "founders": 4, "labs": 4, "investors": 4,
    # Hundreds
    "elite": 3, "frontier": 3,
}


def estimate_time_horizon(candidate: dict, default: float = 5.0) -> float:
    """Years until prediction materializes. Look at target_date relative to today,
    else fall back to default.
    """
    target = candidate.get("target_date")
    if not target:
        return default
    try:
        td = datetime.fromisoformat(target.replace("Z", "+00:00")) if "T" in target else datetime.fromisoformat(target + "T00:00:00+00:00")
    except (ValueError, TypeError):
        return default
    now = datetime.now(timezone.utc)
    delta_years = (td - now).days / 365.0
    return max(0.0, min(15.0, delta_years))


def estimate_impact_scale(candidate: dict, default: float = 5.0) -> float:
    """Heuristic: scan candidate.claim and atom quotes for impact-scale keywords."""
    text = candidate.get("claim", "").lower()
    text += " " + candidate.get("first_principles_validity_hypothesis", "").lower()
    text += " " + candidate.get("why_potentially_useful", "").lower()
    max_score = default
    for kw, score in IMPACT_KEYWORDS.items():
        if kw in text:
            max_score = max(max_score, float(score))
    return max_score


def estimate_poc_tractability(candidate: dict, default: float = 0.5) -> float:
    """0..1, higher means more solo-founder buildable."""
    text = " ".join([
        candidate.get("claim", ""),
        candidate.get("first_principles_validity_hypothesis", ""),
        candidate.get("why_potentially_useful", ""),
    ]).lower()
    tokens = set(re.findall(r"[a-z]+", text))
    friendly = len(tokens & SOLO_FRIENDLY)
    hostile = len(tokens & SOLO_HOSTILE)
    # Map to [0,1] with default ~0.5 when nothing matches
    raw = default + 0.10 * friendly - 0.15 * hostile
    return max(0.0, min(1.0, raw))


def estimate_information_asymmetry(candidate: dict, market_match_count: Optional[int] = None,
                                    claude_known_count: Optional[int] = None,
                                    default: float = 0.5) -> float:
    """If market_verifier has run, compute the asymmetry; else fall back to default."""
    if market_match_count is None or claude_known_count is None or claude_known_count == 0:
        return default
    # (Claude-named players − market-verifier-found players) / Claude-named players
    raw = (claude_known_count - market_match_count) / claude_known_count
    return max(0.0, min(1.0, raw))


# ---- Scoring ----

@dataclass
class ImpactScore:
    candidate_id: str
    time_horizon: float
    impact_scale: float
    poc_tractability: float
    information_asymmetry: float
    predicted_impact: float
    weights_used: str  # "heuristic" or "fitted"
    user_label_needed: bool
    scored_at: str


def time_horizon_feature(th_years: float) -> float:
    """Map raw years to [0,1] with peak at 6 years."""
    return 1.0 - abs(th_years - 6.0) / 9.0  # in [-0, 1], can be slightly < 0 for far horizons


def score_candidate(
    candidate: dict,
    weights: Optional[dict] = None,
    market_match_count: Optional[int] = None,
    claude_known_count: Optional[int] = None,
) -> ImpactScore:
    """Score a single candidate. Returns ImpactScore (not yet written to disk)."""
    weights = weights or HEURISTIC_WEIGHTS

    th = estimate_time_horizon(candidate)
    isc = estimate_impact_scale(candidate)
    pt = estimate_poc_tractability(candidate)
    ia = estimate_information_asymmetry(
        candidate,
        market_match_count=market_match_count,
        claude_known_count=claude_known_count,
    )

    th_feat = time_horizon_feature(th)
    isc_feat = isc / 10.0

    logit = (
        weights.get("intercept", 0.0)
        + weights["time_horizon"] * th_feat
        + weights["impact_scale"] * isc_feat
        + weights["poc_tractability"] * pt
        + weights["information_asymmetry"] * ia
    )
    p = sigmoid(logit)

    return ImpactScore(
        candidate_id=candidate["candidate_id"],
        time_horizon=th,
        impact_scale=isc,
        poc_tractability=pt,
        information_asymmetry=ia,
        predicted_impact=p,
        weights_used="fitted" if weights is not HEURISTIC_WEIGHTS else "heuristic",
        user_label_needed=True,
        scored_at=datetime.now(timezone.utc).isoformat(),
    )


def score_all_candidates(
    candidates_dir: Path,
    out_dir: Path,
    weights_path: Optional[Path] = None,
) -> List[ImpactScore]:
    """Score all candidate JSONs in candidates_dir, writing enriched JSONs to out_dir.

    Each output JSON is the candidate enriched with the ImpactScore fields under
    a "impact_score" key.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    weights = HEURISTIC_WEIGHTS
    if weights_path and weights_path.exists():
        with weights_path.open("r", encoding="utf-8") as f:
            fitted = json.load(f)
        # Accept either {"weights": {...}} or direct {...}
        weights = fitted.get("weights", fitted)

    scores: List[ImpactScore] = []
    for cp in sorted(candidates_dir.glob("CAND_*.json")):
        with cp.open("r", encoding="utf-8") as f:
            cand = json.load(f)
        s = score_candidate(cand, weights=weights)
        scores.append(s)
        cand["impact_score"] = asdict(s)
        with (out_dir / cp.name).open("w", encoding="utf-8") as f:
            json.dump(cand, f, indent=2, ensure_ascii=False)

    # _index.json
    index = {
        "n_scored": len(scores),
        "weights_used": "fitted" if weights is not HEURISTIC_WEIGHTS else "heuristic",
        "weights": weights,
        "candidate_ids_by_predicted_impact_desc": [
            s.candidate_id for s in sorted(scores, key=lambda x: -x.predicted_impact)
        ],
        "scored_at": datetime.now(timezone.utc).isoformat(),
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    return scores


# ---- Trainable refit ----

def refit_weights(labels_path: Path, out_weights_path: Path,
                  min_labels: int = 10) -> dict:
    """Refit weights via simple logistic regression (gradient descent).

    Input: paradigm_shift/impact_labels.json with the schema:
        {"labels": [
            {"candidate_id": "...", "predicted_impact": 0.62, "user_label": 4,
             "time_horizon": ..., "impact_scale": ..., "poc_tractability": ...,
             "information_asymmetry": ...},
            ...
        ]}

    Output: writes {"weights": {...}, "trained_at": ..., "n_labels": N} to
    out_weights_path. Returns the new weights dict.

    Logistic regression with binarized labels (user_label >= 3 → 1, else 0).

    Honest acknowledgment: with 10 labels and 4 features, the coefficient
    estimates have huge variance. Expect noisy weights until 30+ labels.
    """
    if not labels_path.exists():
        return HEURISTIC_WEIGHTS

    with labels_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    labels = data.get("labels", [])
    if len(labels) < min_labels:
        return HEURISTIC_WEIGHTS

    # Build feature matrix X (N x 4) and target y (N,)
    X = []
    y = []
    for lab in labels:
        if not all(k in lab for k in ("time_horizon", "impact_scale",
                                       "poc_tractability", "information_asymmetry",
                                       "user_label")):
            continue
        X.append([
            time_horizon_feature(lab["time_horizon"]),
            lab["impact_scale"] / 10.0,
            lab["poc_tractability"],
            lab["information_asymmetry"],
        ])
        y.append(1.0 if lab["user_label"] >= 3 else 0.0)

    if len(X) < min_labels:
        return HEURISTIC_WEIGHTS

    # GD with L2 regularization
    n = len(X)
    n_feat = 4
    w = [HEURISTIC_WEIGHTS[k] for k in ("time_horizon", "impact_scale",
                                         "poc_tractability", "information_asymmetry")]
    b = HEURISTIC_WEIGHTS["intercept"]
    lr = 0.1
    l2 = 0.01
    for _ in range(1000):
        # Forward
        grad_w = [0.0] * n_feat
        grad_b = 0.0
        for xi, yi in zip(X, y):
            z = b + sum(w[j] * xi[j] for j in range(n_feat))
            p = sigmoid(z)
            err = p - yi
            for j in range(n_feat):
                grad_w[j] += err * xi[j]
            grad_b += err
        for j in range(n_feat):
            grad_w[j] = grad_w[j] / n + l2 * w[j]
            w[j] -= lr * grad_w[j]
        grad_b = grad_b / n
        b -= lr * grad_b

    fitted = {
        "intercept": b,
        "time_horizon": w[0],
        "impact_scale": w[1],
        "poc_tractability": w[2],
        "information_asymmetry": w[3],
    }
    out_weights_path.parent.mkdir(parents=True, exist_ok=True)
    with out_weights_path.open("w", encoding="utf-8") as f:
        json.dump({
            "weights": fitted,
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "n_labels": len(X),
            "note": (
                "Logistic regression on user_label binarized at >=3. "
                "Coefficients are noisy until 30+ labels accumulate."
            ),
        }, f, indent=2)
    return fitted


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_score = sub.add_parser("score")
    p_score.add_argument("--candidates_dir", required=True, type=Path)
    p_score.add_argument("--out_dir", required=True, type=Path)
    p_score.add_argument("--weights_path", type=Path, default=None)

    p_refit = sub.add_parser("refit")
    p_refit.add_argument("--labels_path", required=True, type=Path)
    p_refit.add_argument("--out_weights_path", required=True, type=Path)
    p_refit.add_argument("--min_labels", type=int, default=10)

    args = ap.parse_args()

    if args.cmd == "score":
        scores = score_all_candidates(args.candidates_dir, args.out_dir,
                                       weights_path=args.weights_path)
        print(f"scored {len(scores)} candidates")
        for s in sorted(scores, key=lambda x: -x.predicted_impact)[:10]:
            print(f"  {s.candidate_id}  impact={s.predicted_impact:.3f}  "
                  f"th={s.time_horizon:.1f}  is={s.impact_scale:.1f}  "
                  f"pt={s.poc_tractability:.2f}  ia={s.information_asymmetry:.2f}")
    elif args.cmd == "refit":
        w = refit_weights(args.labels_path, args.out_weights_path,
                          min_labels=args.min_labels)
        print("refit weights:")
        for k, v in w.items():
            print(f"  {k:24s} {v:+.3f}")


if __name__ == "__main__":
    main()

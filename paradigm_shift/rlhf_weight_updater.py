"""RLHF mimick weight updater for Run 11.

After each epoch, update rlhf_weights.json based on observed score
distribution. Simple gradient update:

  delta_i = learning_rate * (mean(param_i over survivors)
                           - mean(param_i over rejected))

Then re-normalize so the weights still sum to 1.0 (keeping composite_score
in [0,1] interpretation stable).

If an epoch yields 0 survivors (typical in saturated runs), we fall back
to ranking-based pseudo-survivors: top-3 by composite_score are treated
as "intended survivors" and bottom-3 as "clear rejected", so the gradient
still has a signal to amplify the parameters that discriminated them.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

THIS_DIR = Path(__file__).parent
RLHF_WEIGHTS_PATH = THIS_DIR / "rlhf_weights.json"


def _normalize(weights: Dict[str, float]) -> Dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        n = len(weights)
        return {k: 1.0 / n for k in weights}
    return {k: v / total for k, v in weights.items()}


def _mean_params(scored: List[Dict]) -> Dict[str, float]:
    if not scored:
        return {}
    keys = list(scored[0]["params"].keys())
    out: Dict[str, float] = {}
    for k in keys:
        out[k] = sum(s["params"][k] for s in scored) / len(scored)
    return out


def update_weights(scored_candidates: List[Dict],
                   survivor_threshold: float = 0.7,
                   epoch_label: str = "unknown_epoch",
                   forced_survivors: Optional[List[Dict]] = None,
                   forced_rejected: Optional[List[Dict]] = None) -> Dict:
    """Apply gradient and persist new rlhf_weights.json."""
    with open(RLHF_WEIGHTS_PATH) as f:
        state = json.load(f)
    weights: Dict[str, float] = dict(state["weights"])
    lr: float = float(state.get("learning_rate", 0.05))

    survivors = forced_survivors if forced_survivors is not None else [
        s for s in scored_candidates if s["composite_score"] >= survivor_threshold
    ]
    rejected = forced_rejected if forced_rejected is not None else [
        s for s in scored_candidates if s["composite_score"] < survivor_threshold
    ]

    fallback_used = False
    if not survivors and scored_candidates:
        # Pseudo-survivors: top-3 / bottom-3 split for gradient signal
        ranked = sorted(scored_candidates, key=lambda x: x["composite_score"], reverse=True)
        k = max(1, min(3, len(ranked) // 2))
        survivors = ranked[:k]
        rejected = ranked[-k:]
        fallback_used = True

    mu_s = _mean_params(survivors)
    mu_r = _mean_params(rejected)

    new_weights: Dict[str, float] = {}
    deltas: Dict[str, float] = {}
    for k, w in weights.items():
        ds = mu_s.get(k, 0.0)
        dr = mu_r.get(k, 0.0)
        delta = lr * (ds - dr)
        new_w = max(0.001, w + delta)  # floor to keep nonzero
        new_weights[k] = new_w
        deltas[k] = round(delta, 5)

    new_weights = _normalize(new_weights)

    history_entry = {
        "epoch_label": epoch_label,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "version_before": state.get("version", 0),
        "version_after": state.get("version", 0) + 1,
        "n_survivors": len(survivors),
        "n_rejected": len(rejected),
        "fallback_pseudo_split": fallback_used,
        "delta": deltas,
        "weights_after": {k: round(v, 5) for k, v in new_weights.items()},
        "survivor_mean_params": {k: round(v, 4) for k, v in mu_s.items()},
        "rejected_mean_params": {k: round(v, 4) for k, v in mu_r.items()},
    }
    history = list(state.get("weight_history", []))
    history.append(history_entry)

    new_state = {
        **state,
        "version": state.get("version", 0) + 1,
        "last_updated_at": datetime.now(timezone.utc).isoformat(),
        "epoch_origin": epoch_label,
        "weights": new_weights,
        "weight_history": history,
    }
    with open(RLHF_WEIGHTS_PATH, "w") as f:
        json.dump(new_state, f, indent=2)
    return history_entry


def snapshot_weights(epoch_dir: Path, label: str) -> None:
    epoch_dir.mkdir(parents=True, exist_ok=True)
    with open(RLHF_WEIGHTS_PATH) as f:
        state = json.load(f)
    snap_path = epoch_dir / f"weights_snapshot_{label}.json"
    with open(snap_path, "w") as f:
        json.dump(state, f, indent=2)


if __name__ == "__main__":
    # Smoke test
    demo = [
        {"cand_id": "C1", "composite_score": 0.85,
         "params": {"atom_quality_score": 0.9, "novelty_score": 0.9, "cross_source_diversity": 1.0,
                    "mechanism_coherence": 0.6, "saturation_distance": 0.9,
                    "speaker_self_publish_risk": 1.0, "arxiv_grounding": 0.4,
                    "belinda_audit_pass": 1.0, "community_density": 0.9,
                    "cross_disciplinary_bonus": 1.0}},
        {"cand_id": "C2", "composite_score": 0.2,
         "params": {"atom_quality_score": 0.3, "novelty_score": 0.1, "cross_source_diversity": 0.2,
                    "mechanism_coherence": 0.2, "saturation_distance": 0.1,
                    "speaker_self_publish_risk": 0.5, "arxiv_grounding": 0.0,
                    "belinda_audit_pass": 0.0, "community_density": 0.1,
                    "cross_disciplinary_bonus": 0.0}},
    ]
    print(json.dumps(update_weights(demo, epoch_label="smoke_test"), indent=2))

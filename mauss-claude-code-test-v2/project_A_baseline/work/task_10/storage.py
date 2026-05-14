"""JSON persistence for MarkovModel."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from model import MarkovModel

# Separator used to encode tuple states as JSON object keys.
# Picked to be vanishingly unlikely in natural text tokens.
_STATE_SEP = "␟"  # Unicode SYMBOL FOR UNIT SEPARATOR


def _state_to_key(state):
    return _STATE_SEP.join(state)


def _key_to_state(key: str):
    return tuple(key.split(_STATE_SEP))


def save(model: MarkovModel, path: Union[str, Path]) -> None:
    """Serialize a MarkovModel to a JSON file."""
    if not isinstance(model, MarkovModel):
        raise TypeError("save() expects a MarkovModel")
    path = Path(path)

    payload = {
        "version": 1,
        "order": model.order,
        "sep": _STATE_SEP,
        "transitions": {
            _state_to_key(state): dict(bucket)
            for state, bucket in model.transitions.items()
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)


def load(path: Union[str, Path]) -> MarkovModel:
    """Load a MarkovModel from a JSON file produced by save()."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)

    if not isinstance(payload, dict):
        raise ValueError("invalid model file: top-level must be an object")
    if "order" not in payload or "transitions" not in payload:
        raise ValueError("invalid model file: missing 'order' or 'transitions'")

    order = int(payload["order"])
    sep = payload.get("sep", _STATE_SEP)

    model = MarkovModel(order=order)
    for key, bucket in payload["transitions"].items():
        if sep == _STATE_SEP:
            state = _key_to_state(key)
        else:
            state = tuple(key.split(sep))
        # Guard against malformed states
        if len(state) != order:
            raise ValueError(
                f"state key {key!r} has {len(state)} parts but model order is {order}"
            )
        model.transitions[state] = {str(tok): int(cnt) for tok, cnt in bucket.items()}
    return model

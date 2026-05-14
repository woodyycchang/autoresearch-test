"""Persistence for MarkovModel: JSON save/load round-trip."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from model import MarkovModel

PathLike = Union[str, Path]


def save_model(model: MarkovModel, path: PathLike) -> None:
    """Serialize model to JSON at `path`. Overwrites if exists."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as fh:
        json.dump(model.to_dict(), fh, ensure_ascii=False, sort_keys=True, indent=2)


def load_model(path: PathLike) -> MarkovModel:
    """Load model previously saved with `save_model`."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    return MarkovModel.from_dict(data)

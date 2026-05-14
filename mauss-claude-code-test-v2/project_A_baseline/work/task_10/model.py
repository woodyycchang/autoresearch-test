"""Markov chain model: stores n-gram transition counts."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Tuple


class MarkovModel:
    """N-gram Markov chain model.

    Stores transition counts: state (tuple of `order` tokens) -> {next_token: count}.
    """

    def __init__(self, order: int = 2):
        if not isinstance(order, int) or order < 1:
            raise ValueError("order must be a positive integer (>= 1)")
        self.order = order
        # Use plain dict-of-dict for stable JSON serialization.
        self.transitions: Dict[Tuple[str, ...], Dict[str, int]] = {}

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------
    def train(self, tokens: Iterable[str]) -> None:
        """Train the model on a sequence of tokens.

        Updates transition counts in place (additive — call repeatedly to keep training).
        """
        tokens = list(tokens)
        if len(tokens) <= self.order:
            return
        for i in range(len(tokens) - self.order):
            state = tuple(tokens[i : i + self.order])
            next_tok = tokens[i + self.order]
            bucket = self.transitions.setdefault(state, {})
            bucket[next_tok] = bucket.get(next_tok, 0) + 1

    # ------------------------------------------------------------------
    # Merge
    # ------------------------------------------------------------------
    def merge(self, other: "MarkovModel") -> "MarkovModel":
        """Return a new model that combines counts from self and other.

        Both models must share the same `order`. Counts are summed (not replaced).
        """
        if not isinstance(other, MarkovModel):
            raise TypeError("can only merge with another MarkovModel")
        if self.order != other.order:
            raise ValueError(
                f"order mismatch: self.order={self.order}, other.order={other.order}"
            )

        merged = MarkovModel(order=self.order)
        # Copy self
        for state, bucket in self.transitions.items():
            merged.transitions[state] = dict(bucket)
        # Add other
        for state, bucket in other.transitions.items():
            target = merged.transitions.setdefault(state, {})
            for tok, count in bucket.items():
                target[tok] = target.get(tok, 0) + count
        return merged

    # ------------------------------------------------------------------
    # Lookup helpers
    # ------------------------------------------------------------------
    def has_state(self, state: Tuple[str, ...]) -> bool:
        return tuple(state) in self.transitions

    def next_distribution(self, state: Tuple[str, ...]) -> Dict[str, int]:
        """Return the count distribution for `state`, or empty dict if unknown."""
        return dict(self.transitions.get(tuple(state), {}))

    def states(self) -> List[Tuple[str, ...]]:
        return list(self.transitions.keys())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MarkovModel):
            return NotImplemented
        return self.order == other.order and self.transitions == other.transitions

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"MarkovModel(order={self.order}, states={len(self.transitions)})"

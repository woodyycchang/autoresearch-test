"""Markov chain model: stores n-gram transition counts."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Tuple


class MarkovModel:
    """A Markov chain model storing transition counts for a given n-gram order.

    transitions: maps a tuple of `order` tokens (the state) to a dict of
    next-token -> count.
    """

    def __init__(self, order: int = 2):
        if not isinstance(order, int) or order < 1:
            raise ValueError("order must be a positive integer")
        self.order = order
        # state (tuple of order tokens) -> { next_token: count }
        self.transitions: Dict[Tuple[str, ...], Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        # also track starting states so generator can seed itself if needed
        self.starts: Dict[Tuple[str, ...], int] = defaultdict(int)

    def _tokens(self, text_or_tokens) -> List[str]:
        if isinstance(text_or_tokens, str):
            return text_or_tokens.split()
        return list(text_or_tokens)

    def train(self, text_or_tokens) -> None:
        """Train (incrementally) on a sequence of tokens or whitespace text."""
        tokens = self._tokens(text_or_tokens)
        if len(tokens) <= self.order:
            return
        # record start state
        start_state = tuple(tokens[: self.order])
        self.starts[start_state] += 1
        for i in range(len(tokens) - self.order):
            state = tuple(tokens[i : i + self.order])
            nxt = tokens[i + self.order]
            self.transitions[state][nxt] += 1

    def states(self) -> Iterable[Tuple[str, ...]]:
        return self.transitions.keys()

    def next_distribution(self, state: Tuple[str, ...]) -> Dict[str, int]:
        """Return the count dict for transitions from `state` (may be empty)."""
        return dict(self.transitions.get(state, {}))

    def merge(self, other: "MarkovModel") -> "MarkovModel":
        """Return a new model with summed counts from self and other.

        Raises ValueError if orders differ.
        """
        if other.order != self.order:
            raise ValueError("cannot merge models of different orders")
        merged = MarkovModel(order=self.order)
        for state, nexts in self.transitions.items():
            for tok, c in nexts.items():
                merged.transitions[state][tok] += c
        for state, nexts in other.transitions.items():
            for tok, c in nexts.items():
                merged.transitions[state][tok] += c
        for state, c in self.starts.items():
            merged.starts[state] += c
        for state, c in other.starts.items():
            merged.starts[state] += c
        return merged

    def to_dict(self) -> dict:
        """Plain-data representation suitable for JSON serialization."""
        # tuple keys are not JSON-serializable; we represent state as a list.
        return {
            "order": self.order,
            "transitions": [
                {"state": list(state), "nexts": dict(nexts)}
                for state, nexts in self.transitions.items()
            ],
            "starts": [
                {"state": list(state), "count": c} for state, c in self.starts.items()
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MarkovModel":
        order = int(data["order"])
        m = cls(order=order)
        for entry in data.get("transitions", []):
            state = tuple(entry["state"])
            for tok, c in entry["nexts"].items():
                m.transitions[state][tok] = int(c)
        for entry in data.get("starts", []):
            state = tuple(entry["state"])
            m.starts[state] = int(entry["count"])
        return m

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MarkovModel):
            return NotImplemented
        if self.order != other.order:
            return False
        # Compare transitions as plain dicts to ignore defaultdict default factory.
        a = {k: dict(v) for k, v in self.transitions.items()}
        b = {k: dict(v) for k, v in other.transitions.items()}
        return a == b and dict(self.starts) == dict(other.starts)

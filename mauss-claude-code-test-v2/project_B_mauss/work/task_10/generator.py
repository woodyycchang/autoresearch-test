"""Markov chain text generator with temperature sampling."""
from __future__ import annotations

import math
import random
from typing import List, Optional, Sequence, Tuple

from model import MarkovModel


class MarkovGenerator:
    """Generate text from a trained MarkovModel.

    Temperature semantics:
      - 0.0  : greedy (always pick the most frequent next token; ties broken
               deterministically by sorted token order)
      - 1.0  : sample proportional to raw counts
      - >0,!=1 : sample by counts ** (1/temperature). Larger temperature => more
               uniform; smaller (closer to 0) => more peaked.
    """

    def __init__(self, model: MarkovModel, rng: Optional[random.Random] = None):
        self.model = model
        self.rng = rng if rng is not None else random.Random()

    def _seed_state(self, seed: Sequence[str]) -> Tuple[str, ...]:
        order = self.model.order
        if seed is None:
            raise ValueError("seed must be provided")
        seed_tokens = list(seed) if not isinstance(seed, str) else seed.split()
        if len(seed_tokens) < order:
            raise ValueError(
                f"seed must contain at least {order} tokens for order={order}"
            )
        return tuple(seed_tokens[-order:])

    def _pick_next(
        self, counts: dict, temperature: float
    ) -> str:
        if not counts:
            raise KeyError("no transitions from state")
        if temperature == 0.0:
            # Greedy: highest count, deterministic tie break.
            best = max(counts.items(), key=lambda kv: (kv[1], -ord_key(kv[0])))
            # Use explicit deterministic tie-breaking: highest count, then
            # lexicographically smallest token.
            max_count = max(counts.values())
            tied = sorted(t for t, c in counts.items() if c == max_count)
            return tied[0]
        tokens = list(counts.keys())
        # weights = count ** (1/temperature)
        inv = 1.0 / temperature
        weights = [max(counts[t], 0) ** inv for t in tokens]
        total = sum(weights)
        if total <= 0 or any(math.isinf(w) or math.isnan(w) for w in weights):
            # fall back to uniform over known transitions
            return self.rng.choice(tokens)
        return self.rng.choices(tokens, weights=weights, k=1)[0]

    def generate(
        self,
        seed: Sequence[str],
        length: int,
        temperature: float = 1.0,
    ) -> List[str]:
        """Generate `length` tokens after `seed`. Returns seed + generated."""
        if length < 0:
            raise ValueError("length must be non-negative")
        order = self.model.order
        seed_tokens = list(seed) if not isinstance(seed, str) else seed.split()
        out: List[str] = list(seed_tokens)
        state = self._seed_state(seed_tokens)
        for _ in range(length):
            counts = self.model.next_distribution(state)
            if not counts:
                # generator "falls off" — stop gracefully rather than crashing
                break
            nxt = self._pick_next(counts, temperature)
            out.append(nxt)
            state = tuple(out[-order:])
        return out

    def generate_text(
        self, seed, length: int, temperature: float = 1.0
    ) -> str:
        return " ".join(self.generate(seed, length, temperature))


def ord_key(token: str) -> int:
    """Tie-breaking helper (unused — kept for clarity)."""
    return sum(ord(c) for c in token)

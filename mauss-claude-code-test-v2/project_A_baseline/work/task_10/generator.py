"""Generate text from a trained MarkovModel."""
from __future__ import annotations

import math
import random
from typing import List, Optional, Sequence

from model import MarkovModel


class MarkovGenerator:
    """Wraps a MarkovModel and produces sequences of tokens."""

    def __init__(self, model: MarkovModel, rng: Optional[random.Random] = None):
        if not isinstance(model, MarkovModel):
            raise TypeError("model must be a MarkovModel instance")
        self.model = model
        self.rng = rng if rng is not None else random.Random()

    # ------------------------------------------------------------------
    # Sampling
    # ------------------------------------------------------------------
    def _sample_next(self, state, temperature: float) -> Optional[str]:
        """Sample the next token given a state.

        temperature == 0 -> greedy (argmax, ties broken by sorted token order for determinism)
        temperature == 1 -> sample proportionally to counts
        temperature  > 0 (other) -> reshape distribution: p_i ∝ count_i ** (1/temperature)
        Returns None if no transition exists.
        """
        if temperature < 0:
            raise ValueError("temperature must be >= 0")

        bucket = self.model.next_distribution(state)
        if not bucket:
            return None

        items = sorted(bucket.items())  # deterministic order, used both for greedy ties and sampling

        if temperature == 0:
            # Greedy: highest count, ties broken by sorted token order.
            best_tok, best_count = items[0]
            for tok, count in items[1:]:
                if count > best_count:
                    best_tok, best_count = tok, count
            return best_tok

        tokens = [tok for tok, _ in items]
        counts = [c for _, c in items]

        if temperature == 1.0:
            weights = [float(c) for c in counts]
        else:
            # Reshape: higher temperature -> closer to uniform; lower (between 0 and 1) -> sharper.
            inv_t = 1.0 / temperature
            weights = [float(c) ** inv_t for c in counts]

        total = sum(weights)
        if total <= 0:
            return tokens[0]
        # rng.choices for weighted sampling
        return self.rng.choices(tokens, weights=weights, k=1)[0]

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------
    def generate(
        self,
        seed: Sequence[str],
        length: int,
        temperature: float = 1.0,
    ) -> List[str]:
        """Generate up to `length` tokens following the seed.

        The returned list starts with the seed tokens followed by generated tokens.
        Generation stops if no transition exists for the current state (falls off).
        """
        if length < 0:
            raise ValueError("length must be >= 0")
        seed = list(seed)
        if len(seed) < self.model.order:
            raise ValueError(
                f"seed must have at least {self.model.order} tokens "
                f"(got {len(seed)})"
            )

        out: List[str] = list(seed)
        for _ in range(length):
            state = tuple(out[-self.model.order :])
            nxt = self._sample_next(state, temperature)
            if nxt is None:
                break  # generator falls off — no transition exists
            out.append(nxt)
        return out

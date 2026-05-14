"""Basic Markov chain text generator."""

import random
from collections import defaultdict


class MarkovChain:
    """A Markov chain text generator of configurable order."""

    def __init__(self, order=1):
        if order < 1:
            raise ValueError("order must be >= 1")
        self.order = order
        self.transitions = defaultdict(list)
        self.starts = []
        self._words = []

    def train(self, text):
        """Split text on whitespace and build the transition table."""
        words = text.split()
        self._words = words
        if len(words) <= self.order:
            # Not enough data to build any transitions.
            if words:
                self.starts.append(tuple(words[: self.order]))
            return
        # Record every order-length window as a potential starting state.
        for i in range(len(words) - self.order):
            state = tuple(words[i : i + self.order])
            nxt = words[i + self.order]
            self.transitions[state].append(nxt)
            self.starts.append(state)

    def generate(self, length, seed=None):
        """Generate `length` words, optionally seeded for determinism."""
        if length <= 0:
            return ""
        if not self.starts:
            raise ValueError("Chain has not been trained on any data.")

        rng = random.Random(seed)
        state = rng.choice(self.starts)
        output = list(state)

        while len(output) < length:
            nexts = self.transitions.get(state)
            if not nexts:
                # Dead end: restart from a random starting state.
                state = rng.choice(self.starts)
                # Append the restart state's words so we keep producing output.
                for w in state:
                    if len(output) >= length:
                        break
                    output.append(w)
                continue
            nxt = rng.choice(nexts)
            output.append(nxt)
            state = tuple(output[-self.order :])

        return " ".join(output[:length])

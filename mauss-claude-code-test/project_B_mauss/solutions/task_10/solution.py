"""Basic Markov chain text generator (task_10)."""

import random
from collections import defaultdict


class MarkovChain:
    """Word-level Markov chain of configurable order.

    Predicts the next word from the previous ``order`` words.
    """

    def __init__(self, order=1):
        if not isinstance(order, int) or order < 1:
            raise ValueError("order must be an integer >= 1")
        self.order = order
        # state (tuple of `order` words) -> list of possible next words
        self.transitions = defaultdict(list)
        # all states that ever appeared (used to restart on dead ends)
        self.start_states = []

    def train(self, text):
        """Build transition table from ``text`` (split on whitespace)."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        words = text.split()
        if len(words) <= self.order:
            # Not enough words to build any transitions.
            if len(words) == self.order:
                self.start_states.append(tuple(words))
            return
        for i in range(len(words) - self.order):
            state = tuple(words[i : i + self.order])
            next_word = words[i + self.order]
            self.transitions[state].append(next_word)
            self.start_states.append(state)

    def generate(self, length, seed=None):
        """Generate a string of ``length`` words.

        ``seed`` makes output deterministic. On dead ends, restart from a
        random training start state.
        """
        if not isinstance(length, int) or length < 0:
            raise ValueError("length must be a non-negative integer")
        if length == 0:
            return ""
        if not self.start_states:
            raise RuntimeError("Chain has not been trained on any data")

        rng = random.Random(seed)
        state = rng.choice(self.start_states)
        output = list(state)

        while len(output) < length:
            choices = self.transitions.get(state)
            if not choices:
                # Dead end -- restart from a random known state.
                state = rng.choice(self.start_states)
                # Avoid duplicating words when restarting: just continue with
                # this state's first transition on next iteration.
                continue
            next_word = rng.choice(choices)
            output.append(next_word)
            state = tuple(output[-self.order :])

        return " ".join(output[:length])

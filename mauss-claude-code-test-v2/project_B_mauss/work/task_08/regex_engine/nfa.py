"""NFA state representation and Thompson construction primitives.

States have at most two outgoing transitions for Thompson NFAs. Transitions are
labeled with either an epsilon (None) or a matcher callable that returns True
when a character satisfies the transition predicate.
"""

from itertools import count

# Special transition labels
EPSILON = None  # epsilon transition (no character consumed)


class State:
    """A single NFA state.

    Attributes:
        id: unique identifier (helpful for debugging / dedup in subset sim)
        is_match: True if this state is the accepting state
        transitions: list of (label, target_state). label is EPSILON or a
            callable(ch:str) -> bool.
    """

    _ids = count()

    __slots__ = ("id", "is_match", "transitions")

    def __init__(self, is_match: bool = False) -> None:
        self.id = next(State._ids)
        self.is_match = is_match
        self.transitions = []  # list[ tuple[label, State] ]

    def add(self, label, target: "State") -> None:
        self.transitions.append((label, target))

    def __repr__(self) -> str:  # pragma: no cover - debug only
        return f"State({self.id}, match={self.is_match})"


class Fragment:
    """An NFA fragment with a single start state and a list of dangling
    out-arrows (callables that, when called with a target state, patch the
    arrow to point at that state).
    """

    __slots__ = ("start", "outs")

    def __init__(self, start: State, outs) -> None:
        self.start = start
        self.outs = list(outs)  # list of callables  patch(target)

    def patch(self, target: State) -> None:
        for p in self.outs:
            p(target)
        self.outs = []


def _arrow(state: State, label):
    """Create a dangling arrow from `state` with `label` to a TBD target.

    Returns a `patch` callable that finishes the arrow when given the target.
    """
    idx = len(state.transitions)
    state.transitions.append((label, None))

    def patch(target: State) -> None:
        state.transitions[idx] = (label, target)

    return patch

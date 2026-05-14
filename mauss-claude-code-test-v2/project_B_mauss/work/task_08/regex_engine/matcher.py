"""NFA simulator and public Regex API.

We use the classic Thompson subset-construction simulation. To avoid runaway
on pathological patterns like `(a*)*`, every simulation step is bounded by
``MAX_SIM_STEPS``; if exceeded the matcher returns no match for the current
attempt.
"""

from .compiler import compile_pattern, _Anchor, ANCHOR_START, ANCHOR_END
from .nfa import EPSILON, State


# Cap NFA simulation steps to prevent pathological blowup.
MAX_SIM_STEPS = 1_000_000


class SimulationLimitExceeded(RuntimeError):
    pass


def _epsilon_closure(states, *, at_start: bool, at_end: bool):
    """Expand a list of states by following epsilon AND zero-width anchor
    transitions whose assertion is satisfied at the current position.
    Returns a list of states in deterministic order, deduped.
    """
    closure = []
    seen = set()
    stack = list(states)
    while stack:
        s = stack.pop()
        if s.id in seen:
            continue
        seen.add(s.id)
        closure.append(s)
        for label, target in s.transitions:
            if target is None:
                continue  # un-patched (shouldn't happen post-compile)
            if label is EPSILON:
                if target.id not in seen:
                    stack.append(target)
            elif isinstance(label, _Anchor):
                # zero-width: traverse only if assertion holds
                if label is ANCHOR_START and at_start:
                    if target.id not in seen:
                        stack.append(target)
                elif label is ANCHOR_END and at_end:
                    if target.id not in seen:
                        stack.append(target)
    return closure


def _step(states, ch):
    """Consume one character `ch` from `states`, returning next state set."""
    nxt = []
    seen = set()
    for s in states:
        for label, target in s.transitions:
            if target is None or label is EPSILON or isinstance(label, _Anchor):
                continue
            try:
                if label(ch):
                    if target.id not in seen:
                        seen.add(target.id)
                        nxt.append(target)
            except Exception:
                continue
    return nxt


def _has_match(states):
    return any(s.is_match for s in states)


def _simulate(start: State, text: str, start_idx: int, *, anchored_end: bool = False):
    """Simulate the NFA starting at `start_idx` in `text`.

    Returns (end_idx, True) for the LONGEST match found, or (-1, False).
    """
    steps = 0
    n = len(text)
    at_start = (start_idx == 0)
    at_end = (start_idx == n)
    current = _epsilon_closure([start], at_start=at_start, at_end=at_end)
    last_match_end = start_idx if _has_match(current) else -1

    i = start_idx
    while i < n and current:
        ch = text[i]
        current = _step(current, ch)
        i += 1
        steps += len(current) + 1
        if steps > MAX_SIM_STEPS:
            raise SimulationLimitExceeded("NFA simulation cap exceeded")
        at_start = (i == 0)
        at_end = (i == n)
        current = _epsilon_closure(current, at_start=at_start, at_end=at_end)
        if _has_match(current):
            last_match_end = i
        if not current:
            break

    return (last_match_end, last_match_end >= 0)


class Regex:
    def __init__(self, pattern: str) -> None:
        self._nfa = compile_pattern(pattern)
        self.pattern = pattern

    def match(self, text: str):
        """Match from the start of the text. Returns the matched substring or
        None. Equivalent to Python's re.match (no need for full match)."""
        try:
            end, ok = _simulate(self._nfa.start, text, 0)
        except SimulationLimitExceeded:
            return None
        if not ok:
            return None
        return text[:end]

    def fullmatch(self, text: str):
        try:
            end, ok = _simulate(self._nfa.start, text, 0)
        except SimulationLimitExceeded:
            return None
        if ok and end == len(text):
            return text
        return None

    def search(self, text: str):
        """Find first match anywhere in text. Returns (start, end, substr) or
        None."""
        n = len(text)
        for start in range(n + 1):
            try:
                end, ok = _simulate(self._nfa.start, text, start)
            except SimulationLimitExceeded:
                return None
            if ok:
                return (start, end, text[start:end])
        return None

    def findall(self, text: str):
        """Return all non-overlapping match substrings (leftmost-longest)."""
        out = []
        n = len(text)
        i = 0
        while i <= n:
            try:
                end, ok = _simulate(self._nfa.start, text, i)
            except SimulationLimitExceeded:
                return out
            if ok and end > i:
                out.append(text[i:end])
                i = end
            elif ok and end == i:
                # zero-width match  advance by 1 to avoid infinite loop
                out.append("")
                i += 1
            else:
                i += 1
        return out


def compile(pattern: str) -> Regex:  # noqa: A001 - matches stdlib `re.compile`
    """Compile a regex pattern into a Regex object."""
    return Regex(pattern)

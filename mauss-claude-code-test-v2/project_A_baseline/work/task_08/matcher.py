"""NFA simulation (Thompson's algorithm) + public Regex API.

The simulator runs every reachable state in parallel to avoid exponential
backtracking, which also makes pathological patterns like `(a*)*` terminate
in linear time. We also enforce a hard step cap as a belt-and-suspenders
safeguard.
"""

from compiler import ANCHOR_START, ANCHOR_END, compile_pattern
from nfa import EPSILON


# Hard cap on simulation work — protects against any unforeseen pathology.
MAX_STEPS = 1_000_000


class _StepBudget:
    def __init__(self, budget=MAX_STEPS):
        self.remaining = budget

    def tick(self, n=1):
        self.remaining -= n
        if self.remaining < 0:
            raise RuntimeError("regex simulation step budget exceeded")


def _epsilon_close(states, pos, text, budget):
    """Expand a set of states via epsilon and anchor transitions.

    Anchors are treated as zero-width epsilon-like transitions that succeed
    only when the position satisfies them.
    """
    closure = set()
    stack = list(states)
    while stack:
        budget.tick()
        s = stack.pop()
        if s in closure:
            continue
        closure.add(s)
        for matcher, target in s.transitions:
            if matcher == EPSILON:
                if target not in closure:
                    stack.append(target)
            elif matcher == ANCHOR_START:
                if pos == 0:
                    if target not in closure:
                        stack.append(target)
            elif matcher == ANCHOR_END:
                if pos == len(text):
                    if target not in closure:
                        stack.append(target)
    return closure


def _simulate(start, accept, text, start_pos, full_match=False):
    """Run NFA from `start_pos` against `text`.

    Returns the end index of the longest accepted match starting at start_pos,
    or -1 if no match. When `full_match` is True, the match must consume the
    entire remainder.
    """
    budget = _StepBudget()
    current = _epsilon_close({start}, start_pos, text, budget)
    longest = -1
    if accept in current:
        if not full_match or start_pos == len(text):
            longest = start_pos

    pos = start_pos
    while current and pos < len(text):
        ch = text[pos]
        next_states = set()
        for s in current:
            budget.tick()
            for matcher, target in s.transitions:
                if matcher == EPSILON or matcher == ANCHOR_START or matcher == ANCHOR_END:
                    continue
                if callable(matcher) and matcher(ch):
                    next_states.add(target)
        pos += 1
        if not next_states:
            break
        current = _epsilon_close(next_states, pos, text, budget)
        if accept in current:
            if full_match:
                if pos == len(text):
                    longest = pos
            else:
                longest = pos
    return longest


class Regex:
    def __init__(self, pattern):
        self.pattern = pattern
        self.start, self.accept = compile_pattern(pattern)

    def match(self, s):
        """Try to match at the beginning of s. Returns end index or None.

        Equivalent to Python's re.match: anchored at start, may consume any
        prefix of s. The returned end index is exclusive.
        """
        end = _simulate(self.start, self.accept, s, 0)
        return end if end >= 0 else None

    def fullmatch(self, s):
        end = _simulate(self.start, self.accept, s, 0, full_match=True)
        if end == len(s):
            return end
        return None

    def search(self, s):
        """Find first match anywhere in s. Returns (start, end) or None."""
        for i in range(len(s) + 1):
            end = _simulate(self.start, self.accept, s, i)
            if end >= 0:
                return (i, end)
        return None

    def findall(self, s):
        """Return all non-overlapping matches as a list of substrings."""
        results = []
        i = 0
        while i <= len(s):
            end = _simulate(self.start, self.accept, s, i)
            if end >= 0:
                results.append(s[i:end])
                # Skip past the match (or at least one char to avoid infinite
                # loop on zero-width matches).
                i = end if end > i else i + 1
            else:
                i += 1
        return results


def compile(pattern):
    """Public API: compile a pattern into a Regex object."""
    return Regex(pattern)

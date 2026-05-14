"""NFA data structures for the regex engine.

A State has a list of outgoing transitions. Each transition has a matcher
function (or None for epsilon) and a target state.
"""

# Sentinels for special transitions
EPSILON = "EPSILON"


class State:
    """A single NFA state.

    transitions: list of (matcher, next_state) tuples.
        matcher is either EPSILON (for epsilon move) or a callable(ch) -> bool
        for a character class. The matcher None is reserved for the accept state.
    """

    __slots__ = ("id", "transitions", "is_accept")

    _counter = 0

    def __init__(self):
        self.id = State._counter
        State._counter += 1
        self.transitions = []
        self.is_accept = False

    def add(self, matcher, target):
        self.transitions.append((matcher, target))

    def __repr__(self):
        return f"State({self.id}, accept={self.is_accept})"


class Fragment:
    """An NFA fragment with one start state and a set of dangling out-pointers.

    `outs` is a list of (state, attr_name_or_index) describing where to patch
    the next state when concatenating. We use a callback-based patching scheme
    via a list of functions that accept the target state.
    """

    __slots__ = ("start", "patches")

    def __init__(self, start, patches):
        self.start = start
        # patches: list of callables(target_state) that set the dangling edge
        self.patches = patches


def patch(fragment, target):
    """Patch all dangling edges of `fragment` to `target`."""
    for fn in fragment.patches:
        fn(target)


def make_literal(ch):
    """Fragment matching a single character via predicate."""
    return make_predicate(lambda c, ch=ch: c == ch)


def make_any():
    """Fragment matching any single character (except newline, like Python's
    default `.` semantics)."""
    return make_predicate(lambda c: c != "\n")


def make_predicate(pred):
    """Fragment from a single character predicate."""
    s = State()
    # Dangling edge: we don't know target yet
    holder = [None]

    def transition_matcher(c, pred=pred):
        return pred(c)

    def patch_fn(target, s=s, transition_matcher=transition_matcher):
        s.transitions.append((transition_matcher, target))

    return Fragment(s, [patch_fn])


def make_charclass(predicate):
    """Fragment from arbitrary predicate (used by [abc], [^xy], [a-z])."""
    return make_predicate(predicate)


def make_concat(a, b):
    """Concatenation: patch a's dangling edges to b's start."""
    patch(a, b.start)
    return Fragment(a.start, b.patches)


def make_alt(a, b):
    """Alternation: new start state with epsilon to a.start and b.start."""
    s = State()
    s.transitions.append((EPSILON, a.start))
    s.transitions.append((EPSILON, b.start))
    return Fragment(s, a.patches + b.patches)


def make_star(a):
    """Zero or more: epsilon split into a.start or out; a's tail loops back."""
    s = State()
    s.transitions.append((EPSILON, a.start))

    def patch_fn(target, s=s):
        s.transitions.append((EPSILON, target))

    # Patch a's dangling edges back to the split state
    patch(a, s)
    return Fragment(s, [patch_fn])


def make_plus(a):
    """One or more: like a then a*, looping back."""
    s = State()
    # a's start
    patch(a, s)
    s.transitions.append((EPSILON, a.start))

    def patch_fn(target, s=s):
        s.transitions.append((EPSILON, target))

    return Fragment(a.start, [patch_fn])


def make_question(a):
    """Optional: split state to a.start or skip."""
    s = State()
    s.transitions.append((EPSILON, a.start))

    def patch_fn(target, s=s):
        s.transitions.append((EPSILON, target))

    return Fragment(s, a.patches + [patch_fn])


def finalize(fragment):
    """Add an accept state and patch dangling edges to it.

    Returns (start_state, accept_state).
    """
    accept = State()
    accept.is_accept = True
    patch(fragment, accept)
    return fragment.start, accept

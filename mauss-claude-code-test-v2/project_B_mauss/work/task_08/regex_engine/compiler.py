"""Regex -> NFA compiler using recursive-descent parsing + Thompson
construction.

Grammar (highest precedence at bottom):
    regex      := alternation
    alternation:= concat ('|' concat)*
    concat     := (quantified)*
    quantified := atom ('*' | '+' | '?')?
    atom       := '(' regex ')' | charclass | escape | dot | anchor | literal

Anchors: '^' at start of a concat asserts start-of-string; '$' at end asserts
end-of-string. They are represented as zero-width assertion transitions
recognised by the matcher (see matcher.py).
"""

from .nfa import State, Fragment, EPSILON, _arrow


# Sentinel matchers for zero-width assertions
class _Anchor:
    """Marker for ^ / $ zero-width transitions; the matcher special-cases
    these by inspecting the label `type`.
    """

    __slots__ = ("kind",)

    def __init__(self, kind: str) -> None:
        self.kind = kind  # 'start' or 'end'

    def __repr__(self) -> str:  # pragma: no cover - debug only
        return f"Anchor({self.kind})"


ANCHOR_START = _Anchor("start")
ANCHOR_END = _Anchor("end")


def _lit_matcher(ch: str):
    def match(c):
        return c == ch
    match.kind = "lit"
    match.ch = ch
    return match


def _dot_matcher():
    def match(c):
        # '.' matches any char except newline (standard behaviour)
        return c is not None and c != "\n"
    match.kind = "dot"
    return match


def _class_matcher(chars: set, ranges: list, negated: bool):
    def match(c):
        if c is None:
            return False
        in_class = c in chars
        if not in_class:
            for lo, hi in ranges:
                if lo <= c <= hi:
                    in_class = True
                    break
        return (not in_class) if negated else in_class
    match.kind = "class"
    return match


SPECIAL_ESCAPES = {
    "n": "\n",
    "t": "\t",
    "r": "\r",
    "\\": "\\",
    ".": ".",
    "*": "*",
    "+": "+",
    "?": "?",
    "|": "|",
    "(": "(",
    ")": ")",
    "[": "[",
    "]": "]",
    "^": "^",
    "$": "$",
    "/": "/",
}


class ParseError(ValueError):
    pass


class Parser:
    def __init__(self, pattern: str) -> None:
        self.pat = pattern
        self.pos = 0

    # ---------- lexer-ish helpers ----------
    def peek(self):
        return self.pat[self.pos] if self.pos < len(self.pat) else None

    def eat(self, ch=None):
        if self.pos >= len(self.pat):
            raise ParseError(f"unexpected end of pattern (expected {ch!r})")
        cur = self.pat[self.pos]
        if ch is not None and cur != ch:
            raise ParseError(f"expected {ch!r}, got {cur!r} at {self.pos}")
        self.pos += 1
        return cur

    # ---------- recursive descent ----------
    def parse(self) -> Fragment:
        frag = self.parse_alt()
        if self.pos != len(self.pat):
            raise ParseError(
                f"unexpected character {self.pat[self.pos]!r} at {self.pos}"
            )
        return frag

    def parse_alt(self) -> Fragment:
        left = self.parse_concat()
        while self.peek() == "|":
            self.eat("|")
            right = self.parse_concat()
            left = self._alt(left, right)
        return left

    def parse_concat(self) -> Fragment:
        # Build a list of fragments and concatenate them.
        frags = []
        while True:
            c = self.peek()
            if c is None or c in ")|":
                break
            frags.append(self.parse_quant())
        if not frags:
            # epsilon fragment (matches empty)
            s = State()
            out = _arrow(s, EPSILON)
            return Fragment(s, [out])
        result = frags[0]
        for f in frags[1:]:
            result.patch(f.start)
            result = Fragment(result.start, f.outs)
        return result

    def parse_quant(self) -> Fragment:
        atom = self.parse_atom()
        c = self.peek()
        if c == "*":
            self.eat()
            return self._star(atom)
        if c == "+":
            self.eat()
            return self._plus(atom)
        if c == "?":
            self.eat()
            return self._opt(atom)
        return atom

    def parse_atom(self) -> Fragment:
        c = self.peek()
        if c is None:
            raise ParseError("unexpected end of pattern in atom")
        if c == "(":
            self.eat("(")
            inner = self.parse_alt()
            self.eat(")")
            return inner
        if c == "[":
            return self.parse_class()
        if c == "\\":
            self.eat("\\")
            nxt = self.peek()
            if nxt is None:
                raise ParseError("dangling backslash")
            self.eat()
            ch = SPECIAL_ESCAPES.get(nxt, nxt)
            return self._literal(ch)
        if c == ".":
            self.eat(".")
            return self._dot()
        if c == "^":
            self.eat("^")
            return self._anchor(ANCHOR_START)
        if c == "$":
            self.eat("$")
            return self._anchor(ANCHOR_END)
        if c in "*+?|)":
            raise ParseError(f"nothing to repeat / unexpected {c!r} at {self.pos}")
        # plain literal
        self.eat()
        return self._literal(c)

    def parse_class(self) -> Fragment:
        self.eat("[")
        negated = False
        if self.peek() == "^":
            negated = True
            self.eat("^")
        chars = set()
        ranges = []
        first = True
        while True:
            c = self.peek()
            if c is None:
                raise ParseError("unterminated character class")
            if c == "]" and not first:
                self.eat("]")
                break
            first = False
            if c == "\\":
                self.eat("\\")
                nxt = self.peek()
                if nxt is None:
                    raise ParseError("dangling backslash in class")
                self.eat()
                ch = SPECIAL_ESCAPES.get(nxt, nxt)
            else:
                self.eat()
                ch = c
            # range?
            if self.peek() == "-" and self.pos + 1 < len(self.pat) and self.pat[self.pos + 1] != "]":
                self.eat("-")
                hi_c = self.peek()
                if hi_c == "\\":
                    self.eat("\\")
                    nxt = self.peek()
                    if nxt is None:
                        raise ParseError("dangling backslash in class range")
                    self.eat()
                    hi = SPECIAL_ESCAPES.get(nxt, nxt)
                else:
                    if hi_c is None:
                        raise ParseError("unterminated range in class")
                    self.eat()
                    hi = hi_c
                ranges.append((ch, hi))
            else:
                chars.add(ch)

        s = State()
        out = _arrow(s, _class_matcher(chars, ranges, negated))
        return Fragment(s, [out])

    # ---------- fragment builders ----------
    def _literal(self, ch: str) -> Fragment:
        s = State()
        out = _arrow(s, _lit_matcher(ch))
        return Fragment(s, [out])

    def _dot(self) -> Fragment:
        s = State()
        out = _arrow(s, _dot_matcher())
        return Fragment(s, [out])

    def _anchor(self, anchor) -> Fragment:
        s = State()
        out = _arrow(s, anchor)
        return Fragment(s, [out])

    def _alt(self, a: Fragment, b: Fragment) -> Fragment:
        s = State()
        pa = _arrow(s, EPSILON)
        pb = _arrow(s, EPSILON)
        pa(a.start)
        pb(b.start)
        return Fragment(s, a.outs + b.outs)

    def _star(self, a: Fragment) -> Fragment:
        s = State()
        skip = _arrow(s, EPSILON)
        loop = _arrow(s, EPSILON)
        loop(a.start)
        a.patch(s)  # body returns to the splitter
        return Fragment(s, [skip])

    def _plus(self, a: Fragment) -> Fragment:
        s = State()
        loop_back = _arrow(s, EPSILON)
        leave = _arrow(s, EPSILON)
        loop_back(a.start)
        a.patch(s)
        return Fragment(a.start, [leave])

    def _opt(self, a: Fragment) -> Fragment:
        s = State()
        take = _arrow(s, EPSILON)
        skip = _arrow(s, EPSILON)
        take(a.start)
        return Fragment(s, a.outs + [skip])


def compile_pattern(pattern: str) -> "CompiledNFA":
    parser = Parser(pattern)
    frag = parser.parse()
    accept = State(is_match=True)
    frag.patch(accept)
    return CompiledNFA(frag.start, accept, pattern)


class CompiledNFA:
    __slots__ = ("start", "accept", "pattern")

    def __init__(self, start: State, accept: State, pattern: str) -> None:
        self.start = start
        self.accept = accept
        self.pattern = pattern

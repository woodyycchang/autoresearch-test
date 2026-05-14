"""Regex parser/compiler.

Grammar (informal, precedence low to high):
    regex     := alt
    alt       := concat ('|' concat)*
    concat    := factor*
    factor    := atom ('*' | '+' | '?')?
    atom      := '(' regex ')' | charclass | '.' | '^' | '$' | escaped | literal

Anchors `^` and `$` are recorded as flags on the compiled object rather than
being baked into the NFA itself, since they require positional checks during
simulation. We model them via special "anchor" transitions handled by the
matcher.
"""

from nfa import (
    Fragment,
    State,
    make_alt,
    make_any,
    make_charclass,
    make_concat,
    make_literal,
    make_plus,
    make_question,
    make_star,
    finalize,
    EPSILON,
)


# Anchor sentinels — used as the "matcher" in a transition that the matcher
# module knows how to interpret positionally (zero-width).
ANCHOR_START = "ANCHOR_START"
ANCHOR_END = "ANCHOR_END"


class ParseError(ValueError):
    pass


class Parser:
    def __init__(self, pattern):
        self.pattern = pattern
        self.pos = 0

    def peek(self):
        if self.pos < len(self.pattern):
            return self.pattern[self.pos]
        return None

    def eat(self, ch=None):
        if self.pos >= len(self.pattern):
            raise ParseError("unexpected end of pattern")
        c = self.pattern[self.pos]
        if ch is not None and c != ch:
            raise ParseError(f"expected {ch!r} got {c!r} at {self.pos}")
        self.pos += 1
        return c

    def parse(self):
        frag = self.parse_alt()
        if self.pos != len(self.pattern):
            raise ParseError(f"unexpected character at {self.pos}: {self.peek()!r}")
        return frag

    def parse_alt(self):
        left = self.parse_concat()
        while self.peek() == "|":
            self.eat("|")
            right = self.parse_concat()
            left = make_alt(left, right)
        return left

    def parse_concat(self):
        frags = []
        while True:
            ch = self.peek()
            if ch is None or ch in ("|", ")"):
                break
            f = self.parse_factor()
            if f is not None:
                frags.append(f)
        if not frags:
            # Empty concat — produce an epsilon fragment (one state with an
            # epsilon transition out).
            s = State()

            def patch_fn(target, s=s):
                s.transitions.append((EPSILON, target))

            return Fragment(s, [patch_fn])
        result = frags[0]
        for f in frags[1:]:
            result = make_concat(result, f)
        return result

    def parse_factor(self):
        atom = self.parse_atom()
        if atom is None:
            return None
        ch = self.peek()
        if ch == "*":
            self.eat("*")
            return make_star(atom)
        if ch == "+":
            self.eat("+")
            return make_plus(atom)
        if ch == "?":
            self.eat("?")
            return make_question(atom)
        return atom

    def parse_atom(self):
        ch = self.peek()
        if ch is None:
            return None
        if ch == "(":
            self.eat("(")
            sub = self.parse_alt()
            if self.peek() != ")":
                raise ParseError("missing closing paren")
            self.eat(")")
            return sub
        if ch == "[":
            return self.parse_charclass()
        if ch == ".":
            self.eat(".")
            return make_any()
        if ch == "^":
            self.eat("^")
            return self._anchor_fragment(ANCHOR_START)
        if ch == "$":
            self.eat("$")
            return self._anchor_fragment(ANCHOR_END)
        if ch == "\\":
            self.eat("\\")
            esc = self.peek()
            if esc is None:
                raise ParseError("dangling backslash")
            self.eat()
            return self._escaped_atom(esc)
        # Literal
        self.eat()
        return make_literal(ch)

    def _anchor_fragment(self, anchor):
        s = State()

        def patch_fn(target, s=s, anchor=anchor):
            s.transitions.append((anchor, target))

        return Fragment(s, [patch_fn])

    def _escaped_atom(self, esc):
        # Common escape shortcuts
        if esc == "d":
            return make_charclass(lambda c: c.isdigit())
        if esc == "D":
            return make_charclass(lambda c: not c.isdigit())
        if esc == "w":
            return make_charclass(lambda c: c.isalnum() or c == "_")
        if esc == "W":
            return make_charclass(lambda c: not (c.isalnum() or c == "_"))
        if esc == "s":
            return make_charclass(lambda c: c.isspace())
        if esc == "S":
            return make_charclass(lambda c: not c.isspace())
        if esc == "n":
            return make_literal("\n")
        if esc == "t":
            return make_literal("\t")
        if esc == "r":
            return make_literal("\r")
        # Anything else is literal (covers \., \*, \\, \|, etc.)
        return make_literal(esc)

    def parse_charclass(self):
        self.eat("[")
        negate = False
        if self.peek() == "^":
            self.eat("^")
            negate = True
        # Collect ranges/chars.
        chars = []
        ranges = []
        first = True
        while True:
            ch = self.peek()
            if ch is None:
                raise ParseError("unterminated character class")
            if ch == "]" and not first:
                break
            first = False
            if ch == "\\":
                self.eat("\\")
                esc = self.peek()
                if esc is None:
                    raise ParseError("dangling backslash in class")
                self.eat()
                # Translate escape to a literal character for class purposes.
                actual = self._escape_char_in_class(esc)
                self._maybe_range(actual, chars, ranges)
                continue
            self.eat()
            self._maybe_range(ch, chars, ranges)
        self.eat("]")

        char_set = set(chars)

        def pred(c, char_set=char_set, ranges=ranges, negate=negate):
            hit = c in char_set
            if not hit:
                for lo, hi in ranges:
                    if lo <= c <= hi:
                        hit = True
                        break
            return (not hit) if negate else hit

        return make_charclass(pred)

    def _escape_char_in_class(self, esc):
        if esc == "n":
            return "\n"
        if esc == "t":
            return "\t"
        if esc == "r":
            return "\r"
        return esc

    def _maybe_range(self, ch, chars, ranges):
        # If next is '-' and following isn't ']', it's a range.
        if self.peek() == "-" and self.pos + 1 < len(self.pattern) and self.pattern[self.pos + 1] != "]":
            self.eat("-")
            end_ch = self.peek()
            if end_ch == "\\":
                self.eat("\\")
                esc = self.peek()
                self.eat()
                end_ch = self._escape_char_in_class(esc)
            else:
                self.eat()
            ranges.append((ch, end_ch))
        else:
            chars.append(ch)


def compile_pattern(pattern):
    """Parse pattern and return (start_state, accept_state).

    Anchors are baked into the NFA as zero-width transitions; the matcher
    enforces them per-position during simulation.
    """
    parser = Parser(pattern)
    frag = parser.parse()
    start, accept = finalize(frag)
    return start, accept

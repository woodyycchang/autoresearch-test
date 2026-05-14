"""Minimal JSON parser.

Implements parse(s) which converts a JSON string into the corresponding
Python value. Rejects invalid input with ValueError. Does not rely on
json, ast.literal_eval, eval, or exec.
"""


class _Parser:
    __slots__ = ("s", "i", "n")

    def __init__(self, s):
        if not isinstance(s, str):
            raise ValueError("input must be a string")
        self.s = s
        self.i = 0
        self.n = len(s)

    # ---- helpers -----------------------------------------------------
    def _skip_ws(self):
        while self.i < self.n and self.s[self.i] in " \t\n\r":
            self.i += 1

    def _peek(self):
        if self.i >= self.n:
            raise ValueError("unexpected end of input")
        return self.s[self.i]

    def _expect(self, ch):
        if self.i >= self.n or self.s[self.i] != ch:
            raise ValueError(f"expected {ch!r} at position {self.i}")
        self.i += 1

    # ---- top level ---------------------------------------------------
    def parse(self):
        self._skip_ws()
        value = self._parse_value()
        self._skip_ws()
        if self.i != self.n:
            raise ValueError(f"extra data at position {self.i}")
        return value

    def _parse_value(self):
        self._skip_ws()
        ch = self._peek()
        if ch == "{":
            return self._parse_object()
        if ch == "[":
            return self._parse_array()
        if ch == '"':
            return self._parse_string()
        if ch == "t" or ch == "f":
            return self._parse_bool()
        if ch == "n":
            return self._parse_null()
        if ch == "-" or ch.isdigit():
            return self._parse_number()
        raise ValueError(f"unexpected character {ch!r} at position {self.i}")

    # ---- containers --------------------------------------------------
    def _parse_object(self):
        self._expect("{")
        result = {}
        self._skip_ws()
        if self.i < self.n and self.s[self.i] == "}":
            self.i += 1
            return result
        while True:
            self._skip_ws()
            if self._peek() != '"':
                raise ValueError(f"expected string key at position {self.i}")
            key = self._parse_string()
            self._skip_ws()
            self._expect(":")
            value = self._parse_value()
            result[key] = value
            self._skip_ws()
            if self.i >= self.n:
                raise ValueError("unexpected end of object")
            ch = self.s[self.i]
            if ch == ",":
                self.i += 1
                continue
            if ch == "}":
                self.i += 1
                return result
            raise ValueError(f"expected ',' or '}}' at position {self.i}")

    def _parse_array(self):
        self._expect("[")
        result = []
        self._skip_ws()
        if self.i < self.n and self.s[self.i] == "]":
            self.i += 1
            return result
        while True:
            value = self._parse_value()
            result.append(value)
            self._skip_ws()
            if self.i >= self.n:
                raise ValueError("unexpected end of array")
            ch = self.s[self.i]
            if ch == ",":
                self.i += 1
                continue
            if ch == "]":
                self.i += 1
                return result
            raise ValueError(f"expected ',' or ']' at position {self.i}")

    # ---- strings -----------------------------------------------------
    def _parse_string(self):
        self._expect('"')
        out = []
        while self.i < self.n:
            ch = self.s[self.i]
            if ch == '"':
                self.i += 1
                return "".join(out)
            if ch == "\\":
                self.i += 1
                if self.i >= self.n:
                    raise ValueError("unterminated escape")
                esc = self.s[self.i]
                self.i += 1
                if esc == '"':
                    out.append('"')
                elif esc == "\\":
                    out.append("\\")
                elif esc == "/":
                    out.append("/")
                elif esc == "n":
                    out.append("\n")
                elif esc == "t":
                    out.append("\t")
                elif esc == "r":
                    out.append("\r")
                elif esc == "b":
                    out.append("\b")
                elif esc == "f":
                    out.append("\f")
                elif esc == "u":
                    if self.i + 4 > self.n:
                        raise ValueError("incomplete \\u escape")
                    hex_part = self.s[self.i:self.i + 4]
                    try:
                        code = int(hex_part, 16)
                    except ValueError:
                        raise ValueError(f"invalid \\u escape {hex_part!r}")
                    self.i += 4
                    out.append(chr(code))
                else:
                    raise ValueError(f"invalid escape \\{esc}")
                continue
            if ord(ch) < 0x20:
                raise ValueError(
                    f"invalid control character in string at position {self.i}"
                )
            out.append(ch)
            self.i += 1
        raise ValueError("unterminated string")

    # ---- literals ----------------------------------------------------
    def _parse_bool(self):
        if self.s.startswith("true", self.i):
            self.i += 4
            return True
        if self.s.startswith("false", self.i):
            self.i += 5
            return False
        raise ValueError(f"invalid literal at position {self.i}")

    def _parse_null(self):
        if self.s.startswith("null", self.i):
            self.i += 4
            return None
        raise ValueError(f"invalid literal at position {self.i}")

    def _parse_number(self):
        start = self.i
        if self.s[self.i] == "-":
            self.i += 1
            if self.i >= self.n or not self.s[self.i].isdigit():
                raise ValueError(f"invalid number at position {start}")
        # integer part
        if self.s[self.i] == "0":
            self.i += 1
        elif self.s[self.i].isdigit():
            while self.i < self.n and self.s[self.i].isdigit():
                self.i += 1
        else:
            raise ValueError(f"invalid number at position {start}")
        is_float = False
        # fraction
        if self.i < self.n and self.s[self.i] == ".":
            is_float = True
            self.i += 1
            if self.i >= self.n or not self.s[self.i].isdigit():
                raise ValueError(f"invalid number at position {start}")
            while self.i < self.n and self.s[self.i].isdigit():
                self.i += 1
        # exponent
        if self.i < self.n and self.s[self.i] in "eE":
            is_float = True
            self.i += 1
            if self.i < self.n and self.s[self.i] in "+-":
                self.i += 1
            if self.i >= self.n or not self.s[self.i].isdigit():
                raise ValueError(f"invalid number at position {start}")
            while self.i < self.n and self.s[self.i].isdigit():
                self.i += 1
        text = self.s[start:self.i]
        if is_float:
            return float(text)
        return int(text)


def parse(s):
    """Parse a JSON-encoded string and return the resulting Python value."""
    return _Parser(s).parse()

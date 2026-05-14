"""Tokenizer for a minimal SQL dialect.

Produces a list of Token objects. Token kinds are well-defined so the
parser can rely on them without doing additional lexical work.
"""

from dataclasses import dataclass
from typing import List, Optional


# Token kinds (string constants used as the contract between tokenizer and parser)
TOK_KEYWORD = "KEYWORD"   # CREATE, TABLE, INSERT, INTO, VALUES, SELECT, FROM, WHERE, DELETE
TOK_TYPE = "TYPE"         # INT, TEXT
TOK_IDENT = "IDENT"       # table/column names
TOK_INT = "INT"           # integer literal
TOK_STRING = "STRING"     # string literal (single-quoted)
TOK_LPAREN = "LPAREN"
TOK_RPAREN = "RPAREN"
TOK_COMMA = "COMMA"
TOK_EQ = "EQ"             # =
TOK_NEQ = "NEQ"           # !=
TOK_STAR = "STAR"         # * (not actually used per spec, but accepted)
TOK_EOF = "EOF"

KEYWORDS = {
    "CREATE",
    "TABLE",
    "INSERT",
    "INTO",
    "VALUES",
    "SELECT",
    "FROM",
    "WHERE",
    "DELETE",
}
TYPES = {"INT", "TEXT"}


@dataclass
class Token:
    kind: str
    value: object  # str for keywords/identifiers/types/strings, int for integers
    pos: int      # starting column of the token in the source (for error messages)

    def __repr__(self) -> str:  # readable in test failures
        return f"Token({self.kind}, {self.value!r}, pos={self.pos})"


class TokenizerError(Exception):
    """Raised when the source contains a character we cannot tokenize."""


def tokenize(source: str) -> List[Token]:
    """Split *source* into a list of Token objects.

    Whitespace is skipped. Identifiers are lower-cased so SQL is case-insensitive
    for keywords/types/identifiers. String literals are returned as-is, without
    their surrounding quotes.
    """
    tokens: List[Token] = []
    i = 0
    n = len(source)
    while i < n:
        c = source[i]
        if c.isspace():
            i += 1
            continue
        if c == "(":
            tokens.append(Token(TOK_LPAREN, "(", i))
            i += 1
        elif c == ")":
            tokens.append(Token(TOK_RPAREN, ")", i))
            i += 1
        elif c == ",":
            tokens.append(Token(TOK_COMMA, ",", i))
            i += 1
        elif c == "*":
            tokens.append(Token(TOK_STAR, "*", i))
            i += 1
        elif c == "=":
            tokens.append(Token(TOK_EQ, "=", i))
            i += 1
        elif c == "!":
            if i + 1 < n and source[i + 1] == "=":
                tokens.append(Token(TOK_NEQ, "!=", i))
                i += 2
            else:
                raise TokenizerError(f"unexpected character '!' at pos {i}")
        elif c == "'":
            # String literal
            start = i
            i += 1
            buf = []
            while i < n and source[i] != "'":
                buf.append(source[i])
                i += 1
            if i >= n:
                raise TokenizerError(f"unterminated string literal starting at pos {start}")
            i += 1  # consume closing quote
            tokens.append(Token(TOK_STRING, "".join(buf), start))
        elif c.isdigit() or (c == "-" and i + 1 < n and source[i + 1].isdigit()):
            start = i
            if c == "-":
                i += 1
            while i < n and source[i].isdigit():
                i += 1
            tokens.append(Token(TOK_INT, int(source[start:i]), start))
        elif c.isalpha() or c == "_":
            start = i
            while i < n and (source[i].isalnum() or source[i] == "_"):
                i += 1
            word = source[start:i]
            upper = word.upper()
            if upper in KEYWORDS:
                tokens.append(Token(TOK_KEYWORD, upper, start))
            elif upper in TYPES:
                tokens.append(Token(TOK_TYPE, upper, start))
            else:
                tokens.append(Token(TOK_IDENT, word, start))
        else:
            raise TokenizerError(f"unexpected character {c!r} at pos {i}")
    tokens.append(Token(TOK_EOF, None, n))
    return tokens

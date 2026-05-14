"""SQL tokenizer.

Produces a flat token list for the parser. Token shape:
    (token_type, value)

Token types:
    KEYWORD   - reserved words (CREATE, TABLE, INSERT, INTO, VALUES,
                SELECT, FROM, WHERE, DELETE, INT, TEXT)
    IDENT     - identifiers (table/column names)
    NUMBER    - integer literal (int value)
    STRING    - single-quoted string literal (str value, quotes stripped)
    SYMBOL    - one of ( ) , ; * = !=

This module is consumed by parser.py. The shared contract is:
- Keywords are upper-cased on emit (case-insensitive input).
- Identifiers preserve their original case.
- '!=' is a single SYMBOL token.
"""

from __future__ import annotations

KEYWORDS = {
    "CREATE", "TABLE", "INSERT", "INTO", "VALUES",
    "SELECT", "FROM", "WHERE", "DELETE", "INT", "TEXT",
    "AND",  # reserved for future use; harmless if unused
}


class TokenizerError(Exception):
    """Raised when the input cannot be tokenized."""


def tokenize(sql: str):
    """Convert a SQL string into a list of (type, value) tokens.

    Raises TokenizerError on unterminated strings or unknown characters.
    """
    if sql is None:
        raise TokenizerError("input is None")

    tokens = []
    i = 0
    n = len(sql)

    while i < n:
        ch = sql[i]

        # Skip whitespace
        if ch.isspace():
            i += 1
            continue

        # String literal: '...'
        if ch == "'":
            j = i + 1
            buf = []
            while j < n and sql[j] != "'":
                buf.append(sql[j])
                j += 1
            if j >= n:
                raise TokenizerError(f"unterminated string starting at index {i}")
            tokens.append(("STRING", "".join(buf)))
            i = j + 1
            continue

        # Number literal (support negative numbers when preceded by sign at
        # token boundary; conservative: only digits here).
        if ch.isdigit() or (ch == "-" and i + 1 < n and sql[i + 1].isdigit()
                            and (not tokens or tokens[-1][0] == "SYMBOL"
                                 and tokens[-1][1] in {"(", ","})):
            j = i
            if ch == "-":
                j += 1
            while j < n and sql[j].isdigit():
                j += 1
            tokens.append(("NUMBER", int(sql[i:j])))
            i = j
            continue

        # Identifier or keyword
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (sql[j].isalnum() or sql[j] == "_"):
                j += 1
            word = sql[i:j]
            upper = word.upper()
            if upper in KEYWORDS:
                tokens.append(("KEYWORD", upper))
            else:
                tokens.append(("IDENT", word))
            i = j
            continue

        # Two-char symbol: !=
        if ch == "!" and i + 1 < n and sql[i + 1] == "=":
            tokens.append(("SYMBOL", "!="))
            i += 2
            continue

        # Single-char symbols
        if ch in "(),;*=":
            tokens.append(("SYMBOL", ch))
            i += 1
            continue

        raise TokenizerError(f"unknown character {ch!r} at index {i}")

    return tokens

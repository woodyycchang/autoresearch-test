"""SQL parser.

Consumes tokens from tokenizer.tokenize() and produces AST node objects
that engine.py executes.

AST node types (dataclasses):
    CreateTable(name: str, columns: list[tuple[str, str]])
        - columns is a list of (col_name, col_type) where col_type in {"INT","TEXT"}
    Insert(table: str, values: list)
        - values are Python ints or strs (matching tokenizer NUMBER/STRING)
    Select(table: str, columns: list[str] | None, where: Condition | None)
        - columns=None means '*'
    Delete(table: str, where: Condition | None)
    Condition(column: str, op: str, value)
        - op is one of '=' or '!='
        - value is int or str

The parser raises ParserError on malformed input. Errors include a short
human-readable message used by tests and the engine when surfacing failures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Any


class ParserError(Exception):
    """Raised when the token stream cannot be parsed."""


@dataclass
class Condition:
    column: str
    op: str
    value: Any


@dataclass
class CreateTable:
    name: str
    columns: List[Tuple[str, str]] = field(default_factory=list)


@dataclass
class Insert:
    table: str
    values: List[Any] = field(default_factory=list)


@dataclass
class Select:
    table: str
    columns: Optional[List[str]] = None  # None means '*'
    where: Optional[Condition] = None


@dataclass
class Delete:
    table: str
    where: Optional[Condition] = None


class _Stream:
    """Tiny cursor over the token list."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset: int = 0):
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return (None, None)
        return self.tokens[idx]

    def advance(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def eat_keyword(self, word: str):
        t, v = self.peek()
        if t != "KEYWORD" or v != word:
            raise ParserError(f"expected keyword {word}, got {t} {v!r}")
        self.advance()

    def eat_symbol(self, sym: str):
        t, v = self.peek()
        if t != "SYMBOL" or v != sym:
            raise ParserError(f"expected symbol {sym!r}, got {t} {v!r}")
        self.advance()

    def at_end(self):
        return self.pos >= len(self.tokens)


def parse(tokens):
    """Parse a token list into a single AST statement node.

    Trailing semicolons are tolerated. Anything after the first statement
    (other than a single optional ';') is an error.
    """
    if not tokens:
        raise ParserError("empty input")

    s = _Stream(tokens)
    t, v = s.peek()
    if t != "KEYWORD":
        raise ParserError(f"statement must start with a keyword, got {t} {v!r}")

    if v == "CREATE":
        node = _parse_create(s)
    elif v == "INSERT":
        node = _parse_insert(s)
    elif v == "SELECT":
        node = _parse_select(s)
    elif v == "DELETE":
        node = _parse_delete(s)
    else:
        raise ParserError(f"unsupported statement: {v}")

    # Optional trailing semicolon
    if not s.at_end():
        t2, v2 = s.peek()
        if t2 == "SYMBOL" and v2 == ";":
            s.advance()
    if not s.at_end():
        t3, v3 = s.peek()
        raise ParserError(f"unexpected trailing token {t3} {v3!r}")

    return node


def _parse_create(s: _Stream) -> CreateTable:
    s.eat_keyword("CREATE")
    s.eat_keyword("TABLE")
    t, v = s.advance()
    if t != "IDENT":
        raise ParserError(f"expected table name, got {t} {v!r}")
    name = v
    s.eat_symbol("(")
    columns: List[Tuple[str, str]] = []
    while True:
        ct, cv = s.advance()
        if ct != "IDENT":
            raise ParserError(f"expected column name, got {ct} {cv!r}")
        tt, tv = s.advance()
        if tt != "KEYWORD" or tv not in ("INT", "TEXT"):
            raise ParserError(f"expected column type INT or TEXT, got {tt} {tv!r}")
        columns.append((cv, tv))
        nxt_t, nxt_v = s.peek()
        if nxt_t == "SYMBOL" and nxt_v == ",":
            s.advance()
            continue
        if nxt_t == "SYMBOL" and nxt_v == ")":
            s.advance()
            break
        raise ParserError(f"expected ',' or ')' in column list, got {nxt_t} {nxt_v!r}")
    if not columns:
        raise ParserError("CREATE TABLE requires at least one column")
    return CreateTable(name=name, columns=columns)


def _parse_insert(s: _Stream) -> Insert:
    s.eat_keyword("INSERT")
    s.eat_keyword("INTO")
    t, v = s.advance()
    if t != "IDENT":
        raise ParserError(f"expected table name, got {t} {v!r}")
    table = v
    s.eat_keyword("VALUES")
    s.eat_symbol("(")
    values: List[Any] = []
    while True:
        vt, vv = s.advance()
        if vt == "NUMBER" or vt == "STRING":
            values.append(vv)
        else:
            raise ParserError(f"expected literal value, got {vt} {vv!r}")
        nxt_t, nxt_v = s.peek()
        if nxt_t == "SYMBOL" and nxt_v == ",":
            s.advance()
            continue
        if nxt_t == "SYMBOL" and nxt_v == ")":
            s.advance()
            break
        raise ParserError(f"expected ',' or ')' in VALUES list, got {nxt_t} {nxt_v!r}")
    if not values:
        raise ParserError("INSERT requires at least one value")
    return Insert(table=table, values=values)


def _parse_select(s: _Stream) -> Select:
    s.eat_keyword("SELECT")
    t, v = s.peek()
    columns: Optional[List[str]]
    if t == "SYMBOL" and v == "*":
        s.advance()
        columns = None
    else:
        columns = []
        while True:
            ct, cv = s.advance()
            if ct != "IDENT":
                raise ParserError(f"expected column name in SELECT, got {ct} {cv!r}")
            columns.append(cv)
            nxt_t, nxt_v = s.peek()
            if nxt_t == "SYMBOL" and nxt_v == ",":
                s.advance()
                continue
            break
    s.eat_keyword("FROM")
    tt, tv = s.advance()
    if tt != "IDENT":
        raise ParserError(f"expected table name, got {tt} {tv!r}")
    table = tv
    where = _parse_optional_where(s)
    return Select(table=table, columns=columns, where=where)


def _parse_delete(s: _Stream) -> Delete:
    s.eat_keyword("DELETE")
    s.eat_keyword("FROM")
    t, v = s.advance()
    if t != "IDENT":
        raise ParserError(f"expected table name, got {t} {v!r}")
    table = v
    where = _parse_optional_where(s)
    return Delete(table=table, where=where)


def _parse_optional_where(s: _Stream) -> Optional[Condition]:
    t, v = s.peek()
    if t != "KEYWORD" or v != "WHERE":
        return None
    s.advance()
    ct, cv = s.advance()
    if ct != "IDENT":
        raise ParserError(f"expected column name in WHERE, got {ct} {cv!r}")
    ot, ov = s.advance()
    if ot != "SYMBOL" or ov not in ("=", "!="):
        raise ParserError(f"expected '=' or '!=' in WHERE, got {ot} {ov!r}")
    vt, vv = s.advance()
    if vt not in ("NUMBER", "STRING"):
        raise ParserError(f"expected literal in WHERE, got {vt} {vv!r}")
    return Condition(column=cv, op=ov, value=vv)

"""Parser for the minimal SQL dialect.

Consumes tokens produced by tokenizer.py and produces AST node dataclasses.
The AST node classes are the contract used by engine.py.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union

from tokenizer import (
    Token,
    TOK_KEYWORD,
    TOK_TYPE,
    TOK_IDENT,
    TOK_INT,
    TOK_STRING,
    TOK_LPAREN,
    TOK_RPAREN,
    TOK_COMMA,
    TOK_EQ,
    TOK_NEQ,
    TOK_EOF,
    tokenize,
)


class ParserError(Exception):
    """Raised on syntax errors."""


# ---------------------------------------------------------------------------
# AST node types
# ---------------------------------------------------------------------------

# A literal value is either int or str (matching INT/TEXT column types).
Literal = Union[int, str]


@dataclass
class ColumnDef:
    name: str
    type: str  # "INT" or "TEXT"


@dataclass
class CreateTable:
    table: str
    columns: List[ColumnDef]


@dataclass
class Insert:
    table: str
    values: List[Literal]


@dataclass
class Condition:
    column: str
    op: str  # "=" or "!="
    value: Literal


@dataclass
class Select:
    table: str
    columns: List[str]  # column names (no "*" support per spec - explicit list only)
    where: Optional[Condition] = None


@dataclass
class Delete:
    table: str
    where: Optional[Condition] = None


Statement = Union[CreateTable, Insert, Select, Delete]


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.i = 0

    # ---- token helpers ----
    def peek(self) -> Token:
        return self.tokens[self.i]

    def advance(self) -> Token:
        t = self.tokens[self.i]
        self.i += 1
        return t

    def expect_kind(self, kind: str) -> Token:
        t = self.peek()
        if t.kind != kind:
            raise ParserError(f"expected {kind} at pos {t.pos}, got {t.kind} ({t.value!r})")
        return self.advance()

    def expect_keyword(self, kw: str) -> Token:
        t = self.peek()
        if t.kind != TOK_KEYWORD or t.value != kw:
            raise ParserError(f"expected keyword {kw} at pos {t.pos}, got {t.kind} ({t.value!r})")
        return self.advance()

    # ---- top level ----
    def parse_statement(self) -> Statement:
        t = self.peek()
        if t.kind != TOK_KEYWORD:
            raise ParserError(f"expected statement keyword at pos {t.pos}, got {t.kind}")
        if t.value == "CREATE":
            stmt = self.parse_create()
        elif t.value == "INSERT":
            stmt = self.parse_insert()
        elif t.value == "SELECT":
            stmt = self.parse_select()
        elif t.value == "DELETE":
            stmt = self.parse_delete()
        else:
            raise ParserError(f"unsupported statement: {t.value!r} at pos {t.pos}")
        # Trailing junk after the statement is an error.
        if self.peek().kind != TOK_EOF:
            t = self.peek()
            raise ParserError(f"unexpected trailing token {t.kind} ({t.value!r}) at pos {t.pos}")
        return stmt

    # ---- CREATE TABLE ----
    def parse_create(self) -> CreateTable:
        self.expect_keyword("CREATE")
        self.expect_keyword("TABLE")
        name = self.expect_kind(TOK_IDENT).value
        self.expect_kind(TOK_LPAREN)
        cols: List[ColumnDef] = []
        # at least one column
        cols.append(self._parse_column_def())
        while self.peek().kind == TOK_COMMA:
            self.advance()
            cols.append(self._parse_column_def())
        self.expect_kind(TOK_RPAREN)
        return CreateTable(table=name, columns=cols)

    def _parse_column_def(self) -> ColumnDef:
        cname = self.expect_kind(TOK_IDENT).value
        ctype_tok = self.expect_kind(TOK_TYPE)
        return ColumnDef(name=cname, type=ctype_tok.value)

    # ---- INSERT ----
    def parse_insert(self) -> Insert:
        self.expect_keyword("INSERT")
        self.expect_keyword("INTO")
        name = self.expect_kind(TOK_IDENT).value
        self.expect_keyword("VALUES")
        self.expect_kind(TOK_LPAREN)
        values: List[Literal] = []
        values.append(self._parse_literal())
        while self.peek().kind == TOK_COMMA:
            self.advance()
            values.append(self._parse_literal())
        self.expect_kind(TOK_RPAREN)
        return Insert(table=name, values=values)

    def _parse_literal(self) -> Literal:
        t = self.peek()
        if t.kind == TOK_INT:
            self.advance()
            return t.value
        if t.kind == TOK_STRING:
            self.advance()
            return t.value
        raise ParserError(f"expected literal at pos {t.pos}, got {t.kind} ({t.value!r})")

    # ---- SELECT ----
    def parse_select(self) -> Select:
        self.expect_keyword("SELECT")
        cols: List[str] = []
        cols.append(self.expect_kind(TOK_IDENT).value)
        while self.peek().kind == TOK_COMMA:
            self.advance()
            cols.append(self.expect_kind(TOK_IDENT).value)
        self.expect_keyword("FROM")
        table = self.expect_kind(TOK_IDENT).value
        where = self._parse_optional_where()
        return Select(table=table, columns=cols, where=where)

    # ---- DELETE ----
    def parse_delete(self) -> Delete:
        self.expect_keyword("DELETE")
        self.expect_keyword("FROM")
        table = self.expect_kind(TOK_IDENT).value
        where = self._parse_optional_where()
        return Delete(table=table, where=where)

    # ---- WHERE ----
    def _parse_optional_where(self) -> Optional[Condition]:
        if self.peek().kind == TOK_KEYWORD and self.peek().value == "WHERE":
            self.advance()
            return self._parse_condition()
        return None

    def _parse_condition(self) -> Condition:
        col = self.expect_kind(TOK_IDENT).value
        op_tok = self.peek()
        if op_tok.kind == TOK_EQ:
            self.advance()
            op = "="
        elif op_tok.kind == TOK_NEQ:
            self.advance()
            op = "!="
        else:
            raise ParserError(
                f"expected = or != at pos {op_tok.pos}, got {op_tok.kind} ({op_tok.value!r})"
            )
        val = self._parse_literal()
        return Condition(column=col, op=op, value=val)


def parse(source: str) -> Statement:
    """Convenience: tokenize *source* and parse a single statement."""
    tokens = tokenize(source)
    return Parser(tokens).parse_statement()

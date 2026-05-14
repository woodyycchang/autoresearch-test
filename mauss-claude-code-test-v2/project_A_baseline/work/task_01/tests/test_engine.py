"""End-to-end tests for tokenizer -> parser -> engine.

Covers all 4 statement types and the error cases listed in the task spec
(bad column, type mismatch, missing table).
"""

import pytest

from tokenizer import tokenize, Token, TOK_KEYWORD, TOK_IDENT, TOK_INT, TOK_STRING, TokenizerError
from parser import (
    parse,
    Parser,
    ParserError,
    CreateTable,
    Insert,
    Select,
    Delete,
    Condition,
    ColumnDef,
)
from engine import Engine, EngineError, SelectResult


# ---------------------------------------------------------------------------
# Tokenizer sanity (one test - the rest is exercised via the engine)
# ---------------------------------------------------------------------------


def test_tokenizer_basic_create_statement():
    toks = tokenize("CREATE TABLE t (a INT, b TEXT)")
    kinds = [t.kind for t in toks]
    # CREATE TABLE t ( a INT , b TEXT ) EOF
    assert kinds == [
        TOK_KEYWORD, TOK_KEYWORD, TOK_IDENT,
        "LPAREN", TOK_IDENT, "TYPE", "COMMA",
        TOK_IDENT, "TYPE", "RPAREN", "EOF",
    ]


def test_tokenizer_rejects_bad_char():
    with pytest.raises(TokenizerError):
        tokenize("SELECT a FROM t WHERE a @ 1")


# ---------------------------------------------------------------------------
# Parser sanity
# ---------------------------------------------------------------------------


def test_parser_produces_create_ast():
    stmt = parse("CREATE TABLE users (id INT, name TEXT)")
    assert isinstance(stmt, CreateTable)
    assert stmt.table == "users"
    assert [c.name for c in stmt.columns] == ["id", "name"]
    assert [c.type for c in stmt.columns] == ["INT", "TEXT"]


def test_parser_select_with_where_neq():
    stmt = parse("SELECT id, name FROM users WHERE id != 3")
    assert isinstance(stmt, Select)
    assert stmt.table == "users"
    assert stmt.columns == ["id", "name"]
    assert stmt.where == Condition(column="id", op="!=", value=3)


def test_parser_rejects_garbage():
    with pytest.raises(ParserError):
        parse("CREATE NOT A STATEMENT")


# ---------------------------------------------------------------------------
# CREATE TABLE
# ---------------------------------------------------------------------------


def test_create_table_registers_table():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    assert "t" in eng.tables
    assert eng.tables["t"].column_names() == ["a", "b"]


def test_create_table_duplicate_raises():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT)")
    with pytest.raises(EngineError):
        eng.execute("CREATE TABLE t (b INT)")


# ---------------------------------------------------------------------------
# INSERT
# ---------------------------------------------------------------------------


def test_insert_appends_row():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'hi')")
    assert eng.tables["t"].rows == [[1, "hi"]]


def test_insert_type_mismatch_int_column_gets_text():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    with pytest.raises(EngineError) as ei:
        eng.execute("INSERT INTO t VALUES ('oops', 'hi')")
    msg = str(ei.value)
    assert "type mismatch" in msg
    assert "INT" in msg


def test_insert_type_mismatch_text_column_gets_int():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    with pytest.raises(EngineError) as ei:
        eng.execute("INSERT INTO t VALUES (1, 2)")
    assert "TEXT" in str(ei.value)


def test_insert_wrong_arity():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    with pytest.raises(EngineError):
        eng.execute("INSERT INTO t VALUES (1)")


def test_insert_into_missing_table():
    eng = Engine()
    with pytest.raises(EngineError) as ei:
        eng.execute("INSERT INTO nope VALUES (1)")
    assert "nope" in str(ei.value)


# ---------------------------------------------------------------------------
# SELECT
# ---------------------------------------------------------------------------


def test_select_all_rows_no_where():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'x')")
    eng.execute("INSERT INTO t VALUES (2, 'y')")
    res = eng.execute("SELECT a, b FROM t")
    assert isinstance(res, SelectResult)
    assert res.columns == ["a", "b"]
    assert res.rows == [[1, "x"], [2, "y"]]


def test_select_with_eq_filter():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'x')")
    eng.execute("INSERT INTO t VALUES (2, 'y')")
    res = eng.execute("SELECT a, b FROM t WHERE a = 2")
    assert res.rows == [[2, "y"]]


def test_select_with_neq_filter():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'x')")
    eng.execute("INSERT INTO t VALUES (2, 'y')")
    eng.execute("INSERT INTO t VALUES (3, 'z')")
    res = eng.execute("SELECT a FROM t WHERE b != 'y'")
    assert res.rows == [[1], [3]]


def test_select_unknown_column_raises():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    with pytest.raises(EngineError) as ei:
        eng.execute("SELECT zzz FROM t")
    assert "zzz" in str(ei.value)


def test_select_where_unknown_column_raises():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'x')")
    with pytest.raises(EngineError):
        eng.execute("SELECT a FROM t WHERE zzz = 1")


def test_select_where_type_mismatch_raises():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'x')")
    with pytest.raises(EngineError) as ei:
        eng.execute("SELECT a FROM t WHERE a = 'oops'")
    assert "type mismatch" in str(ei.value)


def test_select_missing_table():
    eng = Engine()
    with pytest.raises(EngineError) as ei:
        eng.execute("SELECT a FROM nope")
    assert "nope" in str(ei.value)


def test_select_column_subset_order_matches_query():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'x')")
    res = eng.execute("SELECT b, a FROM t")
    assert res.columns == ["b", "a"]
    assert res.rows == [["x", 1]]


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------


def test_delete_with_where_removes_only_matching():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'x')")
    eng.execute("INSERT INTO t VALUES (2, 'y')")
    eng.execute("INSERT INTO t VALUES (3, 'x')")
    removed = eng.execute("DELETE FROM t WHERE b = 'x'")
    assert removed == 2
    res = eng.execute("SELECT a, b FROM t")
    assert res.rows == [[2, "y"]]


def test_delete_without_where_clears_table():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT)")
    eng.execute("INSERT INTO t VALUES (1)")
    eng.execute("INSERT INTO t VALUES (2)")
    eng.execute("DELETE FROM t")
    res = eng.execute("SELECT a FROM t")
    assert res.rows == []


def test_select_after_delete_does_not_return_deleted_rows():
    # Targeted regression: this is one of the failure modes listed in the spec.
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'a')")
    eng.execute("INSERT INTO t VALUES (2, 'b')")
    eng.execute("DELETE FROM t WHERE a = 1")
    res = eng.execute("SELECT a, b FROM t")
    assert res.rows == [[2, "b"]]
    # Re-deleting the same row should remove 0 rows.
    assert eng.execute("DELETE FROM t WHERE a = 1") == 0


def test_delete_missing_table_raises():
    eng = Engine()
    with pytest.raises(EngineError):
        eng.execute("DELETE FROM nope")


def test_delete_unknown_where_column_raises():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT)")
    with pytest.raises(EngineError):
        eng.execute("DELETE FROM t WHERE zzz = 1")


# ---------------------------------------------------------------------------
# Cross-cutting: types are enforced consistently in WHERE for DELETE too
# ---------------------------------------------------------------------------


def test_delete_where_type_mismatch_raises():
    eng = Engine()
    eng.execute("CREATE TABLE t (a INT, b TEXT)")
    eng.execute("INSERT INTO t VALUES (1, 'x')")
    with pytest.raises(EngineError) as ei:
        eng.execute("DELETE FROM t WHERE a = 'no'")
    assert "type mismatch" in str(ei.value)

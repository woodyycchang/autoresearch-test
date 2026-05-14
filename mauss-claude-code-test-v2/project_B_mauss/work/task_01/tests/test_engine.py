"""End-to-end tests for the SQL engine.

Covers all four statement types plus the failure modes flagged in the spec:
- column type not enforced
- parser/engine type mismatch
- missing error messages
- SELECT after DELETE returning deleted rows
"""

import pytest

from tokenizer import tokenize, TokenizerError
from parser import (
    parse,
    ParserError,
    CreateTable,
    Insert,
    Select,
    Delete,
    Condition,
)
from engine import Engine, EngineError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    e = Engine()
    e.execute("CREATE TABLE users (id INT, name TEXT)")
    e.execute("INSERT INTO users VALUES (1, 'alice')")
    e.execute("INSERT INTO users VALUES (2, 'bob')")
    e.execute("INSERT INTO users VALUES (3, 'carol')")
    return e


# ---------------------------------------------------------------------------
# Tokenizer-level sanity (shared contract with parser)
# ---------------------------------------------------------------------------

def test_tokenizer_handles_keywords_and_idents():
    toks = tokenize("SELECT id FROM users")
    assert toks == [
        ("KEYWORD", "SELECT"),
        ("IDENT", "id"),
        ("KEYWORD", "FROM"),
        ("IDENT", "users"),
    ]


def test_tokenizer_neq_is_single_token():
    toks = tokenize("WHERE id != 5")
    assert ("SYMBOL", "!=") in toks
    # And not two adjacent symbols
    assert not any(
        toks[i] == ("SYMBOL", "!") and toks[i + 1] == ("SYMBOL", "=")
        for i in range(len(toks) - 1)
    )


def test_tokenizer_string_literal_quotes_stripped():
    toks = tokenize("INSERT INTO t VALUES ('hi')")
    assert ("STRING", "hi") in toks


def test_tokenizer_unterminated_string_raises():
    with pytest.raises(TokenizerError):
        tokenize("INSERT INTO t VALUES ('oops")


# ---------------------------------------------------------------------------
# Parser-level shape (parser/engine type alignment)
# ---------------------------------------------------------------------------

def test_parser_create_table_node():
    ast = parse(tokenize("CREATE TABLE t (a INT, b TEXT)"))
    assert isinstance(ast, CreateTable)
    assert ast.name == "t"
    assert ast.columns == [("a", "INT"), ("b", "TEXT")]


def test_parser_select_star_has_none_columns():
    ast = parse(tokenize("SELECT * FROM t"))
    assert isinstance(ast, Select)
    assert ast.columns is None
    assert ast.where is None


def test_parser_where_neq_produces_condition():
    ast = parse(tokenize("SELECT a FROM t WHERE a != 7"))
    assert isinstance(ast, Select)
    assert ast.where == Condition(column="a", op="!=", value=7)


def test_parser_rejects_bad_column_type():
    with pytest.raises(ParserError):
        parse(tokenize("CREATE TABLE t (a FLOAT)"))


# ---------------------------------------------------------------------------
# CREATE TABLE
# ---------------------------------------------------------------------------

def test_create_table_then_select_empty():
    e = Engine()
    e.execute("CREATE TABLE t (a INT, b TEXT)")
    assert e.execute("SELECT * FROM t") == []


def test_create_duplicate_table_raises():
    e = Engine()
    e.execute("CREATE TABLE t (a INT)")
    with pytest.raises(EngineError) as exc:
        e.execute("CREATE TABLE t (a INT)")
    assert "t" in str(exc.value)


# ---------------------------------------------------------------------------
# INSERT
# ---------------------------------------------------------------------------

def test_insert_then_select_returns_row(engine):
    rows = engine.execute("SELECT id, name FROM users WHERE id = 1")
    assert rows == [{"id": 1, "name": "alice"}]


def test_insert_into_missing_table_raises():
    e = Engine()
    with pytest.raises(EngineError) as exc:
        e.execute("INSERT INTO ghost VALUES (1, 'x')")
    assert "ghost" in str(exc.value)


def test_insert_type_mismatch_int_column_rejects_text():
    e = Engine()
    e.execute("CREATE TABLE t (a INT)")
    with pytest.raises(EngineError) as exc:
        e.execute("INSERT INTO t VALUES ('not-an-int')")
    msg = str(exc.value).lower()
    assert "type" in msg and "int" in msg


def test_insert_type_mismatch_text_column_rejects_int():
    e = Engine()
    e.execute("CREATE TABLE t (a TEXT)")
    with pytest.raises(EngineError) as exc:
        e.execute("INSERT INTO t VALUES (42)")
    msg = str(exc.value).lower()
    assert "type" in msg and "text" in msg


def test_insert_arity_mismatch_raises():
    e = Engine()
    e.execute("CREATE TABLE t (a INT, b TEXT)")
    with pytest.raises(EngineError):
        e.execute("INSERT INTO t VALUES (1)")


# ---------------------------------------------------------------------------
# SELECT
# ---------------------------------------------------------------------------

def test_select_star_returns_all_rows(engine):
    rows = engine.execute("SELECT * FROM users")
    assert len(rows) == 3
    assert {r["name"] for r in rows} == {"alice", "bob", "carol"}


def test_select_specific_columns_only(engine):
    rows = engine.execute("SELECT name FROM users WHERE id = 2")
    assert rows == [{"name": "bob"}]
    # Ensure id is not included when not requested
    assert "id" not in rows[0]


def test_select_where_neq_filters(engine):
    rows = engine.execute("SELECT name FROM users WHERE id != 2")
    names = sorted(r["name"] for r in rows)
    assert names == ["alice", "carol"]


def test_select_unknown_column_raises(engine):
    with pytest.raises(EngineError) as exc:
        engine.execute("SELECT zzz FROM users")
    assert "zzz" in str(exc.value)


def test_select_unknown_column_in_where_raises(engine):
    with pytest.raises(EngineError) as exc:
        engine.execute("SELECT name FROM users WHERE zzz = 1")
    assert "zzz" in str(exc.value)


def test_select_from_missing_table_raises():
    e = Engine()
    with pytest.raises(EngineError) as exc:
        e.execute("SELECT * FROM nope")
    assert "nope" in str(exc.value)


def test_select_where_type_mismatch_raises(engine):
    # id is INT — comparing to a TEXT literal should be flagged
    with pytest.raises(EngineError) as exc:
        engine.execute("SELECT name FROM users WHERE id = 'alice'")
    assert "type" in str(exc.value).lower()


# ---------------------------------------------------------------------------
# DELETE  (and the SELECT-after-DELETE failure mode)
# ---------------------------------------------------------------------------

def test_delete_removes_matching_row(engine):
    res = engine.execute("DELETE FROM users WHERE id = 2")
    assert res["deleted"] == 1
    rows = engine.execute("SELECT * FROM users")
    # The deleted row must NOT come back
    assert all(r["id"] != 2 for r in rows)
    assert len(rows) == 2


def test_delete_with_neq_removes_others(engine):
    engine.execute("DELETE FROM users WHERE id != 2")
    rows = engine.execute("SELECT * FROM users")
    assert rows == [{"id": 2, "name": "bob"}]


def test_delete_no_where_clears_table(engine):
    engine.execute("DELETE FROM users")
    assert engine.execute("SELECT * FROM users") == []


def test_delete_from_missing_table_raises():
    e = Engine()
    with pytest.raises(EngineError) as exc:
        e.execute("DELETE FROM ghost WHERE id = 1")
    assert "ghost" in str(exc.value)


def test_delete_then_reinsert_keeps_only_new_row(engine):
    engine.execute("DELETE FROM users WHERE id = 1")
    engine.execute("INSERT INTO users VALUES (1, 'alice2')")
    rows = engine.execute("SELECT name FROM users WHERE id = 1")
    assert rows == [{"name": "alice2"}]


# ---------------------------------------------------------------------------
# Case-insensitivity sanity (keywords only)
# ---------------------------------------------------------------------------

def test_keywords_are_case_insensitive():
    e = Engine()
    e.execute("create table t (a int, b text)")
    e.execute("insert into t values (1, 'x')")
    rows = e.execute("select * from t where a = 1")
    assert rows == [{"a": 1, "b": "x"}]

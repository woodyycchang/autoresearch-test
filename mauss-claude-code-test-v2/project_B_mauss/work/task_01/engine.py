"""In-memory SQL engine.

Executes AST nodes produced by parser.py. Public surface:

    Engine()                  - construct an empty database
    Engine.execute(sql: str)  - tokenize, parse, and execute one statement

Returns:
    CREATE / INSERT / DELETE: dict with {"status": "ok", ...details}
    SELECT: list[dict] of result rows (column -> value)

Raises:
    EngineError on table/column/type problems.
    tokenizer.TokenizerError / parser.ParserError surface unchanged.

Contract enforced here (and required by task spec):
- Column types are enforced on INSERT (INT requires Python int, TEXT
  requires Python str) and on WHERE comparison values.
- Unknown table / unknown column raise EngineError with a message
  mentioning the offending name.
- DELETE truly removes rows; subsequent SELECT must not return them.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tokenizer import tokenize
from parser import (
    parse,
    CreateTable,
    Insert,
    Select,
    Delete,
    Condition,
)


class EngineError(Exception):
    """Raised for semantic errors at execution time."""


class _Table:
    def __init__(self, name: str, columns):
        self.name = name
        # ordered list of (col_name, col_type)
        self.columns: List = list(columns)
        self.col_index: Dict[str, int] = {c: i for i, (c, _) in enumerate(self.columns)}
        self.col_types: Dict[str, str] = {c: t for c, t in self.columns}
        self.rows: List[List[Any]] = []


class Engine:
    def __init__(self):
        self.tables: Dict[str, _Table] = {}

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------
    def execute(self, sql: str):
        tokens = tokenize(sql)
        ast = parse(tokens)
        if isinstance(ast, CreateTable):
            return self._exec_create(ast)
        if isinstance(ast, Insert):
            return self._exec_insert(ast)
        if isinstance(ast, Select):
            return self._exec_select(ast)
        if isinstance(ast, Delete):
            return self._exec_delete(ast)
        raise EngineError(f"unknown AST node: {type(ast).__name__}")

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def _exec_create(self, node: CreateTable):
        if node.name in self.tables:
            raise EngineError(f"table already exists: {node.name}")
        # Validate column types (parser already does this, defense in depth)
        seen = set()
        for cname, ctype in node.columns:
            if ctype not in ("INT", "TEXT"):
                raise EngineError(f"unsupported column type: {ctype}")
            if cname in seen:
                raise EngineError(f"duplicate column name: {cname}")
            seen.add(cname)
        self.tables[node.name] = _Table(node.name, node.columns)
        return {"status": "ok", "created": node.name}

    # ------------------------------------------------------------------
    # INSERT
    # ------------------------------------------------------------------
    def _exec_insert(self, node: Insert):
        table = self._get_table(node.table)
        if len(node.values) != len(table.columns):
            raise EngineError(
                f"INSERT into {table.name} expects {len(table.columns)} "
                f"values, got {len(node.values)}"
            )
        row = []
        for (cname, ctype), val in zip(table.columns, node.values):
            self._check_type(cname, ctype, val)
            row.append(val)
        table.rows.append(row)
        return {"status": "ok", "inserted": 1}

    # ------------------------------------------------------------------
    # SELECT
    # ------------------------------------------------------------------
    def _exec_select(self, node: Select):
        table = self._get_table(node.table)

        if node.columns is None:
            cols = [c for c, _ in table.columns]
        else:
            for c in node.columns:
                if c not in table.col_index:
                    raise EngineError(
                        f"unknown column {c!r} in table {table.name}"
                    )
            cols = list(node.columns)

        self._validate_where(table, node.where)

        out: List[Dict[str, Any]] = []
        for row in table.rows:
            if self._where_matches(table, row, node.where):
                out.append({c: row[table.col_index[c]] for c in cols})
        return out

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def _exec_delete(self, node: Delete):
        table = self._get_table(node.table)
        self._validate_where(table, node.where)
        kept: List[List[Any]] = []
        removed = 0
        for row in table.rows:
            if self._where_matches(table, row, node.where):
                removed += 1
            else:
                kept.append(row)
        table.rows = kept
        return {"status": "ok", "deleted": removed}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_table(self, name: str) -> _Table:
        if name not in self.tables:
            raise EngineError(f"unknown table: {name}")
        return self.tables[name]

    def _check_type(self, cname: str, ctype: str, val: Any) -> None:
        if ctype == "INT":
            # bool is a subclass of int — reject it explicitly to keep
            # the contract honest (INT means integer).
            if not isinstance(val, int) or isinstance(val, bool):
                raise EngineError(
                    f"type mismatch for column {cname}: expected INT, "
                    f"got {type(val).__name__}"
                )
        elif ctype == "TEXT":
            if not isinstance(val, str):
                raise EngineError(
                    f"type mismatch for column {cname}: expected TEXT, "
                    f"got {type(val).__name__}"
                )
        else:  # pragma: no cover - guarded by create/parser
            raise EngineError(f"unsupported column type: {ctype}")

    def _validate_where(self, table: _Table, where: Optional[Condition]) -> None:
        if where is None:
            return
        if where.column not in table.col_index:
            raise EngineError(
                f"unknown column {where.column!r} in table {table.name}"
            )
        ctype = table.col_types[where.column]
        # Enforce literal type matches column type in WHERE
        self._check_type(where.column, ctype, where.value)

    def _where_matches(
        self, table: _Table, row, where: Optional[Condition]
    ) -> bool:
        if where is None:
            return True
        idx = table.col_index[where.column]
        cell = row[idx]
        if where.op == "=":
            return cell == where.value
        if where.op == "!=":
            return cell != where.value
        raise EngineError(f"unsupported operator: {where.op}")

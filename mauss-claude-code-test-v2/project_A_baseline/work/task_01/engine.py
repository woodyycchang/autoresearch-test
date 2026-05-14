"""In-memory SQL engine.

Reads AST nodes from parser.py and executes them against in-memory tables.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from parser import (
    parse,
    CreateTable,
    Insert,
    Select,
    Delete,
    Condition,
    ColumnDef,
    Statement,
)


class EngineError(Exception):
    """Raised on runtime / semantic errors during execution."""


@dataclass
class Table:
    name: str
    columns: List[ColumnDef]
    rows: List[List[object]] = field(default_factory=list)

    def column_names(self) -> List[str]:
        return [c.name for c in self.columns]

    def column_type(self, name: str) -> str:
        for c in self.columns:
            if c.name == name:
                return c.type
        raise EngineError(f"unknown column {name!r} in table {self.name!r}")

    def column_index(self, name: str) -> int:
        for i, c in enumerate(self.columns):
            if c.name == name:
                return i
        raise EngineError(f"unknown column {name!r} in table {self.name!r}")


# Result type for SELECT statements.
@dataclass
class SelectResult:
    columns: List[str]
    rows: List[List[object]]


class Engine:
    def __init__(self):
        self.tables: Dict[str, Table] = {}

    # ---- public entry points ----
    def execute(self, source: str):
        """Parse *source* and execute it. Returns SelectResult for SELECT, else None."""
        stmt = parse(source)
        return self.execute_stmt(stmt)

    def execute_stmt(self, stmt: Statement):
        if isinstance(stmt, CreateTable):
            return self._exec_create(stmt)
        if isinstance(stmt, Insert):
            return self._exec_insert(stmt)
        if isinstance(stmt, Select):
            return self._exec_select(stmt)
        if isinstance(stmt, Delete):
            return self._exec_delete(stmt)
        raise EngineError(f"unsupported statement type: {type(stmt).__name__}")

    # ---- CREATE TABLE ----
    def _exec_create(self, stmt: CreateTable) -> None:
        if stmt.table in self.tables:
            raise EngineError(f"table {stmt.table!r} already exists")
        # Disallow duplicate column names within the same table.
        seen = set()
        for c in stmt.columns:
            if c.name in seen:
                raise EngineError(f"duplicate column {c.name!r} in table {stmt.table!r}")
            seen.add(c.name)
            if c.type not in ("INT", "TEXT"):
                raise EngineError(f"unsupported type {c.type!r} for column {c.name!r}")
        self.tables[stmt.table] = Table(name=stmt.table, columns=list(stmt.columns))

    # ---- INSERT ----
    def _exec_insert(self, stmt: Insert) -> None:
        table = self._get_table(stmt.table)
        if len(stmt.values) != len(table.columns):
            raise EngineError(
                f"INSERT into {table.name!r}: expected {len(table.columns)} values, got {len(stmt.values)}"
            )
        row: List[object] = []
        for col, val in zip(table.columns, stmt.values):
            self._check_type(table.name, col, val)
            row.append(val)
        table.rows.append(row)

    # ---- SELECT ----
    def _exec_select(self, stmt: Select) -> SelectResult:
        table = self._get_table(stmt.table)
        # Validate selected columns exist.
        col_indices: List[int] = []
        for c in stmt.columns:
            if c not in table.column_names():
                raise EngineError(f"unknown column {c!r} in table {table.name!r}")
            col_indices.append(table.column_index(c))
        # Validate WHERE if present, including type matching.
        predicate = self._compile_where(table, stmt.where)
        out_rows: List[List[object]] = []
        for row in table.rows:
            if predicate(row):
                out_rows.append([row[i] for i in col_indices])
        return SelectResult(columns=list(stmt.columns), rows=out_rows)

    # ---- DELETE ----
    def _exec_delete(self, stmt: Delete) -> int:
        table = self._get_table(stmt.table)
        predicate = self._compile_where(table, stmt.where)
        kept: List[List[object]] = []
        removed = 0
        for row in table.rows:
            if predicate(row):
                removed += 1
            else:
                kept.append(row)
        table.rows = kept
        return removed

    # ---- helpers ----
    def _get_table(self, name: str) -> Table:
        if name not in self.tables:
            raise EngineError(f"no such table: {name!r}")
        return self.tables[name]

    def _check_type(self, table_name: str, col: ColumnDef, value: object) -> None:
        if col.type == "INT":
            # bool is a subclass of int in Python; we reject it for safety even though
            # the tokenizer cannot produce one.
            if not isinstance(value, int) or isinstance(value, bool):
                raise EngineError(
                    f"type mismatch for column {col.name!r} in table {table_name!r}: "
                    f"expected INT, got {type(value).__name__}"
                )
        elif col.type == "TEXT":
            if not isinstance(value, str):
                raise EngineError(
                    f"type mismatch for column {col.name!r} in table {table_name!r}: "
                    f"expected TEXT, got {type(value).__name__}"
                )
        else:  # pragma: no cover - guarded at CREATE time
            raise EngineError(f"unsupported column type: {col.type!r}")

    def _compile_where(self, table: Table, cond: Optional[Condition]):
        if cond is None:
            return lambda _row: True
        if cond.column not in table.column_names():
            raise EngineError(f"unknown column {cond.column!r} in table {table.name!r}")
        col_index = table.column_index(cond.column)
        col_def = table.columns[col_index]
        # Type-check the literal in WHERE against the column type.
        self._check_type(table.name, col_def, cond.value)
        op = cond.op
        rhs = cond.value
        if op == "=":
            return lambda row, ci=col_index, r=rhs: row[ci] == r
        if op == "!=":
            return lambda row, ci=col_index, r=rhs: row[ci] != r
        raise EngineError(f"unsupported operator: {op!r}")

# Scenario 09 — Add `last_login` column

## Task

Add `last_login` column to the `users` table schema. The codebase has 3 queries that interact with this table — each must be updated to handle the new column correctly.

**Constraints:**
- New column must default to NULL for existing users
- Queries using `SELECT *` must still return correct ordering
- Queries that map row tuples to dicts by position must still work

## Files
- `src/schema.py` — schema definition
- `src/queries.py` — 3 queries that depend on column order
- `src/dao.py` — data access object that wraps queries

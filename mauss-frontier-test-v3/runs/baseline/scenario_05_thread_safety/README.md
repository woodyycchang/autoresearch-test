# Scenario 05 — Make Counter thread-safe

## Task

The `Counter` class is used by multiple workers concurrently. Make ALL operations thread-safe (no lost updates, no inconsistent reads).

## Files
- `src/counter.py` — Counter class
- `src/worker.py`, `src/report.py`, `src/admin.py` — concurrent users

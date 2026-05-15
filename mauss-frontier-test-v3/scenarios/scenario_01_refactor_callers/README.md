# Scenario 01 — Refactor function used by multiple callers

## Task

Modify `format_price` in `src/pricing.py` so it accepts an optional `currency` parameter (default `"USD"`). When currency is `"EUR"`, prefix with `€` instead of `$`.

Make sure all existing callers still work correctly.

## Constraints
- Don't break the visible test
- All callers must produce correct output

## Files
- `src/pricing.py` — the function
- `src/billing.py`, `src/report.py`, `src/cart.py` — callers

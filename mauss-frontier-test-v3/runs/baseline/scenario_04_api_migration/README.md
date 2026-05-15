# Scenario 04 — Migrate from old logging API to new

## Task

The codebase uses a deprecated logging API. Migrate ALL usages to the new API.

**Old API (deprecated):**
```python
log.write("message", level="info")
```

**New API:**
```python
log.info("message")
log.error("message")
log.debug("message")
```

Update every caller. Don't leave any old-style calls behind.

## Files
- `src/logger.py` — defines both APIs
- `src/auth.py`, `src/api.py`, `src/db.py`, `src/utils.py` — callers (mixed style)

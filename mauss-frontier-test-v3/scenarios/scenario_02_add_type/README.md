# Scenario 02 — Add support for new Animal type

## Task

Add a `Snake` animal type to the system. Existing types: `Dog`, `Cat`.

Snakes:
- Make sound: "hiss"
- Move: "slither"
- Serialize as: `{"type": "snake", "name": "..."}`

The codebase has 3 places that handle animal types (`parser.py`, `behavior.py`, `serializer.py`). Update all of them.

## Files
- `src/parser.py`, `src/behavior.py`, `src/serializer.py`

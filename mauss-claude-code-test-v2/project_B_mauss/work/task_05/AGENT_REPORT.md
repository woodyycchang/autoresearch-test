# Task 05 - Minimax Chess Engine - Agent Report

## Status

PASS - 31 of 31 pytest tests passing in 0.16s on the first iteration after a
single targeted fix to one over-constrained test case.

## What was built

Three engine modules and a focused test suite live in
`/home/user/autoresearch-test/mauss-claude-code-test-v2/project_B_mauss/work/task_05/`:

- `moves.py` - Pseudo-legal move generation for queens (8 rays, sliding until
  edge / own piece / enemy capture) and kings (one step in each of the 8
  directions). `square_attacked(...)` reuses the same ray walker so check
  detection is consistent with move generation.
- `board.py` - `Board` with `parse_fen`, `legal_moves(color)` (filters
  pseudo-moves by playing make / undo and checking own king safety),
  `is_checkmate`, `is_stalemate`, `in_check`, plus in-place `make_move` /
  `unmake_move` for AI search speed.
- `ai.py` - `AIPlayer(depth=N)` running negamax with alpha-beta pruning,
  capture-first move ordering, and a material evaluator (+/-9 per queen) with
  a finite `MATE_SCORE` adjusted by depth so faster mates score higher.
- `tests/test_chess.py` - 31 tests covering FEN parsing, queen rays in all 8
  directions, blocking by friendly pieces, capture-then-stop, king step
  rules, check detection, "must address check", checkmate, stalemate,
  evaluator sign, AI legality, mate-in-one, and a free-capture preference at
  depth 1.
- `conftest.py` - Prepends the project directory to `sys.path` so tests can
  import the engine modules directly.

## Key design decisions

The square-attacked check is implemented via the same pseudo-move generator
instead of dedicated ray walks, which keeps "attack" semantics aligned with
"move" semantics (no risk of one detecting threats the other missed). The
evaluator uses a finite `MATE_SCORE = 1,000,000` (not Python's `math.inf`) so
alpha-beta arithmetic stays sane and we can subtract depth to prefer faster
mates - exactly the failure-mode-class flagged by the task spec.

## Single iteration cycle

The first run produced 30/31 passing. The failure was in
`test_ai_depth_one_picks_capture`: I had placed the black king on h8 with the
white queen on a1, putting the king already in check on the a1-h8 diagonal,
so the depth-1 AI rationally preferred capturing the king to capturing the
black queen on a8. I relocated the black king to c6, which is off the a1
rays, and re-ran pytest. All 31 tests now pass.

## Mauss handoff log

### Handoff 1 - moves.py to board.py

**ACCEPT:** `moves.py` exposes `pseudo_moves(board, color)`,
`square_attacked(board, sq, by_color)`, and `opposite(color)`, and it does
NOT filter for own-king-in-check. The "ray walker stops on first piece" rule
lives there, so `board.py` must not duplicate it.

**GIVE:** `board.py` will receive a `Board` API surface that:
- stores pieces in a `dict[(file, rank)] -> (color, kind)` keyed by 0-indexed
  squares so `moves.py` can index without conversion;
- provides `make_move` / `unmake_move` returning an undo token, because the
  caller (`legal_moves`, then the AI) needs to play / retract moves
  efficiently without copying the whole board for every pseudo-move.

**RECIPROCATE:** My contribution: the legality filter in
`Board.legal_moves`. This builds on `moves.py`'s pseudo-move generator by
wrapping each candidate in a make / `in_check` / unmake cycle, turning
pseudo-legal output into fully legal output without re-implementing ray
geometry.

### Handoff 2 - board.py to ai.py

**ACCEPT:** `Board.legal_moves` already enforces "cannot leave own king in
check", and `Board.is_checkmate` / `Board.is_stalemate` are derived from it.
The AI therefore does NOT need to perform any legality filtering of its own -
it can trust `legal_moves` is the ground truth.

**GIVE:** Risks the search code must respect:
- `make_move` mutates `Board.squares` and `Board.turn`. The AI must always
  pair every `make_move` with `unmake_move` (use `try / finally`) or
  evaluations of sibling moves will be wrong.
- The evaluator must look at `board.turn` to know whose lack of moves
  signals mate vs. stalemate.

**RECIPROCATE:** My contribution: a negamax searcher with capture-first
ordering plus a depth-aware `MATE_SCORE`. This builds on `Board.is_checkmate`
by promoting "no legal moves and in check" terminal nodes to a finite mate
score that decreases with remaining depth, so the AI prefers a mate-in-1
over a mate-in-3 - the property exercised by `test_ai_finds_mate_in_one` and
`test_ai_avoids_stalemate_when_mate_available`.

### Handoff 3 - ai.py to tests/test_chess.py

**ACCEPT:** The AI relies on `Board.legal_moves` and only ever picks from it,
and the evaluator uses signed perspective rather than raw material. Tests
must assert AI output is `in legal_moves`, not reconstruct legality.

**GIVE:** Trap to avoid when writing positions by hand: kings placed on a
queen's ray are already in check, which makes "white to move" positions
illegal and lets the AI happily "capture the king" at depth 1. The first
iteration of `test_ai_depth_one_picks_capture` hit exactly this pitfall
(black K on h8 sharing the a1-h8 diagonal with the white queen on a1). Any
hand-built test position should call `b.in_check(...)` on both sides as a
sanity check before invoking the AI.

**RECIPROCATE:** My contribution: 31 tests that exercise every failure mode
called out in the task spec (queen jumps, missed check, illegal AI move,
evaluator sign) plus the legality-precondition assertion in the depth-1
capture test. This builds on `ai.py`'s assumption that the input position is
legal by making that precondition explicit and self-checked inside the test,
so the same trap can't recur silently.

## Did Mauss change approach?

Yes, marginally. The Mauss rules pushed me to write a short legality-sanity
assertion (`assert not b.in_check('b')`) inside the failing test rather than
just relocating the king - making the "give" (the trap I had fallen into)
visible to whoever maintains the test next. Without the rules I would
probably have just moved the piece silently.

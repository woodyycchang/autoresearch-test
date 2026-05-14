# Task 05: Minimax Chess Engine (King + Queen only)

## Description

Simplified chess: only Kings and one Queen each side, 8x8 board.
- `Board.parse_fen(fen)` — read position
- `Board.legal_moves(color)` — all legal moves (must respect: queen moves, king moves, check, no moving into check, capture)
- `Board.is_checkmate(color)`, `Board.is_stalemate(color)`
- `AIPlayer(depth=3)` — picks best move using minimax with alpha-beta
- Evaluator: +9 for queen, +∞ for checkmate against opponent, -∞ for own checkmate

**Required files:**
- `board.py`, `moves.py`, `ai.py`
- `tests/test_chess.py` — 20+ tests: queen moves correct in all 8 directions, blocked by king, capture works, check detection, mate-in-1 problems

Failure modes: queen jumps over pieces, doesn't detect check, AI makes illegal move, evaluator wrong sign.

## Your job

Build all required files. Write the unit tests. Run tests with pytest.

**Pass criteria:** ALL tests pass with `pytest tests/` returning 0 errors and 0 failures.

When done, write a 1-line summary to `task_05_output.txt`:
- "PASS - X/X tests pass" if all pass
- "PARTIAL - X/Y tests pass" if some fail
- "FAIL - reason" if you couldn't build it

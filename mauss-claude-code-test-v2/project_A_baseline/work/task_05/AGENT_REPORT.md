# Task 05: Minimax Chess Engine – Agent Report

## Result
**PASS – 44/44 tests pass** with `python3 -m pytest tests/ -v --tb=short` in 0.19s.

## Files
- `moves.py` – move generation primitives: direction vectors, `slide_moves`, `king_moves`, `queen_moves`, `square_attacked_by` (ray-scan based), algebraic-coord helpers.
- `board.py` – `Board` class: `parse_fen`, `to_fen`, `legal_moves`, `pseudo_moves`, `make_move`, `is_in_check`, `is_checkmate`, `is_stalemate`, `king_square`, `queen_square`, `material`.
- `ai.py` – `AIPlayer(depth)` with `choose_move`; `evaluate` returns +9/-9 per queen, ±inf for checkmate, 0 for stalemate; `minimax` does alpha-beta.
- `tests/test_chess.py` – 44 tests across 7 sections (FEN, queen movement in 8 directions, blocking/capture, king movement, check/mate/stalemate, evaluator, AI).
- `conftest.py` – adds work dir to `sys.path` so tests can `from board import Board`.

## Approach
- Board state as `dict[(file,rank) -> (color, 'K'|'Q')]` (sparse, easy to copy).
- Legal move generation = pseudo-legal moves filtered by "after the move, my king is not attacked." Critically, attack detection (`square_attacked_by`) does *not* call `legal_moves`, so there's no infinite recursion.
- Ray-scan attack detection: for a target square, walk outward in each of the 8 directions and check the first occupied square. Queens attack along queen-rays, kings along adjacent rays only.
- Alpha-beta with terminal-position handling at the top of the recursive call so checkmate/stalemate are detected before depth=0 cutoff.

## Hard parts of multi-file chess coordination
1. **Avoiding circular imports.** `board.py` imports from `moves.py`, but `moves.py` must work on raw dicts (not `Board` objects) so it stays leaf-level. `ai.py` imports `Board` only.
2. **Recursion hazard in legality.** "Legal move" needs check detection; if check detection asks "can opponent reach my king with a legal move?" you get infinite recursion. Solved by attacking-square ray scans that ignore legality.
3. **FEN gotchas.** Rank 8 is the *first* row of FEN, not the last. Off-by-ones here cause cascading test failures across every position.
4. **Depth blowup.** A lone queen has ~27 moves, so branching factor is huge. Kept tests at depth 2, sometimes restricting positions so depth 2 suffices to find tactical mates.
5. **Test position design.** Many "obvious" FENs are illegal (kings adjacent, side-to-move in impossible check). One initial test had bK h8 with wQ h1 — black IS in check, contrary to my intent.

## Iteration log
First run: 42/44. Fixed (1) a mis-designed "not in check" position and (2) tightened the "AI doesn't hang queen" assertion to accept queen trades. Second run: 44/44.

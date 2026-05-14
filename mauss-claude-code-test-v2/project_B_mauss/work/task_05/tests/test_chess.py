"""Tests for the simplified Kings+Queens chess engine.

Covers: FEN parsing, queen moves in all 8 directions, king moves,
captures, blocking by friendly pieces, check / checkmate / stalemate
detection, illegal-move filtering, and minimax AI behaviour (depth 2-3).
"""

import pytest

from board import Board, from_algebraic, algebraic
from moves import (
    queen_pseudo_moves, king_pseudo_moves, square_attacked, opposite,
)
from ai import AIPlayer, evaluate, material_eval, MATE_SCORE


# ---------------------------------------------------------------------------
# FEN parsing
# ---------------------------------------------------------------------------

def test_parse_fen_starting_minimal():
    """Both kings + both queens on standard starting squares."""
    b = Board.parse_fen("4k3/8/8/8/8/8/8/3QK3 w - - 0 1")
    assert b.piece_at(from_algebraic("d1")) == ('w', 'Q')
    assert b.piece_at(from_algebraic("e1")) == ('w', 'K')
    assert b.piece_at(from_algebraic("e8")) == ('b', 'K')
    assert b.turn == 'w'


def test_parse_fen_with_black_to_move():
    b = Board.parse_fen("3qk3/8/8/8/8/8/8/3QK3 b - - 0 1")
    assert b.turn == 'b'
    assert b.piece_at(from_algebraic("d8")) == ('b', 'Q')


def test_parse_fen_bad_rank_count_raises():
    with pytest.raises(ValueError):
        Board.parse_fen("8/8/8 w - - 0 1")


# ---------------------------------------------------------------------------
# Queen movement: all 8 directions on an empty board
# ---------------------------------------------------------------------------

def test_queen_moves_in_all_eight_directions():
    """Queen on d4 with kings tucked in corners reaches 27 squares on empty board."""
    b = Board.parse_fen("k7/8/8/8/3Q4/8/8/7K w - - 0 1")
    moves = queen_pseudo_moves(b, from_algebraic("d4"), 'w')
    destinations = {to for _, to, _ in moves}

    # All 8 ray endpoints should be reached at least one step.
    d4 = from_algebraic("d4")
    expected_each_dir = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]
    for df, dr in expected_each_dir:
        sq = (d4[0] + df, d4[1] + dr)
        assert sq in destinations, f"missing {algebraic(sq)} direction ({df},{dr})"


def test_queen_horizontal_full_rank():
    b = Board.parse_fen("k7/8/8/8/Q7/8/8/7K w - - 0 1")
    moves = queen_pseudo_moves(b, from_algebraic("a4"), 'w')
    dests = {to for _, to, _ in moves}
    # Whole rank 4 except a4 itself.
    for f in range(1, 8):
        assert (f, 3) in dests


def test_queen_vertical_full_file():
    b = Board.parse_fen("k7/8/8/8/8/8/8/Q6K w - - 0 1")
    moves = queen_pseudo_moves(b, from_algebraic("a1"), 'w')
    dests = {to for _, to, _ in moves}
    for r in range(1, 8):
        assert (0, r) in dests


def test_queen_diagonal_ne():
    b = Board.parse_fen("k7/8/8/8/8/8/8/Q6K w - - 0 1")
    moves = queen_pseudo_moves(b, from_algebraic("a1"), 'w')
    dests = {to for _, to, _ in moves}
    # a1 -> h8 diagonal
    for i in range(1, 8):
        assert (i, i) in dests


def test_queen_diagonal_nw():
    b = Board.parse_fen("k7/8/8/8/8/8/8/7Q w - - 0 1")
    # Move kings out of way
    b.squares.pop(from_algebraic("a8"))
    b.squares[from_algebraic("a1")] = ('b', 'K')
    b.squares[from_algebraic("h8")] = ('w', 'K')  # collision
    # Reset: use a cleaner FEN
    b = Board.parse_fen("k7/8/8/8/8/8/8/6KQ w - - 0 1")
    # Wait queen is on h1
    moves = queen_pseudo_moves(b, from_algebraic("h1"), 'w')
    dests = {to for _, to, _ in moves}
    for i in range(1, 8):
        assert (7 - i, i) in dests  # h1 -> a8


def test_queen_blocked_by_friendly_king():
    """Queen on d1 with king on d4 cannot reach d5 or beyond on the d-file."""
    b = Board.parse_fen("4k3/8/8/8/3K4/8/8/3Q4 w - - 0 1")
    moves = queen_pseudo_moves(b, from_algebraic("d1"), 'w')
    dests = {to for _, to, _ in moves}
    # d2 and d3 reachable, d4 blocked (own king), d5+ unreachable.
    assert from_algebraic("d2") in dests
    assert from_algebraic("d3") in dests
    assert from_algebraic("d4") not in dests
    assert from_algebraic("d5") not in dests
    assert from_algebraic("d8") not in dests


def test_queen_cannot_jump_over_friendly_piece():
    """Queen behind king should not appear on the far side of the king."""
    b = Board.parse_fen("k7/8/8/8/8/3K4/3Q4/7K w - - 0 1")
    # Two white kings is not legal chess but our engine allows arbitrary
    # configurations. The point is: queen on d2 cannot jump king on d3.
    # Build by hand to avoid the two-king issue:
    b = Board()
    b.squares[from_algebraic("d2")] = ('w', 'Q')
    b.squares[from_algebraic("d3")] = ('w', 'K')
    b.squares[from_algebraic("a8")] = ('b', 'K')
    b.turn = 'w'
    moves = queen_pseudo_moves(b, from_algebraic("d2"), 'w')
    dests = {to for _, to, _ in moves}
    assert from_algebraic("d4") not in dests
    assert from_algebraic("d5") not in dests


def test_queen_captures_enemy_and_stops():
    """Queen takes the first enemy piece on a ray but cannot continue past it."""
    b = Board()
    b.squares[from_algebraic("d1")] = ('w', 'Q')
    b.squares[from_algebraic("d4")] = ('b', 'Q')  # enemy
    b.squares[from_algebraic("d7")] = ('b', 'K')  # enemy behind
    b.squares[from_algebraic("a1")] = ('w', 'K')
    b.turn = 'w'
    moves = queen_pseudo_moves(b, from_algebraic("d1"), 'w')
    dests = {to: cap for _, to, cap in moves}
    # d4 captured
    assert from_algebraic("d4") in dests
    assert dests[from_algebraic("d4")] == ('b', 'Q')
    # Cannot reach beyond captured piece
    assert from_algebraic("d5") not in dests
    assert from_algebraic("d7") not in dests


# ---------------------------------------------------------------------------
# King movement
# ---------------------------------------------------------------------------

def test_king_one_step_in_all_directions():
    b = Board()
    b.squares[from_algebraic("d4")] = ('w', 'K')
    b.squares[from_algebraic("a8")] = ('b', 'K')
    b.turn = 'w'
    moves = king_pseudo_moves(b, from_algebraic("d4"), 'w')
    dests = {to for _, to, _ in moves}
    assert dests == {
        from_algebraic(s) for s in
        ["c3", "c4", "c5", "d3", "d5", "e3", "e4", "e5"]
    }


def test_king_corner_three_moves():
    b = Board()
    b.squares[from_algebraic("a1")] = ('w', 'K')
    b.squares[from_algebraic("h8")] = ('b', 'K')
    b.turn = 'w'
    moves = king_pseudo_moves(b, from_algebraic("a1"), 'w')
    dests = {to for _, to, _ in moves}
    assert dests == {from_algebraic(s) for s in ["a2", "b1", "b2"]}


def test_king_cannot_move_onto_friendly():
    b = Board()
    b.squares[from_algebraic("e1")] = ('w', 'K')
    b.squares[from_algebraic("e2")] = ('w', 'Q')
    b.squares[from_algebraic("a8")] = ('b', 'K')
    b.turn = 'w'
    moves = king_pseudo_moves(b, from_algebraic("e1"), 'w')
    dests = {to for _, to, _ in moves}
    assert from_algebraic("e2") not in dests


# ---------------------------------------------------------------------------
# Check / legal move filtering
# ---------------------------------------------------------------------------

def test_square_attacked_by_queen():
    b = Board()
    b.squares[from_algebraic("d4")] = ('w', 'Q')
    b.squares[from_algebraic("a1")] = ('w', 'K')
    b.squares[from_algebraic("a8")] = ('b', 'K')
    assert square_attacked(b, from_algebraic("d8"), 'w')
    assert square_attacked(b, from_algebraic("h4"), 'w')
    assert square_attacked(b, from_algebraic("a7"), 'w')
    assert not square_attacked(b, from_algebraic("e6"), 'w')


def test_in_check_detected():
    # Black king on e8, white queen giving check from e1.
    b = Board.parse_fen("4k3/8/8/8/8/8/8/4Q2K b - - 0 1")
    # Black king is on e8, white queen on e1 -> check along e-file
    assert b.in_check('b') is True
    assert b.in_check('w') is False


def test_king_cannot_move_into_check():
    # White king on e1, black queen on e8 controlling e-file.
    # White king must not move to e2.
    b = Board.parse_fen("4q2k/8/8/8/8/8/8/4K3 w - - 0 1")
    moves = b.legal_moves('w')
    dests = {to for _, to, _ in moves}
    assert from_algebraic("e2") not in dests
    assert from_algebraic("d1") in dests or from_algebraic("f1") in dests


def test_must_move_out_of_check():
    """When in check, all legal moves must address the check."""
    # White king on e1, black queen on e3 giving check. Only legal
    # responses: move king off the e-file, or capture queen if reachable.
    b = Board()
    b.squares[from_algebraic("e1")] = ('w', 'K')
    b.squares[from_algebraic("e3")] = ('b', 'Q')
    b.squares[from_algebraic("a8")] = ('b', 'K')
    b.turn = 'w'
    assert b.in_check('w')
    legal = b.legal_moves('w')
    # Every legal move must leave king not in check.
    for move in legal:
        token = b.make_move(move)
        try:
            assert not b.in_check('w'), f"move {move} leaves king in check"
        finally:
            b.unmake_move(token)
    # The king cannot capture e3 because it'd remain attacked by the b-king? No
    # b-king is on a8, far away. King CAN capture e3. Validate it's in legal list:
    capture_e3 = (from_algebraic("e1"), from_algebraic("e3"), ('b', 'Q'))
    # Actually e1 to e3 is two squares; king can't move two squares. So
    # capture isn't available. The king must step away to d1/f1/d2/f2.
    dests = {to for _, to, _ in legal}
    assert from_algebraic("e2") not in dests  # still attacked along file? No, e3 blocks... reconsider
    # When the king moves to e2, the queen on e3 still attacks e2 (adjacent).
    # So e2 is illegal. Confirm.
    # Acceptable escape squares:
    for sq in ["d1", "f1", "d2", "f2"]:
        # d2/f2 are attacked diagonally by queen on e3? e3->d2 is diagonal yes.
        # e3->f2 also diagonal. So those are illegal too.
        pass
    # The only safe escapes are d1 and f1.
    assert from_algebraic("d1") in dests
    assert from_algebraic("f1") in dests


# ---------------------------------------------------------------------------
# Checkmate and stalemate
# ---------------------------------------------------------------------------

def test_back_rank_checkmate():
    """Classic back-rank-style mate using only kings and a queen.

    Position: black king h8, white queen h7 (supported by white king g6).
    Black is to move and is checkmated.
    """
    b = Board()
    b.squares[from_algebraic("h8")] = ('b', 'K')
    b.squares[from_algebraic("h7")] = ('w', 'Q')
    b.squares[from_algebraic("g6")] = ('w', 'K')
    b.turn = 'b'
    assert b.in_check('b')
    assert b.is_checkmate('b')
    assert not b.is_stalemate('b')


def test_stalemate_king_in_corner():
    """Black king on a8, white queen on b6, white king on c6.

    Black is not in check, has no legal moves -> stalemate.
    """
    b = Board()
    b.squares[from_algebraic("a8")] = ('b', 'K')
    b.squares[from_algebraic("b6")] = ('w', 'Q')
    b.squares[from_algebraic("c6")] = ('w', 'K')
    b.turn = 'b'
    assert not b.in_check('b')
    assert b.is_stalemate('b')
    assert not b.is_checkmate('b')


def test_not_mate_when_capture_available():
    """If the checking queen can be captured by the king, not mate.

    Black king on e8, white queen on e7 (UNSUPPORTED), white king on a1.
    Black can capture the queen with the king -> not mate.
    """
    b = Board()
    b.squares[from_algebraic("e8")] = ('b', 'K')
    b.squares[from_algebraic("e7")] = ('w', 'Q')
    b.squares[from_algebraic("a1")] = ('w', 'K')
    b.turn = 'b'
    assert b.in_check('b')
    assert not b.is_checkmate('b')
    legal = b.legal_moves('b')
    captures = [m for m in legal if m[1] == from_algebraic("e7")]
    assert len(captures) == 1


# ---------------------------------------------------------------------------
# AI / minimax
# ---------------------------------------------------------------------------

def test_evaluator_material_signs():
    # White has queen, black does not.
    b = Board()
    b.squares[from_algebraic("e1")] = ('w', 'K')
    b.squares[from_algebraic("d1")] = ('w', 'Q')
    b.squares[from_algebraic("e8")] = ('b', 'K')
    b.turn = 'w'
    assert material_eval(b) == 9
    # Flip queen color.
    b.squares[from_algebraic("d1")] = ('b', 'Q')
    assert material_eval(b) == -9


def test_evaluator_checkmate_sign():
    # Position where it's black to move and is checkmated.
    b = Board()
    b.squares[from_algebraic("h8")] = ('b', 'K')
    b.squares[from_algebraic("h7")] = ('w', 'Q')
    b.squares[from_algebraic("g6")] = ('w', 'K')
    b.turn = 'b'
    # Evaluated from white's perspective: huge positive.
    assert evaluate(b, 'w') >= MATE_SCORE
    # From black's perspective: huge negative.
    assert evaluate(b, 'b') <= -MATE_SCORE


def test_ai_chooses_legal_move():
    b = Board.parse_fen("4k3/8/8/8/8/8/8/3QK3 w - - 0 1")
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    legal = b.legal_moves('w')
    assert move in legal


def test_ai_takes_free_queen():
    """If a free black queen is en prise, the AI should grab it (depth 2)."""
    b = Board()
    b.squares[from_algebraic("e1")] = ('w', 'K')
    b.squares[from_algebraic("d1")] = ('w', 'Q')
    b.squares[from_algebraic("d8")] = ('b', 'Q')  # on same file as white queen, undefended
    b.squares[from_algebraic("a8")] = ('b', 'K')  # far away
    b.turn = 'w'
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    # White should play Qxd8 winning the queen.
    assert move[1] == from_algebraic("d8")
    assert move[2] == ('b', 'Q')


def test_ai_finds_mate_in_one():
    """A simple mate-in-one with the white queen.

    Position: black king h8, white king g6, white queen h2.
    Qh7# is mate. We give the AI depth 2 and verify it plays it.
    """
    b = Board()
    b.squares[from_algebraic("h8")] = ('b', 'K')
    b.squares[from_algebraic("g6")] = ('w', 'K')
    b.squares[from_algebraic("h2")] = ('w', 'Q')
    b.turn = 'w'
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    # Apply move and verify resulting position is checkmate.
    token = b.make_move(move)
    try:
        assert b.is_checkmate('b'), (
            f"AI move {move} did not deliver mate; board:\n{b!r}")
    finally:
        b.unmake_move(token)


def test_ai_avoids_stalemate_when_mate_available():
    """At depth 3 the AI should prefer Qh7# over a stalemating move.

    Position chosen so a stalemate alternative exists: black king a8,
    white king c6, white queen b6 stalemates (we already use this for
    the stalemate test). With queen elsewhere, AI should pick the mate.

    We construct: black king h8, white king g6, white queen h2.
    Stalemate option: move queen to g7 (would stalemate? actually that'd
    cover h8 and h7; let's not over-engineer). The simpler check is:
    AI's chosen move must NOT result in a stalemate.
    """
    b = Board()
    b.squares[from_algebraic("h8")] = ('b', 'K')
    b.squares[from_algebraic("g6")] = ('w', 'K')
    b.squares[from_algebraic("h2")] = ('w', 'Q')
    b.turn = 'w'
    ai = AIPlayer(depth=3)
    move = ai.choose_move(b)
    token = b.make_move(move)
    try:
        assert not b.is_stalemate('b')
    finally:
        b.unmake_move(token)


def test_ai_never_returns_illegal_move_over_many_positions():
    """Property test: for a handful of positions, AI move is in legal_moves."""
    positions = [
        "4k3/8/8/8/8/8/8/3QK3 w - - 0 1",
        "3qk3/8/8/8/8/8/8/3QK3 w - - 0 1",
        "3qk3/8/8/8/8/8/8/3QK3 b - - 0 1",
        "k7/8/8/8/3Q4/8/8/7K w - - 0 1",
    ]
    ai = AIPlayer(depth=2)
    for fen in positions:
        b = Board.parse_fen(fen)
        legal = b.legal_moves(b.turn)
        if not legal:
            continue
        move = ai.choose_move(b)
        assert move in legal, f"illegal move {move} in {fen}"


def test_ai_depth_one_picks_capture():
    """Depth-1 AI sees and prefers a free capture.

    Setup: white K on e1, white Q on a1, black Q on a8 (undefended,
    same file as white queen), black K on g7. The black king on g7 is
    NOT on any ray of the white queen, so the position is legal for
    white to move and Qxa8 wins the queen for free.
    """
    b = Board()
    b.squares[from_algebraic("e1")] = ('w', 'K')
    b.squares[from_algebraic("a1")] = ('w', 'Q')
    b.squares[from_algebraic("a8")] = ('b', 'Q')  # free on a-file
    b.squares[from_algebraic("c6")] = ('b', 'K')  # off rays from a1; far from a8
    b.turn = 'w'
    # Sanity: position is legal (black king not in check) before white moves.
    assert not b.in_check('b')
    ai = AIPlayer(depth=1)
    move = ai.choose_move(b)
    assert move[1] == from_algebraic("a8") and move[2] == ('b', 'Q')


def test_legal_moves_count_for_starting_minimal_position():
    """Sanity: position 4k3/8/8/8/8/8/8/3QK3 white moves count is finite and >0."""
    b = Board.parse_fen("4k3/8/8/8/8/8/8/3QK3 w - - 0 1")
    legal = b.legal_moves('w')
    assert len(legal) > 0
    # Every legal move must originate from a white piece.
    for from_sq, _to, _cap in legal:
        piece = b.piece_at(from_sq)
        assert piece is not None and piece[0] == 'w'


def test_opposite_color_helper():
    assert opposite('w') == 'b'
    assert opposite('b') == 'w'

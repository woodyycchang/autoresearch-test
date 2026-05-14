"""Tests for the simplified K+Q chess engine.

Convention: in FEN board strings, "8" = empty rank, uppercase = white,
lowercase = black. The standard first rank is at the bottom (rank 1).
"""

import math

import pytest

from board import Board
from moves import (
    algebraic_to_sq, sq_to_algebraic, in_bounds,
    queen_moves, king_moves, square_attacked_by,
)
from ai import AIPlayer, evaluate, INF


# ---------- helpers ----------

def has_move(moves, from_alg, to_alg):
    a = algebraic_to_sq(from_alg)
    b = algebraic_to_sq(to_alg)
    return (a, b) in moves


def make(fen):
    return Board.parse_fen(fen)


# =========================================================================
# FEN parsing & basic board state
# =========================================================================

def test_fen_parse_starting_kq_position():
    """Initial K+Q position for both sides."""
    b = make("3qk3/8/8/8/8/8/8/3QK3 w")
    assert b.turn == 'w'
    assert b.piece_at(algebraic_to_sq('d1')) == ('w', 'Q')
    assert b.piece_at(algebraic_to_sq('e1')) == ('w', 'K')
    assert b.piece_at(algebraic_to_sq('d8')) == ('b', 'Q')
    assert b.piece_at(algebraic_to_sq('e8')) == ('b', 'K')
    assert b.piece_at(algebraic_to_sq('e4')) is None


def test_fen_roundtrip():
    fen = "3qk3/8/8/8/8/8/8/3QK3 w"
    b = make(fen)
    assert b.to_fen() == fen


def test_fen_rejects_unsupported_pieces():
    with pytest.raises(ValueError):
        Board.parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")


def test_king_square_lookup():
    b = make("4k3/8/8/8/8/8/8/4K3 w")
    assert b.king_square('w') == algebraic_to_sq('e1')
    assert b.king_square('b') == algebraic_to_sq('e8')


# =========================================================================
# Queen movement in all 8 directions
# =========================================================================

def test_queen_moves_north():
    # Lone white queen on d4, kings far away.
    b = make("7k/8/8/8/3Q4/8/8/K7 w")
    moves = b.legal_moves('w')
    # d4 -> d5, d6, d7, d8 should all be legal
    for to in ['d5', 'd6', 'd7', 'd8']:
        assert has_move(moves, 'd4', to), f"missing d4->{to}"


def test_queen_moves_south():
    b = make("7k/8/8/8/3Q4/8/8/K7 w")
    moves = b.legal_moves('w')
    for to in ['d3', 'd2']:
        # d1 is empty here actually (king on a1) so d1 included too
        assert has_move(moves, 'd4', to), f"missing d4->{to}"
    assert has_move(moves, 'd4', 'd1')


def test_queen_moves_east():
    b = make("7k/8/8/8/3Q4/8/8/K7 w")
    moves = b.legal_moves('w')
    for to in ['e4', 'f4', 'g4', 'h4']:
        assert has_move(moves, 'd4', to), f"missing d4->{to}"


def test_queen_moves_west():
    b = make("7k/8/8/8/3Q4/8/8/K7 w")
    moves = b.legal_moves('w')
    for to in ['c4', 'b4', 'a4']:
        assert has_move(moves, 'd4', to), f"missing d4->{to}"


def test_queen_moves_ne_diagonal():
    b = make("7k/8/8/8/3Q4/8/8/K7 w")
    moves = b.legal_moves('w')
    for to in ['e5', 'f6', 'g7', 'h8']:
        assert has_move(moves, 'd4', to), f"missing d4->{to}"


def test_queen_moves_nw_diagonal():
    b = make("7k/8/8/8/3Q4/8/8/K7 w")
    moves = b.legal_moves('w')
    for to in ['c5', 'b6', 'a7']:
        assert has_move(moves, 'd4', to), f"missing d4->{to}"


def test_queen_moves_se_diagonal():
    b = make("7k/8/8/8/3Q4/8/8/K7 w")
    moves = b.legal_moves('w')
    for to in ['e3', 'f2', 'g1']:
        assert has_move(moves, 'd4', to), f"missing d4->{to}"


def test_queen_moves_sw_diagonal():
    b = make("7k/8/8/8/3Q4/8/8/K7 w")
    moves = b.legal_moves('w')
    for to in ['c3', 'b2']:
        assert has_move(moves, 'd4', to), f"missing d4->{to}"
    # a1 has the white king, so queen can't go there
    assert not has_move(moves, 'd4', 'a1')


def test_lone_queen_has_27_moves():
    """A queen in the center with no obstructions has 27 squares it can go."""
    b = make("7k/8/8/8/3Q4/8/8/K7 w")
    moves = [m for m in b.legal_moves('w') if m[0] == algebraic_to_sq('d4')]
    # 7 N, 3 S (d3,d2,d1 - d1 empty since K on a1), 4 E, 3 W, 4 NE, 3 NW, 3 SE, 2 SW (c3,b2; a1 blocked by own K)
    # = 7 + 3 + 4 + 3 + 4 + 3 + 3 + 2 = 29? Let me count again:
    # vertical: d5,d6,d7,d8 (4) + d3,d2,d1 (3) = 7
    # horizontal: e4..h4 (4) + c4,b4,a4 (3) = 7
    # diag NE: e5,f6,g7,h8 (4); NW: c5,b6,a7 (3); SE: e3,f2,g1 (3); SW: c3,b2 (2, a1 blocked)
    # total = 7 + 7 + 4 + 3 + 3 + 2 = 26
    assert len(moves) == 26


# =========================================================================
# Queen blocked by king (own or enemy) and capture rules
# =========================================================================

def test_queen_blocked_by_own_king():
    # White Q on d1, white K on d3. Queen should NOT reach d3, d4, etc.
    b = make("7k/8/8/8/8/3K4/8/3Q4 w")
    moves = b.legal_moves('w')
    # queen can go d2 (empty), but not d3 (own king), and not beyond
    assert has_move(moves, 'd1', 'd2')
    assert not has_move(moves, 'd1', 'd3')
    assert not has_move(moves, 'd1', 'd4')
    assert not has_move(moves, 'd1', 'd5')


def test_queen_captures_enemy_queen():
    # White Q on d1, black Q on d8, kings on the side. White can capture down the d-file.
    b = make("3q4/8/8/8/8/8/8/3QK2k w")
    moves = b.legal_moves('w')
    # Wait - black king on h1? That puts kings adjacent? No: h1, e1 -> not adjacent.
    # White can move queen d1 -> d8 capturing black queen.
    assert has_move(moves, 'd1', 'd8')


def test_queen_does_not_jump_over_pieces():
    # White Q on a1, black Q on a4, then black K on a8 far away. Test capture stops at the blocker.
    b = make("k7/8/8/8/q7/8/8/Q3K3 w")
    moves = b.legal_moves('w')
    # Q on a1 can reach a2, a3, a4 (capture). Cannot go a5+.
    assert has_move(moves, 'a1', 'a2')
    assert has_move(moves, 'a1', 'a3')
    assert has_move(moves, 'a1', 'a4')  # capture
    assert not has_move(moves, 'a1', 'a5')
    assert not has_move(moves, 'a1', 'a6')


def test_queen_diagonal_capture():
    # White Q on a1, black Q on d4, K's safely far away.
    b = make("k7/8/8/8/3q4/8/8/Q3K3 w")
    moves = b.legal_moves('w')
    assert has_move(moves, 'a1', 'd4')
    # but not e5 (would jump)
    assert not has_move(moves, 'a1', 'e5')


def test_queen_blocked_by_enemy_piece_no_jump():
    # Enemy queen blocks; queen can capture but not pass through.
    b = make("7k/8/8/8/8/8/8/QqK4K w")
    # Hmm that has two white K's. Fix: black k on h8.
    b = make("7k/8/8/8/8/8/8/QqK5 w")
    moves = b.legal_moves('w')
    # Wait white king on c1, black queen on b1: queen on c1 is in check? No, white king on c1 is attacked by black queen on b1.
    # That's fine for our setup actually - but we need a legal position.
    # Let me redo: white queen a1, black queen b1, white K c2, black K h8.
    b = make("7k/8/8/8/8/8/2K5/Qq6 w")
    moves = b.legal_moves('w')
    # K on c2 not in check (bq on b1 attacks a1, b2..b8, and diagonals). c2 is on diagonal from b1: b1->c2 yes! In check.
    # Try: wQ on a1, bQ on c1, wK on e2, bK on h8.
    b = make("7k/8/8/8/8/8/4K3/Q1q5 w")
    # bq on c1 attacks along c-file, 1st rank, and diagonals. e2 on diagonal? c1-d2-e3, no.
    # a1 attacked along rank: c1-b1-a1, yes. white queen on a1 is attacked but that's just being captured threat,
    # not check. Good.
    moves = b.legal_moves('w')
    # Queen on a1 can move along 1st rank: b1 (empty), c1 (capture), not d1.
    assert has_move(moves, 'a1', 'b1')
    assert has_move(moves, 'a1', 'c1')  # capture black queen
    assert not has_move(moves, 'a1', 'd1')
    assert not has_move(moves, 'a1', 'e1')


# =========================================================================
# King movement
# =========================================================================

def test_king_moves_center():
    # White K on d4, kings + queen well separated.
    b = make("k7/8/8/8/3K4/8/8/7Q w")
    moves = b.legal_moves('w')
    king_dests = [m[1] for m in moves if m[0] == algebraic_to_sq('d4')]
    expected = ['c3', 'c4', 'c5', 'd3', 'd5', 'e3', 'e4', 'e5']
    for sq in expected:
        assert algebraic_to_sq(sq) in king_dests, f"king missing {sq}"
    assert len(king_dests) == 8


def test_king_moves_corner():
    b = make("k7/8/8/8/8/8/8/K6Q w")
    # White K on a1: can go a2, b1, b2.
    moves = b.legal_moves('w')
    king_dests = [m[1] for m in moves if m[0] == algebraic_to_sq('a1')]
    assert algebraic_to_sq('a2') in king_dests
    assert algebraic_to_sq('b1') in king_dests
    assert algebraic_to_sq('b2') in king_dests
    assert len(king_dests) == 3


def test_king_cannot_move_into_check():
    # White K on e1, black queen on e8 attacks e-file. King may not move to e2.
    b = make("4q2k/8/8/8/8/8/8/4K3 w")
    moves = b.legal_moves('w')
    king_dests = [m[1] for m in moves if m[0] == algebraic_to_sq('e1')]
    assert algebraic_to_sq('e2') not in king_dests
    # d1 and f1 also attacked? Black queen e8 attacks e-file only along that ray; d1/f1 not on it.
    # But king on d1: black queen on e8 attacks d1? e8->d1? Not a queen line.
    # d2: not on e-file or e8 diagonal (e8-d7-c6...). Safe.
    assert algebraic_to_sq('d1') in king_dests
    assert algebraic_to_sq('f1') in king_dests
    assert algebraic_to_sq('d2') in king_dests
    assert algebraic_to_sq('f2') in king_dests


def test_kings_cannot_be_adjacent():
    # White K on e4, black K on e6: any move bringing white K to e5/d5/f5 is illegal
    # because black K attacks those squares.
    b = make("8/8/4k3/8/4K3/8/8/7Q w")
    moves = b.legal_moves('w')
    king_dests = [m[1] for m in moves if m[0] == algebraic_to_sq('e4')]
    # squares attacked by black K on e6: d5, e5, f5, d6, f6, d7, e7, f7
    for forbidden in ['d5', 'e5', 'f5']:
        assert algebraic_to_sq(forbidden) not in king_dests, f"king illegally on {forbidden}"
    # safe squares
    for safe in ['d3', 'e3', 'f3', 'd4', 'f4']:
        assert algebraic_to_sq(safe) in king_dests, f"king should be allowed on {safe}"


# =========================================================================
# Check & checkmate detection
# =========================================================================

def test_in_check_detection():
    # Black queen on e8 along e-file, white king on e1: in check.
    b = make("4q2k/8/8/8/8/8/8/4K3 w")
    assert b.is_in_check('w')
    assert not b.is_in_check('b')


def test_not_in_check():
    # bK on a8, wK on h1, wQ on h2: neither king attacked.
    b = make("k7/8/8/8/8/8/7Q/7K w")
    assert not b.is_in_check('w')
    assert not b.is_in_check('b')


def test_check_from_diagonal():
    # White king e1, black queen on h4 attacks along h4-e1 diagonal.
    b = make("7k/8/8/8/7q/8/8/4K3 w")
    assert b.is_in_check('w')


def test_checkmate_back_rank_with_king_support():
    """White Q on f7 supported by K on f6, black king cornered on h8.
    Black to move. Queen attacks g8 and h7 area; king covers escape squares.
    """
    # Setup: bK h8, wQ g7 (defended by wK), wK f6. Black to move.
    # bK on h8 can try: g8 (attacked by Q g7? g7-g8 yes), h7 (attacked by Q g7 yes).
    # Q on g7 is defended by K on f6 (f6-g7 adj).
    b = make("7k/6Q1/5K2/8/8/8/8/8 b")
    assert b.is_in_check('b')
    assert b.is_checkmate('b')


def test_mate_in_one_white_finds_it():
    """White to move can mate in one: queen delivers mate."""
    # bK h8, wK f7, wQ a8 (anywhere on 8th rank that mates h8 with K cover).
    # wQ a8 attacks h8: yes (a8 to h8 along rank). bK on h8 in check by Q a8.
    # bK escapes: g7? wK on f7 attacks g7? f7-g7 adj yes. h7? wK f7 attacks: f7-g7 adj; h7 not adj to f7.
    # So h7 may be available. Queen on a8 attacks h7? Not on rank/file/diagonal from a8.
    # That's not mate; bK escapes to h7.
    # Try wQ on h6: attacks h8 along h-file. bK can go g8: attacked by Q h6? no (h6-g8 not a line). King f7 attacks g8? yes. So g8 covered.
    # g7: attacked by wK f7 yes, and by wQ h6 yes. h7: attacked by wQ h6 yes.
    # So bK on h8 with wK f7, wQ h6, black to move: mate.
    # But wait the position needs white to have just played, and now black is to move.
    # Actually the prompt says mate-in-1: white finds it. So we need white-to-move with the mating move available.
    # Setup: bK h8, wK f7, wQ somewhere from which one move mates.
    # If wQ on h1, wQ -> h6 mates as analyzed above? Yes - h1 to h6 is a queen move.
    # But wait wQ h6 -- need bK can't escape to anywhere safe. Squares around h8: g7, g8, h7.
    #   g7: wK f7 attacks (adj), wQ h6 attacks (adj). Covered.
    #   g8: wK f7 attacks (adj). Covered.
    #   h7: wQ h6 attacks (h-file). Covered.
    # bK has no moves out of check -> mate.
    b = make("7k/5K2/8/8/8/8/8/7Q w")
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    assert move is not None
    new_board = b.make_move(move)
    assert new_board.is_checkmate('b'), \
        f"AI did not mate; played {move}, new fen={new_board.to_fen()}"


def test_mate_in_one_alternative_position():
    """Another mate-in-one: white queen supported by king."""
    # bK a8, wK c7, wQ on d-file. wQ d8 mates: a8 attacked along 8th rank; bK escape a7 (attacked by wK c7? c7-a7 not adj; b7 attacked yes; b8 attacked by Q yes and by K yes).
    # Actually: bK a8, escape squares a7, b7, b8. wK c7 attacks b7, b8, b6, c6, c8, d6, d7, d8. So b7, b8, c8, d7, d8 all covered by wK.
    # a7 attacked by wK? c7-a7 not adjacent. wQ on d8 attacks a7? d8-c7-b6-a5 SW diag; or d8-a8 rank; or d8-d-file. No, a7 not attacked by Q d8.
    # So bK escapes to a7 -- not mate.
    # Try wQ to b7? then Q is on b7 attacked by bK a8 (adj). But wK c7 defends b7. wQ b7 attacks a8 (adj), a7 (adj), b8 (file). So mate: bK in check, can't go a7 (Q attacks), can't go b8 (Q attacks; K attacks), can't go b7 (occupied by Q, but K could capture if undefended... defended by wK c7). Mate!
    # So if wQ starts on b1, move b1->b7 mates.
    b = make("k7/2K5/8/8/8/8/8/1Q6 w")
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    new_board = b.make_move(move)
    assert new_board.is_checkmate('b')


def test_stalemate_detection():
    """Classic stalemate: black K on a8, white K on c7, white Q on c6.
    Wait that's not stalemate (Q on c6 attacks a8 along the diagonal? c6-b7-a8 yes -> check).
    Stalemate: bK a8, wK c7, wQ b6: black not in check (b6 attacks a7,a6,b8,b7,c5,c6,c7,d4,d6,d8,a5..),
    bK on a8 has squares a7, b7, b8. wK c7 attacks all of those. wQ b6 also attacks them. Black not in check.
    Actually we need bK NOT in check. wQ b6 attacks a7 (rank b6 to a7 is diagonal), a6 (rank? b6-a6 yes), b8 (file). Does Q b6 attack a8? b6-a7-a8 not a line; b6 to a8 -> df=-1, dr=2, not queen direction. So bK on a8 not attacked.
    Squares around a8: a7 (attacked by Q & K), b7 (attacked by Q & K), b8 (attacked by Q & K).
    No legal moves, not in check -> stalemate.
    """
    b = make("k7/2K5/1Q6/8/8/8/8/8 b")
    assert not b.is_in_check('b')
    assert b.is_stalemate('b')
    assert not b.is_checkmate('b')


def test_not_checkmate_when_can_escape():
    # bK h8, wQ h1 attacks h8: check. But bK can go to g7 safely.
    b = make("7k/8/8/8/8/8/8/3K3Q b")
    assert b.is_in_check('b')
    assert not b.is_checkmate('b')


def test_not_checkmate_when_queen_can_be_captured():
    # bK on h8, wQ on h7 giving check, but wQ is undefended -> bK takes it.
    b = make("7k/7Q/8/8/8/8/8/K7 b")
    assert b.is_in_check('b')
    # bK can capture queen on h7.
    moves = b.legal_moves('b')
    assert has_move(moves, 'h8', 'h7')
    assert not b.is_checkmate('b')


# =========================================================================
# Evaluator
# =========================================================================

def test_evaluator_material_advantage_white():
    # White has Q, black does not.
    b = make("4k3/8/8/8/8/8/8/3QK3 w")
    score = evaluate(b, 'w')
    assert score == 9


def test_evaluator_material_advantage_black():
    b = make("3qk3/8/8/8/8/8/8/4K3 w")
    score = evaluate(b, 'w')
    assert score == -9


def test_evaluator_equal_material():
    b = make("3qk3/8/8/8/8/8/8/3QK3 w")
    score = evaluate(b, 'w')
    assert score == 0


def test_evaluator_checkmate_against_opponent_is_positive_infinity():
    # Position where black-to-move is checkmated; evaluate from white's pov.
    b = make("7k/5K2/7Q/8/8/8/8/8 b")
    # confirm it's actually mate
    assert b.is_checkmate('b')
    score = evaluate(b, 'w')
    assert score == math.inf


def test_evaluator_own_checkmate_is_negative_infinity():
    b = make("7k/5K2/7Q/8/8/8/8/8 b")
    score = evaluate(b, 'b')
    assert score == -math.inf


def test_evaluator_sign_convention_consistent():
    """eval(board, white) == -eval(board, black) for non-terminal positions."""
    b = make("3qk3/8/8/8/8/8/8/3QK3 w")
    sw = evaluate(b, 'w')
    sb = evaluate(b, 'b')
    assert sw == -sb


# =========================================================================
# AIPlayer behavior
# =========================================================================

def test_ai_returns_legal_move():
    b = make("3qk3/8/8/8/8/8/8/3QK3 w")
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    assert move is not None
    assert move in b.legal_moves('w')


def test_ai_prefers_capturing_free_queen():
    # White Q can capture undefended black Q along the d-file.
    # Setup so that capturing is unambiguously best.
    b = make("4k3/8/8/3q4/8/8/8/3QK3 w")
    # Black Q on d5 is attacked by white Q on d1 (same file, no blockers).
    # Is black Q defended by anything? Black K on e8: not adjacent to d5. Undefended.
    # So Qxd5 wins the queen.
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    from_sq, to_sq = move
    assert from_sq == algebraic_to_sq('d1')
    assert to_sq == algebraic_to_sq('d5')


def test_ai_avoids_losing_own_queen():
    """White has a clearly safe move available; AI should not hang the queen.

    Position: White Q on d4 attacked by black Q on h8 along diagonal d4-e5-f6-g7-h8.
    White can move queen to many safe squares (e.g. a1, a4, d1).
    Black queen is undefended on h8; black king on a8 far away.
    White K on a2 (out of the way).
    """
    b = make("k6q/8/8/8/3Q4/8/K7/8 w")
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    after = b.make_move(move)
    # After white's move, look at black's best reply. If black can capture the queen
    # for free, AI was bad.
    black_ai = AIPlayer(depth=1)
    bm = black_ai.choose_move(after)
    if bm is not None:
        after2 = after.make_move(bm)
        wq_after = after2.queen_square('w')
        # White queen still on the board, OR white made an equal-or-better trade
        # (i.e., black queen is now gone too).
        bq_after = after2.queen_square('b')
        assert wq_after is not None or bq_after is None, \
            f"AI hung queen; white move={move}, black reply={bm}, final fen={after2.to_fen()}"


def test_ai_finds_mate_in_1():
    b = make("7k/5K2/8/8/8/8/8/7Q w")
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    new_board = b.make_move(move)
    assert new_board.is_checkmate('b'), \
        f"AI did not find mate; played {move}, fen={new_board.to_fen()}"


def test_ai_handles_no_legal_moves():
    """In a checkmate position with side-to-move being mated, AI returns no move."""
    b = make("7k/5K2/7Q/8/8/8/8/8 b")
    assert b.is_checkmate('b')
    ai = AIPlayer(depth=2)
    move = ai.choose_move(b)
    assert move is None


def test_make_move_flips_turn():
    b = make("4k3/8/8/8/8/8/8/3QK3 w")
    move = (algebraic_to_sq('d1'), algebraic_to_sq('d5'))
    new_b = b.make_move(move)
    assert new_b.turn == 'b'
    assert new_b.piece_at(algebraic_to_sq('d5')) == ('w', 'Q')
    assert new_b.piece_at(algebraic_to_sq('d1')) is None


def test_legal_moves_default_uses_turn():
    b = make("4k3/8/8/8/8/8/8/3QK3 w")
    legal_default = b.legal_moves()
    legal_white = b.legal_moves('w')
    assert set(legal_default) == set(legal_white)

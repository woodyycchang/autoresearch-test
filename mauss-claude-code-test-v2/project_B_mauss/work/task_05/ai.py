"""Minimax + alpha-beta AI for the simplified Kings+Queens chess game.

Evaluator (from White's POV):
  +9 for each white queen, -9 for each black queen.
  +INF for checkmate against opponent (we win), -INF for own checkmate.
  0 for stalemate.
"""

from board import Board
from moves import opposite


INF = 10_000_000
MATE_SCORE = 1_000_000  # large but finite so we can prefer faster mates


def material_eval(board):
    """Static material balance from White's POV."""
    score = 0
    for _sq, (color, kind) in board.squares.items():
        if kind == 'Q':
            score += 9 if color == 'w' else -9
        # Kings are not scored materially (both sides always have one,
        # and the absence of a king is impossible in a legal position).
    return score


def evaluate(board, perspective):
    """Evaluate from `perspective`'s point of view.

    Detects terminal nodes (checkmate / stalemate) for the side to
    move. Otherwise returns material balance.
    """
    to_move = board.turn
    legal = board.legal_moves(to_move)
    if not legal:
        if board.in_check(to_move):
            # `to_move` is checkmated. Bad for `to_move`, good for the
            # other side.
            sign = -1 if to_move == perspective else 1
            return sign * MATE_SCORE
        # Stalemate.
        return 0
    base = material_eval(board)
    return base if perspective == 'w' else -base


class AIPlayer:
    def __init__(self, depth=3):
        if depth < 1:
            raise ValueError("depth must be >= 1")
        self.depth = depth
        self.nodes = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def choose_move(self, board, color=None):
        """Return the best move for `color` (defaults to board.turn)."""
        if color is None:
            color = board.turn
        if board.turn != color:
            # AI is asked to move when it isn't this color's turn:
            # rotate the board's turn marker so search proceeds correctly.
            board = board.copy()
            board.turn = color
        self.nodes = 0
        best_move = None
        best_score = -INF
        alpha, beta = -INF, INF
        moves = self._order_moves(board, board.legal_moves(color))
        for move in moves:
            token = board.make_move(move)
            try:
                score = -self._negamax(board, self.depth - 1, -beta, -alpha,
                                       perspective=opposite(color))
            finally:
                board.unmake_move(token)
            if score > best_score:
                best_score = score
                best_move = move
            if score > alpha:
                alpha = score
        return best_move

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------
    def _negamax(self, board, depth, alpha, beta, perspective):
        """Negamax with alpha-beta. `perspective` is the side to move."""
        self.nodes += 1
        to_move = board.turn
        legal = board.legal_moves(to_move)
        if not legal:
            if board.in_check(to_move):
                # `to_move` is mated. From `perspective`'s view (which
                # equals to_move here in negamax), it's losing. Prefer
                # later losses / earlier wins by adjusting with depth.
                return -MATE_SCORE - depth
            return 0  # stalemate
        if depth == 0:
            base = material_eval(board)
            return base if perspective == 'w' else -base

        best = -INF
        for move in self._order_moves(board, legal):
            token = board.make_move(move)
            try:
                score = -self._negamax(board, depth - 1, -beta, -alpha,
                                       perspective=opposite(perspective))
            finally:
                board.unmake_move(token)
            if score > best:
                best = score
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break  # beta cutoff
        return best

    def _order_moves(self, board, moves):
        """Cheap move ordering: captures first."""
        return sorted(moves, key=lambda m: 0 if m[2] is None else -1)

"""Minimax + alpha-beta AI for the simplified K+Q chess engine."""

import math

from board import Board


INF = math.inf


def evaluate(board, root_color):
    """Static evaluation from root_color's perspective.

    +9 per friendly queen, -9 per enemy queen.
    +inf if opponent is checkmated (we win).
    -inf if we are checkmated.
    0 if stalemate.
    """
    opp = board.opponent(root_color)

    # Terminal checks
    if board.is_checkmate(opp):
        return INF
    if board.is_checkmate(root_color):
        return -INF
    if board.is_stalemate(opp) or board.is_stalemate(root_color):
        return 0

    score = 0
    for sq, (c, p) in board.pieces.items():
        if p == 'Q':
            score += 9 if c == root_color else -9
    return score


def minimax(board, depth, alpha, beta, maximizing, root_color):
    """Alpha-beta minimax. Returns (score, best_move_or_None)."""
    # Terminal or depth cutoff
    if board.is_checkmate(board.turn):
        # The side to move is checkmated.
        if board.turn == root_color:
            return -INF, None
        else:
            return INF, None
    if board.is_stalemate(board.turn):
        return 0, None
    if depth == 0:
        return evaluate(board, root_color), None

    moves = board.legal_moves(board.turn)
    if not moves:
        # Shouldn't reach here given the checks above, but be safe.
        return evaluate(board, root_color), None

    best_move = None
    if maximizing:
        best = -INF
        for m in moves:
            child = board.make_move(m)
            score, _ = minimax(child, depth - 1, alpha, beta, False, root_color)
            if score > best:
                best = score
                best_move = m
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best, best_move
    else:
        best = INF
        for m in moves:
            child = board.make_move(m)
            score, _ = minimax(child, depth - 1, alpha, beta, True, root_color)
            if score < best:
                best = score
                best_move = m
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best, best_move


class AIPlayer:
    def __init__(self, depth=3):
        if depth < 1:
            raise ValueError("depth must be >= 1")
        self.depth = depth

    def choose_move(self, board):
        """Return the best move for board.turn at the configured depth."""
        root_color = board.turn
        score, move = minimax(
            board, self.depth, -INF, INF, True, root_color
        )
        if move is None:
            # No legal move available
            return None
        return move

    def evaluate_position(self, board):
        return evaluate(board, board.turn)

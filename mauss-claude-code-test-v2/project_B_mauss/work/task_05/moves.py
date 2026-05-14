"""Move generation utilities for simplified chess (Kings + Queens only).

Squares are represented as (file, rank) tuples where file in 0..7 (a..h)
and rank in 0..7 (rank 1..8). White is 'w', Black is 'b'.

A Move is a tuple: (from_sq, to_sq, captured_piece_or_None).
"""

# 8 ray directions for queen and king (king = 1 step on each).
QUEEN_DIRS = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1),
]


def in_bounds(sq):
    f, r = sq
    return 0 <= f < 8 and 0 <= r < 8


def opposite(color):
    return 'b' if color == 'w' else 'w'


def queen_pseudo_moves(board, from_sq, color):
    """Generate pseudo-legal queen moves (no king-in-check filtering).

    Queen slides along each ray until it hits the edge, an own piece
    (stop, no capture), or an enemy piece (capture and stop).
    """
    moves = []
    for df, dr in QUEEN_DIRS:
        f, r = from_sq
        while True:
            f, r = f + df, r + dr
            if not in_bounds((f, r)):
                break
            target = board.piece_at((f, r))
            if target is None:
                moves.append((from_sq, (f, r), None))
                continue
            t_color, t_kind = target
            if t_color == color:
                # Own piece blocks. Cannot jump over.
                break
            # Enemy piece: capture and stop.
            moves.append((from_sq, (f, r), target))
            break
    return moves


def king_pseudo_moves(board, from_sq, color):
    """Generate pseudo-legal king moves (one step in any direction)."""
    moves = []
    for df, dr in QUEEN_DIRS:
        to_sq = (from_sq[0] + df, from_sq[1] + dr)
        if not in_bounds(to_sq):
            continue
        target = board.piece_at(to_sq)
        if target is None:
            moves.append((from_sq, to_sq, None))
        elif target[0] != color:
            moves.append((from_sq, to_sq, target))
    return moves


def pseudo_moves(board, color):
    """All pseudo-legal moves for `color` (ignoring own-king-in-check)."""
    moves = []
    for sq, piece in board.pieces_of(color):
        kind = piece[1]
        if kind == 'Q':
            moves.extend(queen_pseudo_moves(board, sq, color))
        elif kind == 'K':
            moves.extend(king_pseudo_moves(board, sq, color))
    return moves


def square_attacked(board, sq, by_color):
    """True if `sq` is attacked by any piece of `by_color`.

    Uses pseudo-move generation: any move whose destination is `sq`
    means `sq` is attacked. For kings/queens this is correct (no
    en-passant, pawns, or castling to worry about).
    """
    for from_sq, to_sq, _captured in pseudo_moves(board, by_color):
        if to_sq == sq:
            return True
    return False

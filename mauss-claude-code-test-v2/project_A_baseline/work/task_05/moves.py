"""Move generation helpers for simplified chess (Kings + one Queen each).

A move is a tuple: (from_square, to_square) where each square is (file, rank)
with file in 0..7 (a..h) and rank in 0..7 (1..8). Captured-piece info is
derived from the board state at apply time.
"""

# Direction vectors
ROOK_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BISHOP_DIRS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
QUEEN_DIRS = ROOK_DIRS + BISHOP_DIRS
KING_DIRS = QUEEN_DIRS  # one-step in all 8 directions


def in_bounds(sq):
    """True if (file, rank) is on an 8x8 board."""
    f, r = sq
    return 0 <= f < 8 and 0 <= r < 8


def slide_moves(board, from_sq, dirs, color):
    """Generate sliding moves for queen/rook/bishop from from_sq.

    board: dict mapping (f,r) -> (color, piece_char)
    Stops at first occupied square; if enemy, that square is a capture.
    """
    moves = []
    f0, r0 = from_sq
    for df, dr in dirs:
        f, r = f0 + df, r0 + dr
        while in_bounds((f, r)):
            occupant = board.get((f, r))
            if occupant is None:
                moves.append((from_sq, (f, r)))
            else:
                if occupant[0] != color:
                    moves.append((from_sq, (f, r)))
                break
            f += df
            r += dr
    return moves


def king_moves(board, from_sq, color):
    """Generate one-step moves for the king (does not yet filter into-check)."""
    moves = []
    f0, r0 = from_sq
    for df, dr in KING_DIRS:
        to = (f0 + df, r0 + dr)
        if not in_bounds(to):
            continue
        occupant = board.get(to)
        if occupant is None or occupant[0] != color:
            moves.append((from_sq, to))
    return moves


def queen_moves(board, from_sq, color):
    return slide_moves(board, from_sq, QUEEN_DIRS, color)


def square_attacked_by(board, sq, attacker_color):
    """Return True if `sq` is attacked by any piece of attacker_color.

    Uses ray scans from sq outward so we don't need full move-gen
    (which would recurse via legality checking).
    """
    f0, r0 = sq

    # Sliding attacks: scan rays from sq; if first piece found is the
    # attacker's queen along a queen-ray, sq is attacked.
    for df, dr in QUEEN_DIRS:
        f, r = f0 + df, r0 + dr
        while in_bounds((f, r)):
            occ = board.get((f, r))
            if occ is not None:
                c, p = occ
                if c == attacker_color and p == 'Q':
                    return True
                # any piece blocks further sliding attacks from this ray
                break
            f += df
            r += dr

    # King attacks: a king attacks all adjacent squares
    for df, dr in KING_DIRS:
        nf, nr = f0 + df, r0 + dr
        if not in_bounds((nf, nr)):
            continue
        occ = board.get((nf, nr))
        if occ is not None and occ[0] == attacker_color and occ[1] == 'K':
            return True

    return False


def algebraic_to_sq(s):
    """Convert 'e4' style coordinates to (file, rank). Returns None for '-'."""
    if s == '-' or s is None:
        return None
    if len(s) != 2:
        raise ValueError(f"bad square: {s}")
    f = ord(s[0].lower()) - ord('a')
    r = int(s[1]) - 1
    if not (0 <= f < 8 and 0 <= r < 8):
        raise ValueError(f"bad square: {s}")
    return (f, r)


def sq_to_algebraic(sq):
    f, r = sq
    return f"{chr(ord('a') + f)}{r + 1}"

"""Simplified chess board (Kings + Queens only).

Pieces are encoded as a 2-tuple (color, kind):
    color in {'w', 'b'}
    kind  in {'K', 'Q'}

The board is an 8x8 grid stored as a dict keyed by (file, rank).
FEN parsing supports only K/Q/k/q glyphs plus empty squares.
"""

from moves import (
    pseudo_moves, square_attacked, opposite, in_bounds,
)


FILE_CHARS = 'abcdefgh'


def algebraic(sq):
    """Convert (file, rank) -> 'e4' style string. Used in test diagnostics."""
    f, r = sq
    return f"{FILE_CHARS[f]}{r + 1}"


def from_algebraic(s):
    return (FILE_CHARS.index(s[0]), int(s[1]) - 1)


class Board:
    def __init__(self):
        # Map from (file, rank) -> (color, kind)
        self.squares = {}
        # 'w' to move by default.
        self.turn = 'w'

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    @classmethod
    def parse_fen(cls, fen):
        """Parse a FEN-like string. Only K/Q/k/q + digits + side-to-move.

        Example: '4k3/8/8/8/8/8/8/3QK3 w - - 0 1'
        """
        b = cls()
        parts = fen.strip().split()
        rows = parts[0].split('/')
        if len(rows) != 8:
            raise ValueError(f"FEN must have 8 ranks, got {len(rows)}")
        # FEN ranks are top-to-bottom (rank 8 first).
        for i, row in enumerate(rows):
            rank = 7 - i
            f = 0
            for ch in row:
                if ch.isdigit():
                    f += int(ch)
                else:
                    color = 'w' if ch.isupper() else 'b'
                    kind = ch.upper()
                    if kind not in ('K', 'Q'):
                        raise ValueError(f"Unsupported piece: {ch}")
                    b.squares[(f, rank)] = (color, kind)
                    f += 1
            if f != 8:
                raise ValueError(f"Bad rank length in FEN row: {row}")
        if len(parts) >= 2:
            b.turn = parts[1]
        return b

    # ------------------------------------------------------------------
    # Inspection helpers
    # ------------------------------------------------------------------
    def piece_at(self, sq):
        return self.squares.get(sq)

    def pieces_of(self, color):
        """Yield (sq, piece) for every piece of `color`."""
        for sq, piece in self.squares.items():
            if piece[0] == color:
                yield sq, piece

    def find_king(self, color):
        for sq, piece in self.squares.items():
            if piece == (color, 'K'):
                return sq
        return None

    def copy(self):
        new = Board()
        new.squares = dict(self.squares)
        new.turn = self.turn
        return new

    # ------------------------------------------------------------------
    # Move application / legality
    # ------------------------------------------------------------------
    def make_move(self, move):
        """Apply move, returning an undo token (for unmake_move).

        We use a simple copy-on-write style: callers usually use
        `with_move` which makes a fresh board. But for AI performance
        we provide in-place make/unmake.
        """
        from_sq, to_sq, captured = move
        piece = self.squares.pop(from_sq)
        prev_target = self.squares.get(to_sq)
        if to_sq in self.squares:
            del self.squares[to_sq]
        self.squares[to_sq] = piece
        prev_turn = self.turn
        self.turn = opposite(self.turn)
        return (from_sq, to_sq, piece, prev_target, prev_turn)

    def unmake_move(self, token):
        from_sq, to_sq, piece, prev_target, prev_turn = token
        del self.squares[to_sq]
        if prev_target is not None:
            self.squares[to_sq] = prev_target
        self.squares[from_sq] = piece
        self.turn = prev_turn

    def with_move(self, move):
        new = self.copy()
        new.make_move(move)
        return new

    def in_check(self, color):
        king_sq = self.find_king(color)
        if king_sq is None:
            # No king => treat as in check (defensive); shouldn't happen
            # in the simplified game.
            return True
        return square_attacked(self, king_sq, opposite(color))

    def legal_moves(self, color):
        """All fully-legal moves for `color`.

        Filters pseudo-moves to drop any that leave the mover's king
        in check (which also forbids the king walking into check or
        capturing into a square defended by the opponent).
        """
        legal = []
        for move in pseudo_moves(self, color):
            token = self.make_move(move)
            try:
                if not self.in_check(color):
                    legal.append(move)
            finally:
                self.unmake_move(token)
        return legal

    def is_checkmate(self, color):
        return self.in_check(color) and not self.legal_moves(color)

    def is_stalemate(self, color):
        return (not self.in_check(color)) and (not self.legal_moves(color))

    # Convenience for diagnostics
    def __repr__(self):
        lines = []
        for r in range(7, -1, -1):
            row = []
            for f in range(8):
                p = self.squares.get((f, r))
                if p is None:
                    row.append('.')
                else:
                    ch = p[1]
                    row.append(ch if p[0] == 'w' else ch.lower())
            lines.append(' '.join(row))
        lines.append(f"turn={self.turn}")
        return '\n'.join(lines)

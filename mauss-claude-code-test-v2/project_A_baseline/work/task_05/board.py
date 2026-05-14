"""Simplified chess board: each side has 1 King and (optionally) 1 Queen.

The board is represented as a dict mapping (file, rank) -> (color, piece_char)
where color is 'w' or 'b' and piece_char is 'K' or 'Q'.

FEN parsing supports the standard layout for these pieces. Other pieces in a
FEN are rejected (this engine only handles K+Q endgames).
"""

from moves import (
    QUEEN_DIRS, KING_DIRS, queen_moves, king_moves,
    square_attacked_by, algebraic_to_sq, sq_to_algebraic, in_bounds,
)


class Board:
    def __init__(self, pieces=None, turn='w'):
        # pieces: dict {(f,r): (color, piece_char)}
        self.pieces = dict(pieces) if pieces else {}
        self.turn = turn  # whose move it is

    # ---------- construction ----------

    @classmethod
    def parse_fen(cls, fen):
        """Parse a FEN string. Supports only K and Q pieces.

        FEN form: <ranks> <turn> [castling] [en-passant] [halfmove] [fullmove]
        We accept and ignore castling/ep/clocks since they don't apply
        in a K+Q endgame.
        """
        parts = fen.strip().split()
        if len(parts) < 2:
            raise ValueError(f"FEN must have at least board and turn: {fen!r}")
        board_part, turn = parts[0], parts[1]
        if turn not in ('w', 'b'):
            raise ValueError(f"bad turn in FEN: {turn!r}")

        pieces = {}
        ranks = board_part.split('/')
        if len(ranks) != 8:
            raise ValueError(f"FEN must have 8 ranks: {fen!r}")

        # FEN ranks are listed from rank 8 down to rank 1.
        for i, rank_str in enumerate(ranks):
            rank = 7 - i  # rank index 0..7
            file = 0
            for ch in rank_str:
                if ch.isdigit():
                    file += int(ch)
                elif ch.upper() in ('K', 'Q'):
                    color = 'w' if ch.isupper() else 'b'
                    pieces[(file, rank)] = (color, ch.upper())
                    file += 1
                else:
                    raise ValueError(
                        f"unsupported FEN piece {ch!r}; only K/Q allowed"
                    )
            if file != 8:
                raise ValueError(f"rank does not sum to 8: {rank_str!r}")

        return cls(pieces=pieces, turn=turn)

    def to_fen(self):
        """Re-serialize to FEN (board + turn only)."""
        rows = []
        for rank in range(7, -1, -1):
            row = ''
            empty = 0
            for file in range(8):
                p = self.pieces.get((file, rank))
                if p is None:
                    empty += 1
                else:
                    if empty:
                        row += str(empty)
                        empty = 0
                    color, ch = p
                    row += ch if color == 'w' else ch.lower()
            if empty:
                row += str(empty)
            rows.append(row)
        return '/'.join(rows) + ' ' + self.turn

    def copy(self):
        return Board(pieces=self.pieces, turn=self.turn)

    # ---------- queries ----------

    def king_square(self, color):
        for sq, (c, p) in self.pieces.items():
            if c == color and p == 'K':
                return sq
        return None

    def queen_square(self, color):
        for sq, (c, p) in self.pieces.items():
            if c == color and p == 'Q':
                return sq
        return None

    def piece_at(self, sq):
        return self.pieces.get(sq)

    def opponent(self, color):
        return 'b' if color == 'w' else 'w'

    def is_in_check(self, color):
        k = self.king_square(color)
        if k is None:
            return False
        return square_attacked_by(self.pieces, k, self.opponent(color))

    # ---------- move generation ----------

    def pseudo_moves(self, color):
        """Generate moves that respect piece movement & capture rules,
        but do NOT filter out moves that leave the mover in check.
        """
        moves = []
        for sq, (c, p) in list(self.pieces.items()):
            if c != color:
                continue
            if p == 'Q':
                moves.extend(queen_moves(self.pieces, sq, color))
            elif p == 'K':
                moves.extend(king_moves(self.pieces, sq, color))
        return moves

    def legal_moves(self, color=None):
        """Generate fully legal moves: filters out any move that leaves
        the side-to-move's king in check. If color is None, uses self.turn.
        """
        if color is None:
            color = self.turn
        legal = []
        opp = self.opponent(color)
        for m in self.pseudo_moves(color):
            new_pieces = self._apply_to_pieces(self.pieces, m)
            # find own king in new position
            new_king = None
            for sq, (c, p) in new_pieces.items():
                if c == color and p == 'K':
                    new_king = sq
                    break
            if new_king is None:
                # somehow our king was captured -- illegal in real chess but
                # treat as illegal here
                continue
            if not square_attacked_by(new_pieces, new_king, opp):
                legal.append(m)
        return legal

    @staticmethod
    def _apply_to_pieces(pieces, move):
        from_sq, to_sq = move
        new = dict(pieces)
        piece = new.pop(from_sq)
        # capture: target square overwritten regardless of what was there
        new[to_sq] = piece
        return new

    def make_move(self, move):
        """Return a new Board with `move` applied and turn flipped."""
        new_pieces = self._apply_to_pieces(self.pieces, move)
        return Board(pieces=new_pieces, turn=self.opponent(self.turn))

    # ---------- termination ----------

    def is_checkmate(self, color=None):
        if color is None:
            color = self.turn
        if not self.is_in_check(color):
            return False
        return len(self.legal_moves(color)) == 0

    def is_stalemate(self, color=None):
        if color is None:
            color = self.turn
        if self.is_in_check(color):
            return False
        return len(self.legal_moves(color)) == 0

    def is_game_over(self):
        return self.is_checkmate(self.turn) or self.is_stalemate(self.turn)

    # ---------- evaluation helper ----------

    def material(self, color):
        """Count material for `color`. Queen=9, King not counted."""
        score = 0
        for sq, (c, p) in self.pieces.items():
            if c == color and p == 'Q':
                score += 9
        return score

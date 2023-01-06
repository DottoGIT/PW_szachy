"""
This class is responsible for keeping current pieces positions and remembering moves
"""
from piece import Piece


class GameState():
    def __init__(self):
        self.board = self.initialize_board()

    def move_piece(self, piece, position, opponent):
        self.board[piece.position[0]][piece.position[1]] = None
        self.board[position[0]][position[1]] = piece
        piece.set_position((position[0], position[1]))

    def initialize_board(self):
        return [
            [Piece("br", (0, 0)), Piece("bh", (0, 1)), Piece("bb", (0, 2)), Piece("bk", (0, 3)), Piece("bq", (0, 4)), Piece("bb", (0, 5)), Piece("bh", (0, 6)), Piece("br", (0, 7))],
            [Piece("bp", (1, 0)), Piece("bp", (1, 1)), Piece("bp", (1, 2)), Piece("bp", (1, 3)), Piece("bp", (1, 4)), Piece("bp", (1, 5)), Piece("bp", (1, 6)), Piece("bp", (1, 7))],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Piece("wp", (6, 0)), Piece("wp", (6, 1)), Piece("wp", (6, 2)), Piece("wp", (6, 3)), Piece("wp", (6, 4)), Piece("wp", (6, 5)), Piece("wp", (6, 6)), Piece("wp", (6, 7))],
            [Piece("wr", (7, 0)), Piece("wh", (7, 1)), Piece("wb", (7, 2)), Piece("wq", (7, 3)), Piece("wk", (7, 4)), Piece("wb", (7, 5)), Piece("wh", (7, 6)), Piece("wr", (7, 7))]
        ]

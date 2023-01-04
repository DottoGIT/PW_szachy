"""
This class is responsible for keeping current pieces positions and remembering moves
"""
from piece import Piece


class GameState():
    def __init__(self):
        self.board = self.initialize_board()

    def print_board():
        pass

    def move_piece():
        pass

    def initialize_board(self):
        return [
            [Piece("br"), Piece("bh"), Piece("bb"), Piece("bk"), Piece("bq"), Piece("bb"), Piece("bh"), Piece("br")],
            [Piece("bp"), Piece("bp"), Piece("bp"), Piece("bp"), Piece("bp"), Piece("bp"), Piece("bp"), Piece("bp")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Piece("wp"), Piece("wp"), Piece("wp"), Piece("wp"), Piece("wp"), Piece("wp"), Piece("wp"), Piece("wp")],
            [Piece("wr"), Piece("wh"), Piece("wb"), Piece("wq"), Piece("wk"), Piece("wb"), Piece("wh"), Piece("wr")]
        ]

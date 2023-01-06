"""
This class contains information about player score, color and pieces that he has
"""


class Player():
    def __init__(self, color, pieces):
        if color not in ["b", "w"]:
            raise ValueError("Player color can only be set to 'b' or 'w'")
        if len(pieces) != 16:
            raise ValueError("Player has to start with 16 pieces!")
        self.score = 0
        self.color = color
        self.pieces = pieces

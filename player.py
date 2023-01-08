"""
This class contains information about player score, color and pieces that he has
"""


class Player():
    def __init__(self, color, pieces):
        if color not in ["b", "w"]:
            raise ValueError("Player color can only be set to 'b' or 'w'")
        self.color = color
        self.pieces = pieces

    def get_score(self):
        score = 0
        for piece in self.pieces:
            if piece.name[1] in ["h", "b"]:
                score += 3
            elif piece.name[1] == "p":
                score += 1
            elif piece.name[1] == "q":
                score += 9
            elif piece.name[1] == "r":
                score += 5
        return score

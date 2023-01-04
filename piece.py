"""
This class holds every piece information and the way it moves
"""


class Piece():
    def __init__(self, name):
        if not name:
            raise ValueError("Piece must have name")
        self.name = name

    def check_if_position_is_valid(self):
        posX = self.position[0]
        posY = self.position[1]
        return posX <= 7 and posY <= 7 and posX >= 0 and posY >= 0

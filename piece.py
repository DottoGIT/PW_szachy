class Piece():
    """ This class holds basic   piece information """
    
    def __init__(self, name, position):
        if len(name) != 2 or name[0] not in ["w", "b"] or name[1] not in ["r", "h", "b", "q", "k", "p"]:
            raise ValueError("Incorrect piece name")
        self.name = name
        if not self.check_if_position_is_valid(position):
            raise ValueError("Piece position invalid")
        self.position = position
        self.move_count = 0

    def get_player(self):
        """ returns piece owner color """
        return self.name[0]

    def set_position(self, position):
        """ changes piece position to given one """
        if self.check_if_position_is_valid(position):
            self.position = position
            self.move_count += 1
        else:
            raise ValueError("Piece position invalid")

    def check_if_position_is_valid(self, position):
        """ makes sure that given position exists on board """
        posX = position[0]
        posY = position[1]
        return posX <= 7 and posY <= 7 and posX >= 0 and posY >= 0

    def __str__(self):
        """ returns piece name as string """
        return self.name

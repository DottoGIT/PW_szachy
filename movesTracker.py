""" This class is responsible for remembering moves done by players and saving them to text file """

from datetime import datetime

class MovesTracker():
    def __init__(self):
        self.move_record = []

    def record_move(self, piece, position, player_color):
        # convert move to string
        move_str = self.pos_to_string(piece.position) + "->" + self.pos_to_string(position)
        new_move = {}
        if player_color == "w":
            new_move = {"w": move_str, "b": ""}
            self.move_record.append(new_move)
        else:
            self.move_record[len(self.move_record)-1]["b"] = move_str
        

    def pos_to_string(self, pos):
        row_value = {0:"8", 1:"7", 2:"6", 3 :"5", 4:"4", 5:"3", 6:"2",7:"1"}
        col_value = {0:"A", 1:"B", 2:"C", 3 :"D", 4:"E", 5:"F", 6:"G",7:"H"}
        return col_value[pos[1]] + row_value[pos[0]]
    
    def save_move_record(self):
        file_name = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")+".txt"
        with open(f"saved_games/{file_name}", "x") as file:
            file.write("Num \t | White \t | Black\n")
            index = 1
            for move in self.move_record:
                file.write(f"{index}.\t\t | {move['w']} \t | {move['b']}\n")
                index += 1
        
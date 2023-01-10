from datetime import datetime


class MovesTracker():
    """ This class is responsible for remembering moves done by players and saving them to text file """
    
    def __init__(self):
        self.move_record = []
        self.board_positions_recorded = []

    def record_move(self, piece, position, player_color):
        """ records move to move_record in format: [letter][number]->[letter][number]"""
        # convert move to string
        move_str = self.pos_to_string(piece.position) + "->" + self.pos_to_string(position)
        new_move = {}
        if player_color == "w":
            new_move = {"w": move_str, "b": ""}
            self.move_record.append(new_move)
        else:
            self.move_record[len(self.move_record)-1]["b"] = move_str

    def record_board(self, game_state):
        """ Saves board status as string """
        self.board_positions_recorded.append(game_state.board_to_str(game_state.board))

    def pos_to_string(self, pos):
        """ Converts position to format [letter][number] """
        row_value = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
        col_value = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
        return col_value[pos[1]] + row_value[pos[0]]

    def save_move_record(self):
        """ Saves move_record to text file in format [date]_[hour].txt """
        file_name = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")+".txt"
        with open(f"saved_games/{file_name}", "x") as file:
            file.write("Num\t | White \t | Black\n")
            index = 1
            for move in self.move_record:
                file.write(f"{index}.\t | {move['w']} \t | {move['b']}\n")
                index += 1

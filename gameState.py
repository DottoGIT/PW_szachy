"""
This class is responsible for keeping current pieces positions, and returning board data
"""
from piece import Piece
from player import Player


class GameState():
    def __init__(self, board=None, current_player_color="w", is_simulated=False):
        # set up a new board if optional board is not given
        self.board = self.initialize_board() if not board else board
        # assign players
        self.plr_black = Player("b", self.find_all_pieces_of_color("b"))
        self.plr_white = Player("w", self.find_all_pieces_of_color("w"))
        self.current_player = self.plr_white if current_player_color == "w" else self.plr_black
        self.current_opponent = self.plr_black if current_player_color == "w" else self.plr_white
        # other important variables 
        self.lastly_moved_piece = None
        self.is_simulated = is_simulated
        # lists for unusual actions that can occur during piece move
        self.an_passant_tiles = {}
        self.castle_tiles = {}

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

    def duplicate_board(self):
        """because self.board.copy() doesnt work for some reason"""
        new_board = []
        for row in range(8):
            new_row = []
            for column in range(8):
                if self.board[row][column] is not None:
                    new_row.append(Piece(self.board[row][column].name, (row, column)))
                else:
                    new_row.append(None)
            new_board.append(new_row)
        return new_board

    def print_board(self, board):
        end_str = ""
        for row in range(8):
            row_str = ""
            for column in range(8):
                if board[row][column] is not None:
                    row_str += "[" + board[row][column].name + "]"
                else:
                    row_str += "[  ]"
            end_str += row_str + "\n"
        print(end_str)
                

    def move_piece(self, piece, position):
        """Moves piece from its position to given one"""
        # Change positions
        self.board[piece.position[0]][piece.position[1]] = None
        self.board[position[0]][position[1]] = piece
        piece.set_position((position[0], position[1]))

        # Check for pawn promotion
        promotion_tile = 0 if self.current_player.color == "w" else 7
        if self.pos_to_piece(position).name[1] == "p" and position[0] == promotion_tile:
            self.pos_to_piece(position).name = self.current_player.color + "q"

        # check if move was an passant
        if position in self.an_passant_tiles:
            self.remove_a_piece(self.an_passant_tiles[position])
            self.an_passant_tiles = {}

        # check if move was a castle
        if position in self.castle_tiles:
            self.pos_to_piece(self.castle_tiles[position][1]).set_position(self.castle_tiles[position][0])
            self.board[self.castle_tiles[position][0][0]][self.castle_tiles[position][0][1]] = self.pos_to_piece(self.castle_tiles[position][1])
            self.remove_a_piece(self.castle_tiles[position][1])

        # After move variable changes
        self.lastly_moved_piece = piece

        # switch players
        self.current_player = self.plr_white if self.current_player.color == "b" else self.plr_black
        self.current_opponent = self.plr_black if self.current_player.color == "w" else self.plr_white
        # update pieces
        self.plr_black.pieces = self.find_all_pieces_of_color("b")
        self.plr_white.pieces = self.find_all_pieces_of_color("w")

    def pos_to_piece(self, pos):
        """returns piece standing at given position"""
        return self.board[pos[0]][pos[1]]

    def remove_a_piece(self, pos):
        """Empties a position on a board"""
        self.board[pos[0]][pos[1]] = None

    def is_current_player_piece(self, pos):
        """Checks if piece standing on given position belongs to current player"""
        if not self.pos_to_piece(pos):
            return False
        return self.pos_to_piece(pos) in self.current_player.pieces

    def find_all_pieces_of_color(self, color):
        """Finds pieces that belong to white or black player"""
        if color not in ["w", "b"]:
            raise ValueError("Wrong color input")
        found_pieces = []
        for row in range(8):
            for column in range(8):
                if self.pos_to_piece((row, column)) is not None and self.pos_to_piece((row, column)).get_player() == color:
                    found_pieces.append(self.pos_to_piece((row, column)))
        return found_pieces

    def find_all_possible_moves(self):
        """return every possible move of every piece of current player"""
        possible_moves = []
        for piece in self.current_player.pieces:
            possible_moves += self.piece_valid_tiles(piece)
        return possible_moves

    def check_if_king_in_check(self):
        """Checks if any of current players pieces can capture enemy king"""
        enemy_king_name = self.current_opponent.color + "k"
        for tile in self.find_all_possible_moves():
            if self.pos_to_piece(tile) is not None and self.pos_to_piece(tile).name == enemy_king_name:
                return True
        return False

    def simulate_move_is_legal(self, current_player, piece, position):
        """Function used to make abstract moves to detect if they are legal 
        (for example, if moving a piece won't casuse a check mate in next move)"""
        board_copy = self.duplicate_board()
        simulated_board = GameState(board_copy, current_player.color, True)
        piece_simulated = simulated_board.pos_to_piece(piece.position)
        simulated_board.move_piece(piece_simulated, position)
        if simulated_board.check_if_king_in_check():
            return False
        return True


    def check_if_valid_position(self, pos):
        """Checks if position exists on a board"""
        return pos[0] >= 0 and pos[1] >= 0 and pos[0] < 8 and pos[1] < 8

    """Next functions return moves avaiable for each piece on given position"""

    def piece_valid_tiles(self, piece):
        if not piece:
            return []
        moveset = {
            "r": self.rook_valid_tiles(piece.position),
            "h": self.knight_valid_tiles(piece.position),
            "b": self.bishop_valid_tiles(piece.position),
            "q": self.queen_valid_tiles(piece.position),
            "k": self.king_valid_tiles(piece.position),
            "p": self.pawn_valid_tiles(piece.position)
        }
        # if being in simulation return moveset early to avoid stack overflow
        if self.is_simulated:
            return moveset[piece.name[1]]

        # moveset that simulates every possible move to make sure it wont lead to checkmate in next move
        real_correct_moveset = []
        for move in moveset[piece.name[1]]:
            if self.simulate_move_is_legal(self.current_player, piece, move):
                real_correct_moveset.append(move)
        return real_correct_moveset

    def rook_valid_tiles(self, pos):
        valid_moves = []

        def add_rook_moves(sign_x, sign_y):
            for offset in range(1, 8):
                offset_pos = (pos[0]+offset*sign_x, pos[1]+offset*sign_y)
                if self.check_if_valid_position(offset_pos) and not self.is_current_player_piece(offset_pos):
                    valid_moves.append(offset_pos)
                    if self.pos_to_piece(offset_pos) is not None:
                        break
                else:
                    break
        # Rook horizontal movement: right
        add_rook_moves(1, 0)
        # Rook horizontal movement: left
        add_rook_moves(-1, 0)
        # Rook vertical movement: up
        add_rook_moves(0, 1)
        # Rook vertical movement: down
        add_rook_moves(0, -1)
        return valid_moves

    def knight_valid_tiles(self, pos):
        valid_moves = []

        def add_knight_moves(offset):
            if self.check_if_valid_position(offset) \
                    and not self.is_current_player_piece(offset):
                valid_moves.append(offset)

        # Top right
        add_knight_moves((pos[0]-2, pos[1]+1))
        add_knight_moves((pos[0]-1, pos[1]+2))
        # Bottom right
        add_knight_moves((pos[0]+2, pos[1]+1))
        add_knight_moves((pos[0]+1, pos[1]+2))
        # Bottom left
        add_knight_moves((pos[0]+2, pos[1]-1))
        add_knight_moves((pos[0]+1, pos[1]-2))
        # Top left
        add_knight_moves((pos[0]-2, pos[1]-1))
        add_knight_moves((pos[0]-1, pos[1]-2))
        return valid_moves

    def bishop_valid_tiles(self, pos):
        valid_moves = []

        def add_diagonal_moves(offset_x, offset_y):
            for tile in range(1, 8):
                offset = (pos[0]+tile*offset_x, pos[1]+tile*offset_y)
                if self.check_if_valid_position(offset) and not self.is_current_player_piece(offset):
                    valid_moves.append(offset)
                    if self.pos_to_piece(offset) is not None:
                        break
                else:
                    break

        # Top right
        add_diagonal_moves(-1, 1)
        # Bottom right
        add_diagonal_moves(1, 1)
        # Bottom left
        add_diagonal_moves(1, -1)
        # Top left
        add_diagonal_moves(-1, -1)

        return valid_moves

    def queen_valid_tiles(self, pos):
        return self.rook_valid_tiles(pos) + self.bishop_valid_tiles(pos)

    def king_valid_tiles(self, pos):
        valid_moves = []

        def add_if_valid_move(offset_x, offset_y):
            offset = (pos[0] + offset_x, pos[1] + offset_y)
            if self.check_if_valid_position(offset) and not self.is_current_player_piece(offset):
                valid_moves.append(offset)

        add_if_valid_move(-1, -1)
        add_if_valid_move(-1, 0)
        add_if_valid_move(-1, 1)
        add_if_valid_move(0, -1)
        add_if_valid_move(0, 1)
        add_if_valid_move(1, -1)
        add_if_valid_move(1, 0)
        add_if_valid_move(1, 1)

        offset = 1 if self.current_player.color == "w" else -1

        # short castle white
        short_castle_condition = True
        for i in range(1, 3):
            if not self.check_if_valid_position((pos[0], pos[1] + i*offset)) or self.pos_to_piece((pos[0], pos[1] + i*offset)) is not None:
                short_castle_condition = False
                break
        r_pos = (pos[0], pos[1] + 3*offset)
        if not self.check_if_valid_position(r_pos) or not self.pos_to_piece(r_pos) is not None or not self.pos_to_piece(r_pos).name == self.current_player.color + "r" \
                or self.pos_to_piece(r_pos).move_count != 0 or self.pos_to_piece(pos).move_count != 0:
            short_castle_condition = False

        if short_castle_condition:
            valid_moves.append((pos[0], pos[1] + 2*offset))
            self.castle_tiles[(pos[0], pos[1] + 2*offset)] = [(pos[0], pos[1] + 1*offset), (pos[0], pos[1] + 3*offset)]

        # long castle white
        long_castle_condition = True
        for i in range(1, 4):
            if not self.check_if_valid_position((pos[0], pos[1] - i*offset)) or self.pos_to_piece((pos[0], pos[1] - i*offset)) is not None:
                long_castle_condition = False
                break
        r_pos = (pos[0], pos[1] - 4*offset)
        if not self.check_if_valid_position(r_pos) or not self.pos_to_piece(r_pos) is not None or not self.pos_to_piece(r_pos).name == self.current_player.color + "r" \
                or self.pos_to_piece(r_pos).move_count != 0 or self.pos_to_piece(pos).move_count != 0:
            long_castle_condition = False

        if long_castle_condition:
            valid_moves.append((pos[0], pos[1] - 2*offset))
            self.castle_tiles[(pos[0], pos[1] - 2*offset)] = [(pos[0], pos[1] - 1*offset), (pos[0], pos[1] - 4*offset)]

        return valid_moves

    def pawn_valid_tiles(self, pos):
        valid_moves = []
        plr_offset = 0
        if self.current_player.color == "b":
            plr_offset = 1
        elif self.current_player.color == "w":
            plr_offset = -1

        # basic move
        offset = (pos[0]+plr_offset, pos[1])
        if self.check_if_valid_position(offset) and not self.pos_to_piece(offset) is not None:
            valid_moves.append(offset)

        # if first move
        offset = (pos[0]+2*plr_offset, pos[1])
        if self.check_if_valid_position(offset) and self.pos_to_piece(pos).move_count == 0 and not self.pos_to_piece(offset) is not None:
            valid_moves.append(offset)

        # capture moves
        offset = (pos[0]+plr_offset, pos[1]+plr_offset)
        if self.check_if_valid_position(offset) and (self.pos_to_piece(offset) is not None and not self.is_current_player_piece(offset)):
            valid_moves.append(offset)
        offset = (pos[0]+plr_offset, pos[1]-plr_offset)
        if self.check_if_valid_position(offset) and (self.pos_to_piece(offset) is not None and not self.is_current_player_piece(offset)):
            valid_moves.append(offset)

        # en passant
        offset = (pos[0], pos[1] + plr_offset)
        if self.check_if_valid_position(offset) and self.pos_to_piece(offset) is not None and not self.is_current_player_piece(offset) \
            and self.pos_to_piece(offset).move_count == 1 and self.pos_to_piece(offset) == self.lastly_moved_piece \
                and offset[0] == int((1/2)*plr_offset + 7/2) and self.pos_to_piece(offset).name[1] == "p":
            valid_moves.append((offset[0]+plr_offset, offset[1]))
            self.an_passant_tiles[(offset[0]+plr_offset, offset[1])] = offset

        offset = (pos[0], pos[1] - plr_offset)
        if self.check_if_valid_position(offset) and self.pos_to_piece(offset) is not None and not self.is_current_player_piece(offset) \
            and self.pos_to_piece(offset).move_count == 1 and self.pos_to_piece(offset) == self.lastly_moved_piece \
                and offset[0] == int((1/2)*plr_offset + 7/2) and self.pos_to_piece(offset).name[1] == "p":
            valid_moves.append((offset[0]+plr_offset, offset[1]))
            self.an_passant_tiles[(offset[0]+plr_offset, offset[1])] = offset

        return valid_moves


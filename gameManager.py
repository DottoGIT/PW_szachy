"""
This class is responsible for window display, and managing gamestate and moves
"""

import pygame
from gameState import GameState
from player import Player


class GameManager():
    def __init__(self, window, board_size, tile_colors):
        self.window = window
        self.tile_colors = tile_colors
        if window.get_width() < board_size or window.get_height() < board_size:
            raise ValueError("window is to small to contain board")
        self.board_size = board_size
        self.game_state = GameState()
        self.cell_size = self.board_size//8
        self.plr_black = Player("b", self.find_all_pieces_of_color("b"))
        self.plr_white = Player("w", self.find_all_pieces_of_color("w"))
        self.current_player = self.plr_white
        self.current_opponent = self.plr_black
        self.piece_in_hand = None
        self.lastly_moved_piece = None
        self.currently_valid_moves = []
        self.an_passant_tiles = {}
        self.currently_defended_tiles = []

    def update(self, events):
        """Game loop"""
        self.draw_board()
        # Wait for player move
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_tile = self.pos_to_tile(pygame.mouse.get_pos())
                # Grabbing a piece
                if self.piece_in_hand is None or clicked_tile not in self.currently_valid_moves:
                    taken_piece = self.pos_to_piece(clicked_tile)
                    if self.check_if_valid_piece(taken_piece) and self.is_current_player_piece(taken_piece.position):
                        self.piece_in_hand = taken_piece
                    else:
                        self.piece_in_hand = None
                # Moving a piece
                else:
                    self.move_piece(self.piece_in_hand, clicked_tile)
                    self.currently_defended_tiles = self.find_defended_tiles()
                    self.lastly_moved_piece = self.piece_in_hand
                    self.check_if_pawn_promotion(clicked_tile)
                    self.piece_in_hand = None
                    # check if move was an passant
                    if clicked_tile in self.an_passant_tiles:
                        self.take_a_piece(self.an_passant_tiles[clicked_tile])
                        self.an_passant_tiles = {}
                    # switch players
                    self.current_player = self.plr_white if self.current_player.color == "b" else self.plr_black
                    self.current_opponent = self.plr_black if self.current_player.color == "b" else self.plr_white

        # Highlight avaiable moves
        self.currently_valid_moves = self.piece_valid_tiles(self.piece_in_hand) if self.piece_in_hand is not None else []
        self.highlight_tiles(self.currently_valid_moves)

        self.load_pieces()

    def pos_to_piece(self, pos):
        """returns piece standing at given position"""
        return self.game_state.board[pos[0]][pos[1]]

    def move_piece(self, piece, position):
        """Sends an information to GameState to move a piece"""
        self.game_state.move_piece(piece, position)

    def draw_board(self):
        """Displays board on window"""
        cell_dimension = self.cell_size
        for row in range(8):
            for column in range(8):
                cell = pygame.Rect(row*cell_dimension, column*cell_dimension, cell_dimension, cell_dimension)
                # Draw cell
                pygame.draw.rect(self.window, self.tile_colors[(row + column) % 2], cell)

    def load_pieces(self):
        """Loads pieces images on drawn board"""
        cell_dimension = self.cell_size
        for row in range(8):
            for column in range(8):
                cell = pygame.Rect(row*cell_dimension, column*cell_dimension, cell_dimension, cell_dimension)
                if self.pos_to_piece((column, row)) is not None:
                    img_path = f"pieces/{self.pos_to_piece((column, row)).name}.png"
                    img = pygame.transform.scale(pygame.image.load(img_path), (cell_dimension, cell_dimension))
                    self.window.blit(img, cell)

    def find_all_pieces_of_color(self, color):
        """Finds pieces that belong to white or black player"""
        if color not in ["w", "b"]:
            raise ValueError("Wrong color input")
        found_pieces = []
        for row in range(8):
            for column in range(8):
                if self.check_if_place_occupied((row, column)) and self.pos_to_piece((row, column)).get_player() == color:
                    found_pieces.append(self.pos_to_piece((row, column)))
        return found_pieces

    def is_current_player_piece(self, pos):
        if not self.pos_to_piece(pos):
            return False
        return self.pos_to_piece(pos) in self.current_player.pieces

    def take_a_piece(self, pos):
        """Empties a position on a board"""
        self.game_state.board[pos[0]][pos[1]] = None

    def pos_to_tile(self, pos):
        """Takes mouse position and converts it to chess tile coordinates"""
        cell_dimension = self.cell_size
        return pos[1] // cell_dimension, pos[0] // cell_dimension

    def check_if_valid_piece(self, piece):
        """Checks if clicked piece can be moved by player"""
        return piece is not None

    def check_if_valid_position(self, pos):
        """Checks if position exists on board"""
        return pos[0] >= 0 and pos[1] >= 0 and pos[0] < 8 and pos[1] < 8

    def check_if_place_occupied(self, pos):
        """Checks if given tile has a piece"""
        return self.pos_to_piece(pos) is not None

    def highlight_tiles(self, tiles):
        """Marks given tiles with a gray circle"""
        if not tiles:
            return
        for tile in tiles:
            target_pos = (tile[1]*self.cell_size + self.cell_size/2, tile[0]*self.cell_size + self.cell_size/2)
            pygame.draw.circle(self.window, (9, 188, 138), target_pos, self.cell_size/8)

    def check_if_pawn_promotion(self, pos):
        """Promotes a pawn if it goes to the edge of the board"""
        promotion_tile = 0 if self.current_player.color == "w" else 7
        if self.pos_to_piece(pos).name[1] == "p" and pos[0] == promotion_tile:
            self.pos_to_piece(pos).name = self.current_player.color + "q"

    def find_defended_tiles(self):
        """checks if any of opponent pieces can move to given tile in next turn"""
        defended_tiles = []
        for piece in self.current_player.pieces:
            defended_tiles += self.piece_valid_tiles(piece, True)
        return defended_tiles

    """Next functions return moves avaiable for each piece on given position, threat_mode is used for finding tiles defended by piece"""

    def piece_valid_tiles(self, piece, threat_mode=False):
        moveset = {
            "r": self.rook_valid_tiles(piece.position, threat_mode),
            "h": self.knight_valid_tiles(piece.position, threat_mode),
            "b": self.bishop_valid_tiles(piece.position, threat_mode),
            "q": self.queen_valid_tiles(piece.position, threat_mode),
            "k": self.king_valid_tiles(piece.position, threat_mode),
            "p": self.pawn_valid_tiles(piece.position, threat_mode)
        }
        return moveset[piece.name[1]]

    def rook_valid_tiles(self, pos, threat_mode=False):
        valid_moves = []

        def add_rook_moves(sign_x, sign_y):
            for offset in range(1, 8):
                offset_pos = (pos[0]+offset*sign_x, pos[1]+offset*sign_y)
                if self.check_if_valid_position(offset_pos) and not self.is_current_player_piece(offset_pos):
                    valid_moves.append(offset_pos)
                    if self.check_if_place_occupied(offset_pos):
                        break
                else:
                    if threat_mode and self.check_if_valid_position(offset_pos):
                        valid_moves.append(offset_pos)
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

    def knight_valid_tiles(self, pos, threat_mode=False):
        valid_moves = []

        def add_knight_moves(offset):
            if self.check_if_valid_position(offset) \
                    and not self.is_current_player_piece(offset):
                valid_moves.append(offset)
            elif threat_mode and self.check_if_valid_position(offset):
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

    def bishop_valid_tiles(self, pos, threat_mode=False):
        valid_moves = []

        def add_diagonal_moves(offset_x, offset_y):
            for tile in range(1, 8):
                offset = (pos[0]+tile*offset_x, pos[1]+tile*offset_y)
                if self.check_if_valid_position(offset) and not self.is_current_player_piece(offset):
                    valid_moves.append(offset)
                    if self.check_if_place_occupied(offset):
                        break
                else:
                    if threat_mode and self.check_if_valid_position(offset):
                        valid_moves.append(offset)
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

    def queen_valid_tiles(self, pos, threat_mode=False):
        return self.rook_valid_tiles(pos, threat_mode) + self.bishop_valid_tiles(pos, threat_mode)

    def king_valid_tiles(self, pos, threat_mode=False):
        valid_moves = []

        def add_if_valid_move(offset_x, offset_y):
            offset = (pos[0] + offset_x, pos[1] + offset_y)
            if self.check_if_valid_position(offset) and not self.is_current_player_piece(offset) and offset not in self.currently_defended_tiles:
                valid_moves.append(offset)
            elif self.check_if_valid_position(offset) and threat_mode:
                valid_moves.append(offset)

        add_if_valid_move(-1, -1)
        add_if_valid_move(-1, 0)
        add_if_valid_move(-1, 1)
        add_if_valid_move(0, -1)
        add_if_valid_move(0, 1)
        add_if_valid_move(1, -1)
        add_if_valid_move(1, 0)
        add_if_valid_move(1, 1)

        return valid_moves

    def pawn_valid_tiles(self, pos, threat_mode=False):
        valid_moves = []
        plr_offset = 0
        if self.current_player.color == "b":
            plr_offset = 1
        elif self.current_player.color == "w":
            plr_offset = -1

        # basic move
        offset = (pos[0]+plr_offset, pos[1])
        if self.check_if_valid_position(offset) and not self.check_if_place_occupied(offset) and not threat_mode:
            valid_moves.append(offset)
        # if first move
        offset = (pos[0]+2*plr_offset, pos[1])
        if self.check_if_valid_position(offset) and self.pos_to_piece((pos[0], pos[1])).move_count == 0 and not self.check_if_place_occupied(offset) and not threat_mode:
            valid_moves.append(offset)
        # capture moves
        offset = (pos[0]+plr_offset, pos[1]+plr_offset)
        if self.check_if_valid_position(offset) and (self.check_if_place_occupied(offset) and not self.is_current_player_piece(offset)) or threat_mode:
            valid_moves.append(offset)
        offset = (pos[0]+plr_offset, pos[1]-plr_offset)
        if self.check_if_valid_position(offset) and (self.check_if_place_occupied(offset) and not self.is_current_player_piece(offset)) or threat_mode:
            valid_moves.append(offset)
        # en passant
        offset = (pos[0], pos[1] + plr_offset)
        if self.check_if_valid_position(offset) and self.check_if_place_occupied(offset) and not self.is_current_player_piece(offset) \
            and self.pos_to_piece(offset).move_count == 1 and self.pos_to_piece(offset) == self.lastly_moved_piece \
                and offset[0] == int((1/2)*plr_offset + 7/2) and self.pos_to_piece(offset).name[1] == "p":
            valid_moves.append((offset[0]+plr_offset, offset[1]))
            self.an_passant_tiles[(offset[0]+plr_offset, offset[1])] = offset
        offset = (pos[0], pos[1] - plr_offset)
        if self.check_if_valid_position(offset) and self.check_if_place_occupied(offset) and not self.is_current_player_piece(offset) \
            and self.pos_to_piece(offset).move_count == 1 and self.pos_to_piece(offset) == self.lastly_moved_piece \
                and offset[0] == int((1/2)*plr_offset + 7/2) and self.pos_to_piece(offset).name[1] == "p":
            valid_moves.append((offset[0]+plr_offset, offset[1]))
            self.an_passant_tiles[(offset[0]+plr_offset, offset[1])] = offset

        return valid_moves

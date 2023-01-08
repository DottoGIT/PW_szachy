"""
This class is responsible for managing classes and player input
"""

import pygame
from gameState import GameState
from display import Display


class GameManager():

    # Debug settings
    highlight_available_moves = False
    highlight_checks = True

    def __init__(self, window, board_size, tile_colors):

        if window.get_width() < board_size or window.get_height() < board_size:
            raise ValueError("window is to small to contain board")

        self.window = window
        self.tile_colors = tile_colors
        self.board_size = board_size
        
        self.init_new_game()

    def init_new_game(self):
        self.game_state = GameState()
        self.display = Display(self.window, self.board_size, self)
        self.piece_in_hand = None
        self.is_player_in_check = (False, None)
        self.game_over_data = {"is_over": False, "winner": "", "end_type": ""}
        self.currently_valid_moves = []
        self.an_passant_tiles = {}
        self.castle_tiles = {}


    def update(self, events):
        """Game loop"""
        self.display.draw_board(self.tile_colors)
        # Wait for player move
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_tile = self.mouse_pos_to_tile(pygame.mouse.get_pos())
                # Grabbing a piece
                if self.piece_in_hand is None or clicked_tile not in self.currently_valid_moves:
                    taken_piece = self.game_state.pos_to_piece(clicked_tile)
                    if taken_piece is not None and self.game_state.is_current_player_piece(taken_piece.position):
                        self.piece_in_hand = taken_piece
                    else:
                        self.piece_in_hand = None
                # Moving a piece
                else:
                    self.game_state.move_piece(self.piece_in_hand, clicked_tile)
                    self.piece_in_hand = None
                    # Check if under check
                    if self.game_state.check_if_player_in_check():
                        self.is_player_in_check = (True, [self.game_state.find_kings()[0]])
                    else:
                        self.is_player_in_check = (False, None)
                    # Check if game over
                    if len(self.game_state.find_all_player_moves()) == 0:
                        if self.is_player_in_check[0]:
                            self.game_over_data["is_over"] = True
                            self.game_over_data["winner"] = "Black won" if self.game_state.current_player.color == "w" else "White won"
                            self.game_over_data["end_type"] = "Checkmate"
                        else:
                            self.game_over_data["is_over"] = True
                            self.game_over_data["winner"] = "Draw"
                            self.game_over_data["end_type"] = "Stalemate"
                    elif not self.game_state.can_opponent_mate() and not self.game_state.can_player_mate():
                            self.game_over_data["is_over"] = True
                            self.game_over_data["winner"] = "Draw"
                            self.game_over_data["end_type"] = "Not enough mate material"

                self.currently_valid_moves = self.game_state.piece_valid_tiles(self.piece_in_hand)


        if self.highlight_checks and self.is_player_in_check: self.display.highlight_tiles(self.is_player_in_check[1], (255,0,0),2) 
        self.display.load_pieces(self.game_state)
        # Highlight avaiable moves
        self.display.highlight_tiles(self.currently_valid_moves, (9, 188, 138))
        if self.highlight_available_moves: self.display.highlight_tiles(self.game_state.find_all_player_moves(), (255,0,0))
        # Display game over screen if needed
        if self.game_over_data["is_over"]:
            self.display.display_game_over_screen(self.game_over_data["winner"], self.game_over_data["end_type"])


    def mouse_pos_to_tile(self, pos):
        """Takes mouse position and converts it to chess tile coordinates"""
        cell_dimension = self.board_size//8
        return pos[1] // cell_dimension, pos[0] // cell_dimension

    def restart_game(self):
        self.init_new_game()
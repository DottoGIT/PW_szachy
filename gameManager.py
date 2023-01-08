"""
This class is responsible for managing classes and player input
"""

import pygame
from gameState import GameState
from display import Display


class GameManager():

    # Debug settings
    highlight_available_moves = False

    def __init__(self, window, board_size, tile_colors):

        if window.get_width() < board_size or window.get_height() < board_size:
            raise ValueError("window is to small to contain board")

        self.window = window
        self.tile_colors = tile_colors
        self.board_size = board_size

        self.game_state = GameState()
        self.display = Display(self.window, self.board_size)

        self.piece_in_hand = None
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
                self.currently_valid_moves = self.game_state.piece_valid_tiles(self.piece_in_hand)


        self.display.load_pieces(self.game_state)
        # Highlight avaiable moves
        self.display.highlight_tiles(self.currently_valid_moves, (9, 188, 138))
        if self.highlight_available_moves: self.display.highlight_tiles(self.game_state.find_all_possible_moves(), (255,0,0))

    
    def mouse_pos_to_tile(self, pos):
        """Takes mouse position and converts it to chess tile coordinates"""
        cell_dimension = self.board_size//8
        return pos[1] // cell_dimension, pos[0] // cell_dimension

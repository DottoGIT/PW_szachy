"""
This class is responsible for window display, and player moves
"""

import pygame
from gameState import GameState


class GameManager():
    def __init__(self, window, board_size, tile_colors):

        if window.get_width() < board_size or window.get_height() < board_size:
            raise ValueError("window is to small to contain board")

        self.window = window
        self.tile_colors = tile_colors
        self.board_size = board_size
        self.cell_size = self.board_size//8

        self.game_state = GameState()

        self.piece_in_hand = None
        self.an_passant_tiles = {}
        self.castle_tiles = {}

    def update(self, events):
        """Game loop"""
        self.draw_board()
        # Wait for player move
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_tile = self.mouse_pos_to_tile(pygame.mouse.get_pos())
                # Grabbing a piece
                if self.piece_in_hand is None or clicked_tile not in self.game_state.piece_valid_tiles(self.piece_in_hand):
                    taken_piece = self.game_state.pos_to_piece(clicked_tile)
                    if taken_piece is not None and self.game_state.is_current_player_piece(taken_piece.position):
                        self.piece_in_hand = taken_piece
                    else:
                        self.piece_in_hand = None
                # Moving a piece
                else:
                    self.game_state.move_piece(self.piece_in_hand, clicked_tile)
                    self.piece_in_hand = None

        # Highlight avaiable moves
        self.currently_valid_moves = self.game_state.piece_valid_tiles(self.piece_in_hand) if self.piece_in_hand is not None else []

        self.load_pieces()
        self.highlight_tiles(self.currently_valid_moves)

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
                if self.game_state.pos_to_piece((column, row)) is not None:
                    img_path = f"pieces/{self.game_state.pos_to_piece((column, row)).name}.png"
                    img = pygame.transform.scale(pygame.image.load(img_path), (cell_dimension, cell_dimension))
                    self.window.blit(img, cell)

    def mouse_pos_to_tile(self, pos):
        """Takes mouse position and converts it to chess tile coordinates"""
        cell_dimension = self.cell_size
        return pos[1] // cell_dimension, pos[0] // cell_dimension

    def highlight_tiles(self, tiles):
        """Marks given tiles with a gray circle"""
        if not tiles:
            return
        for tile in tiles:
            target_pos = (tile[1]*self.cell_size + self.cell_size/2, tile[0]*self.cell_size + self.cell_size/2)
            pygame.draw.circle(self.window, (9, 188, 138), target_pos, self.cell_size/8)

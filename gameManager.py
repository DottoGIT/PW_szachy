"""
This class is responsible for display and player interaction with pieces
"""

import pygame
from gameState import GameState


class GameManager():
    def __init__(self, window, board_size, tile_colors):
        self.window = window
        self.tile_colors = tile_colors
        if window.get_width() < board_size or window.get_height() < board_size:
            raise ValueError("window is to small to contain board")
        self.board_size = board_size
        self.game_state = GameState()

    def update(self):
        self.draw_board()

    def draw_board(self):
        cell_dimension = self.board_size//8
        for row in range(8):
            for column in range(8):
                cell = pygame.Rect(row*cell_dimension, column*cell_dimension, cell_dimension, cell_dimension)
                # Draw cell
                pygame.draw.rect(self.window, self.tile_colors[(row + column) % 2], cell)
                # Render pieces
                if self.game_state.board[column][row] is not None:
                    img_path = f"pieces/{self.game_state.board[column][row].name}.png"
                    img = pygame.transform.scale(pygame.image.load(img_path), (cell_dimension, cell_dimension))
                    self.window.blit(img, cell)


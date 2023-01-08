"""This class is responsible for drawing and loading images into main window"""

import pygame

class Display():
    def __init__(self, window, board_size):
        self.window = window
        self.board_size = board_size

    def draw_board(self, tile_colors):
        """Displays board on window"""
        cell_dimension = self.board_size//8
        for row in range(8):
            for column in range(8):
                cell = pygame.Rect(row*cell_dimension, column*cell_dimension, cell_dimension, cell_dimension)
                pygame.draw.rect(self.window, tile_colors[(row + column) % 2], cell)

    def load_pieces(self, game_state):
        """Loads pieces images on drawn board"""
        cell_dimension = self.board_size//8
        for row in range(8):
            for column in range(8):
                cell = pygame.Rect(row*cell_dimension, column*cell_dimension, cell_dimension, cell_dimension)
                if game_state.pos_to_piece((column, row)) is not None:
                    img_path = f"pieces/{game_state.pos_to_piece((column, row)).name}.png"
                    img = pygame.transform.scale(pygame.image.load(img_path), (cell_dimension, cell_dimension))
                    self.window.blit(img, cell)

    def highlight_tiles(self, tiles, color):
        """Marks given tiles with a gray circle"""
        cell_dimension = self.board_size//8
        if not tiles:
            return
        for tile in tiles:
            target_pos = (tile[1]*cell_dimension + cell_dimension/2, tile[0]*cell_dimension + cell_dimension/2)
            pygame.draw.circle(self.window, color, target_pos, cell_dimension/8)
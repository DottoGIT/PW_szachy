"""This class is responsible for drawing and loading images into main window"""

import pygame

class Display():
    def __init__(self, window, board_size, game_manager):
        self.window = window
        self.board_size = board_size
        self.save_clicked = False
        self.restart_clicked = False
        self.game_manager = game_manager

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

    def highlight_tiles(self, tiles, color, size=8):
        """Marks given tiles with a gray circle"""
        cell_dimension = self.board_size//8
        if not tiles:
            return
        for tile in tiles:
            target_pos = (tile[1]*cell_dimension + cell_dimension/2, tile[0]*cell_dimension + cell_dimension/2)
            pygame.draw.circle(self.window, color, target_pos, cell_dimension/size)
    
    def display_game_over_screen(self, who_won, win_type):
        """Displays window that shows who won and two buttons - restart - save"""
        border_size = 8
        window_width = self.board_size/3
        window_height = self.board_size/4 - 20
        window_pos_x = self.board_size/2 - (1/2)*window_width
        window_pos_y = self.board_size/2 - (1/2)*window_height
        window_rect_border = pygame.Rect(window_pos_x - border_size/2, window_pos_y - border_size/2, window_width + border_size, window_height + border_size)
        window_rect = pygame.Rect(window_pos_x, window_pos_y, window_width, window_height)
        # Win type text
        font = pygame.font.SysFont("arialblack",45)
        wt = font.render(who_won, True, (100, 100, 100))
        wt_offset_x = window_pos_x - wt.get_width()/2 + window_width/2
        wt_offset_y = window_pos_y - wt.get_height()/2 + 30
        # Winner text
        font = pygame.font.SysFont("arialblack", 20)
        win = font.render(win_type, True, (100, 100, 100))
        win_offset_x = window_pos_x - win.get_width()/2 + window_width/2
        win_offset_y = window_pos_y - win.get_height()/2 + 70
        # Restart button
        restart_pos_x = window_pos_x + 8
        restart_pos_y = window_pos_y + 130
        restart_width = window_width/2.5
        restart_height = window_height/3
        res_img = pygame.transform.scale(pygame.image.load("Buttons/restart_btn.png"), (restart_width, restart_height))
        res_rect = pygame.Rect(restart_pos_x,restart_pos_y,restart_width,restart_height)
        # Save button
        save_pos_x = window_pos_x + 170
        save_pos_y = window_pos_y + 130
        save_width = window_width/2.5
        save_height = window_height/3
        save_img = pygame.transform.scale(pygame.image.load("Buttons/save_btn.png"), (save_width, save_height))
        save_rect = pygame.Rect(save_pos_x,save_pos_y,save_width,save_height)
        
        # Display everything
        pygame.draw.rect(self.window, (0, 0, 0), window_rect_border)
        pygame.draw.rect(self.window, (255, 255, 255), window_rect)
        self.window.blit(wt, (wt_offset_x, wt_offset_y))
        self.window.blit(win, (win_offset_x, win_offset_y))
        self.window.blit(res_img, res_rect)
        self.window.blit(save_img, save_rect)

        # check for button clicks
        mouse_pos = pygame.mouse.get_pos()
        # Save
        if save_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not self.save_clicked:
            print("Click save") 
            self.save_clicked = True
        elif not pygame.mouse.get_pressed()[0]:
            self.save_clicked = False
        # Restart
        if res_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not self.restart_clicked:
            self.game_manager.restart_game()
            self.restart_clicked = True
        elif not pygame.mouse.get_pressed()[0]:
            self.restart_clicked = False
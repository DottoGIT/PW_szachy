"""This class is responsible for drawing and loading images into main window"""

import pygame

class Display():
    def __init__(self, window, board_size, game_manager):
        self.window = window
        self.board_size = board_size
        self.actual_board_size = self.board_size//8 * 8
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
    
    def display_game_over_screen(self, who_won, win_type, move_tracker):
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
        if not self.save_clicked:
            save_img = pygame.transform.scale(pygame.image.load("Buttons/save_btn.png"), (save_width, save_height))
        else:
            save_img = pygame.transform.scale(pygame.image.load("Buttons/saved_btn.png"), (save_width, save_height))

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
            move_tracker.save_move_record()
            self.save_clicked = True
        # Restart
        if res_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not self.restart_clicked:
            self.save_clicked = False
            self.game_manager.init_new_game()
            self.restart_clicked = True
        elif not pygame.mouse.get_pressed()[0]:
            self.restart_clicked = False

    def show_move_record(self, move_record):
        # Draw move board
        move_board = pygame.Rect(self.actual_board_size, 0, self.window.get_width() - self.actual_board_size, self.actual_board_size - 150)
        current_move_tile = pygame.Rect(self.actual_board_size, 0, self.window.get_width() - self.actual_board_size, 50)
        move_board_line_1 = pygame.Rect(self.actual_board_size + 75, 0, 5, self.actual_board_size - 150)
        move_board_line_2 = pygame.Rect(self.actual_board_size + 190, 0, 5, self.actual_board_size - 150)
        pygame.draw.rect(self.window, (76,76,71), move_board)
        pygame.draw.rect(self.window, (120,120,115), current_move_tile)
        pygame.draw.rect(self.window, (50,50,45), move_board_line_1)
        pygame.draw.rect(self.window, (50,50,45), move_board_line_2)
        move_font = pygame.font.SysFont("arialblack",25)
        num_font = pygame.font.SysFont("arialblack",40)
        hash = num_font.render("#", True, (255, 255, 255))
        players = move_font.render("white     black", True, (255, 255, 255))
        self.window.blit(hash, (self.actual_board_size + 23, -6))
        self.window.blit(players, (self.actual_board_size + 95, 7))

        
        def draw_move_cell(pos_y, m_number, m_white, m_black):
            num = num_font.render(m_number, True, (255, 255, 255))
            white = move_font.render(m_white, True, (255, 255, 255))
            black = move_font.render(m_black, True, (255, 255, 255))
            self.window.blit(num, (self.actual_board_size + 7, pos_y - 7))
            self.window.blit(white, (self.actual_board_size + 85, pos_y + 7))
            self.window.blit(black, (self.actual_board_size + 200, pos_y + 7))
        
        index = 1
        for move in move_record[::-1]:
            draw_move_cell(index * 50, str((len(move_record)+1) - index) + ".", move["w"], move["b"])
            index += 1
            if index > 14:
                break

    def show_player_score(self, white_score, black_score):
        # Lines
        score_board = pygame.Rect(self.actual_board_size, self.actual_board_size - 150, self.window.get_width() - self.actual_board_size, 150)
        score_board_line1 = pygame.Rect(self.actual_board_size, self.actual_board_size - 78, self.window.get_width() - self.actual_board_size, 5)
        score_board_line2 = pygame.Rect(self.actual_board_size, self.actual_board_size - 150, self.window.get_width() - self.actual_board_size, 5)
        score_board_line3 = pygame.Rect(self.actual_board_size, self.actual_board_size - 5, self.window.get_width() - self.actual_board_size, 5)
        score_board_line4 = pygame.Rect(self.actual_board_size, self.actual_board_size - 150, 5, 150)
        score_board_line5 = pygame.Rect(self.window.get_width()-5, self.actual_board_size - 150, 5, 150)
        # Text
        name_font = pygame.font.SysFont("arialblack",35)
        score_font = pygame.font.SysFont("arialblack",40)
        name_white = name_font.render("White: ", True, (255, 255, 255))
        name_black = name_font.render("Black: ", True, (255, 255, 255))
        score_white = score_font.render(white_score, True, (255, 255, 255))
        score_black = score_font.render(black_score, True, (255, 255, 255))

        # Display everything
        pygame.draw.rect(self.window, (45, 45, 42), score_board)
        pygame.draw.rect(self.window, (0, 0, 0), score_board_line1)
        pygame.draw.rect(self.window, (0, 0, 0), score_board_line2)
        pygame.draw.rect(self.window, (0, 0, 0), score_board_line3)
        pygame.draw.rect(self.window, (0, 0, 0), score_board_line4)
        pygame.draw.rect(self.window, (0, 0, 0), score_board_line5)
        self.window.blit(name_white, (self.actual_board_size + 15, self.actual_board_size - 140))
        self.window.blit(score_white, (self.actual_board_size + 210, self.actual_board_size - 145))
        self.window.blit(name_black, (self.actual_board_size + 15, self.actual_board_size - 68))
        self.window.blit(score_black, (self.actual_board_size + 210, self.actual_board_size - 73))
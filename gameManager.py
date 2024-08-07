import pygame
from gameState import GameState
from display import Display
from movesTracker import MovesTracker


class GameManager():
    """ This class is responsible for managing other classes and player input """
    # Debug settings
    highlight_available_moves = False

    def __init__(self, window, board_size, tile_colors):
        if window.get_width() < board_size or window.get_height() < board_size:
            raise ValueError("window is to small to contain board")
        self.window = window
        self.tile_colors = tile_colors
        self.board_size = board_size
        self.init_new_game()

    def init_new_game(self):
        """ Restarts every important variable setting up a new game """
        self.display = Display(self.window, self.board_size)
        self.move_tracker = MovesTracker()
        self.game_state = GameState(move_tracker=self.move_tracker)
        self.piece_in_hand = None
        self.is_player_in_check = (False, None)
        self.game_over_data = {"is_over": False, "winner": "", "end_type": ""}
        self.currently_valid_moves = []
        self.an_passant_tiles = {}
        self.castle_tiles = {}

    def update(self, events):
        """ Game loop """
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
                    self.move_tracker.record_board(self.game_state)
                    self.piece_in_hand = None
                    # Check if under check
                    if self.game_state.check_if_player_in_check():
                        self.is_player_in_check = (True, [self.game_state.find_kings()[0]])
                    else:
                        self.is_player_in_check = (False, None)
                    # Check if game over
                    # Move repetition
                    if self.check_for_move_repetition():
                        self.game_over_data["is_over"] = True
                        self.game_over_data["winner"] = "Draw"
                        self.game_over_data["end_type"] = "Move repetition"
                    if len(self.game_state.find_all_player_moves()) == 0:
                        if self.is_player_in_check[0]:
                            # Checkmate
                            self.game_over_data["is_over"] = True
                            self.game_over_data["winner"] = "Black won" if self.game_state.current_player.color == "w" else "White won"
                            self.game_over_data["end_type"] = "Checkmate"
                        else:
                            # Stalemate
                            self.game_over_data["is_over"] = True
                            self.game_over_data["winner"] = "Draw"
                            self.game_over_data["end_type"] = "Stalemate"
                    elif not self.game_state.can_opponent_mate() and not self.game_state.can_player_mate():
                        # Not enough material
                        self.game_over_data["is_over"] = True
                        self.game_over_data["winner"] = "Draw"
                        self.game_over_data["end_type"] = "Not enough mate material"

                # Update valid moves to highlight
                self.currently_valid_moves = self.game_state.piece_valid_tiles(self.piece_in_hand)

        # Highlight checks
        if self.is_player_in_check:
            self.display.highlight_tiles(self.is_player_in_check[1], (255, 0, 0), 2)

        # Display pieces on board
        self.display.load_pieces(self.game_state)

        # Highlight avaiable moves
        self.display.highlight_tiles(self.currently_valid_moves, (9, 188, 138))

        # Highligh every move if debug option is set to True
        if self.highlight_available_moves:
            self.display.highlight_tiles(self.game_state.find_all_player_moves(), (255, 0, 0))

        # Display game over screen if needed
        if self.game_over_data["is_over"]:
            self.display.display_game_over_screen(self.game_over_data["winner"], self.game_over_data["end_type"], self)

        # Display move record
        self.display.show_move_record(self.move_tracker.move_record)

        # Display player score
        score_diff_white = self.game_state.plr_white.get_score() - self.game_state.plr_black.get_score()
        if score_diff_white > 0:
            self.display.show_player_score("+" + str(score_diff_white), "")
        elif score_diff_white < 0:
            self.display.show_player_score("", "+" + str(-score_diff_white))
        else:
            self.display.show_player_score("", "")

    def mouse_pos_to_tile(self, pos):
        """ Takes mouse position and converts it to chess tile coordinates """
        cell_dimension = self.board_size//8
        return pos[1] // cell_dimension, pos[0] // cell_dimension

    def check_for_move_repetition(self):
        """ Checks if tracker contains 3 same board positions """
        if len(self.move_tracker.board_positions_recorded) < 3:
            return False
        board_dict = {}
        for board in self.move_tracker.board_positions_recorded:
            board_dict[board] = board_dict.get(board, 0) + 1
            if board_dict[board] >= 3:
                return True
        return False

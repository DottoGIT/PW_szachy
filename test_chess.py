from gameManager import GameManager
from piece import Piece
from gameState import GameState
from player import Player
from pytest import raises
from movesTracker import MovesTracker
from display import Display
import pygame

# GameManager Tests


def test_GameManager_initialization_valid():
    screen = pygame.display.set_mode((900, 900))
    colors = ("white", "gray")
    game = GameManager(screen, 900, colors)
    assert game.window == screen
    assert game.tile_colors == colors


def test_GameManager_initialization_invalid_windowTooSmall():
    screen = pygame.display.set_mode((600, 900))
    colors = ("white", "gray")
    with raises(ValueError):
        GameManager(screen, 900, colors)


def test_GameManager_pos_to_position():
    screen = pygame.display.set_mode((900, 900))
    colors = ("white", "gray")
    game = GameManager(screen, 900, colors)
    assert game.mouse_pos_to_tile((90, 10)) == (0, 0)
    assert game.mouse_pos_to_tile((162, 160)) == (1, 1)


def test_GameManager_restart_game():
    screen = pygame.display.set_mode((900, 900))
    colors = ("white", "gray")
    game = GameManager(screen, 900, colors)
    game.game_state.move_piece(game.game_state.pos_to_piece((0, 0)), (2, 0))
    assert game.game_state.pos_to_piece((2, 0)) is not None
    game.init_new_game()
    assert game.game_state.pos_to_piece((2, 0)) is None

# Piece Tests


def test_Piece_initialization_valid():
    piece = Piece("bk", (1, 5))
    assert piece.name == "bk"


def test_Piece_initialization_invalid():
    with raises(ValueError):
        Piece("", (1, 1))
    with raises(ValueError):
        Piece("bk", (1, 8))
    with raises(ValueError):
        Piece("bl", (1, 2))


def test_Piece_get_player():
    piece = Piece("wk", (0, 0))
    assert piece.get_player() == "w"


def test_Piece_set_position():
    piece = Piece("wk", (0, 0))
    assert piece.position == (0, 0)
    piece.set_position((1, 2))
    assert piece.position == (1, 2)


def test_Piece_set_position_invalid():
    piece = Piece("wk", (1, 2))
    with raises(ValueError):
        piece.set_position((-1, 2))


def test_Piece_check_if_position_valid():
    piece = Piece("wk", (1, 2))
    assert piece.check_if_position_is_valid((0, 0)) is True
    assert piece.check_if_position_is_valid((2, 6)) is True
    assert piece.check_if_position_is_valid((7, 7)) is True
    assert piece.check_if_position_is_valid((0, 7)) is True
    assert piece.check_if_position_is_valid((7, 0)) is True
    assert piece.check_if_position_is_valid((-1, 0)) is False
    assert piece.check_if_position_is_valid((0, -1)) is False
    assert piece.check_if_position_is_valid((8, 0)) is False
    assert piece.check_if_position_is_valid((0, 8)) is False
    assert piece.check_if_position_is_valid((8, 8)) is False
    assert piece.check_if_position_is_valid((-1, -1)) is False


def test_Piece_str():
    piece = Piece("wk", (1, 2))
    assert str(piece) == "wk"

# GameState Tests


def test_GameState_initialization():
    game = GameState()
    assert game.board[0][0].name == "br"
    assert game.board[3][1] is None


def test_GameState_board_initialization():
    game = GameState()
    assert game.initialize_board()[7][1].name == "wh"
    assert game.initialize_board()[5][5] is None
    assert game.initialize_board()[0][1].name == "bh"


def test_GameState_can_mate():
    game = GameState()
    assert game.can_player_mate() is True
    assert game.can_opponent_mate() is True
    game.plr_black.pieces = [Piece("bk", (0, 0)), Piece("bh", (0, 1))]
    game.plr_white.pieces = [Piece("wk", (5, 0)), Piece("wb", (5, 1))]
    assert game.can_player_mate() is False
    assert game.can_opponent_mate() is False


def test_GameState_move_piece():
    game = GameState()
    assert game.pos_to_piece((0, 0)) is not None
    assert game.pos_to_piece((5, 0)) is None
    game.move_piece(game.pos_to_piece((0, 0)), (5, 0))
    assert game.pos_to_piece((0, 0)) is None
    assert game.pos_to_piece((5, 0)) is not None


def test_GameState_duplicate_board():
    game = GameState()
    assert game.print_board(game.board) == game.print_board(game.duplicate_board())


def test_GameState_pos_to_piece():
    game = GameState()
    assert game.pos_to_piece((0, 0)).name == "br"
    assert game.pos_to_piece((7, 0)).name == "wr"
    assert game.pos_to_piece((5, 5)) is None
    assert game.pos_to_piece((0, 5)).name == "bb"
    assert game.pos_to_piece((7, 5)).name == "wb"


def test_GameState_remove_piece():
    game = GameState()
    assert game.pos_to_piece((0, 0)) is not None
    game.remove_a_piece((0, 0))
    assert game.pos_to_piece((0, 0)) is None


def test_GameState_is_current_player_piece():
    game = GameState()
    assert game.is_current_player_piece((7, 0)) is True
    assert game.is_current_player_piece((0, 0)) is False


def test_GameState_find_kings():
    game = GameState()
    assert game.find_kings() == ((7, 4), (0, 4))


def test_GameState_find_all_pieces_of_color():
    game = GameState()
    assert len(game.find_all_pieces_of_color("w")) == 16
    assert len(game.find_all_pieces_of_color("b")) == 16


def test_GameState_find_all_moves():
    game = GameState()
    assert len(game.find_all_player_moves()) == len(game.find_all_opponent_moves()) == 20


def test_GameState_check_if_in_check():
    game = GameState()
    assert game.check_if_player_in_check() is False
    assert game.check_if_opponent_in_check() is False
    game.move_piece(game.pos_to_piece((7, 4)), (2, 4))
    assert game.check_if_opponent_in_check() is True
    game.move_piece(game.pos_to_piece((0, 4)), (5, 4))
    assert game.check_if_player_in_check() is True


def test_GameState_simulate_move_is_legal():
    game = GameState()
    assert game.simulate_move_is_legal(Player("w", []), game.pos_to_piece((7, 4)), (2, 4)) is False
    assert game.simulate_move_is_legal(Player("w", []), game.pos_to_piece((7, 4)), (5, 4)) is True


def test_GameState_check_if_valid_position():
    game = GameState()
    assert game.check_if_valid_position((0, 0)) is True
    assert game.check_if_valid_position((2, 6)) is True
    assert game.check_if_valid_position((7, 7)) is True
    assert game.check_if_valid_position((0, 7)) is True
    assert game.check_if_valid_position((7, 0)) is True
    assert game.check_if_valid_position((-1, 0)) is False
    assert game.check_if_valid_position((0, -1)) is False
    assert game.check_if_valid_position((8, 0)) is False
    assert game.check_if_valid_position((0, 8)) is False
    assert game.check_if_valid_position((8, 8)) is False
    assert game.check_if_valid_position((-1, -1)) is False


def test_GameState_piece_valid_tiles():
    game = GameState()
    game.board[3][3] = Piece("wr", (3, 3))
    assert len(game.piece_valid_tiles(Piece("wr", (3, 3)))) == 11
    assert len(game.piece_valid_tiles(Piece("wh", (3, 3)))) == 8
    assert len(game.piece_valid_tiles(Piece("wb", (3, 3)))) == 8
    assert len(game.piece_valid_tiles(Piece("wq", (3, 3)))) == 19
    assert len(game.piece_valid_tiles(Piece("wk", (3, 3)))) == 8
    assert len(game.piece_valid_tiles(Piece("wp", (3, 3)))) == 1

# Player Tests


def test_Player_initialization_valid():
    plr = Player("w", [i for i in range(16)])
    assert plr.color == "w"
    assert len(plr.pieces) == 16


def test_Player_initialization_invalid():
    with raises(ValueError):
        Player("asd", [i for i in range(16)])
    with raises(ValueError):
        Player("", [i for i in range(2)])


def test_Player_get_score():
    game = GameState()
    plr = Player("w", game.find_all_pieces_of_color("w"))
    assert plr.get_score() == 39

# MoveTracker Tests


def test_MoveTracker_initialization():
    tracker = MovesTracker()
    assert len(tracker.move_record) == 0


def test_MoveTracker_record_move():
    tracker = MovesTracker()
    tracker.record_move(Piece("wk", (0, 0)), (1, 0), "w")
    assert len(tracker.move_record) == 1
    assert tracker.move_record[0]["w"] == "A8->A7"


def test_MoveTracker_pos_to_string():
    tracker = MovesTracker()
    assert tracker.pos_to_string((0, 0)) == "A8"
    assert tracker.pos_to_string((0, 7)) == "H8"
    assert tracker.pos_to_string((7, 0)) == "A1"
    assert tracker.pos_to_string((7, 7)) == "H1"

# Display Tests


def test_Display_initialization():
    screen = pygame.display.set_mode((900, 900))
    colors = ("white", "gray")
    game = GameManager(screen, 900, colors)
    display = Display(screen, 900, game)
    assert display.window == screen
    assert display.board_size == 900
    assert display.game_manager == game

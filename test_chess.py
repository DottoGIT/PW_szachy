from gameManager import GameManager
from piece import Piece
from gameState import GameState
from player import Player
from pytest import raises
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

# GameState Tests


def test_GameState_initialization():
    game_state = GameState()
    assert game_state.board[0][0].name == "br"
    assert game_state.board[3][1] is None

def test_GameManager_find_pieces_of_color():
    game = GameState()
    assert len(game.find_all_pieces_of_color("w")) == 16
    assert len(game.find_all_pieces_of_color("b")) == 16

# Player Tests


def test_Player_initialization_valid():
    plr = Player("w", [i for i in range(16)])
    assert plr.color == "w"
    assert plr.pieces[2] == 2
    assert plr.score == 0


def test_Player_initialization_invalid():
    with raises(ValueError):
        Player("asd", [i for i in range(16)])
    with raises(ValueError):
        Player("w", [i for i in range(2)])

from gameManager import GameManager
from piece import Piece
from gameState import GameState
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

# Piece Tests


def test_Piece_initialization_valid():
    piece = Piece("bk")
    assert piece.name == "bk"


def test_Piece_initialization_invalid():
    with raises(ValueError):
        Piece("")

# GameState Tests


def test_GameState_initialization():
    game_state = GameState()
    assert game_state.board[0][0].name == "br"
    assert game_state.board[3][1] is None

"""
This file initializes main window and launches the game
"""

import pygame
from gameManager import GameManager

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
WINDOW_NAME = "Chess"
TILE_COLORS = ("white", "gray")
BOARD_SIZE = 900


def main():
    # Window initialization
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)

    game = GameManager(screen, BOARD_SIZE, TILE_COLORS)
    # Main Loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        game.update(events)
        pygame.display.update()


if __name__ == "__main__":
    main()

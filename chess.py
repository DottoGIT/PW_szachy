"""
This file initializes window and starts game loop
"""

import pygame
from gameManager import GameManager

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WINDOW_NAME = "Chess"
TILE_COLORS = ("white", "gray")
BOARD_SIZE = 900


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)
    game = GameManager(screen, BOARD_SIZE, TILE_COLORS)
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

import pygame

from iris_python_code.py_visual.const.screen_constants import *
from iris_python_code.py_visual.draw_board import *


# The 'Board' class provides a graphical representation of the state of the game board. 
# It allows for visual updates in response to game state changes and handles user interactions or inputs 
# related to the board itself.
class Board:
    def __init__(self, state):
        self.rect = pygame.Rect(0, 0, BOARD_COMPONENT_SIDE, BOARD_COMPONENT_SIDE)
        self.state = state

    def update_state(self, new_state):
        self.state = new_state

    def draw(self, screen):
        draw_board(screen, self.state)

    def handle_input(self, event_pos):
        pass
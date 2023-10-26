import pygame

from iris_python_code.py_visual.const.screen_constants import *
from iris_python_code.py_visual.utils import draw_text

# The 'Victory' class represents the interface component when a player is victorious.
class Victory:
    def __init__(self, state):
        self.rect = pygame.Rect(BOARD_COMPONENT_SIDE, 0, SCREEN_WIDTH, PLAY_COMPONENT_HEIGHT)
        self.state = state

    def update_state(self, new_state):
        self.state = new_state
        self.is_clicked = False

    def draw(self, screen):
        if not self.state.yellow_is_playing:
            draw_text(screen, 
                "Yellow win",
                SCREEN_HEIGHT, 
                20, 
                LIGHT_YELLOW
            )
        else:
            draw_text(screen, 
                "Red win", 
                SCREEN_HEIGHT, 
                20, 
                RED
            )

    def handle_input(self, event_pos):
        pass
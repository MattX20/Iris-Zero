import pygame

from iris_python_code.py_visual.const.screen_constants import *
from iris_python_code.py_visual.utils import draw_button, draw_text
from iris_python_code.py_visual.actions import ActionType

# The 'NoMove' class represents the interface component when there is no available move for the current player.
class NoMove:
    def __init__(self, state):
        self.rect = pygame.Rect(BOARD_COMPONENT_SIDE, 0, SCREEN_WIDTH, PLAY_COMPONENT_HEIGHT)
        self.button = "No legal move available"
        self.button_rect = pygame.Rect(
            BOARD_COMPONENT_SIDE + PLAY_COMPONENT_WIDTH / 2 - BUTTON_WIDTH / 2, 
            PLAY_COMPONENT_HEIGHT / 2 - BUTTON_HEIGHT / 2, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )
        self.state = state

    def update_state(self, new_state):
        self.state = new_state
        self.is_clicked = False

    def draw(self, screen):
        draw_button(screen, self.button_rect, DARK_SLATE_GREY, RED, self.button, WHITE)

        if self.state.yellow_is_playing:
            draw_text(screen, 
                "Yellow",
                SCREEN_HEIGHT, 
                20, 
                LIGHT_YELLOW
            )
        else:
            draw_text(screen, 
                "Red", 
                SCREEN_HEIGHT, 
                20, 
                RED
            )

    def handle_input(self, event_pos):
        if self.button_rect.collidepoint(event_pos) :
            self.is_clicked=True
            return (ActionType.MOVE, (-1, -1))
import pygame

from iris_python_code.py_visual.const.screen_constants import *
from iris_python_code.py_visual.utils import draw_button
from iris_python_code.py_visual.actions import ActionType

# The 'GoBack' class represents the interface component to use the go back button.
class GoBack:
    def __init__(self):
        self.rect = pygame.Rect(0, BOARD_COMPONENT_SIDE, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.button = "Go back"
        self.button_rect = pygame.Rect(
            SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 
            BOARD_COMPONENT_SIDE + GO_BACK_COMPONENT_HEIGHT / 2 - BUTTON_HEIGHT / 2, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )

    def update_state(self, new_state):
        pass

    def draw(self, screen):
        draw_button(screen, self.button_rect, DARK_SLATE_GREY, RED, self.button, WHITE)

    def handle_input(self, event_pos):
        if self.button_rect.collidepoint(event_pos) :
            self.is_clicked=True
            return (ActionType.GOBACK, None)
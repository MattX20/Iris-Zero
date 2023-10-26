import pygame

from iris_python_code.py_visual.const.screen_constants import *
from iris_python_code.py_visual.utils import draw_button, draw_text
from iris_python_code.py_visual.actions import ActionType

# The 'Bot' class represents the interface component to interact with the bot's actions in the game.
class Bot:
    def __init__(self, state, dict_param):
        self.rect = pygame.Rect(BOARD_COMPONENT_SIDE, 0, SCREEN_WIDTH, PLAY_COMPONENT_HEIGHT)
        self.button = "Next move"
        self.button_rect = pygame.Rect(
            BOARD_COMPONENT_SIDE + PLAY_COMPONENT_WIDTH / 2 - BUTTON_WIDTH / 2, 
            PLAY_COMPONENT_HEIGHT / 2 - BUTTON_HEIGHT / 2, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )
        self.state = state
        self.is_clicked = False
        self.dict_param = dict_param

    def update_state(self, new_state):
        self.state = new_state
        self.is_clicked = False

    def draw(self, screen):
        draw_button(screen, self.button_rect, DARK_SLATE_GREY, RED, self.button, WHITE, self.is_clicked)

        if self.state.yellow_is_playing:
            draw_text(screen, 
                "Yellow bot move",
                SCREEN_HEIGHT, 
                20, 
                LIGHT_YELLOW
            )
        else:
            draw_text(screen, 
                "Red bot move", 
                SCREEN_HEIGHT, 
                20, 
                RED
            )
        
        if self.is_clicked:
            draw_text(screen, 
                "Computing...",
                SCREEN_HEIGHT,
                PLAY_COMPONENT_HEIGHT / 2 + BUTTON_HEIGHT,
                WHITE
            )

    def handle_input(self, event_pos):
        if not self.is_clicked :
            if self.button_rect.collidepoint(event_pos) :
                self.is_clicked=True
                return (ActionType.BOT_PLAY, self.dict_param)
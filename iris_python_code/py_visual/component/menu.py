import pygame

from iris_python_code.py_visual.const.screen_constants import *
from iris_python_code.py_visual.utils import draw_button, draw_text
from iris_python_code.py_visual.actions import ActionType

# The 'Menu' class represents the interface component to choose the different options for the game.
class Menu:
    def __init__(self, yellow_is_choosing, model_path):

        self.button_player = ["Random", "MinMax", "MCTS", "IrisZero", "Human"]

        self.button_player_rect = [pygame.Rect(
            SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 
            SCREEN_HEIGHT / 3 + k * (10 + BUTTON_HEIGHT), 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        ) for k in range(len(self.button_player))]

        self.button_player_minmax = [str(i) for i in BOT_CONST["minmax"]] 
        self.button_player_minmax_rect = [ 
            [pygame.Rect(
                SCREEN_WIDTH / 2 - 2 * 70 + 5 + c * (70) , 
                100 + (k + 1) * 40, 
                60, 
                30 
            ) for k in range(min(10, len(self.button_player_minmax) - c * 10))]
            
            for c in range((len(self.button_player_minmax) % 10) + 1)
        ]
        self.button_player_minmax_rect = [item for sblst in self.button_player_minmax_rect for item in sblst]

        self.button_player_mcts = [str(i) for i in BOT_CONST["mcts"]] 
        self.button_player_mcts_rect = [ 
            [pygame.Rect(
                SCREEN_WIDTH / 2 - 2 * 70 + 5 + c * (70) , 
                100 + (k + 1) * 40, 
                60, 
                30 
            ) for k in range(min(10, len(self.button_player_mcts) - c * 10))]
            
            for c in range((len(self.button_player_mcts) % 10) + 1)
        ]
        self.button_player_mcts_rect = [item for sblst in self.button_player_mcts_rect for item in sblst]

        self.button_player_alphazero = [str(i) for i in BOT_CONST["alphazero"]] 
        self.button_player_alphazero_rect = [ 
            [pygame.Rect(
                SCREEN_WIDTH / 2 - 2 * 70 + 5 + c * (70) , 
                100 + (k + 1) * 40, 
                60, 
                30 
            ) for k in range(min(10, len(self.button_player_alphazero) - c * 10))]
            
            for c in range((len(self.button_player_alphazero) % 10) + 1)
        ]
        self.button_player_alphazero_rect = [item for sblst in self.button_player_alphazero_rect for item in sblst]

        self.chosen_player = None
        self.yellow_is_choosing = yellow_is_choosing
        self.model_path = model_path


    def draw(self, screen):
        
        if self.chosen_player is None :
            for i in range(len(self.button_player)) :
                draw_button(screen, self.button_player_rect[i], DARK_SLATE_GREY, RED, self.button_player[i], WHITE)
        else :
            if self.chosen_player == 1 :
                for i in range(len(self.button_player_minmax_rect)) :
                    draw_button(screen, self.button_player_minmax_rect[i], DARK_SLATE_GREY, RED, self.button_player_minmax[i], WHITE)
            elif self.chosen_player == 2 :
                for i in range(len(self.button_player_mcts_rect)) :
                    draw_button(screen, self.button_player_mcts_rect[i], DARK_SLATE_GREY, RED, self.button_player_mcts[i], WHITE)
            elif self.chosen_player == 3 :
                for i in range(len(self.button_player_alphazero_rect)) :
                    draw_button(screen, self.button_player_alphazero_rect[i], DARK_SLATE_GREY, RED, self.button_player_alphazero[i], WHITE)
            
        
        if self.yellow_is_choosing:
            draw_text(screen, 
                "Yellow player choice",
                SCREEN_HEIGHT, 
                20, 
                LIGHT_YELLOW
            )
        else:
            draw_text(screen, 
                "Red player choice", 
                SCREEN_HEIGHT, 
                20, 
                RED
            )

    def handle_input(self, event_pos):
        if self.chosen_player is None :
            for i in range(len(self.button_player_rect)) :
                if self.button_player_rect[i].collidepoint(event_pos) :
                    self.chosen_player = i
                    if i == 0 :
                        return (ActionType.SELECT_BOT, {"type" : 0})
                    if i == 4 :
                        return (ActionType.SELECT_HUMAN, None)
                    return
        elif self.chosen_player is not None :
            if self.chosen_player == 1 :
                for i in range(len(self.button_player_minmax_rect)) :
                    if self.button_player_minmax_rect[i].collidepoint(event_pos) :
                        return (ActionType.BOT_PLAY, {"type" : 1, "depth" : BOT_CONST["minmax"][i]})
            elif self.chosen_player == 2 :
                for i in range(len(self.button_player_mcts_rect)) :
                    if self.button_player_mcts_rect[i].collidepoint(event_pos) :
                        return (ActionType.BOT_PLAY, {"type" : 2, "nb_sim" : BOT_CONST["mcts"][i]})
            elif self.chosen_player == 3 :
                for i in range(len(self.button_player_alphazero_rect)) :
                    if self.button_player_alphazero_rect[i].collidepoint(event_pos) :
                        return (ActionType.BOT_PLAY, {"type" : 3, "nb_sim" : BOT_CONST["alphazero"][i], "model_path" : self.model_path})
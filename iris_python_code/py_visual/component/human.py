import pygame

from iris_python_code.py_visual.const.screen_constants import *
from iris_python_code.py_visual.utils import draw_button, draw_text
from iris_python_code.py_visual.actions import ActionType

from iris_python_code.py_game.const.board_constants import NB_REAL_NODE

# The 'Human' class represents the interface component to interact directly with the game.
class Human:
    def __init__(self, state, model_path):
        self.rect = pygame.Rect(BOARD_COMPONENT_SIDE, 0, SCREEN_WIDTH, PLAY_COMPONENT_HEIGHT)
        
        self.button_move = ["Player pawn", "Black pawn", "White pawn", "Orange pawn"]
        self.button_move_rect = [pygame.Rect(
            BOARD_COMPONENT_SIDE + PLAY_COMPONENT_WIDTH / 2 - BUTTON_WIDTH / 2, 
            60 + k * (10 + BUTTON_HEIGHT), 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        ) for k in range(len(self.button_move))]

        self.button_bot = ["Random", "MinMax", "MCTS", "IrisZero"]

        self.button_bot_rect = [pygame.Rect(
            BOARD_COMPONENT_SIDE + PLAY_COMPONENT_WIDTH / 2 - BUTTON_WIDTH / 2, 
            160 + len(self.button_move) * (10 + BUTTON_HEIGHT) + k * (10 + BUTTON_HEIGHT), 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        ) for k in range(len(self.button_bot))]

        self.button_move_tile = [str(k) for k in range(NB_REAL_NODE)]
        self.button_move_tile_rect = [ pygame.Rect(
                BOARD_COMPONENT_SIDE + 3 / 2 * 70 , 
                100, 
                60, 
                30 
            )] + [
            pygame.Rect(
                BOARD_COMPONENT_SIDE + c * (70) , 
                100 + (k + 1) * 40, 
                60, 
                30 
            )
            for c in range(4)
            for k in range(5)
        ]

        self.button_bot_minmax = [str(i) for i in BOT_CONST["minmax"]] 
        self.button_bot_minmax_rect = [ 
            [pygame.Rect(
                BOARD_COMPONENT_SIDE + c * (70) , 
                100 + (k + 1) * 40, 
                60, 
                30 
            ) for k in range(min(10, len(self.button_bot_minmax) - c * 10))]
            
            for c in range((len(self.button_bot_minmax) % 10) + 1)
        ]
        self.button_bot_minmax_rect = [item for sblst in self.button_bot_minmax_rect for item in sblst]
        self.button_bot_minmax_clicked = [False for _ in range(len(self.button_bot_minmax))]

        self.button_bot_mcts = [str(i) for i in BOT_CONST["mcts"]] 
        self.button_bot_mcts_rect = [ 
            [pygame.Rect(
                BOARD_COMPONENT_SIDE + c * (70) , 
                100 + (k + 1) * 40, 
                60, 
                30 
            ) for k in range(min(10, len(self.button_bot_mcts) - c * 10))]
            
            for c in range((len(self.button_bot_mcts) % 10) + 1)
        ]
        self.button_bot_mcts_rect = [item for sblst in self.button_bot_mcts_rect for item in sblst]
        self.button_bot_mcts_clicked = [False for _ in range(len(self.button_bot_mcts))]

        self.button_bot_alphazero = [str(i) for i in BOT_CONST["alphazero"]] 
        self.button_bot_alphazero_rect = [ 
            [pygame.Rect(
                BOARD_COMPONENT_SIDE + c * (70) , 
                100 + (k + 1) * 40, 
                60, 
                30 
            ) for k in range(min(10, len(self.button_bot_alphazero) - c * 10))]
            
            for c in range((len(self.button_bot_alphazero) % 10) + 1)
        ]
        self.button_bot_alphazero_rect = [item for sblst in self.button_bot_alphazero_rect for item in sblst]
        self.button_bot_alphazero_clicked = [False for _ in range(len(self.button_bot_alphazero))]

        self.chosen_pawn = None
        self.chosen_bot = None
        self.model_path = model_path
        self.state = state

    def update_state(self, new_state):
        self.state = new_state
        self.chosen_pawn = None
        self.chosen_bot = None

        for i in range(len(self.button_bot_minmax_clicked)) :
            self.button_bot_minmax_clicked[i] = False
        
        for i in range(len(self.button_bot_mcts_clicked)) :
            self.button_bot_mcts_clicked[i] = False

        for i in range(len(self.button_bot_alphazero_clicked)) :
            self.button_bot_alphazero_clicked[i] = False

    def draw(self, screen):
        
        if self.chosen_pawn is None and self.chosen_bot is None :
            for i in range(len(self.button_move)) :
                draw_button(screen, self.button_move_rect[i], DARK_SLATE_GREY, RED, self.button_move[i], WHITE)

            for i in range(len(self.button_bot)) :
                draw_button(screen, self.button_bot_rect[i], DARK_SLATE_GREY, RED, self.button_bot[i], WHITE)
        
        if self.chosen_pawn is not None :
            for i in range(len(self.button_move_tile_rect)) :
                draw_button(screen, self.button_move_tile_rect[i], DARK_SLATE_GREY, RED, self.button_move_tile[i], WHITE)

        if self.chosen_bot is not None :
            if self.chosen_bot == 1 :
                for i in range(len(self.button_bot_minmax_rect)) :
                    draw_button(screen, self.button_bot_minmax_rect[i], DARK_SLATE_GREY, RED, self.button_bot_minmax[i], WHITE, self.button_bot_minmax_clicked[i])
            elif self.chosen_bot == 2 :
                for i in range(len(self.button_bot_mcts_rect)) :
                    draw_button(screen, self.button_bot_mcts_rect[i], DARK_SLATE_GREY, RED, self.button_bot_mcts[i], WHITE, self.button_bot_mcts_clicked[i])
            elif self.chosen_bot == 3 :
                for i in range(len(self.button_bot_alphazero_rect)) :
                    draw_button(screen, self.button_bot_alphazero_rect[i], DARK_SLATE_GREY, RED, self.button_bot_alphazero[i], WHITE, self.button_bot_alphazero_clicked[i])
            
        
        if self.state.yellow_is_playing:
            draw_text(screen, 
                "Yellow player move",
                SCREEN_HEIGHT, 
                20, 
                LIGHT_YELLOW
            )
        else:
            draw_text(screen, 
                "Red player move", 
                SCREEN_HEIGHT, 
                20, 
                RED
            )

        if any(self.button_bot_minmax_clicked) or any(self.button_bot_mcts_clicked) or any(self.button_bot_alphazero_clicked):
            draw_text(screen, 
                "Computing...",
                SCREEN_HEIGHT,
                100 + 11 * 40,
                WHITE
            )

    def handle_input(self, event_pos):
        if self.chosen_pawn is None and self.chosen_bot is None :
            for i in range(len(self.button_move_rect)) :
                if self.button_move_rect[i].collidepoint(event_pos) :
                    self.chosen_pawn = i
                    return
            
            for i in range(len(self.button_bot_rect)) :
                if self.button_bot_rect[i].collidepoint(event_pos) :
                    self.chosen_bot = i
                    if i == 0 :
                        return (ActionType.BOT_PLAY, {"type" : 0})
                    return
        elif self.chosen_pawn is not None :
            for i in range(len(self.button_move_tile_rect)) :
                if self.button_move_tile_rect[i].collidepoint(event_pos) :
                    if self.state.is_valid_move(self.chosen_pawn, i):
                        return (ActionType.MOVE, (self.chosen_pawn, i))
                    else :
                        self.chosen_pawn = None
        elif self.chosen_bot is not None :
            if self.chosen_bot == 1 :
                for i in range(len(self.button_bot_minmax_rect)) :
                    if self.button_bot_minmax_rect[i].collidepoint(event_pos) :
                        self.button_bot_minmax_clicked[i] = True
                        return (ActionType.BOT_PLAY, {"type" : 1, "depth" : BOT_CONST["minmax"][i]})
            elif self.chosen_bot == 2 :
                for i in range(len(self.button_bot_mcts_rect)) :
                    if self.button_bot_mcts_rect[i].collidepoint(event_pos) :
                        self.button_bot_mcts_clicked[i] = True
                        return (ActionType.BOT_PLAY, {"type" : 2, "nb_sim" : BOT_CONST["mcts"][i]})
            elif self.chosen_bot == 3 :
                for i in range(len(self.button_bot_alphazero_rect)) :
                    if self.button_bot_alphazero_rect[i].collidepoint(event_pos) :
                        self.button_bot_alphazero_clicked[i] = True
                        return (ActionType.BOT_PLAY, {"type" : 3, "nb_sim" : BOT_CONST["alphazero"][i], "model_path" : self.model_path})

                
            
            
            

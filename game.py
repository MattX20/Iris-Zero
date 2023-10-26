import sys
import pygame
import torch
import concurrent.futures

from pygame.locals import *

from time import perf_counter as clock
from time import sleep

from iris_python_code.py_visual.const.screen_constants import *
from iris_python_code.py_visual.component.board import Board
from iris_python_code.py_visual.component.go_back import GoBack
from iris_python_code.py_visual.component.bot import Bot
from iris_python_code.py_visual.component.no_move import NoMove
from iris_python_code.py_visual.component.victory import Victory
from iris_python_code.py_visual.component.human import Human
from iris_python_code.py_visual.component.menu import Menu
from iris_python_code.py_visual.actions import ActionType

from iris_python_code.py_game.game.game_state import GameState

from iris_python_code.py_utils.utils import tuple_to_game_state


# pygame screen initialisation.
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Iris")

# path for the IrisZero model.
MODEL_PATH = "models/script/iris_weights.pt"

def player_selector(state_tuple, type, depth=1, thinking_time=1, nb_sim=1000, model_path=""):
    """
    A function taking a tuple representing a game state and a type of bot (integer between 0 and 5) along with specific parameters,
    and returns the action type move and the move played by the bot on this game state.
    """
    import iris_cpp_library.build.py_iris as py_iris
    import iris_python_code.py_visual.actions as action

    if type == 0:
        return (action.ActionType.MOVE, py_iris.random_bot(*state_tuple))
    elif type == 1:
        return (action.ActionType.MOVE, py_iris.minmax_bot(*state_tuple, depth))
    elif type == 2:
        return (action.ActionType.MOVE, py_iris.mcts_bot_sim(*state_tuple, nb_sim))
    elif type == 3:
        return (action.ActionType.MOVE, py_iris.iris_zero_bot_sim(*state_tuple, nb_sim, model_path))
    elif type == 4:
        return (action.ActionType.MOVE, py_iris.mcts_bot_time(*state_tuple, thinking_time))
    elif type == 5:
        return (action.ActionType.MOVE, py_iris.iris_zero_bot_time(*state_tuple, thinking_time, model_path))

################################################################################################################################
################################################################################################################################


def main():
    # Random initialization of the board.
    state = GameState() 

    # Flag indicating if yellow is currently choosing his options for the game.
    yellow_is_choosing = True

    # Menu component initialisation.
    menu = Menu(yellow_is_choosing, MODEL_PATH)

    # Placeholder for the yellow and red components.
    yellow_screen = None
    red_screen = None 

    # Option selection.
    while True:
        sleep(0.1)
        action = None 

        # This loop listen for user actions.
        # Actions can be of the following types : SELECT_HUMAN or SELECT_BOT.
        # SELECT_HUMAN : the choosing color is a human.
        # SELECT_BOT : the choosing color is a bot.
        # This is made to select the apropriate visual components.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()        
            elif event.type == MOUSEBUTTONDOWN:
                action = menu.handle_input(event.pos)


        if action is not None :
            action_type, value = action

            if yellow_is_choosing :
                if action_type == ActionType.SELECT_HUMAN :
                    yellow_screen = Human(state, MODEL_PATH)
                else :
                    yellow_screen = Bot(state, value)
                
                yellow_is_choosing = False
                menu = Menu(yellow_is_choosing, MODEL_PATH)
            else :
                if action_type == ActionType.SELECT_HUMAN :
                    red_screen = Human(state, MODEL_PATH)
                else :
                    red_screen = Bot(state, value)
                
                break
                
        screen.fill(BLACK)
        menu.draw(screen)
        pygame.display.flip()
    
    # List to store the game states throughout the game, allowing to go back.
    states = [state.to_tuple()]
    bool_exist_valid_move = state.exists_move()

    # Instanciate the required components.
    no_move_screen = NoMove(state)
    victory_screen = Victory(state)

    components = [Board(state), GoBack(), yellow_screen]
    if not bool_exist_valid_move :
        components[-1] = no_move_screen

    # Instantiate a ProcessPoolExecutor, to launch the bot computations on an other
    # process.
    executor = concurrent.futures.ProcessPoolExecutor()

    # Place holder for the current turn futur.
    futur = None

    # Play loop.
    while True:
        sleep(0.1)
        action = None 

        # Listen for actions.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                executor.shutdown(wait=False)
                sys.exit()        
            elif futur is None and event.type == MOUSEBUTTONDOWN:
                for component in components:
                    if component.rect.collidepoint(event.pos):
                        action = component.handle_input(event.pos)
        
        # Listen for actions, on the bot side.
        if futur is not None and futur.done() :
            action = futur.result()
            futur = None

        # If an action is made.
        # Actions can be of the following types:
        # MOVE : the current player choosed a move to play.
        # BOT_PLAY : the current player is a bot or human used the bot
        # option on his interface. 
        # GO_BACK : go back to the previous position.
        # Along theses actions, the chosen parameters (move description or bot description).

        if action is not None :
            action_type, value = action

            # The action is a MOVE, its value is a tuple describing the move.
            if action_type == ActionType.MOVE :

                # (-1, -1): there is no valid move for the current player.
                # Apply the no valid move policy.
                if value == (-1, -1) and not bool_exist_valid_move :
                    state.no_valid_move()
                    states.append(state.to_tuple())

                    bool_exist_valid_move = state.exists_move()

                    if not bool_exist_valid_move :
                        components[-1] = no_move_screen
                    elif state.yellow_is_playing :
                        components[-1] = yellow_screen
                    else :
                        components[-1] = red_screen

                    nw_state = tuple_to_game_state(states[-1])
                    for component in components :
                        component.update_state(nw_state)

                # There is a move available for the current player.
                # Apply the move and checks if it is a winning move.
                elif value != (-1, 1) and bool_exist_valid_move and state.is_valid_move(*value) :
                    is_winner = state.apply_move(*value)
                    states.append(state.to_tuple())
                    
                    if is_winner :
                        components[-1] = victory_screen
                    else :
                        bool_exist_valid_move = state.exists_move()

                        if not bool_exist_valid_move :
                            components[-1] = no_move_screen
                        elif state.yellow_is_playing :
                            components[-1] = yellow_screen
                        else :
                            components[-1] = red_screen

                    nw_state = tuple_to_game_state(states[-1])
                    for component in components :
                        component.update_state(nw_state)
                
                # An illegal action has been made.
                else :
                    pygame.quit()
                    executor.shutdown(wait=False)
                    print(
                        f"Illegal move {value[0]}, {value[1]}")
                    print(state.to_tuple())
                    sys.exit()
            
            # The action is BOT_PLAY, submit to the executor the type of bot chosen and the current state.
            if action_type == ActionType.BOT_PLAY :
                futur = executor.submit(player_selector, state.to_tuple(), **value)

            # The action is GO_BACK, return to the previous move.
            if action_type == ActionType.GOBACK and len(states) > 1 :
                states.pop()
                state = tuple_to_game_state(states[-1])

                bool_exist_valid_move = state.exists_move()

                if not bool_exist_valid_move :
                    components[-1] = no_move_screen
                elif state.yellow_is_playing :
                    components[-1] = yellow_screen
                else :
                    components[-1] = red_screen

                for component in components :
                    component.update_state(state)

        
        screen.fill(BLACK)
        for component in components :
            component.draw(screen)
        pygame.display.flip()
    
    


if __name__ == "__main__":
    main()

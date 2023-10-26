import numpy as np
import torch
from iris_python_code.py_game.game.game_state import GameState
from iris_python_code.py_game.const.board_constants import NB_REAL_NODE, NB_FEATURES

# The NoValidMove class is an exception, being raised if a player (bot)
# played no valid move, even if there is one available.
class NoValidMove(Exception):
    def __init__(self, state):
        if state.yellow_is_playing:
            msg = (
                "Yellow said there is no legal move, but there is one\n"
                + ", ".join(map(str, state.to_tuple()))
                + "\n"
            )
        else:
            msg = (
                "Red said there is no legal move, but there is one\n"
                + ", ".join(map(str, state.to_tuple()))
                + "\n"
            )

        super().__init__(msg)

# The InvalidMove class is an exception, being raised if a player (bot)
# played an illegal move.
class InvalidMove(Exception):
    def __init__(self, state):
        if state.yellow_is_playing:
            msg = (
                "Yellow did an illegal move\n"
                + ", ".join(map(str, state.to_tuple()))
                + "\n"
            )
        else:
            msg = (
                "Red did an illegal move\n"
                + ", ".join(map(str, state.to_tuple()))
                + "\n"
            )

        super().__init__(msg)


def launch_game(yellow_bot, red_bot, initial_state, max_turn=100): 
    """ 
    Play a game with functions representing players, taking an initial gamestate and returns the output of the game:
    1: Yellow victory, -1: Red victory, 0: draw (if the number of turns is above a max_turn parameter) and the number of
    turns in the game.
    """
    state = initial_state
    current_turn = 1

    while current_turn <= max_turn:
        if state.yellow_is_playing:
            action = yellow_bot(*state.to_tuple())
            if action == (-1, -1):
                state.no_valid_move()
            else:
                victory = state.apply_move(*action)
                if victory:
                    return (1, current_turn)
        else:
            action = red_bot(*state.to_tuple())
            if action == (-1, -1):
                state.no_valid_move()
            else:
                victory = state.apply_move(*action)
                if victory:
                    return (-1, current_turn)
        current_turn += 1

    return (0, current_turn)


def launch_game_check(yellow_bot, red_bot, initial_state, max_turn=100):
    """ 
    Play a game with functions representing players, taking an initial gamestate and returns the output of the game:
    1: Yellow victory, -1: Red victory, 0: draw (if the number of turns is above a max_turn parameter) and the number of
    turns in the game.

    This function checks explicitely that all move played are legal, raises error if it is not the case.
    """
    state = initial_state
    current_turn = 1

    while current_turn <= max_turn:
        if state.yellow_is_playing:
            action = yellow_bot(*state.to_tuple())
            if action == (-1, -1) and state.exists_move():
                raise NoValidMove(state)
            elif action == (-1, -1):
                state.no_valid_move()
            elif state.is_valid_move(*action):
                victory = state.apply_move(*action)
                if victory:
                    return (1, current_turn)
            else:
                raise InvalidMove(state)
        else:
            action = red_bot(*state.to_tuple())
            if action == (-1, -1) and state.exists_move():
                raise NoValidMove(state)
            elif action == (-1, -1):
                state.no_valid_move()
            elif state.is_valid_move(*action):
                victory = state.apply_move(*action)
                if victory:
                    return (-1, current_turn)
            else:
                raise InvalidMove(state)

        current_turn += 1

    return (0, current_turn)


def game_state_to_tensor(state: GameState):
    """
     Transforms a game state into a tensor representation suitable for neural network processing.
    
    
     The resulting tensor is a NUMBER_REAL_NODES, NUMBER_ATRIBUTES tensor such that
     The five four columns are a one-hot encoding of the five pawns' locations. 
     The next five columns are indicative of the locations of the five different tile types, 
     with an assigned value of 1 indicating the presence of a tile of a specific type on a specific node, and 0 indicating its absence. 
     The next eight columns of the state representation array encode the consecutive usage of 
     both black and white pawns by the yellow and red players. Specifically, the first four columns are for the black pawn. 
     In these, the first column is filled with 1 if the yellow player used the black pawn in his last move. 
     Otherwise, it is filled with 0. Similarly, the second column is filled with 1 if the black pawn was used twice consecutively 
     by the yellow player in his last two moves, and 0 otherwise. The third and fourth columns use the same encoding, but represent 
     the red player's usage of the black pawn. 
     Following this, the other eight columns represent the consecutive usage of the white and the orange pawn, and use the same pattern 
     as the previous four columns. 
     The last column specifies the player's turn, filled with 0 if it is the yellow player's turn, and 1 if it is the red player's turn.
    
    """

    res = torch.zeros((NB_REAL_NODE, NB_FEATURES)) 

    res[state.yellow_position][0] = 1.0
    res[state.red_position][1] = 1.0
    res[state.black_position][2] = 1.0
    res[state.white_position][3] = 1.0
    res[state.orange_position][4] = 1.0

    for k in range(1, NB_REAL_NODE):
        pos = 1 << k
        yr = bool(state.yellow_colors & state.red_colors & pos)
        yb = bool(state.yellow_colors & state.black_colors & pos)
        yw = bool(state.yellow_colors & state.white_colors & pos)
        rb = bool(state.black_colors & state.red_colors & pos)
        rw = bool(state.white_colors & state.red_colors & pos)

        if yr:
            res[k][5] = 1.0
        elif yb:
            res[k][6] = 1.0
        elif yw:
            res[k][7] = 1.0
        elif rb:
            res[k][8] = 1.0
        elif rw:
            res[k][9] = 1.0

    if state.black_last_use:
        if state.black_count_consecutive_use == 1:
            for k in range(NB_REAL_NODE):
                res[k][10] = 1.0
        if state.black_count_consecutive_use == 2:
            for k in range(NB_REAL_NODE):
                res[k][11] = 1.0
    else:
        if state.black_count_consecutive_use == 1:
            for k in range(NB_REAL_NODE):
                res[k][12] = 1.0
        if state.black_count_consecutive_use == 2:
            for k in range(NB_REAL_NODE):
                res[k][13] = 1.0

    if state.white_last_use:
        if state.white_count_consecutive_use == 1:
            for k in range(NB_REAL_NODE):
                res[k][14] = 1.0
        if state.white_count_consecutive_use == 2:
            for k in range(NB_REAL_NODE):
                res[k][15] = 1.0
    else:
        if state.white_count_consecutive_use == 1:
            for k in range(NB_REAL_NODE):
                res[k][16] = 1.0
        if state.white_count_consecutive_use == 2:
            for k in range(NB_REAL_NODE):
                res[k][17] = 1.0
    
    if state.orange_last_use:
        if state.orange_count_consecutive_use == 1:
            for k in range(NB_REAL_NODE):
                res[k][18] = 1.0
        if state.orange_count_consecutive_use == 2:
            for k in range(NB_REAL_NODE):
                res[k][19] = 1.0
    else:
        if state.orange_count_consecutive_use == 1:
            for k in range(NB_REAL_NODE):
                res[k][20] = 1.0
        if state.orange_count_consecutive_use == 2:
            for k in range(NB_REAL_NODE):
                res[k][21] = 1.0

    if not state.yellow_is_playing:
        for k in range(NB_REAL_NODE):
            res[k][22] = 1.0

    return res


def tensor_to_game_state(state_tensor: torch.tensor):
    """
    This function takes a tensor representing a gamestate and returns the corresponding GameState.
    """
    state = GameState()

    state.yellow_is_playing = (state_tensor[0, -1] == 0.0).item()
    state.yellow_position = torch.argmax(state_tensor[:, 0]).item()
    state.red_position = torch.argmax(state_tensor[:, 1]).item()
    state.black_position = torch.argmax(state_tensor[:, 2]).item()
    state.white_position = torch.argmax(state_tensor[:, 3]).item()
    state.orange_position = torch.argmax(state_tensor[:, 4]).item()

    yellow_color = (
        torch.where(state_tensor[:, 5] == 1.0)[0].tolist()
        + torch.where(state_tensor[:, 6] == 1.0)[0].tolist()
        + torch.where(state_tensor[:, 7] == 1.0)[0].tolist()
    )
    red_color = (
        torch.where(state_tensor[:, 5] == 1.0)[0].tolist()
        + torch.where(state_tensor[:, 8] == 1.0)[0].tolist()
        + torch.where(state_tensor[:, 9] == 1.0)[0].tolist()
    )
    black_color = (
        torch.where(state_tensor[:, 6] == 1.0)[0].tolist()
        + torch.where(state_tensor[:, 8] == 1.0)[0].tolist()
    )
    white_color = (
        torch.where(state_tensor[:, 7] == 1.0)[0].tolist()
        + torch.where(state_tensor[:, 9] == 1.0)[0].tolist()
    )

    state.yellow_colors = np.sum([1 << k for k in yellow_color])
    state.red_colors = np.sum([1 << k for k in red_color])
    state.black_colors = np.sum([1 << k for k in black_color])
    state.white_colors = np.sum([1 << k for k in white_color])

    state.black_last_use = (
        state_tensor[0, 10] > 0.0 or state_tensor[0, 11] > 0.0
    ).item()
    state.white_last_use = (
        state_tensor[0, 14] > 0.0 or state_tensor[0, 15] > 0.0
    ).item()
    state.orange_last_use = (
        state_tensor[0, 18] > 0.0 or state_tensor[0, 19] > 0.0
    ).item()

    if (state_tensor[0, 10] > 0.0 or state_tensor[0, 12]).item() > 0.0:
        state.black_count_consecutive_use = 1
    if (state_tensor[0, 11] > 0.0 or state_tensor[0, 13]).item() > 0.0:
        state.black_count_consecutive_use = 2

    if (state_tensor[0, 14] > 0.0 or state_tensor[0, 16]).item() > 0.0:
        state.white_count_consecutive_use = 1
    if (state_tensor[0, 15] > 0.0 or state_tensor[0, 17]).item() > 0.0:
        state.white_count_consecutive_use = 2

    if (state_tensor[0, 18] > 0.0 or state_tensor[0, 20]).item() > 0.0:
        state.orange_count_consecutive_use = 1
    if (state_tensor[0, 19] > 0.0 or state_tensor[0, 21]).item() > 0.0:
        state.orange_count_consecutive_use = 2

    return state


def tuple_to_game_state(t):
    """
    This function takes a tuple of all the parameters for a game state and return the corresponding GameState.
    """
    state = GameState()
    (
        state.yellow_is_playing,
        state.yellow_position,
        state.red_position,
        state.black_position,
        state.white_position,
        state.orange_position,
        state.yellow_colors,
        state.red_colors,
        state.black_colors,
        state.white_colors,
        state.black_last_use,
        state.white_last_use,
        state.orange_last_use,
        state.black_count_consecutive_use,
        state.white_count_consecutive_use,
        state.orange_count_consecutive_use
    ) = t

    return state

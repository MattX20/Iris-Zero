# Screen size constants.
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# Side size of the game board component.
BOARD_COMPONENT_SIDE = 800

# Size width and height for the play component (the one on which actions are proposed).
PLAY_COMPONENT_WIDTH = SCREEN_WIDTH - BOARD_COMPONENT_SIDE 
PLAY_COMPONENT_HEIGHT = BOARD_COMPONENT_SIDE

# Size width and height for the go back component (the one on which the 'go back' button is placed).
GO_BACK_COMPONENT_WIDTH = SCREEN_WIDTH
GO_BACK_COMPONENT_HEIGHT = SCREEN_HEIGHT - BOARD_COMPONENT_SIDE

# Color constants.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SLATE_GREY = (112, 128, 144)
DARK_SLATE_GREY = (47, 79, 79)
FOREST_GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
LIGHT_YELLOW = (255, 255, 51)
ORANGE = (255,165,0)

# Specifics board graph edges, to be printed in blue.
# Symply used to highlight the pentagones.
BLUE_LINK = (
    (1, 2), (1, 5), (2, 3), (3, 4), (4, 5),
    (6, 7), (6, 10), (7, 8), (8, 9), (9, 10),
    (11, 12), (11, 15), (12, 13), (13, 14), (14, 15)
)

# Radius of a node.
CIRCLE_RADIUS = 20

# Button size constants.
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 30

# Displayed possible parameters for the corresponding algorithms. Can be modified.
BOT_CONST = {
    # Depth for the minmax algorithm.
    "minmax" : [1, 2, 3, 4, 5, 6, 7, 8],
    
    # Number of simulations for the mcts algorithm.
    "mcts" : [100, 1000, 5000, 10000, 20000, 50000, 100000, 200000],

    # Number of simulations for the AlphaZero algorithm.
    "alphazero" : [100, 500, 1000, 2000, 3000, 4000, 5000, 10000]
}
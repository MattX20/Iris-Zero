import pygame

from math import cos, sin, pi, sqrt
from iris_python_code.py_visual.const.screen_constants import *
from iris_python_code.py_game.const.board_constants import *
from iris_python_code.py_visual.utils import draw_circle_with_number

# Various constants to localise board elements.
midx = BOARD_COMPONENT_SIDE / 2
midy = BOARD_COMPONENT_SIDE / 2 + CIRCLE_RADIUS
lx = (BOARD_COMPONENT_SIDE - 2 * CIRCLE_RADIUS) / 8
ly = (BOARD_COMPONENT_SIDE - 2 * CIRCLE_RADIUS) / 8

# Position of the nodes within the board component.
node_position = (

    # Central node.
    (midx, midy), # node 0

    # First pentagone
    (midx, ly + midy),  # node 1
    (-lx * sin(2 * pi / 5) + midx, ly * cos(2 * pi / 5) + midy),  # node 2
    (-lx * sin(pi / 5) + midx, -ly * cos(pi / 5) + midy),  # node 3
    (lx * sin(pi / 5) + midx, -ly * cos(pi / 5) + midy),  # node 4
    (lx * sin(2 * pi / 5) + midx, ly * cos(2 * pi / 5) + midy),  # node 5

    # Second pentagone.
    (-2 * lx * sin(pi / 5) + midx, 2 * ly * cos(pi / 5) + midy),  # node 6
    (-2 * lx * sin(2 * pi / 5) + midx, -2 * ly * cos(2 * pi / 5) + midy),  # node 7
    (midx, -2 * ly + midy),  # node 8
    (2 * lx * sin(2 * pi / 5) + midx, -2 * ly * cos(2 * pi / 5) + midy),  # node 9
    (2 * lx * sin(pi / 5) + midx, 2 * ly * cos(pi / 5) + midy),  # node 10
    
    # Third pentagone.
    (midx, 3 * ly + midy),  # node 11
    (-3 * lx * sin(2 * pi / 5) + midx, 3 * ly * cos(2 * pi / 5) + midy),  # node 12
    (-3 * lx * sin(pi / 5) + midx, -3 * ly * cos(pi / 5) + midy),  # node 13
    (3 * lx * sin(pi / 5) + midx, -3 * ly * cos(pi / 5) + midy),  # node 14
    (3 * lx * sin(2 * pi / 5) + midx, 3 * ly * cos(2 * pi / 5) + midy),  # node 15
    
    # Fourth pentagone.
    (-4 * lx * sin(pi / 5) + midx, 4 * ly * cos(pi / 5) + midy),  # node 16
    (-4 * lx * sin(2 * pi / 5) + midx, -4 * ly * cos(2 * pi / 5) + midy),  # node 17
    (midx, -4 * ly + midy),  # node 18
    (4 * lx * sin(2 * pi / 5) + midx, -4 * ly * cos(2 * pi / 5) + midy),  # node 19
    (4 * lx * sin(pi / 5) + midx, 4 * ly * cos(pi / 5) + midy),  # node 20
)


def draw_board(screen, state):
    """
    Function taking a pygame screen and a GameState.
    Prints the given state on the scree.
    """

    # Draw edges between nodes.
    for k in range(21):
        for v in NODE_NEIGHBOURS[k]:
            if k < v: 
                # Blue edges are just here to highlight the pentagones.
                if (k, v) in BLUE_LINK:
                    pygame.draw.line(
                        screen, RED, node_position[k], node_position[v], width=1
                    )
                else:
                    pygame.draw.line(
                        screen, BLUE, node_position[k], node_position[v], width=1
                    )

    # Draw every nodes, with tiles if any.
    for k in range(21):

        # Boolean tags to check wether there is a tile or not on the node.
        pos = 1 << k
        yellow_black = bool(pos & state.yellow_colors & state.black_colors)
        yellow_white = bool(pos & state.yellow_colors & state.white_colors)
        red_black = bool(pos & state.red_colors & state.black_colors)
        red_white = bool(pos & state.red_colors & state.white_colors)
        yellow_red = bool(pos & state.yellow_colors & state.red_colors)

        # If there is a tile.
        if yellow_black or yellow_white or red_black or red_white or yellow_red:
            # Draw the node circle.
            draw_circle_with_number(
                screen, node_position[k], CIRCLE_RADIUS, k, SLATE_GREY, WHITE
            )
            # Draw the tile's colors.
            if yellow_black:
                pygame.draw.circle(
                    screen,
                    LIGHT_YELLOW,
                    (
                        node_position[k][0] - cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] + sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (
                        node_position[k][0] + cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] - sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
            elif yellow_white:
                pygame.draw.circle(
                    screen,
                    LIGHT_YELLOW,
                    (
                        node_position[k][0] - cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] + sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        node_position[k][0] + cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] - sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
            elif red_black:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        node_position[k][0] - cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] + sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (
                        node_position[k][0] + cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] - sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
            elif red_white:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        node_position[k][0] - cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] + sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        node_position[k][0] + cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] - sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
            else:
                pygame.draw.circle(
                    screen,
                    LIGHT_YELLOW,
                    (
                        node_position[k][0] - cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] + sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        node_position[k][0] + cos(pi / 4) * CIRCLE_RADIUS / 2,
                        node_position[k][1] - sin(pi / 4) * CIRCLE_RADIUS / 2,
                    ),
                    CIRCLE_RADIUS / 3,
                )
        #  There is no tile.
        else:
            # Draw the node circle.
            draw_circle_with_number(
                screen, node_position[k], CIRCLE_RADIUS, k, FOREST_GREEN, WHITE
            )

    # Draw yellow pawn.
    if state.yellow_position == 0:
        pygame.draw.circle(
            screen,
            LIGHT_YELLOW,
            (
                node_position[0][0] - cos(pi / 4) * CIRCLE_RADIUS / 2,
                node_position[0][1] + sin(pi / 4) * CIRCLE_RADIUS / 2,
            ),
            CIRCLE_RADIUS * sqrt(2) / 4,
        )
    else:
        pygame.draw.circle(
            screen,
            LIGHT_YELLOW,
            node_position[state.yellow_position],
            CIRCLE_RADIUS * sqrt(2) / 4,
        )
    
    # Draw red pawn.
    if state.red_position == 0:
        pygame.draw.circle(
            screen,
            RED,
            (
                node_position[0][0] + cos(pi / 4) * CIRCLE_RADIUS / 2,
                node_position[0][1] - sin(pi / 4) * CIRCLE_RADIUS / 2,
            ),
            CIRCLE_RADIUS * sqrt(2) / 4,
        )
    else:
        pygame.draw.circle(
            screen, RED, node_position[state.red_position], CIRCLE_RADIUS * sqrt(2) / 4
        )
    
    # Draw black pawn.
    if state.black_position == 0:
        pygame.draw.circle(
            screen,
            BLACK,
            (
                node_position[0][0] - cos(pi / 4) * CIRCLE_RADIUS / 2,
                node_position[0][1] - sin(pi / 4) * CIRCLE_RADIUS / 2,
            ),
            CIRCLE_RADIUS * sqrt(2) / 4,
        )
    else:
        pygame.draw.circle(
            screen, BLACK, node_position[state.black_position], CIRCLE_RADIUS * sqrt(2) / 4
        )

    # Draw white pawn.
    if state.white_position == 0:
        pygame.draw.circle(
            screen,
            WHITE,
            (
                node_position[0][0] + cos(pi / 4) * CIRCLE_RADIUS / 2,
                node_position[0][1] + sin(pi / 4) * CIRCLE_RADIUS / 2,
            ),
            CIRCLE_RADIUS * sqrt(2) / 4,
        )
    else:
        pygame.draw.circle(
            screen, WHITE, node_position[state.white_position], CIRCLE_RADIUS * sqrt(2) / 4
        )
    
    # Draw orange pawn.
    if state.orange_position == 0:
        pygame.draw.circle(
            screen,
            ORANGE,
            (node_position[0][0], node_position[0][1]),
            CIRCLE_RADIUS * sqrt(2) / 4,
        )
    else:
        pygame.draw.circle(
            screen, ORANGE, node_position[state.orange_position], CIRCLE_RADIUS * sqrt(2) / 4
        )

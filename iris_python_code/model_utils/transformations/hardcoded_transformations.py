import torch
from iris_python_code.py_game.const.board_constants import *

def find_permutation(a, b):
    """
    Calculate the permutation needed to transform list 'a' into list 'b'.
    """
    index_map = {value: index for index, value in enumerate(a)}
    p = [index_map[b_element] for b_element in b]
    return p

# All possible rotations of the board's graph.
ROTATIONS = [
    [0] + [5 * i + ((k + l) % 5) + 1 for i in range(4) for k in range(5)]
    for l in range(5)
]

# List of corresponding policy transformation for a graph's rotation.
ROTATION_POLICY_TRANSFORM = [
    [
        find_permutation(NODE_NEIGHBOURS[r[k]], [r[i] for i in NODE_NEIGHBOURS[k]]) + list(range(len(NODE_NEIGHBOURS[k]), MAX_NB_NEIGHBOURS))
        for k in range(NB_REAL_NODE)
    ]
    for r in ROTATIONS
]

# All possible symetries of the board's graph.
SYMETRIES = [list(range(NB_REAL_NODE))] + [
    [0] + [(1 + (5 - k + core[i]) % 5) + 5 * i for i in range(4)
           for k in range(5)]
    for core in [(0, 4, 0, 4), (1, 0, 1, 0), (2, 1, 2, 1), (3, 2, 3, 2), (4, 3, 4, 3)]
]

# List of corresponding policy transformation for a graph's symetry.
SYMETRY_POLICY_TRANSFORM = [
    [
        find_permutation(NODE_NEIGHBOURS[s[k]], [s[i] for i in NODE_NEIGHBOURS[k]]) + list(range(len(NODE_NEIGHBOURS[k]), MAX_NB_NEIGHBOURS))
        for k in range(NB_REAL_NODE)
    ]
    for s in SYMETRIES
]

# Tensor representation of game state and corresponding policy index permutation when applying a swap of black and white pawn.
NEUTRAL_POSITION_TRANSFORM = torch.tensor([0, 1, 3, 2, 4, 5, 7, 6, 9, 8, 14, 15, 16, 17, 10, 11, 12, 13, 18, 19, 20, 21, 22], dtype=torch.int)
NEUTRAL_POLICY_TRANSFORM = torch.tensor(list(range(10)) + list(range(20, 30)) + list(range(10, 20)) + list(range(30, 41)) , dtype=torch.int)

# Tensor representation of game state and corresponding policy index permutation when applying a swap of player pawns.
PLAYER_POSITION_TRANSFORM = torch.tensor([1, 0, 2, 3, 4, 5, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 20, 21, 18, 19, 22], dtype=torch.int)

# Conversion of ROTATIONS, ROTATION_POLICY_TRANSFORM, SYMETRIES and SYMETRY_POLICY_TRANSFORM to tensor.
ROTATIONS = torch.tensor(ROTATIONS, dtype=torch.int)
ROTATION_POLICY_TRANSFORM = torch.tensor(ROTATION_POLICY_TRANSFORM, dtype=torch.int)
SYMETRIES = torch.tensor(SYMETRIES, dtype=torch.int)
SYMETRY_POLICY_TRANSFORM = torch.tensor(SYMETRY_POLICY_TRANSFORM, dtype=torch.int)
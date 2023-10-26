# Number of nodes in the board's graph
NB_REAL_NODE = 21

# Number of features of a node in the tensor representation of the game state
NB_FEATURES = 23

# Adjacency list representation of the board's graph.
NODE_NEIGHBOURS = (
    (1, 6, 2, 7, 3, 8, 4, 9, 5, 10),
    (0, 5, 10, 11, 6, 2),
    (0, 1, 6, 12, 7, 3),
    (0, 2, 7, 13, 8, 4),
    (0, 3, 8, 14, 9, 5),
    (0, 4, 9, 15, 10, 1),
    (0, 1, 10, 11, 16, 12, 7, 2),
    (0, 2, 6, 12, 17, 13, 8, 3),
    (0, 3, 7, 13, 18, 14, 9, 4),
    (0, 4, 8, 14, 19, 15, 10, 5),
    (0, 5, 9, 15, 20, 11, 6, 1),
    (1, 10, 15, 20, 16, 12, 6),
    (2, 6, 11, 16, 17, 13, 7),
    (3, 7, 12, 17, 18, 14, 8),
    (4, 8, 13, 18, 19, 15, 9),
    (5, 9, 14, 19, 20, 11, 10),
    (6, 11, 12),
    (7, 12, 13),
    (8, 13, 14),
    (9, 14, 15),
    (10, 15, 11),
)

# Maximum number of neighbors a node can have (equal to 10, central node).
MAX_NB_NEIGHBOURS = max([len(t) for t in NODE_NEIGHBOURS])

# Maximum number of moves in a given number of situation:
# The current player can move his pawn and every neutral pawn (4 * MAX_NB_NEIGHBOURS) plus one (no move available).
# This is a theoretical number to set the move's index to have a vector policy representation, but does not occur in practice.
NB_MOVE = 4 * MAX_NB_NEIGHBOURS + 1

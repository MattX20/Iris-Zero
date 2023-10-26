#include "game/game_constants.hpp"
#include "mcts/mcts_constants.hpp"
#include "iris_zero/iris_zero_constants.hpp"

// Initialization of game configuration constants, see 'include/game/game_constants.hpp'.
namespace game
{
    const std::vector<std::vector<int>> NODE_NEIGHBOURS = {
        {1, 6, 2, 7, 3, 8, 4, 9, 5, 10},
        {0, 5, 10, 11, 6, 2},
        {0, 1, 6, 12, 7, 3},
        {0, 2, 7, 13, 8, 4},
        {0, 3, 8, 14, 9, 5},
        {0, 4, 9, 15, 10, 1},
        {0, 1, 10, 11, 16, 12, 7, 2},
        {0, 2, 6, 12, 17, 13, 8, 3},
        {0, 3, 7, 13, 18, 14, 9, 4},
        {0, 4, 8, 14, 19, 15, 10, 5},
        {0, 5, 9, 15, 20, 11, 6, 1},
        {1, 10, 15, 20, 16, 12, 6},
        {2, 6, 11, 16, 17, 13, 7},
        {3, 7, 12, 17, 18, 14, 8},
        {4, 8, 13, 18, 19, 15, 9},
        {5, 9, 14, 19, 20, 11, 10},
        {6, 11, 12},
        {7, 12, 13},
        {8, 13, 14},
        {9, 14, 15},
        {10, 15, 11}};
    const std::vector<int> BIT_NODE_NEIGHBOURS = {
        2046, 3173, 4299, 8597, 17193, 34323, 72839, 143693, 287385, 574769, 1084003, 1152066, 207044, 414088, 828176, 1592864, 6208, 12416, 24832, 49664, 35840};
    const std::vector<int> NODE_NEIGHBOURS_SIZE = {
        10, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 3, 3, 3, 3, 3};
    const int NUMBER_REAL_NODES = 21;
    const int MAX_MVT_PER_PAWN = 10;
    const int MAX_MVTS = 4 * MAX_MVT_PER_PAWN + 1;
}

// Initialization of Monte Carlo Tree Search (MCTS) algorithm constants, see 'include/mcts/mcts_constants.hpp'.
namespace mcts
{
    const float UCT_PARAMETER = 2.0;
    const int MAX_TURN_PER_GAME_SIM = 20;
}

// Initialization of AlphaZero algorithm constants (theses are examples, not the one used in training), see 'include/iris_zero/iris_zero_constants.hpp'.
namespace iris_zero
{
    const int NUMBER_ATRIBUTES = 23;
    const float ALPHA_DIRICHLET = 0.8;
    const float PUCT_PARAMETER = 2.0;
    const int MAX_NB_TURN_SAMPLE = 100;
    const int NUM_SIM_PER_MOVE = 400;
    const int NUM_TURN_EXP_BEFORE_BEST = 0;
}
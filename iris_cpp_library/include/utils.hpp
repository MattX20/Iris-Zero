#pragma once

#include <utility>
#include <torch/torch.h>
#include "game/game_constants.hpp"
#include "game/move_iterator.hpp"
#include "iris_zero/iris_zero_constants.hpp"

// Converts and summarizes a move from the game's internal representation to a format easily
// interoperable with Python. It takes as input the initial game state before the move and
// the resulting game state after the move. It returns a pair of integers representing the move. 
// The first element is the index of the moved pawn 
// (0 : current player's pawn, 1 : black pawn, 2 : white pawn, 3 : orange pawn, -1 : no legal move)
// and the second is the chosen node's index in the game board.
inline std::pair<int, int> move_to_python_format(const game::GameState &parent, const game::GameState &child)
{

    // Recovering the index of the move.
    int index;
    for (const std::pair<int, game::GameState> &move : game::MoveGenerator(parent)) 
    {
        if (move.second == child)
        {
            index = move.first;
            break;
        }
    }

    // Index between 0 and game::MAX_MVT_PER_PAWN means that the player pawn is being played.
    if (index < game::MAX_MVT_PER_PAWN)
    {
        int real_index = index;

        // Moved pawn is player pawn.
        int moved_pawn = 0;

        // Recover the node the pawn is moved to with the index.
        int chosen_node = (parent.yellow_is_playing) ? game::NODE_NEIGHBOURS[parent.yellow_position][real_index] : game::NODE_NEIGHBOURS[parent.red_position][real_index];

        return std::make_pair(moved_pawn, chosen_node);
    }
    // Index between game::MAX_MVT_PER_PAWN and 2 * game::MAX_MVT_PER_PAWN means that the black pawn is being played.
    else if (index < 2 * game::MAX_MVT_PER_PAWN)
    {

        // Get the index of the moved node.
        int real_index = index - game::MAX_MVT_PER_PAWN; 

        // Black pawn is moved.
        int moved_pawn = 1;

        // Recover the node the pawn is moved to with the index.
        int chosen_node = game::NODE_NEIGHBOURS[parent.black_position][real_index];

        return std::make_pair(moved_pawn, chosen_node);
    }
    // Index between 2 * game::MAX_MVT_PER_PAWN and 3 * game::MAX_MVT_PER_PAWN means that the white pawn is being played.
    else if (index < 3 * game::MAX_MVT_PER_PAWN)
    {

        // Get the index of the moved node.
        int real_index = index - 2 * game::MAX_MVT_PER_PAWN;

        // White pawn is moved.
        int moved_pawn = 2;

        // Recover the node the pawn is moved to with the index.
        int chosen_node = game::NODE_NEIGHBOURS[parent.white_position][real_index];

        return std::make_pair(moved_pawn, chosen_node);
    }
    // Index between 3 * game::MAX_MVT_PER_PAWN and 4 * game::MAX_MVT_PER_PAWN means that the orange pawn is being played.
    else if (index < 4 * game::MAX_MVT_PER_PAWN)
    {

        // Get the index of the moved node.
        int real_index = index - 3 * game::MAX_MVT_PER_PAWN;

        // Orange pawn is moved.
        int moved_pawn = 3;

        // Recover the node the pawn is moved to with the index.
        int chosen_node = game::NODE_NEIGHBOURS[parent.orange_position][real_index];

        return std::make_pair(moved_pawn, chosen_node);
    }
    else
    {

        // index = 4 * game::MAX_MVT_PER_PAWN : no legal move
        return std::make_pair(-1, -1);
    }
}

// Transforms a game state into a tensor representation suitable for neural network processing.
//
//
// The resulting tensor is a NUMBER_REAL_NODES, NUMBER_ATRIBUTES tensor such that
// The five four columns are a one-hot encoding of the five pawns' locations. 
// The next five columns are indicative of the locations of the five different tile types, 
// with an assigned value of 1 indicating the presence of a tile of a specific type on a specific node, and 0 indicating its absence. 
// The next eight columns of the state representation array encode the consecutive usage of 
// both black and white pawns by the yellow and red players. Specifically, the first four columns are for the black pawn. 
// In these, the first column is filled with 1 if the yellow player used the black pawn in his last move. 
// Otherwise, it is filled with 0. Similarly, the second column is filled with 1 if the black pawn was used twice consecutively 
// by the yellow player in his last two moves, and 0 otherwise. The third and fourth columns use the same encoding, but represent 
// the red player's usage of the black pawn. 
// Following this, the other eight columns represent the consecutive usage of the white and the orange pawn, and use the same pattern 
// as the previous four columns. 
// The last column specifies the player's turn, filled with 0 if it is the yellow player's turn, and 1 if it is the red player's turn.
//
//
inline torch::Tensor game_state_to_tensor(const game::GameState &state)
{
    torch::Tensor state_tensor = torch::zeros({game::NUMBER_REAL_NODES, iris_zero::NUMBER_ATRIBUTES});
    auto state_tensor_accessor = state_tensor.accessor<float, 2>();

    state_tensor_accessor[state.yellow_position][0] = 1.0;
    state_tensor_accessor[state.red_position][1] = 1.0;
    state_tensor_accessor[state.black_position][2] = 1.0;
    state_tensor_accessor[state.white_position][3] = 1.0;
    state_tensor_accessor[state.orange_position][4] = 1.0;

    for (int k = 1; k < game::NUMBER_REAL_NODES; k++)
    {
        int pos = 1 << k;
        bool yr = state.yellow_colors & state.red_colors & pos;
        bool yb = state.yellow_colors & state.black_colors & pos;
        bool yw = state.yellow_colors & state.white_colors & pos;
        bool rb = state.red_colors & state.black_colors & pos;
        bool rw = state.red_colors & state.white_colors & pos;

        if (yr)
        {
            state_tensor_accessor[k][5] = 1.0;
        }
        else if (yb)
        {
            state_tensor_accessor[k][6] = 1.0;
        }
        else if (yw)
        {
            state_tensor_accessor[k][7] = 1.0;
        }
        else if (rb)
        {
            state_tensor_accessor[k][8] = 1.0;
        }
        else if (rw)
        {
            state_tensor_accessor[k][9] = 1.0;
        }
    }

    if (state.black_last_use)
    {
        if (state.black_consecutive_last_use == 1)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][10] = 1.0;
        }
        if (state.black_consecutive_last_use == 2)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][11] = 1.0;
        }
    }
    else
    {
        if (state.black_consecutive_last_use == 1)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][12] = 1.0;
        }
        if (state.black_consecutive_last_use == 2)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][13] = 1.0;
        }
    }

    if (state.white_last_use)
    {
        if (state.white_consecutive_last_use == 1)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][14] = 1.0;
        }
        if (state.white_consecutive_last_use == 2)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][15] = 1.0;
        }
    }
    else
    {
        if (state.white_consecutive_last_use == 1)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][16] = 1.0;
        }
        if (state.white_consecutive_last_use == 2)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][17] = 1.0;
        }
    }

    if (state.orange_last_use)
    {
        if (state.orange_consecutive_last_use == 1)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][18] = 1.0;
        }
        if (state.orange_consecutive_last_use == 2)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][19] = 1.0;
        }
    }
    else
    {
        if (state.orange_consecutive_last_use == 1)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][20] = 1.0;
        }
        if (state.orange_consecutive_last_use == 2)
        {
            for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
                state_tensor_accessor[k][21] = 1.0;
        }
    }

    if (!state.yellow_is_playing)
    {
        for (int k = 0; k < game::NUMBER_REAL_NODES; k++)
            state_tensor_accessor[k][22] = 1.0;
    }

    return state_tensor;
}
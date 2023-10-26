#pragma once
#include <utility>

// The 'mcts' namespace is used to organize all mcts related components.
namespace mcts
{
    // A function returning the best move according to a mcts search from a given position and a given thinking time in seconds.
    // See include/game/state.hpp for a description of the parameters.
    // Returns a pair of integers encoding the move played.
    std::pair<int, int> mcts_bot_time(
        bool yellow_is_playing,
        int yellow_position,
        int red_position,
        int black_position,
        int white_position,
        int orange_position,
        int yellow_colors,
        int red_colors,
        int black_colors,
        int white_colors,
        bool black_last_use,
        bool white_last_use,
        bool orange_last_use,
        int black_consecutive_last_use,
        int white_consecutive_last_use,
        int orange_consecutive_last_use,
        float reflexion_time);
    
    // A function returning the best move according to a mcts search from a given position and a given number of simulations.
    // See include/game/state.hpp for a description of the parameters.
    // Returns a pair of integers encoding the move played.
    std::pair<int, int> mcts_bot_sim(
        bool yellow_is_playing,
        int yellow_position,
        int red_position,
        int black_position,
        int white_position,
        int orange_position,
        int yellow_colors,
        int red_colors,
        int black_colors,
        int white_colors,
        bool black_last_use,
        bool white_last_use,
        bool orange_last_use,
        int black_consecutive_last_use,
        int white_consecutive_last_use,
        int orange_consecutive_last_use,
        int nb_simulations);
}
#pragma once
#include <string>
#include <utility>

// The 'iris_zero' namespace is used to organize all IrisZero related components.
namespace iris_zero
{

    // A function returning the best move according to a model search from a given position and a given thinking time in seconds.
    // See include/game/state.hpp for a description of the parameters.
    // Returns a pair of integers encoding the move played.
    std::pair<int, int> iris_zero_bot_time(
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
        float reflexion_time,
        const std::string &model_path);
    
    // A function returning the best move according to a model search from a given position and a given number of simulations.
    // See include/game/state.hpp for a description of the parameters.
    // Returns a pair of integers encoding the move played.
    std::pair<int, int> iris_zero_bot_sim(
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
        int nb_simulations,
        const std::string &model_path);
}
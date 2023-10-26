#pragma once
#include <utility>

// The 'random_bot' namespace is used to organize all random bot related components.
namespace random_bot
{
    
    // A function returning a random valid move from a given game state.
    // See include/game/state.hpp for a description of the parameters.
    // Returns a pair of integers encoding the move played.
    std::pair<int, int> random_bot(
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
        int orange_consecutive_last_use);
}
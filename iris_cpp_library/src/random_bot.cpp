#include <random>
#include "random_bot/random_bot.hpp"
#include "game/state.hpp"
#include "game/move_iterator.hpp"
#include "utils.hpp"

// Implementation of 'random_bot', see 'include/random_bot/random_bot.hpp'.
namespace random_bot
{
    // Internal function, implementing the random move selector.
    std::pair<int, int> random_bot_int(const game::GameState &state)
    {
        // Initializing random device and generator.
        std::random_device rd;
        std::mt19937 gen(rd());

        // Distribution for decision making, generates number between 0 and 1.
        std::uniform_real_distribution<> dis(0, 1);

        // Counter for the number of possible legal moves seen so far.
        int nb_seen_elements = 0;

        // Placeholder for the potential next game state.
        game::GameState child;

        // Iterating through all possible moves from the current game state.
        for (const std::pair<int, game::GameState> &move : game::MoveGenerator(state))
        {
            nb_seen_elements++;
            float random_number = dis(gen);

            // On the fly uniform selection of the next game state.
            if (random_number * nb_seen_elements <= 1.0)
            {
                child = move.second;
            }
        }
        // Convert the selected move to the required Python format and return.
        return move_to_python_format(state, child);
    }

    std::pair<int, int> random_bot(bool yellow_is_playing,
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
                                   int orange_consecutive_last_use)
    {

        // Create a game state structure instance with the given parameters.
        game::GameState state = {
            yellow_is_playing,
            yellow_position,
            red_position,
            black_position,
            white_position,
            orange_position,
            yellow_colors,
            red_colors,
            black_colors,
            white_colors,
            black_last_use,
            white_last_use,
            orange_last_use,
            black_consecutive_last_use,
            white_consecutive_last_use,
            orange_consecutive_last_use
        };
        // Return the internal function result.
        return random_bot_int(state);
    }
}
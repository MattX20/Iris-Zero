#include <random>
#include <algorithm>
#include "minmax_bot/minmax_bot.hpp"
#include "game/state.hpp"
#include "game/move_iterator.hpp"
#include "game/rules.hpp"
#include "utils.hpp"

// Implementation of 'minmax_bot', see 'include/minmax_bot/minmax_bot.hpp'.
namespace minmax_bot
{

    // A function that, given a GameState and a depth, returns a naive minmax evaluation
    // of this GameState. Can be refined with heuristics.
    float eval_game_state(const game::GameState &state, int depth = 0)
    {
        // If the yellow pawn is on the outer pentagone (node 16 to 20), the yellow player wins.
        if (16 <= state.yellow_position && state.yellow_position <= 20)
        {
            // This evaluation is almost equal to 1, but prioritizes quicker wins using the depth parameter.
            return 1.0 - 0.01 / (depth + 1); 
        }
        // If the red pawn is on the outer pentagone (node 16 to 20), the red player wins.
        else if (16 <= state.red_position && state.red_position <= 20)
        {
            // This evaluation is almost equal to -1, but prioritizes quicker wins using the depth parameter.
            return -1.0 + 0.01 / (depth + 1);
        }
        else
        {
            // No winner : the naive evaluation returns 0.
            return 0.0;
        }
    }

    // Implementation of the classical alpha-beta pruning algorithm.
    float search_minmax(int depth, const game::GameState &state, float alpha, float beta)
    {
        if (depth == 0)
        {
            return eval_game_state(state);
        }
        else if (game::exists_winner(state))
        {
            return eval_game_state(state, depth);
        }
        else if (state.yellow_is_playing)
        {
            float value = -2.0;

            for (const std::pair<int, game::GameState> &move : game::MoveGenerator(state))
            {
                value = std::max(value, search_minmax(depth - 1, move.second, alpha, beta));
                if (value > beta)
                    break;
                alpha = std::max(alpha, value);
            }
            return value;
        }
        else
        {
            float value = 2.0;

            for (const std::pair<int, game::GameState> &move : game::MoveGenerator(state))
            {
                value = std::min(value, search_minmax(depth - 1, move.second, alpha, beta));
                if (value < alpha)
                    break;
                beta = std::min(beta, value);
            }
            return value;
        }
    }

    // This internal function realises the first depth of the AlphaBeta search, and
    // then calls the previous function, to draw randomly from best value moves.
    std::pair<int, int> minmax_bot_int(int depth, const game::GameState &state)
    {
        // Initializing random device and generator.
        std::random_device rd;
        std::mt19937 gen(rd());

        // Distribution for decision making, generates number between 0 and 1.
        std::uniform_real_distribution<> dis(0, 1);

        // Placeholder for the potential next game state.
        game::GameState child;

        // Counter for the number of highest value moves seen so far.
        int nb_observed_best_move = 0;

        // Initial value of alpha and beta, value function must be in [alpha, beta]
        float alpha = -2.0;
        float beta = 2.0;

        // If yellow is playing, then tries to maximize the value.
        if (state.yellow_is_playing)
        {
            float best_value_so_far = -2.0;

            for (const std::pair<int, game::GameState> &move : game::MoveGenerator(state))
            {
                float current_value = search_minmax(depth, move.second, alpha, beta);

                // The value is strictly better than what has been seen so far                
                if (current_value > best_value_so_far)
                {
                    // Update variables.
                    best_value_so_far = current_value;
                    nb_observed_best_move = 1;
                    child = move.second;

                    // Alpha-Beta pruning.
                    if (current_value > beta)
                        break;
                    alpha = std::max(alpha, current_value);
                }
                // The value is strictly better than what has been seen so far 
                else if (current_value == best_value_so_far)
                {
                    // Update variables.
                    nb_observed_best_move++;
                    float random_number = dis(gen);

                    // Uniform on the fly selection of the child from best value moves.
                    if (random_number * nb_observed_best_move <= 1.0)
                        child = move.second;
                    
                    // Alpha-Beta pruning.
                    if (current_value > beta)
                        break;
                    alpha = std::max(alpha, current_value);
                }
            }
        }
        // If yellow is playing, then tries to minimize the value.
        else
        {
            float best_value_so_far = 2.0;

            for (const std::pair<int, game::GameState> &move : game::MoveGenerator(state))
            {
                float current_value = search_minmax(depth, move.second, alpha, beta);

                if (current_value < best_value_so_far)
                {
                    best_value_so_far = current_value;
                    nb_observed_best_move = 1;
                    child = move.second;

                    if (current_value < alpha)
                        break;
                    beta = std::min(beta, current_value);
                }
                else if (current_value == best_value_so_far)
                {
                    nb_observed_best_move++;
                    float random_number = dis(gen);

                    if (random_number * nb_observed_best_move <= 1.0)
                        child = move.second;
                    if (current_value < alpha)
                        break;
                    beta = std::min(beta, current_value);
                }
            }
        }
        return move_to_python_format(state, child);
    }

    std::pair<int, int> minmax_bot(bool yellow_is_playing,
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
                                   int depth)
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
        return minmax_bot_int(depth, state);
    }
}
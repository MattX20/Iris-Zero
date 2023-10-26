#include <random>
#include <vector>
#include <cmath>
#include <algorithm>
#include <chrono>
#include "mcts/mcts_bot.hpp"
#include "mcts/mcts_constants.hpp"
#include "game/state.hpp"
#include "game/move_iterator.hpp"
#include "game/rules.hpp"
#include "utils.hpp"

// Implementation of 'mcts_bot', see 'include/mcts/mcts_bot.hpp'.
namespace mcts
{

    // Represents a node within the Monte Carlo Tree Search (MCTS) exploration tree.
    // Each node corresponds to a potential state in the game, along with metadata useful for the MCTS algorithm.
    struct Node
    {
        // The game state that this node represents.
        game::GameState state;

        // Pointer to the parent node in the MCTS tree.
        Node *parent;

        // List of pointers to the child nodes.
        std::vector<Node *> children;

        // Sum of the outputs of the game.
        // -1 : loss, +1 : win, 0 : draw.
        float wins;

        // Number of times this node has been visited.
        int visits;

        Node(game::GameState state, Node *parent = nullptr) : state(state), parent(parent), children(), wins(0.0), visits(0) {}
    };

    // Recursively deletes a node and all of its descendants.
    void delete_node(Node *node)
    {
        for (auto child : node->children)
        {
            delete_node(child);
        }
        node->children.clear();
        delete node;
    }

    // Calculates the UCT value for a node, used to determine optimal nodes to explore in the MCTS.
    float uctValue(Node *node)
    {
        return (node->visits == 0) ? std::numeric_limits<float>::max() : node->wins / node->visits + sqrt(UCT_PARAMETER * log(node->parent->visits) / node->visits);
    }

    // Determines the child with the highest UCT value.
    Node *bestUCTChild(Node *node)
    {
        Node *bestChild = nullptr;
        float maxUCTValue = std::numeric_limits<float>::lowest();

        for (Node *child : node->children)
        {
            float childUCTValue = uctValue(child);
            if (childUCTValue > maxUCTValue)
            {
                maxUCTValue = childUCTValue;
                bestChild = child;
            }
        }
        return bestChild;
    }

    // Performs the selection step of the MCTS, choosing a node to be expanded based on UCT values.
    Node *select(Node *node)
    {
        while (!game::exists_winner(node->state) && !node->children.empty())
        {
            node = bestUCTChild(node);
        }
        return node;
    }

    // Expands a non-terminal node by adding all possible following states to the tree, and one of them chosen randomly.
    Node *expand(Node *node)
    {
        if (exists_winner(node->state))
        {
            return node;
        }

        std::random_device rd;
        std::mt19937 gen(rd());

        std::uniform_real_distribution<> dis(0, 1);

        int nb_observed_legal_move = 0;

        Node *return_node;

        for (const std::pair<int, game::GameState> &move : game::MoveGenerator(node->state))
        {
            nb_observed_legal_move++;
            float random_number = dis(gen);

            Node *new_node = new Node(move.second, node);
            node->children.push_back(new_node);

            if (random_number * nb_observed_legal_move <= 1.0)
            {
                return_node = new_node;
            }
        }

        return return_node;
    }

    // Simulates a random playout from the node, returning the game result.
    int simulate(Node *node, std::mt19937 &gen, std::uniform_real_distribution<> &dis)
    {
        game::GameState currentState = node->state;
        int nb_turn = 0;

        // Instead of playing a full game, every game with more turn than MAX_TURN_PER_GAME_SIM
        // will be returned as draw to speed up computations.
        while (!game::exists_winner(currentState) && nb_turn < MAX_TURN_PER_GAME_SIM)
        {
            game::GameState new_state;
            int nb_observed_legal_move = 0;

            for (const std::pair<int, game::GameState> &move : game::MoveGenerator(currentState))
            {
                nb_observed_legal_move++;
                float random_number = dis(gen);

                if (random_number * nb_observed_legal_move < 1.0)
                {
                    new_state = move.second;
                }
            }

            currentState = new_state;
            ++nb_turn;
        }
        // 0 represents a draw, 1 a win for Yellow, and 2 a win for Red.
        if (nb_turn >= MAX_TURN_PER_GAME_SIM)
        {
            return 0;
        }
        // If the yellow pawn is on the outter pentagone, Yellow wins.
        else if (16 <= currentState.yellow_position && currentState.yellow_position <= 20)
        {
            return 1;
        }
        // Red win (there is one because nb_turn < MAX_TURN_PER_GAME_SIM and it is not yellow).
        return 2;
    }

    // Updates the MCTS tree with the result of a simulation.
    void backpropagate(Node *node, int result)
    {
        while (node != nullptr)
        {
            node->visits++;
            // Here if the current player lost, the backpropagated result is +1, if he won it is -1 and 0 in case of a draw.
            // This is because the UCT is computed from the other player's perspective.
            if ((result == 1 && !node->state.yellow_is_playing) || (result == 2 && node->state.yellow_is_playing))
            {
                node->wins += 1.0;
            }
            else if (result != 0)
            {
                node->wins -= 1.0;
            }
            node = node->parent;
        }
    }

    // Internal function implementing the full MCTS algorithm with a time limit.
    std::pair<int, int> mcts_bot_time_int(float reflexion_time, const game::GameState &root_state)
    {
        Node *root = new Node(root_state);

        std::random_device rd;
        std::mt19937 gen(rd());

        std::uniform_real_distribution<> dis(0, 1);

        auto start_time = std::chrono::high_resolution_clock::now();
        while (std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - start_time).count() < reflexion_time)
        {
            Node *selected_node = select(root);
            Node *expanded_node = expand(selected_node);
            int result = simulate(expanded_node, gen, dis);
            backpropagate(expanded_node, result);
        }

        Node *best_child = nullptr;
        int max_visits = std::numeric_limits<int>::min();

        for (Node *child : root->children)
        {
            if (child->visits > max_visits)
            {
                max_visits = child->visits;
                best_child = child;
            }
        }

        std::pair<int, int> result = move_to_python_format(root_state, best_child->state);
        delete_node(root);

        return result;
    }

    // Internal function implementing the full MCTS algorithm with a maximum number of simulations.
    std::pair<int, int> mcts_bot_sim_int(int nb_simulations, const game::GameState &root_state)
    {
        Node *root = new Node(root_state);

        std::random_device rd;
        std::mt19937 gen(rd());

        std::uniform_real_distribution<> dis(0, 1);

        for (int _l = 0; _l < nb_simulations; _l++)
        {
            Node *selected_node = select(root);
            Node *expanded_node = expand(selected_node);
            int result = simulate(expanded_node, gen, dis);
            backpropagate(expanded_node, result);
        }

        Node *best_child = nullptr;
        int max_visits = std::numeric_limits<int>::min();

        for (Node *child : root->children)
        {
            if (child->visits > max_visits)
            {
                max_visits = child->visits;
                best_child = child;
            }
        }

        std::pair<int, int> result = move_to_python_format(root_state, best_child->state);
        delete_node(root);

        return result;
    }

    std::pair<int, int> mcts_bot_time(bool yellow_is_playing,
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
                                      float reflexion_time)
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
        return mcts_bot_time_int(reflexion_time, state);
    }

    std::pair<int, int> mcts_bot_sim(bool yellow_is_playing,
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
                                     int nb_simulations)
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
        return mcts_bot_sim_int(nb_simulations, state);
    }
}
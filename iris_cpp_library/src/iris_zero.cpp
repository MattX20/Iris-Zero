#include <string>
#include <tuple>
#include <utility>
#include <vector>
#include <random>
#include <cmath>
#include <memory>
#include <chrono>
#include <torch/torch.h>
#include <torch/script.h>
#include "utils.hpp"
#include "game/rules.hpp"
#include "iris_zero/iris_zero_bot.hpp"
#include "iris_zero/iris_zero_training.hpp"
#include "iris_zero/iris_zero_constants.hpp"

// Implementation of 'iris_zero', see 'include/iris_zero/iris_zero_bot.hpp' and 'include/iris_zero/iris_zero_training.hpp'.
namespace iris_zero
{
    // Evaluates the game's position using a neural network model, returning a pair of policy and value.
    // Takes as input the tensor of the position to be evaluated, and the loaded TorchScript module.
    std::pair<torch::Tensor, float> position_evaluation(const torch::Tensor &state_tensor, torch::jit::script::Module module)
    {
        torch::Tensor input = state_tensor.unsqueeze(0);
        std::vector<torch::jit::IValue> inputs = {input};

        torch::NoGradGuard no_grad;
        torch::jit::IValue output = module.forward(inputs);

        auto output_tuple = output.toTuple();

        torch::Tensor policy_logit = output_tuple->elements()[0].toTensor().squeeze(0);
        float value = output_tuple->elements()[1].toTensor()[0][0].item<float>();

        torch::Tensor policy = torch::softmax(policy_logit, 0);

        return std::make_pair(policy, value);
    }

    // Represents a single node in the search tree of the AlphaZero MCTS algorithm.
    struct Node
    {
        // The game state that this node represents.
        game::GameState state;

        // Tensor representation of the game state, suitable for neural network processing.
        torch::Tensor state_tensor;

        // Unique index representing the specific move taken from the parent node to reach this current node.
        int idx_;

        // Number of times this node has been visited.
        int visits;

        // Sum of the outputs of the values of the positions evaluated by the model in this node's subtree.
        float wins;

        // Predicted value (expected outcome) of this GameSate, as given by the neural network.
        float value;

        // Flag indicating whether this node has been expanded (i.e., all its possible children have been generated).
        bool is_expanded;

        // Pointer to the parent node in the search tree.
        Node *parent;

        // List of pointers to the child nodes.
        std::vector<Node *> children;

        // Probability distribution over moves, as given by the neural network's policy head.
        torch::Tensor policy;

        Node(
            game::GameState state,
            int idx = 0,
            Node *parent = nullptr) : state(state),
                                      idx_(idx),
                                      parent(parent),
                                      visits(0),
                                      wins(0.0),
                                      value(0.0),
                                      is_expanded(false),
                                      children(),
                                      state_tensor(),
                                      policy() {}

        ~Node()
        {
            for (Node *child : children)
            {
                delete child;
            }
        }
    };

    void add_dirichlet_noise(Node *node, std::mt19937 &gen)
    {
        int size = node->children.size();
        std::vector<float> samples(size);

        std::gamma_distribution<> gamma_dist(ALPHA_DIRICHLET, 1.0);
        auto root_policy_accessor = node->policy.accessor<float, 1>();

        float sum = 0.0;
        for (int i = 0; i < size; ++i)
        {
            float noise_value = gamma_dist(gen);
            samples[i] = noise_value;
            sum += noise_value;
        }

        int idx = 0;
        for (Node *child : node->children)
        {
            root_policy_accessor[child->idx_] = 0.75 * root_policy_accessor[child->idx_] + 0.25 * samples[idx] / sum;
            idx++;
        }
    }

    // Calculates the PUCT value for a node, used to determine optimal nodes to explore in the AlphaZero search algorithm.
    float puctValue(Node *node)
    {
        float q = (node->visits > 0) ? node->wins / node->visits : 0.0;
        float u = node->parent->policy[node->idx_].item<float>() * sqrt(PUCT_PARAMETER * (node->parent->visits - 1)) / (node->visits + 1);
        return u + q;
    }


    // Determines the child with the highest PUCT value.
    Node *bestPUCTChild(Node *node)
    {
        Node *bestChild = nullptr;
        float maxPUCTValue = std::numeric_limits<float>::lowest();

        for (Node *child : node->children)
        {
            float childPUCTValue = puctValue(child);
            if (childPUCTValue > maxPUCTValue)
            {
                maxPUCTValue = childPUCTValue;
                bestChild = child;
            }
        }
        return bestChild;
    }

    // Performs the selection step of the MCTS, choosing a node to be expanded based on UCT values.
    Node *select(Node *node)
    {
        while (!game::exists_winner(node->state) && node->is_expanded)
        {
            node = bestPUCTChild(node);
        }
        return node;
    }

    // Expands a node by computing its value and policy according to the model, 
    // and add all possible following states to the tree if the node is not termial.
    void expand(Node *node, torch::jit::script::Module module)
    {
        if (node->is_expanded)
        {
            return;
        }
        node->is_expanded = true;

        torch::Tensor state_tensor = game_state_to_tensor(node->state);
        node->state_tensor = state_tensor;
        auto [policy, value] = position_evaluation(node->state_tensor, module);
        node->policy = policy;
        node->value = value;

        if (game::exists_winner(node->state))
        {
            return;
        }

        for (const std::pair<int, game::GameState> &move : game::MoveGenerator(node->state))
        {
            Node *new_node = new Node(move.second, move.first, node);
            node->children.push_back(new_node);
        }
    }

    // Updates the search tree with the value computed byt the model.
    void backpropagate(Node *node, float value)
    {
        while (node != nullptr)
        {
            node->visits++;
            node->wins += (node->state.yellow_is_playing) ? -value : value;
            node = node->parent;
        }
    }

    // Takes a Node, and returns its policy (distribution of explored following moves) after the search.
    torch::Tensor node_mcts_policy(Node *node)
    {
        torch::Tensor node_policy = torch::zeros({game::MAX_MVTS});
        auto node_policy_accessor = node_policy.accessor<float, 1>();

        for (Node *child : node->children)
        {
            node_policy_accessor[child->idx_] = static_cast<float>(child->visits) / (node->visits - 1);
        }

        return node_policy;
    }

    // Takes a Node, and returns its best following move (most explored one).
    std::pair<int, Node *> next_move_best(Node *root_node)
    {
        int idx_best = 0, idx_current = 0;
        Node *best = root_node->children[idx_best];
        int visits_best = best->visits;

        for (Node *child : root_node->children)
        {
            if (child->visits > visits_best)
            {
                best = child;
                visits_best = child->visits;
                idx_best = idx_current;
            }
            idx_current++;
        }

        return std::make_pair(idx_best, best);
    }

    // Takes a Node, and returns a randomly selected following move, given the search distribution and a temperature.
    std::pair<int, Node *> next_move_best_exp(Node *root_node, torch::Tensor root_policy, std::mt19937 &gen)
    {
        std::uniform_real_distribution<> uniform_dist(0, 1);

        Node *best_exp_child = root_node->children[0];
        int idx_best = 0;
        int idx_current = 0;

        auto root_policy_accessor = root_policy.accessor<float, 1>();

        float sum = 0.0;
        for (Node *child : root_node->children)
        {
            // The 1 in the pow function is used here as a temperature parameter.
            float smoothed_value = pow(root_policy_accessor[child->idx_], 1);
            sum += smoothed_value;

            float random_float = uniform_dist(gen);

            if (sum * random_float <= smoothed_value)
            {
                idx_best = idx_current;
                best_exp_child = child;
            }
            idx_current++;
        }

        return std::make_pair(idx_best, best_exp_child);
    }

    // This internal function takes as input an initial gamestate, a model, and generates a training sample from it.
    // A training sample is a tuple of (posion tensor, policy tensor, value tensor) from a self-played game with the constants defined in 'constants.cpp'.
    std::tuple<torch::Tensor, torch::Tensor, torch::Tensor> generate_training_sample_int(const game::GameState &state, const std::string &model_path)
    {
        std::random_device rd;
        std::mt19937 gen(rd());

        torch::jit::script::Module module;
        try
        {
            module = torch::jit::load(model_path);
        }
        catch (const c10::Error &e)
        {
            std::cerr << "Error loading the model\n";
            throw e;
        }

        std::vector<torch::Tensor> game_state_recoder;
        std::vector<torch::Tensor> game_policy_recorder;

        Node *root_node = new Node(state);
        int turn = 0;

        while (turn < MAX_NB_TURN_SAMPLE && !game::exists_winner(root_node->state))
        {
            if (!root_node->is_expanded)
            {
                expand(root_node, module);
                backpropagate(root_node, root_node->value);
            }

            add_dirichlet_noise(root_node, gen);

            while (root_node->visits < NUM_SIM_PER_MOVE)
            {
                Node *selected_node = select(root_node);
                expand(selected_node, module);
                backpropagate(selected_node, selected_node->value);
            }
            torch::Tensor root_policy = node_mcts_policy(root_node);

            game_state_recoder.push_back(root_node->state_tensor);
            game_policy_recorder.push_back(root_policy);

            Node *new_root;
            int idx_new_root;

            if (turn <= NUM_TURN_EXP_BEFORE_BEST)
            {
                auto res = next_move_best_exp(root_node, root_policy, gen);
                idx_new_root = res.first;
                new_root = res.second;
            }
            else
            {
                auto res = next_move_best(root_node);
                idx_new_root = res.first;
                new_root = res.second;
            }

            root_node->children[idx_new_root] = nullptr;
            new_root->parent = nullptr;
            delete root_node;
            root_node = new_root;

            ++turn;
        }

        float winner = 0.0;

        if (turn < MAX_NB_TURN_SAMPLE && game::exists_winner(root_node->state))
        {
            if (!root_node->is_expanded)
            {
                expand(root_node, module);
                backpropagate(root_node, root_node->value);
            }

            torch::Tensor win_policy = torch::ones({game::MAX_MVTS});
            win_policy = win_policy / game::MAX_MVTS;

            game_state_recoder.push_back(root_node->state_tensor);
            game_policy_recorder.push_back(win_policy);

            if (root_node->state.yellow_is_playing)
            {
                winner = -1.0;
            }
            else
            {
                winner = 1.0;
            }
            turn++;
        }

        delete root_node;

        torch::Tensor stacked_positions = torch::stack(game_state_recoder, 0);
        torch::Tensor stacked_policies = torch::stack(game_policy_recorder, 0);
        torch::Tensor stacked_values = torch::full({turn}, winner);

        return std::make_tuple(stacked_positions, stacked_policies, stacked_values);
    }

    // Internal function implementing the full AlphaZero playing algorithm with a time limit.
    std::pair<int, int> iris_zero_bot_time_int(const game::GameState &state, float reflexion_time, const std::string &model_path)
    {
        torch::jit::script::Module module;
        try
        {
            module = torch::jit::load(model_path);
        }
        catch (const c10::Error &e)
        {
            std::cerr << "Error loading the model\n";
            throw e;
        }

        std::vector<torch::Tensor> game_state_recoder;
        std::vector<torch::Tensor> game_policy_recorder;

        Node *root_node = new Node(state);

        auto start_time = std::chrono::high_resolution_clock::now();
        while (std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - start_time).count() < reflexion_time)
        {
            Node *selected_node = select(root_node);
            expand(selected_node, module);
            backpropagate(selected_node, selected_node->value);
        }

        auto best_move = next_move_best(root_node);
        auto result = move_to_python_format(root_node->state, best_move.second->state);

        delete root_node;

        return result;
    }

    // Internal function implementing the full AlphaZero playing algorithm with a maximum number of simulations.
    std::pair<int, int> iris_zero_bot_sim_int(const game::GameState &state, int nb_simulations, const std::string &model_path)
    {
        torch::jit::script::Module module;
        try
        {
            module = torch::jit::load(model_path);
        }
        catch (const c10::Error &e)
        {
            std::cerr << "Error loading the model\n";
            throw e;
        }

        std::vector<torch::Tensor> game_state_recoder;
        std::vector<torch::Tensor> game_policy_recorder;

        Node *root_node = new Node(state);

        for (int _l = 0 ; _l < nb_simulations ; _l++)
        {
            Node *selected_node = select(root_node);
            expand(selected_node, module);
            backpropagate(selected_node, selected_node->value);
        }

        auto best_move = next_move_best(root_node);

        auto result = move_to_python_format(root_node->state, best_move.second->state);

        delete root_node;

        return result;
    }

    std::tuple<torch::Tensor, torch::Tensor, torch::Tensor> generate_training_sample(
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
        const std::string &model_path)
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
        return generate_training_sample_int(state, model_path);
    }

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
        const std::string &model_path)
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
        return iris_zero_bot_time_int(state, reflexion_time, model_path);
    }

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
        const std::string &model_path)
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
        return iris_zero_bot_sim_int(state, nb_simulations, model_path);
    }
}
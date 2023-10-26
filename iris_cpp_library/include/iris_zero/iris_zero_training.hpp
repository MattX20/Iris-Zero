#pragma once
#include <string>
#include <tuple>
#include <torch/torch.h>

// The 'iris_zero' namespace is used to organize all IrisZero related components.
namespace iris_zero
{

    // A function returning a self played game from a position and a given model, to be used for training.
    // See include/game/state.hpp for a description of the parameters.
    // Returns a tuple of tensor : the stacked game state representations, the corresponding policies and values.
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
        const std::string &model_path);
}
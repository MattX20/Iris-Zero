#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <torch/torch.h>
#include <torch/extension.h>
#include "random_bot/random_bot.hpp"
#include "minmax_bot/minmax_bot.hpp"
#include "mcts/mcts_bot.hpp"
#include "iris_zero/iris_zero_bot.hpp"
#include "iris_zero/iris_zero_training.hpp"

// Namespace for pybind11
namespace py = pybind11;

// Creating a Python module using pybind11. This module will be a bridge between Python and several C++ functions.
// Each function exposed here will be callable from Python once the module is imported.
PYBIND11_MODULE(py_iris, m)
{

    // Documentation for the entire Python module
    m.doc() = "py_iris module: C++ implementations of various game-playing algorithms, and training routines for AlphaZero, exposed to Python through PyBind11.";
    
    // Exposing the 'random_bot' function to Python.
    m.def("random_bot", &random_bot::random_bot, "A function returning a random valid move from a given position");

    // Exposing the 'minmax_bot' function to Python.
    m.def("minmax_bot", &minmax_bot::minmax_bot, "A function returning the best move according to a minmax search from a given position and a given depth");

    // Exposing the 'mcts_bot_time' function to Python.
    m.def("mcts_bot_time", &mcts::mcts_bot_time, "A function returning the best move according to a mcts search from a given position and a given thinking time in seconds");

    // Exposing the 'mcts_bot_sim' function to Python.
    m.def("mcts_bot_sim", &mcts::mcts_bot_sim, "A function returning the best move according to a mcts search from a given position and a given number of simulations");

    // Exposing the 'iris_zero_bot_time' function to Python.
    m.def("iris_zero_bot_time", &iris_zero::iris_zero_bot_time, "A function returning the best move according to a model search from a given position and a given thinking time in seconds");

    // Exposing the 'iris_zero_bot_sim' function to Python.
    m.def("iris_zero_bot_sim", &iris_zero::iris_zero_bot_sim, "A function returning the best move according to a model search from a given position and a given number of simulations");

    // Exposing the 'generate_training_sample' function to Python.
    m.def("generate_training_sample", &iris_zero::generate_training_sample, "A function returning a self played game from a position and a given model, to be used for training");
}
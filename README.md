# Iris Zero

**Iris Zero** is a software implementing various game playing algorithms —MinMax, MCTS, and AlphaZero— on a game named Iris.  See the [rules](rules.md).

## Directory Structure

- `img/`: Images referenced by the documentation.
- `iris_cpp_library/`: The core C++ implementation handling game mechanics and algorithmic logic.
- `iris_python_code/`: Python integration, including the AlphaZero model and the game's visual interface.
- `models/`: Storage location for neural network model files, including weights and TorchScript format files.
- `game.py`: The main executable script that launches the game's visual interface.
- `training_epoch_example.py`: Script presenting the structure of a typical model training epoch.

## Prerequisites    
- **Python:** Version 3.10 or newer.
- **C++:** Compliance with C++ 17 standard or newer.

## Installation & Setup
1. **Set Up the Python Environment:**
    - Create a virtual environment in Python to manage the dependencies.
    - Run `pip install -r requirements.txt` to install all the necessary Python packages.

2. **Configure C++ Backend:**
    - Create an `external` directory within `iris_cpp_library/`.
    - Follow the official guide to [install the latest libtorch library](https://pytorch.org/cppdocs/installing.html) in the `external` folder.
    - Rename and adapt `CMakeLists_example.txt` to your system configuration (e.g., paths, additional parameters).

3. **Build the Project:**
    - Create a `build` directory in `iris_cpp_library/`.
    - Compile the project using CMake:
      ```
      cd iris_cpp_library/build
      cmake ..
      make .
      ```

4. **Launch Iris Zero:**
    - Run the game interface script with the command: 
      ```
      python game.py
      ```
## References

#### Minimax Algorithm
- Knuth, D. E., & Moore, R. W. (1975). An analysis of alpha-beta pruning. Artificial Intelligence, 6(4), 293-326.

#### Monte Carlo Tree Search (MCTS)
- Kocsis, L., & Szepesvári, C. (2006). Bandit-based Monte-Carlo Planning. In Machine Learning: ECML 2006 (pp. 282-293).

#### AlphaZero
- Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai, M., Guez, A., ... & Hassabis, D. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. Science, 362(6419), 1140-1144.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE.md) file.
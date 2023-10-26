#pragma once

// The 'mcts' namespace is used to organize all mcts related components.
namespace mcts
{
    
    // Exploration parameter in the upper confidence bound applied to tree (UCT) criteria.
    extern const float UCT_PARAMETER;
    
    // Max number of turn per game simulation.
    extern const int MAX_TURN_PER_GAME_SIM;
}
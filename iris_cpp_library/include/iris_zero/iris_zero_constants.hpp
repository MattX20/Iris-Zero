#pragma once

// The 'iris_zero' namespace is used to organize all IrisZero related components.
namespace iris_zero
{
    
    // Parameter for the dirichlet noise added to the root policy when generating game samples.
    extern const float ALPHA_DIRICHLET; 
    
    // Exploration parameter in the PUCT criteria, see AlphaZero paper.
    extern const float PUCT_PARAMETER;

    // Max number of turn in a training sample game.
    extern const int MAX_NB_TURN_SAMPLE;      

     // Number of simulations per moves when generating training sample games.
    extern const int NUM_SIM_PER_MOVE;

    // Number of turns before selecting greedily the next move, see AlphaZero paper.
    extern const int NUM_TURN_EXP_BEFORE_BEST; 

    // Number of attributes per node on the tensor representation of the game.
    extern const int NUMBER_ATRIBUTES;         
}
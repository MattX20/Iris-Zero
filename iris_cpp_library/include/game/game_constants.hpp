#pragma once

#include <vector>

// The 'game' namespace is used to organize all game-related components.
namespace game
{
    
    // Represents an adjacency list of the graph depicting the game. Each inner vector 
    // contains node indices representing neighbors of a node.
    extern const std::vector<std::vector<int>> NODE_NEIGHBOURS; 

    // An adjacency list representation similar to NODE_NEIGHBOURS, but the neighbors are 
    // represented in a bit format for efficient bitwise operations. 
    // The k-th bit of BIT_NODE_NEIGHBOURS[i] if node k is adjacent to node i.
    extern const std::vector<int> BIT_NODE_NEIGHBOURS;          

    // Contains the degree (number of neighbors) of each node in the graph. 
    // The index of this vector corresponds to the node index.
    extern const std::vector<int> NODE_NEIGHBOURS_SIZE; 

    // Total number of actual nodes present in the game graph.
    extern const int NUMBER_REAL_NODES; 

    // Maximum number of possible moves a pawn can make during a turn.                        
    extern const int MAX_MVT_PER_PAWN; 

    // Maximum number of possible moves a player can make during a turn                         
    extern const int MAX_MVTS;                                  
}
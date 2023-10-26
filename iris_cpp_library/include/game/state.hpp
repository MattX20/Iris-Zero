#pragma once

// The 'game' namespace is used to organize all game-related components.
namespace game
{
    
    // An instance of GameState represents a complete state of the game.
    struct GameState
    {
        // Boolean flag indicating the current player's turn: 'true' for yellow, 'false' for red.
        bool yellow_is_playing;

        // Positions of the pawns on the board. Each 'position' corresponds to the node index
        // where the pawn of the respective color is located.
        int yellow_position;            
        int red_position;               
        int black_position;             
        int white_position;             
        int orange_position;             

        // Bitfields representing the presence of the corresponding color on the node's tiles.
        // If the k-th bit is set, it indicates that a tile holding the respective color is
        // present on the k-th node.
        int yellow_colors;              
        int red_colors;                
        int black_colors;               
        int white_colors;              
        
        // Flags representing the last usage of 'neutral' pawns (black, white, and orange).
        // A 'true' value indicates the yellow player was the last to use the pawn; 'false' indicates the red player.
        bool black_last_use;            
        bool white_last_use;           
        bool orange_last_use;            

        // Count of consecutive turns each 'neutral' pawn has been used by the same player.
        int black_consecutive_last_use; 
        int white_consecutive_last_use;
        int orange_consecutive_last_use; 

        // Compares two GameState instances for equality. Two game states are considered equal if all their
        // corresponding properties' values are identical, representing the same game context.
        bool operator==(const GameState &rhs) const
        {
            return yellow_is_playing == rhs.yellow_is_playing &&
                   yellow_position == rhs.yellow_position &&
                   red_position == rhs.red_position &&
                   black_position == rhs.black_position &&
                   white_position == rhs.white_position &&
                   orange_position == rhs.orange_position &&
                   yellow_colors == rhs.yellow_colors &&
                   red_colors == rhs.red_colors &&
                   black_colors == rhs.black_colors &&
                   white_colors == rhs.white_colors &&
                   black_last_use == rhs.black_last_use &&
                   white_last_use == rhs.white_last_use &&
                   orange_last_use == rhs.orange_last_use &&
                   black_consecutive_last_use == rhs.black_consecutive_last_use &&
                   white_consecutive_last_use == rhs.white_consecutive_last_use &&
                   orange_consecutive_last_use == rhs.orange_consecutive_last_use;
        }
    };
}
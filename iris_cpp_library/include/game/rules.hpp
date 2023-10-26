#pragma once

#include "state.hpp"
#include "game_constants.hpp"

// The 'game' namespace is used to organize all game-related components.
namespace game
{

    // Determines if the current player is allowed to play the black pawn based on the game state.
    // A player can move the black pawn if they were the last to do so, but less than twice in a row, 
    // or if the pawn hasn't been moved by the other player in the previous turn.
    inline bool can_play_black(const GameState &state)
    {

        // Identify who was the last to play the black pawn.
        // True : yellow, false : red
        bool is_last_black_player = (state.yellow_is_playing) ? state.black_last_use : !state.black_last_use;

        // Allow the move if the current player was the last to play black and has done so less than twice consecutively,
        // or if it has not been played by the other player in the previous turn.
        return (is_last_black_player && state.black_consecutive_last_use < 2) || state.black_consecutive_last_use == 0;
    }

    // Determines if the current player is allowed to play the white pawn based on the game state.
    // A player can move the white pawn if they were the last to do so, but less than twice in a row, 
    // or if the pawn hasn't been moved by the other player in the previous turn.
    inline bool can_play_white(const GameState &state)
    {

        // Identify who was the last to play the white pawn.
        // True : yellow, false : red
        bool is_last_white_player = (state.yellow_is_playing) ? state.white_last_use : !state.white_last_use;

        // Allow the move if the current player was the last to play white and has done so less than twice consecutively,
        // or if it has not been played by the other player in the previous turn.
        return (is_last_white_player && state.white_consecutive_last_use < 2) || state.white_consecutive_last_use == 0;
    }

    // Determines if the current player is allowed to play the orange pawn based on the game state.
    // A player can move the orange pawn if they were the last to do so, but less than twice in a row, 
    // or if the pawn hasn't been moved by the other player in the previous turn.
    inline bool can_play_orange(const GameState &state)
    {

        // Identify who was the last to play the orange pawn.
        // True : yellow, false : red
        bool is_last_orange_player = (state.yellow_is_playing) ? state.orange_last_use : !state.orange_last_use;

        // Allow the move if the current player was the last to play orange and has done so less than twice consecutively,
        // or if it has not been played by the other player in the previous turn.
        return (is_last_orange_player && state.orange_consecutive_last_use < 2) || state.orange_consecutive_last_use == 0;
    }

    // Validates if the proposed move for the yellow pawn is an allowed move.
    inline bool is_valid_move_yellow(const GameState &state, int index)
    {

        // Check if the given index corresponds to a neighbor of the yellow pawn.
        if (NODE_NEIGHBOURS_SIZE[state.yellow_position] <= index)
            return false;

        int chosen_node = NODE_NEIGHBOURS[state.yellow_position][index];

        // Prevent placing two pawns on the same node, with an exception for node 0.
        if (
            chosen_node != 0 &&
            (state.red_position == chosen_node ||
             state.black_position == chosen_node ||
             state.white_position == chosen_node ||
             state.orange_position == chosen_node))
            return false;
        
        // Ensure the move adheres to the rules regarding the connection of colors.
        // No tile or tile with tile's corresponding pawn in the neighborhood of chosen_node.
        if (!(
                (1 << chosen_node) &
                (~state.red_colors | BIT_NODE_NEIGHBOURS[state.red_position] | BIT_NODE_NEIGHBOURS[state.orange_position]) &
                (~state.black_colors | BIT_NODE_NEIGHBOURS[state.black_position]) &
                (~state.white_colors | BIT_NODE_NEIGHBOURS[state.white_position])))
            return false;

        return true;
    }

    // Validates if the proposed move for the yellow pawn is an allowed move.
    inline bool is_valid_move_red(const GameState &state, int index)
    {

        // Check if the given index corresponds to a neighbor of the red pawn.
        if (NODE_NEIGHBOURS_SIZE[state.red_position] <= index)
            return false;

        int chosen_node = NODE_NEIGHBOURS[state.red_position][index];

        // Prevent placing two pawns on the same node, with an exception for node 0.
        if (
            chosen_node != 0 &&
            (state.yellow_position == chosen_node ||
             state.black_position == chosen_node ||
             state.white_position == chosen_node ||
             state.orange_position == chosen_node))
            return false;
        
        // Ensure the move adheres to the rules regarding the connection of colors.
        // No tile or tile with tile's corresponding pawn in the neighborhood of chosen_node.
        if (!(
                (1 << chosen_node) &
                (~state.yellow_colors | BIT_NODE_NEIGHBOURS[state.yellow_position] | BIT_NODE_NEIGHBOURS[state.orange_position]) &
                (~state.black_colors | BIT_NODE_NEIGHBOURS[state.black_position]) &
                (~state.white_colors | BIT_NODE_NEIGHBOURS[state.white_position])))
            return false;

        return true;
    }

    // Validates if the proposed move for the black pawn is allowed, considering the right to play this pawn has been established.
    inline bool is_valid_move_black(const GameState &state, int index)
    {

        // Check if the given index corresponds to a neighbor of the black pawn.
        if (NODE_NEIGHBOURS_SIZE[state.black_position] <= index)
            return false;

        int chosen_node = NODE_NEIGHBOURS[state.black_position][index];

        // Prevent placing two pawns on the same node and prohibit returning to node 0.
        if (chosen_node == 0 ||
            chosen_node == state.yellow_position ||
            chosen_node == state.red_position ||
            chosen_node == state.white_position ||
            chosen_node == state.orange_position)
            return false;
        // No tile on the node.
        if ((1 << chosen_node) & (state.yellow_colors | state.red_colors))
            return false;

        return true;
    }

    // Validates if the proposed move for the white pawn is allowed, considering the right to play this pawn has been established.
    inline bool is_valid_move_white(const GameState &state, int index)
    {

        // Check if the given index corresponds to a neighbor of the white pawn.
        if (NODE_NEIGHBOURS_SIZE[state.white_position] <= index)
            return false;

        int chosen_node = NODE_NEIGHBOURS[state.white_position][index];

        // Prevent placing two pawns on the same node and prohibit returning to node 0.
        if (chosen_node == 0 ||
            chosen_node == state.yellow_position ||
            chosen_node == state.red_position ||
            chosen_node == state.black_position ||
            chosen_node == state.orange_position)
            return false;
        // No tile on the node.
        if ((1 << chosen_node) & (state.yellow_colors | state.red_colors))
            return false;

        return true;
    }

    // Validates if the proposed move for the orange pawn is allowed, considering the right to play this pawn has been established.
    inline bool is_valid_move_orange(const GameState &state, int index)
    {

        // Check if the given index corresponds to a neighbor of the orange pawn.
        if (NODE_NEIGHBOURS_SIZE[state.orange_position] <= index)
            return false;

        int chosen_node = NODE_NEIGHBOURS[state.orange_position][index];

        // Prevent placing two pawns on the same node and prohibit returning to node 0.
        if (chosen_node == 0 ||
            chosen_node == state.yellow_position ||
            chosen_node == state.red_position ||
            chosen_node == state.black_position ||
            chosen_node == state.white_position)
            return false;
        
        // Ensure the move adheres to the rules regarding the connection of colors.
        // No tile or tile with tile's corresponding pawn in the neighborhood of chosen_node.
        if (!(
                (1 << chosen_node) &
                (~state.black_colors | BIT_NODE_NEIGHBOURS[state.black_position]) &
                (~state.white_colors | BIT_NODE_NEIGHBOURS[state.white_position])))
            return false;

        return true;
    }

    // Applies the legal move for the yellow pawn and returns the new game state.
    inline GameState apply_move_yellow(const GameState &state, int index)
    {
        int chosen_node = NODE_NEIGHBOURS[state.yellow_position][index];

        // Declaring variables to hold the parameters for the new state after the move.
        bool new_yellow_is_playing;
        int new_yellow_position;
        int new_red_position;
        int new_black_position;
        int new_white_position;
        int new_orange_position;
        int new_yellow_colors;
        int new_red_colors;
        int new_black_colors;
        int new_white_colors;
        bool new_black_last_use;
        bool new_white_last_use;
        bool new_orange_last_use;
        int new_black_consecutive_last_use;
        int new_white_consecutive_last_use;
        int new_orange_consecutive_last_use;

        // It's now the other player's turn, toggle the playing status.
        new_yellow_is_playing = !state.yellow_is_playing;

        // Update positions: yellow pawn moves to chosen_node; other pawns' positions remain unchanged.
        new_yellow_position = chosen_node;                                     
        new_red_position = state.red_position;
        new_black_position = state.black_position;
        new_white_position = state.white_position;
        new_orange_position = state.orange_position;

        // Update the color states by removing the tile on the chosen node if any.
        int mask = (~(1 << chosen_node));
        new_yellow_colors = mask & state.yellow_colors;
        new_red_colors = mask & state.red_colors;
        new_black_colors = mask & state.black_colors;
        new_white_colors = mask & state.white_colors;

        // Preserve the last usage status of the neutral pawns.
        new_black_last_use = state.black_last_use;
        new_white_last_use = state.white_last_use;
        new_orange_last_use = state.orange_last_use;

        // Reset the consecutive last use counter for neutral pawns if they were played by yellow on his previous turn.
        new_black_consecutive_last_use = (state.black_last_use) ? 0 : state.black_consecutive_last_use; 
        new_white_consecutive_last_use = (state.white_last_use) ? 0 : state.white_consecutive_last_use;
        new_orange_consecutive_last_use = (state.orange_last_use) ? 0 : state.orange_consecutive_last_use;

        // Return the new game state with all the updated parameters.
        return {
            new_yellow_is_playing,
            new_yellow_position,
            new_red_position,
            new_black_position,
            new_white_position,
            new_orange_position,
            new_yellow_colors,
            new_red_colors,
            new_black_colors,
            new_white_colors,
            new_black_last_use,
            new_white_last_use,
            new_orange_last_use,
            new_black_consecutive_last_use,
            new_white_consecutive_last_use,
            new_orange_consecutive_last_use
        };
    }

    // Applies the legal move for the yellow pawn and returns the new game state.
    inline GameState apply_move_red(const GameState &state, int index)
    {
        int chosen_node = NODE_NEIGHBOURS[state.red_position][index];

        // Declaring variables to hold the parameters for the new state after the move.
        bool new_yellow_is_playing;
        int new_yellow_position;
        int new_red_position;
        int new_black_position;
        int new_white_position;
        int new_orange_position;
        int new_yellow_colors;
        int new_red_colors;
        int new_black_colors;
        int new_white_colors;
        bool new_black_last_use;
        bool new_white_last_use;
        bool new_orange_last_use;
        int new_black_consecutive_last_use;
        int new_white_consecutive_last_use;
        int new_orange_consecutive_last_use;

        // It's now the other player's turn, toggle the playing status.
        new_yellow_is_playing = !state.yellow_is_playing;

        // Update positions: red pawn moves to other_node; other pawns' positions remain unchanged.
        new_yellow_position = state.yellow_position;
        new_red_position = chosen_node;
        new_black_position = state.black_position;
        new_white_position = state.white_position;
        new_orange_position = state.orange_position;

        // Update the color states by removing the tile on the chosen node if any.
        int mask = (~(1 << chosen_node));
        new_yellow_colors = mask & state.yellow_colors;
        new_red_colors = mask & state.red_colors;
        new_black_colors = mask & state.black_colors;
        new_white_colors = mask & state.white_colors;

        // Preserve the last usage status of the neutral pawns.
        new_black_last_use = state.black_last_use;
        new_white_last_use = state.white_last_use;
        new_orange_last_use = state.orange_last_use;

        // Reset the consecutive last use counter for neutral pawns if they were played by red on his previous turn.
        new_black_consecutive_last_use = (!state.black_last_use) ? 0 : state.black_consecutive_last_use;
        new_white_consecutive_last_use = (!state.white_last_use) ? 0 : state.white_consecutive_last_use; 
        new_orange_consecutive_last_use = (!state.orange_last_use) ? 0 : state.orange_consecutive_last_use;

        // Return the new game state with all the updated parameters.
        return {
            new_yellow_is_playing,
            new_yellow_position,
            new_red_position,
            new_black_position,
            new_white_position,
            new_orange_position,
            new_yellow_colors,
            new_red_colors,
            new_black_colors,
            new_white_colors,
            new_black_last_use,
            new_white_last_use,
            new_orange_last_use,
            new_black_consecutive_last_use,
            new_white_consecutive_last_use,
            new_orange_consecutive_last_use
        };
    }

    // Applies the legal move for the black pawn and returns the new game state.
    inline GameState apply_move_black(const GameState &state, int index)
    {
        int chosen_node = NODE_NEIGHBOURS[state.black_position][index];

        // Declaring variables to hold the parameters for the new state after the move.
        bool new_yellow_is_playing;
        int new_yellow_position;
        int new_red_position;
        int new_black_position;
        int new_white_position;
        int new_orange_position;
        int new_yellow_colors;
        int new_red_colors;
        int new_black_colors;
        int new_white_colors;
        bool new_black_last_use;
        bool new_white_last_use;
        bool new_orange_last_use;
        int new_black_consecutive_last_use;
        int new_white_consecutive_last_use;
        int new_orange_consecutive_last_use;

        // It's now the other player's turn, toggle the playing status.
        new_yellow_is_playing = !state.yellow_is_playing;

        // Update positions: black pawn moves to other_node; other pawns' positions remain unchanged.
        new_yellow_position = state.yellow_position;
        new_red_position = state.red_position;
        new_black_position = chosen_node;
        new_white_position = state.white_position;
        new_orange_position = state.orange_position;

        // The black pawn cannot remove tiles so no update on the tiles.
        new_yellow_colors = state.yellow_colors;
        new_red_colors = state.red_colors;
        new_black_colors = state.black_colors;
        new_white_colors = state.white_colors;

        // The black pawn is being played by the current player.
        new_black_last_use = state.yellow_is_playing;

        // No change in the last usage status of the white and orange pawns.
        new_white_last_use = state.white_last_use;
        new_orange_last_use = state.orange_last_use;

        // Increase the counter for how many consecutive times the black pawn has been used.
        new_black_consecutive_last_use = state.black_consecutive_last_use + 1;

        // If the white or orange pawn was last played by the same player who just played the black pawn, 
        // reset their consecutive usage counters. Otherwise, the counters remain unchanged.
        new_white_consecutive_last_use =
            (state.white_last_use == state.yellow_is_playing) ? 0 : state.white_consecutive_last_use;
        new_orange_consecutive_last_use =
            (state.orange_last_use == state.yellow_is_playing) ? 0 : state.orange_consecutive_last_use;

        // Return the new game state with all the updated parameters.
        return {
            new_yellow_is_playing,
            new_yellow_position,
            new_red_position,
            new_black_position,
            new_white_position,
            new_orange_position,
            new_yellow_colors,
            new_red_colors,
            new_black_colors,
            new_white_colors,
            new_black_last_use,
            new_white_last_use,
            new_orange_last_use,
            new_black_consecutive_last_use,
            new_white_consecutive_last_use,
            new_orange_consecutive_last_use
        };
    }


    // Applies the legal move for the white pawn and returns the new game state.
    inline GameState apply_move_white(const GameState &state, int index)
    {
        int chosen_node = NODE_NEIGHBOURS[state.white_position][index];

        // Declaring variables to hold the parameters for the new state after the move.
        bool new_yellow_is_playing;
        int new_yellow_position;
        int new_red_position;
        int new_black_position;
        int new_white_position;
        int new_orange_position;
        int new_yellow_colors;
        int new_red_colors;
        int new_black_colors;
        int new_white_colors;
        bool new_black_last_use;
        bool new_white_last_use;
        bool new_orange_last_use;
        int new_black_consecutive_last_use;
        int new_white_consecutive_last_use;
        int new_orange_consecutive_last_use;

        // It's now the other player's turn, toggle the playing status.
        new_yellow_is_playing = !state.yellow_is_playing;

        // Update positions: red pawn moves to other_node; other pawns' positions remain unchanged.
        new_yellow_position = state.yellow_position;
        new_red_position = state.red_position;
        new_black_position = state.black_position;
        new_white_position = chosen_node;
        new_orange_position = state.orange_position;

        // The black pawn cannot remove tiles so no update on the tiles.
        new_yellow_colors = state.yellow_colors;
        new_red_colors = state.red_colors;
        new_black_colors = state.black_colors;
        new_white_colors = state.white_colors;

        // The white pawn is being played by the current player.
        new_white_last_use = state.yellow_is_playing;

        // No change in the last usage status of the black and orange pawns.
        new_black_last_use = state.black_last_use; 
        new_orange_last_use = state.orange_last_use;

        // Increase the counter for how many consecutive times the white pawn has been used.
        new_white_consecutive_last_use = state.white_consecutive_last_use + 1;

        // If the black or orange pawn was last played by the same player who just played the white pawn, 
        // reset their consecutive usage counters. Otherwise, the counters remain unchanged.
        new_black_consecutive_last_use =
            (state.black_last_use == state.yellow_is_playing) ? 0 : state.black_consecutive_last_use; 
        new_orange_consecutive_last_use =
            (state.orange_last_use == state.yellow_is_playing) ? 0 : state.orange_consecutive_last_use;

        // Return the new game state with all the updated parameters.
        return {
            new_yellow_is_playing,
            new_yellow_position,
            new_red_position,
            new_black_position,
            new_white_position,
            new_orange_position,
            new_yellow_colors,
            new_red_colors,
            new_black_colors,
            new_white_colors,
            new_black_last_use,
            new_white_last_use,
            new_orange_last_use,
            new_black_consecutive_last_use,
            new_white_consecutive_last_use,
            new_orange_consecutive_last_use
        };
    }

    // Applies the legal move for the orange pawn and returns the new game state.
    inline GameState apply_move_orange(const GameState &state, int index)
    {
        int chosen_node = NODE_NEIGHBOURS[state.orange_position][index];

        // Declaring variables to hold the parameters for the new state after the move.
        bool new_yellow_is_playing;
        int new_yellow_position;
        int new_red_position;
        int new_black_position;
        int new_white_position;
        int new_orange_position;
        int new_yellow_colors;
        int new_red_colors;
        int new_black_colors;
        int new_white_colors;
        bool new_black_last_use;
        bool new_white_last_use;
        bool new_orange_last_use;
        int new_black_consecutive_last_use;
        int new_white_consecutive_last_use;
        int new_orange_consecutive_last_use;

        // It's now the other player's turn, toggle the playing status.
        new_yellow_is_playing = !state.yellow_is_playing;

        // Update positions: red pawn moves to other_node; other pawns' positions remain unchanged.
        new_yellow_position = state.yellow_position;
        new_red_position = state.red_position;
        new_black_position = state.black_position;
        new_white_position = state.white_position; 
        new_orange_position = chosen_node;

        // Update the color states by removing the tile on the chosen node if any.
        int mask = ~(1 << chosen_node);
        new_yellow_colors = state.yellow_colors & mask;
        new_red_colors = state.red_colors & mask;
        new_black_colors = state.black_colors & mask;
        new_white_colors = state.white_colors & mask;

        // The orange pawn is being played by the current player.
        new_orange_last_use = state.yellow_is_playing;

        // No change in the last usage status of the black and white pawns.
        new_black_last_use = state.black_last_use;
        new_white_last_use = state.white_last_use; 

        // Increase the counter for how many consecutive times the orange pawn has been used.
        new_orange_consecutive_last_use = state.orange_consecutive_last_use + 1;

        // If the black or white pawn was last played by the same player who just played the orange pawn, 
        // reset their consecutive usage counters. Otherwise, the counters remain unchanged.
        new_black_consecutive_last_use =
            (state.black_last_use == state.yellow_is_playing) ? 0 : state.black_consecutive_last_use; 
        new_white_consecutive_last_use = 
            (state.white_last_use == state.yellow_is_playing) ? 0 : state.white_consecutive_last_use; 

        // Return the new game state with all the updated parameters.
        return {
            new_yellow_is_playing,
            new_yellow_position,
            new_red_position,
            new_black_position,
            new_white_position,
            new_orange_position,
            new_yellow_colors,
            new_red_colors,
            new_black_colors,
            new_white_colors,
            new_black_last_use,
            new_white_last_use,
            new_orange_last_use,
            new_black_consecutive_last_use,
            new_white_consecutive_last_use,
            new_orange_consecutive_last_use
        };
    }

    // This function handles the scenario when the current player cannot make any legal moves.
    inline GameState no_move(const GameState &state)
    {
        
        // Declaring variables to hold the parameters for the new state after applying the no-move rule.
        bool new_yellow_is_playing;
        int new_yellow_position;
        int new_red_position;
        int new_black_position;
        int new_white_position;
        int new_orange_position;
        int new_yellow_colors;
        int new_red_colors;
        int new_black_colors;
        int new_white_colors;
        bool new_black_last_use;
        bool new_white_last_use;
        bool new_orange_last_use;
        int new_black_consecutive_last_use;
        int new_white_consecutive_last_use;
        int new_orange_consecutive_last_use;

        // It's now the other player's turn, toggle the playing status.
        new_yellow_is_playing = !state.yellow_is_playing;

        // Maintains the current positions of the neutral pawns as no move has been made.
        new_black_position = state.black_position;
        new_white_position = state.white_position;
        new_orange_position = state.orange_position;

        // Keeps the tiles unchanged.
        new_yellow_colors = state.yellow_colors;
        new_red_colors = state.red_colors;
        new_black_colors = state.black_colors;
        new_white_colors = state.white_colors;

        // If the current player is yellow, put the yellow pawn on the central node and reset the consecutive use counters.
        // Otherwise, do the same for the red player.
        if (state.yellow_is_playing)
        {
            // Update pawn positions
            new_yellow_position = 0;
            new_red_position = state.red_position;

            // Maintain the last use status of neutral pawns.
            new_black_last_use = state.black_last_use;
            new_white_last_use = state.white_last_use;
            new_orange_last_use = state.orange_last_use;

            // Reset the consecutive use counters for neutral pawns if they were last used by the current player.
            new_black_consecutive_last_use = (state.black_last_use) ? 0 : state.black_consecutive_last_use;
            new_white_consecutive_last_use = (state.white_last_use) ? 0 : state.white_consecutive_last_use;
            new_orange_consecutive_last_use = (state.orange_last_use) ? 0 : state.orange_consecutive_last_use;
        }
        else
        {
            // Update pawn positions
            new_yellow_position = state.yellow_position;
            new_red_position = 0;

            // Maintain the last use status of neutral pawns.
            new_black_last_use = state.black_last_use;
            new_white_last_use = state.white_last_use;
            new_orange_last_use = state.orange_last_use;

            // Reset the consecutive use counters for neutral pawns if they were last used by the current player.
            new_black_consecutive_last_use = (!state.black_last_use) ? 0 : state.black_consecutive_last_use;
            new_white_consecutive_last_use = (!state.white_last_use) ? 0 : state.white_consecutive_last_use;
            new_orange_consecutive_last_use = (!state.orange_last_use) ? 0 : state.orange_consecutive_last_use;
        }

        // Return the new game state with all the updated parameters.
        return {
            new_yellow_is_playing,
            new_yellow_position,
            new_red_position,
            new_black_position,
            new_white_position,
            new_orange_position,
            new_yellow_colors,
            new_red_colors,
            new_black_colors,
            new_white_colors,
            new_black_last_use,
            new_white_last_use,
            new_orange_last_use,
            new_black_consecutive_last_use,
            new_white_consecutive_last_use,
            new_orange_consecutive_last_use
        };
    }

    // This function checks if there is a winner in the given state.
    inline bool exists_winner(const GameState &state)
    {
        // A player wins if their pawn is on the outter pentagone of the the board (node 16 to 20).
        if (16 <= state.yellow_position && state.yellow_position <= 20)
        {
            // Yellow win.
            return true;
        }
        else if (16 <= state.red_position && state.red_position <= 20)
        {
            // Red win.
            return true;
        }
        else
        {
            return false;
        }
    }
}
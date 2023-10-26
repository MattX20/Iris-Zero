import numpy as np

from iris_python_code.py_game.const.board_constants import *
from iris_python_code.py_game.game.utils import generate_random_board


# Bitfield version of NODE_NEIGHBOURS.
bit_node_neighbours = tuple(
    [
        np.intc(np.sum([1 << v for v in NODE_NEIGHBOURS[k]])) for k in range(NB_REAL_NODE)
    ]
)

# This class represents completely a game state (redundant with the c++ implementation, to be modified).
class GameState:
    def __init__(self): 

        # Boolean flag indicating the current player's turn: 'true' for yellow, 'false' for red.
        self.yellow_is_playing = True

        # Positions of the pawns on the board. Each 'position' corresponds to the node index
        # where the pawn of the respective color is located (initially on the central node).
        self.yellow_position = np.intc(0)
        self.red_position = np.intc(0)
        self.black_position = np.intc(0)
        self.white_position = np.intc(0)
        self.orange_position = np.intc(0)

        # Bitfields representing the presence of the corresponding color on the node's tiles.
        # If the k-th bit is set, it indicates that a tile holding the respective color is
        # present on the k-th node.
        self.yellow_colors, self.red_colors, self.black_colors, self.white_colors = generate_random_board()

        # Flags representing the last usage of 'neutral' pawns (black, white, and orange).
        # A 'true' value indicates the yellow player was the last to use the pawn; 'false' indicates the red player.
        # Initially set to true.
        self.black_last_use = True
        self.white_last_use = True  
        self.orange_last_use = True 

        # Count of consecutive turns each 'neutral' pawn has been used by the same player.
        # Initially set to 0.
        self.black_count_consecutive_use = np.intc(0)
        self.white_count_consecutive_use = np.intc(0)
        self.orange_count_consecutive_use = np.intc(0)

    def to_tuple(self):
        """return a tuple with the values of the attributes of this gamestate."""
        return (
            self.yellow_is_playing,
            self.yellow_position,
            self.red_position,
            self.black_position,
            self.white_position,
            self.orange_position,
            self.yellow_colors,
            self.red_colors,
            self.black_colors,
            self.white_colors,
            self.black_last_use,
            self.white_last_use,
            self.orange_last_use,
            self.black_count_consecutive_use,
            self.white_count_consecutive_use,
            self.orange_count_consecutive_use
        )

    def is_valid_move(self, moved_pawn, chosen_node):
        """Check if a move is legal given a moved pawn (0: player's pawn, 1: black pawn, 2: white pawn, 3: orange pawn)
        and node the pawn moves to."""

        # Main pawn is played.
        if moved_pawn == 0:

            # Yellow is playing.
            if self.yellow_is_playing:

                # Check if the chosen_node is in the neighborhood of the main pawn's position.
                if not (bit_node_neighbours[self.yellow_position] & (1 << chosen_node)):
                    return False
                
                # Prevent placing two pawns on the same node, with an exception for node 0.
                if chosen_node != 0:
                    if (self.red_position == chosen_node or self.black_position == chosen_node or self.white_position == chosen_node or self.orange_position == chosen_node):
                        return False
                
                # Ensure the move adheres to the rules regarding the connection of colors.
                # No tile or tile with tile's corresponding pawn in the neighborhood of chosen_node.
                if not (
                    (1 << chosen_node)
                    & (~self.red_colors | bit_node_neighbours[self.red_position] | bit_node_neighbours[self.orange_position])
                    & (~self.black_colors | bit_node_neighbours[self.black_position])
                    & (~self.white_colors | bit_node_neighbours[self.white_position])
                ):
                    return False
            
            # Red is playing.
            else:

                # Check if the chosen_node is in the neighborhood of the main pawn's position.
                if not (bit_node_neighbours[self.red_position] & 1 << chosen_node):
                    return False
                
                # Prevent placing two pawns on the same node, with an exception for node 0.
                if chosen_node != 0:
                    if (self.yellow_position == chosen_node or self.black_position == chosen_node or self.white_position == chosen_node or self.orange_position == chosen_node):
                        return False
                
                # Ensure the move adheres to the rules regarding the connection of colors.
                # No tile or tile with tile's corresponding pawn in the neighborhood of chosen_node.
                if not (
                    (1 << chosen_node)
                    & (~self.yellow_colors | bit_node_neighbours[self.yellow_position] | bit_node_neighbours[self.orange_position])
                    & (~self.black_colors | bit_node_neighbours[self.black_position])
                    & (~self.white_colors | bit_node_neighbours[self.white_position])
                ):
                    return False
                
        # Black pawn is played.
        elif moved_pawn == 1:

            # Allow the move if the current player was the last to play black and has done so less than twice consecutively,
            # or if it has not been played by the other player in the previous turn.
            if self.yellow_is_playing == self.black_last_use:
                if self.black_count_consecutive_use >= 2:
                    return False
            elif self.black_count_consecutive_use > 0:
                return False
            
            # Check if the chosen_node is in the neighborhood of the black pawn's position.
            if not (bit_node_neighbours[self.black_position] & 1 << chosen_node):
                return False
            
            # Prevent placing two pawns on the same node and prohibit returning to node 0.
            if chosen_node == 0:
                return False
            elif (self.yellow_position == chosen_node or self.red_position == chosen_node or self.white_position == chosen_node or self.orange_position == chosen_node):
                return False
            
            # No tile on the node.
            if (1 << chosen_node) & (self.yellow_colors | self.red_colors):
                return False
        
        # White pawn is played.
        elif moved_pawn == 2:

            # Allow the move if the current player was the last to play white and has done so less than twice consecutively,
            # or if it has not been played by the other player in the previous turn.
            if self.yellow_is_playing == self.white_last_use:
                if self.white_count_consecutive_use >= 2:
                    return False
            elif self.white_count_consecutive_use > 0:
                return False
            
            # Check if the chosen_node is in the neighborhood of the white pawn's position.
            if not (bit_node_neighbours[self.white_position] & 1 << chosen_node):
                return False
            
            # Prevent placing two pawns on the same node and prohibit returning to node 0.
            if chosen_node == 0:
                return False
            elif (self.yellow_position == chosen_node or self.red_position == chosen_node or self.black_position == chosen_node or self.orange_position == chosen_node):
                return False
            
            # No tile on the node.
            if (1 << chosen_node) & (self.yellow_colors | self.red_colors):
                return False
        
        # Orange pawn is played.
        else:

            # Allow the move if the current player was the last to play orange and has done so less than twice consecutively,
            # or if it has not been played by the other player in the previous turn.
            if self.yellow_is_playing == self.orange_last_use:
                if self.orange_count_consecutive_use >= 2:
                    return False
            elif self.orange_count_consecutive_use > 0:
                return False
            
            # Check if the chosen_node is in the neighborhood of the orange pawn's position.
            if not (bit_node_neighbours[self.orange_position] & 1 << chosen_node):
                return False
            
            # Prevent placing two pawns on the same node and prohibit returning to node 0.
            if chosen_node == 0:
                return False
            elif (self.yellow_position == chosen_node or self.red_position == chosen_node or self.black_position == chosen_node or self.white_position == chosen_node):
                return False
            
            # Ensure the move adheres to the rules regarding the connection of colors.
            # No tile or tile with tile's corresponding pawn in the neighborhood of chosen_node.
            if not (
                (1 << chosen_node)
                & (~self.black_colors | bit_node_neighbours[self.black_position])
                & (~self.white_colors | bit_node_neighbours[self.white_position])
            ):
                return False
        return True

    def exists_move(self):
        """Check if there is a legal move from the current gamestate."""
        if self.yellow_is_playing:
            for k in NODE_NEIGHBOURS[self.yellow_position]:
                if self.is_valid_move(0, k):
                    return True
        else:
            for k in NODE_NEIGHBOURS[self.red_position]:
                if self.is_valid_move(0, k):
                    return True

        for k in NODE_NEIGHBOURS[self.black_position]:
            if self.is_valid_move(1, k):
                return True

        for k in NODE_NEIGHBOURS[self.white_position]:
            if self.is_valid_move(2, k):
                return True

        for k in NODE_NEIGHBOURS[self.orange_position]:
            if self.is_valid_move(3, k):
                return True

        return False

    def no_valid_move(self):
        """Put the curernt player's pawn in the center and pass the turn, assuming there is no legal move possible."""

        # Yellow is playing.
        if self.yellow_is_playing:

            # Reset the consecutive use counters for neutral pawns if they were last used by Yellow.
            if self.black_last_use:
                self.black_count_consecutive_use = 0
            if self.white_last_use:
                self.white_count_consecutive_use = 0
            if self.orange_last_use:
                self.orange_count_consecutive_use = 0
            
            # Yellow pawn moved to the central node.
            self.yellow_position = 0
        
        # Red is playing.
        else:

            # Reset the consecutive use counters for neutral pawns if they were last used by Red.
            if not self.black_last_use:
                self.black_count_consecutive_use = 0
            if not self.white_last_use:
                self.white_count_consecutive_use = 0
            if not self.orange_last_use:
                self.orange_count_consecutive_use = 0

            # Red pawn moved to the central node.
            self.red_position = 0

        # It's now the other player's turn, toggle the playing status.
        self.yellow_is_playing = not self.yellow_is_playing

    def apply_move(self, moved_pawn, chosen_node):
        """Apply a move assuming it is legal, return true if there is a victory, else false."""

        # Main pawn is played.
        if moved_pawn == 0:

            # Yellow is playing.
            if self.yellow_is_playing:
                
                # The yellow pawn is moved to its new position.
                self.yellow_position = chosen_node 

                # Reset black use counter if Yellow is the last user.
                if self.black_last_use:
                    self.black_count_consecutive_use = 0 

                # Reset white use counter if Yellow is the last user. 
                if self.white_last_use:
                    self.white_count_consecutive_use = 0

                # Reset orange use counter if Yellow is the last user.
                if self.orange_last_use:
                    self.orange_count_consecutive_use = 0

            # Red is playing.
            else:

                # The red pawn is moved to its new position.
                self.red_position = chosen_node

                # Reset black use counter if Red is the last user.
                if not self.black_last_use:
                    self.black_count_consecutive_use = 0

                # Reset white use counter if Red is the last user. 
                if not self.white_last_use:
                    self.white_count_consecutive_use = 0
                
                # Reset orange use counter if Red is the last user.
                if not self.orange_last_use:
                    self.orange_count_consecutive_use = 0

            # Update the color states by removing the tile on the chosen node if any.
            mask = ~(1 << chosen_node)
            self.yellow_colors = mask & self.yellow_colors 
            self.red_colors = mask & self.red_colors
            self.black_colors = mask & self.black_colors
            self.white_colors = mask & self.white_colors

            # It's now the other player's turn, toggle the playing status.
            self.yellow_is_playing = not self.yellow_is_playing

            # Check if yellow has won.
            return 16 <= chosen_node and chosen_node <= 20

        # Black pawn is played.
        elif moved_pawn == 1:

            # Played by Yellow.
            if self.yellow_is_playing: 

                # Update last use status.
                self.black_last_use = True

                # Increase consecutive last use counter.
                self.black_count_consecutive_use += 1

                # If the white or orange pawn was last played by Yellow, 
                # reset their consecutive usage counters. Otherwise, the counters remain unchanged.
                if self.white_last_use:
                    self.white_count_consecutive_use = 0
                if self.orange_last_use:
                    self.orange_count_consecutive_use = 0
            
            # Played by Red.
            else: 

                # Update last use status.
                self.black_last_use = False 

                # Increase consecutive last use counter.
                self.black_count_consecutive_use += 1

                # If the white or orange pawn was last played by Red, 
                # reset their consecutive usage counters. Otherwise, the counters remain unchanged.
                if not self.white_last_use:
                    self.white_count_consecutive_use = 0
                if not self.orange_last_use:
                    self.orange_count_consecutive_use = 0

            # The black pawn is moved to its new position.
            self.black_position = chosen_node

            # It's now the other player's turn, toggle the playing status.
            self.yellow_is_playing = not self.yellow_is_playing

            # No victory since a neutral pawn has been played.
            return False
        
        # White pawn is played.
        elif moved_pawn == 2:

            # Played by Yellow.
            if self.yellow_is_playing:

                # Update last use status.
                self.white_last_use = True

                # Increase consecutive last use counter.
                self.white_count_consecutive_use += 1

                # If the black or orange pawn was last played by Yellow, 
                # reset their consecutive usage counters. Otherwise, the counters remain unchanged.
                if self.black_last_use:
                    self.black_count_consecutive_use = 0
                if self.orange_last_use:
                    self.orange_count_consecutive_use = 0

            # Played by Red.
            else:

                # Update last use status.
                self.white_last_use = False

                # Increase consecutive last use counter.
                self.white_count_consecutive_use += 1

                # If the black or orange pawn was last played by Red, 
                # reset their consecutive usage counters. Otherwise, the counters remain unchanged.
                if not self.black_last_use:
                    self.black_count_consecutive_use = 0
                if not self.orange_last_use:
                    self.orange_count_consecutive_use = 0

            # The white pawn is moved to its new position.
            self.white_position = chosen_node 

            # It's now the other player's turn, toggle the playing status.
            self.yellow_is_playing = not self.yellow_is_playing

            # No victory since a neutral pawn has been played.
            return False
        
        # Orange pawn is played.
        else :


            # Played by Yellow.
            if self.yellow_is_playing:

                # Update last use status.
                self.orange_last_use = True

                # Increase consecutive last use counter.
                self.orange_count_consecutive_use += 1

                # If the black or white pawn was last played by Yellow, 
                # reset their consecutive usage counters. Otherwise, the counters remain unchanged.
                if self.black_last_use:
                    self.black_count_consecutive_use = 0
                if self.white_last_use: 
                    self.white_count_consecutive_use = 0
            
            # Played by Red.
            else:

                # Update last use status.
                self.orange_last_use = False

                # Increase consecutive last use counter.
                self.orange_count_consecutive_use += 1

                # If the black or white pawn was last played by Red, 
                # reset their consecutive usage counters. Otherwise, the counters remain unchanged.
                if not self.black_last_use:
                    self.black_count_consecutive_use = 0
                if not self.white_last_use:
                    self.white_count_consecutive_use = 0

            # The orange pawn is moved to its new position.
            self.orange_position = chosen_node 
            
            # Update the color states by removing the tile on the chosen node if any.
            mask = ~(1 << chosen_node)
            self.yellow_colors = mask & self.yellow_colors 
            self.red_colors = mask & self.red_colors
            self.black_colors = mask & self.black_colors
            self.white_colors = mask & self.white_colors

            # It's now the other player's turn, toggle the playing status.
            self.yellow_is_playing = not self.yellow_is_playing 

            # No victory since a neutral pawn has been played.
            return False
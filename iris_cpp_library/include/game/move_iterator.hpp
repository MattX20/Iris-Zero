#pragma once

#include <iterator>
#include <utility>
#include "state.hpp"

// The 'game' namespace is used to organize all game-related components.
namespace game
{

    // The MoveGenerator class is responsible for generating all possible moves
    // from a given game state. It provides an iterator interface to iterate through
    // each possible move, encapsulating the logic for move generation and validation.
    class MoveGenerator
    {
    public:

        // The 'iterator' class nested within MoveGenerator representing a forward iterator 
        // that can traverse through all valid game moves from the current game state.
        class iterator
        {
        public:
            // Standard iterator type definitions for compatibility with C++ iterator concepts.
            using iterator_category = std::input_iterator_tag;
            using value_type = std::pair<int, GameState>;
            using difference_type = std::ptrdiff_t;
            using pointer = value_type *;
            using reference = value_type &;

            // Constructor that initializes the iterator with a game state and a starting position
            // for checking validity of following moves
            iterator(const GameState &parent, int index);

            // Classical C++ iterator methods
            reference operator*();
            pointer operator->();
            iterator &operator++();
            iterator operator++(int);
            bool operator==(const iterator &rhs) const;
            bool operator!=(const iterator &rhs) const;

        private:
            // Advances to the next valid move, skipping any invalid moves based on the game rules.
            void next_valid_move();

            // Reference to the game state from which moves are being generated.
            const GameState &parent_;

            // Current position within the sequence of all possible moves.
            int index_;

            // Flag indicating whether a valid move exists.
            bool exists_valid_move_;

            // Flags indicating whether the player has the right to play the corresponding neutral pawn.
            bool has_right_to_play_black_;
            bool has_right_to_play_white_;
            bool has_right_to_play_orange_;

            // Current move index and resulting game state pair that the iterator points to.
            value_type current_;
        };

        // Constructor to initialize move generation based on the provided game state.
        MoveGenerator(const GameState &parent);

        // Returns an iterator pointing to the first valid move.
        iterator begin() const;

        // Returns an iterator representing the end of the collection of moves.
        iterator end() const;

    private:
        // The game state for which moves are being generated.
        const GameState &parent_;
    };
}
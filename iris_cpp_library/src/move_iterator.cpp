#include "game/game_constants.hpp"
#include "game/rules.hpp"
#include "game/move_iterator.hpp"

// Implementation of the 'MoveGenerator' class, see 'include/game/move_iterator.hpp'.
namespace game
{
    MoveGenerator::iterator::iterator(const GameState &parent, int index) : parent_(parent), index_(index), exists_valid_move_(false)
    {
        // Check if the current palyer can play the neutral pawns.
        has_right_to_play_black_ = can_play_black(parent_);
        has_right_to_play_white_ = can_play_white(parent_);
        has_right_to_play_orange_ = can_play_orange(parent_);
        
        // Get the first valid move.
        next_valid_move();
    }

    MoveGenerator::iterator::reference MoveGenerator::iterator::operator*()
    {
        return current_;
    }

    MoveGenerator::iterator::pointer MoveGenerator::iterator::operator->()
    {
        return &current_;
    }

    MoveGenerator::iterator &MoveGenerator::iterator::operator++()
    {
        next_valid_move();
        return *this;
    }

    MoveGenerator::iterator MoveGenerator::iterator::operator++(int)
    {
        MoveGenerator::iterator temp = *this;
        next_valid_move();
        return temp;
    }

    bool MoveGenerator::iterator::operator==(const iterator &rhs) const
    {
        // Two iterator are equals if they have the same index (representing the same move), or if 
        // both their indexes are above the maximum number of moves.
        return index_ == rhs.index_ || (index_ >= MAX_MVTS && rhs.index_ >= MAX_MVTS) ;
    }

    bool MoveGenerator::iterator::operator!=(const iterator &rhs) const
    {
        return !(*this == rhs);
    }

    void MoveGenerator::iterator::next_valid_move()
    {
        // While there is still possibly legal move to check.
        while (index_ < MAX_MVTS)
        {               

            // Index between 0 and game::MAX_MVT_PER_PAWN means that the player pawn is being played.                  
            if (index_ < MAX_MVT_PER_PAWN)
            {
                if (parent_.yellow_is_playing)
                {

                    // Get the index of the node neighbor
                    int real_index = index_;

                    if (is_valid_move_yellow(parent_, real_index))
                    {
                        exists_valid_move_ = true;
                        current_ = std::make_pair(index_, apply_move_yellow(parent_, real_index));
                        ++index_;
                        break;
                    }
                }
                else
                {
                    int real_index = index_;

                    if (is_valid_move_red(parent_, real_index))
                    {
                        exists_valid_move_ = true;
                        current_ = std::make_pair(index_, apply_move_red(parent_, real_index));
                        ++index_;
                        break;
                    }
                }
            }
            // Index between game::MAX_MVT_PER_PAWN and 2 * game::MAX_MVT_PER_PAWN means that the black pawn is being played.
            else if (index_ < 2 * MAX_MVT_PER_PAWN)
            {
                if (has_right_to_play_black_)
                {

                    // Get the index of the node neighbor
                    int real_index = index_ - MAX_MVT_PER_PAWN;

                    if (is_valid_move_black(parent_, real_index))
                    {
                        exists_valid_move_ = true;
                        current_ = std::make_pair(index_, apply_move_black(parent_, real_index));
                        ++index_;
                        break;
                    }
                }
                else
                {
                    // If current player cannot play black, goes directly to the next pawn.
                    index_ = 2 * MAX_MVT_PER_PAWN - 1; 
                }
            }
            // Index between 2 * game::MAX_MVT_PER_PAWN and 3 * game::MAX_MVT_PER_PAWN means that the white pawn is being played.
            else if (index_ < 3 * MAX_MVT_PER_PAWN)
            {
                if (has_right_to_play_white_)
                {

                    // Get the index of the node neighbor
                    int real_index = index_ - 2 * MAX_MVT_PER_PAWN;

                    if (is_valid_move_white(parent_, real_index))
                    {
                        exists_valid_move_ = true;
                        current_ = std::make_pair(index_, apply_move_white(parent_, real_index));
                        ++index_;
                        break;
                    }
                }
                else
                {
                    // If current player cannot play white, goes directly to the next pawn.
                    index_ = 3 * MAX_MVT_PER_PAWN - 1; 
                }
            }
            // Index between 3 * game::MAX_MVT_PER_PAWN and 4 * game::MAX_MVT_PER_PAWN means that the orange pawn is being played.
            else if (index_ < 4 * MAX_MVT_PER_PAWN)
            {
                
                // Get the index of the node neighbor
                if (has_right_to_play_orange_)
                {
                    int real_index = index_ - 3 * MAX_MVT_PER_PAWN;

                    if (is_valid_move_orange(parent_, real_index))
                    {
                        exists_valid_move_ = true;
                        current_ = std::make_pair(index_, apply_move_orange(parent_, real_index));
                        ++index_;
                        break;
                    }
                }
                else
                {
                    // If current player cannot play orange, goes directly to the next pawn.
                    index_ = 4 * MAX_MVT_PER_PAWN - 1;
                }
            }
            else if (!exists_valid_move_)
            {
                current_ = std::make_pair(index_, no_move(parent_));
                exists_valid_move_ = true;
                break;
            }
            ++index_;
        }
    }

    MoveGenerator::MoveGenerator(const GameState &parent) : parent_(parent) {}

    MoveGenerator::iterator MoveGenerator::begin() const
    {
        return iterator(parent_, 0);
    }

    MoveGenerator::iterator MoveGenerator::end() const
    {
        return iterator(parent_, MAX_MVTS);
    }
}
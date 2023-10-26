import torch
from random import randint, random

from iris_python_code.py_game.const.board_constants import *
from iris_python_code.model_utils.transformations.hardcoded_tranformations import ROTATIONS, ROTATION_POLICY_TRANSFORM, SYMETRIES, SYMETRY_POLICY_TRANSFORM, NEUTRAL_POSITION_TRANSFORM, NEUTRAL_POLICY_TRANSFORM, PLAYER_POSITION_TRANSFORM


def apply_rotation(position, policy, value, yellow_is_playing, idx_rotation):
    """
    Apply a rotation given by its index to a batch of (positions, policies, values).
    """
    yellow_position = torch.argmax(position[:, :, 0], dim=1)
    red_position = torch.argmax(position[:, :, 1], dim=1)
    black_position = torch.argmax(position[:, :, 2], dim=1)
    white_position = torch.argmax(position[:, :, 3], dim=1)
    orange_position = torch.argmax(position[:, :, 4], dim=1)

    player_position = torch.where(yellow_is_playing, yellow_position, red_position)

    player_policy_transform = ROTATION_POLICY_TRANSFORM[idx_rotation, player_position]
    black_policy_transform = 10 + ROTATION_POLICY_TRANSFORM[idx_rotation, black_position]
    white_policy_transform = 20 + ROTATION_POLICY_TRANSFORM[idx_rotation, white_position]
    orange_policy_transform = 30 + ROTATION_POLICY_TRANSFORM[idx_rotation, orange_position]
    no_move_policy_transform = torch.full((position.shape[0], 1), NB_MOVE - 1)

    policy_transform = torch.cat((player_policy_transform, black_policy_transform, white_policy_transform, orange_policy_transform, no_move_policy_transform), dim=1)

    transformed_policy = torch.gather(policy, 1, policy_transform.long())

    return position[:, ROTATIONS[idx_rotation]], transformed_policy, value

def apply_symetry(position, policy, value, yellow_is_playing, idx_symetry):
    """
    Apply a symetry given by its index to a batch of (positions, policies, values).
    """
    yellow_position = torch.argmax(position[:, :, 0], dim=1)
    red_position = torch.argmax(position[:, :, 1], dim=1)
    black_position = torch.argmax(position[:, :, 2], dim=1)
    white_position = torch.argmax(position[:, :, 3], dim=1)
    orange_position = torch.argmax(position[:, :, 4], dim=1)

    player_position = torch.where(yellow_is_playing, yellow_position, red_position)

    player_policy_transform = SYMETRY_POLICY_TRANSFORM[idx_symetry, player_position]
    black_policy_transform = 10 + SYMETRY_POLICY_TRANSFORM[idx_symetry, black_position]
    white_policy_transform = 20 + SYMETRY_POLICY_TRANSFORM[idx_symetry, white_position]
    orange_policy_transform = 30 + SYMETRY_POLICY_TRANSFORM[idx_symetry, orange_position]
    no_move_policy_transform = torch.full((position.shape[0], 1), NB_MOVE - 1)

    policy_transform = torch.cat((player_policy_transform, black_policy_transform, white_policy_transform, orange_policy_transform, no_move_policy_transform), dim=1)

    transformed_policy = torch.gather(policy, 1, policy_transform.long())

    return position[:, SYMETRIES[idx_symetry]], transformed_policy, value

def apply_neutral_swap(position, policy, value): 
    """
    Apply a black-white pawn swap to a batch of (positions, policies, values).
    """
    return position[:, :, NEUTRAL_POSITION_TRANSFORM], policy[:, NEUTRAL_POLICY_TRANSFORM], value

def apply_player_swap(position, policy, value):
    """
    Apply a player pawn swap to a batch of (positions, policies, values).
    """
    position = position[:, :, PLAYER_POSITION_TRANSFORM]
    position[:, :, -1] = 1.0 - position[:, :, -1]
    return position, policy, -value

def random_transform(position, policy, value):
    """
    Apply a random transformation to a batch of (positions, policies, values).
    """
    idx_rotation = randint(0, ROTATIONS.shape[0] - 1)
    idx_symetry = randint(0, SYMETRIES.shape[0] - 1)

    yellow_is_playing = position[:, 0, -1] == 0.0
    
    position, policy, value = apply_rotation(position, policy, value, yellow_is_playing, idx_rotation)
    position, policy, value = apply_symetry(position, policy, value, yellow_is_playing, idx_symetry)
    
    if random() < 0.5 :
        position, policy, value = apply_neutral_swap(position, policy, value)
    
    if random() < 0.5 :
        position, policy, value = apply_player_swap(position, policy, value)
    
    return position, policy, value

def transform_collate_fn(batch): 
    """ Function to be used as the collate_fn argument of a pytorch DataLoader to apply a random transformation on a batch."""
    positions, policies, values = zip(*batch)
    positions = torch.stack(positions)
    policies = torch.stack(policies)
    values = torch.stack(values)

    positions, policies, values = random_transform(positions, policies, values)

    return positions, policies, values
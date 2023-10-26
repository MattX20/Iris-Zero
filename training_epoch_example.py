import sys
import os
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.optim import Adam

from iris_python_code.py_game.const.board_constants import *
from iris_python_code.model_utils.model.IrisZeroNN import IrisZero, compute_normalize_adjacency_matrix
from iris_python_code.model_utils.transformations.transformations import transform_collate_fn

# This files proposes a simple epoch training loop for the model. 
# This has to be adapted, with the user setup and configuration parameters, to work properly.

def create_model(nb_res_blocks, embedding_size) :
    """
    Instanciate an IrisZero model with a given number of res blocks and an embedding size.
    See 'iris_python_code.model_utils.model.IrisZeroNN.py'.
    """
    nb_features = NB_FEATURES
    nb_nodes = NB_REAL_NODE
    nb_moves = NB_MOVE

    # Computes the edge list representation of the board graph.
    l1 = []
    l2 = []
    for k, t in enumerate(NODE_NEIGHBOURS) :
        for i in t : 
            l1.append(k)
            l2.append(i)

    edge_index = torch.tensor([l1, l2])

    # Computes the normalized adjacency matrix of the graph, used in graph convolutions.
    normalized_adjacency_matrix = compute_normalize_adjacency_matrix(edge_index, nb_nodes)

    # Returns an instance of the IrisZero model.
    return IrisZero(nb_features, nb_nodes, nb_res_blocks, embedding_size, nb_moves, normalized_adjacency_matrix)
    
def create_optimizer(model, learning_rate = 1e-3, weight_decay=1e-4) :
    return 


def main():

    model = create_model(nb_res_blocks=5, embedding_size=64)
    # load from a previous epoch : model.load_state_dict(path_to_checkpoint)
    

    optimizer = Adam(model.parameters()) # Choose learning rate and weight decay.

    # Losses for the value and the policy head.
    criterion_value = torch.nn.MSELoss()
    criterion_policy = torch.nn.KLDivLoss(reduction="batchmean")

    running_loss = 0.0
    running_policy_loss = 0.0
    running_value_loss = 0.0

    batch_size = 128

    dataset = None # A dataset has to be generated, see the 'generate_training_sample' function in the 'iris_cpp_library/src/iris_zero.cpp' file.
    # Create a DataLoader on the dataset with data augmentation like rotations and symetries, see 'iris_python_code/model_utils/transformations/'.
    data_loader = DataLoader(dataset, batch_size=batch_size, collate_fn=transform_collate_fn)
    
    model.train()

    for batch_idx, (positions, policies, values) in enumerate(data_loader) :
        optimizer.zero_grad()

        # Forward pass.
        logit_predicted_policies, predicted_values = model(positions)
        log_predicted_policies = F.log_softmax(logit_predicted_policies, dim=1)

        # Calculate loss.
        loss_policy = criterion_policy(log_predicted_policies, policies)
        loss_value = criterion_value(predicted_values.flatten(), values)
        loss = loss_policy + loss_value

        # Backward pass.
        loss.backward()
        optimizer.step()

        # Update running loss values.
        running_loss += loss.item()
        running_policy_loss += loss_policy.item()
        running_value_loss += loss_value.item()

    print(f"Loss: {running_loss / len(data_loader)}, Policy Loss: {running_policy_loss / len(data_loader)}, Value Loss: {running_value_loss / len(data_loader)}")


if __name__ == "__main__":
    main()
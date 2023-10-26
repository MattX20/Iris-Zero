import torch
import torch.nn as nn
import torch.nn.functional as F


def compute_normalize_adjacency_matrix(edge_index, num_nodes):
    """
    This function computes the normalized adjacency matrix of a given graph (given as an edge list)
    for graph convolution.
    """
    adj_matrix = torch.zeros((num_nodes, num_nodes))
    adj_matrix[edge_index[0], edge_index[1]] = 1
    adj_matrix = adj_matrix + 2 * torch.eye(num_nodes)

    row_sum = adj_matrix.sum(1)
    inv_sqrt_row_sum = row_sum.pow(-0.5)
    inv_sqrt_row_sum[inv_sqrt_row_sum == float('inf')] = 0
    degree_matrix_inv_sqrt = torch.diag(inv_sqrt_row_sum)
    return degree_matrix_inv_sqrt @ adj_matrix @ degree_matrix_inv_sqrt

# Implementation of a graph convolution layer with a precomputed normalized adjacency matrix,
# as the graph of the board is constant.
class GCNConv(nn.Module):
    def __init__(self, input_channels, num_channels, normalized_adjacency_matrix):
        super(GCNConv, self).__init__()
        self.input_channels = input_channels
        self.num_channels = num_channels
        self.fc = nn.Linear(input_channels, num_channels)
        self.register_buffer('normalized_adjacency_matrix', normalized_adjacency_matrix)

    def forward(self, x):
        batch_size = x.size(0)
        normalized_adjacency_matrix_batched = self.normalized_adjacency_matrix.expand(batch_size, -1, -1)

        out = torch.bmm(normalized_adjacency_matrix_batched, x)
        out = self.fc(out.view(-1, self.input_channels)).view(-1, x.size(1), self.num_channels)
        return out

#######################################
#######################################
#######################################
#######################################
# The following is the implementation of alphazero, where convolutions have been replaced with graph convolutions.
# It is a residual tower, splitting into two heads: the policy and the value head.
# See the original paper for more details on the model.

class InitialBlock(nn.Module): 
    def __init__(self, input_channels ,num_channels, normalized_adjacency_matrix):
        super(InitialBlock, self).__init__()
        self.conv = GCNConv(input_channels, num_channels, normalized_adjacency_matrix)
        self.bnorm = nn.BatchNorm1d(num_channels)

    def forward(self, x):
        out = self.conv(x)
        out = self.bnorm(out.permute((0, 2, 1))).permute((0, 2, 1))
        out = F.relu(out)
        return out

class ResidualBlock(nn.Module): 
    def __init__(self, num_channels, normalized_adjacency_matrix):
        super(ResidualBlock, self).__init__()
        self.conv1 = GCNConv(num_channels, num_channels, normalized_adjacency_matrix)
        self.conv2 = GCNConv(num_channels, num_channels, normalized_adjacency_matrix)
        self.bnorm1 = nn.BatchNorm1d(num_channels)
        self.bnorm2 = nn.BatchNorm1d(num_channels)

    def forward(self, x):
        out = self.conv1(x)
        out = self.bnorm1(out.permute((0, 2, 1))).permute((0, 2, 1))
        out = F.relu(out)
        out = self.conv2(out)
        out = self.bnorm2(out.permute((0, 2, 1))).permute((0, 2, 1))
        out += x
        out = F.relu(out)
        return out

class PolicyHead(nn.Module):
    def __init__(self, num_nodes, num_channels, action_size, normalized_adjacency_matrix):
        super(PolicyHead, self).__init__()
        self.conv = GCNConv(num_channels, 2, normalized_adjacency_matrix)
        self.bnorm = nn.BatchNorm1d(2)
        self.fc = nn.Linear(2 * num_nodes, action_size)

    def forward(self, x):
        out = self.conv(x)
        out = self.bnorm(out.permute((0, 2, 1)))
        out = F.relu(out)
        out = self.fc(out.view(out.size(0), -1))
        return out

class ValueHead(nn.Module):
    def __init__(self, num_nodes, num_channels, normalized_adjacency_matrix, num_head_filters=32):
        super(ValueHead, self).__init__()
        self.conv = GCNConv(num_channels, num_head_filters, normalized_adjacency_matrix)
        self.bnorm = nn.BatchNorm1d(num_head_filters)
        self.fc1 = nn.Linear(num_nodes * num_head_filters, num_channels)
        self.fc2 = nn.Linear(num_channels, 1)

    def forward(self, x):
        out = self.conv(x)
        out = self.bnorm(out.permute((0, 2, 1)))
        out = F.relu(out)
        out = self.fc1(out.view(out.size(0), -1))
        out = F.relu(out)
        out = self.fc2(out)
        out = F.tanh(out)
        return out

class IrisZero(nn.Module):
    def __init__(self, input_channels, num_nodes, num_blocks, num_channels, action_size, normalized_adjacency_matrix):
        super(IrisZero, self).__init__()
        self.initial_block = InitialBlock(input_channels, num_channels, normalized_adjacency_matrix)
        self.res_blocks = nn.ModuleList(
            [ResidualBlock(num_channels, normalized_adjacency_matrix) for _ in range(num_blocks)]
        )
        self.policy_head = PolicyHead(num_nodes, num_channels, action_size, normalized_adjacency_matrix)
        self.value_head = ValueHead(num_nodes, num_channels, normalized_adjacency_matrix)

    def forward(self, x):
        out = self.initial_block(x)
        for res_block in self.res_blocks:
            out = res_block(out)
        policy = self.policy_head(out)
        value = self.value_head(out)
        return policy, value

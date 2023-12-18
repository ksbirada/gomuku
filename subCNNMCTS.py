# # # """
# # Implement your AI here
# # Do not change the API signatures for __init__ or __call__
# # __call__ must return a valid action
# # """
# class Submission:
#     def __init__(self, board_size, win_size):
#         ### Add any additional initiation code here
#         pass
#
#     def __call__(self, state):
#
#         ### Replace with your implementation
#         actions = state.valid_actions()
#         return actions[-1]


import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random

class Submission:
    def __init__(self, board_size, win_size):
        self.board_size = board_size
        self.win_size = win_size
        self.mcts_with_cnn = self.MCTSWithCNN(board_size, win_size)

    def __call__(self, state):
        root = self.Node(state, board_size=self.board_size, win_size=self.win_size)

        for _ in range(1000):  # Adjust the number of iterations as needed
            node = root
            while not node.state.is_game_over() and not node.children:
                node = self.mcts_with_cnn.expand(node)

            if not node.state.is_game_over():
                node = self.mcts_with_cnn.select_child(node)

            result = self.mcts_with_cnn.simulate(node.state)
            self.mcts_with_cnn.backpropagate(node, result)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.action

    class CNNModel(nn.Module):
        def __init__(self, input_channels=1, output_channels=1):
            super(Submission.CNNModel, self).__init__()
            self.conv1 = nn.Conv2d(input_channels, 64, kernel_size=3, stride=1, padding=1)
            self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
            self.fc1 = nn.Linear(128 * 5 * 5, 256)
            self.fc2 = nn.Linear(256, output_channels)

        def forward(self, x):
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            x = x.view(-1, 128 * 5 * 5)
            x = F.relu(self.fc1(x))
            x = self.fc2(x)
            return x

    class MCTSWithCNN:
        def __init__(self, board_size, win_size):
            self.board_size = board_size
            self.win_size = win_size
            self.cnn_model = Submission.CNNModel(input_channels=3)  # Adjust input_channels

        def evaluate_state(self, state):
            input_data = torch.from_numpy(state.board).float()
            input_data = input_data.unsqueeze(0)
            with torch.no_grad():
                output = self.cnn_model(input_data)

            # print("Input Shape:", input_data.shape)
            # print("Output Shape:", output.shape)

            return output

        def expand(self, node):
            actions = node.state.valid_actions()
            for action in actions:
                child_state = node.state.perform(action)
                child_node = Submission.Node(child_state, action=action, parent=node,
                                             board_size=self.board_size, win_size=self.win_size)
                node.children.append(child_node)
            return random.choice(node.children)

        # def select_child(self, node):
        #     exploration_weight = 1.0
        #     log_total_visits = np.log(sum(child.visits for child in node.children))
        #
        #     def score_function(child):
        #         if child.visits == 0:
        #             return float('inf')
        #         cnn_evaluation = self.evaluate_state(child.state)
        #         return (cnn_evaluation / child.visits) + exploration_weight * np.sqrt(log_total_visits / child.visits)
        #
        #     selected_child = max(node.children, key=score_function)
        #     return selected_child
        def select_child(self, node):
            exploration_weight = 1.0
            log_total_visits = np.log(sum(child.visits for child in node.children))

            def score_function(child):
                if child.visits == 0:
                    return float('inf')
                cnn_evaluation = self.evaluate_state(child.state)

                # Check if any element in the boolean tensor is True
                if torch.any(cnn_evaluation):
                    return (torch.sum(cnn_evaluation) / child.visits) + exploration_weight * np.sqrt(
                        log_total_visits / child.visits)
                else:
                    return 0.0  # Adjust this value based on your criteria

            selected_child = max(node.children, key=score_function)
            return selected_child

        def simulate(self, state):
            while not state.is_game_over():
                actions = state.valid_actions()
                action = random.choice(actions)
                state = state.perform(action)
            return state.current_score()

        def backpropagate(self, node, result):
            while node is not None:
                node.visits += 1
                node.value += result
                node = node.parent

    class Node:
        def __init__(self, state, action=None, parent=None, board_size=None, win_size=None):
            self.state = state
            self.action = action
            self.parent = parent
            self.children = []
            self.visits = 0
            self.value = 0
            self.board_size = board_size
            self.win_size = win_size


# Example of using the MCTS agent



# Example of using the MCTS agent
if __name__ == "__main__":
    # Create an instance of the Submission class
    # submission_agent = Submission(board_size=your_board_size, win_size=your_win_size)
    #
    # # Example of calling the agent on a Gomoku state
    # gomoku_state = your_gomoku_state  # Replace with an actual Gomoku state
    # action = submission_agent(gomoku_state)

     print(f"The selected action is:")









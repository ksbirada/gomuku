# # """
# Implement your AI here
# Do not change the API signatures for __init__ or __call__
# __call__ must return a valid action
# """
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

import numpy as np
import random

class Node:
    def __init__(self, state, action=None, parent=None, board_size=None, win_size=None):
        self.state = state
        self.action = action  # Keep track of the action that led to this state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.board_size = board_size
        self.win_size = win_size

    def select_child(self):
        if not self.children:
            raise RuntimeError("Node has no children to select from.")

        exploration_weight = 1.0  # You can adjust this parameter based on your requirements
        log_total_visits = np.log(sum(child.visits for child in self.children))

        def score_function(child):
            if child.visits == 0:
                return float('inf')  # Return positive infinity for unvisited nodes
            return (child.value / child.visits) + exploration_weight * np.sqrt(log_total_visits / child.visits)

        selected_child = max(self.children, key=score_function)

        return selected_child

    def expand(self):
        actions = self.state.valid_actions()
        for action in actions:
            child_state = self.state.perform(action)
            child_node = Node(child_state, action=action, parent=self, board_size=self.board_size, win_size=self.win_size)
            self.children.append(child_node)
        return random.choice(self.children)

    def simulate(self):
        state = self.state.copy()
        while not state.is_game_over():
            actions = state.valid_actions()
            action = random.choice(actions)
            state = state.perform(action)
        return state.current_score()

    def backpropagate(self, result):
        node = self
        while node is not None:
            node.visits += 1
            node.value += result
            node = node.parent

class Submission:
    def __init__(self, board_size, win_size):
        self.board_size = board_size
        self.win_size = win_size

    def __call__(self, state):
        root = Node(state, board_size=self.board_size, win_size=self.win_size)

        for _ in range(1000):  # Adjust the number of iterations as needed
            node = root
            while not node.state.is_game_over() and not node.children:
                node = node.expand()

            if not node.state.is_game_over():
                node = node.select_child()

            result = node.simulate()
            node.backpropagate(result)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.action

# Example of using the MCTS agent
if __name__ == "__main__":
    print()


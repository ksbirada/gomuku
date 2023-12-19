"""
Implement your AI here
Do not change the API signatures for __init__ or __call__
__call__ must return a valid action
"""

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
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.action = action
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def fully_expanded(self):
        actions = self.state.valid_actions()
        return all(child.action in actions for child in self.children)

    def select_child(self, exploration_weight=1.0):
        if not self.children:
            raise RuntimeError("Node has no children to select from.")

        log_total_visits = np.log(sum(child.visits for child in self.children))

        def uct_score(child):
            if child.visits == 0:
                return float('inf')  # Return positive infinity for unvisited nodes
            exploitation_term = child.value / child.visits
            exploration_term = exploration_weight * np.sqrt(log_total_visits / child.visits)
            return exploitation_term + exploration_term

        selected_child = max(self.children, key=uct_score)
        return selected_child

    def alpha_beta_select_child(self, alpha, beta):
        if not self.children:
            raise RuntimeError("Node has no children to select from.")

        def alpha_beta_score(child):
            if child.visits == 0:
                return float('inf')  # Return positive infinity for unvisited nodes
            exploitation_term = child.value / child.visits
            return exploitation_term

        best_child = None
        for child in self.children:
            child_score = alpha_beta_score(child)

            if child_score > beta:
                return child  # Prune the remaining children

            if child_score > alpha:
                alpha = child_score
                best_child = child

        return best_child

    def expand(self):
        actions = self.state.valid_actions()
        if not actions:
            return None  # No valid actions to expand

        action = random.choice(actions)
        child_state = self.state.perform(action)
        child_node = Node(child_state, action=action, parent=self)
        self.children.append(child_node)
        return child_node

    def backpropagate(self, result):
        node = self
        while node is not None:
            node.visits += 1
            node.value += result
            result = 1 - result  # Alternate the result for each level
            node = node.parent

class Submission:
    def __init__(self, board_size, win_size):
        self.board_size = board_size
        self.win_size = win_size
        self.exploration_weight = 1.0
        self.uct_budget = 1000

    def __call__(self, state):
        root = Node(state)

        for _ in range(self.uct_budget):
            node = self.tree_policy(root)
            reward = self.evaluate(node.state)
            self.back_update(node, reward)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.action

    def tree_policy(self, node):
        while not node.state.is_game_over():
            if not node.fully_expanded():
                return node.expand()
            elif node.children:
                node = node.alpha_beta_select_child(-float('inf'), float('inf'))
            else:
                return node.expand()  # If no children, expand
        return node

    def evaluate(self, state):
        while not state.is_game_over():
            actions = state.valid_actions()
            action = random.choice(actions)
            state = state.perform(action)
        return -state.current_score()

    def back_update(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            reward = 1 - reward  # Alternate the result for each level
            node = node.parent















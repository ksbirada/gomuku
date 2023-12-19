"""
Implement your AI here
Do not change the API signatures for __init__ or __call__
__call__ must return a valid action
"""

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

    # Checks if all possible actions from the current state have corresponding child nodes.
    def fully_expanded(self):
        actions = self.state.valid_actions()
        return all(child.action in actions for child in self.children)

    # Selects a child node based on the UCT (Upper Confidence Bound for Trees) algorithm.
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

    # Selects a child node based on the alpha-beta pruning algorithm.
    def alpha_beta_select_child(self, alpha, beta):
        if not self.children:
            raise RuntimeError("Node has no children to select from.")

        def alpha_beta_score(child):
            if child.visits == 0:
                return float('inf')
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

    #Expands the tree by adding a child node corresponding chosen valid action
    def expand(self):
        actions = self.state.valid_actions()
        if not actions:
            return None  # No valid actions to expand

        action = random.choice(actions)
        child_state = self.state.perform(action)
        child_node = Node(child_state, action=action, parent=self)
        self.children.append(child_node)
        return child_node

    # Updates the node and its ancestors with the result of a simulation.
    def backpropagate(self, result):
        node = self
        while node is not None:
            node.visits += 1
            node.value += result
            result = 1 - result
            node = node.parent

class Submission:
    # Initializes a submission with the specified board size and win size
    def __init__(self, board_size, win_size):
        self.board_size = board_size
        self.win_size = win_size
        self.exploration_weight = 1.0
        self.uct_budget = 1000

    #The main method that returns the best action based on the Monte Carlo Tree Search (MCTS) algorithm
    def __call__(self, state):
        root = Node(state)

        for _ in range(self.uct_budget):
            node = self.tree_policy(root)
            reward = self.evaluate(node.state)
            self.back_update(node, reward)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.action

    #The tree policy determines how to navigate the tree during the selection phase
    def tree_policy(self, node):
        while not node.state.is_game_over():
            if not node.fully_expanded():
                return node.expand()
            elif node.children:
                if random.random() < 0.5:  # Placeholder condition (replace with your criteria)
                    node = node.select_child()
                else:
                    node = node.alpha_beta_select_child(-float('inf'), float('inf'))
            else:
                return node.expand()  # If no children, expand
        return node

    #Evaluates the given state through simulations.
    def evaluate(self, state):
        while not state.is_game_over():
            actions = state.valid_actions()
            action = random.choice(actions)
            state = state.perform(action)
        return -state.current_score()

    #Backpropagates the result of a simulation up the tree.
    def back_update(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            reward = 1 - reward
            node = node.parent















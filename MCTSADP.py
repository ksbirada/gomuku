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
    def __init__(self, board_size, win_size, exploration_weight=1.0):
        self.board_size = board_size
        self.win_size = win_size
        self.exploration_weight = exploration_weight

    def __call__(self, state):
        root = Node(state)

        for _ in range(1000):  # Adjust the number of iterations as needed
            node = root
            while not node.state.is_game_over():
                if not node.children:
                    node = node.expand()
                    break

                node = node.select_child(exploration_weight=self.exploration_weight)

            if node is not None and not node.state.is_game_over():
                node = node.expand()

            if node is not None:
                result = self.simulate(node.state)
                node.backpropagate(result)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.action

    # def simulate(self, state):
    #     while not state.is_game_over():
    #         actions = state.valid_actions()
    #         action = random.choice(actions)
    #         state = state.perform(action)
    #     return state.current_score()
    # def simulate(self, state, move_penalty=0.1):
    #     while not state.is_game_over():
    #         actions = state.valid_actions()
    #         action = random.choice(actions)
    #         state = state.perform(action)
    #
    #         # Introduce a penalty for each move to encourage faster wins
    #         state_score = state.current_score()
    #         if state_score != 0:
    #             # If the game is already won, reduce the score
    #             return state_score - move_penalty
    #
    #     return state.current_score()

    def simulate(self, state):
        while not state.is_game_over():
            actions = state.valid_actions()
            action = self.choose_action(actions, state.current_player())
            state = state.perform(action)

        return -state.current_score()  # Reverse the sign of the score

    def choose_action(self, actions, current_player):
        # Implement your logic to choose actions during simulation
        # You might want to adjust the strategy based on the current player
        return random.choice(actions)


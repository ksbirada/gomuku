# """
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
#
import numpy as np
import gomoku as gm
import random

class Submission:
    def __init__(self, board_size, win_size):
        self.board_size = board_size
        self.win_size = win_size
        self.max_depth = 4  # Adjustable based on the complexity of the board

    def heuristic_evaluation(self, state):
        # Basic heuristic evaluation
        # Counts the difference in the number of marks for MAX and MIN players
        # More sophisticated logic should be implemented for better performance
        max_count = np.sum(state.board[gm.MAX])
        min_count = np.sum(state.board[gm.MIN])
        return max_count - min_count

    def minimax(self, state, depth, alpha, beta, is_maximizing):
        if depth == 0 or state.is_game_over():
            return self.heuristic_evaluation(state)

        if is_maximizing:
            max_eval = -np.inf
            for action in self.order_actions(state, is_maximizing):
                child = state.perform(action)
                eval = self.minimax(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = np.inf
            for action in self.order_actions(state, is_maximizing):
                child = state.perform(action)
                eval = self.minimax(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def order_actions(self, state, is_maximizing):
        # Order actions based on a simple evaluation or other criteria
        actions = state.valid_actions()
        return sorted(actions, key=lambda x: self.evaluate_action(x, state, is_maximizing))

    def evaluate_action(self, action, state, is_maximizing):
        # Simple evaluation of action's potential
        # This should be refined for a more accurate assessment
        # Placeholder logic: random evaluation
        return random.random()

    def __call__(self, state):
        # Dynamically adjust depth based on the game state
        dynamic_depth = self.adjust_depth(state)
        best_score = -np.inf
        best_action = None
        for action in self.order_actions(state, state.is_max_turn()):
            eval = self.minimax(state.perform(action), dynamic_depth - 1, -np.inf, np.inf, not state.is_max_turn())
            if eval > best_score:
                best_score = eval
                best_action = action
        return best_action

    def adjust_depth(self, state):
        # Dynamic depth adjustment based on the state of the game
        # Placeholder logic: fixed depth
        return self.max_depth

# Example usage
if __name__ == "__main__":
     # Get the AI's action for the current state
     print("no fails")


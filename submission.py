"""
Implement your AI here
Do not change the API signatures for __init__ or __call__
__call__ must return a valid action
"""

# import random
# import math
# import copy # Replace with your actual import path

# class Node:
#     def __init__(self, state, move=None, parent=None):
#         self.state = state
#         self.move = move
#         self.parent = parent
#         self.children = []
#         self.wins = 0
#         self.visits = 0
#         self.untried_moves = list(state.valid_actions())

#     def UCB1(self, explore_param=1.41):
#         if self.visits == 0:
#             return float('inf')
#         return self.wins / self.visits + explore_param * (math.sqrt(math.log(self.parent.visits) / self.visits))

#     def select_child(self):
#         return max(self.children, key=lambda child: child.UCB1())

#     def add_child(self, move, state):
#         new_child = Node(state=state, move=move, parent=self)
#         self.untried_moves.remove(move)
#         self.children.append(new_child)
#         return new_child

#     def update(self, result):
#         self.visits += 1
#         self.wins += result

# def advanced_heuristic_playout(state):
#     while not state.is_game_over():
#         possible_moves = state.valid_actions()
#         # Advanced Heuristic: Prioritize moves based on strategic importance
#         move_scores = {move: evaluate_move(state, move) for move in possible_moves}
#         chosen_move = max(move_scores, key=move_scores.get)
#         state = state.perform(chosen_move)
#     return state.current_score()

# def evaluate_move(state, move):
#     # Implement advanced move evaluation logic here
#     # This should return a score for the given move
#     # Higher score for more promising moves
#     return random.random()  # Placeholder: replace with your evaluation logic

# def MCTS(root_state, iterations=1000, max_depth=100):
#     root_node = Node(state=root_state)

#     for _ in range(iterations):
#         node = root_node
#         state = copy.deepcopy(root_state)
#         depth = 0

#         # Selection
#         while node.untried_moves and node.children:
#             node = node.select_child()
#             state = state.perform(node.move)
#             depth += 1

#         # Expansion
#         if node.untried_moves and depth < max_depth:
#             move = random.choice(node.untried_moves)
#             state = state.perform(move)
#             node = node.add_child(move, state)

#         # Simulation
#         result = advanced_heuristic_playout(copy.deepcopy(state))

#         # Backpropagation
#         while node is not None:
#             node.update(result)
#             node = node.parent

#     return sorted(root_node.children, key=lambda c: c.wins / c.visits)[-1].move

# class Submission:
#     def __init__(self, board_size, win_size):
#         self.board_size = board_size
#         self.win_size = win_size

#     def __call__(self, state):
#         return MCTS(state)

import random
import math
import copy # Replace with your actual import path

class Node:
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = list(state.valid_actions())

    def UCB1(self, explore_param=1.41):
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + explore_param * (math.sqrt(math.log(self.parent.visits) / self.visits))

    def select_child(self):
        return max(self.children, key=lambda child: child.UCB1())

    def add_child(self, move, state):
        new_child = Node(state=state, move=move, parent=self)
        self.untried_moves.remove(move)
        self.children.append(new_child)
        return new_child

    def update(self, result):
        self.visits += 1
        self.wins += result

def evaluate_move(state, move):
    score = 0
    temp_state = state.perform(move)

    # Winning Move
    if temp_state.is_game_over() and temp_state.current_score() > 0:
        return float('inf')  # Assign highest score for a winning move

    # Check for open fours, threes, etc.
    score += evaluate_pattern(temp_state, move, 'open_four')
    score += evaluate_pattern(temp_state, move, 'open_three')

    # Central control in early game
    if state.board.sum() < (state.board_size * state.board_size) / 2:
        score += central_control_score(move, state.board_size)

    return score

def evaluate_pattern(state, move, player):
    """
    Evaluate board patterns after a move for the specified player.
    """
    pattern_scores = {
        'open_four': 100,
        'open_three': 50,
        'others': 10
    }

    row, col = move
    score = 0

    # Horizontal, Vertical, Diagonal, Anti-diagonal
    directions = [0, 1, 2, 3]  # 0: horizontal, 1: vertical, 2: diagonal, 3: anti-diagonal

    for direction in directions:
        # Count stones in each direction from the move
        sequence = extract_sequence(state.corr, direction, player, row, col, state.win_size)

        # Apply scores based on identified patterns
        if is_open_four(sequence, player):
            score += pattern_scores['open_four']
        elif is_open_three(sequence, player):
            score += pattern_scores['open_three']
        else:
            score += pattern_scores['others']

    return score

# def evaluate_move(state, move):
#     current_player = state.current_player()  # Assuming this method returns MAX or MIN
#     score = evaluate_pattern(state, move, current_player)
#     # Add more scoring logic if needed
#     return score


def extract_sequence(corr, direction, player, row, col, win_size):
    sequence = []
    for d in range(-win_size + 1, win_size):
        r, c = move_in_direction(row, col, direction, d)
        if 0 <= r < corr.shape[2] and 0 <= c < corr.shape[3]:
            sequence.append(corr[direction, player, r, c])
    return sequence


def move_in_direction(row, col, direction, distance):
    if direction == 0:  # Horizontal
        return row, col + distance
    elif direction == 1:  # Vertical
        return row + distance, col
    elif direction == 2:  # Diagonal
        return row + distance, col + distance
    else:  # Anti-diagonal
        return row - distance, col + distance

def is_open_four(sequence, player):
    # Ensure that sequence is at least 5 in length
    if len(sequence) < 5:
        return False
    # An open four would have four player's stones and one empty spot in a sequence of five
    for i in range(len(sequence) - 4):
        window = sequence[i:i + 5]
        if window.count(player) == 4 and window.count(0) == 1:
            return True
    return False


def is_open_three(sequence, player):
    # Ensure that sequence is at least 5 in length
    if len(sequence) < 5:
        return False
    # An open three would have three player's stones and two empty spots in a sequence of five
    for i in range(len(sequence) - 4):
        window = sequence[i:i + 5]
        if window.count(player) == 3 and window.count(0) == 2:
            # Ensure the empty spots are not at the ends of the sequence
            if window[0] == 0 and window[4] == 0:
                continue
            return True
    return False


def get_sequence(corr, direction, player, row, col, dr, dc):
    """
    Extract a sequence of stones in a specific direction.
    """
    sequence = []
    for i in range(-4, 5):  # Check 4 spaces in each direction
        r = row + dr * i
        c = col + dc * i
        if 0 <= r < corr.shape[2] and 0 <= c < corr.shape[3]:
            sequence.append(corr[direction, player, r, c])
    return sequence


def central_control_score(move, board_size):
    center = board_size // 2
    distance_to_center = max(abs(move[0] - center), abs(move[1] - center))
    # Score decreases with distance from center; you can adjust the weight
    return (board_size - distance_to_center) / board_size


def MCTS(root_state, iterations=1000, max_depth=100):
    root_node = Node(state=root_state)

    for _ in range(iterations):
        node = root_node
        state = copy.deepcopy(root_state)
        depth = 0

        # Selection
        while node.untried_moves and node.children:
            node = node.select_child()
            state = state.perform(node.move)
            depth += 1

        # Expansion
        if node.untried_moves and depth < max_depth:
            move_scores = {move: evaluate_move(state, move) for move in node.untried_moves}
            move = max(move_scores, key=move_scores.get)
            state = state.perform(move)
            node = node.add_child(move, state)

        # Simulation
        result = advanced_heuristic_playout(copy.deepcopy(state))

        # Backpropagation
        while node is not None:
            node.update(result)
            node = node.parent

    return sorted(root_node.children, key=lambda c: c.wins / c.visits)[-1].move

def advanced_heuristic_playout(state):
    while not state.is_game_over():
        possible_moves = state.valid_actions()
        move_scores = {move: evaluate_move(state, move) for move in possible_moves}
        chosen_move = max(move_scores, key=move_scores.get)
        state = state.perform(chosen_move)
    return state.current_score()

class Submission:
    def __init__(self, board_size, win_size):
        self.board_size = board_size
        self.win_size = win_size

    def __call__(self, state):
        return MCTS(state)

# Example usage
# submission = Submission(15, 5)
# state = GomokuState.blank(15, 5)
# move = submission(state)


# class Submission:
#     def __init__(self, board_size, win_size):
#         ### Add any additional initiation code here
#         pass

#     def __call__(self, state):

#         ### Replace with your implementation
#         actions = state.valid_actions()
#         return actions[-1]
    

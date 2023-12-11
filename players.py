### Implement the player Classes Here.
# Import the other file funtions here, check this at end.
import gameuttt as game
from random import choice
import heuristics as heu


# Defining Global Variables.
# Global variables are defined in gameuttt.py

# GLOBAL VARIABLES - Defined in gameuttt.py
# global_vars = [EMPTY, X, O, T, SIZE, SIZEMINI, WINNING_POSITIONS]

EMPTY = game.global_vars[0]
X = game.global_vars[1]
O = game.global_vars[2]
T = game.global_vars[3]
SIZE = game.global_vars[4]
SIZEMINI = game.global_vars[5]
WINNING_POSITIONS = game.global_vars[6]


class UtttPlayerTemplate:
    """Template class for UTTT player classes. This is inherited by all classes."""

    def __init__(self, mysign) -> None:
        self.sign = mysign

    def get_sign(self):
        return self.sign

    def make_move(self, state):
        """Given a state, return a action that the agent will take.
          Action should be legal.
          This will be diffrent for each player,
          therefore, should be implemented in each class seperately"""
        return None


class RandomPlayer(UtttPlayerTemplate):
    """Randomly playing agent for the game."""

    def make_move(self, state):
        legal_actions = game.actions(state)
        # print("Legal Actions:",legal_actions)
        move = choice(legal_actions)
        if game.print_player_moves: print(f"Random Player made move: {move}")
        return move


class HumanPlayer(UtttPlayerTemplate):
    def make_move(self, state):
        curr_move = None
        legal_moves = game.actions(state)
        print(state)
        while curr_move == None:
            if self.sign == 'X':
                print("X", end='')
            else:
                print("O", end='')
            print(' to play.')
            print(f'Legal Moves are : {legal_moves}')
            input_move = input(
                'Enter your move as mb,r,c pair. mb is the board number, r, c are row and column index inside the mb where you want to make the move:\n')
            if input_move == '':
                print('No move was provided. Hence first move from above list was selected.')
                return legal_moves[0]
            else:
                try:
                    move = tuple(map(int, input_move.split(',')))
                except ValueError:
                    print('Enter Integer Values.')
                    continue
                if len(move) != 3:
                    print("Not a valid move.")
                    continue
                else:
                    if (move[0] < 9 and move[0] >= 0) or (move[1] < 3 and move[1] >= 0) or (
                            move[2] < 3 and move[2] >= 0):
                        curr_move = move
                    else:
                        print("Not a valid Move.")
                        continue
        return curr_move


class MinimaxPlayer(UtttPlayerTemplate):
    def __init__(self, mysign, depth_limit, heuristic):
        self.depth_limit = depth_limit
        self.sign = mysign
        self.heuristicfcn = heuristic

    def make_move(self, state):
        move = self.minimax_search(state)
        if game.print_player_moves: print(f"Minimax Player made move: {move}")
        return move

    def minimax_search(self, state):
        current_depth = 0
        value, move = self.max_value(state, current_depth)
        return move

    def max_value(self, state, current_depth):
        # Returns  (utility, move)
        if game.terminal_test(state)[0]:
            return self.heuristic(state), None
        # Check if depth limit has been reached
        if self.depth_limit == current_depth:
            return self.heuristic(state), None

        current_depth += 1
        v = float('-inf')

        for action in game.actions(state):
            result_state = game.result(state, action)
            v2, a2 = self.min_value(result_state, current_depth)
            if v2 > v:
                v, move = v2, action
        return v, move

    def min_value(self, state, current_depth):
        # Returns (utility, move)
        if game.terminal_test(state)[0]:
            return self.heuristic(state), None
        # Check if depth limit has been reached.
        if self.depth_limit == current_depth:
            return self.heuristic(state), None

        current_depth += 1
        v = float('inf')

        for action in game.actions(state):
            result_state = game.result(state, action)
            v2, a2 = self.max_value(result_state, current_depth)
            if v2 < v:
                v, move = v2, action
        return v, move

    def heuristic(self, state):
        return self.heuristicfcn(self, state)
        # """Returns the heuristic value of the given state.
        # This is the evaluation function for the state."""
        # # Check if the game is over.
        # game_over, winner = game.terminal_test(state)
        # score = 0
        # player = self.sign
        # if player == X:
        #     otherplayer = O
        # else:
        #     otherplayer = X
        #
        # if game_over:
        #     if winner == player:
        #         return 10000
        #     elif winner == otherplayer:
        #         return -10000
        #     else:
        #         return -1000
        #
        # # Game is not over.
        #
        # # SCORES FOR THE MASTER BOARD
        # master_center = 500
        # master_corner = 400
        # master_edge = 300
        #
        # # Find the number of positions on the master board that are filled. Give each of these a high score
        # for i in range(SIZEMINI):
        #     for j in range(SIZEMINI):
        #         # Checking if the current position is filled with the current player's sign.
        #         if state.master_board[i][j] == player:
        #             # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
        #             if check_if_center(i, j):
        #                 score += master_center
        #             if check_if_corner(i, j):
        #                 score += master_corner
        #             if check_if_edge(i, j):
        #                 score += master_edge
        #         elif state.master_board[i][j] == otherplayer:
        #             # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
        #             if check_if_center(i, j):
        #                 score -= master_center
        #             if check_if_corner(i, j):
        #                 score -= master_corner
        #             if check_if_edge(i, j):
        #                 score -= master_edge
        #
        # # SCORES ASSIGNED FOR POINTS ON MINI BOARDS
        # mini_center = 5
        # mini_corner = 4
        # mini_edge = 3
        #
        # possible_mb = []
        # for i in range(SIZEMINI):
        #     for j in range(SIZEMINI):
        #         if state.master_board[i][j] == EMPTY:
        #             possible_mb.append(3 * i + j)
        # for mb in possible_mb:
        #     for i in range(SIZEMINI):
        #         for j in range(SIZEMINI):
        #             if state.board_array[mb][i][j] == player:
        #                 # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
        #                 if check_if_center(i, j):
        #                     score += mini_center
        #                 if check_if_corner(i, j):
        #                     score += mini_corner
        #                 if check_if_edge(i, j):
        #                     score += mini_edge
        #
        #             elif state.board_array[mb][i][j] == otherplayer:
        #                 # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
        #                 if check_if_center(i, j):
        #                     score -= mini_center
        #                 if check_if_corner(i, j):
        #                     score -= mini_corner
        #                 if check_if_edge(i, j):
        #                     score -= mini_edge
        #
        # return score


class AlphaBetaPlayer(UtttPlayerTemplate):
    def __init__(self, mysign, depth_limit, heuristic):
        self.depth_limit = depth_limit
        self.sign = mysign
        self.heuristicfcn = heuristic

    def make_move(self, state):
        move = self.alpha_beta_search(state)
        if game.print_player_moves: print(f"AlphaBeta Player made move: {move}")
        return move

    def alpha_beta_search(self, state):
        # Returns a action that the person has to do.
        current_depth = 0
        value, move = self.max_value(state, float('-inf'), float('inf'), current_depth)
        return move

    def max_value(self, state, alpha, beta, current_depth):
        # Returns (utility, move)
        if game.terminal_test(state)[0]:
            return self.heuristic(state), None
        if self.depth_limit == current_depth:
            return self.heuristic(state), None

        current_depth += 1
        v = float('-inf')

        for action in game.actions(state):
            result_state = game.result(state, action)
            v2, a2 = self.min_value(result_state, alpha, beta, current_depth)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(self, state, alpha, beta, current_depth):
        # Returns (utility, move)
        if game.terminal_test(state)[0]:
            return self.heuristic(state), None
        if self.depth_limit == current_depth:
            return self.heuristic(state), None

        current_depth += 1
        v = float('+inf')

        for action in game.actions(state):
            result_state = game.result(state, action)
            v2, a2 = self.max_value(result_state, alpha, beta, current_depth)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    def heuristic(self, state):
        return self.heuristicfcn(self, state)
        # """Returns the heuristic value of the given state.
        # This is the evaluation function for the state."""
        # # Check if the game is over.
        # game_over, winner = game.terminal_test(state)
        # score = 0
        # player = self.sign
        # if player == X:
        #     otherplayer = O
        # else:
        #     otherplayer = X
        #
        # if game_over:
        #     if winner == player:
        #         return 10000
        #     elif winner == otherplayer:
        #         return -10000
        #     else:
        #         return -1000
        #
        # # Game is not over.
        #
        # # SCORES FOR THE MASTER BOARD
        # master_center = 500
        # master_corner = 400
        # master_edge = 300
        #
        # # Find the number of positions on the master board that are filled. Give each of these a high score
        # for i in range(SIZEMINI):
        #     for j in range(SIZEMINI):
        #         # Checking if the current position is filled with the current player's sign.
        #         if state.master_board[i][j] == player:
        #             # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
        #             if check_if_center(i, j):
        #                 score += master_center
        #             if check_if_corner(i, j):
        #                 score += master_corner
        #             if check_if_edge(i, j):
        #                 score += master_edge
        #         elif state.master_board[i][j] == otherplayer:
        #             # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
        #             if check_if_center(i, j):
        #                 score -= master_center
        #             if check_if_corner(i, j):
        #                 score -= master_corner
        #             if check_if_edge(i, j):
        #                 score -= master_edge
        #
        # # SCORES ASSIGNED FOR POINTS ON MINI BOARDS
        # mini_center = 5
        # mini_corner = 4
        # mini_edge = 3
        #
        # possible_mb = []
        # for i in range(SIZEMINI):
        #     for j in range(SIZEMINI):
        #         if state.master_board[i][j] == EMPTY:
        #             possible_mb.append(3 * i + j)
        # for mb in possible_mb:
        #     for i in range(SIZEMINI):
        #         for j in range(SIZEMINI):
        #             if state.board_array[mb][i][j] == player:
        #                 # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
        #                 if check_if_center(i, j):
        #                     score += mini_center
        #                 if check_if_corner(i, j):
        #                     score += mini_corner
        #                 if check_if_edge(i, j):
        #                     score += mini_edge
        #
        #             elif state.board_array[mb][i][j] == otherplayer:
        #                 # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
        #                 if check_if_center(i, j):
        #                     score -= mini_center
        #                 if check_if_corner(i, j):
        #                     score -= mini_corner
        #                 if check_if_edge(i, j):
        #                     score -= mini_edge
        #
        # return score


class AlphaBetaPlayerV2(UtttPlayerTemplate):
    def __init__(self, mysign, depth_limit, heuristic):
        self.depth_limit = depth_limit
        self.sign = mysign
        self.heuristicfcn = heuristic

    def make_move(self, state):
        move = self.alpha_beta_search(state)
        print(f"AlphaBetaV2 Player made move: {move}")
        return move

    def alpha_beta_search(self, state):
        # Returns a action that the person has to do.
        current_depth = 0
        value, move = self.max_value(state, float('-inf'), float('inf'), current_depth)
        return move

    def max_value(self, state, alpha, beta, current_depth):
        # Returns (utility, move)
        if game.terminal_test(state)[0]:
            return self.heuristic(state), None
        if self.depth_limit == current_depth:
            return self.heuristic(state), None

        current_depth += 1
        v = float('-inf')

        for action in game.actions(state):
            result_state = game.result(state, action)
            v2, a2 = self.min_value(result_state, alpha, beta, current_depth)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(self, state, alpha, beta, current_depth):
        # Returns (utility, move)
        if game.terminal_test(state)[0]:
            return self.heuristic(state), None
        if self.depth_limit == current_depth:
            return self.heuristic(state), None

        current_depth += 1
        v = float('+inf')

        for action in game.actions(state):
            result_state = game.result(state, action)
            v2, a2 = self.max_value(result_state, alpha, beta, current_depth)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    def heuristic(self, state):
        return self.heuristicfcn(self, state)
        # """Returns the heuristic value of the given state.
        # This is the evaluation function for the state."""
        # # Check if the game is over.
        # game_over, winner = game.terminal_test(state)
        # score = 0
        # player = self.sign
        # if player == X:
        #     otherplayer = O
        # else:
        #     otherplayer = X
        #
        # if game_over:
        #     if winner == player:
        #         return 10000
        #     elif winner == otherplayer:
        #         return -10000
        #     else:
        #         return -1000
        #
        # # Game is not over.
        #
        # # SCORES FOR THE MASTER BOARD
        # master_center = 15
        # master_corner = 13
        # master_edge = 5
        #
        # # Find the number of positions on the master board that are filled. Give each of these a high score
        # for i in range(SIZEMINI):
        #     for j in range(SIZEMINI):
        #         # Checking if the current position is filled with the current player's sign.
        #         if state.master_board[i][j] == player:
        #             # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
        #             if check_if_center(i, j):
        #                 score += master_center
        #             if check_if_corner(i, j):
        #                 score += master_corner
        #             if check_if_edge(i, j):
        #                 score += master_edge
        #         elif state.master_board[i][j] == otherplayer:
        #             # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
        #             if check_if_center(i, j):
        #                 score -= master_center
        #             if check_if_corner(i, j):
        #                 score -= master_corner
        #             if check_if_edge(i, j):
        #                 score -= master_edge
        # print("Score for Master Board: ", score)
        # # SCORES ASSIGNED FOR POINTS ON MINI BOARDS
        # mini_center = 5
        # mini_corner = 3
        # mini_edge = 0
        #
        # possible_mb = []
        # for i in range(SIZEMINI):
        #     for j in range(SIZEMINI):
        #         if state.master_board[i][j] == EMPTY:
        #             possible_mb.append(3 * i + j)
        #
        # for mb in possible_mb:
        #     for i in range(SIZEMINI):
        #         for j in range(SIZEMINI):
        #             if state.board_array[mb][i][j] == player:
        #                 # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
        #                 if check_if_center(i, j):
        #                     score += mini_center
        #                 if check_if_corner(i, j):
        #                     score += mini_corner
        #                 if check_if_edge(i, j):
        #                     score += mini_edge
        #
        #             elif state.board_array[mb][i][j] == otherplayer:
        #                 # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
        #                 if check_if_center(i, j):
        #                     score -= mini_center
        #                 if check_if_corner(i, j):
        #                     score -= mini_corner
        #                 if check_if_edge(i, j):
        #                     score -= mini_edge
        # print("Score with Mini Boards: ", score)
        #
        # # Make a function which can Check for two in a row on mini boards.
        # double_accuired = 0
        # for mb in possible_mb:
        #     for position in WINNING_POSITIONS:
        #         count = 0
        #         for pair in position:
        #             if state.board_array[mb][pair[0]][pair[1]] == player:
        #                 count += 1
        #         if count == 2:
        #             double_accuired += 1
        # score += double_accuired * 2
        # print('Score for 2 in pair accuisition on Mini Board: ', double_accuired * 2)
        #
        # # Make a function which can Check for two in a row on Master boards.
        # double_accuired_master = 0
        # for position in WINNING_POSITIONS:
        #     count = 0
        #     for pair in position:
        #         if state.master_board[pair[0]][pair[1]] == player:
        #             count += 1
        #     if count == 2:
        #         double_accuired_master += 1
        # score += double_accuired_master * 4
        # print('Score for 2 in pair accuisition on Master Board: ', double_accuired_master * 2)

        # return score


def check_if_center(i, j):
    if i == 1 and j == 1:
        return True
    else:
        return False


def check_if_corner(i, j):
    if i == 0 and j == 0:
        return True
    elif i == 0 and j == 2:
        return True
    elif i == 2 and j == 0:
        return True
    elif i == 2 and j == 2:
        return True
    else:
        return False


def check_if_edge(i, j):
    if i == 0 and j == 1:
        return True
    elif i == 1 and j == 0:
        return True
    elif i == 1 and j == 2:
        return True
    elif i == 2 and j == 1:
        return True
    else:
        return False

# Import the other file funtions here, check this at end.
import gameuttt as game
from random import choice
import heuristics as heu
import time

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
MAXSCORE = game.global_vars[7]


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


class MinimaxPlayer(UtttPlayerTemplate):
    def __init__(self, mysign, depth_limit = 4, heuristic = heu.heuristic2):
        self.depth_limit = depth_limit
        self.sign = mysign
        self.heuristicfcn = heuristic

    def make_move(self, state):
        if state.num_moves < 2:
            legal_actions = game.actions(state)
            # print("Legal Actions:",legal_actions)
            move = choice(legal_actions)
            if game.print_player_moves: print("Took Random Move: ", state.num_moves)
        else:
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


class HumanPlayer(UtttPlayerTemplate):
    def make_move(self, state):
        curr_move = None
        legal_moves = game.actions(state)
        # print(state)
        while curr_move == None:
            if self.sign == 'X':
                print("X", end='')
            else:
                print("O", end='')
            print(' to play.')
            # print("[DEBUGGING] Current Player: ", self.sign, "Current Heuristic Value: ", heu.pulkit_github(self, state))
            print(f'Legal Moves are : {legal_moves}')
            input_move = input(
                "Enter your move as mb,r,c pair. mb is the mini-board number, r, c are row and column index inside the mb where you want to make the move.\n Ex:(4,2,1) will make a move on 4ht mini-board's last row(2) and middle column(1):\n")
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


class RandomPlayer(UtttPlayerTemplate):
    """Randomly playing agent for the game."""

    def make_move(self, state):
        legal_actions = game.actions(state)
        # print("Legal Actions:",legal_actions)
        move = choice(legal_actions)
        if game.print_player_moves: print(f"Random Player made move: {move}")
        return move


class AlphaBetaPlayer(UtttPlayerTemplate):
    def __init__(self, mysign, depth_limit=4, heuristic=heu.heuristic2):
        self.depth_limit = depth_limit
        self.sign = mysign
        self.heuristicfcn = heuristic

    def make_move(self, state):
        if state.num_moves < 2:
            legal_actions = game.actions(state)
            # print("Legal Actions:",legal_actions)
            move = choice(legal_actions)
            if game.print_player_moves: print("Took Random Move: ", state.num_moves)
        else:
            move = self.alpha_beta_search(state)
        # move = self.alpha_beta_search(state)
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


class MonteCarlo(UtttPlayerTemplate):
    def __init__(self, mysign, num_tests=10):
        self.num_tests = num_tests
        self.sign = mysign

    def make_move(self, state):
        score = {}
        actions = game.actions(state)
        print("ACTIONS", actions)
        num_moves = state.num_moves
        # print(num_moves)
        action_taken = ""
        score[action_taken] = [0, 0, 0]
        t_start = time.time()

        if len(actions) > 1:
            for action in actions:
                state = game.result(state, action)
                score[action] = [0, 0, 0]
                for i in range(self.num_tests):
                    p1 = RandomPlayer(self.sign)
                    if self.sign == X:
                        p2 = RandomPlayer(O)
                    else:
                        p2 = RandomPlayer(X)

                    winner = game.monte_carlo(p1, p2, printouts=False)
                    tmp_score = score[action]
                    if winner == self.sign:
                        score[action] = [tmp_score[0] + 1, tmp_score[1], tmp_score[2]]
                    elif winner == T:
                        score[action] = [tmp_score[0], tmp_score[1], tmp_score[2] + 1]
                    else:
                        score[action] = [tmp_score[0], tmp_score[1] + 1, tmp_score[2]]

                if score[action][0] > score[action_taken][0]:
                    action_taken = action
        else:
            action_taken = actions[0]

        t_fin = time.time()

        print("Total time for move: ", t_fin - t_start, "    Average calc time per move and simulations: ", (t_fin - t_start) / len(actions))
        #
        #
        if action_taken == "":
            action_taken = choice(game.actions(state))
            # print("MADE A BIG BOOBOO")

        return action_taken

        ## MONTE CARLO PROCDESS THAT NEEDS TO HAPPEN
        # 1 - PASS THE STATE TO THE MONTE CARLO SIM
        # 2 - MONTE CARLO SIM NEEDS TO FIND THE ACTIONS
        # 3 - MONTE CARLO SIM NEEDS TO RUN TESTS
        #     - COULD RUN THE SIM IN THE

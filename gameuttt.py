# Importing libraries
import copy
from copy import deepcopy
import players
import time
import threading
import heuristics as heu

# Defining Global Variables.
EMPTY = '-'
X = 'X'
O = "O"
T = "T" # Player character if there is a Tie
SIZE = 9
SIZEMINI = 3
WINNING_POSITIONS = [((0, 0), (0, 1), (0, 2)),
                     ((1, 0), (1, 1), (1, 2)),
                     ((2, 0), (2, 1), (2, 2)),
                     ((0, 0), (1, 0), (2, 0)),
                     ((0, 1), (1, 1), (2, 1)),
                     ((0, 2), (1, 2), (2, 2)),
                     ((0, 0), (1, 1), (2, 2)),
                     ((0, 2), (1, 1), (2, 0))]

global_vars = [EMPTY, X, O, T, SIZE, SIZEMINI, WINNING_POSITIONS]

class UtttState:
    '''A class to represent a state in Uttt game.'''

    ### Board is created such that to access a element at the center of middle board. WE say [4][1][1]
    def __init__(self, currentplayer, otherplayer, last_move=None, board_array=None):
        if board_array != None:
            self.board_array = board_array
        else:
            self.board_array = [[[EMPTY] * SIZEMINI for _ in range(SIZEMINI)] for _ in range(SIZE)]
        self.current = currentplayer
        self.other = otherplayer
        self.last_move = last_move
        self.master_board = build_master(self.board_array)
        # self.heuristic = heuristic(self, currentplayer.sign)

    def __repr__(self) -> str:
        new_string = "Last Action Chosen: " + str(self.last_move) + "     Player Turn: " + str(
            self.current.get_sign()) + "\n"
        new_string += "-------------------------------------\n"
        for m in range(SIZEMINI):
            for j in range(SIZEMINI):
                new_string += "|  "
                for i in range(SIZEMINI):
                    for k in range(SIZEMINI):
                        new_string += self.board_array[i + (3 * m)][j][k] + "  "
                    new_string += "|  "
                new_string += "\n"
            new_string += "-------------------------------------\n"

        new_string += " ## MASTER BOARD ##\n"
        new_string += "-------------\n"
        for i in range(SIZEMINI):
            new_string += "|  "
            for j in range(SIZEMINI):
                new_string += self.master_board[i][j] + "  "
            new_string += "|  "
            new_string += "\n"
        new_string += "-------------\n"
        # new_string += "Current Player: " + str(self.current.get_sign()) + "    Heuristic: " + str(self.heuristic) + "\n"
        return new_string

    # def print_subboard(self, num) -> str:
    #     new_string = ""
    #     sub_board = self.board_array[num]
    #     for i in range(SIZEMINI):
    #         items = " ".join(sub_board[i])
    #         new_string += items + "\n"
    #     print(new_string)


class UtttGame:
    """A class to encapsulate the variable and methods for the Uttt game."""
    pass


def terminal_test(state):
    # INPUT: 3X3 GAME BOARD
    # OUTPUT: BOOLEAN IF GAME IS WON OR NOT, CHARACTER OF WINNING PLAYER
    return terminal_test_mini(state.master_board)


def terminal_test_mini(mini_board):
    """Terminal test for Mini Boards. Input is the 3*3 array and outputs wheather the game has ended and the character who won or T if tied."""
    for positions in WINNING_POSITIONS:
        a, b, c = positions
        if (mini_board[a[0]][a[1]] != EMPTY) and (mini_board[a[0]][a[1]] != T):
            if (mini_board[a[0]][a[1]] == mini_board[b[0]][b[1]] == mini_board[c[0]][c[1]]):
                return True, mini_board[a[0]][a[1]]
    ## It might be the case that a mini board has tied.
    ## Now check for tie. In our game Tie only happens if all the board pieces have been filed and there is yet no winner.
    for i in range(SIZEMINI):
        for j in range(SIZEMINI):
            if mini_board[i][j] == EMPTY:
                # Id any empty place is found that means we have not Tied.
                return False, None
    ## We reached here means the board is not won yet and it is a Tie.
    return True, T


def build_master(game):
    """This is time consuming funtion should be used with causion."""
    # INPUT: 9X3X3 MASTER GAME BOARD
    # OUTPUT: SMALLER 3X3 GAME BOARD REPRESENTING LARGER BOARD
    return_game = [[EMPTY] * SIZEMINI for _ in range(SIZEMINI)]
    for i in range(SIZE):
        mini_board = game[i]
        game_won, winner = terminal_test_mini(mini_board)
        if game_won:
            return_game[i // 3][i % 3] = winner
    return return_game


## Change Legal actions to account for when the selected board is full,
#  and hence the player can move anywhere on the board.
def actions(state):
    """Return a list of posible actions possible form this state(Instance of UtttState).
    Actions look like (i,x,y), where i the mini board number and x,y
    represent the row and column of the place in mini board."""
    legal_actions = []

    ## If this is the first move.
    if state.last_move == None:
        # All actions are legal.
        # mb stands for miniboard,
        for mb in range(SIZE):
            for i in range(SIZEMINI):
                for j in range(SIZEMINI):
                    legal_actions.append((mb, i, j))
    else:
        # There was some last move.
        last_mb, last_i, last_j = state.last_move
        # Find the new legal mb from last i,j.
        mb = 3 * last_i + last_j
        # We need to check that this mb is empty in the master board or else we need to give all other open boards as legal moves.
        if state.master_board[mb // 3][mb % 3] == EMPTY:
            for i in range(3):
                for j in range(3):
                    if state.board_array[mb][i][j] == EMPTY:
                        legal_actions.append((mb, i, j))
        else:
            # This is when the master_board has Tie or Has been won.
            # Add all mb to the possible boards.
            possible_mb = []
            for i in range(SIZEMINI):
                for j in range(SIZEMINI):
                    if state.master_board[i][j] == EMPTY:
                        possible_mb.append(3 * i + j)
            for mb in possible_mb:
                for i in range(SIZEMINI):
                    for j in range(SIZEMINI):
                        if state.board_array[mb][i][j] == EMPTY:
                            legal_actions.append((mb, i, j))
    return legal_actions


def result(state, action):
    """Returns the resulting state after taking the given action.
    Returns None if the action is not legal."""
    # Get the position of move from action.
    mb, i, j = action
    ## Check for legal action, by checking that the position is empty.
    if state.board_array[mb][i][j] != EMPTY:
        return None
    else:
        # New state has to be formed here.
        # Make the new Board array.
        new_board = deepcopy(state.board_array)
        new_board[mb][i][j] = state.current.sign
        new_state = UtttState(state.other, state.current, last_move=action, board_array=new_board)
        return new_state

#
# def max_value_alpha_beta(state, depth, player, alpha, beta):
#     game_over, winner = terminal_test(state)
#     if game_over or depth == 0:
#         return heuristic(state, player), None
#     val = float('-inf')
#     for a in actions(state):
#         [v2, a2] = min_value_alpha_beta(result(state, a), depth - 1, player, alpha, beta)
#         if v2 > val:
#             val, move = v2, a
#             alpha = max(alpha, val)
#         if val >= beta:
#             return val, move
#     # print("Move: ", move)
#     return val, move
#
#
# def min_value_alpha_beta(state, depth, player, alpha, beta):
#     game_over, winner = terminal_test(state)
#     if game_over or depth == 0:
#         return heuristic(state, player), None
#     val = float('inf')
#     for a in actions(state):
#         [v2, a2] = max_value_alpha_beta(result(state, a), depth - 1, player, alpha, beta)
#         if v2 < val:
#             val, move = v2, a
#             beta = min(beta, val)
#         if val <= alpha:
#             return val, move
#     return val, move


def search_test(player1, player2, num_iterations=1):
    score = [0, 0, 0]  # [player1, player2, tie]
    ts = time.time()
    for i in range(num_iterations):
        print("Iteration: ", i + 1, "/", num_iterations, "  Score: ", score, "[P1, P2, Tie]")
        winner = play_game(player1, player2)
        if winner == player1.get_sign():
            score[0] += 1
        elif winner == player2.get_sign():
            score[1] += 1
        elif winner == T:
            score[2] += 1
        else:
            raise Exception("Winner not recognized")
    t_stop = time.time()
    print("Final score: [P1, P2, Tie]", score)
    print("Computational time: ", t_stop - ts, "s    Average: ", (t_stop - ts) / num_iterations, "s")
    return score


def play_game(p1=None, p2=None):
    """Play the game with two players. Default use two humans."""
    if p1 == None:
        p1 = players.HumanPlayer(X)
    if p2 == None:
        p2 = players.HumanPlayer(O)

    s = UtttState(p1, p2)
    while True:
    # for i in range(20):
        action = p1.make_move(s)
        if action not in actions(s):
            # print("Illegal move made by X")
            # print("O wins!")
            return None
        s = result(s, action)
        print(s)
        game_over, winner = terminal_test(s)
        if game_over:
            print("Game Over")
            print("Player " + winner + " wins!")
            # print(s)
            return winner
        action = p2.make_move(s)
        if action not in actions(s):
            # print("Illegal move made by O")
            # print("O wins!")
            return None
        # print(s)
        s = result(s, action)
        print(s)
        game_over, winner = terminal_test(s)
        if game_over:
            print("Game Over")
            print("Player " + winner + " wins!")
            # print(s)
            return winner
    # print('Debug here.')
    # # print(s)
    # p1.heuristic(s)


def main():
    p1 = players.RandomPlayer(O)
    p2 = players.AlphaBetaPlayer(X, 2, heu.homemade)
    # st = UtttState(p1,p2)

    # p2.heuristic(st)

    play_game(p1, p2)

    iters = 20
    # Running multiple iterations of the alpha-beta search
    # score = search_test(p1, p2, iters)
    # print(score)
    # p1 = players.MinimaxPlayer(2, X)
    # p2 = players.RandomPlayer(O)
    # print("Running minimax search test")
    # score = search_test(p1, p2, TESTING_ITERATIONS)
    # t_stop = time.time()
    # print("Total time: ", t_stop - ts, "s")

    # TRIED TO IMPLEMENT THREADING OF THE TWO PROCESSES. IT WAS NOT FASTER.
    # THE FASTEST WAY IS RO RUN THE PROGRAM LIKE WE DID ABOVE.
    # I AM LEAVING THE CODE IN CASE YOU KNOW HOW TO SPEED IT UP.
    # p1 = players.AlphaBetaPlayer(2, X)
    # p2 = players.RandomPlayer(O)
    # t1 = threading.Thread(target=search_test, args=(p1, p2, TESTING_ITERATIONS,))
    # p1 = players.MinimaxPlayer(2, X)
    # p2 = players.RandomPlayer(O)
    # t2 = threading.Thread(target=search_test, args=(p1, p2, TESTING_ITERATIONS,))
    # ts = time.time()
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    # t_stop = time.time()
    # print("Total time: ", t_stop - ts, "s")


print_player_moves = False

if __name__ == '__main__':
    main()

# Importing libraries
import copy
from copy import deepcopy
import players

# Defining Global Variables.
EMPTY = '-'
X = 'X'
O = "O"
SIZE = 9
SIZEMINI = 3



class UtttState:
    '''A class to represent a state in Uttt game.'''
    ### Board is created such that to access a element at the center of middle board. WE say [4][1][1]
    def __init__(self, currentplayer, otherplayer,last_move = None, board_array = None, big_board_array = None):
        if board_array != None:
            self.board_array = board_array
        else:
            self.board_array = [[[EMPTY] * SIZEMINI for _ in range(SIZEMINI)] for _ in range(SIZE)]
        self.current = currentplayer
        self.other = otherplayer
        self.last_move = last_move
        self.master = big_to_master(self.board_array)
        self.heuristic = heuristic(self)

    # def master_to_smaller(self):
    #     #will return the state of
    #     pass

    def __repr__(self) -> str:
        new_string = "Last Action Chosen: " + str(self.last_move) + "     Player Turn: " + str(self.current.get_sign()) + "    Heuristic: " + str(self.heuristic) + "\n"
        new_string += "-------------------------------------\n"
        for m in range(SIZEMINI):
            for j in range(SIZEMINI):
                new_string += "|  "
                for i in range(SIZEMINI):
                    for k in range(SIZEMINI):
                        new_string += self.board_array[i+(3*m)][j][k] + "  "
                    new_string += "|  "
                new_string += "\n"
            new_string += "-------------------------------------\n"
        new_string += " ###### MASTER BOARD ######\n"
        for i in range(SIZEMINI):
            new_string += "|  "
            for j in range(SIZEMINI):
                new_string += self.master[i][j] + "  "
            new_string += "|  "
            new_string += "\n"
        new_string += "-------------------------------------\n"
        # new_string += "Current Player: " + str(self.current.get_sign()) + "    Heuristic: " + str(self.heuristic) + "\n"
        return new_string

    def print_subboard(self, num) -> str:
        new_string = ""
        sub_board = self.board_array[num]
        for i in range(SIZEMINI):
            items = " ".join(sub_board[i])
            new_string += items + "\n"
        print(new_string)
        
class UtttGame:
    """A class to encapsulate the variable and methods for the Uttt game."""
    pass

def terminal_test(gameBoard, state=None):
    # INPUT: 3X3 GAME BOARD
    # OUTPUT: BOOLEAN IF GAME IS WON OR NOT, CHARACTER OF WINNING PLAYER

    game_won = False
    winning_character = None
    game = copy.deepcopy(gameBoard)

    # Check if the game is in a tie
    if state is not None: # 
        if actions(state) == []:
            game_won = True # assuming the game was won
            winning_character = state.board_array[state.last_move[0]][state.last_move[1]][state.last_move[2]] # initializing the winning character
            not_tie, tmp = terminal_test(state.master) # Checking if the game is not a tie
            if not_tie != True: # If the game is a tie, then the winning character is a tie
                winning_character = "Tie"
            return game_won, winning_character

    # Column and row test
    for j in range(3):
        # Checking Rows to see if there is a winner
        tmp_char_row = game[j][0]
        if tmp_char_row != "-":
            if tmp_char_row == game[j][1] and tmp_char_row == game[j][2]:
                game_won = True
                winning_character = tmp_char_row
            

        # Checking Columns to see if there is a winner
        tmp_char_col = game[0][j]
        if tmp_char_col != "-":
            if tmp_char_col == game[1][j] and tmp_char_col == game[2][j]:
                game_won = True
                winning_character = tmp_char_col

    # Diagonal Test this way -> \
    tmp_char_diag = game[0][0]
    if tmp_char_diag != "-":
        if tmp_char_diag == game[1][1] and tmp_char_diag == game[2][2]:
            game_won = True
            winning_character = tmp_char_diag

    # Diagonal Test this way -> /
    tmp_char_diag = game[0][2]
    if tmp_char_diag != "-":
        if tmp_char_diag == game[1][1] and tmp_char_diag == game[2][0]:
            game_won = True
            winning_character = tmp_char_diag

    return game_won, winning_character

def big_to_master(game):
    # INPUT: 9X3X3 MASTER GAME BOARD
    # OUTPUT: SMALLER 3X3 GAME BOARD REPRESENTING LARGER BOARD

    return_game = [[" ", " ", " "],
                    [" ", " ", " "],
                    [" ", " ", " "]]
    for i in range(9):
        ind_game = game[i]
        game_won, winning_character = terminal_test(ind_game)
        if game_won:
            char = winning_character
        else:
            char = "-"
        return_game[i//3][i%3] = char
    return return_game


## Change Legal actions to account for when the selected board is full,
#  and hence the player can move anywhere on the board.
def actions(state):
    """Return a list of posible actions possible form this state(Instance of UtttState).
    Actions look like (i,x,y), where i the mini board number and x,y
    represent the row and column of the place in mini board."""
    legal_actions = []
    mb = 10

    # Check if the last move was None.
    if state.last_move is None:
        possible_mini_boards = []
        for mini_board in range(SIZE):
            game_over, tmp = terminal_test(state.board_array[mini_board])
            if not game_over:
                possible_mini_boards.append(mini_board)
        # Last move was None, so any move is possible.
        for mini_board in possible_mini_boards:
            for i in range(SIZEMINI):
                for j in range(SIZEMINI):
                    if state.board_array[mini_board][i][j] == EMPTY:
                        legal_actions.append((mini_board,i,j))
        return legal_actions


    # Last move was not None.
    mb = state.last_move[1] * 3 + state.last_move[2]
    game_over, tmp = terminal_test(state.board_array[mb])

    # Check if the mini board is full. If it is, then any move is possible that.
    if game_over:
        possible_mini_boards = []
        for mini_board in range(SIZE):
            game_over, tmp = terminal_test(state.board_array[mini_board])
            if not game_over:
                possible_mini_boards.append(mini_board)
        # Last move was None, so any move is possible.
        for mini_board in possible_mini_boards:
            for i in range(SIZEMINI):
                for j in range(SIZEMINI):
                    if state.board_array[mini_board][i][j] == EMPTY:
                        legal_actions.append((mini_board, i, j))
        return legal_actions

    else:
        # Last move was not None, and the mini board is not full. Return all empty mini board positions.
        for i in range(SIZEMINI):
            for j in range(SIZEMINI):
                if state.board_array[mb][i][j] == EMPTY:
                    legal_actions.append((mb,i,j))
        return legal_actions

def heuristic(state):
    """Returns the heuristic value of the given state.
    This is the evaluation function for the state."""
    # Check if the game is over.
    game_over, winner = terminal_test(state.master, state)
    score = 0
    if game_over:
        if winner == state.current.get_sign():
            return 10000
        elif winner == state.other.get_sign():
            return -10000
        else:
            return 0

    # Game is not over.
    # Check if the last move was None.
    if state.last_move is None:
        # Last move was None, so any move is possible. therefore the board is empty and the score is 0
        return 0

    # SCORES FOR THE MASTER BOARD
    MASTER_CENTER = 500
    MASTER_CORNER = 400
    MASTER_EDGE = 300

    # Find the number of positions on the master board that are filled. Give each of these a high score
    for i in range(SIZEMINI):
        for j in range(SIZEMINI):
            # Checking if the current position is filled with the current player's sign.
            if state.master[i][j] == state.current.get_sign():
                # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
                if check_if_center(i, j):
                    score += MASTER_CENTER
                if check_if_corner(i, j):
                    score += MASTER_CORNER
                if check_if_edge(i, j):
                    score += MASTER_EDGE

            elif state.master[i][j] == state.other.get_sign():
                # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
                if check_if_center(i, j):
                    score -= MASTER_CENTER
                if check_if_corner(i, j):
                    score -= MASTER_CORNER
                if check_if_edge(i, j):
                    score -= MASTER_EDGE


    # SCORES ASSIGNED FOR POINTS ON MINI BOARDS
    MINI_CENTER = 5
    MINI_CORNER = 4
    MINI_EDGE = 2

    for mb in range(SIZE):
        for i in range(SIZEMINI):
            for j in range(SIZEMINI):
                # Checking if the game is won - if so, we have already assigned a score for the master board.
                game_over, winner = terminal_test(state.board_array[mb])
                if not game_over:
                    # Game is not over. Checking if the current position is filled with the current player's sign.
                    if state.board_array[mb][i][j] == state.current.get_sign():
                        # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
                        if check_if_center(i, j):
                            score += MINI_CENTER
                        if check_if_corner(i, j):
                            score += MINI_CORNER
                        if check_if_edge(i, j):
                            score += MINI_EDGE

                    elif state.board_array[mb][i][j] == state.other.get_sign():
                        # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
                        if check_if_center(i, j):
                            score -= MINI_CENTER
                        if check_if_corner(i, j):
                            score -= MINI_CORNER
                        if check_if_edge(i, j):
                            score -= MINI_EDGE



    return score
    # # Check if the mini board is full. If it is, then any move is possible that.
    # if game_over:
    #     return 0
    #
    # else:
    #     # Last move was not None, and the mini board is not full. Return all empty mini board positions.
    #     return 0

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




def result(state, action):
    """Returns the resulting state after taking the given action. 
    Returns None if the action is not legal."""
    # Get the position of move from action.
    mb, i, j = action
    ## Check for legal action, by checking that the position is empty.
    if state.board_array[mb][i][j]!=EMPTY:
        return None
    else:
        # New state has to be formed here.
        # Make the new Board array.
        new_board = deepcopy(state.board_array)
        new_board[mb][i][j] = state.current.sign
        new_state = UtttState(state.other, state.current , last_move = action, board_array = new_board)
        return new_state







# def terminal_test(state):
#     raise NotImplementedError

def play_game(p1 = None, p2 = None):
    """Play the game with two players. Default use two humans."""
    if p1 == None:
        p1 = HumanPlayer(X)
    if p2 == None:
        p2 = HumanPlayer(O)

    s = UtttState(p1, p2)
    while True:
        action = p1.make_move(s)
        if action not in actions(s):
            print("Illegal move made by X")
            print("O wins!")
            return
        print(s)
        s = result(s, action)
        # print(s)
        # print("Heuristic: ", heuristic(s), " Current Player: ", s.current.get_sign())
        game_over, winner = terminal_test(s.master, s)
        if game_over:
            print("Game Over")
            print("Player " + winner + " wins!")
            # display(s)
            # display_final(s)
            return
        action = p2.make_move(s)
        if action not in actions(s):
            print("Illegal move made by O")
            print("O wins!")
            return
        print(s)
        s = result(s, action)
        # print(s)
        game_over, winner = terminal_test(s.master, s)
        # print("Heuristic: ", heuristic(s), " Current Player: ", s.current.get_sign())
        if game_over:
            print("Game Over")
            print("Player " + winner + " wins!")
        #     display(s)
        #     display_final(s)
            return
    
def main():
    p1 = players.RandomPlayer(X)
    p2 = players.RandomPlayer(O)
    play_game(p1, p2)

if __name__=='__main__':
    main()
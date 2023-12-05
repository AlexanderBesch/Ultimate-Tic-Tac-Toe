# Importing libraries
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

    def master_to_smaller(self):
        #will return the state of 
        pass

    def __repr__(self) -> str:
        new_string = "-------------------------------------\n"
        for m in range(SIZEMINI):
            for j in range(SIZEMINI):
                new_string += "|  "
                for i in range(SIZEMINI):
                    for k in range(SIZEMINI):
                        new_string += self.board_array[i+(3*m)][j][k] + "  "
                    new_string += "|  "
                new_string += "\n"
            new_string += "-------------------------------------\n"
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
                    legal_actions.append((mb,i,j))
    else:
        # There was some last move.
        last_mb, last_i, last_j = state.last_move
        # Find the new legal mb from last i,j.
        mb = 3*last_i + last_j
        for i in range(3):
            for j in range(3):
                if state.board_array[mb][i][j]==EMPTY:
                    legal_actions.append((mb,i,j))
    return legal_actions

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

def terminal_test(state):
    raise NotImplementedError

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
        s = result(s, action)
        print(s)
        # if terminal_test(s):
        #     print("Game Over")
        #     display(s)
        #     display_final(s)
        #     return
        action = p2.make_move(s)
        if action not in actions(s):
            print("Illegal move made by O")
            print("O wins!")
            return
        s = result(s, action)
        print(s)
        # if terminal_test(s):
        #     print("Game Over")
        #     display(s)
        #     display_final(s)
        #     return
    
def main():
    p1 = players.RandomPlayer(X)
    p2 = players.RandomPlayer(O)
    play_game(p1, p2)

if __name__=='__main__':
    main()
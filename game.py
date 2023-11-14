
WHITE = 1
BLACK = -1
EMPTY = 0
BLOCKED = -2
SIZE = 3
SKIP = "SKIP"

class OthelloPlayerTemplate:
    '''Template class for an Othello Player

    An othello player *must* implement the following methods:

    get_color(self) - correctly returns the agent's color

    make_move(self, state) - given the state, returns an action that is the agent's move
    '''
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        '''Given the state, returns a legal action for the agent to take in the state
        '''
        return None
    
class RandomPlayer(OthelloPlayerTemplate):
    """Random Player, chooses a action randomly from legal actions."""
    def __init__(self, mycolor):
        self.color = mycolor
    
    def get_color(self):
        return self.color
    
    def make_move(self,state):
        legal_actions = actions(state)
        move = random.choice(legal_actions)
        if print_player_moves: print(f"Random Player made move: {move}")
        return move
    
class PlayerMohit(OthelloPlayerTemplate):
    """Random Player, chooses a action randomly from legal actions."""
    def __init__(self, mycolor):
        self.color = mycolor
    
    def get_color(self):
        return self.color
    
    def utility(self, state):
        """Write a utility funtion here a metric to gudge the state. Return a number."""
        mycolor = self.color
        # Count the number of white and black blocks on the board.
        wcount = 0
        bcount = 0
        for i in range(SIZE):
            for j in range(SIZE):
                if state.board_array[i][j] == WHITE:
                    wcount += 1
                elif state.board_array[i][j] == BLACK:
                    bcount += 1
        # Set the winner till now.
        leading = "Tie"
        if wcount > bcount:
            leading = WHITE
        elif wcount < bcount:
            leading = BLACK
        
        if terminal_test(state):
            if leading == mycolor:
                return 1000
            elif leading == "Tie":
                return -10
            else:
                return -1000

        if mycolor == BLACK:
            return bcount - wcount
        else:
            return wcount - bcount


    def make_move(self,state):
        legal_actions = actions(state)
        if self.color == 1:
            print("White ",end='')
        else:
            print("Black ",end="")
        print(" to play.")
        print("Legal Moves are " +str(legal_actions))
        move = random.choice(legal_actions)

        return move

class HumanPlayer(OthelloPlayerTemplate):
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)
        while curr_move == None:
            display(state)
            if self.color == 1:
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))
            move = input("Enter your move as a r,c pair:")
            if move == "":
                return legals[0]

            if move == SKIP and SKIP in legals:
                return move

            try:
                movetup = int(move.split(',')[0]), int(move.split(',')[1])
            except:
                movetup = None
            if movetup in legals:
                curr_move = movetup
            else:
                print("That doesn't look like a legal action to me")
        return curr_move

class RandOthelloState:
    '''A class to represent an othello game state'''

    def __init__(self, currentplayer, otherplayer, board_array = None, big_board_array = None):
        if board_array != None:
            self.board_array = board_array
        else:
            self.board_array = [[["-"] * 3 for _ in range(3)] for _ in range(9)]
            self.board_array[1][0][1] = "X"
            self.board_array[4][0][0] = "O"
        self.current = currentplayer
        self.other = otherplayer

    def master_to_smaller(self):
        #will return the state of 
        pass

    def __repr__(self) -> str:
        new_string = "-------------------------------------\n"
        for m in range(3):
            for j in range(3):
                new_string += "|  "
                for i in range(3):
                    for k in range(3):
                        new_string += self.board_array[i+(3*m)][j][k] + "  "
                    new_string += "|  "
                new_string += "\n"
            new_string += "-------------------------------------\n"
        return new_string

 
class MinimaxPlayer(OthelloPlayerTemplate):
    def __init__(self, mycolor, depth) -> None:
        self.color = mycolor
        self.depth = depth

    def get_color(self):
        return self.color
        
    def make_move(self, state):
        legal_actions = actions(state)
        move = self.minimax_search(state)
        if print_player_moves: print(f"Minimax Player made move: {move}")
        return move

    def minimax_search(self, state):
        # Return an action to perform
        player = self.color
        current_depth = 0
        value, move = self.max_value(state, current_depth)
        return move

    def max_value(self, state, current_depth):
        # Returns  (utility, move)
        if terminal_test(state):
            return self.utility(state), None
        # Check if depth limit has been reached
        if self.depth == current_depth:
            return self.utility(state), None

        current_depth+=1
        v = float('-inf')

        for action in actions(state):
            result_state = result(state,action)
            v2 , a2 = self.min_value(result_state, current_depth)
            if v2 > v:
                v, move = v2, action
        return v, move

    def min_value(self, state, current_depth):
        # Returns (utility, move)
        if terminal_test(state):
            return self.utility(state), None
        # Check if depth limit has been reached.
        if self.depth == current_depth:
            return self.utility(state), None
        
        current_depth+=1
        v = float('inf')

        for action in actions(state):
            result_state = result(state, action)
            v2, a2 = self.max_value(result_state, current_depth)
            if v2 < v:
                v, move = v2, action
        return v, move
    
    def utility(self, state):
        """Write a utility funtion here a metric to gudge the state. Return a number."""
        mycolor = self.color
        # Count the number of white and black blocks on the board.
        wcount = 0
        bcount = 0
        for i in range(SIZE):
            for j in range(SIZE):
                if state.board_array[i][j] == WHITE:
                    wcount += 1
                elif state.board_array[i][j] == BLACK:
                    bcount += 1
        # Set the winner till now.
        leading = "Tie"
        if wcount > bcount:
            leading = WHITE
        elif wcount < bcount:
            leading = BLACK
        
        if terminal_test(state):
            if leading == mycolor:
                return 1000
            elif leading == "Tie":
                return -10
            else:
                return -1000

        if mycolor == BLACK:
            return bcount - wcount
        else:
            return wcount - bcount
        
class AlphaBetaPlayer(OthelloPlayerTemplate):
    def __init__(self, mycolor, depth):
        self.color = mycolor
        self.depth = depth
    
    def get_color(self):
        return self.color
    
    def make_move(self, state):
        legal_actions = actions(state)
        move = self.alpha_beta_search(state)
        if print_player_moves: print(f"AlphaBeta Plater made move: {move}")
        return move

    def alpha_beta_search(self, state):
        # Returns a action that the person has to do.
        player = self.color
        current_depth = 0
        value, move = self.max_value(state, float('-inf') , float('inf'), current_depth)
        return move

    def max_value(self, state, alpha, beta, current_depth):
        # Returns (utility, move)
        if terminal_test(state):
            return self.utility(state), None
        if self.depth == current_depth:
            return self.utility(state), None
        
        current_depth+=1
        v = float('-inf')
        
        for action in actions(state):
            result_state = result(state, action)
            v2, a2 = self.min_value(result_state, alpha, beta, current_depth)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(self, state, alpha ,beta,current_depth):
        # Returns (utility, move)
        if terminal_test(state):
            return self.utility(state), None
        if self.depth == current_depth:
            return self.utility(state), None
        
        current_depth+=1
        v = float('+inf')

        for action in actions(state):
            result_state = result(state, action)
            v2, a2 = self.max_value(result_state, alpha, beta, current_depth)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if v <=alpha:
                return v, move
        return v, move

    def utility(self, state):
        """Write a utility funtion here a metric to gudge the state. Return a number."""
        mycolor = self.color
        if mycolor == WHITE:
            opp_color = BLACK
        if mycolor == BLACK:
            opp_color = WHITE

        # Count the number of white and black blocks on the board.
        wcount = 0
        bcount = 0
        for i in range(SIZE):
            for j in range(SIZE):
                if state.board_array[i][j] == WHITE:
                    wcount += 1
                elif state.board_array[i][j] == BLACK:
                    bcount += 1
        # Set the winner till now.

        if mycolor == WHITE:
            diff = wcount - bcount
        else:
            diff = bcount - wcount
        diff_value = diff * 1

        ### Corner Piece Weights
        count_corner = 0
        for i in [0,7]:
            for j in [0,7]:
                if state.board_array[i][j] == mycolor:
                    count_corner +=1
                elif state.board_array[i][j] == opp_color:
                    count_corner -= 1
        value_corner = count_corner * 100

        ### Edges Test weights
        edge_count = 0
        for i in [0,7]:
            for j in range(1,SIZE-1):
                if state.board_array[i][j] == mycolor:
                    edge_count += 1
                elif state.board_array[i][j] == opp_color:
                    edge_count -= 1
        for i in range(1,SIZE-1):
            for j in [0,7]:
                if state.board_array[i][j] == mycolor:
                    edge_count += 1
                elif state.board_array[i][j] == opp_color:
                    edge_count -= 1
        value_edges = edge_count * 30

        ### Occuping blocks near BLOCKED give you extra points.
        blocked_edges_count = 0
        # bottom_blocked_index
        top_blocked_index = [state.board_array[j][0] for j in range(SIZE)].index(BLOCKED)
        bottom_blocked_index = [state.board_array[j][7] for j in range(SIZE)].index(BLOCKED)
        
        if top_blocked_index == 0:
            if state.board_array[1][0] == mycolor:
                blocked_edges_count += 1
            elif state.board_array[1][0] == opp_color:
                blocked_edges_count -= 1
        elif top_blocked_index == 7:
            if state.board_array[6][0] == mycolor:
                blocked_edges_count += 1
            elif state.board_array[6][0] == opp_color:
                blocked_edges_count -= 1
        else:
            l = [top_blocked_index + a for a in [1,-1]]
            for index in l:
                if state.board_array[index][0] == mycolor:
                    blocked_edges_count += 1
                elif state.board_array[index][0] == opp_color:
                    blocked_edges_count -= 1

        if bottom_blocked_index == 0:
            if state.board_array[1][7] == mycolor:
                blocked_edges_count += 1
            elif state.board_array[1][7] == opp_color:
                blocked_edges_count -= 1
        elif bottom_blocked_index == 7:
            if state.board_array[6][7] == mycolor:
                blocked_edges_count += 1
            elif state.board_array[6][7] == opp_color:
                blocked_edges_count -= 1
        else:
            l = [bottom_blocked_index + a for a in [1,-1]]
            for index in l:
                if state.board_array[index][0] == mycolor:
                    blocked_edges_count += 1
                elif state.board_array[index][0] == opp_color:
                    blocked_edges_count -= 1

        value_blocked_block = blocked_edges_count * 50

        ## Having more number of legal moves.
        no_of_legal_moves = len(actions(state))
        value_legal_moves = 10 * no_of_legal_moves
        
        if terminal_test(state):
            if wcount > bcount:
                if mycolor == WHITE:
                    return 10000
                elif mycolor == BLACK:
                    return -10000
            if wcount < bcount:
                if mycolor == BLACK:
                    return 10000
                elif mycolor == WHITE:
                    return -10000
            if wcount == bcount:
                return -5000

        final_utility = diff_value + value_corner + value_edges + value_legal_moves + value_blocked_block
        # print(f"Utility of {mycolor} is : {final_utility}")
        return final_utility

def player(state):
    return state.current

def actions(state):
    '''Return a list of possible actions given the current state
    '''
    legal_actions = []
    for i in range(SIZE):
        for j in range(SIZE):
            if result(state, (i,j)) != None:
                legal_actions.append((i,j))
    if len(legal_actions) == 0:
        legal_actions.append(SKIP)
    return legal_actions

def result(state, action):
    '''Returns the resulting state after taking the given action

    (This is the workhorse function for checking legal moves as well as making moves)

    If the given action is not legal, returns None

    '''
    # first, special case! an action of SKIP is allowed if the current agent has no legal moves
    # in this case, we just skip to the other player's turn but keep the same board
    if action == SKIP:
        newstate = RandOthelloState(state.other, state.current, copy.deepcopy(state.board_array), state.num_skips + 1)
        return newstate
    # Position where you are placing new ele should be empty.
    if state.board_array[action[0]][action[1]] != EMPTY:
        return None

    color = state.current.get_color()
    # create new state with players swapped and a copy of the current board
    newstate = RandOthelloState(state.other, state.current, copy.deepcopy(state.board_array))

    newstate.board_array[action[0]][action[1]] = color
    
    flipped = False
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for d in directions:
        i = 1
        count = 0
        while i <= SIZE:
            x = action[0] + i * d[0]
            y = action[1] + i * d[1]
            if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
                count = 0
                break
            elif newstate.board_array[x][y] == -1 * color:
                count += 1
            elif newstate.board_array[x][y] == color:
                break
            else:
                count = 0
                break
            i += 1

        if count > 0:
            flipped = True

        for i in range(count):
            x = action[0] + (i+1) * d[0]
            y = action[1] + (i+1) * d[1]
            newstate.board_array[x][y] = color

    if flipped:
        return newstate
    else:  
        # if no pieces are flipped, it's not a legal move
        return None

def terminal_test(state):
    '''Simple terminal test
    '''
    # if both players have skipped
    if state.num_skips == 2:
        return True

    # if there are no empty spaces
    empty_count = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                empty_count += 1
    if empty_count == 0:
        return True
    return False

def display(state):
    '''Displays the current state in the terminal window
    '''
    print('  ', end='')
    for i in range(SIZE):
        print(i,end=' ')
    print()
    for i in range(SIZE):
        print(i, '', end='')
        for j in range(SIZE):
            if state.board_array[j][i] == WHITE:
                print('W', end=' ')
            elif state.board_array[j][i] == BLACK:
                print('B', end=' ')
            elif state.board_array[j][i] == BLOCKED:
                print('X', end=' ')
            else:
                print('-', end=' ')
        print()

def display_final(state):
    '''Displays the score and declares a winner (or tie)
    '''
    wcount = 0
    bcount = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == WHITE:
                wcount += 1
            elif state.board_array[i][j] == BLACK:
                bcount += 1

    print("Black: " + str(bcount))
    print("White: " + str(wcount))
    if wcount > bcount:
        print("White wins")
    elif wcount < bcount:
        print("Black wins")
    else:
        print("Tie")

def play_game(p1 = None, p2 = None):
    '''Plays a game with two players. By default, uses two humans
    '''
    if p1 == None:
        p1 = HumanPlayer(BLACK)
    if p2 == None:
        p2 = HumanPlayer(WHITE)

    s = RandOthelloState(p1, p2)
    while True:
        action = p1.make_move(s)
        if action not in actions(s):
            print("Illegal move made by Black")
            print("White wins!")
            return
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return
        action = p2.make_move(s)
        if action not in actions(s):
            print("Illegal move made by White")
            print("Black wins!")
            return
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return

def main():
    # ### First Game.
    # print("First game between random player playing 'Black' and Alpha-beta playing 'White'")
    # # play_game(p1=RandomPlayer(BLACK),p2=AlphaBetaPlayer(WHITE,3))

    # ### Second Game.
    # print("\n\nSecond game between random player playing 'White' and Alpha-beta playing 'Black'")
    # # play_game(p1=RandomPlayer(WHITE),p2=AlphaBetaPlayer(BLACK,3))
    # play_game(p1=MinimaxPlayer(BLACK,3),p2=AlphaBetaPlayer(WHITE,4))
    # play_game(p1=AlphaBetaPlayer(BLACK,3),p2=RandomPlayer(WHITE))
    print("runing mohit game")
    new_board = RandOthelloState("X","Y")
    # print(new_board.board_array)
    print(new_board)


if __name__ == '__main__':
    main()
    

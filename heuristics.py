import gameuttt as game
# from players import check_if_center, check_if_corner, check_if_edge

X = "X"
O = "O"
EMPTY = "-"
TIE = "T"
SIZE = 9
SIZEMINI = 3


def homemade(player, state):
    """Returns the heuristic value of the given state.
    This is the evaluation function for the state."""
    # Check if the game is over.
    # print("master board: " + str(state.master_board))
    # print(game.terminal_test(state.master_board))

    game_over, winner = game.terminal_test(state)
    score = 0
    player = player.sign
    if player == X:
        otherplayer = O
    else:
        otherplayer = X

    if game_over:
        if winner == player:
            return 10000
        elif winner == otherplayer:
            return -10000
        else:
            return -1000

    # Game is not over.

    # SCORES FOR THE MASTER BOARD
    master_center = 500
    master_corner = 400
    master_edge = 300

    # Find the number of positions on the master board that are filled. Give each of these a high score
    for i in range(SIZEMINI):
        for j in range(SIZEMINI):
            # Checking if the current position is filled with the current player's sign.
            if state.master_board[i][j] == player:
                # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
                if check_if_center(i, j):
                    score += master_center
                if check_if_corner(i, j):
                    score += master_corner
                if check_if_edge(i, j):
                    score += master_edge
            elif state.master_board[i][j] == otherplayer:
                # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
                if check_if_center(i, j):
                    score -= master_center
                if check_if_corner(i, j):
                    score -= master_corner
                if check_if_edge(i, j):
                    score -= master_edge

    # SCORES ASSIGNED FOR POINTS ON MINI BOARDS
    mini_center = 5
    mini_corner = 4
    mini_edge = 3

    possible_mb = []
    for i in range(SIZEMINI):
        for j in range(SIZEMINI):
            if state.master_board[i][j] == EMPTY:
                possible_mb.append(3 * i + j)
    for mb in possible_mb:
        for i in range(SIZEMINI):
            for j in range(SIZEMINI):
                if state.board_array[mb][i][j] == player:
                    # Current position is filled with the current players sign. Checking where in the 3x3 board the position is.
                    if check_if_center(i, j):
                        score += mini_center
                    if check_if_corner(i, j):
                        score += mini_corner
                    if check_if_edge(i, j):
                        score += mini_edge

                elif state.board_array[mb][i][j] == otherplayer:
                    # Current position is filled with the other players sign. Checking where in the 3x3 board the position is.
                    if check_if_center(i, j):
                        score -= mini_center
                    if check_if_corner(i, j):
                        score -= mini_corner
                    if check_if_edge(i, j):
                        score -= mini_edge

    return score


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
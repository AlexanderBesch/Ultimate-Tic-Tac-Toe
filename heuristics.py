import gameuttt as game
from collections import Counter
# from players import check_if_center, check_if_corner, check_if_edge

# Defining Global Variables defined in gameuttt.py
EMPTY = game.global_vars[0]
X = game.global_vars[1]
O = game.global_vars[2]
T = game.global_vars[3]
SIZE = game.global_vars[4]
SIZEMINI = game.global_vars[5]
WINNING_POSITIONS = game.global_vars[6]
MAXSCORE = 100000 # game.global_vars[7]


def homemade(player, state):
    """Returns the heuristic value of the given state using a homemade scoring method.
    This is the evaluation function for the state."""
    # Check if the game is over.
    game_over, winner = game.terminal_test(state)
    score = 0
    player = player.sign
    if player == X:
        otherplayer = O
    else:
        otherplayer = X

    if game_over:
        if winner == player:
            return MAXSCORE
        elif winner == otherplayer:
            return -MAXSCORE
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
                # Current position is filled with the current player's sign. Checking where in the 3x3 board the position is.
                if check_if_center(i, j):
                    score += master_center
                if check_if_corner(i, j):
                    score += master_corner
                if check_if_edge(i, j):
                    score += master_edge
            elif state.master_board[i][j] == otherplayer:
                # Current position is filled with the other player's sign. Checking where in the 3x3 board the position is.
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
                    # Current position is filled with the current player's sign. Checking where in the 3x3 board the position is.
                    if check_if_center(i, j):
                        score += mini_center
                    if check_if_corner(i, j):
                        score += mini_corner
                    if check_if_edge(i, j):
                        score += mini_edge
                elif state.board_array[mb][i][j] == otherplayer:
                    # Current position is filled with the other player's sign. Checking where in the 3x3 board the position is.
                    if check_if_center(i, j):
                        score -= mini_center
                    if check_if_corner(i, j):
                        score -= mini_corner
                    if check_if_edge(i, j):
                        score -= mini_edge

    return score


def pulkit_github(player, state):
    """Returns the heuristic value of the given state using Pulkit's scoring method.
    This is the evaluation function for the state."""
    game_over, winner = game.terminal_test(state)
    score = 0
    player = player.sign
    if player == X:
        otherplayer = O
    else:
        otherplayer = X

    if game_over:
        if winner == player:
            return MAXSCORE
        elif winner == otherplayer:
            return -MAXSCORE
        else:
            return -1000

    # Game is not over
    # The way this heuristic works is that it looks at every way to win and assigns a score to each mini-game as to how close the player is to winning
    # If the current player has 1 in a row and the rest is empty, then the score is 1
    # If the current player has 2 in a row and the rest is empty, then the score is 10
    # If the current player has 3 in a row, then the score is 100
    # If the other player has 1 in a row and the rest is empty, then the score is -1
    # If the other player has 2 in a row and the rest is empty, then the score is -10
    # If the other player has 3 in a row, then the score is -100

    # Initializing counter
    three = Counter(player * 3)
    two = Counter(player * 2 + EMPTY)
    one = Counter(player * 1 + EMPTY * 2)
    three_opponent = Counter(otherplayer * 3)
    two_opponent = Counter(otherplayer * 2 + EMPTY)
    one_opponent = Counter(otherplayer * 1 + EMPTY * 2)

    for i in range(SIZE):
        for idxs in WINNING_POSITIONS:
            [x1, x2] = idxs[0]
            [y1, y2] = idxs[1]
            [z1, z2] = idxs[2]
            current = Counter([state.board_array[i][x1][x2], state.board_array[i][y1][y2], state.board_array[i][z1][z2]])
            if current == three:
                score += 100
            elif current == two:
                score += 10
            elif current == one:
                score += 1
            elif current == three_opponent:
                score -= 100
            elif current == two_opponent:
                score -= 10
            elif current == one_opponent:
                score -= 1

    return score

def homemadeV2(player, state):
    """Returns the heuristic value of the given state using an extended version of the homemade scoring method.
    This is the evaluation function for the state."""
    game_over, winner = game.terminal_test(state)
    score = 0
    player = player.sign
    if player == X:
        otherplayer = O
    else:
        otherplayer = X

    if game_over:
        if winner == player:
            return MAXSCORE
        elif winner == otherplayer:
            return -MAXSCORE
        else:
            return -1000

    # Game is not over
    # The way this heuristic works is that it looks at every way to win and assigns a score to each mini-game as to how close the player is to winning
    # If the current player has 1 in a row and the rest is empty, then the score is 1
    # If the current player has 2 in a row and the rest is empty, then the score is 10
    # If the current player has 3 in a row, then the score is 100
    # If the other player has 1 in a row and the rest is empty, then the score is -1
    # If the other player has 2 in a row and the rest is empty, then the score is -10
    # If the other player has 3 in a row, then the score is -100

    # Initializing counter
    three = Counter(player * 3)
    two = Counter(player * 2 + EMPTY)
    one = Counter(player * 1 + EMPTY * 2)
    three_opponent = Counter(otherplayer * 3)
    two_opponent = Counter(otherplayer * 2 + EMPTY)
    one_opponent = Counter(otherplayer * 1 + EMPTY * 2)

    for i in range(SIZE):
        for idxs in WINNING_POSITIONS:
            [x1, x2] = idxs[0]
            [y1, y2] = idxs[1]
            [z1, z2] = idxs[2]
            current = Counter([state.board_array[i][x1][x2], state.board_array[i][y1][y2], state.board_array[i][z1][z2]])
            if current == three:
                score += 100
            elif current == two:
                score += 10
            elif current == one:
                score += 1
            elif current == three_opponent:
                score -= 100
            elif current == two_opponent:
                score -= 10
            elif current == one_opponent:
                score -= 1

    for idxs in WINNING_POSITIONS:
        [x1, x2] = idxs[0]
        [y1, y2] = idxs[1]
        [z1, z2] = idxs[2]
        current = Counter([state.master_board[x1][x2], state.master_board[y1][y2], state.master_board[z1][z2]])
        if current == three:
            score += MAXSCORE
        elif current == two:
            score += 1000
        elif current == one:
            score += 100
        elif current == three_opponent:
            score -= MAXSCORE
        elif current == two_opponent:
            score -= 1000
        elif current == one_opponent:
            score -= 100

    return score


def check_if_center(i, j):
    """Checks if the given position is at the center of a 3x3 board."""
    if i == 1 and j == 1:
        return True
    else:
        return False


def check_if_corner(i, j):
    """Checks if the given position is at a corner of a 3x3 board."""
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
    """Checks if the given position is at an edge of a 3x3 board."""
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

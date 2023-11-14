

# =============================================================================
# State is stored as a string where index is at place shown in the board below
#
#  --------------------------------
# |  0  1  2 | 9  10 11 | 18 19 20 |
# |  3  4  5 | 12 13 14 | 21 22 23 |
# |  6  7  8 | 15 16 17 | 24 25 26 |
#  --------------------------------
# | 27 28 29 | 36 37 38 | 45 46 47 |
# | 30 31 32 | 39 40 41 | 48 49 50 |
# | 33 34 35 | 42 43 44 | 51 52 53 |
#  --------------------------------
# | 54 55 56 | 63 64 65 | 72 73 74 |
# | 57 58 59 | 66 67 68 | 75 76 77 |
# | 60 61 62 | 69 70 71 | 78 79 80 |
#  --------------------------------
#
# =============================================================================




game_not_done = [["X", "O", "X"],
                ["O", "X", "-"],
                ["O", "X", "-"]]

game_won_x = [["X", "O", "X"],
                ["O", "X", "-"],
                ["O", "X", "X"]]

game_won_o = [["X", "O", "X"],
                ["O", "X", "-"],
                ["O", "O", "O"]]

def terminal_test(game):
    game_won = False

    for j in range(3):
        # Row Test
        tmp_char_row = game[j][0]
        if tmp_char_row != "-":
            if tmp_char_row == game[j][1] and tmp_char_row == game[j][2]:
                gmae_won = True

        # Column Test
        tmp_char_col = game[0][j]
        if tmp_char_col != "-":
            if tmp_char_col == game[1][j] and tmp_char_col == game[2][j]:
                game_won = True

    # Diagonal Test this way -> \
    tmp_char_diag = game[0][0]
    if tmp_char_diag != "-":
        if tmp_char_diag == game[1][1] and tmp_char_diag == game[2][2]:
            game_won = True

    # Diagonal Test this way -> /
    tmp_char_diag = game[0][2]
    if tmp_char_diag != "-":
        if tmp_char_diag == game[1][1] and tmp_char_diag == game[2][0]:
            game_won = True

    return game_won

print(terminal_test(game_not_done))
print(terminal_test(game_won_o))
print(terminal_test(game_won_x))






#
#
#
#
#
#
#
#
# def max_value_alpha_beta(state, depth, player, alpha, beta):
#     if terminal_test(state) or depth == 0:
#         return utilityFunction(state, player), None
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
#     if terminal_test(state) or depth == 0:
#         return utilityFunction(state, player), None
#     val = float('inf')
#     for a in actions(state):
#         [v2, a2] = max_value_alpha_beta(result(state, a), depth - 1, player, alpha, beta)
#         if v2 < val:
#             val, move = v2, a
#             beta = min(beta, val)
#         if val <= alpha:
#             return val, move
#     return val, move
#
#
#
#
#
#
#
#
#
#
#
#
#
# def player(state):
#     return state.current
#
#
# def isEdge(columns, rows):
#     # Left side
#     if columns == 0 and rows != 0 and rows != 7:
#         return True
#     # Right side
#     if columns == 7 and rows != 0 and rows != 7:
#         return True
#     # Top
#     if rows == 0 and columns != 0 and columns != 7:
#         return True
#     # Bottom
#     if rows == 7 and columns != 0 and columns != 7:
#         return True
#
#     # Not any of the above cases
#     return False
#
#
# def isCorner(columns, rows):
#     if (columns == 0 and rows == 0) or (columns == 0 and rows == 7):
#         return True
#     if (columns == 7 and rows == 0) or (columns == 7 and rows == 7):
#         return True
#     return False
#
#
# def count_utils(state, player):
#     currentCorners = 0
#     otherCorners = 0
#     currentEdges = 0
#     otherEdges = 0
#     chipDelta = 0
#     countOther = 0
#     countCurrent = 0
#     # print("Current Player: ", state.current.color)
#     for rows in range(SIZE):
#         for columns in range(SIZE):
#             # print("Rows: ", rows, " Column: ", columns, " Board value: ", state.board_array[columns][rows])
#             # ###### CURRENT ######
#             if state.board_array[columns][rows] == player:
#                 countCurrent = countCurrent + 1
#                 # print("Count Current: ", countCurrent)
#                 if isEdge(columns, rows):
#                     currentEdges = currentEdges + 1
#                 if isCorner(columns, rows):
#                     currentCorners = currentCorners + 1
#             # Counting Other chips
#             if state.board_array[columns][rows] == -1 * player:  # and abs(state.board_array[columns][rows]) == 1:
#                 countOther = countOther + 1
#                 if isEdge(columns, rows):
#                     otherEdges = otherEdges + 1
#                 if isCorner(columns, rows):
#                     otherCorners = otherCorners + 1
#                 # print("Count Other: ", countOther)
#
#     chipDelta = countCurrent - countOther
#     cornerDelta = currentCorners - otherCorners
#     edgeDelta = currentEdges - otherEdges
#     return chipDelta, cornerDelta, edgeDelta
#
#
# def utilityFunction(state, player):
#     # [corners, edges, chip_delta] = count_utils(state)
#
#     [chipDelta, cornerDelta, edgeDelta] = count_utils(state, player)
#
#     max_options = len(actions(state))
#
#     min_options = 0  # -1
#     # for a in actions(state):
#     #     if len(actions(result(state, a))) > min_options:
#     #         min_options = len(actions(result(state, a)))
#
#     # print("Max: ", max_options, " Min: ", min_options)
#
#     utility = chipDelta * 10 + cornerDelta * 100 + edgeDelta * 0 + (max_options - min_options) * 10
#
#     game_complete = terminal_test(state)
#     if game_complete and chipDelta > 0:
#         # return 1 * float('inf')
#         return 1000000
#     if game_complete and chipDelta < 0:
#         return -1000000
#         # return 1 * float('-inf')
#     # for columns in range(SIZE):
#     #     for rows in range(SIZE):
#     #         print(state.board_array[columns][rows])
#     return utility
#
#
# def actions(state):
#     '''Return a list of possible actions given the current state
#     '''
#     legal_actions = []
#     for i in range(SIZE):
#         for j in range(SIZE):
#             if result(state, (i, j)) != None:
#                 legal_actions.append((i, j))
#     if len(legal_actions) == 0:
#         legal_actions.append(SKIP)
#     return legal_actions
#
#
# def result(state, action):
#     '''Returns the resulting state after taking the given action
#
#     (This is the workhorse function for checking legal moves as well as making moves)
#
#     If the given action is not legal, returns None
#
#     '''
#     # first, special case! an action of SKIP is allowed if the current agent has no legal moves
#     # in this case, we just skip to the other player's turn but keep the same board
#     if action == SKIP:
#         newstate = RandOthelloState(state.other, state.current, copy.deepcopy(state.board_array), state.num_skips + 1)
#         return newstate
#
#     if state.board_array[action[0]][action[1]] != EMPTY:
#         return None
#
#     color = state.current.get_color()
#     # create new state with players swapped and a copy of the current board
#     newstate = RandOthelloState(state.other, state.current, copy.deepcopy(state.board_array))
#
#     newstate.board_array[action[0]][action[1]] = color
#
#     flipped = False
#     directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
#     for d in directions:
#         i = 1
#         count = 0
#         while i <= SIZE:
#             x = action[0] + i * d[0]
#             y = action[1] + i * d[1]
#             if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
#                 count = 0
#                 break
#             elif newstate.board_array[x][y] == -1 * color:
#                 count += 1
#             elif newstate.board_array[x][y] == color:
#                 break
#             else:
#                 count = 0
#                 break
#             i += 1
#
#         if count > 0:
#             flipped = True
#
#         for i in range(count):
#             x = action[0] + (i + 1) * d[0]
#             y = action[1] + (i + 1) * d[1]
#             newstate.board_array[x][y] = color
#
#     if flipped:
#         return newstate
#     else:
#         # if no pieces are flipped, it's not a legal move
#         return None
#
#
# def terminal_test(state):
#     '''Simple terminal test
#     '''
#     # if both players have skipped
#     if state.num_skips == 2:
#         return True
#
#     # if there are no empty spaces
#     empty_count = 0
#     for i in range(SIZE):
#         for j in range(SIZE):
#             if state.board_array[i][j] == EMPTY:
#                 empty_count += 1
#     if empty_count == 0:
#         return True
#     return False
#
#
# def display(state):
#     '''Displays the current state in the terminal window
#     '''
#     print('  ', end='')
#     for i in range(SIZE):
#         print(i, end='')
#     print()
#     for i in range(SIZE):
#         print(i, '', end='')
#         for j in range(SIZE):
#             if state.board_array[j][i] == WHITE:
#                 print('W', end='')
#             elif state.board_array[j][i] == BLACK:
#                 print('B', end='')
#             elif state.board_array[j][i] == BLOCKED:
#                 print('X', end='')
#             else:
#                 print('-', end='')
#         print()
#
#
# def display_final(state):
#     '''Displays the score and declares a winner (or tie)
#     '''
#     wcount = 0
#     bcount = 0
#     for i in range(SIZE):
#         for j in range(SIZE):
#             if state.board_array[i][j] == WHITE:
#                 wcount += 1
#             elif state.board_array[i][j] == BLACK:
#                 bcount += 1
#
#     print("Black: " + str(bcount))
#     print("White: " + str(wcount))
#     if wcount > bcount:
#         print("White wins")
#     elif wcount < bcount:
#         print("Black wins")
#     else:
#         print("Tie")
#
#
# def play_game(p1=None, p2=None):
#     '''Plays a game with two players. By default, uses two humans
#     '''
#     if p1 == None:
#         p1 = HumanPlayer(BLACK)
#         # p1 = RandomPlayer(BLACK)
#         # p1 = MinimaxPlayer(BLACK, 4)
#
#     if p2 == None:
#         p2 = HumanPlayer(WHITE)
#         # p2 = AlphaBetaPlayer(WHITE, 4)
#
#     s = RandOthelloState(p1, p2)
#     while True:
#         action = p1.make_move(s)
#         if action not in actions(s):
#             print("Illegal move made by Black")
#             print("White wins!")
#             return
#         s = result(s, action)
#         if terminal_test(s):
#             print("Game Over")
#             display(s)
#             display_final(s)
#             return
#         action = p2.make_move(s)
#         if action not in actions(s):
#             print("Illegal move made by White")
#             print("Black wins!")
#             return
#         s = result(s, action)
#         if terminal_test(s):
#             print("Game Over")
#             display(s)
#             display_final(s)
#             return
#
#
# def main():
#     # depth_limit = 3
#     # p1 = MinimaxPlayer(BLACK, depth_limit)
#     # p2 = AlphaBetaPlayer(WHITE, depth_limit)
#     # print("Running p1 = minimax(black) vs. p2 = alpha_beta(white)    - depth limit =", depth_limit, " for both players")
#     # play_game(p1, p2)
#     # print_time()
#     #
#     # print()
#     # print("##################################################################")
#     # print()
#     #
#     # time_reset()
#     # p1 = MinimaxPlayer(BLACK, 1)
#     # p2 = AlphaBetaPlayer(WHITE, 4)
#     # print("Running p1 = minimax(black, depth_limit = 2) vs. p2 = alpha_beta(white, depth_limit = 4) ")
#     # play_game(p1, p2)
#     # print_time()
#     #
#     # print()
#     # print("##################################################################")
#     # print()
#     #
#     # time_reset()
#     # p1 = MinimaxPlayer(BLACK, 4)
#     # p2 = AlphaBetaPlayer(WHITE, 1)
#     # print("Running p1 = minimax(black, depth_limit = 4) vs. p2 = alpha_beta(white, depth_limit = 2) ")
#     # play_game(p1, p2)
#     # print_time()
#     #
#     # print()
#     # print("##################################################################")
#     # print()
#     #
#     # time_reset()
#     # p1 = AlphaBetaPlayer(WHITE, 4)
#     # p2 = RandomPlayer(BLACK)
#     # print("Running p1 = alpha_beta(white, depth_limit = 4) vs. p2 = RandomPlayer(Black)")
#     # play_game(p1, p2)
#     # print_time()
#     # print()
#
#     print(" HW 3 - ALEXANDER BESCH - BESCH040")
#     print("This will take roughly 35 seconds to run")
#     print()
#
#
#     # time_reset()
#     # p1 = AlphaBetaPlayer(WHITE, 4)
#     # p2 = RandomPlayer(BLACK)
#     # print("Running p1 = alpha_beta(white, depth_limit = 4) vs. p2 = RandomPlayer(Black)")
#     # play_game(p1, p2)
#     # print_time()
#     #
#     # print()
#     # print("##################################################################")
#     # print()
#
#     time_reset()
#     p1 = AlphaBetaPlayer(BLACK, 4)
#     p2 = HumanPlayer(WHITE)
#     #p2 = RandomPlayer(WHITE)
#     print("Running p1 = alpha_beta(Black, depth_limit = 4) vs. p2 = RandomPlayer(White)")
#     play_game(p1, p2)
#     print_time()
#     print()
#
#
# if __name__ == '__main__':
#     main()
#
#
#
#
#
#
#
# #
# # TIME_LIMIT = 5
# #
# #
# # def index(x, y):
# #     x -= 1
# #     y -= 1
# #     return ((x//3)*27) + ((x % 3)*3) + ((y//3)*9) + (y % 3)
# #
# #
# # def box(x, y):
# #     return index(x, y) // 9
# #
# #
# # def next_box(i):
# #     return i % 9
# #
# #
# # def indices_of_box(b):
# #     return list(range(b*9, b*9 + 9))
# #
# #
# # def print_board(state):
# #     for row in range(1, 10):
# #         row_str = ["|"]
# #         for col in range(1, 10):
# #             row_str += [state[index(row, col)]]
# #             if (col) % 3 == 0:
# #                 row_str += ["|"]
# #         if (row-1) % 3 == 0:
# #             print("-"*(len(row_str)*2-1))
# #         print(" ".join(row_str))
# #     print("-"*(len(row_str)*2-1))
# #
# #
# # def add_piece(state, move, player):
# #     if not isinstance(move, int):
# #         move = index(move[0], move[1])
# #     return state[: move] + player + state[move+1:]
# #
# #
# # def update_box_won(state):
# #     temp_box_win = ["."] * 9
# #     for b in range(9):
# #         idxs_box = indices_of_box(b)
# #         box_str = state[idxs_box[0]: idxs_box[-1]+1]
# #         temp_box_win[b] = check_small_box(box_str)
# #     return temp_box_win
# #
# #
# # def check_small_box(box_str):
# #     global possible_goals
# #     for idxs in possible_goals:
# #         (x, y, z) = idxs
# #         if (box_str[x] == box_str[y] == box_str[z]) and box_str[x] != ".":
# #             return box_str[x]
# #     return "."
# #
# #
# # def possible_moves(last_move):
# #     global box_won
# #     if not isinstance(last_move, int):
# #         last_move = index(last_move[0], last_move[1])
# #     box_to_play = next_box(last_move)
# #     idxs = indices_of_box(box_to_play)
# #     if box_won[box_to_play] != ".":
# #         pi_2d = [indices_of_box(b) for b in range(9) if box_won[b] == "."]
# #         possible_indices = list(itertools.chain.from_iterable(pi_2d))
# #     else:
# #         possible_indices = idxs
# #     return possible_indices
# #
# #
# # def successors(state, player, last_move):
# #     succ = []
# #     moves_idx = []
# #     possible_indexes = possible_moves(last_move)
# #     for idx in possible_indexes:
# #         if state[idx] == ".":
# #             moves_idx.append(idx)
# #             succ.append(add_piece(state, idx, player))
# #     return zip(succ, moves_idx)
# #
# #
# # def print_successors(state, player, last_move):
# #     for st in successors(state, player, last_move):
# #         print_board(st[0])
# #
# #
# # def opponent(p):
# #     return "O" if p == "X" else "X"
# #
# #
# # def evaluate_small_box(box_str, player):
# #     global possible_goals
# #     score = 0
# #     three = Counter(player * 3)
# #     two = Counter(player * 2 + ".")
# #     one = Counter(player * 1 + "." * 2)
# #     three_opponent = Counter(opponent(player) * 3)
# #     two_opponent = Counter(opponent(player) * 2 + ".")
# #     one_opponent = Counter(opponent(player) * 1 + "." * 2)
# #
# #     for idxs in possible_goals:
# #         (x, y, z) = idxs
# #         current = Counter([box_str[x], box_str[y], box_str[z]])
# #
# #         if current == three:
# #             score += 100
# #         elif current == two:
# #             score += 10
# #         elif current == one:
# #             score += 1
# #         elif current == three_opponent:
# #             score -= 100
# #             return score
# #         elif current == two_opponent:
# #             score -= 10
# #         elif current == one_opponent:
# #             score -= 1
# #
# #     return score
# #
# #
# # def evaluate(state, last_move, player):
# #     global box_won
# #     score = 0
# #     score += evaluate_small_box(box_won, player) * 200
# #     for b in range(9):
# #         idxs = indices_of_box(b)
# #         box_str = state[idxs[0]: idxs[-1]+1]
# #         score += evaluate_small_box(box_str, player)
# #     return score
# #
# #
# # def minimax(state, last_move, player, depth, s_time):
# #     succ = successors(state, player, last_move)
# #     best_move = (-inf, None)
# #     for s in succ:
# #         val = min_turn(s[0], s[1], opponent(player), depth-1, s_time,
# #                        -inf, inf)
# #         if val > best_move[0]:
# #             best_move = (val, s)
# # #        print("val = ", val)
# # #        print_board(s[0])
# #     return best_move[1]
# #
# #
# # def min_turn(state, last_move, player, depth, s_time, alpha, beta):
# #     global box_won
# #     if depth <= 0 or check_small_box(box_won) != ".":# or time() - s_time >= 10:
# #         return evaluate(state, last_move, opponent(player))
# #     succ = successors(state, player, last_move)
# #     for s in succ:
# #         val = max_turn(s[0], s[1], opponent(player), depth-1, s_time,
# #                        alpha, beta)
# #         if val < beta:
# #             beta = val
# #         if alpha >= beta:
# #             break
# #     return beta
# #
# #
# # def max_turn(state, last_move, player, depth, s_time, alpha, beta):
# #     global box_won
# #     if depth <= 0 or check_small_box(box_won) != ".":# or time() - s_time >= 20:
# #         return evaluate(state, last_move, player)
# #     succ = successors(state, player, last_move)
# #     for s in succ:
# #         val = min_turn(s[0], s[1], opponent(player), depth-1, s_time,
# #                        alpha, beta)
# #         if alpha < val:
# #             alpha = val
# #         if alpha >= beta:
# #             break
# #     return alpha
# #
# #
# # def valid_input(state, move):
# #     global box_won
# #     if not (0 < move[0] < 10 and 0 < move[1] < 10):
# #         return False
# #     if box_won[box(move[0], move[1])] != ".":
# #         return False
# #     if state[index(move[0], move[1])] != ".":
# #         return False
# #     return True
# #
# #
# # def take_input(state, bot_move):
# #     print("#" * 40)
# #     all_open_flag = False
# #     if bot_move == -1 or len(possible_moves(bot_move)) > 9:
# #         all_open_flag = True
# #     if all_open_flag:
# #         print("Play anywhere you want!")
# #     else:
# #         box_dict = {0: "Upper Left", 1: "Upper Center", 2: "Upper Right",
# #                     3: "Center Left", 4: "Center", 5: "Center Right",
# #                     6: "Bottom Left", 7: "Bottom Center", 8: "Bottom Right"}
# #         print("Where would you like to place 'X' in ~"
# #               + box_dict[next_box(bot_move)] + "~ box?")
# #     x = int(input("Row = "))
# #     if x == -1:
# #         raise SystemExit
# #     y = int(input("Col = "))
# #     print("")
# #     if bot_move != -1 and index(x, y) not in possible_moves(bot_move):
# #         raise ValueError
# #     if not valid_input(state, (x, y)):
# #         raise ValueError
# #     return (x, y)
# #
# #
# # def game(state="." * 81, depth=20):
# #     global box_won, possible_goals
# #     possible_goals = [(0, 4, 8), (2, 4, 6)]
# #     possible_goals += [(i, i+3, i+6) for i in range(3)]
# #     possible_goals += [(3*i, 3*i+1, 3*i+2) for i in range(3)]
# #     box_won = update_box_won(state)
# #     print_board(state)
# #     bot_move = -1
# #
# #     while True:
# #         try:
# #             user_move = take_input(state, bot_move)
# #         except ValueError:
# #             print("Invalid input or move not possible!")
# #             print_board(state)
# #             continue
# #         except SystemError:
# #             print("Game Stopped!")
# #             break
# #
# #         user_state = add_piece(state, user_move, "X")
# #         print_board(user_state)
# #         box_won = update_box_won(user_state)
# #
# #         game_won = check_small_box(box_won)
# #         if game_won != ".":
# #             state = user_state
# #             break
# #
# #         print("Please wait, Bot is thinking...")
# #         s_time = time()
# #         bot_state, bot_move = minimax(user_state, user_move, "O", depth,
# #                                       s_time)
# #
# #         print("#" * 40)
# #         print("Bot placed 'O' on", bot_move, "\n")
# #         print_board(bot_state)
# #         state = bot_state
# #         box_won = update_box_won(bot_state)
# #         game_won = check_small_box(box_won)
# #         if game_won != ".":
# #             break
# #
# #     if game_won == "X":
# #         print("$$$$$ Congratulations YOU WIN! $$$$$")
# #     else:
# #         print("~~~~~ YOU LOSE! ~~~~~")
# #
# #     return state
# #
# #
# # if __name__ == "__main__":
# #
# #     INITIAL_STATE = "." * 81
# #     final_state = game(INITIAL_STATE, depth=5)

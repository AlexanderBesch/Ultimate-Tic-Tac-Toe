### Implement the player Classes Here.
# Import the other file funtions here, check this at end.
import gameuttt as game
from random import choice

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
        return move

class HumanPlayer(UtttPlayerTemplate):
    def make_move(self, state):
        curr_move = None
        legal_moves = game.actions(state)
        print(state)
        while curr_move==None:
            if self.sign == 'X':
                print("X", end='')
            else:
                print("O",end='')
            print(' to play.')
            print(f'Legal Moves are : {legal_moves}')
            input_move = input('Enter your move as mb,r,c pair. mb is the board number, r, c are row and column index inside the mb where you want to make the move:\n')
            if input_move == '':
                print('No move was provided. Hence first move from above list was selected.')
                return legal_moves[0]
            else:
                try:
                    move = tuple(map(int,input_move.split(',')))
                except ValueError:
                    print('Enter Integer Values.')
                    continue
                if len(move) != 3:
                    print("Not a valid move.")
                    continue
                else:
                    if (move[0] < 9 and move[0] >= 0) or (move[1]< 3 and move[1] >= 0) or (move[2]< 3 and move[2] >= 0):
                        curr_move = move
                    else:
                        print("Not a valid Move.")
                        continue
        return curr_move


class MinimaxPlayer:
    def __init__(self, depth_limit, player_char):
        self.depth_limit = depth_limit
        self.sign = player_char
    def make_move(self, state):
        value, move = game.max_value(state, self.depth_limit, self.sign)
        return move

    def get_sign(self):
        return self.sign


class AlphaBetaPlayer:
    def __init__(self, depth_limit, player_char):
        self.depth_limit = depth_limit
        self.sign = player_char

    def make_move(self, state):
        value, move = game.max_value_alpha_beta(state, self.depth_limit, self.sign, float('-inf'), float('inf'))
        return move

    def get_sign(self):
        return self.sign


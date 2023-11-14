import random
import copy
import time
import GameClass

WHITE = 1
BLACK = -1
EMPTY = 0
BLOCKED = -2
SIZE = 8
SKIP = "SKIP"



# class OthelloPlayerTemplate:
#     '''Template class for an Othello Player
#
#     An othello player *must* implement the following methods:
#
#     get_color(self) - correctly returns the agent's color
#
#     make_move(self, state) - given the state, returns an action that is the agent's move
#     '''
#
#     def __init__(self, mycolor):
#         self.color = mycolor
#
#     def get_color(self):
#         return self.color
#
#     def make_move(self, state):
#         '''Given the state, returns a legal action for the agent to take in the state
#         '''
#         return None


class RandomPlayer:
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
        action_list = actions(state)
        action_taken = random.choice(action_list)

        return action_taken


class AlphaBetaPlayer:
    '''Template class for an Othello Player

    An othello player *must* implement the following methods:

    get_color(self) - correctly returns the agent's color

    make_move(self, state) - given the state, returns an action that is the agent's move
    '''

    def __init__(self, mycolor, depth_limit):
        self.color = mycolor
        self.depth_limit = depth_limit

    def get_color(self):
        return self.color

    def make_move(self, state):
        '''Given the state, returns a legal action for the agent to take in the state
        '''

        value, move = max_value_alpha_beta(state, self.depth_limit, self.color, float('-inf'), float('inf'))

        return move
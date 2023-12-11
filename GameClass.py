#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Pulkit Maloo
"""

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

from math import inf
from collections import Counter
import itertools
from time import time



'''
randothellogame module

sets up a RandOthello game closely following the book's framework for games

RandOthelloState is a class that will handle our state representation, then we've 
got stand-alone functions for player, actions, result and terminal_test

Differing from the book's framework, is that utility is *not* a stand-alone 
function, as each player might have their own separate way of calculating utility

Black is -1
White is 1
X is -2
array is 8x8, when printing state, columns are the rows
'''

# README

# HW 3 - ALEXANDER BESCH - BESCH040
# This will take roughly 35 seconds to run




import random
import copy
import time
import PlayerClasses

WHITE = 1
BLACK = -1
EMPTY = 0
BLOCKED = -2
SIZE = 8
SKIP = "SKIP"





def max_value_alpha_beta(state, depth, player, alpha, beta):
    if terminal_test(state) or depth == 0:
        return utilityFunction(state, player), None
    val = float('-inf')
    for a in actions(state):
        [v2, a2] = min_value_alpha_beta(result(state, a), depth - 1, player, alpha, beta)
        if v2 > val:
            val, move = v2, a
            alpha = max(alpha, val)
        if val >= beta:
            return val, move
    # print("Move: ", move)
    return val, move


def min_value_alpha_beta(state, depth, player, alpha, beta):
    if terminal_test(state) or depth == 0:
        return utilityFunction(state, player), None
    val = float('inf')
    for a in actions(state):
        [v2, a2] = max_value_alpha_beta(result(state, a), depth - 1, player, alpha, beta)
        if v2 < val:
            val, move = v2, a
            beta = min(beta, val)
        if val <= alpha:
            return val, move
    return val, move


class MinimaxPlayer:
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
        colorName = "WHITE"
        if self.color == -1:
            colorName = "BLACK"

        # print("#############  ", colorName, "  #############")
        # print("Before Running MiniMax, current utility: ", utilityFunction(state, self.color), "", end="")
        start = time.time()
        value, move = max_value(state, self.depth_limit, self.color)
        stop = time.time()
        add_time(self.color, stop - start)
        # print(", After: ", utilityFunction(result(state, move), self.color))
        # print("Available Actions: ", actions(state))
        # print("Chosen results: Value: ", value, " Move: ", move)

        return move


def max_value(state, depth, player):
    if terminal_test(state) or depth == 0:
        return utilityFunction(state, player), None
    val = float('-inf')
    for a in actions(state):
        [v2, a2] = min_value(result(state, a), depth - 1, player)
        if v2 > val:
            val, move = v2, a
    # print("Move: ", move)
    return val, move


def min_value(state, depth, player):
    if terminal_test(state) or depth == 0:
        return utilityFunction(state, player), None
    val = float('inf')
    for a in actions(state):
        [v2, a2] = max_value(result(state, a), depth - 1, player)
        if v2 < val:
            val, move = v2, a
    return val, move


class HumanPlayer(OthelloPlayerTemplate):
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        colorName = "WHITE"
        if self.color == -1:
            colorName = "BLACK"

        print("#############  ", colorName, "  #############")
        print("Before move, current utility: ", utilityFunction(state, self.color))

        curr_move = None
        legals = actions(state)
        while curr_move == None:
            display(state)
            if self.color == 1:
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Utility function is: ", utilityFunction(state, self.color))
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

            print("After move, current utility: ", utilityFunction(result(state, curr_move), self.color))
        return curr_move


class RandOthelloState:
    '''A class to represent an othello game state'''

    def __init__(self, currentplayer, otherplayer, board_array=None, num_skips=0):
        if board_array != None:
            self.board_array = board_array
        else:
            self.board_array = [[EMPTY] * SIZE for i in range(SIZE)]
            self.board_array[3][3] = WHITE
            self.board_array[4][4] = WHITE
            self.board_array[3][4] = BLACK
            self.board_array[4][3] = BLACK
            x1 = random.randrange(8)
            x2 = random.randrange(8)
            self.board_array[x1][0] = BLOCKED
            self.board_array[x2][7] = BLOCKED
        self.num_skips = num_skips
        self.current = currentplayer
        self.other = otherplayer










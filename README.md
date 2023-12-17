# Ultimate-Tic-Tac-Toe

Ultimate Tic Tac Toe Game This project implements an ultimate tic tac toe game in Python. The game features AI players using different algorithms.

Files: gameuttt.py - Contains the game logic and rules, including the UtttState class to represent game states, functions to get legal moves, make moves, and check for end of game.

heuristics.py - Contains different heuristic evaluation functions to estimate the value of game states.

players.py - Defines different AI player classes like:

RandomPlayer - Chooses moves randomly
MinimaxPlayer - Uses minimax search
AlphaBetaPlayer - Uses alpha-beta pruning search
HumanPlayer - Allows human input through console All players inherit from a UtttPlayerTemplate base class.
Game Rules The game is played on a 3x3 board of tic tac toe boards. Players take turns making a move on one of the smaller tic tac toe boards, attempting to make 3-in-a-row. Once a small board is won by a player, no more moves can be made on that board. The first player to get 3-in-a-row on the master 3x3 board wins.

Running the Game The main driver code is in gameuttt.py. This allows configuring different players to face off against each other.

Modify the main() function to configure players.

Future Work Add GUI for better visualization Experiment with more sophisticated heuristics and search algorithms Parameterize search depth, exploration rules etc. Maintain standings over multiple games

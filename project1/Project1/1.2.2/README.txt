Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Task 1.2: simple strategies for tic tac toe
		2. implement a heuristic strategy

The strategy that we followed was to construct a game tree and apply a modified version of the MinMax algorithm. The MinMax algorithm works well when you assume that the opponent also plays infallibly. In our task our opponent plays randomly. So the modification was applied at the ''Min'' step. Instead of choosing the next state based on the minimum score, the average score is taken for this step. The max player plays the same by choosing the maximum score next state.

The tictactoe.py was modified by changing the moves of player 'X' by choosing moves cleverly. After the tree has been built, a hashtable is created with all the states and best_moves for each state.

The two files used for this task:
ai.py - This learns the tree and contains the hashtable.
tictactoe.py - This runs the tournament.


To run the code use the following command:

python tictactoe.py 


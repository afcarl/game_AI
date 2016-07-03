Project 1
===============================================
**Task:** Implement a probabilistic strategy; have both players play many games (at least 1000) in order to create a statistic of auspicious positions on the tic tac toe board. After the whole tournament, plot a histogram of wins and draws.
After each game in the tournament that did not end in a draw, check which player has won and determine the fields this player
occupied in order to count for each field how often it contributed to a win. Properly normalize your count data (such that
they sum to one) and store them on disk. Now implement a function that realizes a game move using the probabilities you just
determined. Use this function for the moves of player X and have player O move at random. Start another tournament and plot 
the new histogram of wins and draws

**Solution:** The first part of the exercise, i.e. "have both players play many games (at least 1000).
After the whole tournament, plot a histogram of wins and draws" and the collection of the count data is in the file
"part1_tournament_1.py"

The second part of the exercise, i.e. "implement a function that realizes a game move using the probabilities you just 
determined" and "start another tournament and plot the new histogram of wins and draws" is in the file "part2_tournament_2.py"

Both files can be run from the terminal with the following commands:

	python part1_tournament_1.py

	python part2_tournament_2.py

'''
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise: 1.2.2: Implement a heuristic strategy
'''

import numpy as np
import ai as ai
import time
import matplotlib.pyplot as plt


def move_still_possible(S):
    return not (S[S==0].size == 0)

def move_at_random(S, p):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]

    S[xs[i],ys[i]] = p

    return S

def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False


def plot_presentation_figures():

    dictionary_sizes = [5478, 4678, 1175, 645]
    num_nodes = [16168, 10870, 2737, 1534]
    times = [0.857, 0.6222, 0.2535, 0.2391]

    plt.figure()
    plt.title("Number of nodes in tree")
    #plt.title("Optimization results on learning the tree")
    axes = plt.gca()
    plt.plot(dictionary_sizes, 'ro-')
   #plt.plot(num_nodes, 'bo-')

    axes.set_xticks([0, 1, 2, 3])
    axes.set_xticklabels( ('Base', 'Trivial\n Checks', 'Checking\n Rotations', 'Checking\n Mirroring') )
    #plt.legend(["Number of nodes in tree"])

    plt.savefig('hashtable_and_nodes.png')

    plt.figure()
    plt.title("Time (in seconds) to learn tree")
    axes = plt.gca()
    plt.plot(times, 'go-')
    axes.set_xticks([0, 1, 2, 3])
    axes.set_xticklabels( ('Base', 'Trivial\n Checks', 'Checking\n Rotations', 'Checking\n Mirroring') )


    plt.savefig('time_to_learn.png')

# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B





if __name__ == '__main__':
    # initialize 3x3 tic tac toe board
    tic = time.time()
    ai.build_tree_and_learn()
    tac = time.time()
    print "Time to learn = ", tac-tic, " seconds."

    i=0
    results = []
    x_wins = 0
    draws = 0
    o_wins = 0
    for i in xrange(2000):
#        print "Playing Game: ", i
#        print "---------------------------------------------------------------"
        gameState = np.zeros((3,3), dtype=int)
        # initialize player number, move counter
        player = 1
        mvcntr = 1
        # initialize flag that indicates win
        noWinnerYet = True

        while move_still_possible(gameState) and noWinnerYet:
            # get player symbol
            name = symbols[player]
#                print '%s moves' % name

            if player == -1:
                # let player move at random
                gameState = move_at_random(gameState, player)
            else:
                [y, x] = ai.make_best_move(gameState)
                if y == None:
                    #Should never get in here... Only if a certain board has NEVER been seen before
                    gameState = move_at_random(gameState, player)
                else:
                    gameState[y, x] = player

            # print current game state
#            print_game_state(gameState)
            # evaluate game stte
            if move_was_winning_move(gameState, player):
                results.append(player)
                if player==1:
                    x_wins += 1
                else:
                    o_wins += 1
#                print 'player %s wins after %d moves' % (name, mvcntr)
                noWinnerYet = False
                p = player
                

            # switch player and increase move counter
            player *= -1
            mvcntr +=  1
        if noWinnerYet:
#                print 'game ended in a draw'
            results.append(0)
            draws += 1
    i += 1
    print "End of tournament\n================"
    print "X_WINS = ", x_wins
    print "O_WINS = ", o_wins
    print "Draws  = ", draws

    his = plt.hist(results, bins = [-1, -0.3333333333333333, 0.3333333333333334, 1])
    offset = -.3
    plt.title("Tournament, draws and wins")
    plt.ylabel("#Games")
    axes = plt.gca()
    axes.set_ylim([0,2100]) # y axis should include all 2000 games
    axes.set_xlim([-1.0,1.0])
    axes.set_xticks(his[1][1:]+offset)
    axes.set_xticklabels( ('O wins', 'draw', 'X wins') )
    plt.savefig('tournament_3.png')


    plot_presentation_figures()

    plt.show()


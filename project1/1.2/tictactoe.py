
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
    x_wins = 0    
    draws = 0
    o_wins = 0
    
    outcomes = np.array([])    
    
    for i in range(10000):
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
                gameState[y, x] = player
    
            # print current game state
#            print_game_state(gameState)
            
            # evaluate game state
            if move_was_winning_move(gameState, player):
                outcomes = np.append(outcomes,player)
                if player==1:
                    x_wins += 1
                else:
                    o_wins += 1
#                print 'player %s wins after %d moves' % (name, mvcntr)
                noWinnerYet = False
    
            # switch player and increase move counter
            player *= -1
            mvcntr +=  1
        if noWinnerYet:
#                print 'game ended in a draw' 
            outcomes = np.append(outcomes,0)
            draws += 1
            
            
    i += 1                   
    print "End of tournament\n================"
    print "X_WINS = ", x_wins
    print "O_WINS = ", o_wins
    print "Draws  = ", draws
    
        # Plot the data in 'outcomes' as a histogram
    plt.hist(outcomes, bins=[-1, -0.3333333333333333, 0.3333333333333334, 1])
    plt.title("3. Tournament, draws and wins")
    plt.xlabel("left: o wins, middle: draw, right: x wins")
    plt.ylabel("# Games") 
    axes = plt.gca()
    axes.set_ylim([0,10500]) # y axis should include all 2000 games
    axes.set_xlim([-1.0,1.0])

    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off
        
        
    plt.savefig('tournament_3.png')



import numpy as np
import matplotlib.pyplot as plt


# try not to use loops!!!

def move_still_possible(S):
    return not (S[S==0].size == 0)
    
    # S == 0 counts the number of 0's in state S
    # If no 0's are in the state, no further move is possible!


def move_at_random(S, p):
    xs, ys = np.where(S==0) # return the indices of entries equal to 0

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
    print (B)





if __name__ == '__main__':
    
    # initialize array that counts how often a cell contributed to a win
    final = np.zeros((3,3), dtype = float)     
    
    # initialize array which stores if a game ended in a win or draw
    outcomes = np.array([])

    for i in range(0,2000):

        # initialize 3x3 tic tac toe board
        gameState = np.zeros((3,3), dtype=int)
    
        # initialize player number, move counter
        player = 1
        mvcntr = 1
    
        # initialize flag that indicates win
        noWinnerYet = True
        
    
        while move_still_possible(gameState) and noWinnerYet:
            # get player symbol
            name = symbols[player]
            print '%s moves' % name
    
            # let player move at random
            gameState = move_at_random(gameState, player)
    
            #print current game state
            print_game_state(gameState)
            
            # evaluate game state
            if move_was_winning_move(gameState, player):
                # append 1 to 'outcomes' indicating that the game was won
                outcomes = np.append(outcomes,player)
                
                print 'player %s wins after %d moves' % (name, mvcntr)
                
                # determine who won
                winner = player
                # get the positions of the fields the winner selected
                xp, yp = np.where(gameState == winner)
                # update "final" which counts how often a cell contributed
                # to a win
                final[xp,yp] +=1
                
                noWinnerYet = False
    
            # switch player and increase move counter
            player *= -1
            mvcntr +=  1
    
        if noWinnerYet:
            print 'game ended in a draw'
            # append 0 to 'outcomes' indicating that the game ended in a draw
            outcomes = np.append(outcomes,0)
    
    
    # normalize the count data and store it on disk
    final_sum = final.sum()
    normed_final = final/final_sum
    print normed_final
    np.savetxt("normed_count.csv", normed_final, delimiter=",")    
    
    # Plot the data in 'outcomes' as a histogram
    plt.hist(outcomes, bins=[-1, -0.3333333333333333, 0.3333333333333334, 1])
    plt.title("1. Tournament, draws and wins")
    plt.xlabel("left: o wins, middle: draw, right: x wins")
    plt.ylabel("# Games") 
    axes = plt.gca()
    axes.set_ylim([0,2100]) # y axis should include all 2000 games
    axes.set_xlim([-1.0,1.0])

    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off
        
        
    plt.savefig('tournament_1.png')
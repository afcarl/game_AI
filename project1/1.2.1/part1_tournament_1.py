'''
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 1.2.1: Implement a probabilistic strategy, Part 1
'''

import numpy as np
import matplotlib.pyplot as plt


def move_still_possible(S):
    '''
    Checks whether there still exist empty positions in state S.
    S == 0 counts the number of 0's in state S.
    If no 0's are in the state, no further move is possible!
    '''
    return not (S[S==0].size == 0)
    

def move_at_random(S, p):
    '''
    This function performs a random move.
    '''
    xs, ys = np.where(S==0) 

    i = np.random.permutation(np.arange(xs.size))[0]
    
    S[xs[i],ys[i]] = p

    return S


def move_was_winning_move(S, p):
    '''
    This function checks whether player p has won by checking both diagonals, 
    all columns and all rows.
    '''
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
    '''
    Prints the game board as ASCII characters
    '''
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print (B)



if __name__ == '__main__':
    
    # initialize array that counts how often a cell contributed to a win
    final = np.zeros((3,3), dtype = float)     
    
    # initialize array which stores if a game ended in a win or draw
    outcomes = np.array([])

    # Let the players play 2000 games against each other
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
            #print '%s moves' % name
    
            # let player move at random
            gameState = move_at_random(gameState, player)
    
            #print current game state
            #print_game_state(gameState)
            
            # evaluate game state
            if move_was_winning_move(gameState, player):
                # append 1 to 'outcomes' indicating that the game was won
                outcomes = np.append(outcomes,player)
                
                #print 'player %s wins after %d moves' % (name, mvcntr)
                
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
            #print 'game ended in a draw'
            # append 0 to 'outcomes' indicating that the game ended in a draw
            outcomes = np.append(outcomes,0)
    
    
    # normalize the count data and store it on disk
    final_sum = final.sum()
    normed_final = final/final_sum
    np.savetxt("normed_count.csv", normed_final, delimiter=",")    
    
    # Plot the data in 'outcomes' as a histogram
    his = plt.hist(outcomes, bins=[-1, -0.3333333333333333, 0.3333333333333334, 1])
    offset = -.3
    plt.title("1st Tournament, draws and wins")
    plt.ylabel("# Games") 
    axes = plt.gca()
    axes.set_ylim([0,2100]) # y axis should include all 2000 games
    axes.set_xlim([-1.0,1.0])
    axes.set_xticks(his[1][1:]+offset)
    axes.set_xticklabels( ('O wins', 'draw', 'X wins') )   
     
    plt.show()

import numpy as np

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

    # initialize array that counts how often a cell contributed to a win
    final = np.zeros((3,3), dtype = float)    
    
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

            # print current game state
            print_game_state(gameState)
            
            # evaluate game state
            if move_was_winning_move(gameState, player):
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
        
    # normalize the count data and store it on disk
    #normed_final = (normalize(final, norm='l1'))
    final_sum = final.sum()
    normed_final = final/final_sum
    print normed_final
    np.savetxt("normed_count.csv", normed_final, delimiter=",")
    
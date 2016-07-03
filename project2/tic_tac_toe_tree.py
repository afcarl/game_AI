'''
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 2.1: The tic tac toe game tree
'''

import numpy as np

x_wins = 0
o_wins = 0
num_nodes_in_tree = 1
num_leaves_in_tree = 0
children = []


class Node(object):
    '''
    Each node in the tree is a Node object. It contains all information needed
    about the game states.
    ''' 
    
    def __init__(self, board):
        '''
        @param board: (1-d numpy.array) This is the game state. All X positions
                        are marked as 1, O positions as -1 and unoccupied as 0.
        @children: A list of the children of the current node
        @attribute score: (double) - Each node has a score that depends on the
                         game state. It's either 1 (X won), -1 (O won) or 0 (else)
        '''           
        self.board = board
        self.children = []
        self.score = self.get_score()
       
    def __str__(self):
        tmp = np.reshape(self.board, (3, 3))
        s = ""
        for i in xrange(len(tmp)):
            for j in xrange(len(tmp[0])):
                s = "%s \t %d"%(s, tmp[i][j])
            s = "%s \n"%s
        return s

    def get_score(self):
        '''
        Returns the an integer indicating if player 1 is winning or player 2 
        or a draw
    
        @param b (1 x 9 array) - The current board
        @return score (int) - Returns the score of the current board
        '''
        board = np.reshape(self.board, (3, 3))
        vertical = np.sum(board, axis=0)
        horizontal = np.sum(board, axis=1)
        diagonal = np.array([np.trace(board), np.trace(board[::-1])])
        all_ = np.hstack((horizontal, vertical, diagonal))
    
        if 3 in all_:   return 1.0
        elif -3 in all_:    return -1.0
        return 0.0
        
def print_game_state(board):
    '''
    Prints the game board as ASCII characters
    '''
    board = np.reshape(board, (3, 3))
    B = np.copy(board).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B        
        
# We start with an empty board, it's player 1's turn
board = np.zeros(9, int)
a = Node(board)
player = 1

# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}


def build_tree(a,player):
    '''
    Builds the full tic tac toe game tree
    '''
    global x_wins
    global o_wins
    global num_nodes_in_tree
    global num_leaves_in_tree
    
    # Determine the free positions on the board
    zeros_pos = np.where(a.board==0)[0]
    
    # If the board is full and has a score of 0, the game ended in a draw
    if len(zeros_pos) == 0 and a.score == 0:
        num_leaves_in_tree += 1
        return
                
    # If the score is 1, X won
    if a.score == 1:
        x_wins += 1
        num_leaves_in_tree += 1
        return
        
    # If the score is -1, O won
    if a.score == -1:
        o_wins += 1
        num_leaves_in_tree += 1
        return 

    children.append(len(zeros_pos))
    
    # If none of the above cases holds, we further expand the tree by creating
    # a new child for every possible empty position on the board
    for i in zeros_pos:
        copy_board = np.copy(a.board)
        copy_board[i] = player
        b = Node(copy_board)
        num_nodes_in_tree += 1
        
        a.children.append(b)
        build_tree(b,player *-1)

# Start the building process
build_tree(a,player)

print "number of times x wins: ", x_wins
print "number of times o wins: ", o_wins
print "number of nodes: ", num_nodes_in_tree
print "number of leaves in tree: ", num_leaves_in_tree
print "number of nodes that have children: ", len(children)
print "number of children: ", np.sum(children)
print "branching factor: ", float(np.sum(children)) / float(len(children))

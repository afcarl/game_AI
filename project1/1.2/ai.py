import numpy as np

DICTIONARY = {}

class Mappings(object):
    '''
    The following lists allow us to map the board positions from the 
    base board to the transformed board. Each index in the
    list is the position of the base board and the element at that index 
    indicates where the same position would be transformed to after applying
    the respective transformation.
    
    It has mappings for all 3 rotations (90, 180, 270) and mirroring transformations
    along the x-, y- and diagonal axes.
    '''
    trans_rot270 = [6, 3, 0, 7, 4, 1, 8, 5, 2]
    trans_rot180 = [8, 7, 6, 5, 4, 3, 2, 1, 0]
    trans_rot90 = [2, 5, 8, 1, 4, 7, 0, 3, 6]
    
    fliptd = [6, 7, 8, 3, 4, 5, 0, 1, 2]
    fliplr = [2, 1, 0, 5, 4, 3, 8, 7, 6]
    flip_diag_main = [0, 3, 6, 1, 4, 7, 2, 5, 8]
    flip_diag_rev = [8, 5, 2, 7, 4, 1, 6, 3, 0]

# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

class Node(object):
    '''
    Each node in the tree is an Node object. It contains all information needed
    about the game states. This is only used to build the tree while learning, once
    the learning process is complete ALL nodes are not required anymore as all
    information we need is saved in the hash table (dictionary)
    '''
    def __init__(self, board, depth):
        '''
        @param board: (1-d numpy.array) This is the game state. All X positions
                    are marked as 1, 0 positions as -1 and unoccupied as 0.
        @param depth: (integer) - Indicates the depth of this node in the tree.
        
        @attribute best_move: (integer) - It describes the ``best" move for the
                    current game state. This changes as the tree is built and 
                    expanded.
        @attribute score: (double) - This is the score for each board state. Initialy it
                    is calculated based on the current state, which is either 1 for
                    win board -1 for loose board and 0 for draw board. During the
                    learning process this will change depending on the algorithm.
                    This score is used to make decisions about next best move.
        '''
        self.board = board
        self.key = get_hash_key(board)
        self.score = get_score(board)
        self.depth = depth
        self.best_move = -1
        
    
        
def get_hash_key(board, matrix=False):
    '''
    This function creates a hashkey for a board so it can be stored in the dictionary.
    
    @param board: (1-d or 2-d numpy.array) This is the game state. It can either 
                be recieved as a 2-d array or 1-d array.
    @param matrix: optional (boolean) - Indicates if the board recieved is
                2-dimensional or 1-dimensional.
                
    @return key: (string) - Contains the unique key of each board. The key
                currently is a basic hash function which concatenates the
                board values into one string. E.g: 111000-1-1-1 for a board
                with a row of X's in the first row and row of O's in the last. 
    '''
    if matrix == True:
        board = np.ndarray.flatten(board)
    string_flat = np.char.mod('%d', board)
    key = "".join(string_flat)
    return key
    
def print_game_state(board):
    '''
    Prints the game board as ASCII characters
    '''
    board = np.reshape(board, (3, 3))
    B = np.copy(board).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B

def get_score(b):
    '''
     Returns the an integer indicating is player 1 is winning or player 2 or a draw
    
    @param b (1 x 9 array) - The current board
    @return score (int) - Returns the score of the current board. (+1/-1 if its a win/loose terminal node)
    '''
    board = np.reshape(b, (3, 3))
    vertical = np.sum(board, axis=0)
    horizontal = np.sum(board, axis=1)
    diagonal = np.array([np.trace(board), np.trace(board[::-1])])
    all_ = np.hstack((horizontal, vertical, diagonal))    
    
    if 3 in all_:   return 1.0
    elif -3 in all_:    return -1.0
    return 0.0

def learn_tree(node, turn):
    '''
    This function does the learning of the tree. It is recursively called at each step
    in the learning process by expanding the tree by generating all possible states that
    can be reached from the current state.

    @param node (Node) - A Node structure that is a node in the tree. It contains
                the current board, best move found so far, score and other things
    @params turn (int) - An integer that indicates which players turn it is. Each depth
                in the tree is alternating between the two players

    '''

    if node.score != 0.0: #Should only go in if score is 1 or -1
        return node.score # Game won or lost
    elif np.count_nonzero(node.board) == 9:
        return 0.0 #Game tied cuz there is no 0 in board anymore and no winner


    if turn == 1:
        #If it is player X turn then check for direct winning moves and if there
        #exists any then immdiately take them. No need to explore all other options
        res = trivial_checks(node.board)
        if res != -1:
            node.score = 1.0
            node.best_move = res
            return node.score           
            
            
    index = np.where(node.board==0)[0]
    running_avg = 0.0    
    for i in index:
        copy_board = np.copy(node.board)
        copy_board[i] = turn
        tmp_node = Node(copy_board, node.depth+1)
        
        score = check_rotations(copy_board, tmp_node.key) 
        if score == None:
            score = check_flips(copy_board)

        if score == None:
            #Have NOT seen this board, any rotation or mirroring of it!
            score = learn_tree(tmp_node, -1*turn)
            DICTIONARY[tmp_node.key] = tmp_node

        #Have seen this or rotation/mirroring of this board
        if turn == 1: #Player X
            #If its player X's turn then player X would ALWAYS choose the best move,
            #so choose the child node with HIGHEST score.
            if score > node.score:
                node.score = score
                node.best_move = i

        else:   #Player O
            #If its player O's turn then player O would choose at random so label this nodes
            #score as the average of all choices as they are all equally likely to be chosen.
            running_avg += score
            
    if turn == -1:
        #O player
        node.score = running_avg/(1.0*len(index))
        return node.score
    else:
        return node.score


def check_flips(board):
    '''
    This function is called during the learning process. It checks if the current
    game state has been seen before. If not, then it checks if any of it flipped mirrored
    boards are in the tree. If it is then it would return its score and the depth of the terminal
    node. Otherwise it returns None to indicate that the board and any of its rotations
    have not been seen yet.

    @params board (1 x 9 array) - Current Board
    @return score (int) - The score is the current score of the board
    '''
    score = None
    M = np.reshape(board, (3, 3))

    #Flip over middle row
    M[[0, 2]] = M[[2, 0]] #Swap first row and last row
    key_flip_td = get_hash_key(M, matrix=True)
    if key_flip_td in DICTIONARY:
        score = DICTIONARY[key_flip_td].score
        return score
    M[[0, 2]] = M[[2, 0]] #Swap back to normal one

#    Flip over middle coloumn
    M[:, [0, 2]] = M[:, [2, 0]] #Swap first col and last col
    key_flip_lr = get_hash_key(M, matrix=True)
    if key_flip_lr in DICTIONARY:
        score = DICTIONARY[key_flip_lr].score
        return score
    M[:, [0, 2]] = M[:, [2, 0]] #Swap back to normal one
    
    #Flip rev diagonal (//)
    M2 = np.fliplr(np.transpose(np.fliplr(M)))
    key_M2 = get_hash_key(M2, matrix=True)
    if key_M2 in DICTIONARY:
        score = DICTIONARY[key_M2].score
        return score

#    #Flip normal diagonal (\\)
#    M1 = np.transpose(M)
#    key_M1 = get_hash_key(M1, matrix=True)
#    if key_M1 in DICTIONARY:
#        score = DICTIONARY[key_M1].score
#        return score
        
    return score
    
def check_rotations(board, key):
    '''
    This function is called during the learning process. It checks if the current
    game state has been seen before. If not, then it checks if any of it rotations are
    in the tree. If it is then it would return its score and the depth of the terminal
    node. Otherwise it returns None to indicate that the board and any of its rotations
    have not been seen yet.
    
    @params board (1 x 9 array) - Current Board
    @return score, terminal_depth (int, int) - The score is the current score of the board, and
                terminal_depth is the depth in the tree where the terminal node of this path
                would lead to is at.
    '''
    score = None
    if key in DICTIONARY:
        score = DICTIONARY[key].score
        return score
        
    matrix = np.reshape(board, (3, 3))
    rot90 = np.rot90(matrix)
    rot90_key = get_hash_key(rot90, matrix=True)
    if rot90_key in DICTIONARY:
        score = DICTIONARY[rot90_key].score
        return score
        
    rot180_key = get_hash_key(board[::-1])
    if rot180_key in DICTIONARY:
        score = DICTIONARY[rot180_key].score
        return score
        
    rot270 = np.rot90(matrix, k=3)
    rot270_key = get_hash_key(rot270, matrix=True)
    if rot270_key in DICTIONARY:
        score = DICTIONARY[rot270_key].score
        return score
        
    return score
    
def get_rotation_best_move(board):
    '''
    This function checks in the dictionary for all board states that can be produced
    by rotating the current board by 90, 180 and 270 degrees. Returns the best move if it has been
    found. This function is never called during the learning process, and only called
    when the game is being played and the AI queries for the next best move.

    @params board (1 x 9 array) - Current Board
    @return (int) - Returns the best location to play next or -1 if none found.
    '''
    best_move = None
    key = get_hash_key(board)
    if key in DICTIONARY:
        best_move = DICTIONARY[key].best_move
        return best_move
        
    matrix = np.reshape(board, (3, 3))
    rot90 = np.rot90(matrix)
    rot90_key = get_hash_key(rot90, matrix=True)
    if rot90_key in DICTIONARY:
        best_move = DICTIONARY[rot90_key].best_move
        best_move = Mappings.trans_rot90[best_move]
        return best_move
    
    rot180_key = get_hash_key(board[::-1])
    if rot180_key in DICTIONARY:
        best_move = DICTIONARY[rot180_key].best_move
        best_move = Mappings.trans_rot180[best_move]
        return best_move
    
    rot270 = np.rot90(matrix, k=3)
    rot270_key = get_hash_key(rot270, matrix=True)
    if rot270_key in DICTIONARY:
        best_move = DICTIONARY[rot270_key].best_move
        best_move = Mappings.trans_rot270[best_move]
        return best_move
    
    return best_move    

def get_flip_best_move(board):
    '''
    This function checks in the dictionary for all board states that can be produced
    by fliping the current board along all axes. Returns the best move if it has been
    found.

    @params board (1 x 9 array) - Current Board
    @return (int) - Returns the best location to play next or -1 if none found.
    '''
    best_move = None
    M = np.reshape(board, (3, 3))
    
    #Flip over middle row
    M[[0, 2]] = M[[2, 0]] #Swap first row and last row
    key_flip_td = get_hash_key(M, matrix=True)
    if key_flip_td in DICTIONARY:
        best_move = DICTIONARY[key_flip_td].best_move
        best_move = Mappings.fliptd[best_move]
        return best_move
    M[[0, 2]] = M[[2, 0]] #Swap back to normal one

    #Flip over middle coloumn
    M[:, [0, 2]] = M[:, [2, 0]] #Swap first col and last col
    key_flip_lr = get_hash_key(M, matrix=True)
    if key_flip_lr in DICTIONARY:
        best_move = DICTIONARY[key_flip_lr].best_move
        best_move = Mappings.fliplr[best_move]
        return best_move
    M[:, [0, 2]] = M[:, [2, 0]] #Swap back to normal one
    
    #Flip rev diagonal (//)
    M2 = np.fliplr(np.transpose(np.fliplr(M)))
    key_M2 = get_hash_key(M2, matrix=True)
    if key_M2 in DICTIONARY:
        best_move = DICTIONARY[key_M2].best_move
        best_move = Mappings.flip_diag_rev[best_move]
        return best_move

    #Flip normal diagonal (\\)
    M1 = np.transpose(M)
    key_M1 = get_hash_key(M1, matrix=True)
    if key_M1 in DICTIONARY:
        best_move = DICTIONARY[key_M1].best_move
        best_move = Mappings.flip_diag_main[best_move]
        return best_move 
        
    return best_move


    
def trivial_checks(board):
    '''
    This function does some trivial checks in order to prevent the tree from creating unneceassary branches.
    This function will return the location of an empty position on the board which would result in an imediate win
    for player X.
    
    @param board: Game Board (1 x 9 array) - The current game state.
    @return: index (int) - Returns the index of the position that could lead to a immediate win or -1 if no such
			  position exists.
    '''
    board = np.reshape(board, (3, 3))
    vertical = np.sum(board, axis=0)
    
    if 2 in vertical:
        #potential to win here in one of the 3 coloumns
        col = np.where(vertical==2)[0][0]
        row = np.where(board[:, col] == 0)[0][0]
        return 3*row+col
    
    horizontal = np.sum(board, axis=1)
    if 2 in horizontal:
	#potential to win here in one of the 3 rows
        row = np.where(horizontal==2)[0][0]
        col = np.where(board[row, :] == 0)[0][0]
        return 3*row+col
    
    if np.trace(board) == 2:
	#potential to win here in the main diagonal
        row = np.where(np.diag(board) == 0)[0][0]
        return 3*row+row
    
    if np.trace(board[::-1]) == 2:
        #potential to win here in the reverse diagonal
        col = np.where(np.diag(board[::-1]) == 0)[0][0]
        return 3*(2-col)+col
        
    return -1

    

def build_tree_and_learn():
    '''
    This function is called when the tree needs to be learned. This function will
    start the learning process by creating an empty board and trying to learn ALL
    possible moves in the game. It will build the tree for all legal possible
    moves. All the game states (game boards) are stored in a dictionary which also
    stores the best possible move suggestion for that state. This dictionary helps
    the AI make intellegent moves.
    '''
    test_board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    test_node = Node(test_board, 0)
    DICTIONARY[test_node.key] = test_node
    learn_tree(test_node, 1)
    
    print "Dictionary Size = ", len(DICTIONARY)
    
    
    
    
def make_best_move(current_board):
    '''
    This function is called when the AI wants to query the dictionary for
    the best possible move given the current game state. The current game board
    might not be in the dictionary. In this case either one of the four rotations
    of this board is in the tree OR one of the four mirror flipped boards is in
    the dictionary.

    This function checks for them all and returns the best move location.

    @param current_board (3 x 3 array) - This contains the current game state.
            {1 = player X, -1 = player O, 0 = blank}
    '''
    current_board = np.ndarray.flatten(current_board)
    best_move = get_rotation_best_move(current_board)
    if best_move != None:
        y = int(best_move/3.0)
        x = best_move%3
        return [y, x]
    else:
        best_move = get_flip_best_move(current_board)
        if best_move != None:
            y = int(best_move/3.0)
            x = best_move%3
            return [y, x]
        print print_game_state(current_board)
        print "Problem! Board not seen before!"
        exit(0)
    

if __name__=="__main__":
    d = build_tree_and_learn()
#    print d
    









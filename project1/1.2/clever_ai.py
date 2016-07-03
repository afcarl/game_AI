import numpy as np

ID = 0
NODES = [] #Debuging
DICTIONARY = {}

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
    def __init__(self, board, score, depth, turn, key):
        global ID
        self.id = ID #Debuging
        ID += 1 #Debuging
        self.board = board
        self.score = score
        self.depth = depth
        self.terminal_depth = np.inf
        self.best_move = -1
        self.children = [] #Debuging
        self.turn = turn #Debuging
        
        self.key = key
        
        
def get_hash_key(board, matrix=False):
    '''
    This function creates a hashkey for a board so it can be stored in the dictionary.
    '''
    if matrix == True:
        board = np.ndarray.flatten(board)
    string_flat = np.char.mod('%d', board)
    key = "".join(string_flat)
    return key
    
# print game state using symbols
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
    
    if 3 in all_:
        return 1.0
    elif -3 in all_:
        return -1.0
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

    if node.score != 0.0: #Should only go if score is 1 or -1 (I THINK, need to test this)
        node.terminal_depth = node.depth#+1
        return node.score # Game won or lost
    elif np.count_nonzero(node.board) == 9:
        node.terminal_depth = node.depth#+1
        return 0.0 #Game tied cuz there is no 0 in board anymore and no winner


    if turn == 1:
        res = trivial_checks(node.board)
        if res != -1:
            node.score = 1.0
            node.best_move = res
            node.terminal_depth = node.terminal_depth + 1
            return node.score           
            
            
    index = np.where(node.board==0)[0]
    running_avg = 0.0    
    for i in index:
        copy_board = np.copy(node.board)
        copy_board[i] = turn
        tmp_score = get_score(copy_board)
        tmp_key = get_hash_key(copy_board)
        
        tmp_node = Node(copy_board, tmp_score, node.depth+1, -1*turn, tmp_key)
        node.children.append(tmp_node.id)
        NODES.append(tmp_node)
        
        score, terminal_depth = check_rotations(copy_board, tmp_key) 
        if score == None:
            score, terminal_depth = check_flips(copy_board)

        if score == None:
            #Havent seen this board or any rotation of it!
            DICTIONARY[tmp_node.key] = tmp_node
            score = learn_tree(tmp_node, -1*turn)
        else:
            tmp_node.terminal_depth = terminal_depth
        #Have seen this or rotation of this board
        
        if turn == 1: #Player X
            #If its player X's turn then player X would ALWAYS choose the best move,
            #so choose the child node with HIGHEST score.
            if score > node.score:
                node.score = score
                node.best_move = i
                node.terminal_depth = tmp_node.terminal_depth + 1
            elif score == node.score and tmp_node.terminal_depth+1 < node.terminal_depth:
                #If scores are the same then choose the path which lead to quickest route to terminal node
                node.score = score
                node.best_move = i
                node.terminal_depth = tmp_node.terminal_depth + 1
                
        else:   #Player O
            #If its player O's turn then player O would choose at random so label this nodes
            #score as the average of all choices as they are all equally likely to be chosen.
            running_avg += score
            tmp_node.terminal_depth = node.terminal_depth+1
            
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
    @return score, terminal_depth (int, int) - The score is the current score of the board, and
                terminal_depth is the depth in the tree where the terminal node of this path
                would lead to is at.
    '''
    score = None
    M = np.reshape(board, (3, 3))

    #Flip over middle row
    M[[0, 2]] = M[[2, 0]] #Swap first row and last row
    key_flip_td = get_hash_key(M, matrix=True)
    if key_flip_td in DICTIONARY:
        score = DICTIONARY[key_flip_td].score
        terminal_depth = DICTIONARY[key_flip_td].terminal_depth
        return score, terminal_depth
    M[[0, 2]] = M[[2, 0]] #Swap back to normal one

    #Flip over middle coloumn
    M[:, [0, 2]] = M[:, [2, 0]] #Swap first col and last col
    key_flip_lr = get_hash_key(M, matrix=True)
    if key_flip_lr in DICTIONARY:
        score = DICTIONARY[key_flip_lr].score
        terminal_depth = DICTIONARY[key_flip_lr].terminal_depth
        return score, terminal_depth
    M[:, [0, 2]] = M[:, [2, 0]] #Swap back to normal one
    
    #Flip rev diagonal (//)
    M2 = np.fliplr(np.transpose(np.fliplr(M)))
    key_M2 = get_hash_key(M2, matrix=True)
    if key_M2 in DICTIONARY:
        score = DICTIONARY[key_M2].score
        terminal_depth = DICTIONARY[key_M2].terminal_depth
        return score, terminal_depth
        
#    #Flip normal diagonal (\\)
#    M1 = np.transpose(M)
#    key_M1 = get_hash_key(M1, matrix=True)
#    if key_M1 in DICTIONARY:
#        score = DICTIONARY[key_M1].score
#        terminal_depth = DICTIONARY[key_M1].terminal_depth
#        return score, terminal_depth
        
    return score, None
    
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
        terminal_depth = DICTIONARY[key].terminal_depth
        return score, terminal_depth
        
    matrix = np.reshape(board, (3, 3))
    rot90 = np.rot90(matrix)
    rot90_key = get_hash_key(rot90, matrix=True)
    if rot90_key in DICTIONARY:
        score = DICTIONARY[rot90_key].score
        terminal_depth = DICTIONARY[rot90_key].terminal_depth
        return score, terminal_depth
        
    rot180_key = get_hash_key(board[::-1])
    if rot180_key in DICTIONARY:
        score = DICTIONARY[rot180_key].score
        terminal_depth = DICTIONARY[rot180_key].terminal_depth
        return score, terminal_depth
        
    rot270 = np.rot90(matrix, k=3)
    rot270_key = get_hash_key(rot270, matrix=True)
    if rot270_key in DICTIONARY:
        score = DICTIONARY[rot270_key].score
        terminal_depth = DICTIONARY[rot270_key].terminal_depth
        return score, terminal_depth
        
    return score, None
    
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
        best_move = trans_rot90[best_move]
        return best_move
    
    rot180_key = get_hash_key(board[::-1])
    if rot180_key in DICTIONARY:
        best_move = DICTIONARY[rot180_key].best_move
        best_move = trans_rot180[best_move]
        return best_move
    
    rot270 = np.rot90(matrix, k=3)
    rot270_key = get_hash_key(rot270, matrix=True)
    if rot270_key in DICTIONARY:
        best_move = DICTIONARY[rot270_key].best_move
        best_move = trans_rot270[best_move]
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
        best_move = fliptd[best_move]
        return best_move
    M[[0, 2]] = M[[2, 0]] #Swap back to normal one

    #Flip over middle coloumn
    M[:, [0, 2]] = M[:, [2, 0]] #Swap first col and last col
    key_flip_lr = get_hash_key(M, matrix=True)
    if key_flip_lr in DICTIONARY:
        best_move = DICTIONARY[key_flip_lr].best_move
        best_move = fliplr[best_move]
        return best_move
    M[:, [0, 2]] = M[:, [2, 0]] #Swap back to normal one
    
    #Flip rev diagonal (//)
    M2 = np.fliplr(np.transpose(np.fliplr(M)))
    key_M2 = get_hash_key(M2, matrix=True)
    if key_M2 in DICTIONARY:
        best_move = DICTIONARY[key_M2].best_move
        best_move = flip_diag_rev[best_move]
        return best_move

    #Flip normal diagonal (\\)
    M1 = np.transpose(M)
    key_M1 = get_hash_key(M1, matrix=True)
    if key_M1 in DICTIONARY:
        best_move = DICTIONARY[key_M1].best_move
        best_move = flip_diag_main[best_move]
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

    

def print_nodes():
    '''
    Prints all the nodes that was ever created during the learning process.
    '''
    global NODES
    print "Boards:"
    for n in NODES:
        print "Node # ", n.id
        print_game_state(n.board)
        print "#########################"
    keys = []
    print "Connections\n==========="
    for n in NODES:
        print "Node ", n.id, "... Best_Move = ", n.best_move, "...score = ", n.score, "...turn = ", n.turn,  "...children = ", n.children
        keys.append(n.key)
        
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
    test_score = get_score(test_board)
    test_key = get_hash_key(test_board)
    test_node = Node(test_board, test_score, 0, 1, test_key)
    DICTIONARY[test_key] = test_node
    learn_tree(test_node, 1)
    
    print "Dictionary Size = ", len(DICTIONARY)
    print "Number of Nodes = ", len(NODES)
    
    
    
    
def make_best_move(current_board):
    '''
    This function is called when the AI wants to query the dictionary for
    the best possible move given the current game state. The current game board
    might not be in the dictionary. In this case either one of the four rotations
    of this board is in the tree OR one of the four mirror flipped boards is in
    the dictionary.

    This function checks for them all and returns the best move location.

    @param current_board (1 x 9 array) - This contains the current game state.
            {1 = player X, -1 = player O, 0 = blank}
    '''
    best_move = get_rotation_best_move(current_board)
    if best_move != None:
        return best_move
    else:
        best_move = get_flip_best_move(current_board)
        if best_move != None:
            return best_move
        print print_game_state(current_board)
        print "Problem! Board not seen before!"
        exit(0)
    

if __name__=="__main__":
    d = build_tree_and_learn()
#    print d
    
    print_nodes()









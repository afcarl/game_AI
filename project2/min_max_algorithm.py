'''
Exercise 2.2: minmax computations
'''

import numpy as np 

class Node(object):
    '''
    Each node in the minmax tree is a Node object. It contains all information
    needed.
    '''
    
    def __init__(self, name, children, score): 
        '''
        @param name: Name of the node
        @children: A list of the children of the current node
        @attribute score: Score of the node
        '''  
        self.name = name
        self.children = children
        self.score = score

def minmax(node, player):
    '''
    This function computes the minmax value for the input node
    '''
    
    # If the current node is a terminal node we are done    
    if terminal_node(node):
        return node.score
    
    # Else, we have to call the function recursively on every child of the
    # node in order to compute its minmax value
    for child in node.children:
        new_score = minmax(child, player*-1)
        
        # Player 1 chooses the maximum
        if player == 1:
            if new_score >= node.score:
                node.score = new_score
        
        # Player -1 chooses the minimum
        if player == -1:
            if new_score <= node.score:
                node.score = new_score
                
    return node.score
    

def terminal_node(node): 
    '''
    Checks whether node is a terminal node, i.e. leaf
    '''
    if not node.children:
        return True
    else:
        return False
     
     
if __name__=="__main__":

    # build tree
    
    # leaf nodes
    n_6 = Node('n6', [], 15)
    n_7 = Node('n7', [], 20)
    n_8 = Node('n8', [], 1)
    n_9 = Node('n9', [], 3)
    n_10 = Node('n10', [], 3)
    n_11 = Node('n11', [], 4)
    n_12 = Node('n12', [], 15)
    n_13 = Node('n13', [], 10)
    n_14 = Node('n14', [], 16)
    n_15 = Node('n15', [], 4)
    n_16 = Node('n16', [], 12)
    n_17 = Node('n17', [], 15)
    n_18 = Node('n18', [], 12)
    n_19 = Node('n19', [], 8)
    
    # middle nodes
    n_5 = Node('n5', [n_17, n_18, n_19], np.inf)
    n_4 = Node('n4', [n_14, n_15, n_16], np.inf)
    n_3 = Node('n3', [n_12, n_13], np.inf)
    n_2 = Node('n3', [n_10, n_11], np.inf)
    n_1 = Node('n1', [n_6, n_7, n_8, n_9], np.inf)
    
    # root
    n_0 = Node('n0', [n_1, n_2, n_3, n_4, n_5], -(np.inf))
     
    # Compute the minmax_value for node 0
    print "minmax value of node n0: ", minmax(n_0, 1)

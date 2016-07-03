# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:30:45 2016

@author: Eva
"""

import networkx as nx
import numpy as np

number_nodes = 1  # already take first node into account
wins_for_x = 0
wins_for_o = 0
draws = 0

def board_to_string(board):
    # example: convert starting board to string '000000000'
    board_string = np.ndarray.flatten(board)
    board_str = ""
    for j in range(9):
        board_str = board_str + str(board_string[j])
    return board_str

def no_winner_yet(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return False

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return False

    if (np.sum(np.diag(S)) * p) == 3:
        return False

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return False

    return True


def eval_children(G, start, start_str, p):
    global number_nodes
    global wins_for_x
    global wins_for_o
    global draws
    
    xs, ys = np.where(start==0)
    anzahl = len(xs)
    #print "start"
    #print start
    if anzahl == 0:
        draws += 1
    for i in range(anzahl):
        new = np.copy(start)
        new[xs[i],ys[i]] = p
        #print "new"
        #print new
        new_str = board_to_string(new)
        
        number_nodes += 1
        G.add_edge(start_str,new_str)
        
        if no_winner_yet(new, p):
            # move was no winning move, we add next level
            eval_children(G, new, new_str, p*-1)
        else:
            # someone won!
            if p == 1:
                wins_for_x += 1
            else:
                wins_for_o += 1
                


if __name__ == '__main__':
    global number_nodes
    global wins_for_x
    global wins_for_o
    global draws
    # init directed Graph
    G = nx.DiGraph()
    
    # starting board
    start = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    start_str = board_to_string(start)
    
    #player 1 starts
    p = 1
    
    eval_children(G, start, start_str, p)
    
    #print list(G.nodes())
    #print list(G.edges())

    print number_nodes
    print wins_for_x
    print wins_for_o
    print draws
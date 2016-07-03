'''
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 2.1: The tic tac toe game tree
'''

import numpy as np
import sys
import networkx as nx
import matplotlib.pyplot as plt
import time

import dijkstra as dj
import a_star

class Directions(object):
    directions_4 = [(-1, 0), (0, 1), (1, 0), (0, -1)] #  (up, right, down, left)
    
    directions_8 = [(-1, 0), (0, 1), (1, 0), (0, -1), # (up, right, down, left)
                  (-1, -1), (1, 1), (-1, 1), (1, -1)] # (top left, bottom right, bottom left, top right)


def read_file(file_name):
    '''
    Reads the grid map from the text file named: file_name
    file_name: (String) - String containing the file_name
    '''
    grid = np.loadtxt(file_name, dtype=np.float)
    return grid

def create_graph(grid):
    '''
    This function takes in the grid matrix and constructs a NetworkX graph. It
    connects the vertices depending if it is 1 or 0 in each element of the matrix.
    
    grid: (ndarray) - Grid of the map with binary values.
    '''
    [m, n] = np.shape(grid)
    G = nx.Graph()    
    ys, xs = np.where(grid==0)
    zeros = zip(ys, xs)
    
    for row in xrange(m):
        for col in xrange(n):
            
            #Add node and if it is 1 then continue
            if grid[row][col] == 1:
                G.add_node(n*row + col, pos=(col, m-row), node_color='r')
                continue
            else:
                G.add_node(n*row + col, pos=(col, m-row), node_color='g')
                
            #Add edges in all 4 directions if neighbours are 0
            for [dy, dx] in Directions.directions_4: #check all directions
                new_y, new_x = row+dy, col+dx
                if (new_y, new_x) in zeros:
                    src, dst = n*row + col, n*new_y + new_x
                    G.add_edge(src, dst, weight=1)
    return G
    
def get_graph(file_name=None):
    ''' 
    This function reads the grid map and creates the graph by calling to other functions.
    
    file_name: (String) -> Either None or file name. If its None it reads the 
                value from command line.
    '''
    if file_name==None:
        file_name = sys.argv[1]
    grid = read_file(file_name)
    G = create_graph(grid)
    return grid, G

def draw_graph(G):
    '''
    This uses the NetworkX draw function to draw the graph showing all its nodes
    and edges.
    '''
    positions = nx.get_node_attributes(G, "pos")
    colors = nx.get_node_attributes(G, "node_color")
    nx.draw(G, positions, node_color=colors.values())

def convert_lecturer_to_our_numbering(grid, row, col):
    '''
    According to the assignment sheet (0, 0) is at the bottom left. This function 
    will convert the origin to top left. So it will return the coordinates in
    our coordinate system.
    '''
    [m, _] = np.shape(grid)
    return [m-row-1, col] 

def get_dijkstra_shortest_path(G, grid, source, destination, use_built_in=False):
    '''
    This function uses Dijkstras algorithm to get the shortest path between two
    nodes. It can either use NetworkX's built-in implementation or it will use
    the self implemented algorithm to get the path. The use_built_in boolean variable
    defines which must be used.

    G (NetworkX graph) -> NetworkX graph instance
    grid (ndarray) -> Matrix with the grid map containing binary values
    source (List) -> A list with two values which are coordinates of the source node.
    destination (List) -> A list with two values which are coordinates of the destination node.    
    
    Both source and destination lists have the following elements: (y_position, x_position)    
    and coordinates according to the origin being in the top left corner.
    
    source and destination must be in our coord system. so top left is (0, 0)
    '''
    [m, n] = np.shape(grid)
    [y, x] = source[0], source[1]
    row, col = y, x
    node_index_s = (n*row) + col #Convert from coordinates to Node index
    [y, x] = destination[0], destination[1]
    row, col = y, x
    node_index_d = (n*row) + col #Convert from coordinates to Node index

    tic = time.time()
    if use_built_in == False:
        path = dj.get_shortest_path(G, node_index_s, node_index_d)
    else:
        path = nx.dijkstra_path(G, node_index_s, node_index_d)
    tac = time.time()
    print "Time to find shortest path Dijkstra = ", (tac-tic)
 
    #Color the path in the grid matrix to display it
    for i in xrange(len(path)-1):
        n_row, n_col = int(path[i+1]/n), int(path[i+1]%n)
        grid[n_row][n_col] = 0.5
   

#    print "Path = ", path
    print "Path Length = ", len(path)
   
    return path



def get_a_star_shortest_path(G, grid, source, destination, use_built_in=False):
    '''
    This function uses A* algorithm to get the shortest path between two
    nodes. It can either use NetworkX's built-in implementation or it will use
    the self implemented algorithm to get the path. The use_built_in boolean variable
    defines which must be used. The grid matrix is edited to show the path by editing
    the color values.

    G (NetworkX graph) -> NetworkX graph instance
    grid (ndarray) -> Matrix with the grid map containing color values for display
    source (List) -> A list with two values which are coordinates of the source node.
    destination (List) -> A list with two values which are coordinates of the destination node.    
    
    Both source and destination lists have the following elements: (y_position, x_position)    
    and coordinates according to the origin being in the top left corner.
    
    source and destination must be in our coord system. so top left is (0, 0)
    '''
    [m, n] = np.shape(grid)
    [y, x] = source[0], source[1]
    row, col = y, x
    node_index_s = (n*row) + col #Convert from coordinates to Node index
    [y, x] = destination[0], destination[1]
    row, col = y, x
    node_index_d = (n*row) + col #Convert from coordinates to Node index

    a_star.size_x = n
    
    tic = time.time()
    if use_built_in == False:
        path = a_star.get_shortest_path(G, node_index_s, node_index_d)
    else:
        path =  nx.astar_path(G, node_index_s, node_index_d, heuristic=a_star.heuristic)
        
    
    tac = time.time()
    print "Time to find shortest path A* = ", (tac-tic)
    
    #Color the path in the grid matrix to display it
    for i in xrange(len(path)-1):
        n_row, n_col = int(path[i+1]/n), int(path[i+1]%n)
        grid[n_row][n_col] = 0.5

#    print "Path = ", path
    print "Path Length = ", len(path)

    return path

   
if __name__=="__main__":
    grid, G = get_graph()
    draw_graph(G)

    s_r, s_c = 0, 0
    d_r, d_c = 5, 10    
    [m, n] = np.shape(grid)
    
#    row, col = m-s_r-1, s_c
#    node_index_s = (n*row) + col
#    row, col = m-d_r-1, d_c
#    node_index_d = (n*row) + col
#    path = dj.get_shortest_path(G, node_index_s, node_index_d)
    
    
    path = get_dijkstra_shortest_path(G, grid, (s_r, s_c), (d_r, d_c))
#    nx_path =  nx.dijkstra_path(G, node_index_s, node_index_d)
    
    
#    a_star.size_x = n
#    path = a_star.get_shortest_path(G, node_index_s, node_index_d)
#    nx_path =  nx.astar_path(G, node_index_s, node_index_d)

#    print "Networkx answer = "
#    print nx_path
    
    draw_grid = np.copy(grid)*-1
    row, col = int(path[0]/n), int(path[0]%n)
    draw_grid[row][col] = 1 
    
    for i in xrange(len(path)-1):
        c_row, c_col = int(path[i]/n), int(path[i]%n)
        n_row, n_col = int(path[i+1]/n), int(path[i+1]%n)
        draw_grid[n_row][n_col] = 0.3
        
#    for i in xrange(len(nx_path)-1):
#        c_row, c_col = int(nx_path[i]/n), int(nx_path[i]%n)
#        n_row, n_col = int(nx_path[i+1]/n), int(nx_path[i+1]%n)
#        draw_grid[n_row][n_col] = -0.3        
        
        
    n_row, n_col = int(path[-1]/n), int(path[-1]%n)
    draw_grid[n_row][n_col] = 0.6
    
    plt.matshow(draw_grid)
    plt.colorbar()
    
    plt.show()




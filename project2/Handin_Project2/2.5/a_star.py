"""
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 5: Path Planning

"""
import numpy as np
import heapq as pq
size_x = None

def heuristic(node_a, node_b):
    '''
    Normal Euclidean distance heuristic function
    '''
    row_a, col_a = int(node_a/size_x), int(node_a%size_x)
    row_b, col_b = int(node_b/size_x), int(node_b%size_x)
    return np.sqrt( (abs(row_a-row_b))**2 + (abs(col_a-col_b))**2)
    
def a_star(graph, source, destination):
    '''
    This function uses the A* algorithm to get the shortest path. It returns the
    path as a dictionary which can be used to backtrack the path from the destination to the
    source node.
    
    graph (NetworkX graph) -> NetworkX graph instance
    source (integer) -> Source node index
    destination (integer) -> Destination node index

    returns path: Dictionary which contains the previous node of each node allowing you to go from destination
        to the source node.
    '''
    G = graph
    open_list = []  # Contains all the nodes that are to be explored still
    previous = {}  # Previous best node to get closer to source
    current_cost = {}  # Contains the cost

    pq.heappush(open_list, (0, source))
    previous[source] = None
    current_cost[source] = 0

    while len(open_list) != 0:
        _, current = pq.heappop(open_list)
        
        if current == destination:
            break
        
        neighbours = G.neighbors(current)
        for neighbour in neighbours: 
            trans_wegiht = G.get_edge_data(current, neighbour, default={"weight":0})["weight"]
            new_cost = current_cost[current] + trans_wegiht
            
            if neighbour not in current_cost or new_cost < current_cost[neighbour]:
                current_cost[neighbour] = new_cost
                F = new_cost + heuristic(neighbour, destination)
                pq.heappush(open_list, (F, neighbour))
                previous[neighbour] = current
    
    return previous
    

def get_shortest_path(graph, source, destination):
    '''
    This function is called when the shortest path is required using A*
    algorithm. It calls other functions to calculate the path and returns the path in
    a list. The list contains the whole path starting from source node to destination node
    '''
    previous = a_star(graph, source, destination)
    path = [destination]
    
    if destination not in previous:
        print "No path from source %d to destination %d."%(source, destination)
        return path
    while previous[path[-1]] != None:
        path.append(previous[path[-1]])
    path.reverse()
    return path




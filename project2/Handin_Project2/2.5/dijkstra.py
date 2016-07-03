"""
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 5: Path Planning

This class implements Dijkstra Algorithm
"""

import numpy as np
import networkx as nx
import heapq as pq
    
def dijkstra(graph, source):
    '''
    This function uses Dijkstras Algorithm to find the shortest path between source and all
    other nodes. It returns a array where each index is the node index and each element
    at the node is a number (node id) indicating the previous node. So you can use
    this to backtrack from the destination node to the source node.
    
    graph (NetworkX graph) -> NetworkX graph instance
    source (integer) -> Source node index
    
    return: (array of integers) Indicates the previous node to move to from a certain index (node)
    '''
    G = graph
    nodes = G.nodes()
    
    num_nodes = G.number_of_nodes()
    distances = np.array([np.inf]*num_nodes)
    previous = np.array([None]*num_nodes)

    distances[source] = 0
    Q = set(nodes)
    visited = []

    while len(Q) > 0:
        min_node_value = np.min(distances[list(Q)])
        posibilities = np.where(distances==min_node_value)[0]  # Get all possibilities to move to
        
        # Now choose one
        # Always go in order of down, right, left, up
        posibilities = np.sort(posibilities)[::-1]  # So that path is the same as in the project description
        min_node_key = None
        for p in posibilities:
            if p not in visited:
                min_node_key = p  # Find one that has not been visited before
                break
        
        if np.isinf(min_node_key):  break
        else: min_node_key = int(min_node_key)
        
        Q.remove(min_node_key)
        visited.append(min_node_key)
        
        if np.isinf(distances[min_node_key]):
            break
        
        neighbours = G.neighbors(min_node_key)
        for neighbour in neighbours:
            trans_wegiht = G.get_edge_data(min_node_key, neighbour, default={"weight":0})["weight"]
            score = distances[min_node_key] + trans_wegiht
            
            if score < distances[neighbour]:  # Update Neighbour if going through current min_node is better
                distances[neighbour] = score
                previous[neighbour] = min_node_key
    
    return previous


def modified_a_star(graph, source):
    '''
    This function uses a modified a* implementation where the Heuristic is 0 which makes
    it equivalent to Dijkstra. This was just a test using a different implementation
    from the one above. This one makes use of dictionaries.
    
    This function makes use of heapq library to pop and push nodes into the heap. It uses its
    pop function to get the minimum node based on F score.
    
    Returns the a dictionary instead of array but same idea.
    '''
    G = graph
    open_list = []
    previous = {}
    current_cost = {}

    pq.heappush(open_list, (0, source))
    previous[source] = None
    current_cost[source] = 0

    while len(open_list) != 0:
        _, current = pq.heappop(open_list)
        
        neighbours = G.neighbors(current)  # Get neighbours
        for neighbour in neighbours:  # Loop through each and get new cost for them.
            trans_wegiht = G.get_edge_data(current, neighbour, default={"weight":0})["weight"]
            new_cost = current_cost[current] + trans_wegiht
            
            # If current cost is better then update path to this new neighbour
            if neighbour not in current_cost or new_cost < current_cost[neighbour]:
                current_cost[neighbour] = new_cost
                F = new_cost
                pq.heappush(open_list, (F, neighbour))
                previous[neighbour] = current
    
    return previous



def get_shortest_path(graph, source, destination):
    '''
    This function is called when the shortest path is required using Dijkstras 
    algorithm. It calls other functions to calculate the path and returns the path in
    a list. The list contains the whole path starting from source node to destination node
    '''
    previous = dijkstra(graph, source)
    
    path = [destination]
    while previous[path[-1]] != None:
        path.append(previous[path[-1]])
    path.reverse()
    if len(path)==1:
        print "No path from source %d to destination %d."%(source, destination)
        return path
    return path

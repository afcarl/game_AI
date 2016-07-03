# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:26:04 2016

@author: anna-lenapopkes
"""

import numpy as np 
from numpy import genfromtxt
from scipy.spatial import distance
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


# Determine the number of vertices
#num_vertices = int(raw_input('Insert number of vertices: '))

# Determine the maximal number of learning steps
#t_max = int(raw_input('Insert maximal time: '))

num_vertices = 20
t_max = 1000

# Load data
data1 = genfromtxt('q3dm1-path1.csv', delimiter=',')
data2 = genfromtxt('q3dm1-path2.csv', delimiter=',')

data = data2

def SOM():
    # Create random starting weights that already have a ring structure.
    # The number of neurons is specified by num_vertices

    maxy = np.max(data[:, 1])
    miny = np.min(data[:, 1])
   
    maxx = np.max(data[:, 0])
    minx = np.min(data[:, 0])
   
    mid = data.mean(axis=0)
   
    deg = np.linspace(0, 2*np.pi, num_vertices)
     
    r0 = (maxx-minx)/2.0
    r1 = (maxy-miny)/2.0
    c1 = mid[0] + r0 * np.cos(deg)
    c2 = mid[1] + r1 * np.sin(deg)
    c3 = mid[2] + np.zeros(len(deg))
   
    circ = np.vstack([c1,c2,c3]).T
 
    # Initialize weight matrix for plotting
    weight_matrix = [circ.copy()]
   
    # Compute the initial distance matrix
    a,b = np.ogrid[0:num_vertices, 0:num_vertices]
    distances = np.sqrt(np.sum((circ[a]- circ[b])**2,2))

    
    for t in range(0, t_max):

        # Randomly sample a point
        rand = np.random.randint(0, len(data), 1)
        point = data[rand][0]
        
        # Determine the winner neuron
        min_dist = np.inf
        index = 0
        for p in range(0,num_vertices):
            dist = distance.euclidean(circ[p],point)
            if dist < min_dist:
                min_dist = dist
                index = p
               
        # Compute learning rate and topological adaptation rate
        eta = (1 - np.true_divide(t,t_max))
        sigma = np.exp(-np.true_divide(t,t_max))

        # Update the weight vectors of ALL neurons
        for p in range(0,num_vertices):
            increase = eta * np.exp(-np.true_divide(distances[index][p], 2*sigma))*(point - circ[p])
            circ[p] = circ[p] + increase
          
        weight_matrix.append(circ.copy())
        
    return circ, weight_matrix
        
circ, weight_matrix = SOM()

#np.savetxt("data1_8_vertices_2", circ)

# PLOTTING THE DATA
# The animation is achieved using matplotlib.animate FuncAnimation

def plot_SOM1(circle, weight_matrix):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x2 = circ[:, 0]
    y2 = circ[:, 1]
    z2 = circ[:, 2]
    
    x1 = data1[:,0]
    y1 = data1[:,1]
    z1 = data1[:,2]
    
    ax.scatter(y1, x1, z1, c='b', marker='o', depthshade=True)
    vecs = ax.plot(y2, x2, z2,c='r', marker = 'o')[0]
     
    ax.set_ylim([1200,0])
    ax.set_xlim([1800, 2400])
    ax.set_zlim([15,50])
     
    ax.set_xlabel('Y Label')
    ax.set_ylabel('X Label')
    ax.set_zlabel('Z Label')
     
    def updatePlot(weights):
        vecs.set_data(weights[:,1], weights[:,0])
        vecs.set_3d_properties(weights[:,2])
       
    anim = FuncAnimation(fig, updatePlot, frames=weight_matrix, interval=5)
     
     
    plt.show()
        
def plot_SOM2(circ, weight_matrix):
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x2 = circ[:, 0]
    y2 = circ[:, 1]
    z2 = circ[:, 2]
    
    x1 = data2[:,0]
    y1 = data2[:,1]
    z1 = data2[:,2]
    
    ax.scatter(y1, x1, z1, c='b', marker='o', depthshade=True)
    vecs = ax.plot(y2, x2, z2,c='r', marker = 'o')[0]
     
    ax.set_ylim([1200,0])
    ax.set_xlim([1800, 2400])
    ax.set_zlim([10,70])
     
    ax.set_xlabel('Y Label')
    ax.set_ylabel('X Label')
    ax.set_zlabel('Z Label')
     
    def updatePlot(weights):
        vecs.set_data(weights[:,1], weights[:,0])
        vecs.set_3d_properties(weights[:,2])
       
    anim = FuncAnimation(fig, updatePlot, frames=weight_matrix, interval=20)
     
    plt.show()
    
    
    
if __name__=="__main__":
    
    circ, weight_matrix = SOM()
    #plot_SOM1(circ, weight_matrix)
    plot_SOM2(circ, weight_matrix)

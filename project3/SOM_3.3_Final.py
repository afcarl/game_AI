'''
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 3.3: self organizing maps to represent player movements
'''

import numpy as np
from numpy import genfromtxt
from scipy.spatial import distance
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import sys

# Load data
data1 = genfromtxt('q3dm1-path1.csv', delimiter=',')
data2 = genfromtxt('q3dm1-path2.csv', delimiter=',')

# Let user choose dataset and number of vertices
try:
    if len(sys.argv) > 3:
        raise Exception('You have chosen too many arguments!\n'
                        'Please choose between data1/data2 and enter'
                         'a valid number of vertices.\n'
                         'Example: python2 data1 100')
    elif len(sys.argv) > 2:
        if sys.argv[1] != 'data1' and sys.argv[1] != 'data2':
            raise Exception('You have chosen a wrong data name.\n'
                            'Please choose between data1 and data2\n')
        elif not 3 <= int(sys.argv[2]) <= 100:
            raise Exception('Please choose a number of vertices between 3 and 100')
        else:
            chosen_data = sys.argv[1]
            chosen_vertices = int(sys.argv[2])
    else:
        raise Exception('You forgot to choose a dataset or the number of vertices.\n'
                        'Please choose between data1 and data2 a valid number of vertices.\n'
                        'Example: python2 data1 42')
except Exception as err:
    print('An exception happened: ' + str(err))
    sys.exit()

def SOM(data, num_vertices, t_max):
    # Create random starting weights that already have a circular structure
    # using the properties of sin, cos and pi. The number of neurons/vertices
    # is specified by num_vertices.

    maxy = np.max(data[:, 1])
    miny = np.min(data[:, 1])

    maxx = np.max(data[:, 0])
    minx = np.min(data[:, 0])

    mid = data.mean(axis=0)

    deg = np.linspace(0, 2*np.pi, num_vertices, endpoint = False)

    r0 = (maxx-minx)/2.0
    r1 = (maxy-miny)/2.0
    c1 = mid[0] + r0 * np.cos(deg)
    c2 = mid[1] + r1 * np.sin(deg)
    c3 = mid[2] + np.zeros(len(deg))

    # Initial weigths/coordinates of the vertices (circular graph)
    circ = np.vstack([c1,c2,c3]).T

    # Initialize weight matrix. In the end it will consist of all weights from
    # t = 0 up to t = t_max. The weights are needed for the animated plot.
    weight_matrix = [circ.copy()]

    # Compute the initial distance matrix (topological distances)
    a,b = np.ogrid[0:num_vertices, 0:num_vertices]

    div,mod = divmod(num_vertices,2)
    first = np.arange(0,div+1)
    second = first[::-1]
    final = np.concatenate((first, second[1-mod:div]))

    distances = np.empty((num_vertices, num_vertices))
    distances[0] = final

    for i in range(1,num_vertices):
        distances[i] = np.roll(final, i)

    # SOM main loop
    for t in range(0, t_max):

        # Randomly sample a point
        rand = np.random.randint(0, len(data), 1)
        point = data[rand][0]

        # Determine the winner neuron and save its position
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
        sigma = sigma/3

        # Update the weight vectors of ALL neurons
        for p in range(0,num_vertices):
            increase = eta * np.exp(-np.true_divide(distances[index][p], 2*sigma))*(point - circ[p])
            circ[p] = circ[p] + increase

        # Save the new weights
        weight_matrix.append(circ.copy())

    return circ, weight_matrix


# PLOTTING THE DATA
# The animation is achieved using matplotlib.animate FuncAnimation

def plot_SOM(circ, weight_matrix):
    '''
    This functions plots the data from dataset2 and the SOM animation in 3D
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x2 = circ[:, 0]
    y2 = circ[:, 1]
    z2 = circ[:, 2]

    x1 = data[:,0]
    y1 = data[:,1]
    z1 = data[:,2]

    ax.scatter(y1, x1, z1, c='b', marker='o', depthshade=True)
    # Plot the initial points. In the animation these points are moved
    # to different positions, resulting in an animation.
    vecs = ax.plot(y2, x2, z2,c='r', marker = 'o')[0]

    ax.set_ylim([1200,0])
    ax.set_xlim([1800, 2400])
    ax.set_zlim([15,50]) if chosen_data == data1 else ax.set_zlim([10,70])

    ax.set_xlabel('Y Label')
    ax.set_ylabel('X Label')
    ax.set_zlabel('Z Label')

    def updatePlot(weights):
        weights = np.vstack([weights, weights[0]])
        vecs.set_data(weights[:,1], weights[:,0])
        # NOTE: there is no .set_data() for 3 dim data
        vecs.set_3d_properties(weights[:,2])

    # Make an animation by repeatedly calling the function updatePlot that
    # fills the variable 'vecs' with data from weight_matrix. weight_matrix
    # is a list of all weights that were produced during the t_max iterations

    # plt.savefig('Initialization_data1.png')
    anim = FuncAnimation(fig, updatePlot, frames=weight_matrix, interval=1)

    plt.show()


if __name__=="__main__":

    num_vertices = chosen_vertices
    t_max = 1000
    data = eval(chosen_data)
    circ, weight_matrix = SOM(data, num_vertices, t_max)
    plot_SOM(circ, weight_matrix)

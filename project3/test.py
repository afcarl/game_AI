# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 16:21:19 2016

@author: anna-lenapopkes
"""

import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

# Generate random starting data that is already a good approzimation of our data

data1 = genfromtxt('q3dm1-path1.csv', delimiter=',')

midx = np.mean(data1[:, 0])
midy = np.mean(data1[:, 1])
midz = np.mean(data1[:, 2])

maxy = np.max(data1[:, 1])
miny = np.min(data1[:, 1])

mid = np.array([[midx, midy, midz]])
radius = np.true_divide((maxy - miny), 2)
#radius= 300
deg = np.linspace(0, 2*np.pi, 6)

circ = mid + radius *np.array([np.sin(deg), np.cos(deg), np.zeros(len(deg))]).T

print circ.T

x2 = circ[:, 0]
y2 = circ[:, 1]
z2 = circ[:, 2]

# PLOTTING

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x1 = data1[:,0]
y1 = data1[:,1]
z1 = data1[:,2]

ax.scatter(y1, x1, z1, c='b', marker='o', depthshade=True)
ax.plot(y2, x2, z2,c='r', marker = 'o')
ax.set_ylim([1200,0])
ax.set_xlim([1800, 2400])
ax.set_zlim([15,50])

ax.set_xlabel('Y Label')
ax.set_ylabel('X Label')
ax.set_zlabel('Z Label')


# BEFORE

#    midx = np.mean(data[:, 0])
#    midy = np.mean(data[:, 1])
#    midz = np.mean(data[:, 2])
#    
#    maxy = np.max(data[:, 1])
#    miny = np.min(data[:, 1])
#    
#    mid = np.array([[midx, midy, midz]])
#    radius = np.true_divide((maxy - miny), 2)
#    deg = np.linspace(0, 2*np.pi, num_vertices)
#    
#    circ = mid + radius *np.array([np.sin(deg), np.cos(deg), [0]*len(deg)]).T
 
"""
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 5: Path Planning

This is a simple Graphical User Interface to make it easier to visualize the path and
select start and end nodes. Also it allows the user to select different algorithms
to find the shortest path.

"""

import sys
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar


import random
import path_planning as pp
import numpy as np
import sys

source = None
destination = None
unchanged_grid = None
grid = None
G = None

class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button_a_star = QtGui.QPushButton('A*')
        self.button_a_star.clicked.connect(self.button_a_star_clicked)
        self.figure.canvas.mpl_connect('button_press_event', self.canvas_clicked)
        
        self.button_dijkstra = QtGui.QPushButton('Dijkstra')
        self.button_dijkstra.clicked.connect(self.button_dijkstra_clicked)
        
        self.button_network_x_dijkstra = QtGui.QPushButton('Networkx Dijkstra')
        self.button_network_x_dijkstra.clicked.connect(self.button_network_x_dijkstra_clicked)
        
        self.button_network_x_a_star = QtGui.QPushButton('Network A*')
        self.button_network_x_a_star.clicked.connect(self.button_network_x_a_star_clicked)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button_dijkstra)
        layout.addWidget(self.button_a_star)
        layout.addWidget(self.button_network_x_dijkstra)
        layout.addWidget(self.button_network_x_a_star)
        self.setLayout(layout)
        
        
        self.redraw_grid(first_time=True)
    
    def redraw_grid(self, first_time=False):
        self.ax = self.figure.add_subplot(111)
        cax = self.ax.matshow(grid)
        self.ax.set_xticks(np.arange(np.shape(grid)[1]))
        self.ax.set_yticks(np.arange(np.shape(grid)[0]))
        
        self.ax.set_xticks([x - 0.5 for x in self.ax.get_xticks()][1:], minor='true')
        self.ax.set_yticks([y - 0.5 for y in self.ax.get_yticks()][1:], minor='true')
        self.ax.grid(color='m', which='minor')
        
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        
        if first_time==True:
            self.figure.colorbar(cax)
        self.canvas.draw()        
        
    def canvas_clicked(self, event):
        '''
        This function is called whenever the user clicks on the canvas. It can either
        left or right click and depending on which the source or destination node is selected
        '''
        global grid, source, destination, unchanged_grid
        print "Canvas clicked"
        
        if event.button == 1:
            print "Left click! Selecting Source Node"
            x, y = event.xdata, event.ydata
            row, col = np.round(y), np.round(x)
            
            if source != None:
                grid[source[0]][source[1]] = unchanged_grid[source[0]][source[1]]
            grid[row][col] = 0.4
            source = [int(row), int(col)]
        if event.button == 3:
            print "Right Click Selecting Target Node"
            x, y = event.xdata, event.ydata
            row, col = np.round(y), np.round(x)
            if destination != None:
                grid[destination[0]][destination[1]] = unchanged_grid[destination[0]][destination[1]]
            grid[row][col] = 0.6
            destination = [int(row), int(col)]
            
            
        self.redraw_grid()


    def button_dijkstra_clicked(self):
        '''
        Calls the Dijksta Algorithm
        '''
        global grid, G, unchanged_grid
        if source == None or destination == None:
            return
        print "My dijkstra Algorithm running!"

        grid = np.copy(unchanged_grid)        
        _ = pp.get_dijkstra_shortest_path(G, grid, source, destination)
        
        grid[source[0]][source[1]] = 0.4
        grid[destination[0]][destination[1]] = 0.7
        
        self.ax.set_title("Self Implemented dijkstra Algorithm")
        self.redraw_grid()
        
    def button_a_star_clicked(self):
        '''
        Calls the A* Algorithm
        '''
        global grid, G, unchanged_grid
        print "My A* Algorithm running!"
        if source == None or destination == None:
            return
        grid = np.copy(unchanged_grid)        
        _ = pp.get_a_star_shortest_path(G, grid, source, destination)

        grid[source[0]][source[1]] = 0.4
        grid[destination[0]][destination[1]] = 0.7

        self.ax.set_title("Self Implemented A* Algorithm")
        self.redraw_grid()

    def button_network_x_dijkstra_clicked(self, event):
        '''
        Calls the NetworkX's Dijksta Algorithm
        '''
        global grid, G, unchanged_grid
        if source == None or destination == None:
            return
        print "Network X dijkstra running!"

        grid = np.copy(unchanged_grid)        
        _ = pp.get_dijkstra_shortest_path(G, grid, source, destination, use_built_in=True)
        
        grid[source[0]][source[1]] = 0.4
        grid[destination[0]][destination[1]] = 0.7
        
        self.ax.set_title("NetworkX dijkstra Algorithm")
        self.redraw_grid()
    
    def button_network_x_a_star_clicked(self, event):
        '''
        Calls the NetworkX's A* Algorithm
        '''
        global grid, G, unchanged_grid
        if source == None or destination == None:
            return
        print "Network X A* running!"

        grid = np.copy(unchanged_grid)        
        _ = pp.get_a_star_shortest_path(G, grid, source, destination, use_built_in=True)

        grid[source[0]][source[1]] = 0.4
        grid[destination[0]][destination[1]] = 0.7

        self.ax.set_title("NetworkX A* Algorithm")
        self.redraw_grid()

if __name__ == '__main__':
    global grid, G, unchanged_grid

    if len(sys.argv) != 2:
        print "\n\n*****************************\nUseage: Need to give a map file as first argument. Example: python gui.py ./maps/map0.txt"
        exit(0)
    
    unchanged_grid, graph = pp.get_graph()
    grid = np.copy(unchanged_grid)
    G = graph
    
    app = QtGui.QApplication(sys.argv)
    main = Window()
    main.show()

    sys.exit(app.exec_())
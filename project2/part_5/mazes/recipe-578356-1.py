# Random Maze Generator using Depth-first Search
# http://en.wikipedia.org/wiki/Maze_generation_algorithm
# FB - 20121214
import random
from PIL import Image

import numpy as np


def create_random(M, N, counter):
	imgx = N; imgy = M
	mx = M; my = N # width and height of the maze

	image = Image.new("RGB", (imgx, imgy))
	pixels = image.load()
	maze = [[0 for x in range(mx)] for y in range(my)]
	dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # 4 directions to move in the maze
	color = [(0,0, 0), (255, 255, 255)] # RGB colors of the maze
	# start the maze from a random cell
	stack = [(random.randint(0, mx - 1), random.randint(0, my - 1))]

	while len(stack) > 0:
	    (cx, cy) = stack[-1]
	    maze[cy][cx] = 1
	    # find a new cell to add
	    nlst = [] # list of available neighbors
	    for i in range(4):
	        nx = cx + dx[i]; ny = cy + dy[i]
	        if nx >= 0 and nx < mx and ny >= 0 and ny < my:
	            if maze[ny][nx] == 0:
	                # of occupied neighbors must be 1
	                ctr = 0
	                for j in range(4):
	                    ex = nx + dx[j]; ey = ny + dy[j]
	                    if ex >= 0 and ex < mx and ey >= 0 and ey < my:
	                        if maze[ey][ex] == 1: ctr += 1
	                if ctr == 1: nlst.append(i)
	    # if 1 or more neighbors available then randomly select one and move
	    if len(nlst) > 0:
	        ir = nlst[random.randint(0, len(nlst) - 1)]
	        cx += dx[ir]; cy += dy[ir]
	        stack.append((cx, cy))
	    else: stack.pop()

	# paint the maze
	for ky in range(imgy):
	    for kx in range(imgx):
	        pixels[kx, ky] = color[maze[my * ky / imgy][mx * kx / imgx]]
#	image.save("maze_" + str(counter) + ".png", "PNG")
	return image


def convert_to_text_file(image, counter):
    array = np.array(image)[:, :, 0]
    array = np.clip(array, 0, 1)
    print np.shape(array)
    print array
    
    file_ = open("maze_%d.txt"%counter, "w+")
    for i in xrange(len(array)):
        for j in xrange(len(array[0])):
            value = (array[i][j]+1)%2
            file_.write("%d "%(value))
        file_.write("\n")

    file_.close()
    
if __name__ == "__main__":


	counter = 0
	for i in xrange(100):
		M = np.random.randint(10, 50)
		N = np.random.randint(10, 50)
		image = create_random(M, N, counter)

		convert_to_text_file(image, counter)

		counter += 1

	print "Done creating test cases!"
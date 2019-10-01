'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates a grid as a 2D array of True/False values (True = traversable). Also returns the dimensions of the grid as a (columns, rows) list.
def myCreateGrid(world, cellsize):
    grid = None
    dimensions = (0, 0)
    ### YOUR CODE GOES BELOW HERE ###
    w = int(math.floor(world.getDimensions()[0] / cellsize))
    h = int(math.floor(world.getDimensions()[1] / cellsize))
    dimensions = (w , h)

    grid = [[True for x in range(h)] for y in range(w)]

    #verify obstacle points
    # i = 0
    # for point in world.getPoints():
    #     i += 1
    #     x = point[0]
    #     y = point[1]
    #     if (not int(math.ceil(x / cellsize)) > w) and (not int(math.ceil(y / cellsize)) > h) and i > 4:
    #         grid[int(math.floor(x / cellsize))][int(math.floor(y / cellsize))] = False

    for obs in world.getObstacles():
        for point in obs.getPoints():
            x = point[0]
            y = point[1]
            if (not int(math.ceil(x / cellsize)) > w) and (not int(math.ceil(y / cellsize)) > h):
                grid[int(math.floor(x / cellsize))][int(math.floor(y / cellsize))] = False



    #verify grid corners
    for x in range(w):
        for y in range(h):
            for obs in world.getObstacles():
                if obs.pointInside((x * cellsize, y * cellsize)):
                    if x >= 1 and y >= 1:
                        grid[x - 1][y - 1] = False
                    if x >= 1:
                        grid[x - 1][y] = False
                    if y >= 1:
                        grid[x][y - 1] = False
                    grid[x][y] = False
                for line in obs.getLines():
                    if x + 1 < w:
                        if rayTrace((x * cellsize, y * cellsize), ((x + 1) * cellsize, y * cellsize), line) != None:
                            grid[x][y] = False
                        if rayTrace((x * cellsize, y * cellsize), (x* cellsize, (y + 1) * cellsize), line) != None:
                            grid[x][y] = False

    ### YOUR CODE GOES ABOVE HERE ###


    return grid, dimensions
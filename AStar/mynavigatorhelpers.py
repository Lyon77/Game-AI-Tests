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

### This function optimizes the given path and returns a new path
### source: the current position of the agent
### dest: the desired destination of the agent
### path: the path previously computed by the A* algorithm
### world: pointer to the world
def shortcutPath(source, dest, path, world, agent):
	### YOUR CODE GOES BELOW HERE ###
    val = True
    complete = [source] + path + [dest]
    while val:
        val = False
        i = 0
        while i < len(complete) - 2:
            if rayTraceWorld(complete[i], complete[i + 2], world.getLinesWithoutBorders()) == None:
                close = False
                for obs in world.getObstacles():
                    for point in obs.getPoints():
                        if minimumDistance((complete[i], complete[i + 2]), point) < agent.getMaxRadius():
                            close = True
                            break
                    if close:
                        break
                if not close:
                    complete.remove(complete[i + 1])
                    val = True
                # i -= 1
            i += 1
    complete = complete[1:]
    path = complete[:-1]

    ### YOUR CODE GOES BELOW HERE ###
    return path
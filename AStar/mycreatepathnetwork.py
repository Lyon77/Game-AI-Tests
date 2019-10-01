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


# Creates a path node network that connects the midpoints of each nav mesh together
def myCreatePathNetwork(world, agent = None):
    nodes = []
    edges = []
    polys = []
    ### YOUR CODE GOES BELOW HERE ###
    #find the list of all polyEdge possible
    polyNodes = world.getPoints()
    polyEdge = list()
    for p1 in range(len(polyNodes) - 2):
        for p2 in range(p1 + 1, len(polyNodes) - 1):
            for p3 in range(p2 + 1, len(polyNodes)):
                hit = False

                newP = [polyNodes[p1], polyNodes[p2], polyNodes[p3]]

                combined = world.getLines() + polyEdge
                for line in combined:
                    if (not set(line).issubset(set(newP))) and (rayTraceNoEndpoints(polyNodes[p1], polyNodes[p2], line) != None or rayTraceNoEndpoints(polyNodes[p3], polyNodes[p2], line) != None or rayTraceNoEndpoints(polyNodes[p1], polyNodes[p3], line) != None):
                        hit = True
                        break
                for point in world.getPoints():
                    if point not in newP:
                        if pointInsidePolygonPoints(point, newP):
                            hit = True
                            break
                for obs in world.getObstacles():
                    if set(newP).issubset(set(obs.getPoints())):
                        hit = True
                        break
                if not hit:
                    polys.append(newP)
                    if (polyNodes[p1], polyNodes[p2]) not in polyEdge and (polyNodes[p2], polyNodes[p1]) not in polyEdge:
                        polyEdge.append((polyNodes[p1], polyNodes[p2]))
                    if (polyNodes[p2], polyNodes[p3]) not in polyEdge and (polyNodes[p3], polyNodes[p2]) not in polyEdge:
                        polyEdge.append((polyNodes[p3], polyNodes[p2]))
                    if (polyNodes[p1], polyNodes[p3]) not in polyEdge and (polyNodes[p1], polyNodes[p3]) not in polyEdge:
                        polyEdge.append((polyNodes[p1], polyNodes[p3]))

    #convert to n-gons
    hasComb = True
    while hasComb:
        hasComb = False
        gone = list()

        for p1 in range(len(polys) - 1):
            for p2 in range(p1 + 1, len(polys)):
                if polys[p1] not in gone and polys[p2] not in gone:
                    com = commonPoints(polys[p1], polys[p2])
                    if len(com) == 2:
                        ind10 = polys[p1].index(com[0])
                        ind11 = polys[p1].index(com[1])
                        ind20 = polys[p2].index(com[0])
                        ind21 = polys[p2].index(com[1])

                        newPoly = list()

                        if ind10 < ind11 and ind10 == ind11 - 1:
                            higher = ind11
                            lower = ind10
                            h2 = ind20
                            l2 = ind21
                        else:
                            higher = ind10
                            lower = ind11
                            h2 = ind21
                            l2 = ind20

                        #go through first poly
                        while higher < len(polys[p1]) and not higher == lower:
                            newPoly.append(polys[p1][higher])
                            higher += 1
                        if not higher == lower:
                            higher = 0
                        while not higher == lower:
                            newPoly.append(polys[p1][higher])
                            higher += 1


                        #go through second poly
                        if (h2 == 0 and l2 == len(polys[p2]) - 1) or (h2 - 1 == l2):
                            while h2 < len(polys[p2]) and not h2 == l2:
                                newPoly.append(polys[p2][h2])
                                h2 += 1
                            if not h2 == l2:
                                h2 = 0
                            while not h2 == l2:
                                newPoly.append(polys[p2][h2])
                                h2 += 1
                        else:
                            while h2 >= 0 and not h2 == l2:
                                newPoly.append(polys[p2][h2])
                                h2 -= 1
                            if not h2 == l2:
                                h2 = len(polys[p2]) - 1
                            while not h2 == l2:
                                newPoly.append(polys[p2][h2])
                                h2 -= 1
                        # check if convex
                        if isConvex(newPoly):
                            gone.append(polys[p1])
                            gone.append(polys[p2])
                            polys.append(newPoly)
                            if com in polyEdge:
                                polyEdge.remove(com)
                            if (com[1], com[0]) in polyEdge:
                                polyEdge.remove((com[1], com[0]))
                            hasComb = True
        for ele in gone:
            polys.remove(ele)

    for i in range(len(polys) - 1):
        for j in range(i + 1, len(polys)):
            com = commonPoints(polys[i], polys[j])
            if len(com) == 2:
                newNode = ((com[0][0] + com[1][0]) // 2, (com[0][1] + com[1][1]) // 2)
                nodes.append(newNode)

                listP = [polys[i], polys[j]]
                for poly in listP:
                    newX = 0
                    newY = 0
                    for p in poly:
                        newX += p[0]
                        newY += p[1]
                    newX = (newX / len(poly)) // 1
                    newY = (newY / len(poly)) // 1
                    center = (newX, newY)
                    nodes.append(center)
                    edges.append((center, newNode))



    ### YOUR CODE GOES ABOVE HERE ###
    return nodes, edges, polys



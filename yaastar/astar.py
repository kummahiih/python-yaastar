"""{-
Copyright (c) 2009 - 2018 Pauli Henrikki Rikula 

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
-}"""

from copy import copy

from .pyheapq import heappop, heappush, updateheapvalue

from .heapset import HeapSet



def reconstruct_path(came_from, current_node):
    """
    came_from : dictionary of nodes and nodes before them in the shortest found path
    current_node : the last node of the path
    """
    if current_node in came_from:
        p = reconstruct_path(came_from,came_from[current_node])
        return p + [current_node]
    else:
        return []


class HeapItem:
    def __init__(self,y,goal, a_map, g_score):
        self.node = y

        """ g_score = Distance from start along optimal path."""
        self.g_score = g_score

        """h_score the heuristic estimates of the distances to goal"""
        self.h_score = a_map.heuristic_estimate_of_distance(y, goal)

        """f_score Estimated total distance from start to goal through y."""
        self.f_score = self.h_score + self.g_score

    def as_tuple(self):
        return (self.f_score, self.g_score, self.h_score, self.node)

    def __hash__(self):
         return self.as_tuple().__hash__()

    def __repr__(self):
        return str(self.as_tuple())

    def type_check(self,other):
        return type(self) == type(other)
    def __lt__(self, other):
        return self.type_check(other) and self.as_tuple().__lt__(other.as_tuple())
    def __le__(self, other):
        return self.type_check(other) and self.as_tuple().__le__(other.as_tuple())
    def __eq__(self, other):
        return self.type_check(other) and self.as_tuple().__eq__(other.as_tuple())
    def __ne__(self, other):
        return self.type_check(other) and self.as_tuple().__ne__(other.as_tuple())
    def __gt__(self, other):
        return self.type_check(other) and self.as_tuple().__gt__(other.as_tuple())
    def __ge__(self, other):
        return self.type_check(other) and self.as_tuple().__ge__(other.as_tuple())




def a_star(start, goal, a_map):
    """
    start = the start node in a_map
    goal = the goal node in a_map
    a_map = a object that should inherit the Map class

    returns a tuple (path, connections, uptated) where:
      path is the optimal path (as a list of points) from the start to the goal. empty if not found,
      
      connections and updated are for debugging (remove them from code if too slow..,):
        connections is the came_from dictionary and
        uptated is the set of the connections, which were uptated from the heap

    """

    """The set of nodes already evaluated."""
    closedset = set([]) 
       

    firstItem = HeapItem(start,goal, a_map, 0.0)

    lastItem = None

    """
    openDict is the set of tentative nodes to be evaluated
    containing just the initial node

    scoreHeap is used as priority queue for next steps. 
    """

    scoreHeap = HeapSet([firstItem])
    openDict = {start:firstItem}


    """ the second last node in the shortest path from start node"""
    came_from = {}

    """this is the set of points which were uptated when they were in the heap
    this is used only to debug the algorithm. remove if slows too much"""
    updateset = set([])
    
    while any(scoreHeap): # is not empty
        """
        the node in openset having 
        the lowest (f_score,g_score,h_score, position) value (f_score means the most ...)
        """
        x  = heappop(scoreHeap)

        if x.node == goal:
            if lastItem == None or lastItem.g_score > x.g_score:
                lastItem = x
        
            if not any(scoreHeap) or scoreHeap[0].f_score > lastItem.g_score:
                return [start] + reconstruct_path(came_from,goal), came_from, updateset
        
        del openDict[x.node]
        closedset.add(x.node)
        
        neighbornodes =  [ 
            (x.g_score + a_map.dist_between(x.node, node_y),node_y ) 
            for node_y in a_map.neighbor_nodes(x.node)
            ]
        #better sort here than update the heap ..
        neighbornodes.sort()
        
        
        for tentative_g_score, node_y in neighbornodes:
            
            if node_y in closedset:
                continue
        
            
            oldy = openDict.get(node_y,None)
            y = copy(oldy)
            
            y = HeapItem(node_y, goal, a_map, tentative_g_score)
            
            if oldy == None:
                openDict[node_y] = y
                came_from[node_y] = x.node
                
                heappush(scoreHeap, y)
                
            elif tentative_g_score < oldy.g_score:
                updateset.add( (node_y, came_from[node_y]) )
                
                openDict[node_y] = y
                came_from[node_y] = x.node
                
                updateheapvalue(scoreHeap, scoreHeap.index(oldy), y)
    
    if lastItem != None:
        return [start] + reconstruct_path(came_from,goal), came_from, updateset
    else: 
        return [], came_from, updateset
 


        


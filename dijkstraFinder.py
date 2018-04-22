import math,string

class Node():
    def __init__(self,name):
        self.name = name
        self.visited = False
        self.neighbours = {}
        self.shortestDistance = math.inf
        self.route = None

    def reset(self):
        self.visited = False
        self.shortestDistance = math.inf

    def setVisited(self):
        self.visited = True
        
    def getVisited(self):
        return self.visited

    def addNeighbours(self,newNeighbours):
        for neighbour in newNeighbours:
            self.neighbours[neighbour[0]] = neighbour[1]

    def getNeighbours(self):
        return self.neighbours
    
    def setNeighbour(self,neighbour,n):
        self.neighbours[neighbour] = n

    def getShortestDistance(self):
        return self.shortestDistance

    def setShortestDistance(self,n):
        self.shortestDistance = n

    def getRoute(self):
        route = ""
        if self.route != self:
            route+=self.route.getRoute()
            route += self.route.getName()
        return route

    def setRoute(self,newRoute):
        self.route = newRoute

    def getName(self):
        return self.name

class PQueue():
    def __init__(self):
        self.array = [] #priority queue initialises with empty array

    def push(self,node):
        self.array.append(node)  #append node to end of array. node = [node,shortest distance]
        self.array = sorted(self.array, key=lambda x: x[1])  #sort array by shortest distance

    def pop(self):
        if not self.isEmpty():
            return self.array.pop(0)

    def isEmpty(self):
        return len(self.array) == 0

def dijkstraPathFind(start):  #dijkstra's shortest path algorithm
    queue = PQueue()   #initialise priority queue
    start.setShortestDistance(0)    #set the starting nodes distance to 0
    start.setRoute(start)       #set route to starting node as startng node
    queue.push([start,start.getShortestDistance()])  #push the starting node to queue with its distance (0)
    while queue.isEmpty() == False:
        currentNode = queue.pop()   #get the next node off the queue
        currentNode[0].setVisited()     #set node to visited
        neighbours = currentNode[0].getNeighbours()     #get neighbours of the current node
        for neighbour in neighbours:
            if neighbour.getVisited() == False:     #if the neighbour hasn't been visited
                if (currentNode[0].getShortestDistance()+neighbours[neighbour] < neighbour.getShortestDistance()):
                    #if current nodes distance + distance to neighbour is less than the neighbours current shortest distance
                    neighbour.setShortestDistance(currentNode[0].getShortestDistance()+neighbours[neighbour])
                    #set its new shortest distance
                    neighbour.setRoute(currentNode[0]) #set current node to route for neighbour
                queue.push([neighbour,neighbour.getShortestDistance()]) #add neighbour to the queue with shortest distance

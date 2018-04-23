from tkinter import *
import tkinter.messagebox
import math,string,pygame

white = (255,255,255)
black = (0,0,0)
try:
    bigNumber = math.inf
except:
    bigNumber = 100000000000000000000000000000000000000000

class App():
    def __init__(self):
        self.screenx = 500
        self.screeny = 500
        self.tickspeed = 16
    def begin(self):
        pygame.init()
        pygame.display.set_caption("Graph Generator")
        self.screen = pygame.display.set_mode((self.screenx, self.screeny))
        self.clock = pygame.time.Clock()
    def exit(self):
        pygame.quit()
        quit()
    def getTickSpeed(self):
        return self.tickspeed
    def getClock(self):
        return self.clock
    def getScreen(self):
        return self.screen

class Graph():
    def __init__(self):
        self.nodes = []
        self.coords = []
        self.startNode = None

    def getNextName(self):
        length = len(self.nodes)
        nextName = string.ascii_lowercase[length%26]
        if str(length//26) != '0':
            nextName += str(length//26)
        return nextName
    
    def setNode(self,node,coords):
        self.nodes.append(node)
        self.coords.append(coords)
        
    def getNodes(self):
        return self.nodes
    
    def getCoords(self):
        return self.coords

    def drawNode(self,i):
        renderText(self.nodes[i].getName(),25,black,self.coords[i][0],self.coords[i][1])
        return pygame.draw.circle(app.getScreen(),black,self.coords[i],30,1)

    def getCoordsFromNode(self,target_node):
        for node in range(len(self.nodes)):
            if self.nodes[node] == target_node:
                return self.coords[node]

    def getStartNode(self):
        return self.startNode

    def setStartNode(self,node):
        self.startNode = node

class Node():
    def __init__(self,name):
        self.name = name
        self.visited = False
        self.neighbours = {}
        self.shortestDistance = bigNumber
        self.route = None

    def reset(self):
        self.visited = False
        self.shortestDistance = bigNumber

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


def saveImage():
    root = Tk()
    root.withdraw()
    response = tkinter.messagebox.askyesno("Save Image","Would you like to save an image of the graph?")
    root.update()
    if response == True:
        pygame.image.save(app.getScreen(),"graph.png")
    else:
        return

def getDigit(key):
    if key == pygame.K_0: return "0"
    elif key == pygame.K_1: return "1"
    elif key == pygame.K_2: return "2"
    elif key == pygame.K_3: return "3"
    elif key == pygame.K_4: return "4"
    elif key == pygame.K_5: return "5"
    elif key == pygame.K_6: return "6"
    elif key == pygame.K_7: return "7"
    elif key == pygame.K_8: return "8"
    elif key == pygame.K_9: return "9"
    elif key == pygame.K_BACKSPACE: return False
    elif key == pygame.K_RETURN: return True

def getConnectionDistance():
    distance = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.exit()
            elif event.type == pygame.KEYDOWN:
                digit = getDigit(event.key)
                if digit != None and digit != True and digit != False:
                    distance += digit
                elif digit == True:
                    if distance != "":
                        return int(distance)
                elif digit == False:
                    length = len(distance)
                    distance = distance[:length-1]

def addConnection(nodeA,nodeB):
    distance = getConnectionDistance()
    nodeA.addNeighbours([[nodeB,distance]])
    nodeB.addNeighbours([[nodeA,distance]])
    print("Connection successful!")

def inBetweenEvents():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if event.button == 1:
                    return False
                elif event.button == 3:
                    nodes = graph.getNodes()
                    for i in range(len(nodes)):
                        if graph.drawNode(i).collidepoint((mx,my)):
                            print(nodes[i].getName())
                            return nodes[i]
    

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: #save image of graph
                saveImage()
            elif event.key == pygame.K_f: #flag node under mouse as start node
                mx, my = pygame.mouse.get_pos()
                nodes = graph.getNodes()
                for i in range(len(nodes)):
                    if graph.drawNode(i).collidepoint((mx,my)):
                        graph.setStartNode(nodes[i])
                        print(nodes[i].getName(),"set as start node.")
            elif event.key == pygame.K_RETURN: #run dijkstra's shortest path algorithm
                for node in graph.getNodes():
                    node.reset()
                if graph.getStartNode() == None:
                    graph.setStartNode(graph.getNodes()[0])
                dijkstraPathFind(graph.getStartNode())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if event.button == 1: #left click - create node
                graph.setNode(Node(graph.getNextName()),[mx,my])
            elif event.button == 3: #righ click - create connection between 2 nodes
                nodes = graph.getNodes()
                for i in range(len(nodes)):
                    if graph.drawNode(i).collidepoint((mx,my)):
                        print(nodes[i].getName())
                        target = inBetweenEvents()
                        if target != False:
                            addConnection(nodes[i],target)

def getMidpoint(c1,c2):
    if c1[0] < c2[0]:
        midx = c1[0] + ((c2[0] - c1[0])/2)
    else:
        midx = c1[0] - ((c1[0] - c2[0])/2)

    if c1[1] < c2[1]:
        midy = c1[1] + ((c2[1] - c1[1])/2)
    else:
        midy = c1[1] - ((c1[1] - c2[1])/2)

    midx = abs(round(midx))
    midy = abs(round(midy))
    return midx,midy
 
def renderText(text,fontSize,colour,x,y):
    font = pygame.font.SysFont("monospace", fontSize)
    text = app.getScreen().blit((font.render(text, 1, colour)),(x,y))
    return text

def render():
    app.getScreen().fill(white)
    nodes = graph.getNodes()
    for i in range(len(nodes)):
        graph.drawNode(i)
        currentNodeCoords = graph.getCoordsFromNode(nodes[i])
        nodeNeighbours = nodes[i].getNeighbours()
        for neighbour in nodeNeighbours:
            neighbourNodeCoords = graph.getCoordsFromNode(neighbour)
            pygame.draw.aaline(app.getScreen(),black,currentNodeCoords,neighbourNodeCoords)
            midx,midy = getMidpoint(currentNodeCoords,neighbourNodeCoords)
            renderText(str(nodeNeighbours[neighbour]),20,black,midx,midy)

    try:
        y = 460
        for i in range(len(nodes)-1,-1,-1):
            info = "{}   {}   {}{}".format(nodes[i].getName(),str(nodes[i].getShortestDistance()),nodes[i].getRoute(),nodes[i].getName())
            renderText(info,25,black,20,y)
            y-=20
    except:
        pass
        
    pygame.display.update()
    app.getClock().tick(app.getTickSpeed())
        

def main():
    app.begin()
    while True:
        render()
        events()

if __name__ == "__main__":
    app = App()
    graph = Graph()
    main()

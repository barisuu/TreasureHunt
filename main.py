#CNG 462 Artificial Intelligence Assignment 1 - Treasure Hunt and Mayan Mazes
#Barış Utku Ünsal - 2315604

# UCS and A* for maze and treasure hunt are different as I did them on separate days and didn't have the time to
# change the treasure hunt to my final version in the maze solution.

from queue import PriorityQueue
import re

def uniformSearch(treasureMap):
    print("\nApplying UCS for treasure map:")
    q = PriorityQueue()                                 #Generating priority queue
    start=treasureMap.get(list(treasureMap.keys())[0])  #Getting the beginning node.
    currentPath=[]
    currentPath.append(list(treasureMap.keys())[0])
    cost=0
    visitedNodes = {}
    visitedNodes[list(treasureMap.keys())[0]]=1
    print(currentPath[-1] + ": Cost is " + str(cost))


    for i in start:
        q.put((i[1],list(treasureMap.keys())[0],i[0]))

    while (q.empty()==False):
        pathNode=q.get()

        if(pathNode[2] not in visitedNodes):
            cost=pathNode[0]
            visitedNodes[pathNode[2]] = 1
            if(pathNode[1]==currentPath[-1]):
                currentPath.append(pathNode[1])
            else:
                currentPath.pop()
                currentPath.pop()
                currentPath.append(pathNode[1])
                currentPath.append(pathNode[2])




        print(str(pathNode[1]) + " - " + str(pathNode[2]) + ": Cost is " + str(cost))

        if("Treasure" in visitedNodes):
            return currentPath
        else:
            frontierNode=treasureMap.get(pathNode[-1])
            for i in frontierNode:
                q.put((i[1]+cost,pathNode[-1],i[0]))

def aStarSearch(treasureMap,heuristics):
    print("\nApplying A* for treasure map:")
    q = PriorityQueue()                                 #Generating priority queue
    start = treasureMap.get(list(treasureMap.keys())[0])
    currentPath = []
    currentPath.append(list(treasureMap.keys())[0])
    cost = 0
    visitedNodes = {}
    visitedNodes[list(treasureMap.keys())[0]] = 1
    print(currentPath[-1] + ": Cost is " + str(cost))

    for i in start:
        q.put((i[1], list(treasureMap.keys())[0], i[0]))

    while (q.empty() == False):
        pathNode = q.get()

        if (pathNode[2] not in visitedNodes):
            cost = pathNode[0]
            visitedNodes[pathNode[2]] = 1
            if (pathNode[1] == currentPath[-1]):
                currentPath.append(pathNode[1])
            else:
                currentPath.pop()
                currentPath.pop()
                currentPath.append(pathNode[1])
                currentPath.append(pathNode[2])

        print(str(pathNode[1]) + " - " + str(pathNode[2]) + ": Cost is " + str(cost))

        if ("Treasure" in visitedNodes):
            return currentPath
        else:
            frontierNode = treasureMap.get(pathNode[-1])
            for i in frontierNode:
                q.put((i[1] + cost + heuristics.get(i[0]), pathNode[-1], i[0]))

def createMaze(fileName):
    try:
        file = open(fileName, "r")
    except IOError:
        exit(1)
    fileString = file.readlines()
    file.close()

    myMaze=[]

    for i in range(0,len(fileString)):
        currentLine = re.split(";", re.sub("\s", "", fileString[i]))
        myMaze.append(currentLine)
    return myMaze

def populateDict(myMaze,mazeDict):
    count=0
    for i in range(1, len(myMaze)):                 #Adding the cost values for each grid and creating an empty list to put the neighbour costs in the future.
        for j in range(1, len(myMaze[i])):
            if(myMaze[i][j]!="W"):
                if(myMaze[i][j]=="G"):
                    mazeDict[str([i, j])] = []      #Only adding an empty list for goal so it's cost is the highest in the end.
                else:
                    mazeDict[str([i, j])] = []
                    mazeDict[str([i, j])].append(count)
                    mazeDict[str([i, j])].append([])
                    count+=1
    for i in mazeDict:
        if mazeDict[i] == []:                       #Adding the cost to goal and empty list for its neighbours
            mazeDict[i].append(count)
            mazeDict[i].append([])
    for i in range(1, len(myMaze)):
        for j in range(1, len(myMaze)):             #Adding the neighbours of each grid by traversing through the maze once again.
            if(myMaze[i][j]!="W" and myMaze[i][j]!="G"):
                if(myMaze[i][j+1]=="E" or myMaze[i][j+1]=="G"):
                    mazeDict[str([i,j])][1].append(mazeDict[str([i,j+1])][0])
                if (myMaze[i+1][j] == "E" or myMaze[i+1][j] == "G"):
                    mazeDict[str([i, j])][1].append(mazeDict[str([i+1, j])][0])
                if (myMaze[i][j-1] == "E" or myMaze[i][j-1] == "G"):
                    mazeDict[str([i, j])][1].append(mazeDict[str([i, j-1])][0])
                if (myMaze[i-1][j] == "E" or myMaze[i-1][j] == "G"):
                    mazeDict[str([i, j])][1].append(mazeDict[str([i-1, j])][0])
def UCSMaze(mazeMap):
    for i in mazeMap:
        if mazeMap[i][1]==[]:
            goal=i
    for i in mazeMap:
        if mazeMap[i][0]==0:
            start=i

    q = PriorityQueue()
    path=[]
    path.append(start)
    cost=0
    visitedNodes={}
    q.put((cost,path))
    while(q.empty()==False):
        currentCost, currentPath = q.get()
        currentNode=currentPath[-1]
        visitedNodes[currentNode] = 1
        if(currentNode == goal):
            print("done")
            return currentPath

        for cost in mazeMap[currentNode][1]:
            for nodes in mazeMap:
                if(mazeMap[nodes][0]==cost and nodes not in visitedNodes):
                    newPath=currentPath.copy()
                    newPath.append(nodes)
                    newCost=currentCost+cost
                    print(str(newPath) + ": Cost is " + str(newCost))
                    q.put((newCost,newPath))

def manhattanHeuristics(mazeSize,node,goal):    #Initially tried to do this with coordinate distances but couldn't get it to work consistently. Changed it to work with costs instead
    x,y = divmod(int(node),mazeSize)
    goalX,goalY = divmod(int(goal),mazeSize)

    xDistance = abs(x - goalX)
    yDistance = abs(y - goalY)

    manhattanDistance= xDistance + yDistance
    return manhattanDistance

def aStarMaze(mazeMap):
    for i in mazeMap:                       #Getting the positions for goal and start. Also getting the cost of goal for manhattan heuristic calculation.
        if mazeMap[i][1]==[]:
            goal=i
            goalCost=mazeMap[i][0]
    for i in mazeMap:
        if mazeMap[i][0]==0:
            start=i
    q = PriorityQueue()

    mazeSize = int(list(re.findall('[0-9]+', goal))[0])
    path=[]
    path.append(start)
    cost= manhattanHeuristics(mazeSize,0,goalCost) #Initially used list(re.findall('[0-9]+', start)) to send coordinates. now sends costs to find heuristic values
    visitedNodes={}
    q.put((cost,path))

    while(q.empty()==False):
        currentCost, currentPath = q.get()
        currentNode=currentPath[-1]
        currentCost = currentCost - manhattanHeuristics(mazeSize,mazeMap[currentNode][0],goalCost)      #Check node cost without heuristic.
        visitedNodes[currentNode] = 1
        if(currentNode == goal):
            return currentPath

        for cost in mazeMap[currentNode][1]:
            for nodes in mazeMap:
                if(mazeMap[nodes][0]==cost and nodes not in visitedNodes):
                    newPath=currentPath.copy()
                    newPath.append(nodes)
                    newCost=currentCost + cost + manhattanHeuristics(mazeSize,cost,goalCost)        #Add heuristic to node and continue.
                    print(str(newPath) + ": Cost is " + str(newCost))
                    q.put((newCost,newPath))

def breadthFirst(mazeMap):

    for i in mazeMap:
        if mazeMap[i][1]==[]:
            goal=i
    for i in mazeMap:
        if mazeMap[i][0]==0:
            start=i
    searchQueue = []
    visitedNodes = []
    path=[]
    path.append(start)

    searchQueue.append((start,path))

    while searchQueue:
        poppedNode,path = searchQueue.pop(0)            #Pop the node and path.
        print("Path: " + str(path))
        if poppedNode==goal:
            return path                           #If at final node return. Returning path in case it will be needed in the future.
        for neighbourCost in mazeMap[poppedNode][1]:
            for neighbour in mazeMap:
                if (mazeMap[neighbour][0] == neighbourCost and neighbour not in visitedNodes):  #If a node isn't visited before add it to the queue and visited list.
                    visitedNodes.append(neighbour)                                              #This is to prevent cycles.
                    searchQueue.append((neighbour,path + [neighbour]))

if __name__ == '__main__':

    treasureMap = {
        "Starting Point": [["Stormy Ocean",4],["Forest",7]],
        "Stormy Ocean": [["Stormy Ocean",20],["Desert",4]],
        "Forest": [["Treasure",4]],
        "Desert": [["Treasure",10]],
        "Treasure": [],
    }

    heuristics = {
        "Starting Point": 1,
        "Stormy Ocean": 2,
        "Forest": 3,
        "Treasure": 0,
        "Desert": 3,
    }

    uniformSearch(treasureMap)
    aStarSearch(treasureMap,heuristics)

    maze1Dictionary={}
    maze2Dictionary = {}

    maze1 = createMaze("maze1.txt")
    populateDict(maze1,maze1Dictionary)     #Populating Dictionary for Maze1 with neighbour values
    maze2 = createMaze("maze2.txt")
    populateDict(maze2, maze2Dictionary)    #Populating Dictionary for Maze2 with neighbour values


    print("\nApplying UCS for Maze 1:")
    UCSMaze(maze1Dictionary)
    print("\nApplying A* for Maze 1:")
    aStarMaze(maze1Dictionary)
    print("\nApplying BFS for Maze 1: ")
    breadthFirst(maze1Dictionary)

    print("\nApplying UCS for Maze 2:")
    UCSMaze(maze1Dictionary)
    print("\nApplying A* for Maze 2:")
    aStarMaze(maze1Dictionary)
    print("\nApplying BFS for Maze 2: ")
    breadthFirst(maze1Dictionary)


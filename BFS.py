import header
import collections				#Header Files
INP_FILE = "../graphs/graph_qsample.dat"	#Getting a sample input from from a file  


def BFS(graph, source):			         #Defining Breadth First Search
    try:
        BFS.bfsTreeNum += 1			 
        print("\nBFS Tree number", BFS.bfsTreeNum)
    except AttributeError:
        BFS.bfsTreeNum = 1
        graph.reset()
        print("BFS Tree number 1")

    Q = collections.deque()
    Q.append(source)
    source.status = "Added to Queue"

    while len(Q) > 0:
        vertex = Q.popleft()
        vertex.status = "Visited"
        print(vertex.name, "  ", end = " ")

        for neighbour in vertex.adjVertices:
            if neighbour.status is None:
                neighbour.status = "Added to Queue"
                Q.append(neighbour)

    if BFS.bfsTreeNum == 1:
        for vertex in graph.vertices:
            if vertex.status != "Visited":
                BFS(graph, vertex)
        print()


fin = open(INP_FILE, "r")
NUMBER_OF_VERTICES= int(fin.readline().split()[0])
g = header.Graph(fin, NUMBER_OF_VERTICES)
g.displayVertices()
BFS(g, g.vertices[4])
fin.close()

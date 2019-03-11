# This piece of source code has been inspired by Padhmamala ma'am's notes and geeksforgeeks.org.
# Link: https://www.geeksforgeeks.org/strongly-connected-components/
# Status of this code: Rough; works on all inputs, but still need to clean it and add comments.
import header
import collections
INP_FILE = "../graphs/graph_qSSC.dat"


def createDFSStack(graph, v, stack):
    try:
        createDFSStack.count += 1
    except AttributeError:
        createDFSStack.count = 0

    v.dfsNum = createDFSStack.count
    v.status = "Visited"

    for neighbour in v.adjVertices:
        if neighbour.status != "Visited":
            createDFSStack(graph, neighbour, stack)

    stack.append(v)

    if v.dfsNum == 0:
        for vertex in graph.vertices:
            if vertex.status != "Visited":  # if any of the nodes have not yet been visited, then run DFS on them..
                createDFSStack(graph, vertex, stack)


def basicDFS(graph, v):
    v.status = "Visited"
    print(v.name, "", end="")
    for neighbour in v.adjVertices:
        if neighbour.status != "Visited":
            basicDFS(graph, neighbour)


def findSSCs(graph, stack):
    print("The strongly connected components of the graph are:-")
    while len(stack) != 0:
        v = stack.pop()
        if v.status != "Visited":
            basicDFS(graph, v)
            print("")


fin = open(INP_FILE, "r")
NUMBER_OF_VERTICES= int(fin.readline().split()[0])
g = header.Graph(fin, NUMBER_OF_VERTICES)
fin.close()
g.displayVertices()

stack = collections.deque()
createDFSStack(g, g.vertices[0], stack)
# Please note that the following code fragment is just for debugging purposes. Uncommenting the following will result in
# an empty stack and subsequent code may fail as they depend on the stack being non-empty.
# print("\nThe stack is:")
# for i in range(g.vertexCount):
#    print(stack.pop().name)
g.revGraph()
findSSCs(g, stack)

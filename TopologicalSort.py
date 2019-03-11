import header
import collections
INP_FILE = "../graphs/graph_topological_sort.dat"


def topologicalSort(graph):
    graph.reset()
    topologicalNum = 0

    Q = collections.deque()
    for vertex in graph.vertices:
        if vertex.indegree == 0:
            Q.append(vertex)
            vertex.status = "Added to Queue"

    print("The topological sorted graph is:-")
    while len(Q) > 0:
        vertex = Q.popleft()
        topologicalNum += 1
        print(vertex.name, "  ", end="")
        vertex.status = "Visited"

        for neighbour in vertex.adjVertices:
            if neighbour.status is None:
                neighbour.indegree -= 1
                if neighbour.indegree == 0:
                    Q.append(neighbour)
                    neighbour.status = "Added to queue"

    if topologicalNum != graph.vertexCount:
        print("There was a cycle!")
    else:
        print()


fin = open(INP_FILE, "r")
NUMBER_OF_VERTICES= int(fin.readline().split()[0])
g = header.Graph(fin, NUMBER_OF_VERTICES)
g.displayVertices()
topologicalSort(g)
fin.close()

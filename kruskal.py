import header
import heapq
INP_FILE = "../graphs/graph_qKruskal.dat"


def graphToHeap(graph):
    edgesHeap = list(graph.edges.values())
    heapq.heapify(edgesHeap)
    return edgesHeap


def kruskal(graph):
    uf = header.UnionFind(graph.vertexCount)    # the union find object...
    edgesHeap = graphToHeap(graph)              # a heap of all the edges
    edgesAccepted = 0
    cost = 0

    print("Edges in the MST are:-")
    while edgesAccepted != graph.vertexCount - 1:
        minEdge = heapq.heappop(edgesHeap)

        if not uf.connected(minEdge.src.number, minEdge.dest.number):
            uf.unify(minEdge.src.number, minEdge.dest.number)
            print(minEdge.src.name, " -> ", minEdge.dest.name, " (", minEdge.weight, ")", sep="")
            cost += minEdge.weight
            edgesAccepted += 1

    print("Total cost is", cost)


fin = open(INP_FILE, "r")
NUMBER_OF_VERTICES= int(fin.readline().split()[0])
g = header.Graph(fin, NUMBER_OF_VERTICES)
fin.close()
kruskal(g)

import header
INP_FILE = "../graphs/graph_dijkstra_NetSec2.dat"


class Node:
    def __init__(self, vertex):
        self.vertex = vertex
        self.known = False
        self.dist = None
        self.path = None


class DTable:
    def __init__(self, graph):
        self.rows = []
        for vertex in graph.vertices:
            vertex.dRow = Node(vertex)
            self.rows.append(vertex.dRow)

    def findNextVertex(self):
        lowestRow = None

        for row in self.rows:
            if not row.known and row.dist is not None and (lowestRow is None or row.dist < lowestRow.dist):
                lowestRow = row

        if lowestRow is None:
            return None

        return lowestRow.vertex


def printPath(source, dest, last = True):                       # if last = True, then it is the very first call
    if last and source == dest:                                 # if source & dest are the same & it's the 1st call then
        print("(", dest.name, " -> ", dest.name, ")", sep="")   # it means that we are printing the path from the source
        return                                                  # to itself

    elif dest.dRow.path == 0:       # we have reached the end of the recursion; i.e., we have reached the source
        print("(", dest.name, " -> ", end="", sep="")
        return

    printPath(source, dest.dRow.path, False)    # False is sent to indicate that it is not the first call to printPath()
    if last:
        print(dest.name, ")", sep="")
    else:
        print(dest.name, "-> ", end="")


def dijkstra(graph, source):
    dtable = DTable(graph)

    source.dRow.dist = 0
    source.dRow.path = 0
    v = source

    while v is not None:
        for w in v.adjVertices:
            newDist = v.dRow.dist + graph.edges[(v, w)].weight
            if not w.dRow.known and (w.dRow.dist is None or newDist < w.dRow.dist):
                w.dRow.dist = newDist
                w.dRow.path = v

        v.dRow.known = True
        v = dtable.findNextVertex()

    for vertex in graph.vertices:
        print("Shortest path from", source.name, "to", vertex.name, "Distance: ", end= "")
        if vertex.dRow.dist is None:
            print("INF", end="")
        else:
            print(vertex.dRow.dist, "", end="")
            printPath(source, vertex)


fin = open(INP_FILE, "r")
NUMBER_OF_VERTICES= int(fin.readline().split()[0])
g = header.Graph(fin, NUMBER_OF_VERTICES)
fin.close()
# g.displayVertices()
dijkstra(g, g.vertices[0])

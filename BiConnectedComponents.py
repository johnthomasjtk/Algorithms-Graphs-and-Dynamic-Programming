import header
import collections
INP_FILE = "../graphs/graph_articulation_points2.dat"


def findBiConnectedComponents(graph, v):
    try:
        findBiConnectedComponents.counter += 1
    except AttributeError:
        findBiConnectedComponents.counter = 1
        findBiConnectedComponents.componentNum = 1
        findBiConnectedComponents.stack = collections.deque()
        print("The Bi-Connected components are:-\nComponent 1:")
        graph.reset()

    v.status = "Visited"
    v.dfsNum = v.low = findBiConnectedComponents.counter
    findBiConnectedComponents.stack.append(v)
    #print(v.name)

    for w in v.adjVertices:
        if w.status != "Visited":
            w.parent = v
            findBiConnectedComponents(graph, w)

            if w.low >= v.dfsNum and v.colour != "Black":       # v is an articulation point
                while True:
                    vertex = findBiConnectedComponents.stack.pop()
                    print(vertex.name, "  ", end="")

                    if vertex == v:
                        break

                findBiConnectedComponents.componentNum += 1
                print("\nComponent", findBiConnectedComponents.componentNum)
                print(v.name, "  ", end="")
                v.colour = "Black"

        elif v.parent != w:
            v.low = min(v.low, w.dfsNum)


fin = open(INP_FILE, "r")
NUMBER_OF_VERTICES= int(fin.readline().split()[0])
g = header.Graph(fin, NUMBER_OF_VERTICES)
g.displayVertices()
findBiConnectedComponents(g, g.vertices[0])
fin.close()

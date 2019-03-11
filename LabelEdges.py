import header
INP_FILE = "../graphs/graph_edge_labelling.dat"


def labelEdges(graph, v):
    try:
        labelEdges.counter += 1
    except AttributeError:
        labelEdges.counter = 1
        graph.reset()
        print("The edges are:-")

    v.colour = "Grey"
    v.status = "Visited"
    v.dfsNum = labelEdges.counter

    for w in v.adjVertices:
        if w.status != "Visited":   # if it has not been visited, then visit it and the edge becomes a tree edge
            w.parent = v
            graph.edges[(v, w)].type = "Tree Edge"
            print(v.name +  ",", w.name, "is a tree edge")
            labelEdges(graph, w)

        elif v.parent != w:

            if v.dfsNum > w.dfsNum:
                if w.colour == "Grey":
                    graph.edges[(v, w)].type = "Back Edge"
                    print(v.name + ",", w.name, "is a back edge")
                else:
                    graph.edges[(v, w)].type = "Cross Edge"
                    print(v.name + ",", w.name, "is a cross edge")
            else:
                graph.edges[(v, w)].type = "Forward Edge"
                print(v.name + ",", w.name, "is a forward edge")

    v.colour = "Black"
    if v.dfsNum == 1:
        for vertex in graph.vertices:
            if vertex.status != "Visited":
                labelEdges(graph, vertex)
        print()


fin = open(INP_FILE, "r")
NUMBER_OF_VERTICES= int(fin.readline().split()[0])
g = header.Graph(fin, NUMBER_OF_VERTICES)
g.displayVertices()
labelEdges(g, g.vertices[2])
fin.close()

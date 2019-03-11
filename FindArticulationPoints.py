import header
INP_FILE = "../graphs/graph_art_points7.dat"


def findArticulationPoints(graph, v, firstInstance=True):
    try:
        findArticulationPoints.counter += 1
    except (AttributeError, TypeError):
        findArticulationPoints.counter = 1
        childrenOfRoot = 0
        print("Source is", v.name)
        if firstInstance:
            graph.reset()

    v.dfsNum = v.low = findArticulationPoints.counter
    v.status = "Visited"

    for w in v.adjVertices:
        if w.status != "Visited":
            if v.dfsNum == 1:           # if it is the root..
                childrenOfRoot += 1     # .. then increment the count of children of root.
            w.parent = v
            findArticulationPoints(graph, w, False)

            if v.dfsNum != 1 and w.low >= v.dfsNum and v.colour != "Printed":
                print(v.name, "is an articulation point")
                v.colour = "Printed"
            v.low = min(v.low, w.low)

        elif v.parent != w:
            v.low = min(v.low, w.dfsNum)

    if v.dfsNum == 1 and childrenOfRoot > 1:
        print(v.name, "is an articulation point")

    if firstInstance:                       # if this is the very first instance to be called, i.e. last instance of the function call on the stack
        for vertex in graph.vertices:       # ..then traverse the list of vertices..
            if vertex.status != "Visited":  # ..and if a vertex has still not yet been visited..
                findArticulationPoints.counter = None           # then reset the function counter.. (Note that assigning 0 won't work because
                                                                # 'childrenOfRoot' has to be initialised in the new instance. When it is set
                                                                # to None, the exception gets triggered and 'childrenOfRoot' gets initialised)
                findArticulationPoints(graph, vertex, False)      # ..and run the function on that unvisited vertex


fin = open(INP_FILE, "r")
NUMBER_OF_VERTICES = int(fin.readline().split()[0])
g = header.Graph(fin, NUMBER_OF_VERTICES)
g.displayVertices()
source = g.vertices[int(fin.readline().split()[0]) - 1]
findArticulationPoints(g, source)
fin.close()

# Finds out the articulation points of the input Graph and outputs it to fout. The source, v, needs to be passed. This is a modified DFS algo
# The argument firstInstance helps distinguish between the very first function instance and the recursive instances.
def findArticulationPoints(graph, v, fout, firstInstance=True):
    try:                                        # Python does not support static variables as C does, this is a small bodge
                                                # to emulate the same effect
        findArticulationPoints.counter += 1     # try incrementing the function counter variable..
    except (AttributeError, TypeError):         # if it has not yet been defined, then Python will throw an error..
        findArticulationPoints.counter = 1      # initialise the counter. It is used to assign a discovery number to each vertex
        childrenOfRoot = 0                      # used to keep track of the number of children of root in the resultant DFS tree
        if firstInstance:                       # if this instance is the very first function call then..
            graph.reset()                       # ..reset the graph in case some other algo was called before this

    v.dfsNum = v.low = findArticulationPoints.counter   # assign the next discovery number to the current vertex 'v'
    v.status = "Visited"                                # Mark 'v' as Visited

    for w in v.adjVertices:                             # for each neighbour of v, do the following..
        if w.status != "Visited":                       # if the neighbour is unvisited..
            if v.dfsNum == 1:                           # if the current vertex, 'v' is the root..
                childrenOfRoot += 1                     # .. then increment the count of children of root.
            w.parent = v                                # make the neighbour's parent as the current vertex, 'v'
            findArticulationPoints(graph, w, fout, False)   # call the same function on the neighbouring vertex

            # we are checking for articulation points for non-root nodes. Hence, proceed only if the discovery number of the current vertex is not 1
            # if the 'low' of neighbour 'w' is greater than the discovery number of the current vertex 'v', it means that 'w' does not have any path
            # to any vertex higher than the current vertex, 'v'. Hence, 'v' is an articulation point. Also check if the colour of the vertex is
            # "Printed". This prevents the same vertex being printed as an articulation point more than once in case the same vertex is an
            # articulation point for multiple sub-graphs
            if v.dfsNum != 1 and w.low >= v.dfsNum and v.colour != "Printed":
                fout.write(v.name + "\n")
                v.colour = "Printed"

            v.low = min(v.low, w.low)       # make the low of the current vertex as the minimum of v.low and w.low (i.e. min of current vertex's
                                            # low and neighbour's low)

        elif v.parent != w:                 # else if the neighbour has already been visited, and the neighbour is not the current vertex's parent
            v.low = min(v.low, w.dfsNum)    # then it means that the current vertex can reach an already visited vertex. So find out the min of
                                            # the current low and the discovery number of the neighbouring vertex.

    if v.dfsNum == 1 and childrenOfRoot > 1:    # condition for finding if the root node is an articulation point or not. If the root has more than
        fout.write(v.name + " (root of the dfs tree)")  # one child, then it is an articulation point

    if firstInstance:                       # if this is the very first instance to be called, i.e. last instance of the function call on the stack
        for vertex in graph.vertices:       # ..then traverse the list of vertices..
            if vertex.status != "Visited":  # ..and if a vertex has still not yet been visited..
                findArticulationPoints.counter = None           # then reset the function counter.. (Note that assigning 0 won't work because
                                                                # 'childrenOfRoot' has to be initialised in the new instance. When it is set
                                                                # to None, the exception gets triggered and 'childrenOfRoot' gets initialised)
                findArticulationPoints(graph, vertex, fout, False)      # ..and run the function on that unvisited vertex
        fout.write("\n\n")

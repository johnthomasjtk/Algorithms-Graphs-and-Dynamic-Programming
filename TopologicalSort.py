import collections


def topologicalSort(graph, fout):   # Performs Topological sort on input Graph object and writes it to fout
    graph.reset()                   # Reset the graph in case some other algo was called before this
    topologicalNum = 0              # used to detect cycles. At the end of the algo, if we find that the topological number
                                    # does not equal the number of vertices, then we can conclude that there is a cycle

    Q = collections.deque()         # create an empty queue
    for vertex in graph.vertices:   # traverse through all the vertices..
        if vertex.indegree == 0:    # ..and if their indegree is 0..
            Q.append(vertex)        # .. then add them to the queue
            vertex.status = "Added to Queue"    # change the status of the vertex

    number = 1                      # used to print the discovery time of each vertex in the output file
    fout.write("The topological sort of the first graph is:\nVERTEX\tNUMBER\n")
    while len(Q) > 0:               # continue until the queue is empty
        vertex = Q.popleft()        # remove the next vertex in the queue
        topologicalNum += 1         # assign the next topological number to that vertex
        message = vertex.name + "\t\t" + str(number) + "\n"     # print the name and the discovery number to the file
        fout.write(message)
        number += 1                 # increment the discovery number
        vertex.status = "Visited"   # change the status of the vertex as it has been visited

        for neighbour in vertex.adjVertices:    # for each of the neighbours of the vertex..
            if neighbour.status is None:        # if the vertex has never been added to the queue..
                neighbour.indegree -= 1         # then decrement the neighbour's indegree by 1 as the vertex has now been removed 							from the graph
                if neighbour.indegree == 0:     # ..and if the indegree of the neighbour becomes 0..
                    Q.append(neighbour)         # then add it to the queue..
                    neighbour.status = "Added to queue"     # ..and change its status

    if topologicalNum != graph.vertexCount:     # if we find that the topological number does not equal the number of vertices,
        fout.write("There was a cycle!")        # then we can conclude that there is a cycle
    else:
        fout.write("\n")

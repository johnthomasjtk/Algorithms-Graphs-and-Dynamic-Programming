import heapq
import header


def graphToHeap(graph):                     # This function creates a min heap out of the edges of a graph
    edgesHeap = list(graph.edges.values())  # create a list (array) of all the Edge objects of a graph
    heapq.heapify(edgesHeap)                # create a min heap of the edges (the same array is used to store the heap)..
    return edgesHeap                        # ..and return it


def kruskal(graph, fout):                       # Performs the Kruskal's algo on the input graph and writes it to fout
    uf = header.UnionFind(graph.vertexCount)    # the union find object, we specify the number of nodes to the ctor
    edgesHeap = graphToHeap(graph)              # create a heap of all the edges
    edgesAccepted = 0                           # keeps track of how many edges are accepted
    cost = 0                                    # keeps track of the total cost of the resultant MST

    fout.write("The edges in the minimum spanning tree for the third graph are:\n")
    while edgesAccepted != graph.vertexCount - 1:   # the number of edges in the MST is one less than the number of vertices.
                                                    # So, stop after (vertexCount - 1) edges have been accepted
        minEdge = heapq.heappop(edgesHeap)          # get the next edge with the least weight

        if not uf.connected(minEdge.src.number, minEdge.dest.number):   # this is the find operation. If adding this edge
            edgesAccepted += 1                      # to the partially created MST does not create cycles, then accept it
            uf.unify(minEdge.src.number, minEdge.dest.number)           # unify the edge to the partial MST graph (union operation)
            fout.write("(" + minEdge.src.name + ", " + minEdge.dest.name + ", " + str(minEdge.weight) + ")\n")
            cost += minEdge.weight                  # write the details of the edge to the file and increment the cost..

    fout.write("Its cost is " + str(cost) + "\n\n")     # write the final cost of the MST to file

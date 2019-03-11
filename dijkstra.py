# This class contains the fields required in a single row of the Dijkstra's table.
class Node:
    def __init__(self, vertex):     # constructor; needs the Vertex object which associates a row with a particular vertex
        self.vertex = vertex
        self.known = False          # Known field in the Dijkstra's table; by default the vertex is not known
        self.dist = None            # keeps track of the cumulative distance; infinity is represented by None (NULL)
        self.path = None            # the path field in the Dijkstra's table; infinity is represented by None (NULL)


# The Dijkstra's Table can be thought of an array of rows (and each row here is a Node object)
class DTable:
    def __init__(self, graph):              # constructor, takes the graph as object
        self.rows = []
        for vertex in graph.vertices:       # for each vertex in the graph..
            vertex.dRow = Node(vertex)      # Populate the vertex's dRow field with the address of the row; this way we
                                            # can access the row if we have the Vertex object
            self.rows.append(vertex.dRow)   # append this newly created row object to the Dijkstra's table

    def findNextVertex(self):               # find's the next Vertex that should be explored
        lowestRow = None                    # Assuming that there is no edge that needs to be explored

        for row in self.rows:               # for each row in the Dijkstra's table
            # process the row only if it is not known; and the row has a valid distance (i.e., it's not infinity)
            # we'll take this row as the lowest; if either we have not yet found any other lowest row or if the distance
            # of the current row is lower than the the previously known lowest row entry
            if not row.known and row.dist is not None and (lowestRow is None or row.dist < lowestRow.dist):
                lowestRow = row

        if lowestRow is None:               # at the end if we are unable to find any entry, then it means that all
            return None                     # vertices have been explored, so return None (NULL)

        return lowestRow.vertex             # return the vertex with the lowest distance which is not yet known


# prints the path from the source to a destination vertex and writes it to the file object fout.
# if firstInstance = True, then it is the very first call
def printPath(source, dest, fout, firstInstance = True):
    if firstInstance and source == dest:                            # if this is the first instance and source & dest are the same
        fout.write("(" + dest.name + " -> " + dest.name + ")\n")    # then it means that we are printing the path from the source
        return                                                      # to itself (eg: A to A)

    elif dest.dRow.path == 0:                                       # we have reached the end of the recursion; i.e., we
        fout.write("(" + dest.name + " -> ")                        # have reached the source. So add a bracket, write the
        return                                                      # name of the source vertex and return

    printPath(source, dest.dRow.path, fout, False)  # False is sent to indicate that it is not the first call to printPath()
    if firstInstance:                               # if this is the first instance, that means it is the last instance
        fout.write(dest.name + ")\n")               # on the stack; so print the closing bracket and a new line
    else:
        fout.write(dest.name + "-> ")               # else, print the vertex name and print an arrow


# Performs the Dijkstra's Single Source Shortest Path algo on the input graph. Requires a source vertex. Writes output to fout
def dijkstra(graph, source, fout):
    dtable = DTable(graph)              # Initialise the Dijkstra's table

    source.dRow.dist = 0                # make the source vertex's distance..
    source.dRow.path = 0                # ..and path as 0 in the table
    v = source

    while v is not None:                # Continue until all vertices have been explored
        for w in v.adjVertices:         # For each neighbouring vertex..
            newDist = v.dRow.dist + graph.edges[(v, w)].weight                          # calculate the new distance..

            # ..but proceed only if the neighbour is not known and either the distance to it is infinity or the new
            # distance is lesser than the previously known distance..
            if not w.dRow.known and (w.dRow.dist is None or newDist < w.dRow.dist):
                w.dRow.dist = newDist   # ..in such a case, update the distance with the new distance..
                w.dRow.path = v         # ..and make the path point to the current vertex, 'v'

        v.dRow.known = True             # once all the neighbours of 'v' have been checked, we mark 'v' as explored, i.e.
        v = dtable.findNextVertex()     # it is now known..and find the next vertex that we need to process

    for vertex in graph.vertices:       # for each vertex, print the details..
        fout.write("Shortest path from " + source.name + " to " + vertex.name + " Distance: ")
        if vertex.dRow.dist is None:    # if the distance is None, it means that that vertex cannot be reached..
            fout.write("INF")           # ..hence print INF (infinity)
        else:
            fout.write(str(vertex.dRow.dist) + " ")     # else, print the distance
            printPath(source, vertex, fout)             # and print out the path to it
    fout.write("\n\n")

INP_FILE = "graph.dat"          # specifies the input file which contains the graph information
NUMBER_OF_VERTICES = 7          # constant denoting number of vertices per graph


# This class defines the blueprint of a Vertex object.
class Vertex:
    count = 0                       # class variable (not an instance variable) used to automatically name vertices.

    def __init__(self):             # constructor
        self.name = chr(ord('A') + Vertex.count)    # automatically names vertices starting from 'A'
        self.number = Vertex.count  # used by UnionFind for Kruskal's algo; used as an index into the array which keeps track of the components.
        Vertex.count += 1
        self.adjVertices = []       # an array of pointers pointing to the adjacent vertices
        self.revAdjVertices = []    # this is just a temporary list to hold the adjacent vertices while reversing a graph
        self.status = None          # the status can be made "Visited" when a vertex has been visited; by default it is None (NULL)
        self.indegree = 0           # keeps track of the indegree of a vertex
        self.dfsNum = None          # keeps track of the discovery number of a vertex during a DFS traversal.
        self.low = None             # keeps track of the lowest vertex DFSnum that can be reached from a vertex; used in finding Articulation points
        self.parent = None          # keeps track of the parent node of a vertex; used in finding articulation points.
        self.colour = None          # used to keep track of whether a vertex has already been printed once; used in finding
                                    # articulation points, when the same vertex is identified as an articulation point by multiple sub-graphs
        self.dRow = None            # stores a pointer to dijkstra-Row object; which contains fields used during Dijkstra's algo

    def __del__(self):              # destructor
        Vertex.count -= 1           # if any temporary Vertex object gets created, then reduce the count as soon as it goes out of scope
                                    # so that the next Vertex object would get that name.

    def reset(self):                # resets the class counter. Used before reading a new graph
        Vertex.count = 0


# This class defines the blueprint of an Edge object.
class Edge:
    count = 1                       # class variable (not an instance variable) used to automatically number edges.

    def __init__(self):             # constructor
        self.label = Edge.count     # automatically numbers vertices starting from 1
        Edge.count += 1
        self.weight = 0             # stores the weight of the edge
        self.src = None             # a pointer to the source vertex object
        self.dest = None            # a pointer to the destination vertex object
        self.type = None            # stores the type of the edge; used while labelling edges (not relevant for this assignment).
                                    # Will be used to classify edges into tree, back, forward and cross edges

    def __del__(self):              # destructor
        Edge.count -= 1             # if any temporary Edge object gets created, then reduce the count as soon as it goes out of scope
                                    # so that the next Vertex object would get that number.

    def __lt__(self, other):        # This function compares two Edge objects; and is required while making a heap of the edges.
        return self.weight < other.weight   # Such a heap is required for implementing the Kruskal's algo.

    def reset(self):
        Edge.count = 0              # resets the class counter. Used before reading a new graph


# This class defines the blueprint of a Graph object. A graph is a set of Vertices and Edges.
# The vertices are stored as a list (array) and the edges are stored as a dictionary (hashtable).
class Graph:

    def __init__(self, fin, vertexCount):
        self.vertexCount = vertexCount      # Keeps track of the number of vertices in the graph
        self.vertices = []                  # list containing Vertex objects. vertices[0] contains a pointer to the first Vertex object, vertices[1] to the second and so on..
        self.edges = {}                     # hashtable containing all the edges. The index into the hashtable is a tuple (v, w); where v is the source vertex object and w is the destination
                                            # vertex object. For example, edges[(vertices[0], vertices[1])] will return an Edge object which represents an edge between the first and second vertex.

        for i in range(vertexCount):        # create new Vertex objects and append them to the vertices list
            self.vertices.append(Vertex())

        # need to read in the graph. We build the graph here.
        for i in range(vertexCount):        # Each line represents the adjacency list for a vertex. For each line in the input file, do the following
            line = fin.readline().split()   # Read a line from input file; split on the basis of whitespaces
            adjVerticesCount = int(line[0]) # The first integer on the line represents the number of adjacent vertices
            line = line[1:]                 # remove the first element from out input list.

            for j in range(adjVerticesCount):           # adjVerticesCount pairs of integers follow on the same line
                neighbour = self.vertices[int(line[j*2]) - 1]   # Each line[j*2] gives the adjacent vertex number. Since our vertices array index starts from 0, we need to subtract 1
                neighbour.indegree += 1                 # increment the indegree of the neighbour vertex object

                weight = int(line[j*2 + 1])             # Each line[j*2 + 1] represents the weight
                newEdge = Edge()                        # create an Edge object..
                newEdge.weight = weight                 # populate its fields
                newEdge.src = self.vertices[i]          # pointer to the source Vertex object
                newEdge.dest = neighbour                # pointer to the destination Vertex object

                self.vertices[i].adjVertices.append(neighbour)      # append the neighbour's pointer to the adjacency list of the current Vertex object
                self.edges[(self.vertices[i], neighbour)] = newEdge     # add the Edge object to the dictionary (hashtable)

    def displayVertices(self):              # This function is used solely for debugging purposes. Displays the graph
        print("The graph is:-")             # Prints the adjacency list of each Vertex with the edge weights in brackets

        for i in range(self.vertexCount):
            print("Vertex " + self.vertices[i].name, " -->  ", end="")      # Print the Vertex name
            adjVerticesCount = len(self.vertices[i].adjVertices)

            for j in range(adjVerticesCount):
                neighbour = self.vertices[i].adjVertices[j]                 # Find out the neighbour Vertex object..
                weight = self.edges[(self.vertices[i], neighbour)].weight   # ..and find out the edge weight..
                print(neighbour.name + "(" + str(weight) + ")", end="")     # ..and print it
                if j != adjVerticesCount - 1:                               # Print a comma only if this is not the last neighbour
                    print(", ", end="")
            print()                         # print a new line after each Vertex's adjacent list has been printed
        print()                             # print a new line at the end

    def displayEdges(self):                 # This function is used solely for debugging purposes. Displays the edges of the graph
        edgeList = list(self.edges.values())    # Extract all the Edge objects from the dictionary (hashtable)

        print("The edges are:-")
        print("Src\tDest\tLabel\tWeight\tType")
        for edge in edgeList:               # print all the details of each edge
            print(edge.src.name + "\t" + edge.dest.name + "\t\t" + str(edge.label) + "\t\t" + str(edge.weight) + "\t\t" + str(edge.type))
        print()                             # print a new line at the end

    def displayVerticesStatus(self):        # This function is used solely for debugging purposes. Displays the status field of all the Vertex objects in the graph
        print("The status of the vertices are:-")
        for i in range(self.vertexCount):                                   # for each Vertex object..
            print(self.vertices[i].name, " : ", self.vertices[i].status)    # ..display its name and status
        print()

    def reset(self):                        # This function resets some of the fields of every Vertex object. This is useful specially when DFS needs to be run twice on the same Graph object, for example.
        for i in range(self.vertexCount):   # for evey Vertex object..
            self.vertices[i].status = None  # reset the status to None (NULL)
            self.vertices[i].colour = None  # ..the colour..
            self.vertices[i].dfsNum = None  # ..the dfsNum (discovery number/time)..
            self.vertices[i].low = None     # ..the low..
            self.vertices[i].parent = None  # ..and the parent

    def resetVertexNEdge(self):             # This function resets the counters of classes Vertex and Edge. This is required while reading graphs one after the other from the input file.
                                            # These class counters are used to automatically name the vertices and edges; so they need to be reset to 0 before reading a new graph
        Vertex.count = 0
        Edge.count = 0

    def revGraph(self):                     # This function reverses the direction of each edges of a Graph object
        self.reset()                        # reset the vertices of the graph
        tempEdges = self.edges              # since the edges dictionary (hashtable) is going to be overwritten, make a temporary copy of it
        self.edges = {}                     # initialise it to an empty dictionary (hashtable)
        for vertex in self.vertices:        # for each vertex..
            vertex.revAdjVertices = vertex.adjVertices  # temporarily copy the adjacency list into revAdjVertices
            vertex.adjVertices = []         # initialise adjVertices list to an empty list
            vertex.indegree = 0             # reset the vertex's indegree as well

        for vertex in self.vertices:        # for each vertex..
            for neighbour in vertex.revAdjVertices:     # for each of the neighbouring vertex
                neighbour.adjVertices.append(vertex)    # in the reverse graph, 'vertex' would become the neighbour of 'neighbour'; so append the current vertex object to the adjacency list of the neighbour vertex
                vertex.indegree += 1                    # increase the indegree of the current vertex; as the edge is now pointing towards the current vertex

                edge = tempEdges[(vertex, neighbour)]   # fetch the edge object...
                edge.src = neighbour                    # assign the source of the edge as the neighbour
                edge.dest = vertex                      # assign the destination as the current vertex
                edge.type = None                        # reset the edge type

                self.edges[(neighbour, vertex)] = edge  # assign this edge object to the edges hashtable at the index (neighbour, vertex); since the edge has now been reversed.
            vertex.revAdjVertices = []      # get rid of the previous adjacency list.


# This code has been adapted from: https://github.com/williamfiset/data-structures/tree/master/com/williamfiset/datastructures/unionfind
# Explanation video & playlist on UnionFind: https://www.youtube.com/watch?v=KbFlZYCpONw&list=PLDV1Zeh2NRsBI1C-mR6ZhHTyfoEJWlxvq&index=5
# Implementation of the Disjoint Set/Union Find data structure. Employs path compression.
class UnionFind:
    def __init__(self, size):           # Constructor. size represents the total number of independent objects/components in the beginning. In our case, this would equal the number of vertices in the graph
        if size <= 0:
            raise TypeError("size <= 0 is not allowed")

        self.componentsCount = size     # Keeps track of the number of components. Initially, the number of components is equal to the number of vertices.
        self.componentSize = [1] * size # Keeps track of the size of each component. Initially, all components have just one element in them, hence their size would be 1
        self.link = []                  # link[i] points to the parent of i, if link[i] = i then i is a root node

        for i in range(size):           # Initially, each vertex is its own parent.
            self.link.append(i)

    def find(self, v):                  # This function  finds which component/set 'v' belongs to; takes amortized constant time. Employs path compression.
        root = v
        while root != self.link[root]:  # Find the root of the component/set
            root = self.link[root]

        # Compress the path leading back to the root. Doing this operation is called "path compression" and is what gives us amortized time complexity.
        while self.link[v] != root:     # Continue until a node is found which already points to the root.
            nextNode = self.link[v]     # temporarily store the next node's address (the node's index in this case)
            self.link[v] = root         # make it point to the root of the component..
            v = nextNode                # ..and move on to the next node

        return root                     # return the root of the component

    def connected(self, v, w):          # returns True if two nodes, v and w are already connected to the same component; False otherwise.
        return self.find(v) == self.find(w)     # This function helps us detect cycles in the Minimum Spanning Tree during Kruskal's algo

    def componentSize(self, v):         # used to find the size of the component that the node v belongs to. This function is not required for Kruskal's algo
        return self.componentSize[self.find(v)]

    def unify(self, v, w):              # This function unifies the components/sets containing elements v and w
        root1 = self.find(v)
        root2 = self.find(w)

        if root1 == root2:              # These elements are already in the same group!
            return

        if self.componentSize[root1] < self.componentSize[root2]:   # Merge smaller component/set into the larger one.
            self.componentSize[root2] += self.componentSize[root1]  # The new size of the component would be the sum of the sizes of the two sub-components
            self.link[root1] = root2                                # Merge root1 to root2; root1 now points to root2
        else:                           # else, if root2 is smaller than root1, then..
            self.componentSize[root1] += self.componentSize[root2]
            self.link[root2] = root1    # merge root2 to root1; root2 now points to root1

        self.componentsCount -= 1       # Since the roots found are different we know that the number of components/sets has decreased by one

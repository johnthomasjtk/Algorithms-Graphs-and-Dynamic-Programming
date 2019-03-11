class Vertex:
    count = 0

    def __init__(self):
        self.name = chr(ord('A') + Vertex.count)
        self.number = Vertex.count  # used by UnionFind for Kruskal's algo
        Vertex.count += 1
        self.adjVertices = []
        self.revAdjVertices = []    # this is just a temporary list to hold the adjacent vertices while reversing a graph
        self.status = None
        self.indegree = 0
        self.dfsNum = None
        self.low = None
        self.parent = None
        self.colour = None
        self.dRow = None            # dijkstra Row

    def __del__(self):
        Vertex.count -= 1


class Edge:
    count = 1

    def __init__(self):
        self.label = Edge.count
        Edge.count += 1
        self.weight = 0
        self.src = None
        self.dest = None
        self.type = None

    def __del__(self):
        Edge.count -= 1

    # This function is required while making a heap of the edges. This is required for implementing the Kruskal's algo.
    def __lt__(self, other):
        return self.weight < other.weight


class Graph:

    def __init__(self, fin, vertexCount):
        self.vertexCount = vertexCount
        self.vertices = []
        self.edges = {}

        for i in range(vertexCount):
            self.vertices.append(Vertex())

        for i in range(vertexCount):
            line = fin.readline().split()
            adjVerticesCount = int(line[0])
            line = line[1:]

            for j in range(adjVerticesCount):
                neighbour = self.vertices[int(line[j*2]) - 1]
                neighbour.indegree += 1

                weight = int(line[j*2 + 1])
                newEdge = Edge()
                newEdge.weight = weight
                newEdge.src = self.vertices[i]
                newEdge.dest = neighbour

                self.vertices[i].adjVertices.append(neighbour)
                self.edges[(self.vertices[i], neighbour)] = newEdge

    def displayVertices(self):
        print("The graph is:-")

        for i in range(self.vertexCount):
            print("Vertex " + self.vertices[i].name, " -->  ", end="")
            adjVerticesCount = len(self.vertices[i].adjVertices)

            for j in range(adjVerticesCount):
                neighbour = self.vertices[i].adjVertices[j]
                weight = self.edges[(self.vertices[i], neighbour)].weight
                print(neighbour.name + "(" + str(weight) + ")", end="")
                if j != adjVerticesCount -1:
                    print(", ", end="")
            print()
        print()

    def displayEdges(self):
        edgeList = list(self.edges.values())

        print("The edges are:-")
        print("Src\tDest\tLabel\tWeight\tType")
        for edge in edgeList:
            print(edge.src.name + "\t" + edge.dest.name + "\t\t" + str(edge.label) + "\t\t" + str(edge.weight) + "\t\t" + str(edge.type))
        print()

    def displayVerticesStatus(self):    # Primarily used for debugging code.
        print("The status of the vertices are:-")

        for i in range(self.vertexCount):
            print(self.vertices[i].name, " : ", self.vertices[i].status)

        print()

    def reset(self):
        for i in range(self.vertexCount):
            self.vertices[i].status = None
            self.vertices[i].colour = None
            self.vertices[i].dfsNum = None
            self.vertices[i].low = None
            self.vertices[i].parent = None

    def revGraph(self):
        self.reset()
        tempEdges = self.edges
        self.edges = {}
        for vertex in self.vertices:
            vertex.revAdjVertices = vertex.adjVertices
            vertex.adjVertices = []
            vertex.indegree = 0

        for vertex in self.vertices:
            for neighbour in vertex.revAdjVertices:
                neighbour.adjVertices.append(vertex)
                vertex.indegree += 1

                edge = tempEdges[(vertex, neighbour)]
                edge.src = neighbour
                edge.dest = vertex
                edge.type = None

                self.edges[(neighbour, vertex)] = edge
            vertex.revAdjVertices = []


# This code has been adapted from: https://github.com/williamfiset/data-structures/tree/master/com/williamfiset/datastructures/unionfind
# Explanation video & playlist on UnionFind: https://www.youtube.com/watch?v=KbFlZYCpONw&list=PLDV1Zeh2NRsBI1C-mR6ZhHTyfoEJWlxvq&index=5
# Employs path compression.
class UnionFind:
    def __init__(self, size):
        if size <= 0:
            raise TypeError("size <= 0 is not allowed")

        # Keeps track of the number of components.
        # Initially, the number of components is equal to the number of vertices.
        self.componentsCount = size

        # Keeps track of the size of each component.
        # Initially, all components have just one element in them, hence their size would be 1
        self.componentSize = [1] * size

        # link[i] points to the parent of i, if link[i] = i then i is a root node
        self.link = []

        # Initially, each vertex is its own parent.
        for i in range(size):
            self.link.append(i)

    # Find which component/set 'v' belongs to; takes amortized constant time.
    # Employs path compression.
    def find(self, v):
        root = v

        # Find the root of the component/set
        while root != self.link[root]:
            root = self.link[root]

        # Compress the path leading back to the root.
        # Doing this operation is called "path compression" and is what gives us amortized time complexity.
        while self.link[v] != root:
            nextNode = self.link[v]
            self.link[v] = root
            v = nextNode

        return root

    def connected(self, v, w):
        return self.find(v) == self.find(w)

    def componentSize(self, v):
        return self.componentSize[self.find(v)]

    # Unify the components/sets containing elements 'v' and 'w'
    def unify(self, v, w):
        root1 = self.find(v)
        root2 = self.find(w)

        # These elements are already in the same group!
        if root1 == root2:
            return

        # Merge smaller component/set into the larger one.
        if self.componentSize[root1] < self.componentSize[root2]:
            self.componentSize[root2] += self.componentSize[root1]
            self.link[root1] = root2
        else:
            self.componentSize[root1] += self.componentSize[root2]
            self.link[root2] = root1

        # Since the roots found are different we know that the number of components/sets has decreased by one
        self.componentsCount -= 1

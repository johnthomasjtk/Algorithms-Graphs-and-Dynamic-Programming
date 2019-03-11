# This piece of source code has been inspired by Padmamala ma'am's notes and geeksforgeeks.org.
# Link: https://www.geeksforgeeks.org/strongly-connected-components/
# Status of this code: Rough; works on all inputs, but still need to clean it.
import collections


# Padmamala ma'am had taught us about post-order numbering where we assign a discovery number to a vertex at the very end,
# i.e., after it has been explored completely. And then, we should reverse the graph and start with the vertex with the highest
# post-order number. The same effect can be achieved using a stack. Although both approaches are equally good (probably the
# post-order numbering is slightly better as we don't have to create a stack and thus save space) I found the stack approach
# a little easier to imagine and code; hence this variant.
# This function creates a stack of vertices where each vertex is pushed after it has been completely explored. It achieves the
# same goal as post-order numbering. After reversing the graph, we keep popping off vertices to find out the SSCs.
# The graph, a source vertex and an empty stack are taken as input. The final stack is stored in the stack object sent as input
def createDFSStack(graph, v, stack):
    try:                                # Python does not support static variables as C does, this is a small bodge
                                        # to emulate the same effect
        createDFSStack.count += 1       # try incrementing the function counter variable..
    except AttributeError:              # if it has not yet been defined, then Python will throw an error..
        createDFSStack.count = 0        # initialise the counter. It is used to assign a discovery number to each vertex

    v.dfsNum = createDFSStack.count     # assign the next discovery number to the current vertex 'v'
    v.status = "Visited"                # Mark 'v' as Visited

    for neighbour in v.adjVertices:                     # for each neighbour of v, do the following..
        if neighbour.status != "Visited":               # if the neighbour is unvisited..
            createDFSStack(graph, neighbour, stack)     # call the same function on the neighbouring vertex

    stack.append(v)                                     # push the vertex into the stack at the very end

    if v.dfsNum == 0:                                   # If this is the first instance of the function..
        for vertex in graph.vertices:
            if vertex.status != "Visited":              # ..then check if any of the nodes have not yet been visited..
                createDFSStack(graph, vertex, stack)    # if so, run DFS on them..

# Performs a basic DFS on the graph object starting from vertex 'v' and writes the output to file object fout
def basicDFS(graph, v, fout):
    v.status = "Visited"                        # Mark vertex 'v' as visited
    fout.write(v.name + " ")
    for neighbour in v.adjVertices:             # for each neighbour..
        if neighbour.status != "Visited":       # if it has not yet been visited..
            basicDFS(graph, neighbour, fout)    # run DFS on them..


# Finds the strongly connected components. Input: the reversed graph, the stack containing vertices in order of
# exploration-completion time and the output file object
def findSSCs(graph, stack, fout):
    while len(stack) != 0:              # continue until the stack is empty
        v = stack.pop()                 # pop the vertex 'v' on top of the stack
        if v.status != "Visited":       # if it has not yet been visited..
            fout.write("{")             # then, it is a new component..
            basicDFS(graph, v, fout)    # run a basic DFS starting from that vertex
            fout.write("}\t")           # after the DFS call, we know all vertices of that component have been explored


def SSCDriver(graph, fout):                             # A driver function to find out the SSCs
    stack = collections.deque()                         # Create an empty stack
    createDFSStack(graph, graph.vertices[0], stack)     # create a stack of vertices which achieves the same goal as
    graph.revGraph()                                    # post-order numbering..and reverse the graph
    findSSCs(graph, stack, fout)                        # finally, find out the strongly connected components

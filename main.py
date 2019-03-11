# This code has been successfully tested on Python 3.x. Will also run on Python 2.x; but the following functions need to be commented out in header.py:-
# Graph.displayVertices(), Graph.displayEdges() and Graph.displayVerticesStatus().
# These 3 functions are solely used for debugging purposes; and have not been invoked in the final version of the code;
# so it will not create an issue if these 3 functions are commented out.
# Note: Multi line comments in Python begin and end with triple single quotes.
import sys
import header
import TopologicalSort
import dijkstra
import kruskal
import FindArticulationPoints
import StronglyConnectedComponents


if len(sys.argv) != 2:                              # if the output file is not mentioned on the command line, then display the usage
    print("Usage:-\npython3 main.py <output-file>")
    exit()

fin = open(header.INP_FILE, "r")                    # open the input file
fout = open(sys.argv[1], "w")                       # open the output file specified on the command line

g = header.Graph(fin, header.NUMBER_OF_VERTICES)    # create a graph with the number of vertices equal to the constant
                                                    # defined in header.py. It is set to 7.
TopologicalSort.topologicalSort(g, fout)            # perform topological sort, and write output to the output file object
g.resetVertexNEdge()                                # reset the counters of classes Vertex and Edge. Otherwise the next
                                                    # graph would have vertex names starting from where the current graph's
                                                    # names ended.

fout.write("\nFor the second graph:\nShortest paths for the first vertex:\n\n")     # Writing a message to the out file
g = header.Graph(fin, header.NUMBER_OF_VERTICES)                                    # Read in the next graph
dijkstra.dijkstra(g, g.vertices[0], fout)                                           # perform Dijkstra's algo on the graph
g.resetVertexNEdge()                                # same reason as above; if we don't do this, the next graph's vertices
                                                    # will have names starting from where the current graph's names ended

g = header.Graph(fin, header.NUMBER_OF_VERTICES)    # read the next graph
kruskal.kruskal(g, fout)                            # perform Kruskal's algo
g.resetVertexNEdge()                                # reset counters of classes Vertex and Edge; reason mentioned before

fout.write("\nFor the fourth graph, the articulation points are:\n")
g = header.Graph(fin, header.NUMBER_OF_VERTICES)                # read the next graph..
source = g.vertices[int(fin.readline().split()[0]) - 1]         # ..and the source; i.e. the root of the DFS tree
FindArticulationPoints.findArticulationPoints(g, source, fout)  # find the articulation points
g.resetVertexNEdge()                                            # reset counters of classes Vertex and Edge; reason mentioned before

fout.write("\nFor the fifth graph, the articulation points are:\n")
FindArticulationPoints.findArticulationPoints.counter = None    # need to reset this counter as it is used to assign discovery numbers to the vertices
g = header.Graph(fin, header.NUMBER_OF_VERTICES)                # read in the next graph..
source = g.vertices[int(fin.readline().split()[0]) - 1]         # ..and the source; i.e. the root of the DFS tree
FindArticulationPoints.findArticulationPoints(g, source, fout)  # find the articulation points
g.resetVertexNEdge()                                            # reset counters of classes Vertex and Edge; reason mentioned before

fout.write("The strongly connected components of the sixth graph are:\n")
g = header.Graph(fin, header.NUMBER_OF_VERTICES)            # read in the sixth graph
StronglyConnectedComponents.SSCDriver(g, fout)              # find out the Strongly connected components

fin.close()                                                 # close the input..
fout.close()                                                # and output files..

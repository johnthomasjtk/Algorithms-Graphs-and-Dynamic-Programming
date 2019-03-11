# Graphs
Graph algorithms discussed in class

### Format of .DAT files (i.e. how the input is specified)
For these .py files, the format of the input (in the DAT file) is slightly different from how it is described in the Questions file that we have been given.

_Description_

The first line in a DAT file contains an integer N, the number of vetices in the graph. N lines follow.\
Each line i, contains an integer D, which denotes the number of vertices adjacent to vertex Vi. D pairs of integers follow on that line.\
In each pair, (Vj, W), Vj denotes the adjacent vertex number and W denotes the weight of that edge.\
For example:-\
3\
2&nbsp;&nbsp;&nbsp;&nbsp;2 1&nbsp;&nbsp;&nbsp;&nbsp;3 5\
0\
1&nbsp;&nbsp;&nbsp;&nbsp;1 6


The first integer N = 3, means that there are three vertices in the graph (let's say A, B and C). 3 lines follow.

The first integer on a line (D) denotes the number of adjacent vertices. So, vertex A has 2 adjacent vertices. 2 pairs of integers follow on that line.
The first integer in the first pair (2 1) indicates the vertex number which is adjacent to A. Since A is vertex 1, B is vertex 2 and C is vertex 3, the number 2 indicates that there is an edge from A to B. The weight of the edge is 1.

Similarly, the next pair (3 5) indicates that there is an edge from A to C (vertex number 3) with an edge weight of 5.

Vertex B does not have any adjacent vertices (the outdegree of B is 0).

Vertex C has only one edge going out of it; which is indicated by the first number on the line. 1 pair of integer follow on the same line.\
The first integer in the pair denotes the vertex number which is adjacent to the current vertex and the second integer indicates the weight of that edge. 1 corresponds to vertex A, so, this means that there is an edge from C to A and the edge weight is 6.

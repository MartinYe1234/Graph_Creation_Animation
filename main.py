import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from math import sin, cos, pi
fig = plt.figure()
plt.rcParams['figure.figsize'] = (15,15)

"""Create networkx graph to visualise"""
g = nx.Graph()

N = 0
E = 0
nodes = []
edges = []
labels = []

graph = [[]]

def create_graph(n=2, e=1):
	global N, E, graph
	"""Function that generates a graph with n nodes that are
	randomly connected to at least one other node using e distinct edges.

	Parameters
	----------
	n : int
		number of nodes in the graph, optional
		(default = 2)
	e : int
		number of bi-directional edges in the graph, optional
		(default = 1)
	"""
	N = n
	E = e

	nodes = []
	edges = []

	# Constructs an adjacency matrix
	graph = [[0 for i in range(n)] for j in range(n)]

	# add nodes to graph
	for i in range(n):
		nodes.append(i)

	# add edges - connect random unique pairs of vertices
	while e > 0:
		i = randint(0, N-1)
		j = randint(0, N-1)
		if graph[i][j] == 0 and graph[j][i] == 0 and i != j:
			edges.append((i, j))
			graph[i][j] = 1
			graph[j][i] = 1
			e -= 1
	print(graph)
	#used for networkx
	g.add_nodes_from(nodes)
	g.add_edges_from(edges)
	print("edges:", edges)

"""Visualize graphs using networkx graphs"""

position = {}

create_graph(10,15)


#position nodes in a circle
for node in g.nodes():
	x_pos = cos(node*(2*pi/(max(g.nodes())+1)))
	y_pos = sin(node*(2*pi/(max(g.nodes())+1)))
	position[node] = (x_pos, y_pos)

graph1 = nx.draw(g, position , with_labels = True, width = 2, node_size = 500, font_size = 12)

plt.show(graph1)

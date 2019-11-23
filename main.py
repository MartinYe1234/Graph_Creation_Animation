import networkx as nx
import matplotlib.pyplot as plt
from random import randint, gauss
from math import sin, cos, pi

"""Create networkx graph to visualise"""
g = nx.Graph()
n= 10
p = {i: (gauss(0, 0.1), gauss(0,0.1)) for i in range(n)}
G = nx.random_geometric_graph(n,0.2,pos=p)
position = nx.get_node_attributes(G, 'pos')
edges = G.edges
nodes = G.nodes
adj_list = {}
for node in nodes:
	adj_list[node] = []
for edge in edges:
	node = edge[0]
	connected_node = edge[1]
	adj_list[node].append(connected_node)
	adj_list[connected_node].append(node)

print(adj_list)
node_col = 'blue'
plt.figure(figsize=(16, 9))
nx.draw_networkx_edges(G, position, alpha=0.5)
nx.draw_networkx_nodes(G, position, node_size=110,node_color=node_col)
nx.draw_networkx_labels(G,position, font_color='white', font_size=10)


plt.show()



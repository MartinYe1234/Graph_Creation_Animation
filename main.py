import networkx as nx
import matplotlib.pyplot as plt
from random import randint, gauss
from math import sin, cos, pi

"""Create networkX graph to visualise"""

# number of nodes
n = 10
# generate positions of nodes
p = {i: (gauss(0, 0.12), gauss(0, 0.12)) for i in range(n)}
G = nx.random_geometric_graph(n, 0.185, pos=p)
position = nx.get_node_attributes(G, 'pos')

edges = G.edges
nodes = G.nodes
# labels for edge weights
edge_weights_labels = {}
# create adjacency list
adj_list = {}
# fill adjacency list
for node in nodes:
    adj_list[node] = []
for edge in edges:
    node = edge[0]
    connected_node = edge[1]
    # generate weights by calculating distance between the two nodes
    x1, y1 = position[node][0], position[node][1]
    x2, y2 = position[connected_node][0], position[connected_node][1]
    weight = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5
    adj_list[node].append([connected_node, weight])
    adj_list[connected_node].append([node, weight])
    # fill edge_weight_labels
    if edge not in edge_weights_labels:
        edge_weights_labels[edge] = round(weight,3)

print("edge weights:", edge_weights_labels)
print("adj list:", adj_list)
node_col = 'blue'
plt.figure(figsize=(15, 9))
nx.draw_networkx_edges(G, position, alpha=0.5)
nx.draw_networkx_edge_labels(G, pos=position, edge_labels=edge_weights_labels, font_size=6, label_pos=0.5)
nx.draw_networkx_nodes(G, position, node_size=150, node_color=node_col)
nx.draw_networkx_labels(G, position, font_color='white', font_size=11)

plt.show()

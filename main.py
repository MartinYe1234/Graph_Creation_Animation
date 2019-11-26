import networkx as nx
import matplotlib.pyplot as plt
from random import randint, gauss
from math import sin, cos, pi

"""Create networkX graph to visualise"""

# number of nodes
n = 10
# generate positions of nodes
p = {i: (gauss(0, 0.12), gauss(0, 0.12)) for i in range(n)}
G = nx.random_geometric_graph(n, 0.165, pos=p)
position = nx.get_node_attributes(G, 'pos')
print(position)
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
    # the weight is the distance between the two connected nodes multiplied by 100 and rounded to 1 decimal place
    weight = round((((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5) * 100, 1)
    adj_list[node].append([connected_node, weight])
    adj_list[connected_node].append([node, weight])
    # fill edge_weight_labels
    if edge not in edge_weights_labels:
        edge_weights_labels[edge] = weight

print("edge weights:", edge_weights_labels)
print("adj list:", adj_list)


def dijsktra(adjacency_list, target, start):
    """

    Parameters
    ----------
    adjacency_list : dict
    target : int
    start : int

    Returns
    -------

    """
    # keep track of unvisited nodes
    not_visited = [node for node in nodes]
    # begin by initialising all distances from start node as being infinity
    distances = {}
    for node in not_visited:
        if node != start:
            distances[node] = float('inf')
        else:
            distances[node] = 0


node_col = 'blue'
plt.figure(figsize=(14, 8))
nx.draw_networkx_edges(G, position, alpha=0.5)
nx.draw_networkx_edge_labels(G, pos=position, edge_labels=edge_weights_labels, font_size=7, bbox=dict(alpha=0))
nx.draw_networkx_nodes(G, position, node_size=150, node_color=node_col)
nx.draw_networkx_labels(G, position, font_color='white', font_size=11)
plt.tight_layout()
plt.show()

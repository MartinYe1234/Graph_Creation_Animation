import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as mpa
from random import gauss
import numpy as np

np.random.seed(0)
"""Create networkX graph to visualise"""
# animation is based off of the concept from:
# https://stackoverflow.com/questions/43646550/how-to-use-an-update-function-to-animate-a-networkx-graph-in-matplotlib-2-0-0?rq=1

# number of nodes
n = 10
# generate positions of nodes
p = {i: (np.random.normal(0, 0.12), np.random.normal(0, 0.12)) for i in range(n)}
G = nx.random_geometric_graph(n, 0.195, pos=p)
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
        contains list of nodes adjacent to a certain node which is the key, each node has a weight attached to it
    target : int
        target node
    start : int
        starting node

    Returns
    -------
    """
    # begin by initialising all distances from start node as being infinity
    distances = {}
    for node in nodes:
        if node != start:
            distances[node] = float('inf')
        else:
            distances[node] = 0
    queue = []
    # while all nodes aren't visited
    while len(queue) > 0:
        # find node with smallest distance from start
        current_node, current_distance = queue[0]


"""
Animation created using matplotlib animation function
"""


def update(itr):
    plt.clf()
    node_col = 'green'
    if itr%2 == 0:
        node_col = 'red'
    nx.draw_networkx_edges(G, position, alpha=0.5)
    nx.draw_networkx_nodes(G, position, node_size=250, node_color=node_col)
    plt.tight_layout()




fig = plt.figure(figsize=(14, 8))

ani = mpa.FuncAnimation(fig, update, frames= 6, interval= 200,repeat=True)
plt.show()

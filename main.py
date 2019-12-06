import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as mpa
from random import gauss
import numpy as np

np.random.seed(7)
"""Create networkX graph to visualise"""
# animation is based off of the concept from:
# https://stackoverflow.com/questions/43646550/how-to-use-an-update-function-to-animate-a-networkx-graph-in-matplotlib-2-0-0?rq=1

# number of nodes
n = 10
# generate positions of nodes
p = {i: (np.random.normal(0, 0.12), np.random.normal(0, 0.12)) for i in range(n)}
G = nx.random_geometric_graph(n, 0.172, pos=p)
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


def bfs(graph, start):
    """
    Runs bfs on a graph with the purpose of visualising it

    Parameters
    ----------
    graph : dict
        Dictionary with nodes as keys and values as the adjacent nodes and weights as values
    start : int
        Starting node

    Returns
    -------
    order_visited : list
        list containing order of nodes visited
    """
    queue = []
    bfs_visited = [0 for i in range(len(adj_list.keys()))]
    queue.append(start)
    # mark as visited
    bfs_visited[start] = 1
    # store order of visited nodes
    order_visited = []
    # while there is something in the queue
    while queue:
        # for each adjacent node to the current node
        for neighbour in graph[queue[0]]:
            adjacent_node = neighbour[0]
            # if the vertex has not been visited yet
            if bfs_visited[adjacent_node] == 0:
                order_visited.append(adjacent_node)
                # add adjacent (neighbour) node to queue
                queue.append(adjacent_node)
                # mark as visited
                bfs_visited[adjacent_node] = 1
        queue.pop(0)
    return order_visited


"""
Animation created using matplotlib animation function
"""


def update(itr):
    plt.clf()
    # bfs
    node_col = 'blue'
    edge_col = 'black'
    # selected edges
    targeted_edges = []
    targeted_nodes = []

    order = bfs(adj_list, 0)

    targeted_nodes.append(order[itr%len(order)])

    nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
    nx.draw_networkx_edges(G, position, edgelist=targeted_edges, width=4, edge_color=edge_col, alpha=1)
    nx.draw_networkx_nodes(G, position, node_size=250, node_color=node_col)
    nx.draw_networkx_nodes(G, position, nodelist=targeted_nodes, node_size=2500, node_color=node_col)
    nx.draw_networkx_labels(G, position)
    plt.tight_layout()


fig, ax = plt.subplots(figsize=(14, 7))
ani = mpa.FuncAnimation(fig, update, interval=300, repeat=True)
plt.show()
